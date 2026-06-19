"""One-click reproduction of every figure used in the Word analysis report.

Run from any directory:
    python generate_all_figures.py

The default ``report`` profile reproduces the figures delivered with the report:
- all deterministic analyses use ``--quick``;
- Monte Carlo uses 30 runs with the fixed seed embedded in the model;
- outputs are written into ``generated_figures`` beside this script.
"""
from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from pathlib import Path
from time import perf_counter

PROJECT_ROOT = Path(__file__).resolve().parent
PACKAGE_DIR = PROJECT_ROOT / "BatteryModel"

EXPECTED_PNG = [
    "01_initial_soc/initial_soc_tte.png",
    "01_initial_soc/initial_soc_scenario_comparison.png",
    "02_temperature/temperature_tte.png",
    "02_temperature/temperature_scenario_heatmap.png",
    "02_temperature/game_voltage_by_temperature.png",
    "02_temperature/game_temperature_trajectories.png",
    "02_temperature/game_soc_by_temperature.png",
    "02_temperature/temperature_relative_aging_rate.png",
    "03_soh/soh_tte.png",
    "03_soh/soh_voltage_trajectories.png",
    "04_ablation/model_ablation.png",
    "05_stop_reason/stop_reason_map.png",
    "06_interactions/brightness_cpu_heatmap.png",
    "06_interactions/brightness_cpu_contour.png",
    "06_interactions/brightness_cpu_surface.png",
    "06_interactions/cpu_gpu_heatmap.png",
    "06_interactions/cpu_gpu_contour.png",
    "06_interactions/cpu_gpu_surface.png",
    "06_interactions/network_signal_heatmap.png",
    "06_interactions/network_signal_contour.png",
    "06_interactions/network_signal_surface.png",
    "06_interactions/temperature_soh_heatmap.png",
    "06_interactions/temperature_soh_contour.png",
    "06_interactions/temperature_soh_surface.png",
    "07_power_contribution/power_contribution_stacked.png",
    "08_monte_carlo/monte_carlo_histogram.png",
    "08_monte_carlo/monte_carlo_boxplot.png",
    "09_validation/predicted_vs_reference.png",
    "10_timestep/timestep_error.png",
    "10_timestep/timestep_runtime.png",
]

STEPS = [
    ("soc", "初始 SOC—TTE 分析"),
    ("temperature", "环境温度分析"),
    ("soh", "SOH 老化分析"),
    ("ablation", "模型增量与消融分析"),
    ("stop", "TTE 终止原因分析"),
    ("interaction", "双因素交互分析"),
    ("contribution", "场景功耗贡献分解"),
    ("monte_carlo", "蒙特卡洛不确定性分析"),
    ("validation", "基准一致性分析"),
    ("timestep", "时间步长稳定性分析"),
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="生成报告中使用的全部电池 TTE 分析图")
    parser.add_argument(
        "--profile",
        choices=["report", "full"],
        default="report",
        help="report=复现已交付报告图；full=更细时间步和默认500次蒙特卡洛",
    )
    parser.add_argument(
        "--output",
        default=str(PROJECT_ROOT / "generated_figures"),
        help="结果输出目录",
    )
    parser.add_argument(
        "--mc-runs",
        type=int,
        default=None,
        help="覆盖蒙特卡洛次数；report 默认30，full 默认500",
    )
    parser.add_argument(
        "--only",
        choices=[name for name, _ in STEPS],
        default=None,
        help="只运行某一个分析模块",
    )
    return parser


def run_step(name: str, label: str, output: Path, profile: str, mc_runs: int) -> float:
    command = [
        sys.executable,
        "-m",
        "BatteryModel.main",
        "--analysis",
        name,
        "--output",
        str(output),
    ]
    if profile == "report":
        command.append("--quick")
    if name == "monte_carlo":
        command.extend(["--mc-runs", str(mc_runs)])

    print(f"\n[{label}] 开始", flush=True)
    print("命令：" + " ".join(command), flush=True)
    started = perf_counter()
    log_dir = output / "_run_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{name}.log"
    try:
        with log_path.open("w", encoding="utf-8") as log_handle:
            subprocess.run(
                command,
                cwd=PROJECT_ROOT,
                check=True,
                stdout=log_handle,
                stderr=subprocess.STDOUT,
                timeout=1800,
            )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        tail = ""
        if log_path.is_file():
            lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
            tail = "\n".join(lines[-30:])
        raise RuntimeError(f"{label}运行失败。日志：{log_path}\n{tail}") from exc
    elapsed = perf_counter() - started
    print(f"[{label}] 完成，用时 {elapsed:.1f} s；日志：{log_path.name}", flush=True)
    return elapsed


def write_manifest(output: Path, timings: list[tuple[str, str, float]]) -> None:
    missing = [relative for relative in EXPECTED_PNG if not (output / relative).is_file()]
    manifest_path = output / "figure_manifest.csv"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["relative_path", "exists", "size_bytes"])
        for relative in EXPECTED_PNG:
            path = output / relative
            writer.writerow([relative, path.is_file(), path.stat().st_size if path.is_file() else 0])

    timing_path = output / "run_timings.csv"
    with timing_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["analysis", "label", "elapsed_seconds"])
        writer.writerows(timings)

    if missing:
        formatted = "\n".join(f"- {item}" for item in missing)
        raise RuntimeError(f"运行完成，但以下图片缺失：\n{formatted}")


def main() -> None:
    args = build_parser().parse_args()
    if not PACKAGE_DIR.is_dir():
        raise FileNotFoundError(f"未找到 BatteryModel 包目录：{PACKAGE_DIR}")

    output = Path(args.output).expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    mc_runs = args.mc_runs if args.mc_runs is not None else (30 if args.profile == "report" else 500)
    if mc_runs < 2:
        raise ValueError("蒙特卡洛次数至少为 2")

    selected = [(name, label) for name, label in STEPS if args.only in (None, name)]
    timings: list[tuple[str, str, float]] = []
    total_start = perf_counter()
    print("=" * 72)
    print("电池 TTE 报告图表一键生成")
    print(f"运行配置：{args.profile}")
    print(f"输出目录：{output}")
    print(f"蒙特卡洛次数：{mc_runs}")
    print("=" * 72, flush=True)

    for name, label in selected:
        elapsed = run_step(name, label, output, args.profile, mc_runs)
        timings.append((name, label, elapsed))

    if args.only is None:
        write_manifest(output, timings)
        print(f"\n全部 {len(EXPECTED_PNG)} 张图片均已生成并通过完整性检查。", flush=True)
    else:
        print("\n指定模块运行完成。", flush=True)
    print(f"总用时：{perf_counter() - total_start:.1f} s")
    print(f"结果位置：{output}")


if __name__ == "__main__":
    main()
