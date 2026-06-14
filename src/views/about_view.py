from __future__ import annotations

from rich.console import Console
from rich.panel import Panel

from src.utils.constants import APP_NAME, APP_VERSION


class AboutView:
    def __init__(self) -> None:
        self.console = Console()

    def show(self) -> None:
        content = (
            f"Projeto: {APP_NAME}\n"
            f"Versao: {APP_VERSION}\n\n"
            "Disciplina:\nSistemas Operacionais\n\n"
            "Conceitos Demonstrados:\n"
            "✓ Concorrencia\n"
            "✓ Threads\n"
            "✓ Regiao Critica\n"
            "✓ Exclusao Mutua\n"
            "✓ Deadlock\n"
            "✓ Sincronizacao\n"
            "✓ Semaforos"
        )
        self.console.print(Panel(content, title="Sobre o Projeto", border_style="cyan"))
        self.console.input("[bold cyan]Pressione Enter para voltar ao menu...[/bold cyan]")
