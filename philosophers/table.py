from __future__ import annotations

import threading
import time
from typing import Dict, List

from philosophers.philosopher import Philosopher
from philosophers.states import PhilosopherState
from synchronization.forks import Fork
from utils.config import NUM_PHILOSOPHERS, SIMULATION_CYCLES
from utils.logger import SimulationLogger


class DiningTable:
    def __init__(self, num_philosophers: int = NUM_PHILOSOPHERS) -> None:
        self.num_philosophers = num_philosophers
        self.logger = SimulationLogger()
        self.stop_event = threading.Event()
        self.state_lock = threading.Lock()
        self.progress_lock = threading.Lock()
        self.start_barrier = threading.Barrier(num_philosophers)
        self.deadlock_barrier = threading.Barrier(num_philosophers)
        self.forks: List[Fork] = [Fork(index) for index in range(num_philosophers)]
        self.states: Dict[int, PhilosopherState] = {
            index: PhilosopherState.THINKING for index in range(num_philosophers)
        }
        self.last_progress = time.monotonic()

    def left_fork(self, philosopher_id: int) -> Fork:
        return self.forks[philosopher_id]

    def right_fork(self, philosopher_id: int) -> Fork:
        return self.forks[(philosopher_id + 1) % self.num_philosophers]

    def set_state(self, philosopher_id: int, state: PhilosopherState) -> None:
        with self.state_lock:
            self.states[philosopher_id] = state
        self.logger.state_change(philosopher_id, state)
        self.mark_progress()

    def get_states_snapshot(self) -> Dict[int, PhilosopherState]:
        with self.state_lock:
            return dict(self.states)

    def all_waiting(self) -> bool:
        snapshot = self.get_states_snapshot()
        return all(state == PhilosopherState.WAITING for state in snapshot.values())

    def mark_progress(self) -> None:
        with self.progress_lock:
            self.last_progress = time.monotonic()

    def time_since_progress(self) -> float:
        with self.progress_lock:
            return time.monotonic() - self.last_progress

    def create_philosophers(
        self,
        *,
        version: str,
        waiter=None,
        cycles: int = SIMULATION_CYCLES,
        daemon: bool = False,
    ) -> List[Philosopher]:
        philosophers: List[Philosopher] = []
        for philosopher_id in range(self.num_philosophers):
            philosopher = Philosopher(
                philosopher_id,
                self,
                self.left_fork(philosopher_id),
                self.right_fork(philosopher_id),
                version=version,
                waiter=waiter,
                cycles=cycles,
                daemon=daemon,
            )
            philosophers.append(philosopher)
        return philosophers
