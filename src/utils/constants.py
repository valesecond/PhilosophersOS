from __future__ import annotations

APP_NAME = "PHILOSOPHERS OS"
APP_TAGLINE = "Deadlock & Concurrency Simulator"
APP_VERSION = "1.0.0"

STATUS_READY = "READY"
STATUS_RUNNING = "RUNNING"
STATUS_STOPPED = "STOPPED"

STRATEGY_DEADLOCK = "Deadlock (vulnerável)"
STRATEGY_SOLUTION = "Garçom Semáforo (solução)"

MENU_ACTIONS = {
    "1": "Simular Deadlock",
    "2": "Simular Solução",
    "3": "Comparar Implementações",
    "4": "Configurações",
    "5": "Arquitetura do Sistema",
    "6": "Sobre",
    "0": "Encerrar Sistema",
}
