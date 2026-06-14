from __future__ import annotations

import threading

from src.monitors.execution_monitor import ExecutionMonitor
from src.philosophers.table import DiningTable
from src.utils.config import SimulationConfig
from src.utils.constants import STRATEGY_SOLUTION
from src.utils.logger import SimulationLogger


def run_solution_version(config: SimulationConfig) -> dict[str, float | int | str]:
    logger = SimulationLogger()
    logger.banner()
    logger.info("Executando simulacao com garcom semaforo para evitar deadlock.")
    logger.info("Somente 4 filosofos podem disputar recursos simultaneamente.")

    table = DiningTable(config)
    table.assign_logger(logger)
    waiter = threading.Semaphore(4)
    philosophers = table.create_philosophers(strategy="solution", waiter=waiter)
    dashboard = ExecutionMonitor(lambda: _build_dashboard(table), refresh_rate=0.2 / config.simulation_speed, stop_event=table.stop_event)

    for philosopher in philosophers:
        philosopher.start()

    dashboard.start()

    for philosopher in philosophers:
        philosopher.join()

    table.stop_event.set()
    dashboard.join(timeout=1)

    snapshot = table.snapshot()
    return {
        "elapsed": snapshot.elapsed,
        "meals": snapshot.meals,
        "deadlocks": snapshot.deadlocks,
        "active_threads": snapshot.active_threads,
        "strategy": STRATEGY_SOLUTION,
    }


def _build_dashboard(table: DiningTable):
    from rich.console import Group
    from rich.panel import Panel
    from rich.table import Table

    snapshot = table.snapshot()
    summary = Table.grid(expand=True)
    summary.add_column(justify="left")
    summary.add_column(justify="right")
    summary.add_row("Tempo de execucao", f"{snapshot.elapsed:0.2f}s")
    summary.add_row("Refeicoes", str(snapshot.meals))
    summary.add_row("Deadlocks detectados", str(snapshot.deadlocks))
    summary.add_row("Threads ativas", str(snapshot.active_threads))
    summary.add_row("Estrategia", snapshot.strategy)
    summary.add_row("Status", snapshot.status)
    return Panel(Group(summary, table.render_activity_table()), title="PHILOSOPHERS OS", border_style="green")
