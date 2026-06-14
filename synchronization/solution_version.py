from __future__ import annotations

import threading

from philosophers.table import DiningTable
from utils.config import NUM_PHILOSOPHERS, SOLUTION_MAX_CONTENDERS


class SolutionSimulation:
    def __init__(self, num_philosophers: int = NUM_PHILOSOPHERS) -> None:
        self.table = DiningTable(num_philosophers)
        permit_count = min(SOLUTION_MAX_CONTENDERS, max(1, num_philosophers - 1))
        self.waiter = threading.Semaphore(permit_count)

    def run(self) -> None:
        self.table.logger.header("Versao com Solucao")
        self.table.logger.system(
            "Um semaforo atua como garcom e permite apenas parte dos filosofos na regiao critica."
        )

        philosophers = self.table.create_philosophers(
            version="solution",
            waiter=self.waiter,
            daemon=False,
        )

        for philosopher in philosophers:
            philosopher.start()

        for philosopher in philosophers:
            philosopher.join()

        self.table.logger.success("Simulacao encerrada com sucesso.")


def run_solution_version(num_philosophers: int = NUM_PHILOSOPHERS) -> None:
    SolutionSimulation(num_philosophers).run()
