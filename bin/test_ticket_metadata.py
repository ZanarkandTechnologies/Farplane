#!/usr/bin/env python3

from __future__ import annotations

import tempfile
import textwrap
import unittest
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tickets" / "scripts" / "check_ticket_metadata.py"


VALID_TICKET_TEXT = """\
---
ticket_id: TASK-9999
title: valid ticket
phase: planning
status: review
owner: codex
claimed_by:
priority: medium
depends_on: []
blocked_by: []
ready: false
approval_required: true
created_at: 2026-04-10T00:00:00Z
updated_at: 2026-04-10T00:00:00Z
next_action: wait for approval
last_verification: none
---

# TASK-9999: valid ticket

## Summary
Validator fixture.
"""


def write_file(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text), encoding="utf-8")


def load_ticket_metadata_module():
    spec = importlib.util.spec_from_file_location("codexter_ticket_metadata_test", SCRIPT)
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
                VALID_TICKET_TEXT.replace("claimed_by:\n", "claimed_by:\nsession_id: sess-123\n"),
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


if __name__ == "__main__":
    unittest.main()
