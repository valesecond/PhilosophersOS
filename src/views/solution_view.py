from __future__ import annotations

from src.synchronization.solution_version import run_solution_version
from src.utils.config import SimulationConfig


class SolutionView:
    def show(self, config: SimulationConfig) -> None:
        run_solution_version(config)
