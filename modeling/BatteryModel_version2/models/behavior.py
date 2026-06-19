"""User workload definitions used by the battery simulation."""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Dict
import numpy as np


@dataclass
class UserBehavior:
    """Normalized phone workload.

    Parameters are expected in [0, 1], except ``network_traffic`` which also
    accepts the legacy 0--10 scale, and ``signal_quality`` which uses 1--5
    (1 = very weak, 5 = excellent).
    """

    brightness: float = 0.6
    cpu: float = 0.35
    gpu: float = 0.10
    network_traffic: float = 0.5
    signal_quality: float = 4.0
    gps: float = 0.0
    background: float = 0.08

    def clipped(self) -> "UserBehavior":
        traffic = float(self.network_traffic)
        if traffic > 1.0:  # backward compatible with the old 0--10 inputs
            traffic /= 10.0
        return UserBehavior(
            brightness=float(np.clip(self.brightness, 0.0, 1.0)),
            cpu=float(np.clip(self.cpu, 0.0, 1.0)),
            gpu=float(np.clip(self.gpu, 0.0, 1.0)),
            network_traffic=float(np.clip(traffic, 0.0, 1.0)),
            signal_quality=float(np.clip(self.signal_quality, 1.0, 5.0)),
            gps=float(np.clip(self.gps, 0.0, 1.0)),
            background=float(np.clip(self.background, 0.0, 1.0)),
        )

    def copy_with(self, **changes: float) -> "UserBehavior":
        return replace(self, **changes)


class PiecewiseRandomBehavior:
    """Piecewise-constant stochastic workload for Monte Carlo analysis.

    A new sample is generated every ``interval_s`` seconds. Samples follow
    clipped normal distributions around the base behavior, which captures both
    run-to-run variability and temporal fluctuations without making the
    simulation unnecessarily expensive.
    """

    def __init__(
        self,
        base: UserBehavior,
        rng: np.random.Generator,
        interval_s: float = 60.0,
        relative_sigma: Dict[str, float] | None = None,
    ) -> None:
        self.base = base.clipped()
        self.rng = rng
        self.interval_s = max(float(interval_s), 1.0)
        self.relative_sigma = relative_sigma or {
            "brightness": 0.08,
            "cpu": 0.15,
            "gpu": 0.18,
            "network_traffic": 0.20,
            "signal_quality": 0.10,
            "background": 0.15,
        }
        self._bin = None
        self._current = self.base

    def __call__(self, time_s: float) -> UserBehavior:
        current_bin = int(time_s // self.interval_s)
        if current_bin != self._bin:
            self._bin = current_bin
            values = {}
            for name in (
                "brightness", "cpu", "gpu", "network_traffic",
                "signal_quality", "background",
            ):
                mean = float(getattr(self.base, name))
                sigma = self.relative_sigma.get(name, 0.0) * max(abs(mean), 0.05)
                values[name] = float(self.rng.normal(mean, sigma))
            values["gps"] = self.base.gps
            self._current = self.base.copy_with(**values).clipped()
        return self._current
