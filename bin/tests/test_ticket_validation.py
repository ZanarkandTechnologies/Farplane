from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from bin.core.validation.models import CheckResult, CheckSpec, PathBoundary, ValidationReceipt
from bin.core.validation.boundary import explicit_boundary
from bin.core.validation.receipt import write_receipt
from bin.core.validation.registry import CheckRegistry
from bin.core.validation.run import validate_ticket
from bin.core.validation.select import select_checks


RULES = """
[phase.planning]
checks = ["ticket.metadata"]
[phase.complete]
checks = ["ticket.metadata", "ticket.completion-evidence"]
[[path_check]]
globs = ["skills/**"]
checks = ["skills.check"]
[[path_check]]
globs = ["docs/**"]
checks = ["docs.check"]
"""


def passing(check_id: str):
    def run(context, mode):
        return CheckResult(check_id=check_id, mode=mode, status="pass", output="ok")

    return run


class TicketValidationTest(unittest.TestCase):
    def test_planning_selects_ticket_and_linked_companion(self):
        with tempfile.TemporaryDirectory() as tmp:
            rules = Path(tmp) / "validation.toml"
            rules.write_text(RULES)
            selected = select_checks(
                "planning",
                PathBoundary(source="unavailable"),
                "- Visual companion: `tickets/TASK-0001/diagrams.md`",
                rules,
            )
            self.assertEqual(selected, ["ticket.metadata", "ticket.visual-companion"])

    def test_planning_cannot_bypass_missing_companion_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            rules = Path(tmp) / "validation.toml"
            rules.write_text(RULES)
            selected = select_checks("planning", PathBoundary(source="unavailable"), "# Ticket", rules)
            self.assertEqual(selected, ["ticket.metadata", "ticket.visual-companion"])

    def test_complete_requires_explicit_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            rules = Path(tmp) / "validation.toml"
            rules.write_text(RULES)
            with self.assertRaisesRegex(ValueError, "explicit --path or --base"):
                select_checks("complete", PathBoundary(source="unavailable"), "", rules)

    def test_complete_deduplicates_path_selected_checks(self):
        with tempfile.TemporaryDirectory() as tmp:
            rules = Path(tmp) / "validation.toml"
            rules.write_text(RULES)
            selected = select_checks(
                "complete",
                PathBoundary(source="explicit", paths=("skills/a/SKILL.md", "skills/b/SKILL.md")),
                "",
                rules,
            )
            self.assertEqual(selected, ["ticket.metadata", "ticket.completion-evidence", "skills.check"])

    def test_path_order_does_not_change_selection(self):
        with tempfile.TemporaryDirectory() as tmp:
            rules = Path(tmp) / "validation.toml"
            rules.write_text(RULES)
            first = select_checks(
                "complete",
                PathBoundary(source="explicit", paths=("docs/a.md", "skills/a/SKILL.md")),
                "",
                rules,
            )
            second = select_checks(
                "complete",
                PathBoundary(source="explicit", paths=("skills/a/SKILL.md", "docs/a.md")),
                "",
                rules,
            )
            self.assertEqual(first, second)

    def test_validation_writes_deterministic_receipts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "rules").mkdir()
            (root / "rules" / "validation.toml").write_text(RULES)
            ticket_dir = root / "tickets" / "TASK-0001"
            ticket_dir.mkdir(parents=True)
            ticket = ticket_dir / "ticket.md"
            ticket.write_text("# Ticket\n")
            registry = CheckRegistry()
            registry.register(CheckSpec("ticket.metadata", passing("ticket.metadata")))
            registry.register(CheckSpec("ticket.visual-companion", passing("ticket.visual-companion")))
            receipt = validate_ticket(
                root=root,
                ticket=ticket,
                phase="planning",
                boundary=PathBoundary(source="unavailable"),
                registry=registry,
            )
            self.assertTrue(receipt.ok)
            self.assertTrue((ticket_dir / "artifacts" / "validation" / "planning.json").is_file())
            self.assertTrue((ticket_dir / "artifacts" / "validation" / "planning.md").is_file())

    def test_registry_rejects_unknown_and_duplicate_ids(self):
        registry = CheckRegistry()
        registry.register(CheckSpec("known", passing("known")))
        with self.assertRaisesRegex(ValueError, "duplicate"):
            registry.register(CheckSpec("known", passing("known")))
        with self.assertRaisesRegex(ValueError, "unknown"):
            registry.resolve("arbitrary shell command")

    def test_explicit_boundary_rejects_escape_and_absolute_paths(self):
        for path in ("../escape", "/tmp/escape", "skills/../../escape"):
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, "repository-relative"):
                explicit_boundary([path])

    def test_canonical_receipt_excludes_runtime_duration(self):
        base = dict(
            schema_version=1,
            ticket="tickets/TASK-0001/ticket.md",
            phase="planning",
            path_source="explicit",
            base=None,
            changed_paths=["a.py"],
            selected_checks=["ticket.metadata"],
        )
        first = ValidationReceipt(**base, results=[CheckResult("ticket.metadata", "block", "pass", duration_ms=1)])
        second = ValidationReceipt(**base, results=[CheckResult("ticket.metadata", "block", "pass", duration_ms=999)])
        self.assertEqual(first.as_dict(), second.as_dict())


if __name__ == "__main__":
    unittest.main()
