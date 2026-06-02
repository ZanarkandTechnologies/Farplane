from __future__ import annotations

import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from farplane_boards import BoardAdapterError, FileTicketAdapter, WorkItem, WorkItemSelector


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


def assert_work_item_contract(test_case: unittest.TestCase, item: WorkItem) -> None:
    test_case.assertEqual(item.source, "filesystem")
    test_case.assertRegex(item.identifier, r"^TASK-\d{4}$")
    test_case.assertTrue(item.title)
    test_case.assertIsInstance(item.labels, tuple)
    test_case.assertIsInstance(item.blocked_by, tuple)
    test_case.assertIsInstance(item.depends_on, tuple)
    test_case.assertIsInstance(item.ready, bool)
    test_case.assertIsInstance(item.approval_required, bool)
    test_case.assertIsInstance(item.requires_qa, bool)
    test_case.assertIsInstance(item.requires_demo, bool)
    test_case.assertTrue(item.local_ticket_path.endswith("/ticket.md"))
    test_case.assertTrue(item.artifacts_path.endswith("/artifacts"))


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

    def test_filesystem_adapter_satisfies_board_conformance_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "tickets" / "TASK-1234" / "ticket.md", TICKET_TEXT)
            adapter = FileTicketAdapter(root)

            item = adapter.read_work_item(WorkItemSelector(work_item_id="TASK-1234"))
            writeback = adapter.write_evidence(
                item,
                "tickets/TASK-1234/artifacts/review.json",
            )

            assert_work_item_contract(self, item)
            self.assertEqual(item.blocked_by, ("TASK-0002",))
            self.assertEqual(item.depends_on, ("TASK-0001",))
            self.assertEqual(item.compute_target, "local_worktree")
            self.assertFalse(writeback.ok)
            self.assertFalse(writeback.changed)
            self.assertIn("manual", writeback.message)

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
