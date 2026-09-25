import json
import tempfile
import unittest
from pathlib import Path

from xauusd_paper_assistant.src.cli import run


ROOT = Path(__file__).resolve().parents[2]


class PaperResearchReportTests(unittest.TestCase):
    def test_synthetic_run_emits_insufficient_evidence_report(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            run(
                ROOT / "xauusd_paper_assistant/data/sample_xauusd_m5.csv",
                ROOT / "xauusd_paper_assistant/config/paper.json",
                output,
            )
            report = json.loads((output / "paper_research_report.json").read_text())
        self.assertEqual(report["mode"], "PAPER")
        self.assertEqual(report["data_kind"], "synthetic")
        self.assertEqual(report["evidence_status"], "INSUFFICIENT_EVIDENCE")
