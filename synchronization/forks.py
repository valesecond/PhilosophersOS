from __future__ import annotations

import threading


class Fork:
    def __init__(self, fork_id: int) -> None:
        self.fork_id = fork_id
        self.lock = threading.Lock()

    def acquire(self) -> None:
        self.lock.acquire()

    def release(self) -> None:
        self.lock.release()
