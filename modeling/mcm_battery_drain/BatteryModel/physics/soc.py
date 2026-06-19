from modeling.mcm_battery_drain.BatteryModel.models.state import BatteryState
from modeling.mcm_battery_drain.BatteryModel.params.soc_params import SocParams
from modeling.mcm_battery_drain.BatteryModel.params.thermal_params import ThermalParams
from modeling.mcm_battery_drain.BatteryModel.physics.thermal import effective_capacity

def soc_derivative(
    state: BatteryState,
    q_nom: float,
    thermal_params: ThermalParams,
    soc_params: SocParams
):

    q_eff = effective_capacity(
        q_nom,
        state,
        thermal_params
    )

    if q_eff <= 0:
        return 0.0

    dz_dt = (
        -soc_params.eta
        * state.current
        / (
            3600
            * q_eff
        )
    )

    return dz_dt

def update_soc(
    state: BatteryState,
    q_nom: float,
    thermal_params: ThermalParams,
    soc_params: SocParams,
    dt: float
):

    dz_dt = soc_derivative(
        state,
        q_nom,
        thermal_params,
        soc_params
    )

    state.soc += dz_dt * dt

    state.soc = max(
        0.0,
        min(
            1.0,
            state.soc
        )
    )