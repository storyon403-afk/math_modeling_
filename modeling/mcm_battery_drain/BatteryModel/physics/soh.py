from math import exp

from modeling.mcm_battery_drain.BatteryModel.models.state import BatteryState

class AgingParams:

    def __init__(self):

        # 老化速率系数
        self.k0 = 1e-8

        # 活化能(J/mol)
        self.Ea = 35000.0

        # 气体常数
        self.Rg = 8.314

        # C倍率指数
        self.mu = 1.2

        # SOC偏离惩罚
        self.rho = 2.0

        # 最佳SOC区间
        self.z_mid = 0.5

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