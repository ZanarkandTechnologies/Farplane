from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = ROOT / "bin" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from farplane_event_store import pending_events
from farplane_ticket_close import TicketCloseError, close_ticket


def no_signal_runner(command: list[str], prompt: str, cwd: Path, timeout: int):
    output = Path(command[command.index("--output-last-message") + 1])
    output.write_text(
        json.dumps(
            {
                "status": "no_signal",
                "summary": "No actionable issue found.",
                "material_findings": [],
                "source_gaps": [],
            }
        ),
        encoding="utf-8",
    )
    return subprocess.CompletedProcess(command, 0, stdout="", stderr="")


def write_project(root: Path) -> Path:
    farplane = root / "farplane"
    farplane.mkdir()
    (farplane / "bindings.yaml").write_text(
        "kind: project-bindings\n"
        "project:\n"
        "  id: close-test\n"
        "event_routes:\n"
        "  - route_id: completion-learning\n"
        "    event_name: farplane.ticket.completed\n"
        "    program_ref: core:ticket-completion-learning@1.2.0\n",
        encoding="utf-8",
    )
    ticket = root / "tickets" / "TASK-0001" / "ticket.md"
    ticket.parent.mkdir(parents=True)
    ticket.write_text(
        "---\n"
        "ticket_id: TASK-0001\n"
        "title: Close fixture\n"
        "status: active\n"
        "claimed_by: codex-test\n"
        "created_at: 2026-07-18T00:00:00Z\n"
        "updated_at: 2026-07-18T00:00:00Z\n"
        "---\n\n# TASK-0001\n",
        encoding="utf-8",
    )
    return ticket


class TicketCloseTests(unittest.TestCase):
    def test_close_archives_updates_metadata_and_emits_once(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_project(root)

            first = close_ticket(root, "task-0001", codex_runner=no_signal_runner)
            second = close_ticket(root, "TASK-0001", codex_runner=no_signal_runner)

            archived = root / "tickets" / "archive" / "TASK-0001" / "ticket.md"
            text = archived.read_text(encoding="utf-8")
            self.assertFalse((root / "tickets" / "TASK-0001").exists())
            self.assertIn("status: done", text)
            self.assertNotIn("claimed_by:", text)
            self.assertNotIn("updated_at: 2026-07-18T00:00:00Z", text)
            self.assertEqual(first["status"], "closed")
            self.assertEqual(second["status"], "already_closed")
            self.assertEqual(first["event_id"], second["event_id"])
            self.assertEqual(first["runs"][0]["run_id"], second["runs"][0]["run_id"])
            self.assertEqual(pending_events(root), [])
            self.assertTrue(Path(second["receipt_path"]).is_file())

    def test_close_rejects_non_success_terminal_ticket(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            ticket.write_text(ticket.read_text(encoding="utf-8").replace("status: active", "status: rejected"), encoding="utf-8")

            with self.assertRaisesRegex(TicketCloseError, "non_success_terminal_status"):
                close_ticket(root, "TASK-0001", codex_runner=no_signal_runner)

    def test_close_keeps_completion_event_pending_when_route_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_project(root)
            bindings = root / "farplane" / "bindings.yaml"
            bindings.write_text(
                bindings.read_text(encoding="utf-8").replace(
                    "core:ticket-completion-learning@1.2.0",
                    "core:missing-program@9.9.9",
                ),
                encoding="utf-8",
            )

            receipt = close_ticket(root, "TASK-0001", codex_runner=no_signal_runner)

            self.assertFalse(receipt["ok"])
            self.assertEqual(receipt["mining_status"], "pending")
            self.assertTrue(receipt["event_id"])
            self.assertTrue((root / "tickets" / "archive" / "TASK-0001" / "ticket.md").is_file())
            self.assertEqual(len(pending_events(root)), 1)


if __name__ == "__main__":
    unittest.main()
