import csv
import tempfile
import unittest
from pathlib import Path

from xauusd_paper_assistant.src.mt5_source import rows_to_csv


class Mt5ExportFormatTests(unittest.TestCase):
    def test_export_marks_bar_available_only_at_close(self):
        rows = [{"time": 1735689600, "open": 1, "high": 2, "low": 0.5, "close": 1.5, "spread": 20, "tick_volume": 10}]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bars.csv"
            self.assertEqual(rows_to_csv(rows, "XAUUSD", "M5", path), 1)
            with path.open() as handle:
                exported = list(csv.DictReader(handle))[0]
        self.assertEqual(exported["event_time_utc"], "2025-01-01T00:05:00Z")
        self.assertEqual(exported["available_at_utc"], "2025-01-01T00:05:00Z")
        self.assertEqual(exported["source"], "MT5")
