#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_validate_qa_result import valid_result
from validate_eval_run import validate_answer


PROJECT_ROOT = Path(__file__).resolve().parents[3]
FIXTURE_ROOT = PROJECT_ROOT / "skills/qa/evals/fixtures"


def answer_with(payload: dict) -> str:
    return f"```json\n{json.dumps(payload)}\n```\nQA_RESULT: verdict={payload['verdict']} evidence=inline-result.json reason=fixture"


class ValidateEvalRunTest(unittest.TestCase):
    def test_accepts_valid_receipt_with_existing_artifact(self):
        with tempfile.TemporaryDirectory() as root:
            root_path = Path(root)
            artifact = root_path / "fixture.log"
            artifact.write_text("pass\n", encoding="utf-8")
            payload = valid_result(
                best_evidence="fixture.log",
                artifacts=["fixture.log"],
            )
            self.assertEqual(validate_answer(answer_with(payload), root_path), [])

    def test_rejects_schema_invalid_receipt(self):
        payload = valid_result(
            proof_type="api",
            runtime_target=None,
        )
        errors = validate_answer(answer_with(payload), PROJECT_ROOT)
        self.assertTrue(any("runtime_target" in error for error in errors))

    def test_rejects_nonexistent_artifact(self):
        payload = valid_result(
            best_evidence="skills/qa/evals/fixtures/missing.log",
            artifacts=["skills/qa/evals/fixtures/missing.log"],
        )
        errors = validate_answer(answer_with(payload), PROJECT_ROOT)
        self.assertTrue(any("does not exist" in error for error in errors))

    def test_requires_exactly_one_canonical_receipt(self):
        self.assertTrue(any("exactly one" in error for error in validate_answer("no json", PROJECT_ROOT)))

    def test_rejects_qa_result_that_points_to_best_evidence(self):
        with tempfile.TemporaryDirectory() as root:
            root_path = Path(root)
            (root_path / "fixture.log").write_text("pass\n", encoding="utf-8")
            payload = valid_result(best_evidence="fixture.log", artifacts=["fixture.log"])
            answer = answer_with(payload).replace("inline-result.json", "fixture.log")
            errors = validate_answer(answer, root_path)
            self.assertTrue(any("must name the result.json" in error for error in errors))

    def test_rejects_qa_result_verdict_that_contradicts_receipt(self):
        with tempfile.TemporaryDirectory() as root:
            root_path = Path(root)
            (root_path / "fixture.log").write_text("pass\n", encoding="utf-8")
            payload = valid_result(best_evidence="fixture.log", artifacts=["fixture.log"])
            answer = answer_with(payload).replace("verdict=pass", "verdict=blocked")
            errors = validate_answer(answer, root_path)
            self.assertTrue(any("does not match receipt verdict" in error for error in errors))

    def test_fixture_tickets_use_current_sections_and_link_existing_files(self):
        for ticket_id in ("TASK-0042", "TASK-0043", "TASK-0044", "TASK-0045", "TASK-0046"):
            ticket_path = FIXTURE_ROOT / ticket_id / "ticket.md"
            text = ticket_path.read_text(encoding="utf-8")
            self.assertIn("## Done\n", text)
            self.assertIn("## QA Strategy\n", text)
            self.assertNotIn("Done / Proof", text)
            for raw in re.findall(r"`([^`]+)`", text.split("## Links", 1)[1]):
                if raw.startswith("http"):
                    continue
                self.assertTrue((ticket_path.parent / raw).is_file(), raw)


if __name__ == "__main__":
    unittest.main()
