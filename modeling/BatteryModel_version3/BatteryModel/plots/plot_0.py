"""Scientific plotting utilities for a single simulation history."""
from __future__ import annotations

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def _df(history) -> pd.DataFrame:
    frame = pd.DataFrame(history)
    if frame.empty:
        raise ValueError("Simulation history is empty")
    return frame


def _line_plot(history, y: str, ylabel: str, title: str, path: Path) -> None:
    df = _df(history)
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    ax.plot(df["time"] / 3600.0, df[y])
    ax.set_xlabel("Time (h)")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def save_history_plots(history, output_dir: str | Path) -> None:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    _line_plot(history, "soc", "SOC", "State of charge", output / "soc_time.png")
    _line_plot(history, "soh", "SOH", "State of health", output / "soh_time.png")
    _line_plot(history, "temp", "Temperature (°C)", "Battery temperature", output / "temperature_time.png")
    _line_plot(history, "voltage", "Terminal voltage (V)", "Thevenin terminal voltage", output / "voltage_time.png")
    _line_plot(history, "power", "Load power (W)", "Phone load power", output / "power_time.png")
    if "tte_estimate" in _df(history):
        _line_plot(history, "tte_estimate", "Instantaneous TTE estimate (s)", "Instantaneous energy/power TTE estimate", output / "tte_estimate_time.png")

    df = _df(history)
    variables = ["soc", "soh", "temp", "voltage", "current", "power"]
    corr = df[variables].corr()
    fig, ax = plt.subplots(figsize=(7.2, 6.0))
    im = ax.imshow(corr.values, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(variables)), variables, rotation=35, ha="right")
    ax.set_yticks(range(len(variables)), variables)
    for i in range(len(variables)):
        for j in range(len(variables)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=8)
    ax.set_title("State-variable correlation matrix")
    fig.colorbar(im, ax=ax, label="Correlation")
    fig.tight_layout()
    fig.savefig(output / "correlation_matrix.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


# Backward-compatible function names from the original project.
def soc_plot(history):
    _line_plot(history, "soc", "SOC", "Battery State of Charge", Path("soc_time.png"))

def soh_plot(history):
    _line_plot(history, "soh", "SOH", "Battery State of Health", Path("soh_time.png"))

def temp_plot(history):
    _line_plot(history, "temp", "Temperature (°C)", "Battery Temperature", Path("temperature_time.png"))

def behavior_plot(history):
    _line_plot(history, "power", "Power (W)", "Phone Power Consumption", Path("power_time.png"))

def ecm_plot(history):
    _line_plot(history, "voltage", "Voltage (V)", "Terminal Voltage", Path("voltage_time.png"))

def tte_plot(history):
    key = "tte_estimate" if "tte_estimate" in _df(history) else "tte"
    _line_plot(history, key, "TTE (s)", "TTE vs Time", Path("tte_time.png"))

def soc_temp_plot(history): save_history_plots(history, "legacy_plots")
def soc_voltage_plot(history): save_history_plots(history, "legacy_plots")
def soc_temp_voltage_plot(history): save_history_plots(history, "legacy_plots")
def heat_map_plot(history): save_history_plots(history, "legacy_plots")
def soc_tte_plot(history): save_history_plots(history, "legacy_plots")
def power_tte_plot(history): save_history_plots(history, "legacy_plots")
def tte_heatmap(history): save_history_plots(history, "legacy_plots")
