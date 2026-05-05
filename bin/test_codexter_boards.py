from __future__ import annotations

import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from codexter_boards import BoardAdapterError, FileTicketAdapter, WorkItemSelector


TICKET_TEXT = """\
---
ticket_id: TASK-1234
title: normalize filesystem tickets
phase: planning
status: review
owner: codex
claimed_by:
priority: high
depends_on:
  - TASK-0001
blocked_by:
  - TASK-0002
ready: false
approval_required: true
requires_qa: true
requires_demo: false
compute_target: local_worktree
created_at: 2026-05-05T00:00:00Z
updated_at: 2026-05-05T00:00:00Z
next_action: approve the adapter
last_verification: none
---

# TASK-1234: normalize filesystem tickets

## Summary
Fixture ticket.
"""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text), encoding="utf-8")


class FileTicketAdapterTests(unittest.TestCase):
    def test_read_work_item_by_ticket_id_normalizes_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "tickets" / "TASK-1234" / "ticket.md", TICKET_TEXT)
            adapter = FileTicketAdapter(root)

            item = adapter.read_work_item(WorkItemSelector(work_item_id="TASK-1234"))

            self.assertEqual(item.source, "filesystem")
            self.assertEqual(item.identifier, "TASK-1234")
            self.assertEqual(item.title, "normalize filesystem tickets")
            self.assertEqual(item.phase, "planning")
            self.assertEqual(item.status, "review")
            self.assertEqual(item.depends_on, ("TASK-0001",))
            self.assertEqual(item.blocked_by, ("TASK-0002",))
            self.assertFalse(item.ready)
            self.assertTrue(item.approval_required)
            self.assertTrue(item.requires_qa)
            self.assertFalse(item.requires_demo)
            self.assertEqual(item.compute_target, "local_worktree")
            self.assertTrue(item.artifacts_path.endswith("tickets/TASK-1234/artifacts"))

    def test_read_work_item_by_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = root / "tickets" / "TASK-1234" / "ticket.md"
            write(ticket, TICKET_TEXT)
            adapter = FileTicketAdapter(root)

            item = adapter.read_work_item(WorkItemSelector(work_item_path=str(ticket)))

            self.assertEqual(item.id, "TASK-1234")

    def test_rejects_path_outside_board_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "tickets").mkdir()
            ticket = root / "outside" / "TASK-1234" / "ticket.md"
            write(ticket, TICKET_TEXT)
            adapter = FileTicketAdapter(root)

            with self.assertRaises(BoardAdapterError):
                adapter.read_work_item(WorkItemSelector(work_item_path=str(ticket)))

    def test_rejects_missing_board_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            with self.assertRaises(BoardAdapterError):
                FileTicketAdapter(root)

    def test_rejects_non_ticket_filename(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = root / "tickets" / "TASK-1234" / "notes.md"
            write(ticket, TICKET_TEXT)
            adapter = FileTicketAdapter(root)

            with self.assertRaises(BoardAdapterError):
                adapter.read_work_item(WorkItemSelector(work_item_path=str(ticket)))

    def test_list_candidates_filters_by_active_phase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "tickets" / "TASK-1234" / "ticket.md", TICKET_TEXT)
            write(
                root / "tickets" / "TASK-1235" / "ticket.md",
                TICKET_TEXT.replace("TASK-1234", "TASK-1235").replace(
                    "phase: planning", "phase: complete"
                ),
            )
            adapter = FileTicketAdapter(root)

            candidates = adapter.list_candidates(active_phases=("planning",))

            self.assertEqual([item.identifier for item in candidates], ["TASK-1234"])

    def test_write_evidence_is_explicitly_manual_in_v1(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "tickets" / "TASK-1234" / "ticket.md", TICKET_TEXT)
            adapter = FileTicketAdapter(root)
            item = adapter.read_work_item(WorkItemSelector(work_item_id="TASK-1234"))

            result = adapter.write_evidence(item, "tickets/TASK-1234/artifacts/review.json")

            self.assertFalse(result.ok)
            self.assertFalse(result.changed)
            self.assertIn("manual", result.message)


if __name__ == "__main__":
    unittest.main()
