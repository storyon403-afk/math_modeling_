class BatteryState:
    def __init__(
        self, 
        soc: float = 1.0,        # 默认 100% 满电
        soh: float = 1.0,        # 默认 100% 健康度
        temp: float = 25.0,      # 默认 25 摄氏度
        voltage: float = 4.2,    # 默认满电电压 4.2V
        current: float = 0.0,    # 默认初始无电流
        v1: float = 0.0,         # 2RC模型极化电压1默认为0
        v2: float = 0.0          # 2RC模型极化电压2默认为0
    ):
        self.time = 0            # 仿真初始时间为 0
        self.soc = soc
        self.soh = soh
        self.temp = temp
        self.voltage = voltage
        self.current = current
        self.v1 = v1
        self.v2 = v2