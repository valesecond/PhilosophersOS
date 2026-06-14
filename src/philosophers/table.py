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
from src.utils.constants import STATUS_READY


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

    def alert_deadlock(self) -> None:
        self.statistics.mark_deadlock()
        self.stop_event.set()
        if self.logger is not None:
            self.logger.deadlock_alert("DEADLOCK DETECTADO")

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
        )
