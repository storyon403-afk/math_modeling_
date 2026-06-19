"""Shared helpers for analysis modules."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from BatteryModel.analysis.scenario_analysis import get_scenario, behavior_from_scenario
from BatteryModel.models.state import BatteryState
from BatteryModel.params.load_params import LoadPowerParams
from BatteryModel.params.electrical_params import ElectricalParams
from BatteryModel.params.thermal_params import ThermalParams
from BatteryModel.params.soc_params import SocParams
from BatteryModel.params.aging_params import AgingParams
from BatteryModel.params.resistance_params import ResistanceParams
from BatteryModel.simulation.config import SimulationConfig, SimulationResult
from BatteryModel.simulation.simulator import simulate_case


@dataclass
class ModelParameters:
    load: LoadPowerParams
    electrical: ElectricalParams
    thermal: ThermalParams
    soc: SocParams
    aging: AgingParams
    resistance: ResistanceParams


def default_parameters() -> ModelParameters:
    return ModelParameters(
        load=LoadPowerParams(),
        electrical=ElectricalParams(),
        thermal=ThermalParams(),
        soc=SocParams(),
        aging=AgingParams(),
        resistance=ResistanceParams(),
    )


def ensure_output_dir(path: str | Path) -> Path:
    output = Path(path)
    output.mkdir(parents=True, exist_ok=True)
    return output


def save_dataframe(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")


def run_scenario_case(
    scenario_name: str | int,
    *,
    initial_soc: float = 1.0,
    initial_soh: float | None = None,
    ambient_temp: float | None = None,
    behavior_overrides: dict[str, float] | None = None,
    config: SimulationConfig | None = None,
    params: ModelParameters | None = None,
    behavior_source: Any | None = None,
) -> tuple[SimulationResult, dict, ModelParameters]:
    scenario = get_scenario(scenario_name)
    params = deepcopy(params or default_parameters())
    temp = float(scenario.get("temperature", 25.0) if ambient_temp is None else ambient_temp)
    soh = float(scenario.get("soh", 1.0) if initial_soh is None else initial_soh)
    params.thermal.T_env = temp

    state = BatteryState(soc=initial_soc, soh=soh, temp=temp)
    behavior = behavior_from_scenario(scenario)
    if behavior_overrides:
        behavior = behavior.copy_with(**behavior_overrides)
    behavior = behavior_source or behavior

    config = config or SimulationConfig(dt_s=5.0, record_interval_s=30.0)
    result = simulate_case(
        state,
        behavior,
        params.load,
        params.electrical,
        params.thermal,
        params.soc,
        params.aging,
        params.resistance,
        config,
    )
    return result, scenario, params
