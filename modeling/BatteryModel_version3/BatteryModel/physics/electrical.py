"""Thevenin 2RC electrical model."""
from __future__ import annotations

from math import sqrt, exp
from BatteryModel.models.state import BatteryState


def ocv(soc: float) -> float:
    """Smooth monotonic OCV approximation for a single Li-ion cell."""
    z = min(max(float(soc), 0.0), 1.0)
    # A mild S-shape is more realistic than the original strictly linear OCV.
    return 3.0 + 1.05 * z + 0.15 * z * z


def calc_current(state: BatteryState, p_load: float, r0: float) -> float:
    """Solve P = I(U_oc - V1 - V2 - I R0) for the physical low-current root."""
    if p_load <= 0:
        return 0.0
    a = max(ocv(state.soc) - state.v1 - state.v2, 1e-6)
    r0 = max(float(r0), 1e-9)
    discriminant = a * a - 4.0 * r0 * p_load
    if discriminant <= 0.0:
        # Requested power exceeds the static maximum-power point. Returning the
        # MPP current makes the terminal voltage collapse and triggers cutoff.
        return a / (2.0 * r0)
    return (a - sqrt(discriminant)) / (2.0 * r0)


def _update_rc_voltage(previous: float, current: float, resistance: float, capacitance: float, dt: float) -> float:
    """Exact zero-order-hold discretization of a first-order RC branch.

    This avoids the explicit-Euler instability that occurred when dt exceeded
    the fast branch time constant R1*C1 (5 s in the default parameters).
    """
    tau = max(resistance * capacitance, 1e-12)
    decay = exp(-dt / tau)
    return previous * decay + current * resistance * (1.0 - decay)


def update_v1(state: BatteryState, r1: float, c1: float, dt: float) -> None:
    state.v1 = _update_rc_voltage(state.v1, state.current, r1, c1, dt)


def update_v2(state: BatteryState, r2: float, c2: float, dt: float) -> None:
    state.v2 = _update_rc_voltage(state.v2, state.current, r2, c2, dt)


def update_voltage(state: BatteryState, r0: float) -> None:
    state.voltage = ocv(state.soc) - state.current * r0 - state.v1 - state.v2
