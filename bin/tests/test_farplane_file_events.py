from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = ROOT / "bin" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

import farplane_file_events as file_events


def write_project(root: Path) -> Path:
    farplane = root / "farplane"
    farplane.mkdir()
    (farplane / "bindings.yaml").write_text("project:\n  id: event-test\n", encoding="utf-8")
    (farplane / "hooks.json").write_text(
        json.dumps(
            {
                "version": 1,
                "file_events": {
                    "enabled": True,
                    "events": list(file_events.DEFAULT_EVENTS),
                    "patterns": list(file_events.DEFAULT_PATTERNS),
                },
            }
        ),
        encoding="utf-8",
    )
    ticket = root / "tickets" / "TASK-0001" / "ticket.md"
    ticket.parent.mkdir(parents=True)
    ticket.write_text("---\nstatus: todo\n---\n\n# Ticket\n", encoding="utf-8")
    return ticket


def payload(root: Path, *, session: str = "session-a") -> dict[str, object]:
    return {
        "hook_event_name": "PostToolUse",
        "tool_name": "apply_patch",
        "cwd": str(root),
        "session_id": session,
        "tool_input": {"patch": "*** Update File: tickets/TASK-0001/ticket.md"},
    }


class FarplaneFileEventTests(unittest.TestCase):
    def test_first_observation_of_terminal_ticket_emits_completion_and_redacts_sensitive_preview(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            ticket.write_text(
                "---\nstatus: completed\napi_token: should-not-leak\n---\n\n# Ticket\n",
                encoding="utf-8",
            )

            event = file_events.capture_payload(payload(root), project_root=root)[0]

            self.assertEqual(event["event_name"], "farplane.ticket.completed")
            token_delta = next(row for row in event["privacy_safe_delta"]["changed_fields"] if row["path"] == "api_token")
            self.assertEqual(token_delta["after"]["preview"], "[redacted]")
            self.assertNotIn("should-not-leak", json.dumps(event))
            snapshot = file_events.read_json(file_events.snapshot_path(root, "tickets/TASK-0001/ticket.md"))
            self.assertNotIn("should-not-leak", json.dumps(snapshot))

    def test_event_and_outbox_are_durable_before_snapshot_and_retry_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            baseline = file_events.capture_payload(payload(root), project_root=root)[0]
            file_events.acknowledge_event(root, baseline["event_id"])
            ticket.write_text("---\nstatus: completed\n---\n\n# Ticket\n", encoding="utf-8")

            real_atomic_write = file_events.atomic_write_json

            def fail_snapshot(path: Path, value: object) -> None:
                if path.parent.name == "state":
                    raise OSError("simulated snapshot failure")
                real_atomic_write(path, value)

            with mock.patch.object(file_events, "atomic_write_json", side_effect=fail_snapshot):
                with self.assertRaisesRegex(OSError, "snapshot failure"):
                    file_events.capture_payload(payload(root), project_root=root)

            queued = file_events.pending_events(root)
            self.assertEqual(len(queued), 1)
            event_id = queued[0]["event_id"]
            self.assertEqual(queued[0]["event_name"], "farplane.ticket.completed")
            self.assertTrue(file_events.event_record_path(root, event_id).is_file())
            snapshot = file_events.read_json(file_events.snapshot_path(root, "tickets/TASK-0001/ticket.md"))
            self.assertFalse(snapshot["terminal"])

            retried = file_events.capture_payload(payload(root, session="session-b"), project_root=root)
            self.assertEqual([row["event_id"] for row in retried], [event_id])
            self.assertEqual(file_events.pending_events(root)[0]["provenance"]["session_id"], "session-a")
            snapshot = file_events.read_json(file_events.snapshot_path(root, "tickets/TASK-0001/ticket.md"))
            self.assertTrue(snapshot["terminal"])
            self.assertEqual(snapshot["last_event_id"], event_id)

    def test_payload_filters_non_write_tools_and_paths_outside_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_project(root)
            read_payload = {**payload(root), "tool_name": "view_image"}
            outside_payload = {**payload(root), "tool_input": {"path": "/tmp/not-farplane.md"}}

            self.assertEqual(file_events.capture_payload(read_payload, project_root=root), [])
            self.assertEqual(file_events.capture_payload(outside_payload, project_root=root), [])
            self.assertEqual(file_events.pending_events(root), [])


if __name__ == "__main__":
    unittest.main()
