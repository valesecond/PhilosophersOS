from __future__ import annotations

from rich.box import ROUNDED
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.ui.theme import THEME
from src.utils.config import SimulationConfig, save_config
from src.utils.helpers import clear_screen


class ConfigurationView:
    def __init__(self) -> None:
        self.console = Console()

    def show(self, config: SimulationConfig) -> None:
        while True:
            clear_screen()
            self.console.print(self._render(config))
            menu = Table.grid(padding=(0, 1))
            menu.add_column(style="bold bright_cyan")
            menu.add_row("[1] Número de filósofos")
            menu.add_row("[2] Tempo de pensamento")
            menu.add_row("[3] Tempo de alimentação")
            menu.add_row("[4] Velocidade da simulação")
            menu.add_row("[5] Ciclos por execução")
            menu.add_row("[6] Limite do garçom (semáforo)")
            menu.add_row("[0] Voltar ao menu principal")
            self.console.print(Panel(menu, title="[bold]Editar Configuração[/bold]", border_style=THEME.menu_border, box=ROUNDED))

            choice = self.console.input("\n[bold cyan]▸ Escolha o campo:[/bold cyan] ").strip()

            if choice == "0":
                return
            if choice == "1":
                config.num_philosophers = int(self.console.input("Novo número de filósofos: "))
            elif choice == "2":
                config.thinking_time = float(self.console.input("Novo tempo de pensamento (s): "))
            elif choice == "3":
                config.eating_time = float(self.console.input("Novo tempo de alimentação (s): "))
            elif choice == "4":
                config.simulation_speed = float(self.console.input("Nova velocidade (1.0 = normal): "))
            elif choice == "5":
                config.cycles = int(self.console.input("Novo número de ciclos: "))
            elif choice == "6":
                config.waiter_limit = int(self.console.input("Novo limite do garçom: "))
            else:
                self.console.print("[bold red]✗ Opção inválida.[/bold red]")
                continue

            save_config(config)
            self.console.print("[bold green]✓ Configuração salva em config.json[/bold green]")

    def _render(self, config: SimulationConfig) -> Panel:
        table = Table(title="[bold]Configurações Atuais[/bold]", expand=True, box=ROUNDED, header_style=f"bold {THEME.accent}")
        table.add_column("Parâmetro", style=THEME.stat_label)
        table.add_column("Valor", style="bold white")
        table.add_row("Filósofos", str(config.num_philosophers))
        table.add_row("Tempo de pensamento", f"{config.thinking_time:.2f}s")
        table.add_row("Tempo de alimentação", f"{config.eating_time:.2f}s")
        table.add_row("Velocidade", f"x{config.simulation_speed:.2f}")
        table.add_row("Ciclos", str(config.cycles))
        table.add_row("Timeout deadlock", f"{config.deadlock_timeout:.2f}s")
        table.add_row("Limite garçom", str(config.waiter_limit))
        return Panel(table, border_style=THEME.card_border)
