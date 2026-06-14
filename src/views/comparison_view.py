from __future__ import annotations

from rich.console import Console
from rich.table import Table

from src.synchronization.deadlock_version import run_deadlock_version
from src.synchronization.solution_version import run_solution_version
from src.utils.config import SimulationConfig


class ComparisonView:
    def __init__(self) -> None:
        self.console = Console()

    def show(self, config: SimulationConfig) -> None:
        deadlock_result = run_deadlock_version(config)
        solution_result = run_solution_version(config)

        table = Table(title="Comparacao das Implementacoes", expand=True)
        table.add_column("Cenario")
        table.add_column("Refeicoes")
        table.add_column("Deadlocks")
        table.add_column("Tempo")
        table.add_row("Deadlock", str(deadlock_result["meals"]), str(deadlock_result["deadlocks"]), f"{deadlock_result['elapsed']:.2f}s")
        table.add_row("Solucao", str(solution_result["meals"]), str(solution_result["deadlocks"]), f"{solution_result['elapsed']:.2f}s")
        self.console.print(table)
        self.console.input("[bold cyan]Pressione Enter para voltar ao menu...[/bold cyan]")
