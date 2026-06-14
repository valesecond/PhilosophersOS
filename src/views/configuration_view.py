from __future__ import annotations

from rich.console import Console
from rich.table import Table

from src.utils.config import SimulationConfig, save_config


class ConfigurationView:
    def __init__(self) -> None:
        self.console = Console()

    def show(self, config: SimulationConfig) -> None:
        while True:
            self.console.print(self._render(config))
            self.console.print("[bold cyan]1[/bold cyan] - Filosofos")
            self.console.print("[bold cyan]2[/bold cyan] - Tempo de pensamento")
            self.console.print("[bold cyan]3[/bold cyan] - Tempo de alimentacao")
            self.console.print("[bold cyan]4[/bold cyan] - Velocidade da simulacao")
            self.console.print("[bold cyan]5[/bold cyan] - Ciclos por execucao")
            self.console.print("[bold cyan]0[/bold cyan] - Voltar")
            choice = self.console.input("[bold cyan]Escolha o campo:[/bold cyan] ").strip()

            if choice == "0":
                return
            if choice == "1":
                config.num_philosophers = int(self.console.input("Novo numero de filosofos: "))
            elif choice == "2":
                config.thinking_time = float(self.console.input("Novo tempo de pensamento: "))
            elif choice == "3":
                config.eating_time = float(self.console.input("Novo tempo de alimentacao: "))
            elif choice == "4":
                config.simulation_speed = float(self.console.input("Nova velocidade da simulacao: "))
            elif choice == "5":
                config.cycles = int(self.console.input("Novo numero de ciclos: "))
            else:
                self.console.print("[bold red]Opcao invalida.[/bold red]")
                continue

            save_config(config)
            self.console.print("[bold green]Configuracao salva com sucesso.[/bold green]")

    def _render(self, config: SimulationConfig) -> Table:
        table = Table(title="Configuracoes Atuais", expand=True)
        table.add_column("Parametro")
        table.add_column("Valor")
        table.add_row("Filosofos", str(config.num_philosophers))
        table.add_row("Tempo de pensamento", f"{config.thinking_time:.2f}s")
        table.add_row("Tempo de alimentacao", f"{config.eating_time:.2f}s")
        table.add_row("Velocidade", f"x{config.simulation_speed:.2f}")
        table.add_row("Ciclos", str(config.cycles))
        table.add_row("Timeout deadlock", f"{config.deadlock_timeout:.2f}s")
        return table
