from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UITheme:
    accent: str = "bright_cyan"
    accent_dim: str = "cyan"
    success: str = "bright_green"
    warning: str = "bright_yellow"
    danger: str = "bright_red"
    muted: str = "dim white"
    title: str = "bold bright_white"
    border: str = "bright_blue"
    menu_border: str = "magenta"
    card_border: str = "blue"
    header_border: str = "bright_cyan"
    deadlock_border: str = "bright_red"
    solution_border: str = "bright_green"
    stat_label: str = "cyan"
    stat_value: str = "bold white"


THEME = UITheme()

STATE_STYLES = {
    "PENSANDO": "bright_blue",
    "COM FOME": "bright_yellow",
    "ESPERANDO": "bright_red",
    "COMENDO": "bright_green",
    "LIBERANDO": "bright_magenta",
}

STATE_ICONS = {
    "PENSANDO": "◉",
    "COM FOME": "◈",
    "ESPERANDO": "◌",
    "COMENDO": "●",
    "LIBERANDO": "◇",
}
