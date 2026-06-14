from __future__ import annotations

import unittest

from philosophers.states import PhilosopherState
from philosophers.table import DiningTable
from synchronization.forks import Fork
from synchronization.solution_version import SolutionSimulation


class SimulationSmokeTests(unittest.TestCase):
    def test_states_include_required_values(self) -> None:
        self.assertEqual(PhilosopherState.THINKING.value, "THINKING")
        self.assertEqual(PhilosopherState.HUNGRY.value, "HUNGRY")
        self.assertEqual(PhilosopherState.WAITING.value, "WAITING")
        self.assertEqual(PhilosopherState.EATING.value, "EATING")
        self.assertEqual(PhilosopherState.RELEASING.value, "RELEASING")

    def test_fork_uses_lock(self) -> None:
        fork = Fork(0)
        self.assertTrue(hasattr(fork, "lock"))
        self.assertTrue(fork.lock.acquire(blocking=False))
        fork.release()

    def test_table_builds_custom_number_of_philosophers(self) -> None:
        table = DiningTable(num_philosophers=3)
        self.assertEqual(table.num_philosophers, 3)
        self.assertEqual(len(table.forks), 3)
        self.assertEqual(len(table.get_states_snapshot()), 3)

    def test_solution_uses_waiter_limit(self) -> None:
        simulation = SolutionSimulation(num_philosophers=5)
        self.assertEqual(simulation.waiter._value, 4)


if __name__ == "__main__":
    unittest.main()
