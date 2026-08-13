from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from bin.validators.check_ticket_closure_gate import (
    validate_terminal_ticket_hygiene,
    validate_ticket_closure,
)


def write_ticket(root: Path, relative: str, *, status: str = "done", thread_id: str = "") -> None:
    path = root / relative / "ticket.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    ticket_id = path.parent.name
    path.write_text(
        "\n".join(
            [
                "---",
                f"ticket_id: {ticket_id}",
                "title: fixture ticket",
                f"status: {status}",
                *([f"thread_id: {thread_id}"] if thread_id else []),
                "created_at: 2026-07-03T00:00:00Z",
                "updated_at: 2026-07-03T00:00:00Z",
                "---",
                "",
                f"# {ticket_id}: fixture",
                "",
            ]
        ),
        encoding="utf-8",
    )


class TicketClosureGateTest(unittest.TestCase):
    def test_unrelated_active_ticket_does_not_block_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "tickets/TASK-9999", status="active")

            errors = validate_ticket_closure(root)

        self.assertEqual(errors, [])

    def test_archived_associated_ticket_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "tickets/archive/TASK-9999")

            errors = validate_ticket_closure(root)

        self.assertEqual(errors, [])

    def test_unrelated_terminal_ticket_does_not_block_session_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "tickets/TASK-9999", status="done")

            errors = validate_ticket_closure(root)

        self.assertEqual(errors, [])

    def test_terminal_ticket_hygiene_reports_unarchived_packet(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "tickets/TASK-9999", status="done")

            errors = validate_terminal_ticket_hygiene(root)

        self.assertIn("active ticket is terminal and should be archived", "\n".join(errors))

    def test_ambient_current_run_active_ticket_does_not_block_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "tickets/TASK-9999", status="active")
            path = root / ".farplane" / "state" / "current-run.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                json.dumps({"session_id": "session-current", "current_ticket_id": "TASK-9999"}),
                encoding="utf-8",
            )

            errors = validate_ticket_closure(root)

        self.assertEqual(errors, [])

    def test_env_associated_active_ticket_blocks_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "tickets/TASK-9999", status="active", thread_id="session-abc")

            errors = validate_ticket_closure(
                root,
                environ={"CODEX_SESSION_ID": "session-abc"},
            )

        self.assertIn("current session is still tied to active TASK-9999", "\n".join(errors))

    def test_env_associated_archived_ticket_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "tickets/archive/TASK-9999", thread_id="session-abc")

            errors = validate_ticket_closure(
                root,
                environ={"CODEX_SESSION_ID": "session-abc"},
            )

        self.assertEqual(errors, [])

    def test_legacy_session_state_active_ticket_does_not_block_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "tickets/TASK-9999", status="active")
            path = root / ".farplane" / "state" / "sessions" / "session-abc.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                json.dumps({"session_id": "session-abc", "current_ticket_id": "TASK-9999"}),
                encoding="utf-8",
            )

            errors = validate_ticket_closure(
                root,
                environ={"CODEX_SESSION_ID": "session-abc"},
            )

        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
