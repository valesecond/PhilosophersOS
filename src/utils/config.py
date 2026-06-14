from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from src.utils.helpers import project_root


CONFIG_FILE = project_root() / "config.json"


@dataclass(slots=True)
class SimulationConfig:
    num_philosophers: int = 5
    thinking_time: float = 0.8
    eating_time: float = 0.6
    simulation_speed: float = 1.0
    cycles: int = 3
    deadlock_timeout: float = 3.0
    deadlock_poll_interval: float = 0.2
    waiter_limit: int = 4

    def validated(self) -> "SimulationConfig":
        return SimulationConfig(
            num_philosophers=max(2, self.num_philosophers),
            thinking_time=max(0.05, self.thinking_time),
            eating_time=max(0.05, self.eating_time),
            simulation_speed=max(0.1, self.simulation_speed),
            cycles=max(1, self.cycles),
            deadlock_timeout=max(0.5, self.deadlock_timeout),
            deadlock_poll_interval=max(0.05, self.deadlock_poll_interval),
            waiter_limit=max(1, self.waiter_limit),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "num_philosophers": self.num_philosophers,
            "thinking_time": self.thinking_time,
            "eating_time": self.eating_time,
            "simulation_speed": self.simulation_speed,
            "cycles": self.cycles,
            "deadlock_timeout": self.deadlock_timeout,
            "deadlock_poll_interval": self.deadlock_poll_interval,
            "waiter_limit": self.waiter_limit,
        }


DEFAULT_CONFIG = SimulationConfig()


def load_config() -> SimulationConfig:
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    try:
        payload = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return DEFAULT_CONFIG

    return SimulationConfig(
        num_philosophers=int(payload.get("num_philosophers", DEFAULT_CONFIG.num_philosophers)),
        thinking_time=float(payload.get("thinking_time", DEFAULT_CONFIG.thinking_time)),
        eating_time=float(payload.get("eating_time", DEFAULT_CONFIG.eating_time)),
        simulation_speed=float(payload.get("simulation_speed", DEFAULT_CONFIG.simulation_speed)),
        cycles=int(payload.get("cycles", DEFAULT_CONFIG.cycles)),
        deadlock_timeout=float(payload.get("deadlock_timeout", DEFAULT_CONFIG.deadlock_timeout)),
        deadlock_poll_interval=float(payload.get("deadlock_poll_interval", DEFAULT_CONFIG.deadlock_poll_interval)),
        waiter_limit=int(payload.get("waiter_limit", DEFAULT_CONFIG.waiter_limit)),
    ).validated()


def save_config(config: SimulationConfig) -> None:
    CONFIG_FILE.write_text(json.dumps(config.validated().to_dict(), indent=2), encoding="utf-8")
