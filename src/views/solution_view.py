from __future__ import annotations

from rich.console import Console

from src.synchronization.solution_version import run_solution_version
from src.utils.config import SimulationConfig


class SolutionView:
    def __init__(self) -> None:
        self.console = Console()

    def show(self, config: SimulationConfig) -> None:
        result = run_solution_version(config)
        self.console.print(
            f"\n[bold green]SOLUCAO CONCLUIDA[/bold green] | Refeicoes: {result['meals']} | Deadlocks: {result['deadlocks']} | Tempo: {result['elapsed']:.2f}s"
        )
        self.console.input("[bold cyan]Pressione Enter para voltar ao menu...[/bold cyan]")
