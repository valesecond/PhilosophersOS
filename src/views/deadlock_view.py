from __future__ import annotations

from rich.console import Console

from src.synchronization.deadlock_version import run_deadlock_version
from src.utils.config import SimulationConfig


class DeadlockView:
    def __init__(self) -> None:
        self.console = Console()

    def show(self, config: SimulationConfig) -> None:
        result = run_deadlock_version(config)
        self.console.print(
            f"\n[bold red]DEADLOCK DETECTADO[/bold red] | Refeicoes: {result['meals']} | Tempo: {result['elapsed']:.2f}s"
        )
        self.console.input("[bold cyan]Pressione Enter para voltar ao menu...[/bold cyan]")
