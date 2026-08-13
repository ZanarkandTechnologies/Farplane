#!/usr/bin/env python3

from __future__ import annotations

import tempfile
import textwrap
import unittest
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tickets" / "scripts" / "check_ticket_metadata.py"


VALID_TICKET_TEXT = """\
---
ticket_id: TASK-9999
title: valid ticket
status: awaiting_review
priority: medium
created_at: 2026-04-10T00:00:00Z
updated_at: 2026-04-10T00:00:00Z
---

# TASK-9999: valid ticket

## Summary
Validator fixture.
"""
def write_file(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text), encoding="utf-8")


def load_ticket_metadata_module():
    spec = importlib.util.spec_from_file_location("farplane_ticket_metadata_test", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load ticket metadata module from {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CheckTicketMetadataTest(unittest.TestCase):
    def setUp(self) -> None:
        self.ticket_metadata = load_ticket_metadata_module()

    def test_validator_passes_for_valid_ticket(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tmpdir:
            root = Path(tmpdir)
            path = root / "TASK-9999" / "ticket.md"
            write_file(path, VALID_TICKET_TEXT)
            errors = self.ticket_metadata.validate_ticket(path)
            self.assertEqual(errors, [])

    def test_validator_rejects_session_id_in_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tmpdir:
            root = Path(tmpdir)
            path = root / "TASK-9999" / "ticket.md"
            write_file(
                path,
                VALID_TICKET_TEXT.replace("status: awaiting_review\n", "status: awaiting_review\nsession_id: sess-123\n"),
            )
            errors = self.ticket_metadata.validate_ticket(path)
            self.assertTrue(errors)
            self.assertIn("session_id must not appear in frontmatter", "\n".join(errors))

    def test_validator_rejects_a_task_thread_bound_to_multiple_tickets(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tmpdir:
            root = Path(tmpdir)
            first = root / "TASK-9998" / "ticket.md"
            second = root / "TASK-9999" / "ticket.md"
            write_file(
                first,
                VALID_TICKET_TEXT.replace("TASK-9999", "TASK-9998").replace(
                    "status: awaiting_review\n",
                    "status: awaiting_review\nthread_id: task-thread-1\n",
                ),
            )
            write_file(
                second,
                VALID_TICKET_TEXT.replace(
                    "status: awaiting_review\n",
                    "status: awaiting_review\nthread_id: task-thread-1\n",
                ),
            )
            errors = self.ticket_metadata.validate_unique_thread_ids([first, second])

        self.assertEqual(len(errors), 1)
        self.assertIn("bound to multiple tickets", errors[0])

    def test_validator_accepts_optional_compute_target(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tmpdir:
            root = Path(tmpdir)
            path = root / "TASK-9999" / "ticket.md"
            write_file(
                path,
                VALID_TICKET_TEXT.replace(
                    "priority: medium\n",
                    "priority: medium\ncompute_target: local_worktree\n",
                ),
            )
            errors = self.ticket_metadata.validate_ticket(path)
            self.assertEqual(errors, [])

    def test_validator_accepts_timezone_bearing_due_at_or_absence(self) -> None:
        for due_at in (None, "2026-04-10T09:00:00Z", "2026-04-10T17:00:00+08:00"):
            with self.subTest(due_at=due_at), tempfile.TemporaryDirectory(dir=ROOT) as tmpdir:
                root = Path(tmpdir)
                path = root / "TASK-9999" / "ticket.md"
                insertion = "" if due_at is None else f"due_at: {due_at}\n"
                write_file(
                    path,
                    VALID_TICKET_TEXT.replace("priority: medium\n", f"priority: medium\n{insertion}"),
                )
                self.assertEqual(self.ticket_metadata.validate_ticket(path), [])

    def test_validator_rejects_invalid_due_at(self) -> None:
        for due_at in ("2026-04-10", "2026-04-10T09:00:00", "not-a-deadline"):
            with self.subTest(due_at=due_at), tempfile.TemporaryDirectory(dir=ROOT) as tmpdir:
                root = Path(tmpdir)
                path = root / "TASK-9999" / "ticket.md"
                write_file(
                    path,
                    VALID_TICKET_TEXT.replace(
                        "priority: medium\n", f"priority: medium\ndue_at: {due_at}\n"
                    ),
                )
                errors = self.ticket_metadata.validate_ticket(path)
                self.assertIn(
                    "due_at must be a timezone-bearing ISO-8601 timestamp",
                    "\n".join(errors),
                )

    def test_validator_rejects_retired_duplicate_state_fields(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tmpdir:
            root = Path(tmpdir)
            path = root / "TASK-9999" / "ticket.md"
            write_file(
                path,
                VALID_TICKET_TEXT.replace("status: awaiting_review\n", "status: awaiting_review\nready: false\nphase: planning\n"),
            )
            errors = self.ticket_metadata.validate_ticket(path)
            self.assertIn("retired metadata fields", "\n".join(errors))

    def test_validator_rejects_ticket_specific_metadata(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tmpdir:
            root = Path(tmpdir)
            path = root / "TASK-9999" / "ticket.md"
            write_file(
                path,
                VALID_TICKET_TEXT.replace("status: awaiting_review\n", "status: awaiting_review\nworkflow_id: social_thread\n"),
            )
            errors = self.ticket_metadata.validate_ticket(path)
            self.assertIn("unsupported metadata fields", "\n".join(errors))

    def test_validator_rejects_unknown_compute_target(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tmpdir:
            root = Path(tmpdir)
            path = root / "TASK-9999" / "ticket.md"
            write_file(
                path,
                VALID_TICKET_TEXT.replace(
                    "priority: medium\n",
                    "priority: medium\ncompute_target: hidden_cluster\n",
                ),
            )
            errors = self.ticket_metadata.validate_ticket(path)
            self.assertTrue(errors)
            self.assertIn("compute_target must be one of", "\n".join(errors))

    def test_validator_accepts_rejected_terminal_status(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tmpdir:
            root = Path(tmpdir)
            path = root / "TASK-9999" / "ticket.md"
            write_file(
                path,
                VALID_TICKET_TEXT.replace("status: awaiting_review\n", "status: rejected\nrejection_reason: boring premise\n"),
            )
            errors = self.ticket_metadata.validate_ticket(path)
            self.assertEqual(errors, [])

    def test_validator_active_requires_claim(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tmpdir:
            root = Path(tmpdir)
            path = root / "TASK-9999" / "ticket.md"
            write_file(path, VALID_TICKET_TEXT.replace("status: awaiting_review\n", "status: active\n"))
            errors = self.ticket_metadata.validate_ticket(path)
            self.assertTrue(errors)
            self.assertIn("status=active requires claimed_by", "\n".join(errors))

    def test_validator_rejected_requires_reason(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tmpdir:
            root = Path(tmpdir)
            path = root / "TASK-9999" / "ticket.md"
            write_file(
                path,
                VALID_TICKET_TEXT.replace("status: awaiting_review\n", "status: rejected\n"),
            )
            errors = self.ticket_metadata.validate_ticket(path)
            self.assertTrue(errors)
            self.assertIn("status=rejected requires rejection_reason or a rejection entry", "\n".join(errors))


if __name__ == "__main__":
    unittest.main()
