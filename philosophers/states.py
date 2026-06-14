from __future__ import annotations

from enum import Enum


class PhilosopherState(str, Enum):
    THINKING = "THINKING"
    HUNGRY = "HUNGRY"
    WAITING = "WAITING"
    EATING = "EATING"
    RELEASING = "RELEASING"


STATE_LABELS = {
    PhilosopherState.THINKING: "Pensando",
    PhilosopherState.HUNGRY: "Com fome",
    PhilosopherState.WAITING: "Aguardando recurso",
    PhilosopherState.EATING: "Comendo",
    PhilosopherState.RELEASING: "Liberando recursos",
}
