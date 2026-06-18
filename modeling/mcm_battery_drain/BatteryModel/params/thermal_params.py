class ThermalParams:

    def __init__(self):

        # 热容
        self.C_th = 500.0

        # 散热系数
        self.h = 5.0

        # 环境温度
        self.T_env = 25.0

        # 低温容量修正
        self.T_ref = 25.0
        self.a_low = 0.01

        # 高温降频
        self.T_hot = 45.0
        self.a_hot = 0.02

        # 过热保护
        self.T_max = 60.0