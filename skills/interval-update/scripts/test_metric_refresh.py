from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

_PATH = Path(__file__).with_name("metric_refresh.py")
_SPEC = importlib.util.spec_from_file_location("farplane_interval_metric_refresh", _PATH)
assert _SPEC is not None and _SPEC.loader is not None
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)
count_ticket_kpi_rewards = _MODULE.count_ticket_kpi_rewards
resolve_refresh_plan = _MODULE.resolve_refresh_plan
calculate_autonomy_savings = _MODULE.calculate_autonomy_savings
record_refresh_result = _MODULE.record_refresh_result
resolve_interval_refresh_plan = _MODULE.resolve_interval_refresh_plan


class RefreshPlanTests(unittest.TestCase):
    def test_group_is_executed_once_for_flat_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            metrics = Path(temp_dir) / "metrics.yaml"
            metrics.write_text("refreshers:\n  instagram:\n    refresh: Call Instagram for <YYYY-MM-DD>.\n    provides: [views, likes]\nmetrics:\n  views: {refresh_ref: instagram}\n  likes: {refresh_ref: instagram}\n", encoding="utf-8")
            result = resolve_refresh_plan(metrics, ["views", "likes"], "2026-07-12")
        self.assertEqual(len(result["refresh_groups"]), 1)
        self.assertEqual(result["refresh_groups"][0]["requested_metric_ids"], ["views", "likes"])

    def test_fresh_metrics_skip_and_missing_owner_gaps(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            metrics = Path(temp_dir) / "metrics.yaml"
            metrics.write_text("refreshers:\n  local:\n    refresh: Run local.\n    provides: [fresh]\nmetrics:\n  fresh: {refresh_ref: local}\n  missing: {}\n", encoding="utf-8")
            result = resolve_refresh_plan(metrics, ["fresh", "missing"], "2026-07-12", {"fresh"})
        self.assertEqual(result["refresh_groups"], [])
        self.assertEqual(result["skipped_metric_ids"], ["fresh"])
        self.assertEqual(result["source_gaps"], ["invalid_refresh_owner:missing"])

    def test_autonomy_savings_requires_terminal_tas_a_and_reports_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            ticket = root / "tickets" / "archive" / "TASK-0001" / "ticket.md"
            ticket.parent.mkdir(parents=True)
            ticket.write_text("---\nticket_id: TASK-0001\nstatus: done\ncompleted_at: 2026-07-12T12:00:00Z\n---\n\n## Done / Proof\nProof passed; TAS-A verdict pass.\n", encoding="utf-8")
            review = ticket.parent / "artifacts" / "review" / "completion.md"
            review.parent.mkdir(parents=True)
            review.write_text("verdict: pass\noverall_tas: TAS-A\n", encoding="utf-8")
            state = root / ".farplane" / "state"
            state.mkdir(parents=True)
            (state / "ticket-thread-associations.jsonl").write_text('{"ticket_id":"TASK-0001","thread_id":"thread-1","execution_started_at":"2026-07-12T10:00:00Z"}\n', encoding="utf-8")
            result = calculate_autonomy_savings(root / "tickets", root / ".farplane", "2026-07-12", 10, 20)
        self.assertEqual(result["payload"]["accepted_clone_hours"], 2.0)
        self.assertEqual(result["payload"]["nonaccepted_clone_hours"], 0.0)
        self.assertEqual(result["payload"]["attribution_coverage"], 1.0)
        self.assertEqual(result["payload"]["baseline_provenance"]["reasonable_hours_per_day"], 10)

    def test_group_result_writes_partial_flat_observations(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            job = {"refresh_id": "instagram", "requested_metric_ids": ["views", "likes", "shares"]}
            receipt = record_refresh_result(root, "2026-07-12", job, {"views": {"value": 10, "status": "available", "payload": {}}, "likes": {"value": 2, "status": "available", "payload": {}}})
            payload = __import__("json").loads(Path(receipt["path"]).read_text(encoding="utf-8"))
        self.assertEqual(receipt["observation_metric_ids"], ["views", "likes", "shares"])
        self.assertEqual(receipt["source_gaps"], ["missing_refresh_output:shares"])
        self.assertEqual([row["metric_id"] for row in payload["observations"]], ["views", "likes", "shares"])
        self.assertEqual(payload["observations"][-1]["status"], "source_gap")
        self.assertEqual(payload["status"], "partial")

    def test_disabled_daily_and_weekly_resolve_zero_jobs(self) -> None:
        self.assertEqual(resolve_interval_refresh_plan("daily", False, Path("unused"), [], "2026-07-12")["reason"], "refresh_disabled")
        self.assertEqual(resolve_interval_refresh_plan("weekly", True, Path("unused"), [], "2026-07-12")["reason"], "weekly_read_only")


class AcceptedRewardMetricTests(unittest.TestCase):
    def write_ticket(
        self,
        root: Path,
        *,
        with_review: bool,
        decision: str = "accept",
        actual_result: str = "accepted proof remained",
        evaluated_at: str = "2026-07-12T00:00:00Z",
        evidence_refs: str = "[artifacts/proof.md]",
        status: str = "done",
        phase: str = "",
        legacy_score: str = "",
    ) -> Path:
        ticket = root / "tickets" / "archive" / "TASK-0001" / "ticket.md"
        ticket.parent.mkdir(parents=True)
        ticket.write_text(
            """---
ticket_id: TASK-0001
status: {status}
phase: {phase}
updated_at: 2026-07-12T00:00:00Z
---

## Reward

```yaml
kpi_rewards:
  - reward_id: accepted-evidence-7d
    kpi_id: accepted_evidence_cycles
    expected_reward: accepted proof
    actual_result: {actual_result}
    decision: {decision}
    evaluated_at: {evaluated_at}
    evaluation_key: eval-1
    supersedes_evaluation_key:
    evidence_refs: {evidence_refs}
{legacy_score}
```

## Done / Proof

Implementation proof exists.
""".format(
                status=status,
                phase=phase,
                actual_result=actual_result,
                decision=decision,
                evaluated_at=evaluated_at,
                evidence_refs=evidence_refs,
                legacy_score=legacy_score,
            ),
            encoding="utf-8",
        )
        if with_review:
            review = ticket.parent / "artifacts" / "review" / "result.md"
            review.parent.mkdir(parents=True)
            review.write_text("overall_tas: TAS-A\nverdict: pass\n", encoding="utf-8")
        return ticket

    def test_accepted_metric_requires_ticket_scoped_pass_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_ticket(root, with_review=False)
            result = count_ticket_kpi_rewards(root / "tickets", "2026-07-12", "accepted_evidence_cycles")
        self.assertEqual(result["value"], 0)
        self.assertEqual(result["status"], "source_gap")
        self.assertTrue(any("missing_acceptance_evidence" in gap for gap in result["payload"]["gaps"]))

    def test_accepted_metric_counts_tas_a_pass_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_ticket(root, with_review=True)
            result = count_ticket_kpi_rewards(root / "tickets", "2026-07-12", "accepted_evidence_cycles")
        self.assertEqual(result["value"], 1)

    def test_declared_monitor_kill_and_score_only_rows_do_not_count(self) -> None:
        cases = [
            ({"decision": "", "actual_result": ""}, "source_gap"),
            ({"decision": "monitor"}, "source_gap"),
            ({"decision": "kill"}, "available"),
            ({"decision": "accept", "actual_result": ""}, "source_gap"),
            ({"decision": "accept", "evaluated_at": ""}, "source_gap"),
            ({"decision": "accept", "evidence_refs": "[]"}, "source_gap"),
            (
                {
                    "decision": "",
                    "legacy_score": "    reward_score: 1\n    reward_score_reason: legacy positive",
                },
                "source_gap",
            ),
        ]
        for index, (case, expected_status) in enumerate(cases):
            with self.subTest(index=index), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.write_ticket(root, with_review=True, **case)
                result = count_ticket_kpi_rewards(
                    root / "tickets", "2026-07-12", "accepted_evidence_cycles"
                )
                self.assertEqual(result["value"], 0)
                self.assertEqual(result["status"], expected_status)

    def test_status_and_phase_must_both_allow_realized_aggregation(self) -> None:
        for status, phase in (("rejected", "complete"), ("done", "planning")):
            with self.subTest(status=status, phase=phase), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.write_ticket(
                    root,
                    with_review=True,
                    status=status,
                    phase=phase,
                )
                result = count_ticket_kpi_rewards(
                    root / "tickets", "2026-07-12", "accepted_evidence_cycles"
                )
                self.assertEqual(result["value"], 0)


if __name__ == "__main__":
    unittest.main()
