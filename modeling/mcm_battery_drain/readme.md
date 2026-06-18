项目目录结构如下：


BatteryModel/

├── models/
│
│   ├── state.py          # BatteryState
│   ├── params.py         # BatteryParams
│   ├── behavior.py       # 用户行为层
│   ├── electrical.py     # Thevenin 2RC + 电流求解
│   ├── thermal.py        # 热模型
│   ├── soc.py            # SOC方程
│   ├── soh.py            # SOH方程
│   └── tte.py            # TTE终止判断
│
├── simulation/
│
│   └── simulator.py      # 主迭代循环
│
├── data/
│
├── plots/
│
└── main.py