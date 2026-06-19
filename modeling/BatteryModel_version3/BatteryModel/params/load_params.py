"""Parameters of the component-level phone power model."""


class LoadPowerParams:
    def __init__(self, p0: float = 0.35):
        # Base/platform power (W)
        self.p0 = p0

        # Display
        self.k0 = 1.2
        self.As = 1.0
        self.gamma = 1.4

        # CPU/GPU dynamic power
        self.kc = 1.5
        self.alpha = 2.0
        self.kg = 1.8
        self.beta = 2.2

        # Radio: traffic is normalized to 0--1; weak-signal penalty is 0--1.
        self.p_net0 = 0.25
        self.kr = 0.65
        self.ks = 0.65
        self.s_ref = 0.7  # retained for compatibility; no longer used directly

        self.k_gps = 0.35
        self.k_bg = 0.30
