from __future__ import annotations

import threading


class Fork:
    """Representa um garfo compartilhado protegido por exclusão mútua.

    MECANISMO DE SINCRONIZAÇÃO: threading.Lock
    - Garante que apenas um filósofo segure o garfo por vez.
    - Implementa exclusão mútua sobre o recurso compartilhado.
    """

    def __init__(self, fork_id: int) -> None:
        self.fork_id = fork_id
        # Lock exclusivo — mutex do garfo (recurso compartilhado)
        self._lock = threading.Lock()
        self.owner: int | None = None

    @property
    def lock(self) -> threading.Lock:
        return self._lock

    def acquire(self, philosopher_id: int) -> None:
        """Adquire o garfo. Bloqueia até o recurso estar disponível."""
        self._lock.acquire()
        self.owner = philosopher_id

    def release(self) -> None:
        """Libera o garfo para outros filósofos."""
        self.owner = None
        self._lock.release()

    def label(self) -> str:
        return f"F{self.fork_id}"
