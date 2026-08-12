from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = ROOT / "bin" / "core"
TEST_DIR = Path(__file__).resolve().parent
for path in (CORE_DIR, TEST_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from farplane_project_snapshot import build_metric_card, load_project_snapshot
from test_farplane_project_snapshot import add_metric, write_minimal_project


class LeverageMetricProjectionTests(unittest.TestCase):
    def test_markdown_metric_uses_latest_text_without_numeric_projections(self) -> None:
        observations = [
            {"metric_id": "edge", "date": "2026-07-01", "value": "One hard-earned proof.", "status": "available"},
            {"metric_id": "edge", "date": "2026-07-01", "value": "One hard-earned proof.", "status": "available"},
            {"metric_id": "edge", "date": "2026-07-02", "value": "A newer demonstrable advantage.", "status": "available"},
        ]
        card = build_metric_card("edge", {"type": "markdown", "leverage": "edge", "max_age_days": 7}, observations, "2026-07-02")

        self.assertEqual(card["current"]["value"], "A newer demonstrable advantage.")
        self.assertEqual(card["current"]["observed_at"], "2026-07-02")
        self.assertEqual(card["status"], "available")
        self.assertEqual(card["leverage"], "edge")
        self.assertIsNone(card["comparison"])
        self.assertIsNone(card["cumulative"])
        self.assertEqual(card["series"], [])
        self.assertNotIn("display", card)
        self.assertNotIn("unit", card)
        self.assertNotIn("target", card)

    def test_markdown_metric_conflict_becomes_a_source_gap(self) -> None:
        observations = [
            {"metric_id": "edge", "date": "2026-07-02", "value": "First claim.", "status": "available"},
            {"metric_id": "edge", "date": "2026-07-02", "value": "Conflicting claim.", "status": "available"},
        ]
        card = build_metric_card("edge", {"type": "markdown", "leverage": "edge", "max_age_days": 7}, observations, "2026-07-02")

        self.assertEqual(card["status"], "source_gap")
        self.assertIsNone(card["current"]["value"])
        self.assertIsNone(card["comparison"])
        self.assertEqual(card["source_gaps"][0]["reason"], "conflicting_daily_observations")

    def test_markdown_metric_preserves_last_valid_value_after_a_source_gap(self) -> None:
        observations = [
            {"metric_id": "edge", "date": "2026-07-01", "value": "Verified proof.", "status": "available"},
            {"metric_id": "edge", "date": "2026-07-02", "value": None, "status": "source_gap", "payload": {"reason": "invalid_markdown_refresh_value"}},
        ]
        card = build_metric_card("edge", {"type": "markdown", "leverage": "edge", "max_age_days": 7}, observations, "2026-07-02")

        self.assertEqual(card["status"], "partial")
        self.assertEqual(card["current"]["value"], "Verified proof.")
        self.assertEqual(card["current"]["observed_at"], "2026-07-01")
        self.assertEqual(card["source_gaps"][0]["reason"], "invalid_markdown_refresh_value")

    def test_snapshot_carries_observed_distribution_account_on_the_raw_card(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_minimal_project(root)
            add_metric(
                root,
                "instagram_followers",
                {"label": "Instagram followers", "description": "Current follower count.", "type": "stock", "unit": "followers", "display": "line", "direction": "maximize", "leverage": "distribution"},
                "Collect the account follower count.",
            )
            batch_path = root / ".farplane" / "metrics" / "observations" / "instagram_account_metrics" / "2026-08-12.json"
            batch_path.parent.mkdir(parents=True)
            batch_path.write_text(json.dumps({"schema_version": 1, "date": "2026-08-12", "source_id": "instagram_account_metrics", "status": "available", "observations": [{"metric_id": "instagram_followers", "date": "2026-08-12", "value": 921, "status": "available"}], "gaps": [], "payload": {"distribution_account": {"platform": "instagram", "account_id": "17841400000000000", "label": "@kenji"}}}), encoding="utf-8")

            snapshot = load_project_snapshot(root, "2026-08-12")

        card = {card["metric_id"]: card for card in snapshot["metrics"]["series"]}["instagram_followers"]
        self.assertEqual(card["distribution_account"], {"platform": "instagram", "account_id": "17841400000000000", "label": "@kenji"})


if __name__ == "__main__":
    unittest.main()
