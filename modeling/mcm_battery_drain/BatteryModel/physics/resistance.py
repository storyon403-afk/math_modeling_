from math import exp

from modeling.mcm_battery_drain.BatteryModel.models.state import BatteryState
from modeling.mcm_battery_drain.BatteryModel.params.resistance_params import ResistanceParams

def calc_resistance(
    r_ref: float,
    state: BatteryState,
    params: ResistanceParams
) -> float:

    return (
        r_ref
        * (
            1
            + params.a
            * (1 - state.soh)
        )
        * exp(
            params.lam
            * (
                params.T_ref
                - state.temp
            )
        )
        * (
            1
            + params.c
            * (
                state.soc
                - params.z_ref
            ) ** 2
        )
    )