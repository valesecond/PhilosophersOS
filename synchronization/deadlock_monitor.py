from __future__ import annotations

import threading
import time

from utils.config import DEADLOCK_CHECK_INTERVAL, DEADLOCK_TIMEOUT


class DeadlockMonitor(threading.Thread):
    def __init__(self, table, timeout: float = DEADLOCK_TIMEOUT, interval: float = DEADLOCK_CHECK_INTERVAL) -> None:
        super().__init__(daemon=True, name="DeadlockMonitor")
        self.table = table
        self.timeout = timeout
        self.interval = interval

    def run(self) -> None:
        while not self.table.stop_event.is_set():
            time.sleep(self.interval)

            if not self.table.all_waiting():
                continue

            if self.table.time_since_progress() >= self.timeout:
                self.table.logger.deadlock("DEADLOCK DETECTADO")
                self.table.stop_event.set()
                return
