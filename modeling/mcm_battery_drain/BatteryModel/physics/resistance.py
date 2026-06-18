from math import exp

from modeling.mcm_battery_drain.BatteryModel.models.state import BatteryState


class ResistanceParams:

    def __init__(self):

        self.T_ref = 25.0

        self.z_ref = 0.5

        # SOH影响系数
        self.a = 3.0

        # 温度影响系数
        self.lam = 0.03

        # SOC影响系数
        self.c = 1.0


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