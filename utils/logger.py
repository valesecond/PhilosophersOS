from __future__ import annotations

import datetime as _datetime

from philosophers.states import PhilosopherState, STATE_LABELS

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
except Exception:  # pragma: no cover - fallback quando rich nao estiver instalado
    Console = None
    Panel = None
    Text = None


class SimulationLogger:
    def __init__(self) -> None:
        self._console = Console() if Console is not None else None

    def header(self, title: str) -> None:
        if self._console is None:
            print(f"\n=== {title} ===\n")
            return

        content = Text(title, style="bold cyan")
        self._console.print(Panel(content, border_style="cyan", expand=False))

    def system(self, message: str) -> None:
        self._print("cyan", f"[Sistema] {message}")

    def success(self, message: str) -> None:
        self._print("green", f"[Sistema] {message}")

    def warning(self, message: str) -> None:
        self._print("yellow", f"[Sistema] {message}")

    def deadlock(self, message: str) -> None:
        self._print("bold red", message)

    def philosopher(self, philosopher_id: int, message: str, state: PhilosopherState | None = None) -> None:
        prefix = f"[Filosofo {philosopher_id}]"
        if state is not None:
            label = STATE_LABELS[state]
            self._print("white", f"{prefix} {label}... {message}".strip())
            return

        self._print("white", f"{prefix} {message}")

    def state_change(self, philosopher_id: int, state: PhilosopherState) -> None:
        label = STATE_LABELS[state]
        self._print("bold white", f"[Filosofo {philosopher_id}] Estado -> {label}")

    def _print(self, style: str, message: str) -> None:
        timestamp = _datetime.datetime.now().strftime("%H:%M:%S")
        output = f"[{timestamp}] {message}"
        if self._console is None:
            print(output)
            return

        self._console.print(f"[{style}]{output}[/{style}]")
