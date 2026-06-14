from __future__ import annotations

import sys

from src.views.main_menu_view import MainMenuView


def _configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8")
            except (OSError, ValueError):
                pass


def run_app() -> None:
    _configure_stdio()
    MainMenuView().show()
