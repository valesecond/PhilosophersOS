from __future__ import annotations

import threading
import time
from dataclasses import dataclass

from rich.live import Live

from src.utils.constants import STATUS_RUNNING


@dataclass(slots=True)
class ExecutionSnapshot:
    elapsed: float
    meals: int
    deadlocks: int
    active_threads: int
    strategy: str
    status: str = STATUS_RUNNING


class ExecutionMonitor(threading.Thread):
    def __init__(self, dashboard_builder, refresh_rate: float, stop_event: threading.Event) -> None:
        super().__init__(daemon=True)
        self.dashboard_builder = dashboard_builder
        self.refresh_rate = refresh_rate
        self.stop_event = stop_event

    def run(self) -> None:
        with Live(self.dashboard_builder(), refresh_per_second=max(2, int(1 / self.refresh_rate)), screen=True) as live:
            while not self.stop_event.is_set():
                live.update(self.dashboard_builder())
                time.sleep(self.refresh_rate)
            live.update(self.dashboard_builder())
