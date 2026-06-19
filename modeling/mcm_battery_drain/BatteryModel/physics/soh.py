from math import exp

from modeling.mcm_battery_drain.BatteryModel.models.state import BatteryState
from modeling.mcm_battery_drain.BatteryModel.params.aging_params import AgingParams

def soc_stress_factor(
    soc: float,
    params: AgingParams
) -> float:

    return (
        1
        + params.rho
        * (soc - params.z_mid) ** 2
    )

def soh_derivative(
    state: BatteryState,
    q_nom: float,
    params: AgingParams
) -> float:

    arrhenius = exp(
        -params.Ea
        / (
            params.Rg
            * (
                state.temp
                + 273.15
            )
        )
    )

    c_rate = (
        abs(state.current)
        / q_nom
    ) ** params.mu

    soc_factor = soc_stress_factor(
        state.soc,
        params
    )

    dsoh_dt = (
        -params.k0
        / q_nom
        * arrhenius
        * c_rate
        * soc_factor
    )

    return dsoh_dt

def update_soh(
    state: BatteryState,
    q_nom: float,
    params: AgingParams,
    dt: float
):

    dsoh_dt = soh_derivative(
        state,
        q_nom,
        params
    )

    state.soh += dsoh_dt * dt

    state.soh = max(
        0.0,
        min(
            1.0,
            state.soh
        )
    )