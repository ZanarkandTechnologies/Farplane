from __future__ import annotations

import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from next_ticket_id import durable_ticket_ids, next_ticket_ids, reserve_ticket_ids


class NextTicketIdTests(unittest.TestCase):
    def test_scans_active_archive_and_nested_legacy_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            active = root / "tickets" / "TASK-0007"
            archived = root / "tickets" / "archive" / "TASK-0012"
            nested = root / "tickets" / "archive" / "legacy" / "TASK-0021"
            for path, ticket_id in ((active, "TASK-0007"), (archived, "TASK-0012"), (nested, "TASK-0021")):
                path.mkdir(parents=True)
                (path / "ticket.md").write_text(f"---\nticket_id: {ticket_id}\n---\n", encoding="utf-8")
            self.assertEqual(durable_ticket_ids(root), {"TASK-0007", "TASK-0012", "TASK-0021"})
            self.assertEqual(next_ticket_ids(root, 3), ["TASK-0022", "TASK-0023", "TASK-0024"])

    def test_ignores_ticket_fixtures_nested_under_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture = root / "tickets" / "TASK-0007" / "artifacts" / "fixture" / "tickets" / "TASK-9001"
            fixture.mkdir(parents=True)
            (fixture / "ticket.md").write_text("---\nticket_id: TASK-9001\n---\n", encoding="utf-8")
            (root / "tickets" / "TASK-0007" / "ticket.md").write_text("---\nticket_id: TASK-0007\n---\n", encoding="utf-8")
            self.assertEqual(next_ticket_ids(root), ["TASK-0008"])

    def test_frontmatter_identity_counts_even_when_archive_folder_is_wrong(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "tickets" / "archive" / "wrong-folder"
            path.mkdir(parents=True)
            (path / "ticket.md").write_text("---\nticket_id: TASK-0099\n---\n", encoding="utf-8")
            self.assertEqual(next_ticket_ids(root), ["TASK-0100"])

    def test_concurrent_reservations_do_not_collide(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with ThreadPoolExecutor(max_workers=4) as pool:
                batches = list(pool.map(lambda _: reserve_ticket_ids(root, 3), range(4)))
            flattened = [ticket_id for batch in batches for ticket_id in batch]
            self.assertEqual(len(flattened), 12)
            self.assertEqual(len(set(flattened)), 12)


if __name__ == "__main__":
    unittest.main()
