# 分析报告图表复现说明

本压缩包可以直接重新生成 Word 报告中使用的全部图表。此前版本的问题是：各分析只能逐项运行，没有把报告所采用的 `--quick` 参数和 30 次蒙特卡洛固定为一个完整流程，因此容易出现“代码能运行单项，但无法一次生成报告全部图片”的情况。

## 最简单的运行方法（Windows）

1. 解压整个压缩包，不能只单独复制 `BatteryModel` 文件夹中的某个 `.py` 文件。
2. 安装 Python 3.10 或更高版本。
3. 双击：`运行全部报告图表.bat`。
4. 全部结果会写入：`generated_figures`。

脚本会先检查依赖；缺少依赖时会自动执行：

```bash
python -m pip install -r requirements.txt
```

## 命令行运行

在本说明文件所在目录执行：

```bash
python generate_all_figures.py --profile report --output generated_figures
```

这条命令与已交付 Word 报告的计算配置一致：

- 初始 SOC、温度、SOH、消融、终止机制、交互、功耗分解、验证和时间步分析均使用快速复现配置；
- 蒙特卡洛固定随机种子，运行 30 次；
- 自动生成 30 张 PNG、各模块 CSV、`figure_manifest.csv` 和运行时间记录；
- 结束前会逐张检查图片是否存在，缺失时直接报错。

## 完整精度分析

```bash
python generate_all_figures.py --profile full --mc-runs 500 --output full_results
```

完整精度配置计算量更大，结果与报告中的“快速复现图”可能有小幅差异，这是时间步和蒙特卡洛样本数不同造成的。

## 单独生成某类图片

```bash
python generate_all_figures.py --only interaction --profile report --output generated_figures
python generate_all_figures.py --only monte_carlo --profile report --mc-runs 30 --output generated_figures
```

`--only` 可选值：

- `soc`
- `temperature`
- `soh`
- `ablation`
- `stop`
- `interaction`
- `contribution`
- `monte_carlo`
- `validation`
- `timestep`

## 报告中配图与输出文件对应关系

- 初始 SOC：`01_initial_soc`
- 温度分析：`02_temperature`
- SOH 分析：`03_soh`
- 模型消融：`04_ablation`
- 终止机制：`05_stop_reason`
- 双因素交互：`06_interactions`
- 功耗贡献：`07_power_contribution`
- 蒙特卡洛：`08_monte_carlo`
- 基准一致性：`09_validation`
- 时间步稳定性：`10_timestep`

## 常见问题

### 1. 提示 No module named BatteryModel

必须在压缩包解压后的根目录运行 `generate_all_figures.py`，不要进入 `BatteryModel` 子目录后再运行 `python -m BatteryModel.main`。

### 2. 运行很久没有图片

图表在每个分析模块结束时写入。交互分析需要完成 95 个耦合工况；完整精度下的 500 次蒙特卡洛也需要较长计算。使用报告复现配置即可生成报告中同类型、同参数的图片。

### 3. 中文目录或路径问题

脚本使用 `pathlib` 处理路径，支持中文目录。仍建议将压缩包解压到较短路径，例如：

```text
D:\BatteryModel_reproducible
```
