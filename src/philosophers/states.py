from __future__ import annotations

from enum import Enum


class PhilosopherState(str, Enum):
    """Estados obrigatórios do ciclo de vida de cada filósofo."""

    THINKING = "PENSANDO"
    HUNGRY = "COM FOME"
    WAITING = "ESPERANDO"
    EATING = "COMENDO"
    RELEASING = "LIBERANDO"


STATE_ORDER = (
    PhilosopherState.THINKING,
    PhilosopherState.HUNGRY,
    PhilosopherState.WAITING,
    PhilosopherState.EATING,
    PhilosopherState.RELEASING,
)
