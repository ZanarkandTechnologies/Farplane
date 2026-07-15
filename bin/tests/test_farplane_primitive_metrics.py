from __future__ import annotations

import json
import os
import sqlite3
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = ROOT / "bin" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from farplane_primitive_metrics import (
    activated_external_projects,
    backfill_ticket_thread_associations,
    fetch_codex_thread_usage,
    primitive_snapshot,
    window_for_date,
)


def write_ticket(root: Path, ticket_id: str, body: str) -> None:
    ticket_dir = root / "tickets" / ticket_id
    ticket_dir.mkdir(parents=True)
    (ticket_dir / "ticket.md").write_text(body, encoding="utf-8")


def write_activation_manifest(root: Path, project_id: str, spec_version: str, template_version: str) -> Path:
    manifest_path = root / "farplane" / "manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(
            {
                "project_id": project_id,
                "spec_version": spec_version,
                "template_uses": {"farplane-framework": template_version},
            }
        ),
        encoding="utf-8",
    )
    return manifest_path


def write_pulse_decision(root: Path, timestamp: datetime) -> None:
    decisions = root / ".farplane" / "automation" / "decisions.jsonl"
    decisions.parent.mkdir(parents=True, exist_ok=True)
    decisions.write_text(
        json.dumps(
            {
                "ts": timestamp.isoformat(),
                "automation_id": "fixture-ticket-update",
                "lane": "pulse",
                "mode": "work_pulse",
                "action": "no_op",
            }
        )
        + "\n",
        encoding="utf-8",
    )


class FarplanePrimitiveMetricsTests(unittest.TestCase):
    def test_activated_external_projects_requires_current_manifest_and_post_migration_pulse(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            projects = Path(tmp) / "projects"
            root = projects / "Farplane"
            current = projects / "Current"
            inactive = projects / "Inactive"
            drifted = projects / "Drifted"
            for project in (root, current, inactive, drifted):
                (project / "farplane").mkdir(parents=True)
            standard = {
                "project_id": "Farplane",
                "spec_version": "2.0.0",
                "template_uses": {"farplane-framework": "2.0.0"},
            }
            (root / "farplane" / "manifest.json").write_text(json.dumps(standard), encoding="utf-8")
            (current / "farplane" / "manifest.json").write_text(
                json.dumps({**standard, "project_id": "Current"}), encoding="utf-8"
            )
            (inactive / "farplane" / "manifest.json").write_text(
                json.dumps({**standard, "project_id": "Inactive"}), encoding="utf-8"
            )
            (drifted / "farplane" / "manifest.json").write_text(
                json.dumps({**standard, "project_id": "Drifted", "spec_version": "1.0.0"}),
                encoding="utf-8",
            )
            decisions = current / ".farplane" / "automation" / "decisions.jsonl"
            decisions.parent.mkdir(parents=True)
            decisions.write_text(
                json.dumps(
                    {
                        "ts": (datetime.now(timezone.utc) + timedelta(seconds=5)).isoformat(),
                        "automation_id": "current-ticket-update",
                        "lane": "pulse",
                        "mode": "work_pulse",
                        "action": "no_op",
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            result = activated_external_projects(root)

        self.assertEqual(result["status"], "available")
        self.assertEqual(result["value"], 1)
        self.assertEqual(result["payload"]["projects"][0]["project_id"], "Current")
        excluded = {row["project_id"]: row for row in result["payload"]["excluded"]}
        self.assertIn("Drifted", excluded)
        self.assertEqual(
            excluded["Inactive"]["activation_gap"],
            "no_work_pulse_decision_after_manifest_update",
        )

    def test_activation_lifecycle_fixture_matrix_isolates_manifest_and_decision_conditions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            projects = Path(tmp) / "projects"
            root = projects / "Farplane"
            current = projects / "Current"
            stale_manifest = projects / "StaleManifest"
            missing_decision = projects / "MissingDecision"
            manifest_time = datetime(2026, 7, 14, 7, 30, tzinfo=timezone.utc).timestamp()

            for project, project_id, spec, template in (
                (root, "Farplane", "2.0.4", "2.0.4"),
                (current, "Current", "2.0.4", "2.0.4"),
                (stale_manifest, "StaleManifest", "2.0.3", "2.0.3"),
                (missing_decision, "MissingDecision", "2.0.4", "2.0.4"),
            ):
                manifest_path = write_activation_manifest(project, project_id, spec, template)
                os.utime(manifest_path, (manifest_time, manifest_time))

            write_pulse_decision(current, datetime.fromtimestamp(manifest_time, tz=timezone.utc) + timedelta(minutes=5))
            write_pulse_decision(
                stale_manifest,
                datetime.fromtimestamp(manifest_time, tz=timezone.utc) + timedelta(minutes=5),
            )

            result = activated_external_projects(root)

        self.assertEqual(result["status"], "available")
        self.assertEqual(result["value"], 1)
        self.assertEqual(result["payload"]["projects"][0]["project_id"], "Current")
        excluded = {row["project_id"]: row for row in result["payload"]["excluded"]}
        self.assertEqual(
            excluded["StaleManifest"]["drift"],
            [
                "spec_version:2.0.3!=2.0.4",
                "template:farplane-framework:2.0.3!=2.0.4",
            ],
        )
        self.assertNotIn("activation_gap", excluded["StaleManifest"])
        self.assertEqual(excluded["MissingDecision"]["drift"], [])
        self.assertEqual(
            excluded["MissingDecision"]["activation_gap"],
            "no_work_pulse_decision_after_manifest_update",
        )

    def test_kpi_counts_require_realized_accepted_ticket_rewards(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            write_ticket(
                root,
                "TASK-0001",
                """---
ticket_id: TASK-0001
phase: complete
status: done
created_at: 2026-07-03T01:00:00Z
updated_at: 2026-07-03T02:00:00Z
---

# TASK-0001

## Reward

```yaml
kpi_rewards:
  - reward_id: accepted-harness-7d
    kpi_id: accepted_harness_improvements
    expected_reward: one accepted improvement
    actual_result: improvement retained after review
    decision: accept
    evaluated_at: 2026-07-03T02:00:00Z
    evaluation_key: eval-accepted-harness-7d
    evidence_refs: [artifacts/proof.md]
```

## Done / Proof
- Evidence: artifacts/proof.md
- TAS-A verdict: pass
""",
            )
            write_ticket(
                root,
                "TASK-0002",
                """---
ticket_id: TASK-0002
phase: planning
status: review
created_at: 2026-07-03T03:00:00Z
updated_at: 2026-07-03T03:30:00Z
---

# TASK-0002

## Reward

```yaml
owner: human
```
""",
            )

            payload = primitive_snapshot(root, "2026-07-03", root / ".codex", monthly_spend=None, write=False)

        self.assertEqual(payload["primitives"]["ticket_count_by_kpi"]["accepted_harness_improvements"]["value"], 1)
        self.assertEqual(
            payload["primitives"]["ticket_count_by_kpi"]["accepted_harness_improvements"]["payload"]["reward_contract"],
            "terminal_evidence_v1",
        )
        self.assertNotIn("ticket_count_by_product", payload["primitives"])
        self.assertEqual(payload["primitives"]["tickets_with_kpi_reward_count"]["value"], 1)
        self.assertEqual(payload["primitives"]["kpi_attributed_ticket_ratio"]["value"], 0.5)
        self.assertNotIn("tickets/TASK-0002/ticket.md:missing_kpi_rewards", payload["source_gaps"])
        self.assertIn("tickets/TASK-0002/ticket.md:missing_kpi_rewards", payload["diagnostics"]["ticket_parse_gaps"])

    def test_rejected_ticket_status_counts_by_kpi_and_rejection_rate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            write_ticket(
                root,
                "TASK-0001",
                """---
ticket_id: TASK-0001
phase: failed
status: rejected
created_at: 2026-07-03T01:00:00Z
updated_at: 2026-07-03T02:00:00Z
---

# TASK-0001

## Reward

```yaml
kpi_rewards:
  - reward_id: rejected-harness-7d
    kpi_id: accepted_harness_improvements
    expected_reward: one accepted improvement
    actual_result: rejected by operator
    decision: kill
    evaluated_at: 2026-07-03T02:00:00Z
    evaluation_key: eval-rejected-harness-7d
    evidence_refs: [artifacts/rejection.md]
```

## Done / Proof
- Rejected by Kenji: boring premise.
""",
            )
            write_ticket(
                root,
                "TASK-0002",
                """---
ticket_id: TASK-0002
phase: complete
status: done
created_at: 2026-07-03T03:00:00Z
updated_at: 2026-07-03T04:00:00Z
---

# TASK-0002

## Reward

```yaml
kpi_rewards:
  - reward_id: accepted-harness-7d
    kpi_id: accepted_harness_improvements
    expected_reward: one accepted improvement
    actual_result: improvement retained after review
    decision: accept
    evaluated_at: 2026-07-03T04:00:00Z
    evaluation_key: eval-accepted-harness-7d
    evidence_refs: [artifacts/proof.md]
```

## Done / Proof
- Evidence: artifacts/proof.md
- TAS-A verdict: pass
""",
            )
            write_ticket(
                root,
                "TASK-0003",
                """---
ticket_id: TASK-0003
status: rejected
created_at: 2026-07-03T04:30:00Z
updated_at: 2026-07-03T05:00:00Z
---

## Reward

```yaml
kpi_rewards:
  - reward_id: direct-rejected
    kpi_id: accepted_harness_improvements
    expected_reward: direct request
    actual_result: rejected direct request
    decision: kill
    evaluated_at: 2026-07-03T05:00:00Z
    evaluation_key: direct-rejected
    evidence_refs: [artifacts/direct-rejection.md]
```
""",
            )
            decisions = root / ".farplane" / "automation" / "decisions.jsonl"
            decisions.parent.mkdir(parents=True)
            decisions.write_text(
                json.dumps(
                    {
                        "action": "plan_next_wave",
                        "pulse_receipt": {"admitted": ["TASK-0001"]},
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            payload = primitive_snapshot(
                root,
                "2026-07-03",
                root / ".codex",
                monthly_spend=None,
                write=False,
                ticket_status="rejected",
            )

        rejected_counts = payload["primitives"]["ticket_count_by_kpi_status:rejected"]
        self.assertEqual(rejected_counts["_total"]["value"], 2)
        self.assertEqual(rejected_counts["accepted_harness_improvements"]["value"], 2)
        self.assertEqual(
            rejected_counts["accepted_harness_improvements"]["payload"]["tickets"][0]["status"],
            "rejected",
        )
        realized = payload["primitives"]["ticket_count_by_kpi"]["accepted_harness_improvements"]["value"]
        self.assertEqual(realized, 1)
        planner_rejections = payload["primitives"]["planner_ticket_quality"][
            "rejected_ai_ticket_count"
        ]
        self.assertEqual(planner_rejections["value"], 1)
        self.assertEqual(
            planner_rejections["payload"]["origin_filter"],
            "pulse_plan_next_wave_admitted",
        )

    def test_empty_windows_are_zero_readings_not_source_gaps(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            (root / "farplane" / "bindings.yaml").write_text(
                """kind: project-bindings
spend_model:
  monthly_ai_spend: 62
""",
                encoding="utf-8",
            )
            write_ticket(
                root,
                "TASK-0001",
                """---
ticket_id: TASK-0001
phase: complete
status: done
created_at: 2026-07-01T01:00:00Z
updated_at: 2026-07-01T02:00:00Z
completed_at: 2026-07-01T02:00:00Z
---

# TASK-0001

## Reward

```yaml
kpi_rewards:
  - reward_id: accepted-harness-old
    kpi_id: accepted_harness_improvements
    expected_reward: one accepted improvement
    actual_result: improvement retained
    decision: accept
    evaluated_at: 2026-07-01T02:00:00Z
    evaluation_key: eval-accepted-harness-old
    evidence_refs: [artifacts/proof.md]
```
""",
            )

            payload = primitive_snapshot(root, "2026-07-03", root / ".codex", monthly_spend=None, write=False)

        self.assertEqual(payload["primitives"]["kpi_attributed_ticket_ratio"]["status"], "available")
        self.assertEqual(payload["primitives"]["kpi_attributed_ticket_ratio"]["value"], 0)
        self.assertEqual(payload["primitives"]["ticket_thread_link_coverage"]["status"], "available")
        self.assertEqual(payload["primitives"]["ticket_thread_link_coverage"]["value"], 0)
        self.assertEqual(payload["primitives"]["ai_burn_estimate"]["status"], "available")
        self.assertEqual(payload["primitives"]["ai_burn_estimate"]["payload"]["monthly_spend"], 62.0)
        self.assertNotIn("no_completed_tickets_in_window", payload["source_gaps"])
        self.assertNotIn("missing_spend_model", payload["source_gaps"])

    def test_score_only_and_inconsistent_lifecycle_rows_are_not_realized(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            write_ticket(
                root,
                "TASK-SCORE-ONLY",
                """---
ticket_id: TASK-SCORE-ONLY
status: done
created_at: 2026-07-03T01:00:00Z
updated_at: 2026-07-03T02:00:00Z
---

## Reward

```yaml
kpi_rewards:
  - reward_id: score-only
    kpi_id: accepted_harness_improvements
    expected_reward: declared only
    reward_score: 1
    reward_score_reason: legacy positive
```

## Done / Proof
- TAS-A verdict: pass
""",
            )
            write_ticket(
                root,
                "TASK-PHASE-MISMATCH",
                """---
ticket_id: TASK-PHASE-MISMATCH
status: done
phase: planning
created_at: 2026-07-03T01:00:00Z
updated_at: 2026-07-03T02:00:00Z
---

## Reward

```yaml
kpi_rewards:
  - reward_id: phase-mismatch
    kpi_id: accepted_harness_improvements
    expected_reward: should not aggregate
    actual_result: result
    decision: accept
    evaluated_at: 2026-07-03T02:00:00Z
    evaluation_key: eval-phase-mismatch
    evidence_refs: [artifacts/proof.md]
```

## Done / Proof
- TAS-A verdict: pass
""",
            )

            payload = primitive_snapshot(
                root, "2026-07-03", root / ".codex", monthly_spend=None, write=False
            )

        unrealized = payload["primitives"]["ticket_count_by_kpi"][
            "accepted_harness_improvements"
        ]
        self.assertEqual(unrealized["value"], 0)
        self.assertEqual(unrealized["status"], "source_gap")
        self.assertEqual(len(unrealized["payload"]["gaps"]), 2)

    def test_mine_backfill_writes_completion_only_association_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mine_run = root / ".farplane" / "mine" / "runs" / "mine-a"
            mine_run.mkdir(parents=True)
            (mine_run / "input.json").write_text(
                json.dumps(
                    {
                        "sourceEventKey": "farplane-file-event:abc:tickets/TASK-0001/ticket.md:hash",
                        "sources": [
                            {
                                "ticketId": "TASK-0001",
                                "inputRef": "tickets/TASK-0001/ticket.md",
                                "sessionId": "thread-a",
                                "threadId": "thread-a",
                                "updatedAt": 1783020000,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            output = root / ".farplane" / "state" / "ticket-thread-associations.jsonl"

            result = backfill_ticket_thread_associations(root, root / ".farplane" / "mine" / "runs", output)
            rows = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]

        self.assertEqual(result["status"], "available")
        self.assertEqual(rows[0]["confidence"], "completion_only")
        self.assertNotIn("execution_started_at", rows[0])

    def test_existing_association_log_covers_archived_completed_ticket(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            ticket_dir = root / "tickets" / "archive" / "TASK-0001"
            ticket_dir.mkdir(parents=True)
            (ticket_dir / "ticket.md").write_text(
                """---
ticket_id: TASK-0001
phase: complete
status: done
created_at: 2026-07-03T01:00:00Z
updated_at: 2026-07-03T03:00:00Z
completed_at: 2026-07-03T03:00:00Z
---

# TASK-0001

## Done / Proof
- Evidence: artifacts/proof.md
""",
                encoding="utf-8",
            )
            state = root / ".farplane" / "state"
            state.mkdir(parents=True)
            (state / "ticket-thread-associations.jsonl").write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-0001",
                        "thread_id": "thread-outcome",
                        "source": "ticket_thread_association",
                        "source_event_key": "test:TASK-0001:thread-outcome",
                        "observed_at": "2026-07-03T03:10:00Z",
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            payload = primitive_snapshot(root, "2026-07-03", root / ".codex", monthly_spend=31, write=True)
            association_rows = [
                json.loads(line)
                for line in (root / ".farplane" / "state" / "ticket-thread-associations.jsonl")
                .read_text(encoding="utf-8")
                .splitlines()
            ]

        coverage = payload["primitives"]["ticket_thread_link_coverage"]
        self.assertEqual(coverage["payload"]["completed_tickets"], 1)
        self.assertEqual(coverage["payload"]["associated_completed_tickets"], 1)
        self.assertEqual(coverage["value"], 1.0)
        self.assertEqual({row["ticket_id"] for row in association_rows}, {"TASK-0001"})

    def test_codex_thread_usage_reads_sqlite_and_session_token_counts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            root.mkdir()
            codex_home = Path(tmp) / ".codex"
            sqlite_dir = codex_home / "sqlite"
            sqlite_dir.mkdir(parents=True)
            db = sqlite_dir / "state_5.sqlite"
            con = sqlite3.connect(db)
            con.execute(
                """create table threads (
                id text, rollout_path text, created_at integer, updated_at integer,
                source text, model_provider text, cwd text, title text,
                sandbox_policy text, approval_mode text, tokens_used integer,
                has_user_event integer, archived integer, archived_at integer,
                git_sha text, git_branch text, git_origin_url text, cli_version text,
                first_user_message text, agent_nickname text, agent_role text,
                memory_mode text, model text, reasoning_effort text, agent_path text,
                created_at_ms integer, updated_at_ms integer, thread_source text,
                preview text
                )"""
            )
            con.execute("create table thread_spawn_edges (parent_thread_id text, child_thread_id text, status text)")
            start_ms = int(datetime(2026, 7, 3, 1, tzinfo=timezone.utc).timestamp() * 1000)
            con.execute(
                "insert into threads values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    "thread-a",
                    None,
                    None,
                    None,
                    "codex",
                    "openai",
                    str(root.resolve()),
                    "Test",
                    None,
                    None,
                    99,
                    1,
                    0,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    "gpt",
                    None,
                    None,
                    start_ms,
                    start_ms + 60000,
                    "codex",
                    None,
                ),
            )
            con.commit()
            con.close()
            session_dir = codex_home / "sessions" / "2026" / "07" / "03"
            session_dir.mkdir(parents=True)
            (session_dir / "session.jsonl").write_text(
                "\n".join(
                    [
                        json.dumps({"type": "session_meta", "timestamp": "2026-07-03T01:00:00Z", "payload": {"id": "thread-a", "cwd": str(root.resolve())}}),
                        json.dumps({"type": "event_msg", "timestamp": "2026-07-03T01:00:01Z", "payload": {"type": "task_started"}}),
                        json.dumps(
                            {
                                "type": "event_msg",
                                "timestamp": "2026-07-03T01:00:02Z",
                                "payload": {
                                    "type": "token_count",
                                    "info": {
                                        "last_token_usage": {
                                            "input_tokens": 3,
                                            "cached_input_tokens": 2,
                                            "output_tokens": 4,
                                            "reasoning_output_tokens": 1,
                                            "total_tokens": 10,
                                        }
                                    },
                                },
                            }
                        ),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            result = fetch_codex_thread_usage(codex_home, root, window_for_date("2026-07-03"))

        self.assertEqual(result["status"], "available")
        self.assertEqual(result["payload"]["thread_count"], 1)
        self.assertEqual(result["payload"]["turn_count"], 1)
        self.assertEqual(result["payload"]["tokens"]["total"], 10)


if __name__ == "__main__":
    unittest.main()
