# 手机电池 SOC–SOH–Thevenin 2RC–热效应耦合模型

本版本在原项目基础上完成了结构化重构，并新增论文所需的高级分析。核心变化包括：

- TTE 改为仿真到实际终止条件的时间，不再仅用固定 1 小时后的瞬时能量/功率比代替；
- 统一记录 `SOC threshold`、`voltage cutoff`、`thermal protection` 和最大仿真时间；
- 修复信号质量 1–5 与原弱信号参考值 0.7 不一致、弱信号效应失效的问题；
- 网络流量同时兼容 0–1 归一化输入和原代码的 0–10 输入；
- 统一包路径，可在任意父目录运行，不依赖原 GitHub 仓库层级；
- 2RC 极化支路改为精确离散更新，避免大时间步下显式欧拉积分发散；
- 热模型加入设备功耗向电池的热耦合，温度轨迹不再被过大的散热系数压平；
- 仿真配置、结果、场景、随机行为和分析模块解耦；
- 所有分析自动导出 UTF-8-SIG CSV 和 300 dpi PNG。

## 安装

```bash
pip install -r BatteryModel/requirements.txt
```

在 `BatteryModel` 的上一级目录运行：

```bash
python -m BatteryModel.main --analysis scenario --scenario game --output results
```

也可直接运行：

```bash
python BatteryModel/main.py --analysis scenario --scenario game --output results
```

## 新增分析命令

```bash
# 1. 初始 SOC–TTE
python -m BatteryModel.main --analysis soc --output results

# 2. 环境温度
python -m BatteryModel.main --analysis temperature --output results

# 3. SOH
python -m BatteryModel.main --analysis soh --output results

# 4. 模型增量/消融
python -m BatteryModel.main --analysis ablation --output results

# 5. TTE 终止原因与区域图
python -m BatteryModel.main --analysis stop --output results

# 6. 双因素交互：亮度×CPU、CPU×GPU、网络×信号、温度×SOH
python -m BatteryModel.main --analysis interaction --output results

# 7. 场景内功耗贡献分解
python -m BatteryModel.main --analysis contribution --output results

# 8. 蒙特卡洛不确定性（默认 500 次）
python -m BatteryModel.main --analysis monte_carlo --mc-runs 500 --output results

# 9. 与现有 TTE 基准表进行物理一致性比较
python -m BatteryModel.main --analysis validation --output results

# 10. 时间步长与数值稳定性
python -m BatteryModel.main --analysis timestep --output results
```

## 单因素灵敏度

```bash
python -m BatteryModel.main --analysis sensitivity --scenario game \
  --parameter brightness --values 0.2,0.4,0.6,0.8,1.0 --output results
```

可选参数：`brightness`、`cpu`、`gpu`、`network_traffic`、`signal_quality`、`gps`、`background`。

## 输出结构

每项分析单独保存在编号目录中：

- `01_initial_soc`
- `02_temperature`
- `03_soh`
- `04_ablation`
- `05_stop_reason`
- `06_interactions`
- `07_power_contribution`
- `08_monte_carlo`
- `09_validation`
- `10_timestep`

其中验证模块使用项目已有的 `data/extracted_csvs/06_TTE基准结果.csv`。该数据不是完整实测放电数据，因此程序明确将结果标记为“基准/物理一致性比较”，不能在论文中表述为严格实验验证。

## 回归测试

```bash
python -m unittest BatteryModel.tests.test_smoke -v
```

测试覆盖弱信号惩罚、低温、SOH、终止原因以及 1–30 s 时间步稳定性。

## 一键复现 Word 报告中的全部图片

请返回压缩包根目录，不要停留在 `BatteryModel` 子目录中，执行：

```bash
python generate_all_figures.py --profile report --output generated_figures
```

Windows 用户也可直接双击根目录下的：

```text
运行全部报告图表.bat
```

该入口会采用报告实际使用的参数，生成 30 张 PNG、对应 CSV、运行日志和图片完整性清单。详细说明见根目录的 `README_图表复现说明.md`。
