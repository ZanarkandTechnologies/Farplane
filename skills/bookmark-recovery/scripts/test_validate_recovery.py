from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("validate_recovery.py")
SPEC = importlib.util.spec_from_file_location("validate_recovery", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ValidateRecoveryTests(unittest.TestCase):
    POLICY = {
        "run_id": "run-1",
        "generated_at": "2026-09-22T23:00:00+08:00",
        "candidate_limit": 20,
        "project_match_limit": 3,
        "sources": {"x", "instagram"},
        "source_refs": {"x": {"./x.json#item-123"}, "instagram": set()},
        "projects": {
            "project-1": {
                "project_name": "Farplane",
                "evidence_refs": {"./project-memory.md#constraint"},
            }
        },
    }

    def test_documented_example_accepts_mixed_coverage_and_hypothesis(self) -> None:
        payload = {
            "schema_version": 2,
            "run_id": "run-1",
            "generated_at": "2026-09-22T23:00:00+08:00",
            "candidate_limit": 20,
            "project_match_limit": 3,
            "coverage": [
                {"source": "x", "status": "complete", "item_count": 1, "limitation": None},
                {"source": "instagram", "status": "blocked", "item_count": 0, "limitation": "no adapter"},
            ],
            "candidates": [{
                "canonical_key": "x:123", "source": "x", "source_id": "123",
                "url": "https://x.com/example/status/123", "priority": "medium",
                "route": "intelligest_candidate",
                "possible_use": {"kind": "ai_hypothesis", "text": "reference", "confidence": "low"},
                "evidence_refs": ["./x.json#item-123"],
            }],
            "project_matches": [{
                "canonical_key": "x:123", "project_id": "project-1", "project_name": "Farplane",
                "relation": "addresses_constraint",
                "reason": {"kind": "ai_hypothesis", "text": "May help", "confidence": "medium"},
                "evidence_refs": ["./x.json#item-123", "./project-memory.md#constraint"],
            }],
            "duplicates": [], "excluded": [], "limitations": ["instagram blocked"],
        }
        self.assertEqual(MODULE.validate(payload, self.POLICY), [])

    def test_rejects_duplicate_keys_and_unattributed_possible_use(self) -> None:
        payload = {
            "schema_version": 2, "run_id": "r", "generated_at": "t",
            "candidate_limit": 1,
            "project_match_limit": 3,
            "coverage": [{"source": "x", "status": "complete"}],
            "candidates": [
                {"canonical_key": "x:1", "source": "x", "priority": "high", "route": "dismiss", "evidence_refs": ["a"]},
                {"canonical_key": "x:1", "source": "x", "priority": "high", "route": "dismiss", "possible_use": {"text": "idea"}, "evidence_refs": ["b"]},
            ],
            "project_matches": [], "duplicates": [], "excluded": [], "limitations": [],
        }
        policy = {"run_id": "r", "generated_at": "t", "candidate_limit": 1,
                  "project_match_limit": 3, "sources": {"x"},
                  "source_refs": {"x": {"a", "b"}}, "projects": {}}
        errors = MODULE.validate(payload, policy)
        self.assertTrue(any("duplicate candidate" in error for error in errors))
        self.assertTrue(any("ai_hypothesis" in error for error in errors))

    def test_rejects_cross_disposition_duplicate_and_count_mismatch(self) -> None:
        payload = {
            "schema_version": 2, "run_id": "r", "generated_at": "t", "candidate_limit": 20,
            "project_match_limit": 3,
            "coverage": [{"source": "x", "status": "complete", "item_count": 999}],
            "candidates": [{
                "canonical_key": "x:1", "source": "x", "priority": "high",
                "route": "intelligest_candidate", "evidence_refs": ["a"],
            }],
            "duplicates": [{"canonical_key": "x:1", "source": "x", "reason": "seen"}],
            "project_matches": [], "excluded": [], "limitations": [],
        }
        policy = {"run_id": "r", "generated_at": "t", "candidate_limit": 20,
                  "project_match_limit": 3, "sources": {"x"},
                  "source_refs": {"x": {"a"}}, "projects": {}}
        errors = MODULE.validate(payload, policy)
        self.assertTrue(any("multiple dispositions" in error for error in errors))
        self.assertTrue(any("does not reconcile" in error for error in errors))

    def test_rejects_unbounded_or_unattributed_project_matches(self) -> None:
        payload = {
            "schema_version": 2, "run_id": "r", "generated_at": "t", "candidate_limit": 20,
            "project_match_limit": 1,
            "coverage": [{"source": "x", "status": "complete", "item_count": 1}],
            "candidates": [{
                "canonical_key": "x:1", "source": "x", "priority": "high",
                "route": "intelligest_candidate", "evidence_refs": ["source"],
            }],
            "project_matches": [
                {"canonical_key": "x:1", "project_id": "p1", "project_name": "One",
                 "relation": "addresses_constraint", "reason": {"kind": "fact", "confidence": "high"},
                 "evidence_refs": ["source"]},
                {"canonical_key": "x:1", "project_id": "p2", "project_name": "Two",
                 "relation": "project_opportunity",
                 "reason": {"kind": "ai_hypothesis", "text": "Maybe", "confidence": "low"},
                 "evidence_refs": ["source", "memory"]},
            ],
            "duplicates": [], "excluded": [], "limitations": [],
        }
        policy = {
            "run_id": "r", "generated_at": "t", "candidate_limit": 20,
            "project_match_limit": 1, "sources": {"x"}, "source_refs": {"x": {"source"}},
            "projects": {
                "p1": {"project_name": "One", "evidence_refs": {"memory"}},
                "p2": {"project_name": "Two", "evidence_refs": {"memory"}},
            },
        }
        errors = MODULE.validate(payload, policy)
        self.assertTrue(any("reason must be an ai_hypothesis" in error for error in errors))
        self.assertTrue(any("must cite source and Project Memory" in error for error in errors))
        self.assertTrue(any("exceeds project_match_limit" in error for error in errors))

    def test_rejects_invented_source_project_and_evidence(self) -> None:
        payload = {
            "schema_version": 2, "run_id": "r", "generated_at": "t", "candidate_limit": 20,
            "project_match_limit": 3,
            "coverage": [{"source": "invented", "status": "complete", "item_count": 1}],
            "candidates": [{
                "canonical_key": "invented:1", "source": "invented", "priority": "high",
                "route": "intelligest_candidate", "evidence_refs": ["fake.json#item"],
            }],
            "project_matches": [{
                "canonical_key": "invented:1", "project_id": "made-up", "project_name": "Fake",
                "relation": "project_opportunity",
                "reason": {"kind": "ai_hypothesis", "text": "Maybe", "confidence": "low"},
                "evidence_refs": ["fake.json#item", "fake-memory.json#constraint"],
            }],
            "duplicates": [], "excluded": [], "limitations": [],
        }
        errors = MODULE.validate(payload, self.POLICY)
        self.assertTrue(any("coverage sources" in error for error in errors))
        self.assertTrue(any("frozen source cache" in error for error in errors))
        self.assertTrue(any("not eligible" in error for error in errors))
        self.assertTrue(any("candidate and Project Memory" in error for error in errors))

    def _person_payload(self, match: dict) -> dict:
        return {
            "schema_version": 2, "run_id": "run-1", "generated_at": "2026-09-22T23:00:00+08:00",
            "candidate_limit": 20, "project_match_limit": 3,
            "coverage": [
                {"source": "x", "status": "complete", "item_count": 1},
                {"source": "instagram", "status": "blocked", "item_count": 0},
            ],
            "candidates": [{
                "canonical_key": "x:123", "source": "x", "priority": "medium",
                "route": "intelligest_candidate", "evidence_refs": ["./x.json#item-123"],
            }],
            "project_matches": [], "person_matches": [match],
            "duplicates": [], "excluded": [], "limitations": [],
        }

    def test_person_match_to_open_wiki_problem_is_accepted(self) -> None:
        policy = {**self.POLICY, "problems": {
            "jane-manual-listing-workflow": {"person_ids": {"jane-initech"}, "evidence_refs": {"./wiki-problems.json#jane-manual-listing-workflow"}},
        }}
        match = {
            "canonical_key": "x:123", "problem_id": "jane-manual-listing-workflow",
            "person_ids": ["jane-initech"], "relation": "may_solve_problem",
            "reason": {"kind": "ai_hypothesis", "text": "Shows sheet-driven listing automation", "confidence": "medium"},
            "evidence_refs": ["./x.json#item-123", "./wiki-problems.json#jane-manual-listing-workflow"],
        }
        self.assertEqual(MODULE.validate(self._person_payload(match), policy), [])

    def test_person_match_rejects_invented_problem_and_unlinked_person(self) -> None:
        policy = {**self.POLICY, "problems": {
            "jane-manual-listing-workflow": {"person_ids": {"jane-initech"}, "evidence_refs": {"./wiki-problems.json#p"}},
        }}
        invented = {
            "canonical_key": "x:123", "problem_id": "made-up", "person_ids": ["someone"],
            "relation": "may_solve_problem",
            "reason": {"kind": "ai_hypothesis", "text": "Maybe", "confidence": "low"},
            "evidence_refs": ["./x.json#item-123", "./wiki-problems.json#p"],
        }
        errors = MODULE.validate(self._person_payload(invented), policy)
        self.assertTrue(any("not an open problem" in error for error in errors))
        wrong_person = {**invented, "problem_id": "jane-manual-listing-workflow", "person_ids": ["hank-globex"]}
        errors = MODULE.validate(self._person_payload(wrong_person), policy)
        self.assertTrue(any("people linked to that problem" in error for error in errors))

    def test_rejects_wrong_run_inflated_limits_and_missing_fragment(self) -> None:
        payload = {
            "schema_version": 2, "run_id": "wrong-run", "generated_at": "2099-01-01T00:00:00Z",
            "candidate_limit": 999, "project_match_limit": 999,
            "coverage": [
                {"source": "x", "status": "complete", "item_count": 1},
                {"source": "instagram", "status": "blocked", "item_count": 0},
            ],
            "candidates": [{
                "canonical_key": "x:1", "source": "x", "priority": "high",
                "route": "intelligest_candidate", "evidence_refs": ["./x.json#does-not-exist"],
            }],
            "project_matches": [], "duplicates": [], "excluded": [], "limitations": [],
        }
        errors = MODULE.validate(payload, self.POLICY)
        self.assertTrue(any("run_id must match" in error for error in errors))
        self.assertTrue(any("generated_at must match" in error for error in errors))
        self.assertTrue(any("candidate_limit must match" in error for error in errors))
        self.assertTrue(any("project_match_limit must match" in error for error in errors))
        self.assertTrue(any("frozen source cache" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
