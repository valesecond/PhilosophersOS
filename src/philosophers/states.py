from __future__ import annotations

from enum import Enum


class PhilosopherState(str, Enum):
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
