from modeling.mcm_battery_drain.BatteryModel.models.state import BatteryState
from modeling.mcm_battery_drain.BatteryModel.models.behavior import UserBehavior

from modeling.mcm_battery_drain.BatteryModel.physics.load import calc_load_power

from modeling.mcm_battery_drain.BatteryModel.physics.electrical import (
    calc_current,
    update_v1,
    update_v2,
    update_voltage
)

from modeling.mcm_battery_drain.BatteryModel.physics.thermal import (
    update_temperature
)

from modeling.mcm_battery_drain.BatteryModel.physics.soc import (
    update_soc
)

from modeling.mcm_battery_drain.BatteryModel.physics.soh import (
    update_soh
)

from modeling.mcm_battery_drain.BatteryModel.physics.resistance import (
    calc_resistance
)

def simulate(
    state: BatteryState,
    user: UserBehavior,
    load_params,
    electrical_params,
    thermal_params,
    soc_params,
    aging_params,
    resistance_params,
    q_nom: float,
    dt: float,
    total_time: float
):
    history = []
    steps = int(
        total_time / dt
        )

    for _ in range(steps):
            load_info = calc_load_power(
            user,
            load_params
            )

            p_load = load_info["total"]

            R0 = calc_resistance(
                electrical_params.R0_ref,
                state,
                resistance_params
            )

            R1 = calc_resistance(
                electrical_params.R1_ref,
                state,
                resistance_params
            )

            R2 = calc_resistance(
                electrical_params.R2_ref,
                state,
                resistance_params
            )

            state.current = calc_current(
                state,
                p_load,
                R0
            )
            update_v1(
                state,
                R1,
                electrical_params.C1,
                dt
            )

            update_v2(
                state,
                R2,
                electrical_params.C2,
                dt
            )

            update_voltage(
                state,
                R0
            )

            update_temperature(
                state,
                thermal_params,
                R0,
                R1,
                R2,
                dt
            )

            update_soc(
                state,
                q_nom,
                thermal_params,
                soc_params,
                dt
            )

            update_soh(
                state,
                q_nom,
                aging_params,
                dt
            )

            state.time += dt

            history.append({
                "time": state.time,
                "soc": state.soc,
                "soh": state.soh,
                "temp": state.temp,
                "voltage": state.voltage,
                "current": state.current,
                "v1": state.v1,
                "v2": state.v2,
                "power": p_load
            })

            if state.soc <= 0.05:
                break

            if state.voltage <= 3.0:
                break

            if state.temp >= thermal_params.T_max:
                break

            return history