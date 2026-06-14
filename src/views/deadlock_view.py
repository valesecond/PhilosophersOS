from __future__ import annotations

from src.synchronization.deadlock_version import run_deadlock_version
from src.utils.config import SimulationConfig


class DeadlockView:
    def show(self, config: SimulationConfig) -> None:
        run_deadlock_version(config)
