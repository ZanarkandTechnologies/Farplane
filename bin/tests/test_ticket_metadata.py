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
