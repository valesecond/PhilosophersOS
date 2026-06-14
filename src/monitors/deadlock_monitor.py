from __future__ import annotations

import threading
import time

from src.philosophers.states import PhilosopherState


class DeadlockMonitor(threading.Thread):
    """Monitor externo que detecta deadlock por ausência de progresso.

    MECANISMO: thread dedicada de monitoramento com polling periódico.
    Considera deadlock quando todos os filósofos estão em WAITING
    e nenhum progresso ocorre por mais de `timeout` segundos.
    """

    def __init__(self, table, timeout: float, poll_interval: float) -> None:
        super().__init__(name="DeadlockMonitor", daemon=True)
        self.table = table
        self.timeout = timeout
        self.poll_interval = poll_interval

    def run(self) -> None:
        while not self.table.stop_event.is_set():
            time.sleep(self.poll_interval)
            snapshot = self.table.state_snapshot()
            if not snapshot:
                continue

            all_waiting = all(state == PhilosopherState.WAITING for state in snapshot.values())
            wait_time = self.table.seconds_since_progress()

            if all_waiting and wait_time >= self.timeout:
                self.table.alert_deadlock(wait_time)
                return
