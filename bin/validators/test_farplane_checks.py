from __future__ import annotations

import unittest
import tempfile
from pathlib import Path

from bin.core.validation.models import PathBoundary, ValidationContext
from bin.validators.farplane_checks import (
    build_registry,
    completion_evidence_check,
    ticket_context_budget_check,
)


class FarplaneChecksTest(unittest.TestCase):
    def test_registry_is_allowlisted_and_contains_no_mutating_modes(self):
        registry = build_registry()
        self.assertEqual(
            registry.ids(),
            (
                "docs.contracts",
                "docs.features",
                "docs.refs",
                "docs.sources",
                "harness.check",
                "project.check",
                "skills.check",
                "templates.check",
                "ticket.completion-evidence",
                "ticket.context-budget",
                "ticket.metadata",
                "ticket.reward",
                "ticket.visual-companion",
            ),
        )

    def test_ticket_context_budget_uses_bounded_progress_tail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket_dir = root / "tickets" / "TASK-0001"
            ticket_dir.mkdir(parents=True)
            ticket = ticket_dir / "ticket.md"
            ticket.write_text("\n".join(["ticket"] * 150) + "\n")
            (ticket_dir / "program.md").write_text("\n".join(["program"] * 60) + "\n")
            (ticket_dir / "progress.md").write_text("\n".join(["progress"] * 1000) + "\n")
            context = ValidationContext(root, ticket, "planning", PathBoundary("unavailable"))

            result = ticket_context_budget_check(context, "block")

            self.assertEqual(result.status, "pass")
            self.assertIn("total=290", result.output)
            self.assertIn("progress_tail=80/1000", result.output)

    def test_ticket_context_budget_blocks_above_400_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket_dir = root / "tickets" / "TASK-0001"
            ticket_dir.mkdir(parents=True)
            ticket = ticket_dir / "ticket.md"
            ticket.write_text("\n".join(["ticket"] * 250) + "\n")
            (ticket_dir / "program.md").write_text("\n".join(["program"] * 100) + "\n")
            (ticket_dir / "progress.md").write_text("\n".join(["progress"] * 80) + "\n")
            context = ValidationContext(root, ticket, "complete", PathBoundary("explicit", ("a.py",)))

            result = ticket_context_budget_check(context, "block")

            self.assertEqual(result.status, "fail")
            self.assertIn("total=430", result.output)
            self.assertIn("do not weaken proof", result.output)

    def test_validation_registry_does_not_expose_workflow_actions(self):
        forbidden = {"write", "install", "credentials", "repair-ticket", "hardcase"}
        for check_id in build_registry().ids():
            self.assertTrue(forbidden.isdisjoint(check_id.split(".")))

    def test_completion_evidence_enforces_existing_flags_and_reviewer(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket_dir = root / "tickets" / "TASK-0001"
            ticket_dir.mkdir(parents=True)
            ticket = ticket_dir / "ticket.md"
            ticket.write_text("## QA Strategy\n\nproof_weight: demo\ndelegated_lanes: [qa-tester, reviewer, demo]\n")
            context = ValidationContext(root, ticket, "complete", PathBoundary("explicit", ("a.py",)))
            result = completion_evidence_check(context, "block")
            self.assertEqual(result.status, "fail")
            self.assertIn("no passing QA", result.output)
            self.assertIn("no passing demo", result.output)
            self.assertIn("completion-review", result.output)

            for kind in ("qa", "demo"):
                path = ticket_dir / "artifacts" / kind / "run"
                path.mkdir(parents=True)
                (path / "result.json").write_text('{"verdict":"pass"}\n')
            review = ticket_dir / "artifacts" / "review"
            review.mkdir(parents=True)
            (review / "completion-review.md").write_text("---\nverdict: pass\noverall_tas: TAS-A\n---\n")
            self.assertEqual(completion_evidence_check(context, "block").status, "pass")

    def test_completion_uses_latest_result_and_correlated_review_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket_dir = root / "tickets" / "TASK-0001"
            ticket_dir.mkdir(parents=True)
            ticket = ticket_dir / "ticket.md"
            ticket.write_text("## QA Strategy\n\nproof_weight: qa\ndelegated_lanes: [qa-tester, reviewer]\n")
            context = ValidationContext(root, ticket, "complete", PathBoundary("explicit", ("a.py",)))
            qa = ticket_dir / "artifacts" / "qa"
            old = qa / "20260101-old"
            new = qa / "20260102-new"
            old.mkdir(parents=True)
            new.mkdir(parents=True)
            (old / "result.json").write_text('{"verdict":"pass"}\n')
            (new / "result.json").write_text('{"verdict":"fail"}\n')
            review = ticket_dir / "artifacts" / "review"
            review.mkdir(parents=True)
            review_path = review / "completion-review.md"

            for payload in (
                "---\nverdict: pass\noverall_tas: TAS-B\n---\n",
                "---\nverdict: revise\noverall_tas: TAS-A\n---\n",
                "not frontmatter",
            ):
                review_path.write_text(payload)
                self.assertEqual(completion_evidence_check(context, "block").status, "fail")

            (new / "result.json").write_text('{"verdict":"pass"}\n')
            review_path.write_text("---\nverdict: pass\noverall_tas: TAS-A\n---\n")
            self.assertEqual(completion_evidence_check(context, "block").status, "pass")

            (new / "result.json").write_text("{malformed")
            self.assertEqual(completion_evidence_check(context, "block").status, "fail")


if __name__ == "__main__":
    unittest.main()
