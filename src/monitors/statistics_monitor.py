from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field


@dataclass(slots=True)
class SimulationStatistics:
    start_time: float = field(default_factory=time.perf_counter)
    meals: int = 0
    deadlocks: int = 0
    lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def mark_meal(self) -> None:
        with self.lock:
            self.meals += 1

    def mark_deadlock(self) -> None:
        with self.lock:
            self.deadlocks += 1

    def snapshot(self, active_threads: int, strategy: str) -> dict[str, float | int | str]:
        with self.lock:
            elapsed = time.perf_counter() - self.start_time
            return {
                "elapsed": elapsed,
                "meals": self.meals,
                "deadlocks": self.deadlocks,
                "active_threads": active_threads,
                "strategy": strategy,
            }
