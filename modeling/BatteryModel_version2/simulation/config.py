"""Simulation configuration and result types."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class SimulationConfig:
    q_nom_ah: float = 3.45
    dt_s: float = 1.0
    max_time_s: float = 24 * 3600.0
    record_interval_s: float = 10.0

    soc_min: float = 0.03
    voltage_cutoff_v: float = 3.0

    use_2rc: bool = True
    use_thermal: bool = True
    use_soh: bool = True
    use_dynamic_resistance: bool = True

    stop_on_soc: bool = True
    stop_on_voltage: bool = True
    stop_on_temperature: bool = True

    def validate(self) -> None:
        if self.q_nom_ah <= 0:
            raise ValueError("q_nom_ah must be positive")
        if self.dt_s <= 0 or self.max_time_s <= 0:
            raise ValueError("dt_s and max_time_s must be positive")
        if not 0 <= self.soc_min < 1:
            raise ValueError("soc_min must be in [0, 1)")


@dataclass
class SimulationResult:
    history: list[dict[str, Any]]
    stop_reason: str
    elapsed_time_s: float
    final_state: Any

    @property
    def tte_hours(self) -> float:
        return self.elapsed_time_s / 3600.0
