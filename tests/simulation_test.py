from __future__ import annotations

import unittest

from src.philosophers.states import PhilosopherState
from src.philosophers.table import DiningTable
from src.synchronization.forks import Fork
from src.synchronization.solution_version import run_solution_version
from src.utils.config import SimulationConfig


class SimulationSmokeTests(unittest.TestCase):
    def test_states_include_required_values(self) -> None:
        self.assertEqual(PhilosopherState.THINKING.value, "PENSANDO")
        self.assertEqual(PhilosopherState.HUNGRY.value, "COM FOME")
        self.assertEqual(PhilosopherState.WAITING.value, "ESPERANDO")
        self.assertEqual(PhilosopherState.EATING.value, "COMENDO")
        self.assertEqual(PhilosopherState.RELEASING.value, "LIBERANDO")

    def test_fork_uses_lock(self) -> None:
        fork = Fork(0)
        self.assertTrue(hasattr(fork, "lock"))
        self.assertTrue(fork.lock.acquire(blocking=False))
        fork.release()

    def test_table_builds_custom_number_of_philosophers(self) -> None:
        table = DiningTable(SimulationConfig(num_philosophers=3, cycles=1))
        self.assertEqual(table.num_philosophers, 3)
        self.assertEqual(len(table.forks), 3)
        self.assertEqual(len(table.state_snapshot()), 3)

    def test_solution_uses_waiter_limit(self) -> None:
        result = run_solution_version(
            SimulationConfig(num_philosophers=5, cycles=1, simulation_speed=10.0),
            wait_at_end=False,
            clear_before=False,
        )
        self.assertEqual(result["deadlocks"], 0)
        self.assertGreaterEqual(result["meals"], 1)


if __name__ == "__main__":
    unittest.main()
