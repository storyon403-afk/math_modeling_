# BatteryModel Version 3

手机电池 SOC-SOH-Thevenin 2RC-热效应耦合仿真与报告图表复现项目。

项目用于模拟不同使用场景下的手机电池剩余可用时间（TTE）、终止原因、温度轨迹、SOH 老化影响、双因素交互和不确定性分析。核心代码位于 `BatteryModel/`，根目录保留一键复现脚本、依赖文件、复现说明和已生成的报告图表。

## 项目结构

```text
BatteryModel/
  analysis/        高级分析、场景分析、灵敏度分析
  data/            原始 Excel 与提取后的基准 CSV 数据
  data_progress/   数据读取与参数映射工具
  models/          状态与行为数据结构
  params/          电池、电路、热、负载等参数
  physics/         SOC、SOH、2RC、电压、热、电量终止模型
  plots/           基础绘图工具
  simulation/      仿真配置与主循环
  tests/           回归测试
generated_figures/ 报告复现输出图表与 CSV
generate_all_figures.py
requirements.txt
```

## 环境安装

建议使用 Python 3.10 或更高版本。

```bash
python -m pip install -r requirements.txt
```

## 快速运行

单场景仿真：

```bash
python -m BatteryModel.main --analysis scenario --scenario game --output results
```

运行某个分析模块：

```bash
python -m BatteryModel.main --analysis temperature --quick --output results
python -m BatteryModel.main --analysis monte_carlo --quick --mc-runs 30 --output results
```

一键复现报告图表：

```bash
python generate_all_figures.py --profile report --output generated_figures
```

完整精度分析：

```bash
python generate_all_figures.py --profile full --mc-runs 500 --output full_results
```

Windows 用户可直接运行根目录下的 `运行全部报告图表.bat` 或 `运行完整精度分析.bat`。

## 测试

```bash
python -m unittest BatteryModel.tests.test_smoke -v
```

测试覆盖弱信号惩罚、低温影响、SOH 影响、终止原因记录和时间步稳定性。

## 说明文件

- `BatteryModel/README.md`：模型模块、分析命令和理论改动说明。
- `README_图表复现说明.md`：报告图表复现流程。
- `VERIFICATION.md`：已执行的复现和测试验证记录。

## 输出与清理

默认输出目录包括 `results/`、`generated_figures/`、`full_results/`。其中 `generated_figures/` 当前保留为报告复现样例；新的临时输出建议写入 `results/` 或自定义目录。
