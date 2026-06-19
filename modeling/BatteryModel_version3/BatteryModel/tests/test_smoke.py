"""Lightweight regression tests for the optimized battery model."""
from __future__ import annotations

import unittest

from BatteryModel.analysis.common import run_scenario_case
from BatteryModel.physics.load import weak_signal_penalty
from BatteryModel.simulation.config import SimulationConfig


class BatteryModelSmokeTests(unittest.TestCase):
    def test_weak_signal_penalty_is_monotonic(self):
        self.assertGreater(weak_signal_penalty(1), weak_signal_penalty(3))
        self.assertGreater(weak_signal_penalty(3), weak_signal_penalty(5))
        self.assertEqual(weak_signal_penalty(5), 0.0)

    def test_lower_soh_reduces_game_tte(self):
        cfg = SimulationConfig(dt_s=10, max_time_s=24 * 3600, record_interval_s=300)
        new, _, _ = run_scenario_case("game", initial_soh=1.0, config=cfg)
        aged, _, _ = run_scenario_case("game", initial_soh=0.8, config=cfg)
        self.assertLess(aged.tte_hours, new.tte_hours)

    def test_low_temperature_reduces_game_tte(self):
        cfg = SimulationConfig(dt_s=10, max_time_s=24 * 3600, record_interval_s=300)
        normal, _, _ = run_scenario_case("game", ambient_temp=25, config=cfg)
        cold, _, _ = run_scenario_case("game", ambient_temp=0, config=cfg)
        self.assertLess(cold.tte_hours, normal.tte_hours)

    def test_time_step_stability(self):
        fine_cfg = SimulationConfig(dt_s=1, max_time_s=24 * 3600, record_interval_s=600)
        coarse_cfg = SimulationConfig(dt_s=30, max_time_s=24 * 3600, record_interval_s=600)
        fine, _, _ = run_scenario_case("game", config=fine_cfg)
        coarse, _, _ = run_scenario_case("game", config=coarse_cfg)
        relative_error = abs(coarse.tte_hours - fine.tte_hours) / fine.tte_hours
        self.assertLess(relative_error, 0.01)

    def test_stop_reason_is_recorded(self):
        cfg = SimulationConfig(dt_s=10, max_time_s=24 * 3600, record_interval_s=300)
        result, _, _ = run_scenario_case("game", config=cfg)
        self.assertIn(result.stop_reason, {"SOC threshold", "voltage cutoff", "thermal protection"})
        self.assertTrue(result.history)
        self.assertEqual(result.history[-1]["stop_reason"], result.stop_reason)


if __name__ == "__main__":
    unittest.main()
