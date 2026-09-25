import tempfile
import unittest
from pathlib import Path

from xauusd_paper_assistant.src.data import load_csv


class DataTests(unittest.TestCase):
    def test_look_ahead_bar_is_rejected(self):
        content = "event_time_utc,available_at_utc,open,high,low,close,spread_points,tick_volume,symbol,source\n2025-01-01T00:00:00Z,2025-01-01T00:05:00Z,1,2,0.5,1.5,2,3,XAUUSD,test\n"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bars.csv"
            path.write_text(content)
            bars, issues = load_csv(path)
        self.assertEqual(bars, [])
        self.assertIn("ROW_2:LOOK_AHEAD_AVAILABLE_AT", issues)
