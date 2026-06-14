from __future__ import annotations

import os
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def dataclass_to_dict(value: Any) -> dict[str, Any]:
    if is_dataclass(value):
        return asdict(value)
    raise TypeError("Expected dataclass instance")
