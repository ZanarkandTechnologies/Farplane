from __future__ import annotations

import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import runner


class RunnerExpectationTests(unittest.TestCase):
    def test_accept_case_requires_all_fixture_and_gate_assertions_to_pass(self) -> None:
        case = {"id": "good", "expected_outcome": "accept"}
        assertions = [
            {"name": "candidate_output_present", "passed": True},
            {"name": "gate", "passed": True},
        ]
        self.assertTrue(runner.score_case(case, assertions)["expectation_passed"])

    def test_reject_case_passes_when_fixture_is_present_and_gate_fails(self) -> None:
        case = {"id": "bad", "expected_outcome": "reject"}
        assertions = [
            {"name": "candidate_output_present", "passed": True},
            {"name": "quality_gate", "passed": False},
        ]
        score = runner.score_case(case, assertions)
        self.assertTrue(score["expectation_passed"])
        self.assertTrue(score["rejected_by_gate"])

    def test_reject_case_does_not_pass_when_only_fixture_assertion_fails(self) -> None:
        case = {"id": "missing", "expected_outcome": "reject"}
        assertions = [
            {"name": "candidate_output_present", "passed": False},
            {"name": "quality_gate", "passed": True},
        ]
        self.assertFalse(runner.score_case(case, assertions)["expectation_passed"])


if __name__ == "__main__":
    unittest.main()
