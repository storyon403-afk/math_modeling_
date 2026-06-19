"""Representative phone-use scenarios and helpers."""
from __future__ import annotations

from copy import deepcopy
from BatteryModel_version2.models.behavior import UserBehavior


# Values are normalized workloads. ``network_traffic`` uses 0--1 here, while
# the load model remains compatible with the original 0--10 inputs.
SCENARIO_LIBRARY = {
    "office": {
        "name": "Light daily use",
        "brightness": 0.35,
        "cpu": 0.20,
        "gpu": 0.05,
        "network_traffic": 0.20,
        "signal_quality": 5.0,
        "gps": 0.0,
        "background": 0.10,
        "temperature": 25.0,
        "soh": 1.0,
    },
    "video": {
        "name": "Video streaming (Wi-Fi)",
        "brightness": 0.65,
        "cpu": 0.35,
        "gpu": 0.18,
        "network_traffic": 0.35,
        "signal_quality": 5.0,
        "gps": 0.0,
        "background": 0.12,
        "temperature": 25.0,
        "soh": 1.0,
    },
    "navigation": {
        "name": "Navigation",
        "brightness": 0.65,
        "cpu": 0.45,
        "gpu": 0.10,
        "network_traffic": 0.45,
        "signal_quality": 2.0,
        "gps": 1.0,
        "background": 0.12,
        "temperature": 25.0,
        "soh": 1.0,
    },
    "game": {
        "name": "Mobile game",
        "brightness": 0.75,
        "cpu": 0.85,
        "gpu": 0.75,
        "network_traffic": 0.15,
        "signal_quality": 4.0,
        "gps": 0.0,
        "background": 0.15,
        "temperature": 25.0,
        "soh": 1.0,
    },
    "standby": {
        "name": "Standby",
        "brightness": 0.0,
        "cpu": 0.05,
        "gpu": 0.0,
        "network_traffic": 0.01,
        "signal_quality": 5.0,
        "gps": 0.0,
        "background": 0.08,
        "temperature": 25.0,
        "soh": 1.0,
    },
    "weak_signal": {
        "name": "Weak-signal social/video",
        "brightness": 0.45,
        "cpu": 0.30,
        "gpu": 0.10,
        "network_traffic": 0.35,
        "signal_quality": 1.0,
        "gps": 0.0,
        "background": 0.15,
        "temperature": 25.0,
        "soh": 1.0,
    },
    "cold_aged": {
        "name": "Cold aged light use",
        "brightness": 0.35,
        "cpu": 0.20,
        "gpu": 0.05,
        "network_traffic": 0.20,
        "signal_quality": 5.0,
        "gps": 0.0,
        "background": 0.10,
        "temperature": 10.0,
        "soh": 0.83,
    },
}

# Legacy integer choices used by the original interactive main.py.
SCENARIOS = {
    1: deepcopy(SCENARIO_LIBRARY["office"]),
    2: deepcopy(SCENARIO_LIBRARY["video"]),
    3: deepcopy(SCENARIO_LIBRARY["navigation"]),
    4: deepcopy(SCENARIO_LIBRARY["game"]),
    5: deepcopy(SCENARIO_LIBRARY["standby"]),
    6: deepcopy(SCENARIO_LIBRARY["weak_signal"]),
    7: deepcopy(SCENARIO_LIBRARY["cold_aged"]),
}


def get_scenario(name_or_id: str | int) -> dict:
    if isinstance(name_or_id, int) or str(name_or_id).isdigit():
        key = int(name_or_id)
        if key not in SCENARIOS:
            raise KeyError(f"Unknown scenario id: {key}")
        return deepcopy(SCENARIOS[key])
    key = str(name_or_id).strip().lower()
    if key not in SCENARIO_LIBRARY:
        valid = ", ".join(SCENARIO_LIBRARY)
        raise KeyError(f"Unknown scenario '{name_or_id}'. Valid names: {valid}")
    return deepcopy(SCENARIO_LIBRARY[key])


def behavior_from_scenario(scenario: dict) -> UserBehavior:
    return UserBehavior(
        brightness=scenario["brightness"],
        cpu=scenario["cpu"],
        gpu=scenario["gpu"],
        network_traffic=scenario["network_traffic"],
        signal_quality=scenario["signal_quality"],
        gps=scenario["gps"],
        background=scenario["background"],
    )
