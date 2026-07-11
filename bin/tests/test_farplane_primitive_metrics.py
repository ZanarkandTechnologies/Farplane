from __future__ import annotations

import json
import sqlite3
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = ROOT / "bin" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from farplane_primitive_metrics import (
    backfill_ticket_thread_associations,
    fetch_codex_thread_usage,
    primitive_snapshot,
    window_for_date,
)


def write_ticket(root: Path, ticket_id: str, body: str) -> None:
    ticket_dir = root / "tickets" / ticket_id
    ticket_dir.mkdir(parents=True)
    (ticket_dir / "ticket.md").write_text(body, encoding="utf-8")


class FarplanePrimitiveMetricsTests(unittest.TestCase):
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

            payload = primitive_snapshot(
                root,
                "2026-07-03",
                root / ".codex",
                monthly_spend=None,
                write=False,
                ticket_status="rejected",
            )

        rejected_counts = payload["primitives"]["ticket_count_by_kpi_status:rejected"]
        self.assertEqual(rejected_counts["_total"]["value"], 1)
        self.assertEqual(rejected_counts["accepted_harness_improvements"]["value"], 1)
        self.assertEqual(
            rejected_counts["accepted_harness_improvements"]["payload"]["tickets"][0]["status"],
            "rejected",
        )
        realized = payload["primitives"]["ticket_count_by_kpi"]["accepted_harness_improvements"]["value"]
        self.assertEqual(realized, 1)

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
