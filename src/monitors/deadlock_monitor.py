from __future__ import annotations

import threading
import time

from src.philosophers.states import PhilosopherState


class DeadlockMonitor(threading.Thread):
    def __init__(self, table, timeout: float, poll_interval: float) -> None:
        super().__init__(daemon=True)
        self.table = table
        self.timeout = timeout
        self.poll_interval = poll_interval

    def run(self) -> None:
        while not self.table.stop_event.is_set():
            time.sleep(self.poll_interval)
            snapshot = self.table.state_snapshot()
            if snapshot and all(state == PhilosopherState.WAITING for state in snapshot.values()):
                if self.table.seconds_since_progress() >= self.timeout:
                    self.table.alert_deadlock()
                    return
