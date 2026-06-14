from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.utils.config import load_config
from src.utils.constants import APP_NAME, APP_TAGLINE, MENU_ACTIONS, STATUS_READY
from src.utils.helpers import clear_screen
from src.utils.logger import SimulationLogger
from src.views.about_view import AboutView
from src.views.comparison_view import ComparisonView
from src.views.configuration_view import ConfigurationView
from src.views.deadlock_view import DeadlockView
from src.views.solution_view import SolutionView


class MainMenuView:
    def __init__(self) -> None:
        self.console = Console()
        self.logger = SimulationLogger()

    def show(self) -> None:
        while True:
            config = load_config()
            clear_screen()
            self.console.print(self._header(config.num_philosophers))
            self.console.print(self._menu())
            choice = self.console.input("[bold cyan]Selecione uma opcao:[/bold cyan] ").strip()

            if choice == "1":
                DeadlockView().show(config)
            elif choice == "2":
                SolutionView().show(config)
            elif choice == "3":
                ComparisonView().show(config)
            elif choice == "4":
                ConfigurationView().show(config)
            elif choice == "5":
                AboutView().show()
            elif choice == "0":
                clear_screen()
                self.console.print(Panel.fit("Sistema encerrado.", border_style="cyan"))
                break
            else:
                self.console.print("[bold red]Opcao invalida.[/bold red]")

    def _header(self, philosophers: int) -> Panel:
        table = Table.grid(expand=True)
        table.add_column()
        table.add_column(justify="right")
        table.add_row(f"[bold]{APP_NAME}[/bold]", "[bold]Dining Philosophers & Deadlock Simulator[/bold]")
        table.add_row(f"Status: {STATUS_READY}", f"Filosofos: {philosophers}")
        table.add_row("Threads Ativas: 0", "Estrategias Disponiveis: 2")
        return Panel(table, border_style="cyan")

    def _menu(self) -> Panel:
        options = Table.grid(padding=(0, 2))
        options.add_column(justify="left")
        options.add_row("[1] Simular Deadlock")
        options.add_row("[2] Simular Solucao (Semaphore Waiter)")
        options.add_row("[3] Comparar Implementacoes")
        options.add_row("[4] Configuracoes")
        options.add_row("[5] Sobre o Projeto")
        options.add_row("")
        options.add_row("[0] Encerrar Sistema")
        return Panel(options, title="MENU PRINCIPAL", border_style="magenta")
