from __future__ import annotations

import random
import threading
import time
from dataclasses import dataclass

from src.philosophers.states import PhilosopherState
from src.utils.config import SimulationConfig


@dataclass(slots=True)
class PhilosopherActivity:
    philosopher_id: int
    state: PhilosopherState = PhilosopherState.THINKING
    resources: str = "-"


class Philosopher(threading.Thread):
    """Filósofo representado como thread Python (threading.Thread).

    Cada filósofo executa um ciclo contínuo de pensar, ficar com fome,
    adquirir garfos, comer e liberar recursos compartilhados.
    """

    def __init__(
        self,
        philosopher_id: int,
        table,
        left_fork,
        right_fork,
        *,
        strategy: str,
        config: SimulationConfig,
        waiter: threading.Semaphore | None = None,
        daemon: bool = True,
    ) -> None:
        super().__init__(name=f"Philosopher-{philosopher_id}", daemon=daemon)
        self.philosopher_id = philosopher_id
        self.table = table
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.strategy = strategy
        self.config = config
        # MECANISMO DE SINCRONIZAÇÃO: threading.Semaphore (garçom)
        # Limita quantos filósofos entram na região crítica simultaneamente.
        self.waiter = waiter

    def run(self) -> None:
        try:
            self.table.start_barrier.wait(timeout=5)
        except threading.BrokenBarrierError:
            pass

        for _ in range(self.config.cycles):
            if self.table.stop_event.is_set():
                break

            self._think()
            self._become_hungry()

            if self.strategy == "solution" and self.waiter is not None:
                self.table.update_state(self.philosopher_id, PhilosopherState.WAITING, "Esperando garçom")
                self.waiter.acquire()

            self._enter_critical_region()
            self._eat()
            self._release_resources()

            if self.strategy == "solution" and self.waiter is not None:
                self.waiter.release()

        self.table.update_state(self.philosopher_id, PhilosopherState.THINKING, "Ciclo concluído")

    def _sleep_scaled(self, duration: float) -> None:
        time.sleep(duration / self.config.simulation_speed)

    def _think(self) -> None:
        self.table.update_state(self.philosopher_id, PhilosopherState.THINKING, "Pensando")
        self._sleep_scaled(random.uniform(self.config.thinking_time * 0.75, self.config.thinking_time * 1.25))

    def _become_hungry(self) -> None:
        self.table.update_state(self.philosopher_id, PhilosopherState.HUNGRY, "Com fome")

    def _enter_critical_region(self) -> None:
        # ===================================================
        # REGIÃO CRÍTICA
        # Acesso aos recursos compartilhados (garfos).
        #
        # Neste trecho, cada filósofo disputa dois Locks simultaneamente.
        # A exclusão mútua é garantida por threading.Lock em cada garfo.
        # O deadlock ocorre quando todos seguram o garfo esquerdo e
        # aguardam indefinidamente o garfo direito — espera circular.
        # ===================================================

        self.table.update_state(self.philosopher_id, PhilosopherState.WAITING, "Pegando garfo esquerdo")
        self.left_fork.acquire(self.philosopher_id)
        self.table.register_resource(self.philosopher_id, self.left_fork.label())

        if self.strategy == "deadlock":
            # Barrier força todos a pegarem o garfo esquerdo ao mesmo tempo,
            # maximizando o risco de deadlock na versão vulnerável.
            try:
                self.table.deadlock_barrier.wait(timeout=5)
            except threading.BrokenBarrierError:
                pass

        self.table.update_state(self.philosopher_id, PhilosopherState.WAITING, "Pegando garfo direito")
        self.right_fork.acquire(self.philosopher_id)
        self.table.register_resource(
            self.philosopher_id,
            f"{self.left_fork.label()} + {self.right_fork.label()}",
        )

    def _eat(self) -> None:
        self.table.update_state(self.philosopher_id, PhilosopherState.EATING, "Comendo")
        self.table.statistics.mark_meal()
        self._sleep_scaled(random.uniform(self.config.eating_time * 0.75, self.config.eating_time * 1.25))

    def _release_resources(self) -> None:
        self.table.update_state(self.philosopher_id, PhilosopherState.RELEASING, "Liberando recursos")
        self.right_fork.release()
        self.left_fork.release()
        self.table.register_resource(self.philosopher_id, "-")
