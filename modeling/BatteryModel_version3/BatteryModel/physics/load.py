"""Phone component power model."""
from __future__ import annotations

from BatteryModel.models.behavior import UserBehavior
from BatteryModel.params.load_params import LoadPowerParams


def normalize_traffic(value: float) -> float:
    """Accept both normalized 0--1 and legacy 0--10 traffic inputs."""
    value = float(value)
    if value > 1.0:
        value /= 10.0
    return min(max(value, 0.0), 1.0)


def weak_signal_penalty(signal_quality: float, _legacy_s_ref: float = 0.7) -> float:
    """Return a 0--1 radio penalty for signal quality on the 1--5 scale."""
    quality = min(max(float(signal_quality), 1.0), 5.0)
    return (5.0 - quality) / 4.0


def calc_load_power(user: UserBehavior, params: LoadPowerParams) -> dict[str, float]:
    user = user.clipped()
    traffic = normalize_traffic(user.network_traffic)

    p_screen = params.k0 * params.As * user.brightness ** params.gamma
    p_cpu = params.kc * user.cpu ** params.alpha
    p_gpu = params.kg * user.gpu ** params.beta

    penalty = weak_signal_penalty(user.signal_quality, params.s_ref)
    p_net = params.p_net0 + params.kr * traffic + params.ks * penalty
    p_gps = params.k_gps * user.gps
    p_bg = params.k_bg * user.background

    p_load = params.p0 + p_screen + p_cpu + p_gpu + p_net + p_gps + p_bg

    return {
        "total": float(p_load),
        "base": float(params.p0),
        "screen": float(p_screen),
        "cpu": float(p_cpu),
        "gpu": float(p_gpu),
        "network": float(p_net),
        "gps": float(p_gps),
        "background": float(p_bg),
    }
