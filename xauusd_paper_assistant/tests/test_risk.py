import unittest
from datetime import datetime, timezone

from xauusd_paper_assistant.src.models import SignalIntent
from xauusd_paper_assistant.src.risk import decide


CONFIG = {"max_open_positions": 1, "max_daily_drawdown_pct": 2, "min_rr": 2, "tick_size": .01, "tick_value_per_lot": 1, "max_risk_pct": 1, "volume_min": .01, "volume_max": 5, "volume_step": .01}
SIGNAL = SignalIntent("BUY", 100, 99, 102, datetime.now(timezone.utc), "test")


class RiskTests(unittest.TestCase):
    def test_size_is_rounded_down_and_within_budget(self):
        decision = decide(SIGNAL, 10000, 10000, 0, CONFIG)
        self.assertTrue(decision.approved)
        self.assertEqual(decision.volume, 1.0)

    def test_minimum_volume_rejects_instead_of_exceeding_risk(self):
        config = {**CONFIG, "volume_min": 2.0}
        decision = decide(SIGNAL, 10000, 10000, 0, config)
        self.assertFalse(decision.approved)
        self.assertIn("MIN_VOLUME_EXCEEDS_RISK", decision.reason_codes)

    def test_circuit_breaker_rejects(self):
        decision = decide(SIGNAL, 9700, 10000, 0, CONFIG)
        self.assertFalse(decision.approved)
        self.assertIn("DAILY_CIRCUIT_BREAKER", decision.reason_codes)
