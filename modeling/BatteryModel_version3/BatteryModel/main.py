"""Command-line entry point for the optimized battery digital-twin project."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow both ``python -m BatteryModel.main`` and ``python BatteryModel/main.py``.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd

from BatteryModel.analysis.advanced_analysis import (
    initial_soc_analysis,
    temperature_analysis,
    soh_analysis,
    model_ablation_analysis,
    stop_reason_analysis,
    interaction_analysis,
    power_contribution_analysis,
    monte_carlo_analysis,
    validation_analysis,
    timestep_analysis,
)
from BatteryModel.analysis.common import ensure_output_dir, run_scenario_case, save_dataframe
from BatteryModel.analysis.scenario_analysis import SCENARIO_LIBRARY
from BatteryModel.analysis.sensitivity import DEFAULT_VALUES, plot_sensitivity, run_sensitivity
from BatteryModel.plots.plot_0 import save_history_plots
from BatteryModel.simulation.config import SimulationConfig


def _parse_values(text: str | None) -> list[float] | None:
    if not text:
        return None
    return [float(item.strip()) for item in text.split(",") if item.strip()]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="SOC-SOH-Thevenin 2RC-thermal coupled phone battery simulation",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--analysis",
        default="scenario",
        choices=[
            "scenario", "sensitivity", "soc", "temperature", "soh",
            "ablation", "stop", "interaction", "contribution",
            "monte_carlo", "validation", "timestep",
        ],
        help="Analysis module to run",
    )
    parser.add_argument("--scenario", default="game", choices=sorted(SCENARIO_LIBRARY))
    parser.add_argument("--parameter", default="brightness", choices=sorted(DEFAULT_VALUES))
    parser.add_argument("--values", default=None, help="Comma-separated sensitivity values")
    parser.add_argument("--initial-soc", type=float, default=1.0)
    parser.add_argument("--initial-soh", type=float, default=None)
    parser.add_argument("--temperature", type=float, default=None)
    parser.add_argument("--dt", type=float, default=5.0, help="Simulation time step in seconds")
    parser.add_argument("--max-hours", type=float, default=24.0)
    parser.add_argument("--output", default="results")
    parser.add_argument("--quick", action="store_true", help="Use reduced Monte Carlo size and coarser grids/time steps")
    parser.add_argument("--mc-runs", type=int, default=None, help="Override Monte Carlo run count")
    parser.add_argument(
        "--benchmark-csv",
        default=str(Path(__file__).resolve().parent / "data" / "extracted_csvs" / "06_TTE基准结果.csv"),
    )
    return parser


def run_scenario(args: argparse.Namespace) -> None:
    output = ensure_output_dir(Path(args.output) / "scenario" / args.scenario)
    config = SimulationConfig(
        dt_s=args.dt,
        max_time_s=args.max_hours * 3600.0,
        record_interval_s=max(10.0, args.dt),
    )
    result, scenario, _ = run_scenario_case(
        args.scenario,
        initial_soc=args.initial_soc,
        initial_soh=args.initial_soh,
        ambient_temp=args.temperature,
        config=config,
    )
    history = pd.DataFrame(result.history)
    save_dataframe(history, output / "simulation_history.csv")
    save_history_plots(result.history, output)
    summary = pd.DataFrame([{
        "scenario": scenario["name"],
        "actual_tte_h": result.tte_hours,
        "stop_reason": result.stop_reason,
        "final_soc": result.final_state.soc,
        "final_soh": result.final_state.soh,
        "final_temperature_c": result.final_state.temp,
        "final_voltage_v": result.final_state.voltage,
    }])
    save_dataframe(summary, output / "simulation_summary.csv")
    print(summary.to_string(index=False))


def run_selected(args: argparse.Namespace) -> None:
    output = Path(args.output)
    if args.analysis == "scenario":
        run_scenario(args)
    elif args.analysis == "sensitivity":
        values = _parse_values(args.values)
        results = run_sensitivity(
            args.parameter,
            values,
            scenario=args.scenario,
            dt=args.dt,
            total_time=args.max_hours * 3600.0,
        )
        df = plot_sensitivity(results, args.parameter, output / "sensitivity" / args.scenario)
        print(df.to_string(index=False))
    elif args.analysis == "soc":
        print(initial_soc_analysis(output, args.quick).to_string(index=False))
    elif args.analysis == "temperature":
        print(temperature_analysis(output, args.quick).to_string(index=False))
    elif args.analysis == "soh":
        print(soh_analysis(output, args.quick).to_string(index=False))
    elif args.analysis == "ablation":
        print(model_ablation_analysis(output, args.quick).to_string(index=False))
    elif args.analysis == "stop":
        print(stop_reason_analysis(output, args.quick).to_string(index=False))
    elif args.analysis == "interaction":
        print(interaction_analysis(output, args.quick).head(20).to_string(index=False))
    elif args.analysis == "contribution":
        print(power_contribution_analysis(output).to_string(index=False))
    elif args.analysis == "monte_carlo":
        df = monte_carlo_analysis(output, args.quick, n_runs=args.mc_runs)
        print(df["tte_h"].describe().to_string())
    elif args.analysis == "validation":
        print(validation_analysis(output, args.benchmark_csv, args.quick).to_string(index=False))
    elif args.analysis == "timestep":
        print(timestep_analysis(output, args.quick).to_string(index=False))



def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    run_selected(args)
    print(f"Results saved to: {Path(args.output).resolve()}")


if __name__ == "__main__":
    main()
