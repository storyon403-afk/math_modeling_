"""Battery state container."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BatteryState:
    time: float = 0.0
    soc: float = 1.0
    soh: float = 1.0
    temp: float = 25.0
    voltage: float = 4.2
    current: float = 0.0
    v1: float = 0.0
    v2: float = 0.0

    def copy(self) -> "BatteryState":
        return BatteryState(**self.__dict__)
