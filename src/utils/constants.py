from __future__ import annotations

APP_NAME = "PHILOSOPHERS OS"
APP_TAGLINE = "Dining Philosophers & Deadlock Simulator"
APP_VERSION = "1.0.0"

STATUS_READY = "READY"
STATUS_RUNNING = "RUNNING"
STATUS_STOPPED = "STOPPED"

STRATEGY_DEADLOCK = "Deadlock"
STRATEGY_SOLUTION = "Semaphore Waiter"

MENU_ACTIONS = {
    "1": "Simular Deadlock",
    "2": "Simular Solucao (Semaphore Waiter)",
    "3": "Comparar Implementacoes",
    "4": "Configuracoes",
    "5": "Sobre o Projeto",
    "0": "Encerrar Sistema",
}
