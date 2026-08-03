from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = ROOT / "bin" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

import farplane_ticket_history as history


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


def write_archive_index(root: Path, *rows: dict[str, object]) -> None:
    path = root / "tickets" / "archive-index.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


class FarplaneTicketHistoryTests(unittest.TestCase):
    def make_root(self, tmp: str) -> Path:
        root = Path(tmp)
        farplane = root / "farplane"
        farplane.mkdir()
        (farplane / "harness.yaml").write_text(
            '''areas:\n  marketing:\n    metric_refs:\n      - metric_id: reach_per_artifact\n  self_improvement:\n    metric_refs:\n      - metric_id: accepted_harness_improvements\n''',
            encoding="utf-8",
        )
        return root

    def test_projects_rewards_areas_and_origin(self) -> None:
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

            result = history.build_ticket_history(root)

        self.assertEqual([row["ticket_id"] for row in result["rows"]], ["TASK-0002", "TASK-0001"])
        self.assertEqual(result["rows"][0]["rewards"][0]["expected_reward"], "expected accepted_harness_improvements")
        self.assertEqual(result["rows"][0]["rewards"][0]["actual_result"], "observed result")
        self.assertEqual(result["rows"][1]["creation_origin"], "ai_planned")

    def test_mixed_active_legacy_and_github_issue_history_preserves_ordering(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            write_ticket(
                root,
                "TASK-0001",
                updated_at="2026-07-10T00:00:00Z",
                archived=False,
            )
            write_ticket(root, "TASK-0002", updated_at="2026-07-11T00:00:00Z")
            write_archive_index(
                root,
                {
                    "schema_version": 1,
                    "storage": "github_issue",
                    "ticket_id": "TASK-0003",
                    "title": "Remote close",
                    "status": "done",
                    "closed_at": "2026-07-12T00:00:00Z",
                    "github_issue_url": "https://github.com/acme/archive/issues/3",
                    "github_issue_number": 3,
                    "media_comment_urls": ["https://github.com/acme/archive/issues/3#issuecomment-1"],
                    "event_id": "event-3",
                    "runs": ["run-3"],
                },
            )

            result = history.build_ticket_history(root)

        self.assertEqual(
            [row["ticket_id"] for row in result["rows"]],
            ["TASK-0003", "TASK-0002", "TASK-0001"],
        )
        self.assertEqual(
            [row["storage"] for row in result["rows"]],
            ["github_issue", "local_archive", "local_active"],
        )
        self.assertEqual(
            result["rows"][0]["github_issue_url"],
            "https://github.com/acme/archive/issues/3",
        )
        self.assertEqual(result["diagnostics"], [])

    def test_progressive_filters_and_exact_planner_skill_call(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            write_ticket(root, "TASK-0003", updated_at="2026-07-12T00:00:00Z", kpi_id="accepted_harness_improvements", decision="accept")
            decisions = root / ".farplane" / "automation" / "decisions.jsonl"
            decisions.parent.mkdir(parents=True)
            decisions.write_text(
                json.dumps(
                    {
                        "action": "plan_next_wave",
                        "admitted_skill_calls": [
                            {
                                "ticket_id": "TASK-0003",
                                "area_id": "self_improvement",
                                "skill_ref": "self-improve",
                            }
                        ],
                    }
                ) + "\n",
                encoding="utf-8",
            )

            result = history.build_ticket_history(
                root,
                origins={"ai_planned"},
                areas={"self_improvement"},
                skills={"self-improve"},
                reward_decisions={"accept"},
            )

        self.assertEqual([row["ticket_id"] for row in result["rows"]], ["TASK-0003"])
        self.assertEqual(result["schema"], "farplane.ticket_history_query.v2")
        self.assertEqual(result["rows"][0]["area_derivation"], "planner_skill_call")
        self.assertEqual(result["rows"][0]["area_refs"], ["self_improvement"])
        self.assertEqual(result["rows"][0]["skill_ref"], "self-improve")
        self.assertEqual(result["rows"][0]["skill_derivation"], "planner_skill_call")
        self.assertEqual(result["skill_distribution"], {"self-improve": 1})
        self.assertNotIn("lane", result["rows"][0])
        self.assertNotIn("lane_distribution", result)

    def test_reserved_wave_materialization_preserves_origin_and_area(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            write_ticket(root, "TASK-0005", updated_at="2026-07-13T00:00:00Z", kpi_id="accepted_harness_improvements")
            decisions = root / ".farplane" / "automation" / "decisions.jsonl"
            decisions.parent.mkdir(parents=True)
            decisions.write_text(
                json.dumps(
                    {
                        "action": "materialize_reserved_wave",
                        "pulse_receipt": {
                            "admitted": ["TASK-0005"],
                            "admitted_specs": [
                                {
                                    "ticket_id": "TASK-0005",
                                    "area_id": "self_improvement",
                                    "ranking": {"lane": "rollout"},
                                }
                            ],
                        },
                    }
                ) + "\n",
                encoding="utf-8",
            )

            result = history.build_ticket_history(root, origins={"ai_planned"})

        self.assertEqual([row["ticket_id"] for row in result["rows"]], ["TASK-0005"])
        self.assertEqual(result["rows"][0]["area_refs"], ["self_improvement"])
        self.assertEqual(
            result["rows"][0]["area_derivation"], "historical_admitted_spec"
        )
        self.assertEqual(result["rows"][0]["skill_ref"], "unknown")
        self.assertEqual(result["rows"][0]["skill_derivation"], "unknown")

    def test_skill_filter_excludes_unknown_history(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            write_ticket(
                root,
                "TASK-0006",
                updated_at="2026-07-13T00:00:00Z",
                kpi_id="accepted_harness_improvements",
            )

            result = history.build_ticket_history(root, skills={"farplane-ablation-proof"})

        self.assertEqual(result["rows"], [])
        self.assertEqual(result["receipt"]["filtered_count"], 0)

    def test_reward_decision_filter_supports_monitor_and_pending(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            write_ticket(
                root,
                "TASK-0007",
                updated_at="2026-07-14T00:00:00Z",
                kpi_id="accepted_harness_improvements",
                decision="monitor",
            )
            write_ticket(
                root,
                "TASK-0008",
                updated_at="2026-07-13T00:00:00Z",
                kpi_id="accepted_harness_improvements",
            )

            result = history.build_ticket_history(
                root,
                reward_decisions={"monitor", "pending"},
            )

        self.assertEqual(
            [row["ticket_id"] for row in result["rows"]],
            ["TASK-0007", "TASK-0008"],
        )
        self.assertEqual(
            [row["rewards"][0]["decision"] for row in result["rows"]],
            ["monitor", "pending"],
        )

    def test_cli_summary_is_compact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            write_ticket(root, "TASK-0004", updated_at="2026-07-12T00:00:00Z", archived=False)
            args = argparse.Namespace(
                project_root=str(root), limit=20, sort="recent", origin=None,
                area=None, skill=None, status=None, kpi=None, reward_decision=None,
                active_only=False, json=False, all_results=False,
            )
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                exit_code = history.run_history(args)

        self.assertEqual(exit_code, 0)
        self.assertIn("1 returned / 1 matched / 1 scanned", output.getvalue())
        self.assertIn("TASK-0004", output.getvalue())

    def test_all_returns_every_match_with_exhaustion_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_root(tmp)
            for index in range(25):
                write_ticket(
                    root,
                    f"TASK-{index:04d}",
                    updated_at=f"2026-07-{(index % 20) + 1:02d}T00:00:00Z",
                    kpi_id="accepted_harness_improvements",
                )

            limited = history.build_ticket_history(
                root, limit=20, areas={"self_improvement"}
            )
            complete = history.build_ticket_history(
                root, limit=None, areas={"self_improvement"}
            )

        self.assertEqual(limited["receipt"]["returned_count"], 20)
        self.assertFalse(limited["receipt"]["exhausted"])
        self.assertEqual(complete["query"]["limit"], "all")
        self.assertEqual(complete["receipt"]["returned_count"], 25)
        self.assertTrue(complete["receipt"]["exhausted"])


if __name__ == "__main__":
    unittest.main()
