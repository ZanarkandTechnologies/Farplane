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

LEAN_GOALS = """---
kind: project-goals
---

# Goals

## Goals

```yaml
goals:
  distribution_from_evidence:
    question: Can Farplane turn evidence into audience?
    evidence_hints:
      - content views
    smart_goals:
      - id: evidence_distribution_q3
        target: 100000 evidence-backed views by 2026-09-30
        kpis:
          - x_views
          - x_likes
        update_hint: Use x-account snapshots and tracked content.

  project_control:
    question: Can Farplane control projects?
    evidence_hints:
      - ready ticket count
    smart_goals:
      - id: project_control_q3
        target: Keep ready tickets under 3 by 2026-09-30
        kpis:
          - ready_unclaimed_ticket_count
        update_hint: Use ticket board readings.
      - id: budget_accountability_weekly
        target: Active projects get weekly runway decisions
        kpis:
          - weekly_runway_review_count
          - projects_with_runway_decisions
        update_hint: Use weekly interval reports.
```
"""


LEAN_BINDINGS = """---
kind: project-bindings
---

# Bindings

## Metric Providers

```yaml
metric_providers:
  x_account_metrics:
    provider: skill_snapshot
    skill: x-account
    writes: .farplane/metrics/manual/x_account.json
    provides:
      - x_views
      - x_likes

  ticket_board:
    provider: local_files
    path: tickets/TASK-*/ticket.md
    provides:
      - ready_unclaimed_ticket_count

  runway_review_notes:
    provider: interval_report
    path: .farplane/reports/interval/weekly_interval
    provides:
      - weekly_runway_review_count
      - projects_with_runway_decisions
```
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
                        "ts": "2026-06-29T23:00:00Z",
                        "outcome": "positive",
                        "evidence": ["tickets/TASK-0000/artifacts/proof.md"],
                    }
                )
                + "\n"
                + json.dumps(
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
        self.assertEqual(by_id["accepted_output_events"]["current"], 3)
        self.assertEqual(by_id["accepted_output_events"]["target_hit"]["hit_value"], 3)
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

    def test_reads_lean_goals_bindings_and_compact_metric_snapshots(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            (root / "farplane" / "goals.md").write_text(LEAN_GOALS, encoding="utf-8")
            (root / "farplane" / "bindings.md").write_text(LEAN_BINDINGS, encoding="utf-8")
            (root / ".farplane" / "metrics" / "manual").mkdir(parents=True)
            (root / ".farplane" / "metrics" / "manual" / "x_account.json").write_text(
                json.dumps(
                    {
                        "source": "x_account_metrics",
                        "date": "2026-07-01",
                        "status": "available",
                        "metrics": {
                            "x_views": {
                                "value": 206,
                                "items": [
                                    {
                                        "id": "x:2063623337851691167",
                                        "value": 206,
                                        "kind": "post",
                                    }
                                ],
                            },
                            "x_likes": {"value": 0},
                        },
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
updated_at: 2026-07-01T00:00:00Z
next_action: execute
---
""",
                encoding="utf-8",
            )

            generate_metric_snapshots(root, "2026-06-30")
            result = generate_metric_snapshots(root, "2026-07-01")
            payload = json.loads(result.ui_snapshot_path.read_text(encoding="utf-8"))

        by_id = {metric["metric_id"]: metric for metric in payload["metrics"]}
        self.assertEqual(by_id["x_views"]["source_id"], "x_account_metrics")
        self.assertEqual(by_id["x_views"]["current"], 206)
        self.assertIsNone(by_id["x_views"]["series"][0]["daily_diff"])
        self.assertEqual(by_id["x_views"]["series"][-1]["daily_diff"], 0)
        self.assertEqual(by_id["x_views"]["series"][-1]["items"][0]["id"], "x:2063623337851691167")
        self.assertEqual(by_id["ready_unclaimed_ticket_count"]["current"], 1)
        self.assertEqual(by_id["weekly_runway_review_count"]["status"], "source_gap")

    def test_reads_budget_runway_review_from_weekly_interval_reports(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            (root / "farplane" / "goals.md").write_text(LEAN_GOALS, encoding="utf-8")
            (root / "farplane" / "bindings.md").write_text(LEAN_BINDINGS, encoding="utf-8")
            (root / ".farplane" / "metrics" / "manual").mkdir(parents=True)
            (root / ".farplane" / "metrics" / "manual" / "x_account.json").write_text(
                json.dumps({"status": "source_gap", "gaps": ["not_configured"]}),
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
ready: false
approval_required: false
updated_at: 2026-07-01T00:00:00Z
next_action: wait
---
""",
                encoding="utf-8",
            )
            report_dir = root / ".farplane" / "reports" / "interval" / "weekly_interval"
            report_dir.mkdir(parents=True)
            (report_dir / "2026-07-01T000000Z.md").write_text(
                """# Weekly

## Budget / Runway Review

| Active project | Contribution mode | Spend / attention used | Expected reward | Observed evidence | Decision | Next constraint |
| --- | --- | --- | --- | --- | --- | --- |
| Evidence loop | distribution | rough: one ticket | views | metric snapshot | continue | ship two posts |
| Adoption loop | learning | rough: one ticket | provider | source gap | instrument | add ledger |

## Next Window Plan
""",
                encoding="utf-8",
            )

            result = generate_metric_snapshots(root, "2026-07-01")
            payload = json.loads(result.ui_snapshot_path.read_text(encoding="utf-8"))

        by_id = {metric["metric_id"]: metric for metric in payload["metrics"]}
        self.assertEqual(by_id["weekly_runway_review_count"]["current"], 1)
        self.assertEqual(by_id["projects_with_runway_decisions"]["current"], 2)


if __name__ == "__main__":
    unittest.main()
