class AgingParams:

    def __init__(self):

        # 老化速率系数
        self.k0 = 1e-8

        # 活化能(J/mol)
        self.Ea = 35000.0

        # 气体常数
        self.Rg = 8.314

        # C倍率指数
        self.mu = 1.2

        # SOC偏离惩罚
        self.rho = 2.0

        # 最佳SOC区间
        self.z_mid = 0.5