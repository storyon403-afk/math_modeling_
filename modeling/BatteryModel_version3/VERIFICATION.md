# 复现验证记录

本版本已执行以下检查：

1. `python -m compileall`：通过。
2. `python -m unittest BatteryModel.tests.test_smoke -v`：5 项测试全部通过。
3. `generate_all_figures.py --only interaction --profile report`：成功生成 4 组交互分析的热力图、等高线图和三维响应面，共 12 张 PNG。
4. `generate_all_figures.py --only monte_carlo --profile report`：成功生成 30 次蒙特卡洛结果；运行 CSV 与交付报告使用的样例 CSV 数值完全一致。
5. `generate_all_figures.py --only validation --profile report`：成功生成预测值—基准值散点图及误差 CSV。
6. `generate_all_figures.py --only timestep --profile report`：成功生成时间步误差图和运行时间图。
7. 初始 SOC、温度、SOH、模型消融、终止机制的复现 CSV 与报告样例结果逐项一致。

完整一键入口会依次调用同一批已验证模块，并在结束时检查 30 张预期 PNG 是否全部存在。
