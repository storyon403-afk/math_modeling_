from models.behavior import UserBehavior
from modeling.mcm_battery_drain.BatteryModel.params.load_params import LoadPowerParams

def weak_signal_penalty(
    signal_quality: float,
    s_ref: float
) -> float:

    return max(
        0.0,
        s_ref - signal_quality
    )
def calc_load_power(
    user: UserBehavior,
    params: LoadPowerParams
):
    p_screen = (
        params.k0
        * params.As
        * user.brightness ** params.gamma
    )

    p_cpu = (
        params.kc
        * user.cpu ** params.alpha
    )

    p_gpu = (
        params.kg
        * user.gpu ** params.beta
    )

    penalty = weak_signal_penalty(
        user.signal_quality,
        params.s_ref
    )

    p_net = (
        params.p_net0
        + params.kr * user.network_traffic
        + params.ks * penalty
    )

    p_gps = (
        params.k_gps
        * user.gps
    )

    p_bg = (
        params.k_bg
        * user.background
    )

    p_load = (
        params.p0
        + p_screen
        + p_cpu
        + p_gpu
        + p_net
        + p_gps
        + p_bg
    )

    return {
        "total": p_load,
        "screen": p_screen,
        "cpu": p_cpu,
        "gpu": p_gpu,
        "network": p_net,
        "gps": p_gps,
        "background": p_bg,
    }