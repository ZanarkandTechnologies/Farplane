#!/usr/bin/env python3
"""Contract checks for Plan Next Wave eval fixtures."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
WORLD_MEMORY_VALIDATOR = ROOT / "skills" / "feed-scout" / "scripts" / "validate_world_memory.py"
MEMORY_FIXTURE = ROOT / "skills" / "plan-next-wave" / "evals" / "fixtures" / "icp-world-memory.md"
WAVE_FIXTURE = ROOT / "skills" / "plan-next-wave" / "evals" / "fixtures" / "skill-call-wave.json"
HARNESS = ROOT / "farplane" / "harness.yaml"
GOLDEN = ROOT / "skills" / "plan-next-wave" / "examples" / "golden" / "compelling-proposal.md"
SKILL = ROOT / "skills" / "plan-next-wave" / "SKILL.md"
EVALS = ROOT / "skills" / "plan-next-wave" / "evals" / "evals.json"


def load_memory_validator():
    spec = importlib.util.spec_from_file_location("memory_validator", WORLD_MEMORY_VALIDATOR)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class EvalFixtureContractTest(unittest.TestCase):
    def test_world_memory_fixture_passes(self) -> None:
        validator = load_memory_validator()
        self.assertEqual([], validator.validate_world_memory(MEMORY_FIXTURE, harness_path=HARNESS))

    def test_golden_is_a_skill_call_not_a_workflow(self) -> None:
        text = GOLDEN.read_text(encoding="utf-8")
        for value in ("skill_ref: farplane-content-creation", "problem_ref:", "system_ref:", "feature_refs:", "expected_artifact:", "## Transferable invariants"):
            self.assertIn(value, text)
        self.assertNotIn("proposal_type:", text)
        self.assertNotIn("lane:", text)

    def test_fixture_stores_call_once(self) -> None:
        payload = json.loads(WAVE_FIXTURE.read_text(encoding="utf-8"))
        call = payload["proposed_skill_calls"][0]
        self.assertEqual([call["call_id"]], payload["decision"]["admitted_call_ids"])
        self.assertNotIn("admitted_specs", payload["decision"])
        self.assertNotIn("idea_cards", payload)
        self.assertNotIn("lane_receipts", payload)

    def test_skill_eval_suite_covers_configured_calls_and_content(self) -> None:
        payload = json.loads(EVALS.read_text(encoding="utf-8"))
        ids = {row["id"] for row in payload["evals"]}
        self.assertIn("planner_selects_only_configured_skills", ids)
        self.assertIn("planner_content_call_uses_one_transformation_ticket", ids)
        self.assertIn("references/skill-call-contract.md", SKILL.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
