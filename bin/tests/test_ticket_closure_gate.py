from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from bin.validators.check_ticket_closure_gate import validate_ticket_closure


def write_ticket(root: Path, relative: str, *, phase: str = "complete", status: str = "done") -> None:
    path = root / relative / "ticket.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    ticket_id = path.parent.name
    path.write_text(
        "\n".join(
            [
                "---",
                f"ticket_id: {ticket_id}",
                "title: fixture ticket",
                f"phase: {phase}",
                f"status: {status}",
                "owner: codex",
                "claimed_by:",
                "priority: medium",
                "depends_on: []",
                "blocked_by: []",
                "ready: false",
                "approval_required: false",
                "created_at: 2026-07-03T00:00:00Z",
                "updated_at: 2026-07-03T00:00:00Z",
                "next_action: fixture",
                "last_verification: fixture",
                "---",
                "",
                f"# {ticket_id}: fixture",
                "",
            ]
        ),
        encoding="utf-8",
    )


def append_association(root: Path, ticket_id: str, thread_id: str = "thread-123") -> None:
    path = root / ".farplane" / "state" / "ticket-thread-associations.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "ticket_id": ticket_id,
        "thread_id": thread_id,
        "session_id": thread_id,
        "confidence": "completion_only",
        "observed_at": "2026-07-03T00:00:00Z",
    }
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row) + "\n")


class TicketClosureGateTest(unittest.TestCase):
    def test_unrelated_active_ticket_does_not_block_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "tickets/TASK-9999", phase="building", status="building")
            append_association(root, "TASK-9999")

            errors = validate_ticket_closure(root)

        self.assertEqual(errors, [])

    def test_archived_associated_ticket_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "tickets/archive/TASK-9999")
            append_association(root, "TASK-9999")

            errors = validate_ticket_closure(root)

        self.assertEqual(errors, [])

    def test_active_complete_ticket_blocks_until_archived(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "tickets/TASK-9999", phase="complete", status="done")

            errors = validate_ticket_closure(root)

        self.assertIn("active ticket is already complete/done and should be archived", "\n".join(errors))

    def test_active_done_status_blocks_even_when_phase_not_complete(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "tickets/TASK-9999", phase="documenting", status="done")

            errors = validate_ticket_closure(root)

        self.assertIn("active ticket is already complete/done and should be archived", "\n".join(errors))

    def test_missing_associated_ticket_blocks_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            append_association(root, "TASK-9999")

            errors = validate_ticket_closure(root)

        self.assertIn("neither active nor archived", "\n".join(errors))

    def test_ambient_current_run_active_ticket_does_not_block_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "tickets/TASK-9999", phase="building", status="building")
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
            write_ticket(root, "tickets/TASK-9999", phase="building", status="building")
            append_association(root, "TASK-9999", thread_id="session-abc")

            errors = validate_ticket_closure(
                root,
                environ={"CODEX_SESSION_ID": "session-abc"},
            )

        self.assertIn("current session is still tied to active TASK-9999", "\n".join(errors))

    def test_env_associated_archived_ticket_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "tickets/archive/TASK-9999")
            append_association(root, "TASK-9999", thread_id="session-abc")

            errors = validate_ticket_closure(
                root,
                environ={"CODEX_SESSION_ID": "session-abc"},
            )

        self.assertEqual(errors, [])

    def test_legacy_session_state_active_ticket_does_not_block_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "tickets/TASK-9999", phase="building", status="building")
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
