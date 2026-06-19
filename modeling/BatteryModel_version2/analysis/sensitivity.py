"""Single-factor sensitivity analysis using actual simulated TTE."""
from __future__ import annotations

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from BatteryModel_version2.analysis.common import ensure_output_dir, run_scenario_case, save_dataframe
from BatteryModel_version2.simulation.config import SimulationConfig


DEFAULT_VALUES = {
    "brightness": [0.2, 0.4, 0.6, 0.8, 1.0],
    "cpu": [0.1, 0.3, 0.5, 0.7, 0.9],
    "gpu": [0.0, 0.2, 0.4, 0.6, 0.8],
    "network_traffic": [0.0, 0.25, 0.5, 0.75, 1.0],
    "signal_quality": [1, 2, 3, 4, 5],
    "gps": [0.0, 0.25, 0.5, 0.75, 1.0],
    "background": [0.0, 0.1, 0.2, 0.3, 0.4],
}


def run_sensitivity(
    param_name: str,
    values: list[float] | None = None,
    *,
    scenario: str = "game",
    q_nom: float = 3.45,
    dt: float = 5.0,
    total_time: float = 24 * 3600,
    **_legacy_params,
) -> list[dict]:
    if param_name not in DEFAULT_VALUES:
        raise ValueError(f"Unsupported parameter: {param_name}")
    values = list(values or DEFAULT_VALUES[param_name])
    rows = []
    for value in values:
        config = SimulationConfig(
            q_nom_ah=q_nom,
            dt_s=dt,
            max_time_s=total_time,
            record_interval_s=max(30.0, dt),
        )
        result, scenario_cfg, _ = run_scenario_case(
            scenario,
            behavior_overrides={param_name: value},
            config=config,
        )
        rows.append({
            "parameter": param_name,
            "value": value,
            "scenario": scenario_cfg["name"],
            "tte_h": result.tte_hours,
            "stop_reason": result.stop_reason,
            "final_soc": result.final_state.soc,
            "final_soh": result.final_state.soh,
            "final_temp_c": result.final_state.temp,
            "final_voltage_v": result.final_state.voltage,
        })
    return rows


def plot_sensitivity(
    results: list[dict],
    param_name: str,
    output_dir: str | Path = "results/sensitivity",
) -> pd.DataFrame:
    output = ensure_output_dir(output_dir)
    df = pd.DataFrame(results).sort_values("value")
    save_dataframe(df, output / f"{param_name}_sensitivity.csv")

    plot_specs = [
        ("tte_h", "Actual TTE (h)", f"{param_name}_tte.png"),
        ("final_temp_c", "Final temperature (°C)", f"{param_name}_temperature.png"),
        ("final_soc", "Final SOC", f"{param_name}_soc.png"),
        ("final_voltage_v", "Final terminal voltage (V)", f"{param_name}_voltage.png"),
    ]
    for column, ylabel, filename in plot_specs:
        fig, ax = plt.subplots(figsize=(8.0, 5.0))
        ax.plot(df["value"], df[column], marker="o")
        ax.set_xlabel(param_name)
        ax.set_ylabel(ylabel)
        ax.set_title(f"Single-factor sensitivity: {param_name}")
        ax.grid(alpha=0.3)
        fig.tight_layout()
        fig.savefig(output / filename, dpi=300, bbox_inches="tight")
        plt.close(fig)
    return df
