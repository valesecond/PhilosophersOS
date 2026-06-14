from __future__ import annotations

from rich.console import Console

from src.ui.components import render_architecture_panel
from src.utils.config import SimulationConfig
from src.utils.helpers import clear_screen


class ArchitectureView:
    def __init__(self) -> None:
        self.console = Console()

    def show(self, config: SimulationConfig) -> None:
        clear_screen()
        self.console.print(render_architecture_panel(config))
        self.console.input("\n[bold cyan]▸ Pressione Enter para voltar ao menu...[/bold cyan]")
