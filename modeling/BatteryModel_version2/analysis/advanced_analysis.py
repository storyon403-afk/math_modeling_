"""Advanced analyses for the SOC-SOH-2RC-thermal-TTE battery model."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from time import perf_counter
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from BatteryModel_version2.analysis.common import (
    ModelParameters,
    default_parameters,
    ensure_output_dir,
    run_scenario_case,
    save_dataframe,
)
from BatteryModel_version2.analysis.scenario_analysis import (
    SCENARIO_LIBRARY,
    behavior_from_scenario,
    get_scenario,
)
from BatteryModel_version2.models.behavior import PiecewiseRandomBehavior
from BatteryModel_version2.models.state import BatteryState
from BatteryModel_version2.physics.load import calc_load_power
from BatteryModel_version2.physics.thermal import low_temp_factor
from BatteryModel_version2.physics.soh import soh_derivative
from BatteryModel_version2.simulation.config import SimulationConfig
from BatteryModel_version2.simulation.simulator import simulate_case

PLOT_DPI = 300


def _save_fig(fig: plt.Figure, path: Path) -> None:
    fig.tight_layout()
    fig.savefig(path, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)


def _base_config(dt_s: float = 5.0, record_interval_s: float = 30.0) -> SimulationConfig:
    return SimulationConfig(
        dt_s=dt_s,
        max_time_s=24 * 3600,
        record_interval_s=record_interval_s,
        soc_min=0.03,
        voltage_cutoff_v=3.0,
    )


def initial_soc_analysis(output_dir: str | Path, quick: bool = False) -> pd.DataFrame:
    output = ensure_output_dir(output_dir) / "01_initial_soc"
    output.mkdir(parents=True, exist_ok=True)
    soc_values = [0.2, 0.4, 0.6, 0.8, 1.0]
    scenarios = ["office", "video", "navigation", "game"]
    rows = []
    for scenario_name in scenarios:
        for soc in soc_values:
            result, scenario, _ = run_scenario_case(
                scenario_name,
                initial_soc=soc,
                config=_base_config(dt_s=10.0 if quick else 5.0),
            )
            rows.append({
                "scenario": scenario["name"],
                "initial_soc": soc,
                "tte_h": result.tte_hours,
                "stop_reason": result.stop_reason,
                "final_soc": result.final_state.soc,
                "final_voltage_v": result.final_state.voltage,
            })
    df = pd.DataFrame(rows)
    save_dataframe(df, output / "initial_soc_tte.csv")

    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    for name, group in df.groupby("scenario"):
        ax.plot(group["initial_soc"] * 100, group["tte_h"], marker="o", label=name)
    ax.set_xlabel("Initial SOC (%)")
    ax.set_ylabel("Actual TTE (h)")
    ax.set_title("Initial SOC–TTE relationship")
    ax.grid(alpha=0.3)
    ax.legend()
    _save_fig(fig, output / "initial_soc_tte.png")

    pivot = df.pivot(index="initial_soc", columns="scenario", values="tte_h")
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    pivot.plot(kind="bar", ax=ax)
    ax.set_xlabel("Initial SOC")
    ax.set_ylabel("Actual TTE (h)")
    ax.set_title("Scenario comparison at identical initial SOC")
    ax.grid(axis="y", alpha=0.3)
    _save_fig(fig, output / "initial_soc_scenario_comparison.png")
    return df


def temperature_analysis(output_dir: str | Path, quick: bool = False) -> pd.DataFrame:
    output = ensure_output_dir(output_dir) / "02_temperature"
    output.mkdir(parents=True, exist_ok=True)
    temperatures = [-10, 0, 10, 25, 40]
    scenarios = ["office", "video", "navigation", "game"]
    rows = []
    detailed = {}
    for scenario_name in scenarios:
        for temp in temperatures:
            result, scenario, params = run_scenario_case(
                scenario_name,
                ambient_temp=temp,
                config=_base_config(dt_s=10.0 if quick else 5.0),
            )
            initial_soh_loss_rate = float("nan")
            if result.history:
                first = result.history[0]
                rate_state = BatteryState(
                    soc=first["soc"], soh=first["soh"], temp=first["temp"],
                    voltage=first["voltage"], current=first["current"],
                    v1=first["v1"], v2=first["v2"],
                )
                initial_soh_loss_rate = -soh_derivative(
                    rate_state, 3.45, params.aging
                ) * 3600.0
            rows.append({
                "scenario": scenario["name"],
                "ambient_temp_c": temp,
                "tte_h": result.tte_hours,
                "stop_reason": result.stop_reason,
                "final_temp_c": result.final_state.temp,
                "final_voltage_v": result.final_state.voltage,
                "final_soc": result.final_state.soc,
                "initial_soh_loss_rate_per_hour": initial_soh_loss_rate,
            })
            if scenario_name == "game":
                detailed[temp] = pd.DataFrame(result.history)
    df = pd.DataFrame(rows)
    baseline_rates = (
        df[df["ambient_temp_c"] == 25]
        .set_index("scenario")["initial_soh_loss_rate_per_hour"]
        .to_dict()
    )
    df["relative_aging_rate_vs_25c"] = [
        row.initial_soh_loss_rate_per_hour / max(baseline_rates.get(row.scenario, np.nan), 1e-30)
        for row in df.itertuples()
    ]
    save_dataframe(df, output / "temperature_tte.csv")

    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    for name, group in df.groupby("scenario"):
        ax.plot(group["ambient_temp_c"], group["tte_h"], marker="o", label=name)
    ax.set_xlabel("Ambient temperature (°C)")
    ax.set_ylabel("Actual TTE (h)")
    ax.set_title("Environmental temperature effect on TTE")
    ax.grid(alpha=0.3)
    ax.legend()
    _save_fig(fig, output / "temperature_tte.png")

    pivot = df.pivot(index="scenario", columns="ambient_temp_c", values="tte_h")
    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    im = ax.imshow(pivot.values, aspect="auto", cmap="viridis")
    ax.set_xticks(range(len(pivot.columns)), pivot.columns)
    ax.set_yticks(range(len(pivot.index)), pivot.index)
    ax.set_xlabel("Ambient temperature (°C)")
    ax.set_title("Scenario–temperature TTE heatmap")
    fig.colorbar(im, ax=ax, label="TTE (h)")
    _save_fig(fig, output / "temperature_scenario_heatmap.png")

    for variable, label, filename in [
        ("voltage", "Terminal voltage (V)", "game_voltage_by_temperature.png"),
        ("temp", "Battery temperature (°C)", "game_temperature_trajectories.png"),
        ("soc", "SOC", "game_soc_by_temperature.png"),
    ]:
        fig, ax = plt.subplots(figsize=(8.2, 5.2))
        for temp, hist in detailed.items():
            ax.plot(hist["time"] / 3600, hist[variable], label=f"{temp}°C")
        ax.set_xlabel("Time (h)")
        ax.set_ylabel(label)
        ax.set_title(f"Mobile game: {label} trajectories")
        ax.grid(alpha=0.3)
        ax.legend()
        _save_fig(fig, output / filename)

    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    for name, group in df.groupby("scenario"):
        ax.plot(group["ambient_temp_c"], group["relative_aging_rate_vs_25c"], marker="o", label=name)
    ax.set_yscale("log")
    ax.set_xlabel("Ambient temperature (°C)")
    ax.set_ylabel("Relative initial aging rate (25°C = 1)")
    ax.set_title("Temperature acceleration of SOH degradation")
    ax.grid(alpha=0.3)
    ax.legend()
    _save_fig(fig, output / "temperature_relative_aging_rate.png")
    return df


def soh_analysis(output_dir: str | Path, quick: bool = False) -> pd.DataFrame:
    output = ensure_output_dir(output_dir) / "03_soh"
    output.mkdir(parents=True, exist_ok=True)
    soh_values = [1.0, 0.9, 0.8, 0.7]
    rows = []
    histories = {}
    for soh in soh_values:
        result, scenario, _ = run_scenario_case(
            "game",
            initial_soh=soh,
            config=_base_config(dt_s=10.0 if quick else 5.0),
        )
        rows.append({
            "scenario": scenario["name"],
            "initial_soh": soh,
            "tte_h": result.tte_hours,
            "stop_reason": result.stop_reason,
            "final_voltage_v": result.final_state.voltage,
            "final_soc": result.final_state.soc,
        })
        histories[soh] = pd.DataFrame(result.history)
    df = pd.DataFrame(rows)
    tte_new = float(df.loc[df["initial_soh"] == 1.0, "tte_h"].iloc[0])
    df["tte_decline_pct"] = (tte_new - df["tte_h"]) / tte_new * 100
    save_dataframe(df, output / "soh_tte.csv")

    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    ax.plot(df["initial_soh"] * 100, df["tte_h"], marker="o")
    ax.set_xlabel("Initial SOH (%)")
    ax.set_ylabel("Actual TTE (h)")
    ax.set_title("SOH effect on mobile-game endurance")
    ax.grid(alpha=0.3)
    _save_fig(fig, output / "soh_tte.png")

    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    for soh, hist in histories.items():
        ax.plot(hist["time"] / 3600, hist["voltage"], label=f"SOH={soh:.1f}")
    ax.axhline(3.0, linestyle="--", linewidth=1, label="Voltage cutoff")
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("Terminal voltage (V)")
    ax.set_title("Voltage trajectories under battery aging")
    ax.grid(alpha=0.3)
    ax.legend()
    _save_fig(fig, output / "soh_voltage_trajectories.png")
    return df


def _analytic_baseline_tte_h(
    scenario: dict,
    initial_soc: float,
    initial_soh: float,
    ambient_temp: float,
    params: ModelParameters,
    soc_min: float = 0.03,
) -> float:
    user = behavior_from_scenario(scenario)
    power = calc_load_power(user, params.load)["total"]
    usable_fraction = max(initial_soc - soc_min, 0.0)
    capacity_factor = max(low_temp_factor(ambient_temp, params.thermal), 0.05)
    energy_wh = usable_fraction * initial_soh * params.electrical.__dict__.get("nominal_voltage", 3.7)
    energy_wh *= 3.45 * capacity_factor
    return energy_wh / max(power, 1e-9)


def model_ablation_analysis(output_dir: str | Path, quick: bool = False) -> pd.DataFrame:
    output = ensure_output_dir(output_dir) / "04_ablation"
    output.mkdir(parents=True, exist_ok=True)
    cases = [
        ("Standby", "standby", 25.0, 1.0),
        ("Game", "game", 25.0, 1.0),
        ("Low-temperature game", "game", 0.0, 1.0),
        ("Aged game", "game", 25.0, 0.8),
    ]
    rows = []
    for case_name, scenario_name, ambient, soh in cases:
        scenario = get_scenario(scenario_name)
        base_params = default_parameters()
        rows.append({
            "case": case_name,
            "model": "Baseline energy/power",
            "tte_h": _analytic_baseline_tte_h(scenario, 1.0, 1.0, 25.0, base_params),
            "stop_reason": "analytic estimate",
        })

        # Model A: SOC dynamics only; no voltage, thermal, or aging correction.
        neutral = deepcopy(base_params)
        neutral.thermal.T_env = 25.0
        cfg_a = _base_config(dt_s=10.0 if quick else 5.0)
        cfg_a.use_2rc = False
        cfg_a.use_thermal = False
        cfg_a.use_soh = False
        cfg_a.use_dynamic_resistance = False
        cfg_a.stop_on_voltage = False
        result, _, _ = run_scenario_case(
            scenario_name, initial_soh=1.0, ambient_temp=25.0,
            config=cfg_a, params=neutral,
        )
        rows.append({"case": case_name, "model": "Model A: SOC", "tte_h": result.tte_hours, "stop_reason": result.stop_reason})

        # Model B: SOC + 2RC; condition-specific thermal and SOH effects omitted.
        cfg_b = _base_config(dt_s=10.0 if quick else 5.0)
        cfg_b.use_thermal = False
        cfg_b.use_soh = False
        result, _, _ = run_scenario_case(
            scenario_name, initial_soh=1.0, ambient_temp=25.0,
            config=cfg_b, params=neutral,
        )
        rows.append({"case": case_name, "model": "Model B: SOC + 2RC", "tte_h": result.tte_hours, "stop_reason": result.stop_reason})

        # Model C: add thermal effects, but keep a new battery.
        cfg_c = _base_config(dt_s=10.0 if quick else 5.0)
        cfg_c.use_soh = False
        result, _, _ = run_scenario_case(
            scenario_name, initial_soh=1.0, ambient_temp=ambient,
            config=cfg_c,
        )
        rows.append({"case": case_name, "model": "Model C: + thermal", "tte_h": result.tte_hours, "stop_reason": result.stop_reason})

        # Full model: thermal + SOH + dynamic resistance/aging.
        result, _, _ = run_scenario_case(
            scenario_name, initial_soh=soh, ambient_temp=ambient,
            config=_base_config(dt_s=10.0 if quick else 5.0),
        )
        rows.append({"case": case_name, "model": "Full model: + SOH", "tte_h": result.tte_hours, "stop_reason": result.stop_reason})

    df = pd.DataFrame(rows)
    full = df[df["model"] == "Full model: + SOH"].set_index("case")["tte_h"]
    df["relative_error_to_full_pct"] = [
        (row.tte_h - full.loc[row.case]) / full.loc[row.case] * 100
        for row in df.itertuples()
    ]
    save_dataframe(df, output / "model_ablation.csv")

    pivot = df.pivot(index="case", columns="model", values="tte_h")
    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    pivot.plot(kind="bar", ax=ax)
    ax.set_xlabel("")
    ax.set_ylabel("TTE (h)")
    ax.set_title("Incremental model / ablation comparison")
    ax.grid(axis="y", alpha=0.3)
    ax.legend(fontsize=8)
    _save_fig(fig, output / "model_ablation.png")
    return df


def stop_reason_analysis(output_dir: str | Path, quick: bool = False) -> pd.DataFrame:
    output = ensure_output_dir(output_dir) / "05_stop_reason"
    output.mkdir(parents=True, exist_ok=True)
    temperatures = [-10, 0, 10, 25, 40, 55, 58]
    soh_values = [0.7, 0.8, 0.9, 1.0]
    rows = []
    for temp in temperatures:
        for soh in soh_values:
            result, scenario, _ = run_scenario_case(
                "game", ambient_temp=temp, initial_soh=soh,
                config=_base_config(dt_s=10.0 if quick else 5.0),
            )
            rows.append({
                "scenario": scenario["name"],
                "ambient_temp_c": temp,
                "initial_soh": soh,
                "stop_reason": result.stop_reason,
                "tte_h": result.tte_hours,
                "final_soc": result.final_state.soc,
                "final_voltage_v": result.final_state.voltage,
                "final_temp_c": result.final_state.temp,
            })
    df = pd.DataFrame(rows)
    save_dataframe(df, output / "stop_reason_table.csv")

    reason_order = ["SOC threshold", "voltage cutoff", "thermal protection", "maximum simulation time"]
    reason_to_code = {name: i for i, name in enumerate(reason_order)}
    pivot = df.pivot(index="initial_soh", columns="ambient_temp_c", values="stop_reason")
    coded = pivot.map(lambda value: reason_to_code.get(value, len(reason_order)))
    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    im = ax.imshow(coded.values, aspect="auto", cmap="tab10", vmin=0, vmax=max(len(reason_order) - 1, 1))
    ax.set_xticks(range(len(pivot.columns)), pivot.columns)
    ax.set_yticks(range(len(pivot.index)), [f"{x:.1f}" for x in pivot.index])
    ax.set_xlabel("Ambient temperature (°C)")
    ax.set_ylabel("Initial SOH")
    ax.set_title("TTE termination mechanism regions (mobile game)")
    handles = [plt.Line2D([0], [0], marker="s", linestyle="", markersize=8,
                          markerfacecolor=im.cmap(im.norm(i)), markeredgecolor="none", label=name)
               for i, name in enumerate(reason_order) if name in set(df["stop_reason"])]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=2)
    _save_fig(fig, output / "stop_reason_map.png")
    return df


def _interaction_grid(
    pair_name: str,
    x_name: str,
    x_values: list[float],
    y_name: str,
    y_values: list[float],
    output: Path,
    quick: bool,
) -> pd.DataFrame:
    rows = []
    for y in y_values:
        for x in x_values:
            overrides = {}
            ambient = 25.0
            soh = 1.0
            if x_name == "ambient_temp_c":
                ambient = x
            elif x_name == "initial_soh":
                soh = x
            else:
                overrides[x_name] = x
            if y_name == "ambient_temp_c":
                ambient = y
            elif y_name == "initial_soh":
                soh = y
            else:
                overrides[y_name] = y
            result, _, _ = run_scenario_case(
                "game",
                ambient_temp=ambient,
                initial_soh=soh,
                behavior_overrides=overrides,
                config=_base_config(dt_s=15.0 if quick else 10.0, record_interval_s=120.0),
            )
            rows.append({x_name: x, y_name: y, "tte_h": result.tte_hours, "stop_reason": result.stop_reason})
    df = pd.DataFrame(rows)
    save_dataframe(df, output / f"{pair_name}.csv")
    pivot = df.pivot(index=y_name, columns=x_name, values="tte_h")
    x_grid, y_grid = np.meshgrid(pivot.columns.astype(float), pivot.index.astype(float))
    z = pivot.values

    fig, ax = plt.subplots(figsize=(7.6, 5.2))
    im = ax.imshow(z, origin="lower", aspect="auto", cmap="viridis",
                   extent=[x_grid.min(), x_grid.max(), y_grid.min(), y_grid.max()])
    ax.set_xlabel(x_name)
    ax.set_ylabel(y_name)
    ax.set_title(f"{pair_name}: TTE heatmap")
    fig.colorbar(im, ax=ax, label="TTE (h)")
    _save_fig(fig, output / f"{pair_name}_heatmap.png")

    fig, ax = plt.subplots(figsize=(7.6, 5.2))
    contour = ax.contourf(x_grid, y_grid, z, levels=12, cmap="viridis")
    ax.set_xlabel(x_name)
    ax.set_ylabel(y_name)
    ax.set_title(f"{pair_name}: TTE contours")
    fig.colorbar(contour, ax=ax, label="TTE (h)")
    _save_fig(fig, output / f"{pair_name}_contour.png")

    fig = plt.figure(figsize=(8.0, 5.8))
    ax3d = fig.add_subplot(111, projection="3d")
    ax3d.plot_surface(x_grid, y_grid, z, cmap="viridis", edgecolor="none", alpha=0.9)
    ax3d.set_xlabel(x_name)
    ax3d.set_ylabel(y_name)
    ax3d.set_zlabel("TTE (h)")
    ax3d.set_title(f"{pair_name}: response surface")
    _save_fig(fig, output / f"{pair_name}_surface.png")
    return df


def interaction_analysis(output_dir: str | Path, quick: bool = False) -> pd.DataFrame:
    output = ensure_output_dir(output_dir) / "06_interactions"
    output.mkdir(parents=True, exist_ok=True)
    specs = [
        ("brightness_cpu", "brightness", [0.2, 0.4, 0.6, 0.8, 1.0], "cpu", [0.1, 0.3, 0.5, 0.7, 0.9]),
        ("cpu_gpu", "cpu", [0.1, 0.3, 0.5, 0.7, 0.9], "gpu", [0.1, 0.3, 0.5, 0.7, 0.9]),
        ("network_signal", "network_traffic", [0.0, 0.25, 0.5, 0.75, 1.0], "signal_quality", [1, 2, 3, 4, 5]),
        ("temperature_soh", "ambient_temp_c", [-10, 0, 10, 25, 40], "initial_soh", [0.7, 0.8, 0.9, 1.0]),
    ]
    frames = []
    for spec in specs:
        frame = _interaction_grid(*spec, output=output, quick=quick)
        frame.insert(0, "interaction", spec[0])
        frames.append(frame)
    combined = pd.concat(frames, ignore_index=True, sort=False)
    save_dataframe(combined, output / "all_interactions.csv")
    return combined


def power_contribution_analysis(output_dir: str | Path) -> pd.DataFrame:
    output = ensure_output_dir(output_dir) / "07_power_contribution"
    output.mkdir(parents=True, exist_ok=True)
    params = default_parameters()
    rows = []
    for key, scenario in SCENARIO_LIBRARY.items():
        load = calc_load_power(behavior_from_scenario(scenario), params.load)
        total = load["total"]
        row = {"scenario_key": key, "scenario": scenario["name"], "total_power_w": total}
        for component in ["base", "screen", "cpu", "gpu", "network", "gps", "background"]:
            row[f"{component}_power_w"] = load[component]
            row[f"{component}_share_pct"] = load[component] / total * 100
        rows.append(row)
    df = pd.DataFrame(rows)
    save_dataframe(df, output / "power_contribution.csv")

    components = ["base", "screen", "cpu", "gpu", "network", "gps", "background"]
    fig, ax = plt.subplots(figsize=(11.0, 5.8))
    bottom = np.zeros(len(df))
    x = np.arange(len(df))
    for component in components:
        values = df[f"{component}_power_w"].to_numpy()
        ax.bar(x, values, bottom=bottom, label=component)
        bottom += values
    ax.set_xticks(x, df["scenario"], rotation=20, ha="right")
    ax.set_ylabel("Power (W)")
    ax.set_title("Component-level power contribution by scenario")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(ncol=4)
    _save_fig(fig, output / "power_contribution_stacked.png")
    return df


def monte_carlo_analysis(
    output_dir: str | Path,
    quick: bool = False,
    n_runs: int | None = None,
    seed: int = 2026,
) -> pd.DataFrame:
    output = ensure_output_dir(output_dir) / "08_monte_carlo"
    output.mkdir(parents=True, exist_ok=True)
    n_runs = n_runs or (100 if quick else 500)
    scenario = get_scenario("game")
    base_behavior = behavior_from_scenario(scenario)
    params = default_parameters()
    params.thermal.T_env = 25.0
    rng = np.random.default_rng(seed)
    rows = []
    for run in range(n_runs):
        behavior_rng = np.random.default_rng(rng.integers(0, 2**32 - 1))
        stochastic_behavior = PiecewiseRandomBehavior(base_behavior, behavior_rng, interval_s=60.0)
        state = BatteryState(soc=1.0, soh=1.0, temp=25.0)
        config = _base_config(dt_s=15.0 if quick else 10.0, record_interval_s=600.0)
        result = simulate_case(
            state, stochastic_behavior,
            params.load, params.electrical, params.thermal,
            params.soc, params.aging, params.resistance, config,
        )
        rows.append({
            "run": run + 1,
            "tte_h": result.tte_hours,
            "stop_reason": result.stop_reason,
            "final_soc": result.final_state.soc,
            "final_voltage_v": result.final_state.voltage,
            "final_temp_c": result.final_state.temp,
        })
    df = pd.DataFrame(rows)
    save_dataframe(df, output / "monte_carlo_runs.csv")
    summary = pd.DataFrame([{
        "n_runs": n_runs,
        "mean_tte_h": df["tte_h"].mean(),
        "std_tte_h": df["tte_h"].std(ddof=1),
        "ci95_lower_h": df["tte_h"].quantile(0.025),
        "ci95_upper_h": df["tte_h"].quantile(0.975),
        "median_tte_h": df["tte_h"].median(),
    }])
    save_dataframe(summary, output / "monte_carlo_summary.csv")

    fig, ax = plt.subplots(figsize=(8.0, 5.0))
    ax.hist(df["tte_h"], bins=20, alpha=0.85)
    ax.axvline(df["tte_h"].mean(), linestyle="--", label=f"Mean={df['tte_h'].mean():.2f} h")
    ax.set_xlabel("TTE (h)")
    ax.set_ylabel("Frequency")
    ax.set_title("Monte Carlo distribution of mobile-game TTE")
    ax.grid(axis="y", alpha=0.25)
    ax.legend()
    _save_fig(fig, output / "monte_carlo_histogram.png")

    fig, ax = plt.subplots(figsize=(5.2, 5.0))
    ax.boxplot(df["tte_h"], vert=True)
    ax.set_ylabel("TTE (h)")
    ax.set_title("Monte Carlo TTE boxplot")
    ax.grid(axis="y", alpha=0.25)
    _save_fig(fig, output / "monte_carlo_boxplot.png")
    return df


def _load_benchmark_csv(data_path: str | Path) -> pd.DataFrame:
    raw = pd.read_csv(data_path, header=2)
    required = {"Scenario", "Initial_SOC", "Time_to_empty_hours"}
    missing = required - set(raw.columns)
    if missing:
        raise ValueError(f"Benchmark CSV missing columns: {sorted(missing)}")
    return raw.dropna(subset=["Scenario", "Initial_SOC", "Time_to_empty_hours"]).copy()


def validation_analysis(
    output_dir: str | Path,
    benchmark_csv: str | Path,
    quick: bool = False,
) -> pd.DataFrame:
    output = ensure_output_dir(output_dir) / "09_validation"
    output.mkdir(parents=True, exist_ok=True)
    benchmark = _load_benchmark_csv(benchmark_csv)
    name_map = {scenario["name"]: key for key, scenario in SCENARIO_LIBRARY.items()}
    rows = []
    for row in benchmark.itertuples(index=False):
        if row.Scenario not in name_map:
            continue
        key = name_map[row.Scenario]
        scenario = get_scenario(key)
        result, _, _ = run_scenario_case(
            key,
            initial_soc=float(row.Initial_SOC),
            initial_soh=float(scenario.get("soh", 1.0)),
            ambient_temp=float(scenario.get("temperature", 25.0)),
            config=_base_config(dt_s=15.0 if quick else 10.0),
        )
        observed = float(row.Time_to_empty_hours)
        predicted = result.tte_hours
        rows.append({
            "scenario": row.Scenario,
            "initial_soc": float(row.Initial_SOC),
            "reference_tte_h": observed,
            "predicted_tte_h": predicted,
            "error_h": predicted - observed,
            "absolute_error_h": abs(predicted - observed),
            "absolute_percentage_error_pct": abs(predicted - observed) / max(observed, 1e-9) * 100,
            "stop_reason": result.stop_reason,
        })
    df = pd.DataFrame(rows)
    save_dataframe(df, output / "benchmark_consistency_results.csv")
    if df.empty:
        raise ValueError("No benchmark scenarios matched the scenario library")
    metrics = pd.DataFrame([{
        "MAE_h": df["absolute_error_h"].mean(),
        "RMSE_h": math.sqrt(np.mean(df["error_h"] ** 2)),
        "MAPE_pct": df["absolute_percentage_error_pct"].mean(),
        "n": len(df),
        "validation_type": "benchmark/physical-consistency comparison; not experimental validation",
    }])
    save_dataframe(metrics, output / "benchmark_consistency_metrics.csv")

    fig, ax = plt.subplots(figsize=(6.0, 6.0))
    ax.scatter(df["reference_tte_h"], df["predicted_tte_h"], alpha=0.8)
    limit = max(df["reference_tte_h"].max(), df["predicted_tte_h"].max()) * 1.05
    ax.plot([0, limit], [0, limit], linestyle="--", label="y = x")
    ax.set_xlim(0, limit)
    ax.set_ylim(0, limit)
    ax.set_xlabel("Reference TTE (h)")
    ax.set_ylabel("Predicted TTE (h)")
    ax.set_title("Benchmark consistency of TTE prediction")
    ax.grid(alpha=0.3)
    ax.legend()
    _save_fig(fig, output / "predicted_vs_reference.png")
    return df


def timestep_analysis(output_dir: str | Path, quick: bool = False) -> pd.DataFrame:
    output = ensure_output_dir(output_dir) / "10_timestep"
    output.mkdir(parents=True, exist_ok=True)
    dt_values = [0.5, 1.0, 5.0, 10.0, 30.0]
    if quick:
        dt_values = [1.0, 5.0, 10.0, 30.0]
    rows = []
    for dt in dt_values:
        start = perf_counter()
        result, _, _ = run_scenario_case(
            "game",
            config=_base_config(dt_s=dt, record_interval_s=max(30.0, dt)),
        )
        runtime = perf_counter() - start
        rows.append({
            "dt_s": dt,
            "tte_h": result.tte_hours,
            "runtime_s": runtime,
            "stop_reason": result.stop_reason,
        })
    df = pd.DataFrame(rows).sort_values("dt_s")
    reference = float(df.iloc[0]["tte_h"])
    df["absolute_tte_error_h"] = abs(df["tte_h"] - reference)
    df["relative_tte_error_pct"] = df["absolute_tte_error_h"] / max(reference, 1e-9) * 100
    save_dataframe(df, output / "timestep_stability.csv")

    fig, ax = plt.subplots(figsize=(8.0, 5.0))
    ax.plot(df["dt_s"], df["relative_tte_error_pct"], marker="o")
    ax.set_xscale("log")
    ax.set_xlabel("Time step Δt (s, log scale)")
    ax.set_ylabel("Relative TTE error (%)")
    ax.set_title("Numerical time-step stability")
    ax.grid(alpha=0.3)
    _save_fig(fig, output / "timestep_error.png")

    fig, ax = plt.subplots(figsize=(8.0, 5.0))
    ax.plot(df["dt_s"], df["runtime_s"], marker="o")
    ax.set_xscale("log")
    ax.set_xlabel("Time step Δt (s, log scale)")
    ax.set_ylabel("Computation time (s)")
    ax.set_title("Accuracy–efficiency trade-off")
    ax.grid(alpha=0.3)
    _save_fig(fig, output / "timestep_runtime.png")
    return df


ANALYSIS_FUNCTIONS = {
    "soc": initial_soc_analysis,
    "temperature": temperature_analysis,
    "soh": soh_analysis,
    "ablation": model_ablation_analysis,
    "stop": stop_reason_analysis,
    "interaction": interaction_analysis,
    "contribution": power_contribution_analysis,
    "monte_carlo": monte_carlo_analysis,
    "timestep": timestep_analysis,
}


