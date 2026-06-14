from __future__ import annotations

import threading
from collections import deque
from datetime import datetime

from rich.box import HEAVY, ROUNDED
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from src.philosophers.states import PhilosopherState
from src.philosophers.table import DeadlockInfo
from src.ui.theme import STATE_STYLES, THEME
from src.utils.constants import APP_NAME, APP_TAGLINE

MAX_LOG_EVENTS = 30


class SimulationConsole:
    """Console estável: dashboard + log persistente, atualizado apenas por evento.

    Usa Rich Live com auto_refresh=False — nunca faz polling nem limpa a tela.
    Cada mudança de estado dispara uma única atualização do painel completo.
    """

    def __init__(self) -> None:
        self.console = Console()
        self._lock = threading.Lock()
        self._live: Live | None = None
        self._events: deque[tuple[str, str, str]] = deque(maxlen=MAX_LOG_EVENTS)
        self._states: dict[int, PhilosopherState] = {}
        self._resources: dict[int, str] = {}
        self._num_philosophers = 0
        self._border_style = THEME.accent
        self._strategy = "-"
        self._session_open = False

    def open_session(self, *, strategy: str, num_philosophers: int, border_style: str) -> None:
        with self._lock:
            self._strategy = strategy
            self._num_philosophers = num_philosophers
            self._border_style = border_style
            self._states = {index: PhilosopherState.THINKING for index in range(num_philosophers)}
            self._resources = {index: "-" for index in range(num_philosophers)}
            self._events.clear()
            self._session_open = True

            self._live = Live(
                self._render_panel(),
                console=self.console,
                refresh_per_second=4,
                auto_refresh=False,
                screen=False,
                transient=False,
            )
            self._live.start()
            self._append_event("Simulação iniciada", THEME.accent_dim)

    def close_session(self) -> None:
        with self._lock:
            if self._live is not None:
                self._live.stop()
                self._live = None
            self._session_open = False

    def philosopher_line(self, philosopher_id: int, state: str, message: str) -> None:
        with self._lock:
            if not self._session_open:
                return

            try:
                enum_state = PhilosopherState(state)
            except ValueError:
                enum_state = PhilosopherState.THINKING

            self._states[philosopher_id] = enum_state
            event_text = _format_event(philosopher_id, enum_state, message)
            self._append_event(event_text, _event_style(enum_state))

    def register_resource(self, philosopher_id: int, resources: str) -> None:
        with self._lock:
            if not self._session_open:
                return
            self._resources[philosopher_id] = resources
            self._refresh()

    def info(self, message: str) -> None:
        with self._lock:
            if self._session_open:
                self._append_event(message, THEME.accent_dim)

    def deadlock_alert(self, info: DeadlockInfo | str) -> None:
        with self._lock:
            if not self._session_open:
                return
            if isinstance(info, DeadlockInfo):
                blocked = ", ".join(f"P{pid}" for pid in info.blocked_philosophers)
                self._append_event(
                    f"DEADLOCK DETECTADO — bloqueados: {blocked} | espera: {info.wait_time:.2f}s",
                    f"bold {THEME.danger}",
                )
                self._append_event(
                    f"Recursos aguardados: {info.waiting_resources_summary()}",
                    THEME.danger,
                )
            else:
                self._append_event(str(info), f"bold {THEME.danger}")

    def show_summary(
        self,
        *,
        elapsed: float,
        strategy: str,
        meals: int,
        deadlocks: int,
        num_philosophers: int,
        active_threads: int,
        deadlock_info: DeadlockInfo | None = None,
    ) -> None:
        self.close_session()
        self.console.print()

        table = Table(box=ROUNDED, expand=True, header_style=f"bold {THEME.accent}")
        table.add_column("Indicador", style=THEME.stat_label)
        table.add_column("Valor", style="bold white")
        table.add_row("Tempo total", f"{elapsed:.2f}s")
        table.add_row("Estratégia", strategy)
        table.add_row("Refeições realizadas", str(meals))
        table.add_row("Deadlocks detectados", str(deadlocks))
        table.add_row("Filósofos", str(num_philosophers))
        table.add_row("Threads ativas", str(active_threads))
        table.add_row("Eventos registrados", str(len(self._events)))

        if deadlock_info is not None:
            table.add_row("Filósofos bloqueados", ", ".join(f"P{pid}" for pid in deadlock_info.blocked_philosophers))
            table.add_row("Tempo de espera", f"{deadlock_info.wait_time:.2f}s")
            title = "[bold red]Resumo Final — Deadlock Detectado[/bold red]"
            border = THEME.deadlock_border
        elif deadlocks == 0:
            table.add_row("Status", "[bright_green]Execução concluída sem deadlock[/bright_green]")
            title = "[bold green]Resumo Final — Simulação Concluída[/bold green]"
            border = THEME.solution_border
        else:
            title = "[bold]Resumo Final[/bold]"
            border = THEME.border

        self.console.print(Panel(table, title=title, border_style=border, box=HEAVY))

    def wait_enter(self, prompt: str = "Pressione Enter para voltar ao menu...") -> None:
        self.console.input(f"\n[bold cyan]> {prompt}[/bold cyan]")

    def _append_event(self, message: str, style: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        self._events.append((timestamp, message, style))
        self._refresh()

    def _refresh(self) -> None:
        if self._live is not None:
            self._live.update(self._render_panel(), refresh=True)

    def _render_panel(self) -> Panel:
        header = Panel(
            Text(f"{APP_NAME}  |  {APP_TAGLINE}\nEstratégia: {self._strategy}", justify="center"),
            border_style=self._border_style,
            box=HEAVY,
        )
        dashboard = _render_state_dashboard(self._states, self._resources, border_style=self._border_style)
        log_body = _render_event_log(self._events)
        log_panel = Panel(
            log_body,
            title=f"[bold]Log de Eventos[/bold]  [dim](últimos {len(self._events)}/{MAX_LOG_EVENTS})[/dim]",
            border_style=THEME.card_border,
            box=ROUNDED,
        )
        return Panel(
            Group(header, dashboard, log_panel),
            border_style=self._border_style,
            padding=(0, 1),
        )


def _render_state_dashboard(
    states: dict[int, PhilosopherState],
    resources: dict[int, str],
    *,
    border_style: str,
) -> Panel:
    body = Table.grid(padding=(0, 1))
    body.add_column(style="bold white", width=6)
    body.add_column(style="bold cyan", width=4)
    body.add_column(min_width=14)

    for philosopher_id in sorted(states):
        state = states[philosopher_id]
        style = STATE_STYLES.get(state.value, "white")
        body.add_row(
            f"P{philosopher_id}",
            "->",
            f"[{style}]{state.value}[/{style}]",
        )

    return Panel(
        body,
        title="[bold]Dashboard de Estado Atual[/bold]",
        border_style=border_style,
        box=ROUNDED,
    )


def _render_event_log(events: deque[tuple[str, str, str]]) -> Text:
    if not events:
        return Text("Aguardando eventos...", style=THEME.muted)

    log = Text()
    for index, (timestamp, message, style) in enumerate(events):
        if index > 0:
            log.append("\n")
        log.append(f"[{timestamp}] ", style="dim")
        log.append(message, style=style)
    return log


def _format_event(philosopher_id: int, state: PhilosopherState, detail: str) -> str:
    detail_lower = detail.lower()
    if state == PhilosopherState.THINKING:
        if "conclu" in detail_lower:
            return f"P{philosopher_id} concluiu o ciclo"
        return f"P{philosopher_id} começou a pensar"
    if state == PhilosopherState.HUNGRY:
        return f"P{philosopher_id} ficou com fome"
    if state == PhilosopherState.WAITING:
        if "garçom" in detail_lower or "garcom" in detail_lower:
            return f"P{philosopher_id} aguardando permissão do garçom"
        if "esquerdo" in detail_lower:
            return f"P{philosopher_id} tentando pegar garfo esquerdo"
        if "direito" in detail_lower:
            return f"P{philosopher_id} tentando pegar garfo direito"
        return f"P{philosopher_id} aguardando recursos"
    if state == PhilosopherState.EATING:
        return f"P{philosopher_id} começou a comer"
    if state == PhilosopherState.RELEASING:
        return f"P{philosopher_id} liberou os garfos"
    return f"P{philosopher_id} — {detail}"


def _event_style(state: PhilosopherState) -> str:
    mapping = {
        PhilosopherState.THINKING: "bright_blue",
        PhilosopherState.HUNGRY: "bright_yellow",
        PhilosopherState.WAITING: "bright_red",
        PhilosopherState.EATING: "bright_green",
        PhilosopherState.RELEASING: "bright_magenta",
    }
    return mapping.get(state, "white")
