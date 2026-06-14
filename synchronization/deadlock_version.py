from __future__ import annotations

from philosophers.table import DiningTable
from synchronization.deadlock_monitor import DeadlockMonitor
from utils.config import NUM_PHILOSOPHERS


class DeadlockSimulation:
    def __init__(self, num_philosophers: int = NUM_PHILOSOPHERS) -> None:
        self.table = DiningTable(num_philosophers)

    def run(self) -> None:
        self.table.logger.header("Versao com Deadlock")
        self.table.logger.system(
            "Todos os filosofos pegam primeiro o garfo esquerdo e depois tentam pegar o direito."
        )
        self.table.logger.system("Isso pode provocar espera circular e deadlock.")

        philosophers = self.table.create_philosophers(version="deadlock", daemon=True)
        monitor = DeadlockMonitor(self.table)

        for philosopher in philosophers:
            philosopher.start()

        monitor.start()
        monitor.join()
        self.table.stop_event.set()


def run_deadlock_version(num_philosophers: int = NUM_PHILOSOPHERS) -> None:
    DeadlockSimulation(num_philosophers).run()
