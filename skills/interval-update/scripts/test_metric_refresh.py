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
