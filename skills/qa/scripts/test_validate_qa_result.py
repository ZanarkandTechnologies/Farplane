#!/usr/bin/env python3

from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_qa_result import validate


def valid_result(**overrides):
    payload = {
        "schema_version": "1",
        "ticket_id": "ZanarkandTechnologies/Farplane#41",
        "phase": "qa",
        "proof_type": "cli",
        "runtime_target": None,
        "proof_policy": "Done + QA Strategy",
        "verdict": "pass",
        "summary": "Focused checks passed.",
        "gate_results": {
            "contract": "pass",
            "mechanism": "pass",
            "journey": "pass",
            "adversarial": "pass",
            "receipt": "pass",
        },
        "best_evidence": ".farplane/qa/41/run/checks.txt",
        "artifacts": [
            ".farplane/qa/41/run/report.md",
            ".farplane/qa/41/run/checks.txt",
        ],
        "blockers": [],
        "residual_risk": [],
        "judgment_receipts": [],
        "learning": {"outcome": "ticket_only", "ref": None},
    }
    payload.update(overrides)
    return payload


class ValidateQaResultTest(unittest.TestCase):
    def test_cli_pass_accepts_non_image_evidence(self):
        self.assertEqual(validate(valid_result()), [])

    def test_ui_pass_requires_runtime_and_image(self):
        payload = valid_result(proof_type="ui", runtime_target=None)
        errors = validate(payload)
        self.assertTrue(any("runtime_target" in error for error in errors))
        self.assertTrue(any("image path" in error for error in errors))

        image = ".farplane/qa/41/run/screens/final.png"
        payload["runtime_target"] = "http://127.0.0.1:3000"
        payload["best_evidence"] = image
        payload["artifacts"].append(image)
        self.assertEqual(validate(payload), [])

    def test_api_requires_runtime(self):
        errors = validate(valid_result(proof_type="api"))
        self.assertTrue(any("required for api" in error for error in errors))

    def test_pass_rejects_failed_gate_or_blocker(self):
        failed_gate = valid_result()
        failed_gate["gate_results"]["journey"] = "fail"
        self.assertTrue(any("every gate" in error for error in validate(failed_gate)))
        self.assertTrue(any("cannot contain blockers" in error for error in validate(valid_result(blockers=["gap"]))))

    def test_non_pass_requires_blocker(self):
        self.assertTrue(any("requires at least one blocker" in error for error in validate(valid_result(verdict="blocked"))))
        payload = valid_result(verdict="not_provable", blockers=["Missing runtime observation."])
        payload["gate_results"]["journey"] = "blocked"
        self.assertEqual(validate(payload), [])

    def test_ui_non_pass_may_record_missing_best_evidence_as_null(self):
        payload = valid_result(
            proof_type="ui",
            runtime_target="http://127.0.0.1:3000",
            verdict="revise",
            best_evidence=None,
            blockers=["Missing required screenshot evidence."],
        )
        payload["gate_results"]["journey"] = "blocked"
        self.assertEqual(validate(payload), [])

    def test_pass_requires_concrete_best_evidence(self):
        errors = validate(valid_result(best_evidence=None))
        self.assertTrue(any("passing result requires" in error for error in errors))

    def test_pass_requires_named_judgment_receipts_from_policy(self):
        payload = valid_result(
            proof_policy="Done + QA Strategy + visual + adversarial + reviewer"
        )
        errors = validate(payload)
        self.assertTrue(any("visual receipt" in error for error in errors))
        self.assertTrue(any("adversarial receipt" in error for error in errors))
        self.assertTrue(any("reviewer receipt" in error for error in errors))

        payload["judgment_receipts"] = [
            ".farplane/qa/41/run/visual.md",
            ".farplane/qa/41/run/adversarial/review.json",
            ".farplane/review/41/completion-review.md",
        ]
        self.assertEqual(validate(payload), [])

    def test_non_pass_may_block_on_missing_required_judgment(self):
        payload = valid_result(
            verdict="blocked",
            proof_policy="Done + QA Strategy + visual",
            blockers=["Required visual judgment has not run."],
        )
        payload["gate_results"]["adversarial"] = "blocked"
        self.assertEqual(validate(payload), [])

    def test_ticket_id_accepts_issue_refs_and_legacy_ids(self):
        for ticket_id in ("ZanarkandTechnologies/Farplane#41", "#41", "TASK-0356"):
            self.assertEqual(validate(valid_result(ticket_id=ticket_id)), [])
        self.assertTrue(any("ticket_id" in error for error in validate(valid_result(ticket_id="41"))))

    def test_best_evidence_must_be_an_artifact(self):
        errors = validate(valid_result(best_evidence="elsewhere.txt"))
        self.assertTrue(any("must also appear" in error for error in errors))

    def test_learning_reference_rules(self):
        self.assertTrue(any("requires a non-empty reference" in error for error in validate(valid_result(learning={"outcome": "cookbook_update", "ref": None}))))
        payload = valid_result(learning={"outcome": "cookbook_update", "ref": "docs/qa/checkout.md"})
        self.assertEqual(validate(payload), [])
        self.assertTrue(any("requires null" in error for error in validate(valid_result(learning={"outcome": "ticket_only", "ref": "report.md"}))))

    def test_rejects_missing_and_unknown_fields(self):
        missing = valid_result()
        missing.pop("proof_policy")
        self.assertTrue(any("missing fields" in error for error in validate(missing)))
        extra = valid_result(extra_field=True)
        self.assertTrue(any("unknown fields" in error for error in validate(extra)))

    def test_validation_does_not_mutate_payload(self):
        payload = valid_result()
        before = copy.deepcopy(payload)
        validate(payload)
        self.assertEqual(payload, before)


if __name__ == "__main__":
    unittest.main()
