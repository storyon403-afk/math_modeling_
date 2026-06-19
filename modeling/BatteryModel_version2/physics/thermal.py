"""Lumped electro-thermal battery model."""
from __future__ import annotations

from BatteryModel_version2.models.state import BatteryState
from BatteryModel_version2.params.thermal_params import ThermalParams


def heat_generation(
    state: BatteryState,
    r0: float,
    r1: float,
    r2: float,
    p_load: float = 0.0,
    device_heat_fraction: float = 0.0,
) -> float:
    electrical_heat = (
        state.current ** 2 * r0
        + state.v1 ** 2 / max(r1, 1e-12)
        + state.v2 ** 2 / max(r2, 1e-12)
    )
    coupled_device_heat = max(device_heat_fraction, 0.0) * max(p_load, 0.0)
    return electrical_heat + coupled_device_heat


def update_temperature(
    state: BatteryState,
    params: ThermalParams,
    r0: float,
    r1: float,
    r2: float,
    dt: float,
    p_load: float = 0.0,
) -> None:
    q_gen = heat_generation(
        state,
        r0,
        r1,
        r2,
        p_load=p_load,
        device_heat_fraction=params.device_heat_fraction,
    )
    dT_dt = (q_gen - params.h * (state.temp - params.T_env)) / params.C_th
    state.temp += dT_dt * dt


def low_temp_factor(temp: float, params: ThermalParams) -> float:
    return max(0.05, 1.0 - params.a_low * max(0.0, params.T_ref - temp))


def hot_temp_factor(temp: float, params: ThermalParams) -> float:
    return max(0.0, 1.0 - params.a_hot * max(0.0, temp - params.T_hot))


def effective_capacity(q_nom: float, state: BatteryState, params: ThermalParams) -> float:
    return q_nom * state.soh * low_temp_factor(state.temp, params)
