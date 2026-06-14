from __future__ import annotations

from src.monitors.deadlock_monitor import DeadlockMonitor
from src.philosophers.table import DiningTable
from src.ui.simulation_console import SimulationConsole
from src.ui.theme import THEME
from src.utils.config import SimulationConfig
from src.utils.constants import STRATEGY_DEADLOCK
from src.utils.helpers import clear_screen


def run_deadlock_version(
    config: SimulationConfig,
    *,
    clear_before: bool = True,
    wait_at_end: bool = True,
    enter_prompt: str = "Pressione Enter para voltar ao menu...",
) -> dict:
    if clear_before:
        clear_screen()

    console = SimulationConsole()
    console.open_session(
        strategy=STRATEGY_DEADLOCK,
        num_philosophers=config.num_philosophers,
        border_style=THEME.deadlock_border,
    )
    console.info("Versão vulnerável: todos adquirem o garfo esquerdo simultaneamente.")

    table = DiningTable(config)
    table.assign_logger(console)
    table.mark_running()
    philosophers = table.create_philosophers(strategy="deadlock")
    monitor = DeadlockMonitor(table, timeout=config.deadlock_timeout, poll_interval=config.deadlock_poll_interval)

    for philosopher in philosophers:
        philosopher.start()

    monitor.start()

    for philosopher in philosophers:
        philosopher.join(timeout=config.deadlock_timeout + 2)

    table.stop_event.set()
    monitor.join(timeout=1)

    snapshot = table.snapshot()
    result = {
        "elapsed": snapshot.elapsed,
        "meals": snapshot.meals,
        "deadlocks": snapshot.deadlocks,
        "active_threads": snapshot.active_threads,
        "strategy": STRATEGY_DEADLOCK,
        "deadlock_info": table.deadlock_info,
        "num_philosophers": config.num_philosophers,
    }

    console.show_summary(
        elapsed=snapshot.elapsed,
        strategy=STRATEGY_DEADLOCK,
        meals=snapshot.meals,
        deadlocks=snapshot.deadlocks,
        num_philosophers=config.num_philosophers,
        active_threads=snapshot.active_threads,
        deadlock_info=table.deadlock_info,
    )
    if wait_at_end:
        console.wait_enter(enter_prompt)
    return result
