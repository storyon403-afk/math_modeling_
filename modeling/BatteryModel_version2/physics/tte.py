from BatteryModel_version2.models.state import BatteryState


def calc_tte(
    state: BatteryState,
    q_nom: float,
    power: float
):
    """
    返回剩余时间(秒)
    """

    if power <= 0:
        return float("inf")

    # 剩余电量(Wh)

    remaining_energy = (
        state.soc
        * state.soh
        * q_nom
        * state.voltage
    )

    # TTE(h)

    tte_hour = (
        remaining_energy
        / power
    )

    return tte_hour * 3600

