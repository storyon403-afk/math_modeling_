"""Coulomb-counting SOC dynamics with optional temperature correction."""
from __future__ import annotations

from BatteryModel_version2.models.state import BatteryState
from BatteryModel_version2.params.soc_params import SocParams
from BatteryModel_version2.params.thermal_params import ThermalParams
from BatteryModel_version2.physics.thermal import effective_capacity


def soc_derivative(
    state: BatteryState,
    q_nom: float,
    thermal_params: ThermalParams,
    soc_params: SocParams,
    use_temperature_effect: bool = True,
) -> float:
    if use_temperature_effect:
        q_eff = effective_capacity(q_nom, state, thermal_params)
    else:
        q_eff = q_nom * state.soh

    if q_eff <= 0:
        return 0.0

    return -soc_params.eta * state.current / (3600.0 * q_eff)


def update_soc(
    state: BatteryState,
    q_nom: float,
    thermal_params: ThermalParams,
    soc_params: SocParams,
    dt: float,
    use_temperature_effect: bool = True,
) -> None:
    state.soc += soc_derivative(
        state,
        q_nom,
        thermal_params,
        soc_params,
        use_temperature_effect=use_temperature_effect,
    ) * dt
    state.soc = max(0.0, min(1.0, state.soc))
