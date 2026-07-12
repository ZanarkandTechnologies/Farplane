#!/usr/bin/env python3
"""Focused tests for adaptive ticket-history projection."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("query_ticket_history.py")
SPEC = importlib.util.spec_from_file_location("query_ticket_history", MODULE_PATH)
assert SPEC and SPEC.loader
HISTORY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HISTORY)


def write_ticket(
    root: Path,
    ticket_id: str,
    *,
    updated_at: str,
    status: str = "done",
    kpi_id: str | None = None,
    decision: str = "",
    archived: bool = True,
) -> None:
    base = root / "tickets" / ("archive" if archived else "") / ticket_id
    base.mkdir(parents=True, exist_ok=True)
    reward = ""
    if kpi_id:
        reward = f'''\n## Reward\n\n```yaml\nkpi_rewards:\n  - reward_id: {ticket_id.lower()}-reward\n    kpi_id: {kpi_id}\n    expected_reward: expected {kpi_id}\n    actual_result: observed result\n    decision: {decision}\n    check_in_at: 2026-07-10T00:00:00Z\n    evaluated_at: 2026-07-11T00:00:00Z\n    evidence_refs: [proof.md]\n```\n'''
    (base / "ticket.md").write_text(
        f'''---\nticket_id: {ticket_id}\ntitle: {ticket_id} title\nstatus: {status}\ncreated_at: 2026-07-01T00:00:00Z\nupdated_at: {updated_at}\n---\n\n# {ticket_id}\n\n## Summary\n\nReason for creating {ticket_id}.\n{reward}''',
        encoding="utf-8",
    )


class TicketHistoryQueryTests(unittest.TestCase):
    def make_root(self, tmp: str) -> Path:
        root = Path(tmp)
        farplane = root / "farplane"
        farplane.mkdir()
        (farplane / "harness.yaml").write_text(
            '''areas:\n  marketing:\n    metric_refs:\n      - metric_id: reach_per_artifact\n  self_improvement:\n    metric_refs:\n      - metric_id: accepted_harness_improvements\n''',
            encoding="utf-8",
        )
        return root

    def test_recent_global_sample_projects_rewards_areas_and_origin(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            write_ticket(root, "TASK-0001", updated_at="2026-07-10T00:00:00Z", kpi_id="reach_per_artifact", decision="accept")
            write_ticket(root, "TASK-0002", updated_at="2026-07-11T00:00:00Z", kpi_id="accepted_harness_improvements", decision="kill")
            decisions = root / ".farplane" / "automation" / "decisions.jsonl"
            decisions.parent.mkdir(parents=True)
            decisions.write_text(
                json.dumps({"action": "plan_next_wave", "pulse_receipt": {"admitted": ["TASK-0001"]}}) + "\n",
                encoding="utf-8",
            )

            result = HISTORY.build_history(root, limit=20)

            self.assertEqual([row["ticket_id"] for row in result["rows"]], ["TASK-0002", "TASK-0001"])
            first = result["rows"][0]
            self.assertEqual(first["area_refs"], ["self_improvement"])
            self.assertEqual(first["rewards"][0]["actual_result"], "observed result")
            self.assertEqual(result["rows"][1]["creation_origin"], "ai_planned")
            self.assertEqual(result["area_distribution"], {"marketing": 1, "self_improvement": 1})

    def test_progressive_filters_narrow_ai_created_area_history(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            write_ticket(root, "TASK-0001", updated_at="2026-07-10T00:00:00Z", kpi_id="reach_per_artifact", decision="accept")
            write_ticket(root, "TASK-0002", updated_at="2026-07-11T00:00:00Z", kpi_id="accepted_harness_improvements", decision="kill")
            decisions = root / ".farplane" / "automation" / "decisions.jsonl"
            decisions.parent.mkdir(parents=True)
            decisions.write_text(
                json.dumps({"action": "plan_next_wave", "pulse_receipt": {"admitted": ["TASK-0001", "TASK-0002"]}}) + "\n",
                encoding="utf-8",
            )

            result = HISTORY.build_history(
                root,
                origins={"ai_planned"},
                areas={"marketing"},
                reward_decisions={"accept"},
            )

            self.assertEqual([row["ticket_id"] for row in result["rows"]], ["TASK-0001"])
            self.assertEqual(result["query"]["areas"], ["marketing"])

    def test_unknown_area_is_explicit_and_title_is_not_used(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            write_ticket(root, "TASK-MARKETING-NAME", updated_at="2026-07-10T00:00:00Z", kpi_id=None)

            result = HISTORY.build_history(root)

            self.assertEqual(result["rows"][0]["area_refs"], ["unknown"])
            self.assertEqual(result["rows"][0]["creation_origin"], "direct_or_unknown")

    def test_planner_receipt_selected_area_overrides_shared_kpi_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            (root / "farplane" / "harness.yaml").write_text(
                '''areas:\n  self_improvement:\n    metric_refs:\n      - metric_id: accepted_harness_improvements\n  framework_delivery:\n    metric_refs:\n      - metric_id: accepted_harness_improvements\n''',
                encoding="utf-8",
            )
            write_ticket(
                root,
                "TASK-0003",
                updated_at="2026-07-12T00:00:00Z",
                kpi_id="accepted_harness_improvements",
            )
            decisions = root / ".farplane" / "automation" / "decisions.jsonl"
            decisions.parent.mkdir(parents=True)
            decisions.write_text(
                json.dumps(
                    {
                        "action": "plan_next_wave",
                        "status": "completed",
                        "admitted": ["TASK-0003"],
                        "admitted_specs": [
                            {"ticket_id": "TASK-0003", "area_id": "framework_delivery"}
                        ],
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            result = HISTORY.build_history(root)

            self.assertEqual(result["rows"][0]["area_refs"], ["framework_delivery"])
            self.assertEqual(result["rows"][0]["area_derivation"], "planner_receipt")


if __name__ == "__main__":
    unittest.main()
