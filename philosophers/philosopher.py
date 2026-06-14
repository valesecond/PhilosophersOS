from __future__ import annotations

import random
import threading
import time

from philosophers.states import PhilosopherState
from utils.config import EATING_TIME, SIMULATION_CYCLES, THINKING_TIME


class Philosopher(threading.Thread):
    def __init__(
        self,
        philosopher_id: int,
        table,
        left_fork,
        right_fork,
        *,
        version: str,
        waiter=None,
        cycles: int = SIMULATION_CYCLES,
        daemon: bool = False,
    ) -> None:
        super().__init__(name=f"Philosopher-{philosopher_id}", daemon=daemon)
        self.philosopher_id = philosopher_id
        self.table = table
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.version = version
        self.waiter = waiter
        self.cycles = cycles

    def run(self) -> None:
        try:
            self.table.start_barrier.wait(timeout=5)
        except threading.BrokenBarrierError:
            pass

        for _ in range(self.cycles):
            if self.table.stop_event.is_set():
                break

            self._think()
            if self.table.stop_event.is_set():
                break

            self._get_hungry()

            if self.version == "solution" and self.waiter is not None:
                self._wait_for_waiter()

            if self.table.stop_event.is_set():
                break

            self._enter_critical_region()
            self._eat()
            self._release_resources()

            if self.version == "solution" and self.waiter is not None:
                self.waiter.release()

        self.table.set_state(self.philosopher_id, PhilosopherState.THINKING)

    def _think(self) -> None:
        self.table.set_state(self.philosopher_id, PhilosopherState.THINKING)
        self.table.logger.philosopher(self.philosopher_id, "Pensando...")
        time.sleep(random.uniform(*THINKING_TIME))

    def _get_hungry(self) -> None:
        self.table.set_state(self.philosopher_id, PhilosopherState.HUNGRY)
        self.table.logger.philosopher(self.philosopher_id, "Com fome...")

    def _wait_for_waiter(self) -> None:
        self.table.set_state(self.philosopher_id, PhilosopherState.WAITING)
        self.table.logger.philosopher(self.philosopher_id, "Aguardando o garcom...")
        self.waiter.acquire()
        self.table.mark_progress()

    def _enter_critical_region(self) -> None:
        # Regiao critica: o filosofo precisa sincronizar o acesso aos dois garfos.
        self.table.set_state(self.philosopher_id, PhilosopherState.WAITING)
        self.table.logger.philosopher(self.philosopher_id, "Pegando garfo esquerdo...")
        self.left_fork.acquire()
        self.table.mark_progress()
        self.table.logger.philosopher(self.philosopher_id, "Pegou garfo esquerdo.")

        if self.version == "deadlock":
            try:
                self.table.logger.philosopher(
                    self.philosopher_id,
                    "Sincronizando para tentar o garfo direito ao mesmo tempo...",
                )
                self.table.deadlock_barrier.wait(timeout=5)
            except threading.BrokenBarrierError:
                pass

        self.table.logger.philosopher(self.philosopher_id, "Tentando pegar garfo direito...")
        self.right_fork.acquire()
        self.table.mark_progress()
        self.table.logger.philosopher(self.philosopher_id, "Pegou garfo direito.")

    def _eat(self) -> None:
        self.table.set_state(self.philosopher_id, PhilosopherState.EATING)
        self.table.logger.philosopher(self.philosopher_id, "Comendo...")
        time.sleep(random.uniform(*EATING_TIME))

    def _release_resources(self) -> None:
        self.table.set_state(self.philosopher_id, PhilosopherState.RELEASING)
        self.table.logger.philosopher(self.philosopher_id, "Liberando recursos...")

        self.right_fork.release()
        self.left_fork.release()
        self.table.mark_progress()
