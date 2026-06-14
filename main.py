from __future__ import annotations

import os
from typing import Callable

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
except Exception:  # pragma: no cover - fallback para ambiente sem rich
    Console = None
    Panel = None
    Text = None

from synchronization.deadlock_version import run_deadlock_version
from synchronization.solution_version import run_solution_version
from utils.config import NUM_PHILOSOPHERS
from utils.logger import SimulationLogger


console = Console() if Console is not None else None
logger = SimulationLogger()


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def render_menu() -> None:
    clear_screen()

    if console is None:
        print("==================================")
        print("PhilosophersOS")
        print("==================================")
        print(f"Numero de filosofos: {NUM_PHILOSOPHERS}")
        print()
        print("1 - Executar versao com Deadlock")
        print("2 - Executar versao com Solucao")
        print("3 - Sair")
        print()
        return

    title = Text("PhilosophersOS", style="bold cyan")
    subtitle = Text("Simulacao do Problema do Jantar dos Filosofos", style="bold white")

    console.print(Panel(title, subtitle=subtitle, border_style="cyan", expand=False))
    console.print(f"[bold yellow]Numero de filosofos:[/bold yellow] [bold white]{NUM_PHILOSOPHERS}[/bold white]")
    console.print()
    console.print("[bold green]1[/bold green] - Executar versao com Deadlock")
    console.print("[bold green]2[/bold green] - Executar versao com Solucao")
    console.print("[bold green]3[/bold green] - Sair")
    console.print()


def run_option(option: str) -> None:
    actions: dict[str, Callable[[], None]] = {
        "1": run_deadlock_version,
        "2": run_solution_version,
    }

    action = actions.get(option)
    if action is None:
        if option == "3":
            raise SystemExit
        logger.warning("Opcao invalida. Tente novamente.")
        return

    clear_screen()
    action()
    if console is None:
        print()
        print("Pressione Enter para voltar ao menu...")
    else:
        console.print()
        console.print("[bold cyan]Pressione Enter para voltar ao menu...[/bold cyan]")
    input()


def main() -> None:
    while True:
        render_menu()
        choice = input("Escolha uma opcao: ").strip()
        try:
            run_option(choice)
        except SystemExit:
            clear_screen()
            if console is None:
                print("==================================")
                print("Saindo do PhilosophersOS")
                print("==================================")
            else:
                console.print(Panel("Saindo do PhilosophersOS", border_style="cyan", expand=False))
            break


if __name__ == "__main__":
    main()
