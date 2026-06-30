from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = ROOT / "bin" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from farplane_metrics import generate_metric_snapshots


GOALS = """---
kind: project-goals
---

# Goals

## Tracked KPIs

| Metric | Label | Axis | Product | Source | Aggregation | Cumulative | Target | Unit | Display |
| --- | --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| x_followers | X followers | distribution_from_evidence | distribution | manual_x_account | point | false | 100 | followers | line |
| x_views | X views | distribution_from_evidence | distribution | manual_x_account | daily | true | 10 | views | bar_plus_cumulative |
| accepted_output_events | Accepted output events | validated_self_improvement | productization | pulse_reward_ledger | daily | true | 2 | events | bar_plus_cumulative |
| ready_unclaimed_ticket_count | Ready unclaimed tickets | project_control | productization | ticket_board | point | false | 1 | tickets | line |
"""


BINDINGS = """---
kind: project-bindings
---

# Bindings

## Metric Source Bindings

| Source | Enabled | Type | Fetch | Path Or Account | Raw Snapshot Dir |
| --- | --- | --- | --- | --- | --- |
| pulse_reward_ledger | true | local_jsonl | farplane_metrics | .farplane/automation/rewards.jsonl | .farplane/metrics/source-snapshots/pulse_reward_ledger |
| ticket_board | true | local_files | farplane_metrics | tickets/TASK-*/ticket.md | .farplane/metrics/source-snapshots/ticket_board |
| manual_x_account | true | manual | manual_snapshot | .farplane/metrics/manual/x_account.json | .farplane/metrics/source-snapshots/manual_x_account |
"""


class FarplaneMetricsTests(unittest.TestCase):
    def test_generates_point_daily_cumulative_and_target_hits(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            (root / "farplane" / "goals.md").write_text(GOALS, encoding="utf-8")
            (root / "farplane" / "bindings.md").write_text(BINDINGS, encoding="utf-8")
            (root / ".farplane" / "automation").mkdir(parents=True)
            (root / ".farplane" / "automation" / "rewards.jsonl").write_text(
                json.dumps(
                    {
                        "ts": "2026-06-30T01:00:00Z",
                        "outcome": "positive",
                        "evidence": ["tickets/TASK-0001/artifacts/proof.md"],
                    }
                )
                + "\n"
                + json.dumps(
                    {
                        "ts": "2026-06-30T02:00:00Z",
                        "outcome": "partial_positive",
                        "evidence": ["skills/example/SKILL.md"],
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            (root / ".farplane" / "metrics" / "manual").mkdir(parents=True)
            (root / ".farplane" / "metrics" / "manual" / "x_account.json").write_text(
                json.dumps(
                    {
                        "observations": [
                            {"metric_id": "x_followers", "date": "2026-06-30", "value": 101, "status": "available"},
                            {"metric_id": "x_views", "date": "2026-06-30", "value": 4, "status": "available"},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            ticket_dir = root / "tickets" / "TASK-0001"
            ticket_dir.mkdir(parents=True)
            (ticket_dir / "ticket.md").write_text(
                """---
ticket_id: TASK-0001
title: Test
phase: building
status: todo
owner: codex
claimed_by:
ready: true
approval_required: false
updated_at: 2026-06-30T00:00:00Z
next_action: execute
---
""",
                encoding="utf-8",
            )

            result = generate_metric_snapshots(root, "2026-06-30")
            payload = json.loads(result.ui_snapshot_path.read_text(encoding="utf-8"))

        by_id = {metric["metric_id"]: metric for metric in payload["metrics"]}
        self.assertEqual(by_id["x_followers"]["current"], 101)
        self.assertEqual(by_id["x_followers"]["target_hit"]["hit_at"], "2026-06-30")
        self.assertEqual(by_id["x_views"]["series"][0]["cumulative"], 4)
        self.assertEqual(by_id["accepted_output_events"]["current"], 2)
        self.assertEqual(by_id["accepted_output_events"]["target_hit"]["hit_value"], 2)
        self.assertEqual(by_id["ready_unclaimed_ticket_count"]["current"], 1)

    def test_missing_manual_source_is_source_gap_not_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            (root / "farplane" / "goals.md").write_text(GOALS, encoding="utf-8")
            (root / "farplane" / "bindings.md").write_text(BINDINGS.replace("true | manual", "false | manual"), encoding="utf-8")
            (root / ".farplane" / "automation").mkdir(parents=True)
            (root / ".farplane" / "automation" / "rewards.jsonl").write_text("", encoding="utf-8")
            (root / "tickets").mkdir()

            result = generate_metric_snapshots(root, "2026-06-30")
            payload = json.loads(result.ui_snapshot_path.read_text(encoding="utf-8"))

        by_id = {metric["metric_id"]: metric for metric in payload["metrics"]}
        self.assertEqual(by_id["x_followers"]["status"], "source_gap")
        self.assertIsNone(by_id["x_followers"]["current"])
        self.assertIn("x_followers", {gap["metric_id"] for gap in payload["source_gaps"]})


if __name__ == "__main__":
    unittest.main()
