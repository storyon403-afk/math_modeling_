"""Thermal parameters for the coupled battery/device model."""


class ThermalParams:
    def __init__(self):
        # Lumped battery/device thermal capacity (J/K)
        self.C_th = 500.0

        # Effective heat-transfer coefficient to ambient (W/K). The original
        # value 5 W/K suppressed almost all temperature dynamics; 0.15 W/K
        # corresponds to a thermal time constant of roughly 0.9 h.
        self.h = 0.15

        # Fraction of phone load power thermally coupled into the battery pack.
        # This complements I^2R heat and captures CPU/GPU/display heat transfer.
        self.device_heat_fraction = 0.18

        self.T_env = 25.0

        # Low-temperature usable-capacity correction
        self.T_ref = 25.0
        self.a_low = 0.01

        # Reserved thermal-throttling parameters
        self.T_hot = 45.0
        self.a_hot = 0.02

        # Thermal protection threshold
        self.T_max = 60.0
