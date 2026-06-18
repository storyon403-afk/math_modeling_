
from modeling.mcm_battery_drain.BatteryModel.models.state import BatteryState
from modeling.mcm_battery_drain.BatteryModel.params.thermal_params import ThermalParams

def heat_generation(
    state: BatteryState,
    r0: float,
    r1: float,
    r2: float
) -> float:

    return (
        state.current ** 2 * r0
        + state.v1 ** 2 / r1
        + state.v2 ** 2 / r2
    )

def update_temperature(
    state: BatteryState,
    params: ThermalParams,
    r0: float,
    r1: float,
    r2: float,
    dt: float
):

    q_gen = heat_generation(
        state,
        r0,
        r1,
        r2
    )

    dT_dt = (
        q_gen
        - params.h
        * (
            state.temp
            - params.T_env
        )
    ) / params.C_th

    state.temp += dT_dt * dt

def low_temp_factor(
    temp: float,
    params: ThermalParams
):

    return (
        1
        - params.a_low
        * max(
            0,
            params.T_ref - temp
        )
    )
def hot_temp_factor(
    temp: float,
    params: ThermalParams
):

    return max(
        0,
        1
        - params.a_hot
        * max(
            0,
            temp - params.T_hot
        )
    )

def effective_capacity(
    q_nom: float,
    state: BatteryState,
    params: ThermalParams
):

    return (
        q_nom
        * state.soh
        * low_temp_factor(
            state.temp,
            params
        )
    )