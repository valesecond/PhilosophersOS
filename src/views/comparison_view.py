from __future__ import annotations

from rich.box import ROUNDED
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.synchronization.deadlock_version import run_deadlock_version
from src.synchronization.solution_version import run_solution_version
from src.ui.theme import THEME
from src.utils.config import SimulationConfig
from src.utils.helpers import clear_screen


class ComparisonView:
    def __init__(self) -> None:
        self.console = Console()

    def show(self, config: SimulationConfig) -> None:
        clear_screen()
        self.console.print(
            Panel(
                "[bold]Comparação lado a lado[/bold]\n"
                "Serão executadas as duas versões em sequência.\n"
                "Cada simulação mantém dashboard estável e log persistente.",
                border_style=THEME.accent,
            )
        )
        self.console.input("\n[bold cyan]▸ Pressione Enter para iniciar a 1ª simulação (Deadlock)...[/bold cyan]")

        deadlock_result = run_deadlock_version(
            config,
            clear_before=True,
            enter_prompt="Pressione Enter para iniciar a 2ª simulação (Solução)...",
        )
        solution_result = run_solution_version(config, clear_before=True)

        self.console.print()
        table = Table(
            title="[bold]Comparativo Final[/bold]",
            expand=True,
            box=ROUNDED,
            header_style=f"bold {THEME.accent}",
            show_lines=True,
        )
        table.add_column("Cenário", style="bold white")
        table.add_column("Refeições", justify="center")
        table.add_column("Deadlocks", justify="center")
        table.add_column("Tempo", justify="center")
        table.add_column("Resultado", justify="center")

        table.add_row(
            "Versão Deadlock",
            str(deadlock_result["meals"]),
            str(deadlock_result["deadlocks"]),
            f"{float(deadlock_result['elapsed']):.2f}s",
            "[bold red]Deadlock detectado[/bold red]",
        )
        table.add_row(
            "Versão Solução",
            str(solution_result["meals"]),
            str(solution_result["deadlocks"]),
            f"{float(solution_result['elapsed']):.2f}s",
            "[bold green]Execução estável[/bold green]",
        )

        analysis = Table.grid(padding=(0, 1))
        analysis.add_column(style=THEME.stat_label)
        analysis.add_column()
        analysis.add_row(
            "Diferença de refeições:",
            str(solution_result["meals"] - deadlock_result["meals"]),
        )
        analysis.add_row(
            "Conclusão:",
            "O semáforo garçom evita espera circular e permite progresso contínuo.",
        )

        self.console.print(Panel(table, border_style=THEME.border, title="[bold]Resultados[/bold]"))
        self.console.print(Panel(analysis, border_style=THEME.card_border, title="[bold]Análise[/bold]"))
        self.console.input("\n[bold cyan]▸ Pressione Enter para voltar ao menu...[/bold cyan]")
