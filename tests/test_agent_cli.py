import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src import agent_cli


class AgentCliTests(unittest.TestCase):
    def test_persian_agent_aliases_are_supported(self):
        self.assertEqual(agent_cli.AGENT_ALIASES["کدکس"], "codex")
        self.assertEqual(agent_cli.AGENT_ALIASES["اخبار"], "news")

    def test_news_draft_contains_high_impact_events(self):
        events = [
            {"country": "USD", "date": "2026-09-24T12:30:00+00:00", "title": "CPI", "impact": "High"},
            {"country": "EUR", "date": "2026-09-24T08:00:00+00:00", "title": "Survey", "impact": "Low"},
        ]
        with tempfile.TemporaryDirectory() as directory, patch.object(agent_cli, "OUTPUT", Path(directory)), patch.object(agent_cli, "fetch_calendar", return_value=events):
            target = agent_cli.run_news("https://example.test/calendar.json")
            report = target.read_text(encoding="utf-8")
        self.assertIn("CPI", report)
        self.assertNotIn("Survey", report)
        self.assertIn("نه سیگنال", report)

    def test_studio_rejects_missing_screenshot_before_model_call(self):
        with self.assertRaises(SystemExit), patch.object(agent_cli, "call_gemini") as model:
            agent_cli.run_studio("brief", Path("not-a-real-chart.png"))
        model.assert_not_called()


if __name__ == "__main__":
    unittest.main()
