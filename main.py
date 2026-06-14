from __future__ import annotations

import sys

from src.app import run_app


def _configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8")
            except (OSError, ValueError):
                pass


if __name__ == "__main__":
    _configure_stdio()
    run_app()
