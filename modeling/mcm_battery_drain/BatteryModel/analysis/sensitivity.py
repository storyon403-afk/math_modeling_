import pandas as pd
import matplotlib.pyplot as plt

from modeling.mcm_battery_drain.BatteryModel.models.state import BatteryState
from modeling.mcm_battery_drain.BatteryModel.models.behavior import UserBehavior

from modeling.mcm_battery_drain.BatteryModel.simulation.simulator import simulate


def run_sensitivity(
    param_name,
    values,

    load_params,
    electrical_params,
    thermal_params,
    soc_params,
    aging_params,
    resistance_params,

    q_nom=3.45,
    dt=1.0,
    total_time=3600
):

    results = []

    for value in values:

        print(
            f"Running {param_name} = {value}"
        )

        state = BatteryState()

        user = UserBehavior(
            brightness=0.6,
            cpu=0.35,
            gpu=0.10,
            network_traffic=5.0,
            signal_quality=4.0,
            gps=1,
            background=0.08
        )

        # 动态修改参数
        setattr(
            user,
            param_name,
            value
        )

        history = simulate(
            state,
            user,

            load_params,
            electrical_params,
            thermal_params,

            soc_params,
            aging_params,
            resistance_params,

            q_nom,
            dt,
            total_time
        )

        if len(history) == 0:
            continue

        last = history[-1]

        results.append({
            "value": value,

            "soc": last["soc"],

            "soh": last["soh"],

            "temp": last["temp"],

            "voltage": last["voltage"],

            "power": last["power"],

            "tte": last["tte"] / 3600
        })

    return results


def plot_sensitivity(
    results,
    param_name
):

    df = pd.DataFrame(results)

    print(df)

    # TTE

    plt.figure(figsize=(8,5))

    plt.plot(
        df["value"],
        df["tte"],
        marker="o"
    )

    plt.xlabel(param_name)

    plt.ylabel("TTE (h)")

    plt.title(
        f"{param_name} vs TTE"
    )

    plt.grid(True)

    plt.savefig(
        f"{param_name}_tte.png",
        dpi=300
    )

    plt.show()

    # Temperature
    plt.figure(figsize=(8,5))

    plt.plot(
        df["value"],
        df["temp"],
        marker="o"
    )

    plt.xlabel(param_name)

    plt.ylabel("Temperature (°C)")

    plt.title(
        f"{param_name} vs Temperature"
    )

    plt.grid(True)

    plt.savefig(
        f"{param_name}_temp.png",
        dpi=300
    )

    plt.show()

    # SOC

    plt.figure(figsize=(8,5))

    plt.plot(
        df["value"],
        df["soc"] * 100,
        marker="o"
    )

    plt.xlabel(param_name)

    plt.ylabel("Final SOC (%)")

    plt.title(
        f"{param_name} vs SOC"
    )

    plt.grid(True)

    plt.savefig(
        f"{param_name}_soc.png",
        dpi=300
    )

    plt.show()

    # SOH

    plt.figure(figsize=(8,5))

    plt.plot(
        df["value"],
        df["soh"] * 100,
        marker="o"
    )

    plt.xlabel(param_name)

    plt.ylabel("Final SOH (%)")

    plt.title(
        f"{param_name} vs SOH"
    )

    plt.grid(True)

    plt.savefig(
        f"{param_name}_soh.png",
        dpi=300
    )

    plt.show()

    return df