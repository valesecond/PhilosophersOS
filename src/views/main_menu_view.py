from __future__ import annotations

from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from src.ui.components import render_app_banner, render_main_menu, render_status_cards
from src.ui.theme import THEME
from src.utils.config import load_config
from src.utils.helpers import clear_screen
from src.views.about_view import AboutView
from src.views.architecture_view import ArchitectureView
from src.views.comparison_view import ComparisonView
from src.views.configuration_view import ConfigurationView
from src.views.deadlock_view import DeadlockView
from src.views.solution_view import SolutionView


class MainMenuView:
    def __init__(self) -> None:
        self.console = Console()

    def show(self) -> None:
        while True:
            config = load_config()
            clear_screen()
            self.console.print(render_app_banner())
            self.console.print(render_status_cards(system_online=True, num_philosophers=config.num_philosophers))
            self.console.print(render_main_menu())
            choice = self.console.input("\n[bold bright_cyan]▸ Selecione uma opção:[/bold bright_cyan] ").strip()

            if choice == "1":
                DeadlockView().show(config)
            elif choice == "2":
                SolutionView().show(config)
            elif choice == "3":
                ComparisonView().show(config)
            elif choice == "4":
                ConfigurationView().show(config)
            elif choice == "5":
                ArchitectureView().show(config)
            elif choice == "6":
                AboutView().show()
            elif choice == "0":
                clear_screen()
                farewell = Panel(
                    Align.center(Text("Sistema encerrado com sucesso.\nObrigado por utilizar o PhilosophersOS.", style=THEME.muted)),
                    title="[bold bright_cyan]Até logo[/bold bright_cyan]",
                    border_style=THEME.header_border,
                )
                self.console.print(farewell)
                break
            else:
                self.console.print("[bold red]✗ Opção inválida. Tente novamente.[/bold red]")
