from math import sqrt

from modeling.mcm_battery_drain.BatteryModel.models.state import BatteryState


def ocv(
    soc: float
) -> float:
    """
    开路电压模型
    后续可替换成查表
    """

    return 3.0 + 1.2 * soc


def calc_current(
    state: BatteryState,
    p_load: float,
    r0: float
) -> float:
    """
    论文公式(4.1.6)
    """

    u_oc = ocv(state.soc)

    A = (
        u_oc
        - state.v1
        - state.v2
    )

    delta = (
        A * A
        - 4 * r0 * p_load
    )

    if delta <= 0:
        delta = 0

    current = (
        A
        - sqrt(delta)
    ) / (
        2 * r0
    )

    return current


def update_v1(
    state: BatteryState,
    r1: float,
    c1: float,
    dt: float
):
    """
    论文公式(4.1.3)
    """

    dv1_dt = (
        -state.v1
        / (r1 * c1)
        + state.current
        / c1
    )

    state.v1 += dv1_dt * dt


def update_v2(
    state: BatteryState,
    r2: float,
    c2: float,
    dt: float
):
    """
    论文公式(4.1.4)
    """

    dv2_dt = (
        -state.v2
        / (r2 * c2)
        + state.current
        / c2
    )

    state.v2 += dv2_dt * dt


def update_voltage(
    state: BatteryState,
    r0: float
):
    """
    论文公式(4.1.2)
    """

    u_oc = ocv(state.soc)

    state.voltage = (
        u_oc
        - state.current * r0
        - state.v1
        - state.v2
    )