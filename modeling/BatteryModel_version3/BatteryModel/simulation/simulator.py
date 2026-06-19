"""Core battery digital-twin simulation."""
from __future__ import annotations

from collections.abc import Callable
from typing import Union

from BatteryModel.models.state import BatteryState
from BatteryModel.models.behavior import UserBehavior
from BatteryModel.physics.load import calc_load_power
from BatteryModel.physics.electrical import calc_current, update_v1, update_v2, update_voltage, ocv
from BatteryModel.physics.tte import calc_tte
from BatteryModel.physics.thermal import update_temperature
from BatteryModel.physics.soc import update_soc
from BatteryModel.physics.soh import update_soh
from BatteryModel.physics.resistance import calc_resistance
from BatteryModel.simulation.config import SimulationConfig, SimulationResult

BehaviorSource = Union[UserBehavior, Callable[[float], UserBehavior]]


def _resolve_behavior(source: BehaviorSource, time_s: float) -> UserBehavior:
    behavior = source(time_s) if callable(source) else source
    if not isinstance(behavior, UserBehavior):
        raise TypeError("behavior source must return UserBehavior")
    return behavior.clipped()


def _stop_reason(state: BatteryState, config: SimulationConfig, t_max: float) -> str | None:
    if config.stop_on_soc and state.soc <= config.soc_min:
        return "SOC threshold"
    if config.stop_on_voltage and state.voltage <= config.voltage_cutoff_v:
        return "voltage cutoff"
    if config.stop_on_temperature and state.temp >= t_max:
        return "thermal protection"
    return None


def simulate_case(
    state: BatteryState,
    behavior: BehaviorSource,
    load_params,
    electrical_params,
    thermal_params,
    soc_params,
    aging_params,
    resistance_params,
    config: SimulationConfig | None = None,
) -> SimulationResult:
    """Run a simulation until a physical stop condition or ``max_time_s``.

    The original project estimated TTE from instantaneous energy/power after a
    fixed one-hour run. This function instead reports the actual simulated time
    required to reach SOC, voltage, or thermal limits.
    """
    config = config or SimulationConfig()
    config.validate()

    # Keep initial voltage consistent with the selected initial SOC.
    state.soc = min(max(float(state.soc), 0.0), 1.0)
    state.soh = min(max(float(state.soh), 0.0), 1.0)
    state.voltage = ocv(state.soc) - state.v1 - state.v2

    history: list[dict] = []
    record_every = max(1, int(round(config.record_interval_s / config.dt_s)))
    max_steps = int(config.max_time_s / config.dt_s)
    stop_reason = _stop_reason(state, config, thermal_params.T_max)

    for step in range(max_steps):
        if stop_reason is not None:
            break

        user = _resolve_behavior(behavior, state.time)
        load_info = calc_load_power(user, load_params)
        p_load = load_info["total"]

        if config.use_dynamic_resistance:
            r0 = calc_resistance(electrical_params.R0_ref, state, resistance_params)
            r1 = calc_resistance(electrical_params.R1_ref, state, resistance_params)
            r2 = calc_resistance(electrical_params.R2_ref, state, resistance_params)
        else:
            r0 = electrical_params.R0_ref
            r1 = electrical_params.R1_ref
            r2 = electrical_params.R2_ref

        state.current = calc_current(state, p_load, max(r0, 1e-9))

        if config.use_2rc:
            update_v1(state, max(r1, 1e-9), electrical_params.C1, config.dt_s)
            update_v2(state, max(r2, 1e-9), electrical_params.C2, config.dt_s)
        else:
            state.v1 = 0.0
            state.v2 = 0.0

        update_voltage(state, r0)

        if config.use_thermal:
            update_temperature(state, thermal_params, r0, r1, r2, config.dt_s, p_load=p_load)
        else:
            state.temp = thermal_params.T_env

        # SOH always affects usable capacity when supplied as an initial state;
        # ``use_soh`` controls only dynamic degradation during this discharge.
        update_soc(
            state,
            config.q_nom_ah,
            thermal_params,
            soc_params,
            config.dt_s,
            use_temperature_effect=config.use_thermal,
        )
        if config.use_soh:
            update_soh(state, config.q_nom_ah, aging_params, config.dt_s)

        state.time += config.dt_s
        stop_reason = _stop_reason(state, config, thermal_params.T_max)

        if step % record_every == 0 or stop_reason is not None or step == max_steps - 1:
            row = {
                "time": state.time,
                "soc": state.soc,
                "soh": state.soh,
                "temp": state.temp,
                "voltage": state.voltage,
                "current": state.current,
                "v1": state.v1,
                "v2": state.v2,
                "R0": r0,
                "R1": r1,
                "R2": r2,
                "power": p_load,
                "tte_estimate": calc_tte(state, config.q_nom_ah, p_load),
                "brightness": user.brightness,
                "cpu_load": user.cpu,
                "gpu_load": user.gpu,
                "network_traffic": user.network_traffic,
                "signal_quality": user.signal_quality,
                "gps_flag": user.gps,
            }
            for key, value in load_info.items():
                if key != "total":
                    row[f"power_{key}"] = value
            history.append(row)

    if stop_reason is None:
        stop_reason = "maximum simulation time"

    if history:
        history[-1]["stop_reason"] = stop_reason
        history[-1]["actual_tte_s"] = state.time

    return SimulationResult(
        history=history,
        stop_reason=stop_reason,
        elapsed_time_s=state.time,
        final_state=state.copy(),
    )


def simulate(
    state: BatteryState,
    user: BehaviorSource,
    load_params,
    electrical_params,
    thermal_params,
    soc_params,
    aging_params,
    resistance_params,
    q_nom: float = 3.45,
    dt: float = 1.0,
    total_time: float = 3600.0,
):
    """Backward-compatible wrapper returning only the history list."""
    config = SimulationConfig(
        q_nom_ah=q_nom,
        dt_s=dt,
        max_time_s=total_time,
        record_interval_s=dt,
    )
    result = simulate_case(
        state, user, load_params, electrical_params, thermal_params,
        soc_params, aging_params, resistance_params, config,
    )
    # Preserve the old key used by existing plotting code.
    for row in result.history:
        row["tte"] = row["tte_estimate"]
    return result.history
