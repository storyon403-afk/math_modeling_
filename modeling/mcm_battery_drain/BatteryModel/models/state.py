from dataclasses import dataclass


@dataclass
class BatteryState:

    soc: float
    soh: float

    temp: float

    voltage: float
    current: float

    v1: float
    v2: float