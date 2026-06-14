from __future__ import annotations

import threading
import time
from collections import OrderedDict
from dataclasses import dataclass

from rich.table import Table as RichTable

from src.monitors.statistics_monitor import SimulationStatistics
from src.philosophers.philosopher import Philosopher, PhilosopherActivity
from src.philosophers.states import PhilosopherState
from src.synchronization.forks import Fork
from src.utils.config import SimulationConfig
from src.utils.constants import STATUS_READY, STATUS_RUNNING, STATUS_STOPPED


@dataclass(slots=True)
class DeadlockInfo:
    blocked_philosophers: list[int]
    waiting_resources: dict[int, str]
    wait_time: float

    def waiting_resources_summary(self) -> str:
        if not self.waiting_resources:
            return "-"
        parts = [f"P{pid}→{resource}" for pid, resource in sorted(self.waiting_resources.items())]
        return " | ".join(parts)


@dataclass(slots=True)
class TableSnapshot:
    activities: list[PhilosopherActivity]
    elapsed: float
    meals: int
    deadlocks: int
    active_threads: int
    strategy: str
    status: str = STATUS_READY


class DiningTable:
    """Mesa compartilhada que coordena filósofos, garfos e estatísticas.

    MECANISMOS DE SINCRONIZAÇÃO utilizados:
    - threading.Lock (state_lock): protege o estado compartilhado dos filósofos
    - threading.Lock (progress_lock): protege timestamp de progresso
    - threading.Barrier (start_barrier): sincroniza início simultâneo
    - threading.Barrier (deadlock_barrier): força cenário de deadlock
    - threading.Event (stop_event): sinaliza encerramento da simulação
    """

    def __init__(self, config: SimulationConfig) -> None:
        self.config = config
        self.num_philosophers = config.num_philosophers
        self.stop_event = threading.Event()
        self.state_lock = threading.Lock()
        self.progress_lock = threading.Lock()
        self.start_time = time.perf_counter()
        self.last_progress = self.start_time
        self.statistics = SimulationStatistics(start_time=self.start_time)
        self.forks = [Fork(index) for index in range(self.num_philosophers)]
        self.start_barrier = threading.Barrier(self.num_philosophers)
        self.deadlock_barrier = threading.Barrier(self.num_philosophers)
        self._states: OrderedDict[int, PhilosopherActivity] = OrderedDict(
            (index, PhilosopherActivity(index)) for index in range(self.num_philosophers)
        )
        self.strategy = "-"
        self.logger = None
        self.deadlock_info: DeadlockInfo | None = None
        self.status = STATUS_READY

    def assign_logger(self, logger) -> None:
        self.logger = logger

    def update_state(self, philosopher_id: int, state: PhilosopherState, message: str) -> None:
        with self.state_lock:
            self._states[philosopher_id].state = state
        self.mark_progress()
        if self.logger is not None:
            self.logger.philosopher_line(philosopher_id, state.value, message)

    def register_resource(self, philosopher_id: int, resources: str) -> None:
        with self.state_lock:
            self._states[philosopher_id].resources = resources
        self.mark_progress()
        if self.logger is not None and hasattr(self.logger, "register_resource"):
            self.logger.register_resource(philosopher_id, resources)

    def state_snapshot(self) -> dict[int, PhilosopherState]:
        with self.state_lock:
            return {pid: activity.state for pid, activity in self._states.items()}

    def activity_snapshot(self) -> list[PhilosopherActivity]:
        with self.state_lock:
            return [PhilosopherActivity(activity.philosopher_id, activity.state, activity.resources) for activity in self._states.values()]

    def mark_progress(self) -> None:
        with self.progress_lock:
            self.last_progress = time.perf_counter()

    def seconds_since_progress(self) -> float:
        with self.progress_lock:
            return time.perf_counter() - self.last_progress

    def alert_deadlock(self, wait_time: float) -> None:
        self.statistics.mark_deadlock()
        self.status = STATUS_STOPPED
        snapshot = self.activity_snapshot()
        blocked = [activity.philosopher_id for activity in snapshot if activity.state == PhilosopherState.WAITING]
        waiting_resources = {
            activity.philosopher_id: activity.resources
            for activity in snapshot
            if activity.state == PhilosopherState.WAITING
        }
        self.deadlock_info = DeadlockInfo(
            blocked_philosophers=blocked,
            waiting_resources=waiting_resources,
            wait_time=wait_time,
        )
        self.stop_event.set()
        if self.logger is not None:
            self.logger.deadlock_alert(self.deadlock_info)

    def mark_running(self) -> None:
        self.status = STATUS_RUNNING

    def create_philosophers(self, *, strategy: str, waiter=None) -> list[Philosopher]:
        self.strategy = strategy
        philosophers: list[Philosopher] = []
        for philosopher_id in range(self.num_philosophers):
            philosopher = Philosopher(
                philosopher_id,
                self,
                self.forks[philosopher_id],
                self.forks[(philosopher_id + 1) % self.num_philosophers],
                strategy=strategy,
                config=self.config,
                waiter=waiter,
            )
            philosophers.append(philosopher)
        return philosophers

    def active_threads(self) -> int:
        return sum(1 for thread in threading.enumerate() if thread.name.startswith("Philosopher-"))

    def render_activity_table(self) -> RichTable:
        table = RichTable(title="Monitoramento em Tempo Real", expand=True, header_style="bold cyan")
        table.add_column("Filosofo", style="bold white", justify="center")
        table.add_column("Estado", style="bold yellow", justify="center")
        table.add_column("Recursos", style="bold green", justify="center")
        for activity in self.activity_snapshot():
            table.add_row(f"P{activity.philosopher_id}", activity.state.value, activity.resources)
        return table

    def snapshot(self) -> TableSnapshot:
        stats = self.statistics.snapshot(self.active_threads(), self.strategy)
        return TableSnapshot(
            activities=self.activity_snapshot(),
            elapsed=float(stats["elapsed"]),
            meals=int(stats["meals"]),
            deadlocks=int(stats["deadlocks"]),
            active_threads=int(stats["active_threads"]),
            strategy=str(stats["strategy"]),
            status=self.status,
        )
