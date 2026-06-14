from __future__ import annotations

from dataclasses import dataclass

from rich.console import Console
from rich.panel import Panel

from src.philosophers.table import DeadlockInfo
from src.ui.components import render_deadlock_alert
from src.utils.constants import APP_NAME, APP_TAGLINE, APP_VERSION


@dataclass(slots=True)
class LoggerTheme:
    accent: str = "cyan"
    success: str = "green"
    warning: str = "yellow"
    danger: str = "bold red"
    muted: str = "white"


class SimulationLogger:
    def __init__(self) -> None:
        self.console = Console()
        self.theme = LoggerTheme()

    def banner(self) -> None:
        self.console.print(
            Panel.fit(
                f"[bold]{APP_NAME}[/bold]\n[white]{APP_TAGLINE}[/white]\n[dim]Versão {APP_VERSION}[/dim]",
                border_style=self.theme.accent,
                title="Sistema",
            )
        )

    def info(self, message: str) -> None:
        self.console.print(f"[cyan]▸ {message}[/cyan]")

    def philosopher_line(self, philosopher_id: int, state: str, message: str) -> None:
        self.console.print(f"[bold white][P{philosopher_id}] {state}:[/bold white] {message}")

    def deadlock_alert(self, info: DeadlockInfo | str) -> None:
        if isinstance(info, DeadlockInfo):
            self.console.print(render_deadlock_alert(info))
        else:
            self.console.print(f"[bold red]{info}[/bold red]")

    def success(self, message: str) -> None:
        self.console.print(f"[green]✓ {message}[/green]")

    def warning(self, message: str) -> None:
        self.console.print(f"[yellow]⚠ {message}[/yellow]")

    def danger(self, message: str) -> None:
        self.console.print(f"[bold red]✗ {message}[/bold red]")

    def plain(self, message: str) -> None:
        self.console.print(message)
