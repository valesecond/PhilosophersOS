from __future__ import annotations

from dataclasses import dataclass

from rich.align import Align
from rich.box import DOUBLE, HEAVY, ROUNDED, SIMPLE_HEAVY
from rich.columns import Columns
from rich.console import Group, RenderableType
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich.text import Text

from src.philosophers.table import DeadlockInfo, DiningTable, TableSnapshot
from src.ui.theme import STATE_ICONS, STATE_STYLES, THEME
from src.utils.constants import APP_NAME, APP_TAGLINE, APP_VERSION, STATUS_READY, STATUS_RUNNING, STATUS_STOPPED


@dataclass(slots=True)
class DashboardContext:
    snapshot: TableSnapshot
    border_style: str
    num_philosophers: int
    deadlock_info: DeadlockInfo | None = None


def render_app_banner() -> Panel:
    title = Text()
    title.append("╔", style=THEME.header_border)
    title.append("═" * 62, style=THEME.header_border)
    title.append("╗\n", style=THEME.header_border)
    title.append("║", style=THEME.header_border)
    title.append(f"{'PHILOSOPHERS OS':^62}", style=f"bold bright_white on grey23")
    title.append("║\n", style=THEME.header_border)
    title.append("║", style=THEME.header_border)
    title.append(f"{'Deadlock & Concurrency Simulator':^62}", style=THEME.muted)
    title.append("║\n", style=THEME.header_border)
    title.append("╚", style=THEME.header_border)
    title.append("═" * 62, style=THEME.header_border)
    title.append("╝", style=THEME.header_border)
    return Panel(Align.center(title), border_style=THEME.header_border, box=ROUNDED, padding=(0, 1))


def render_status_cards(*, system_online: bool, num_philosophers: int, active_threads: int = 0) -> Columns:
    cards = [
        _stat_card("Sistema", "● Online" if system_online else "○ Offline", THEME.success if system_online else THEME.danger),
        _stat_card("Versão", APP_VERSION, THEME.accent),
        _stat_card("Threads Ativas", str(active_threads), THEME.warning),
        _stat_card("Filósofos", str(num_philosophers), THEME.accent_dim),
    ]
    return Columns(cards, equal=True, expand=True)


def render_main_menu() -> Panel:
    menu = Table.grid(padding=(0, 2))
    menu.add_column(style="bold bright_white", justify="left")
    menu.add_row("  [1]  Simular Deadlock")
    menu.add_row("  [2]  Simular Solução")
    menu.add_row("  [3]  Comparar Implementações")
    menu.add_row("  [4]  Configurações")
    menu.add_row("  [5]  Arquitetura do Sistema")
    menu.add_row("  [6]  Sobre")
    menu.add_row("")
    menu.add_row("  [0]  Encerrar Sistema")
    return Panel(
        menu,
        title="[bold bright_white]MENU PRINCIPAL[/bold bright_white]",
        border_style=THEME.menu_border,
        box=HEAVY,
        padding=(1, 2),
    )


def render_philosopher_table(snapshot: TableSnapshot) -> Table:
    table = Table(
        title="[bold]Estado dos Filósofos[/bold]",
        expand=True,
        box=ROUNDED,
        header_style=f"bold {THEME.accent}",
        border_style=THEME.card_border,
        show_lines=True,
    )
    table.add_column("Filósofo", justify="center", style="bold white", width=10)
    table.add_column("Estado", justify="center", min_width=14)
    table.add_column("Recursos", justify="center", style="bright_green", min_width=12)

    for activity in snapshot.activities:
        state_value = activity.state.value
        icon = STATE_ICONS.get(state_value, "○")
        style = STATE_STYLES.get(state_value, "white")
        table.add_row(
            f"P{activity.philosopher_id}",
            f"[{style}]{icon} {state_value}[/{style}]",
            activity.resources,
        )
    return table


def render_execution_stats(snapshot: TableSnapshot, num_philosophers: int) -> Panel:
    grid = Table.grid(expand=True, padding=(0, 1))
    grid.add_column(style=THEME.stat_label, ratio=1)
    grid.add_column(style=THEME.stat_value, ratio=1)
    grid.add_row("⏱  Tempo de execução", f"{snapshot.elapsed:0.2f}s")
    grid.add_row("🍽  Refeições realizadas", str(snapshot.meals))
    grid.add_row("🧵  Threads ativas", str(snapshot.active_threads))
    grid.add_row("⚠  Deadlocks detectados", str(snapshot.deadlocks))
    grid.add_row("⚙  Estratégia", snapshot.strategy)
    grid.add_row("👥  Filósofos", str(num_philosophers))
    grid.add_row("●  Status", _status_label(snapshot.status))
    return Panel(grid, title="[bold]Métricas[/bold]", border_style=THEME.card_border, box=ROUNDED)


def render_execution_dashboard(context: DashboardContext) -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=3),
    )
    layout["header"].update(
        Panel(
            Align.center(
                Text(f"◆ {APP_NAME} — Monitor de Execução ◆", style=f"bold {THEME.title}")
            ),
            border_style=context.border_style,
            box=HEAVY,
        )
    )

    progress = _execution_progress(context.snapshot)
    layout["body"].split_row(
        Layout(Panel(progress, title="[bold]Progresso[/bold]", border_style=THEME.card_border, box=ROUNDED), ratio=1),
        Layout(render_execution_stats(context.snapshot, context.num_philosophers), ratio=1),
    )

    body_bottom = Layout()
    body_bottom.split_column(
        Layout(render_philosopher_table(context.snapshot), ratio=3),
    )
    layout["body"].split_column(
        Layout(
            Columns(
                [
                    Panel(progress, title="[bold]Progresso[/bold]", border_style=THEME.card_border, box=ROUNDED),
                    render_execution_stats(context.snapshot, context.num_philosophers),
                ],
                equal=True,
                expand=True,
            ),
            size=8,
        ),
        Layout(render_philosopher_table(context.snapshot)),
    )

    if context.deadlock_info is not None:
        layout["footer"].update(render_deadlock_alert(context.deadlock_info))
    else:
        layout["footer"].update(
            Panel(
                Align.center(Text("Monitoramento em tempo real — aguardando eventos...", style=THEME.muted)),
                border_style=context.border_style,
                box=SIMPLE_HEAVY,
            )
        )
    return layout


def build_execution_panel(table: DiningTable, *, border_style: str) -> Panel:
    snapshot = table.snapshot()
    deadlock_info = table.deadlock_info
    context = DashboardContext(
        snapshot=snapshot,
        border_style=border_style,
        num_philosophers=table.num_philosophers,
        deadlock_info=deadlock_info,
    )

    progress = _execution_progress(snapshot)
    top_row = Columns(
        [
            Panel(progress, title="[bold]Progresso[/bold]", border_style=THEME.card_border, box=ROUNDED),
            render_execution_stats(snapshot, table.num_philosophers),
        ],
        equal=True,
        expand=True,
    )

    sections: list[RenderableType] = [
        Panel(
            Align.center(Text(f"◆ {APP_NAME} — Monitor de Execução ◆", style=f"bold {THEME.title}")),
            border_style=border_style,
            box=HEAVY,
        ),
        top_row,
        render_philosopher_table(snapshot),
    ]

    if deadlock_info is not None:
        sections.append(render_deadlock_alert(deadlock_info))

    return Panel(
        Group(*sections),
        title=f"[bold]{APP_TAGLINE}[/bold]",
        border_style=border_style,
        box=DOUBLE,
        padding=(0, 1),
    )


def render_deadlock_alert(info: DeadlockInfo) -> Panel:
    content = Table.grid(expand=True, padding=(0, 1))
    content.add_column(style=THEME.danger)
    content.add_column(style="bold white")
    content.add_row("═══════════════════════════════════════════════", "")
    content.add_row("⚠  DEADLOCK DETECTADO", "")
    content.add_row("═══════════════════════════════════════════════", "")
    content.add_row("", "")
    content.add_row("Filósofos bloqueados:", ", ".join(f"P{pid}" for pid in info.blocked_philosophers))
    content.add_row("Recursos aguardados:", info.waiting_resources_summary())
    content.add_row("Tempo de espera:", f"{info.wait_time:.2f}s")
    content.add_row("Condição detectada:", "Espera circular — todos aguardam o segundo garfo")
    return Panel(content, border_style=THEME.deadlock_border, box=HEAVY, title="[bold red]ALERTA CRÍTICO[/bold red]")


def render_deadlock_summary(info: DeadlockInfo, result: dict) -> Panel:
    table = Table(box=ROUNDED, expand=True, header_style=f"bold {THEME.danger}")
    table.add_column("Indicador", style=THEME.stat_label)
    table.add_column("Valor", style="bold white")
    table.add_row("Filósofos bloqueados", ", ".join(f"P{pid}" for pid in info.blocked_philosophers))
    table.add_row("Recursos aguardados", info.waiting_resources_summary())
    table.add_row("Tempo de espera", f"{info.wait_time:.2f}s")
    table.add_row("Refeições antes do bloqueio", str(result.get("meals", 0)))
    table.add_row("Tempo total", f"{float(result.get('elapsed', 0.0)):0.2f}s")
    return Panel(
        Group(render_deadlock_alert(info), table),
        title="[bold red]Relatório de Deadlock[/bold red]",
        border_style=THEME.deadlock_border,
        box=DOUBLE,
    )


def render_architecture_panel(config) -> Panel:
    from src.utils.config import SimulationConfig

    cfg: SimulationConfig = config
    waiter_limit = min(cfg.waiter_limit, max(1, cfg.num_philosophers - 1))

    overview = Table.grid(expand=True, padding=(0, 1))
    overview.add_column(style=THEME.stat_label, ratio=1)
    overview.add_column(style=THEME.stat_value, ratio=2)
    overview.add_row("Threads (filósofos)", str(cfg.num_philosophers))
    overview.add_row("Locks (garfos)", str(cfg.num_philosophers))
    overview.add_row("Semáforos", "1 (garçom)")
    overview.add_row("Barriers", "2 (início + sincronização deadlock)")
    overview.add_row("Estratégia de solução", f"Garçom — máx. {waiter_limit} filósofos simultâneos")
    overview.add_row("Estratégia de deadlock", "Aquisição simultânea do garfo esquerdo")

    flow = Table(box=ROUNDED, expand=True, show_lines=True, header_style=f"bold {THEME.accent}")
    flow.add_column("Etapa", style=THEME.stat_label)
    flow.add_column("Descrição")
    flow.add_row("1. THINKING", "Filósofo pensa por tempo aleatório")
    flow.add_row("2. HUNGRY", "Filósofo fica com fome e deseja comer")
    flow.add_row("3. WAITING", "Tenta adquirir garfo esquerdo e direito (região crítica)")
    flow.add_row("4. EATING", "Consome refeição com ambos os garfos")
    flow.add_row("5. RELEASING", "Libera garfos para outros filósofos")

    resources = Table(box=ROUNDED, expand=True, header_style=f"bold {THEME.accent}")
    resources.add_column("Recurso")
    resources.add_column("Tipo")
    resources.add_column("Função")
    for index in range(cfg.num_philosophers):
        resources.add_row(f"F{index}", "threading.Lock", "Exclusão mútua do garfo")
    resources.add_row("Garçom", "threading.Semaphore", "Limita filósofos na região crítica")
    resources.add_row("state_lock", "threading.Lock", "Protege estado compartilhado da mesa")

    return Panel(
        Group(
            Panel(overview, title="[bold]Visão Geral[/bold]", border_style=THEME.card_border, box=ROUNDED),
            Panel(flow, title="[bold]Fluxo de Execução[/bold]", border_style=THEME.card_border, box=ROUNDED),
            Panel(resources, title="[bold]Recursos Compartilhados[/bold]", border_style=THEME.card_border, box=ROUNDED),
        ),
        title="[bold bright_white]Arquitetura do Sistema[/bold bright_white]",
        border_style=THEME.border,
        box=DOUBLE,
    )


def _stat_card(label: str, value: str, value_style: str) -> Panel:
    body = Table.grid(expand=True)
    body.add_row(Text(label, style=THEME.muted))
    body.add_row(Text(value, style=value_style))
    return Panel(body, border_style=THEME.card_border, box=ROUNDED, padding=(0, 1))


def _execution_progress(snapshot: TableSnapshot) -> Progress:
    total = max(snapshot.meals + snapshot.deadlocks, 1)
    completed = snapshot.meals
    progress = Progress(
        SpinnerColumn(style=THEME.accent),
        TextColumn("[bold blue]Simulação[/bold blue]"),
        BarColumn(bar_width=30, complete_style=THEME.success, finished_style=THEME.success),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        expand=True,
    )
    progress.add_task("run", total=total, completed=min(completed, total))
    return progress


def _status_label(status: str) -> str:
    mapping = {
        STATUS_READY: f"[{THEME.accent_dim}]Pronto[/{THEME.accent_dim}]",
        STATUS_RUNNING: f"[{THEME.success}]Em execução[/{THEME.success}]",
        STATUS_STOPPED: f"[{THEME.danger}]Encerrado[/{THEME.danger}]",
    }
    return mapping.get(status, status)
