from __future__ import annotations

import threading


class Fork:
    def __init__(self, fork_id: int) -> None:
        self.fork_id = fork_id
        self._lock = threading.Lock()
        self.owner: int | None = None

    @property
    def lock(self) -> threading.Lock:
        return self._lock

    def acquire(self, philosopher_id: int) -> None:
        self._lock.acquire()
        self.owner = philosopher_id

    def release(self) -> None:
        self.owner = None
        self._lock.release()

    def label(self) -> str:
        return f"F{self.fork_id}"
