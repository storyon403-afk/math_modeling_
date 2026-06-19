# 优化与新增内容

## 核心仿真修正

1. 将 TTE 从“固定仿真时长后的瞬时能量/功率估算”改为“达到实际终止条件的仿真时间”。
2. 新增统一终止原因：SOC 阈值、端电压截止、热保护、最大仿真时间。
3. Thevenin 2RC 支路使用精确零阶保持离散公式，解决 `dt > R1*C1` 时的数值发散。
4. 修复信号质量尺度不一致问题，使 1–5 级信号能够真实影响通信功耗。
5. 网络流量同时支持 0–1 和旧版 0–10 输入。
6. 热模型加入 CPU/GPU/屏幕等设备功耗向电池的热耦合，并调整等效散热参数。
7. OCV 曲线由线性模型改为平滑非线性近似。
8. 所有仓库特定绝对导入改为独立 `BatteryModel` 包导入。

## 新增分析

- 初始 SOC–TTE 分析；
- 环境温度、端电压、SOC、温升及相对老化速率分析；
- 初始 SOH 与续航下降率分析；
- 基准、SOC、2RC、热效应、SOH 的逐步增量/消融分析；
- TTE 终止原因表与温度–SOH 终止机制区域图；
- 亮度×CPU、CPU×GPU、网络×信号、温度×SOH 双因素交互；
- 功耗组成与占比分解；
- 蒙特卡洛不确定性、95% 区间和分布图；
- 基准表物理一致性比较及 MAE、RMSE、MAPE；
- 时间步长误差和计算效率分析。

## 输出与工程化

- 每项分析自动输出 UTF-8-SIG CSV；
- 自动生成 300 dpi PNG；
- 新增命令行参数、场景库、统一仿真配置和结果对象；
- 新增 5 项轻量回归测试；
- 保留原 `simulate()` 接口和旧绘图函数名以兼容已有调用。

## Reproducible report-figure release

- Added root-level `generate_all_figures.py` to reproduce every figure used in the Word report.
- Added a fixed `report` profile: quick deterministic analyses plus 30 Monte Carlo runs with the existing fixed random seed.
- Added per-module log files, progress reporting, output manifest, and missing-figure validation.
- Added Windows launchers `运行全部报告图表.bat` and `运行完整精度分析.bat`.
- Added `README_图表复现说明.md` with exact commands and output-to-report mapping.
