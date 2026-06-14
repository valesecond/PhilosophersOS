from __future__ import annotations

from rich.box import DOUBLE, ROUNDED
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.ui.theme import THEME
from src.utils.constants import APP_NAME, APP_VERSION
from src.utils.helpers import clear_screen


class AboutView:
    def __init__(self) -> None:
        self.console = Console()

    def show(self) -> None:
        clear_screen()

        concepts = Table(box=ROUNDED, expand=True, show_header=False)
        concepts.add_column(style=THEME.success, width=3)
        concepts.add_column(style="white")
        for label in (
            "Concorrência",
            "Threads",
            "Região Crítica",
            "Exclusão Mútua",
            "Deadlock",
            "Sincronização",
            "Semáforos",
        ):
            concepts.add_row("✓", label)

        info = Table.grid(padding=(0, 1))
        info.add_column(style=THEME.stat_label)
        info.add_column(style="bold white")
        info.add_row("Projeto", APP_NAME)
        info.add_row("Versão", APP_VERSION)
        info.add_row("Disciplina", "Sistemas Operacionais")
        info.add_row("Instituição", "Trabalho Prático — Deadlocks")
        info.add_row("Linguagem", "Python 3.10+")
        info.add_row("Interface", "Rich CLI")

        self.console.print(
            Panel(
                info,
                title=f"[bold bright_white]Sobre — {APP_NAME}[/bold bright_white]",
                border_style=THEME.header_border,
                box=DOUBLE,
            )
        )
        self.console.print(Panel(concepts, title="[bold]Conceitos Demonstrados[/bold]", border_style=THEME.card_border))
        self.console.input("\n[bold cyan]▸ Pressione Enter para voltar ao menu...[/bold cyan]")
