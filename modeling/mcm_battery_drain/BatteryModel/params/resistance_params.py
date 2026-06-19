class ResistanceParams:

    def __init__(self):

        self.T_ref = 25.0

        self.z_ref = 0.5

        # SOH影响系数
        self.a = 3.0

        # 温度影响系数
        self.lam = 0.03

        # SOC影响系数
        self.c = 1.0