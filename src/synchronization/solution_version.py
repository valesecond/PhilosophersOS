from __future__ import annotations

import threading

from src.philosophers.table import DiningTable
from src.ui.simulation_console import SimulationConsole
from src.ui.theme import THEME
from src.utils.config import SimulationConfig
from src.utils.constants import STRATEGY_SOLUTION
from src.utils.helpers import clear_screen


def run_solution_version(
    config: SimulationConfig,
    *,
    clear_before: bool = True,
    wait_at_end: bool = True,
    enter_prompt: str = "Pressione Enter para voltar ao menu...",
) -> dict:
    if clear_before:
        clear_screen()

    waiter_limit = min(config.waiter_limit, max(1, config.num_philosophers - 1))
    console = SimulationConsole()
    console.open_session(
        strategy=STRATEGY_SOLUTION,
        num_philosophers=config.num_philosophers,
        border_style=THEME.solution_border,
    )
    console.info(f"Garçom semáforo ativo — máximo de {waiter_limit} filósofos disputando garfos.")

    table = DiningTable(config)
    table.assign_logger(console)
    table.mark_running()
    waiter = threading.Semaphore(waiter_limit)
    philosophers = table.create_philosophers(strategy="solution", waiter=waiter)

    for philosopher in philosophers:
        philosopher.start()

    for philosopher in philosophers:
        philosopher.join()

    table.stop_event.set()

    snapshot = table.snapshot()
    result = {
        "elapsed": snapshot.elapsed,
        "meals": snapshot.meals,
        "deadlocks": snapshot.deadlocks,
        "active_threads": snapshot.active_threads,
        "strategy": STRATEGY_SOLUTION,
        "deadlock_info": None,
        "num_philosophers": config.num_philosophers,
    }

    console.show_summary(
        elapsed=snapshot.elapsed,
        strategy=STRATEGY_SOLUTION,
        meals=snapshot.meals,
        deadlocks=snapshot.deadlocks,
        num_philosophers=config.num_philosophers,
        active_threads=snapshot.active_threads,
    )
    if wait_at_end:
        console.wait_enter(enter_prompt)
    return result
