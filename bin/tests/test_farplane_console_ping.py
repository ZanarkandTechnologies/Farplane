from __future__ import annotations

import importlib.util
import io
import json
import os
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
HOOK_PATH = ROOT / "hooks" / "farplane_console_ping.py"

spec = importlib.util.spec_from_file_location("farplane_console_ping", HOOK_PATH)
assert spec is not None
farplane_console_ping = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(farplane_console_ping)


class FarplaneConsolePingTests(unittest.TestCase):
    def write_ticket(
        self,
        root: Path,
        ticket_id: str,
        title: str,
        *,
        archived: bool = False,
        thread_id: str | None = None,
    ) -> Path:
        base = root / "tickets" / ("archive" if archived else "") / ticket_id
        path = base / "ticket.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        thread_line = f"thread_id: {json.dumps(thread_id)}\n" if thread_id else ""
        path.write_text(
            f"---\nticket_id: {ticket_id}\n{thread_line}title: {title}\n---\n\n# {ticket_id}: {title}\n",
            encoding="utf-8",
        )
        return path

    def write_session_index(self, codex_home: Path, rows: list[object]) -> None:
        codex_home.mkdir(parents=True, exist_ok=True)
        (codex_home / "session_index.jsonl").write_text(
            "".join((json.dumps(row) if isinstance(row, dict) else str(row)) + "\n" for row in rows),
            encoding="utf-8",
        )

    def test_default_endpoint_uses_hook_telemetry_ingress(self) -> None:
        with patch.dict(
            os.environ,
            {
                "FARPLANE_CONFIG_DISABLE": "1",
                "FARPLANE_CONVEX_SITE_URL": "https://example.convex.site",
            },
            clear=True,
        ):
            self.assertEqual(
                farplane_console_ping.telemetry_endpoint(),
                "https://example.convex.site/telemetry/hooks",
            )

    def test_endpoint_uses_saved_runtime_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane_home = root / "farplane"
            farplane_home.mkdir()
            (farplane_home / "config.toml").write_text(
                "[env]\nFARPLANE_CONVEX_SITE_URL = \"https://saved.convex.site\"\n",
                encoding="utf-8",
            )
            with patch.dict(os.environ, {"FARPLANE_STATE_DIR": str(farplane_home)}, clear=True):
                self.assertEqual(
                    farplane_console_ping.telemetry_endpoint(),
                    "https://saved.convex.site/telemetry/hooks",
                )

    def test_build_ping_wraps_turn_start_as_hook_telemetry(self) -> None:
        with (
            patch.dict(
                os.environ,
                {
                    "AIKAGE_AGENT_NAME": "codex",
                    "AIKAGE_MACHINE_NAME": "Studio Mac",
                    "FARPLANE_CONFIG_DISABLE": "1",
                },
                clear=True,
            ),
            patch.object(farplane_console_ping.socket, "gethostname", return_value="studio.local"),
        ):
            body = farplane_console_ping.build_ping(
                {
                    "hook_event_name": "UserPromptSubmit",
                    "session_id": "session-1",
                    "turn_id": "turn-1",
                    "cwd": "/Users/kenji/Farplane UI",
                    "prompt": "secret prompt longer than needed",
                }
            )

        self.assertEqual(body["hookName"], "farplane-console-ping")
        self.assertEqual(body["hookType"], "UserPromptSubmit")
        self.assertEqual(body["sessionId"], "session-1")
        self.assertEqual(
            body["eventKey"],
            "codex-lifecycle:session-1:session-1:turn-1:UserPromptSubmit",
        )
        self.assertEqual(body["projectId"], "codex-proj-users-kenji-farplane-ui")
        self.assertEqual(body["payload"]["eventType"], "turn_start")
        self.assertEqual(body["payload"]["source"], "codex-user-prompt")
        self.assertEqual(body["payload"]["turnId"], "turn-1")
        self.assertEqual(body["payload"]["projectName"], "Farplane UI")
        self.assertEqual(body["payload"]["projectDirectory"], "/Users/kenji/Farplane UI")
        self.assertEqual(body["payload"]["machineId"], "studio.local")
        self.assertEqual(body["payload"]["machineName"], "Studio Mac")
        self.assertNotIn("prompt", body["payload"])

    def test_build_ping_wraps_stop_as_hook_telemetry(self) -> None:
        with patch.dict(os.environ, {"AIKAGE_MACHINE_NAME": "Studio Mac", "FARPLANE_CONFIG_DISABLE": "1"}, clear=True):
            body = farplane_console_ping.build_ping(
                {
                    "hook_event_name": "Stop",
                    "session_id": "session-1",
                    "turn_id": "turn-1",
                    "cwd": "/Users/kenji/Farplane UI",
                }
            )

        self.assertEqual(body["hookType"], "Stop")
        self.assertEqual(body["payload"]["eventType"], "turn_end")
        self.assertEqual(body["payload"]["source"], "codex-stop")

    def test_latest_native_title_enriches_root_lifecycle_and_normalizes_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            codex = root / "codex"
            project = root / "project"
            (project / ".farplane").mkdir(parents=True)
            self.write_session_index(
                codex,
                [
                    {"id": "session-1", "thread_name": "Old title"},
                    "malformed",
                    {"id": "session-10", "thread_name": "Prefix collision"},
                    {"id": "session-1", "thread_name": " Latest\n native\t title "},
                ],
            )
            with patch.dict(os.environ, {"CODEX_HOME": str(codex), "FARPLANE_CONFIG_DISABLE": "1"}, clear=True):
                body = farplane_console_ping.build_ping(
                    {"hook_event_name": "Stop", "session_id": "session-1", "turn_id": "turn-1", "cwd": str(project)}
                )

        self.assertEqual(body["payload"]["nativeThreadTitle"], "Latest native title")
        self.assertEqual(body["payload"]["titleSource"], "native")

    def test_single_ticket_prompt_binds_ticket_thread_without_prompt(self) -> None:
        secret = "bind TASK-0055 and keep secret words private"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            codex = root / "codex"
            project = root / "project"
            self.write_session_index(codex, [])
            self.write_ticket(project, "TASK-0055", " Propagate\tthread\x01 titles ")
            with patch.dict(os.environ, {"CODEX_HOME": str(codex), "FARPLANE_CONFIG_DISABLE": "1"}, clear=True):
                body = farplane_console_ping.build_ping(
                    {
                        "hook_event_name": "UserPromptSubmit",
                        "session_id": "session-1",
                        "turn_id": "turn-1",
                        "cwd": str(project),
                        "prompt": secret,
                    }
                )
            ticket_path = project / "tickets" / "TASK-0055" / "ticket.md"
            bound_thread_id = farplane_console_ping.ticket_thread_id(ticket_path)
            ticket_text = ticket_path.read_text(encoding="utf-8")

        self.assertEqual(body["payload"]["ticketId"], "TASK-0055")
        self.assertEqual(body["payload"]["ticketTitle"], "Propagate thread titles")
        self.assertEqual(body["payload"]["ticketDisplayTitle"], "[TASK-0055] Propagate thread titles")
        self.assertEqual(body["payload"]["titleSource"], "ticket")
        self.assertEqual(bound_thread_id, "session-1")
        self.assertNotIn(secret, json.dumps(body))
        self.assertNotIn(secret, ticket_text)

    def test_later_stop_reloads_existing_ticket_binding(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            codex = root / "codex"
            project = root / "project"
            self.write_session_index(codex, [])
            self.write_ticket(project, "TASK-0055", "Thread titles")
            with patch.dict(os.environ, {"CODEX_HOME": str(codex), "FARPLANE_CONFIG_DISABLE": "1"}, clear=True):
                farplane_console_ping.build_ping(
                    {"hook_event_name": "UserPromptSubmit", "session_id": "session-1", "turn_id": "turn-1", "cwd": str(project), "prompt": "TASK-0055"}
                )
                body = farplane_console_ping.build_ping(
                    {"hook_event_name": "Stop", "session_id": "session-1", "turn_id": "turn-1", "cwd": str(project)}
                )

        self.assertEqual(body["payload"]["ticketDisplayTitle"], "[TASK-0055] Thread titles")

    def test_archived_ticket_uses_h1_fallback_and_caps_titles(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            ticket = project / "tickets" / "archive" / "TASK-0055" / "ticket.md"
            ticket.parent.mkdir(parents=True)
            ticket.write_text(
                f"---\nticket_id: TASK-0055\nthread_id: session-1\n---\n\n# TASK-0055: {'x' * 180}\n",
                encoding="utf-8",
            )
            with patch.dict(os.environ, {"CODEX_HOME": str(root / "codex"), "FARPLANE_CONFIG_DISABLE": "1"}, clear=True):
                body = farplane_console_ping.build_ping(
                    {"hook_event_name": "Stop", "session_id": "session-1", "turn_id": "turn-1", "cwd": str(project)}
                )

        self.assertEqual(len(body["payload"]["ticketTitle"]), 120)
        self.assertEqual(len(body["payload"]["ticketDisplayTitle"]), 120)

    def test_unbound_ticket_is_ignored_on_later_lifecycle(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            self.write_ticket(project, "TASK-0055", "Unbound")
            with patch.dict(os.environ, {"CODEX_HOME": str(root / "codex"), "FARPLANE_CONFIG_DISABLE": "1"}, clear=True):
                body = farplane_console_ping.build_ping(
                    {"hook_event_name": "Stop", "session_id": "session-1", "turn_id": "turn-1", "cwd": str(project)}
                )

        self.assertIsNone(body["payload"]["ticketId"])

    def test_ambiguous_ticket_prompt_and_active_archive_collision_write_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            self.write_ticket(project, "TASK-0055", "Active title")
            self.write_ticket(project, "TASK-0055", "Archive title", archived=True)
            self.write_ticket(project, "TASK-0056", "Other title")
            with patch.dict(os.environ, {"CODEX_HOME": str(root / "codex"), "FARPLANE_CONFIG_DISABLE": "1"}, clear=True):
                collision = farplane_console_ping.build_ping(
                    {"hook_event_name": "UserPromptSubmit", "session_id": "session-1", "turn_id": "turn-1", "cwd": str(project), "prompt": "TASK-0055"}
                )
                multiple = farplane_console_ping.build_ping(
                    {"hook_event_name": "UserPromptSubmit", "session_id": "session-2", "turn_id": "turn-2", "cwd": str(project), "prompt": "compare TASK-0055 and TASK-0056"}
                )

            active_thread = farplane_console_ping.ticket_thread_id(project / "tickets" / "TASK-0055" / "ticket.md")
            other_thread = farplane_console_ping.ticket_thread_id(project / "tickets" / "TASK-0056" / "ticket.md")

        self.assertIsNone(collision["payload"]["ticketId"])
        self.assertIsNone(multiple["payload"]["ticketId"])
        self.assertEqual(active_thread, "")
        self.assertEqual(other_thread, "")

    def test_second_thread_cannot_replace_ticket_thread(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            self.write_ticket(project, "TASK-0055", "Thread titles")
            with patch.dict(os.environ, {"CODEX_HOME": str(root / "codex"), "FARPLANE_CONFIG_DISABLE": "1"}, clear=True):
                first = farplane_console_ping.build_ping(
                    {"hook_event_name": "UserPromptSubmit", "session_id": "thread-a", "turn_id": "turn-1", "cwd": str(project), "prompt": "TASK-0055"}
                )
                second = farplane_console_ping.build_ping(
                    {"hook_event_name": "UserPromptSubmit", "session_id": "thread-b", "turn_id": "turn-2", "cwd": str(project), "prompt": "TASK-0055"}
                )
            bound_thread_id = farplane_console_ping.ticket_thread_id(project / "tickets" / "TASK-0055" / "ticket.md")

        self.assertEqual(first["payload"]["ticketId"], "TASK-0055")
        self.assertIsNone(second["payload"]["ticketId"])
        self.assertEqual(bound_thread_id, "thread-a")

    def test_concurrent_threads_bind_only_one_ticket_thread(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            self.write_ticket(project, "TASK-0055", "Thread titles")

            def bind(thread_id: str) -> dict[str, object]:
                return farplane_console_ping.build_ping(
                    {
                        "hook_event_name": "UserPromptSubmit",
                        "session_id": thread_id,
                        "turn_id": thread_id,
                        "cwd": str(project),
                        "prompt": "TASK-0055",
                    }
                )

            with patch.dict(os.environ, {"CODEX_HOME": str(root / "codex"), "FARPLANE_CONFIG_DISABLE": "1"}, clear=True):
                with ThreadPoolExecutor(max_workers=2) as executor:
                    bodies = list(executor.map(bind, ["thread-a", "thread-b"]))
            ticket_path = project / "tickets" / "TASK-0055" / "ticket.md"
            bound_thread_id = farplane_console_ping.ticket_thread_id(ticket_path)
            lock_path = farplane_console_ping.ticket_thread_lock_path(project, ticket_path)

        self.assertIn(bound_thread_id, {"thread-a", "thread-b"})
        self.assertEqual(
            sum(body["payload"]["ticketId"] == "TASK-0055" for body in bodies),
            1,
        )
        self.assertFalse(lock_path.exists())

    def test_native_title_outranks_ticket_binding(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            codex = root / "codex"
            project = root / "project"
            self.write_session_index(codex, [{"id": "session-1", "thread_name": "Native name"}])
            self.write_ticket(project, "TASK-0055", "Ticket name")
            with patch.dict(os.environ, {"CODEX_HOME": str(codex), "FARPLANE_CONFIG_DISABLE": "1"}, clear=True):
                body = farplane_console_ping.build_ping(
                    {"hook_event_name": "UserPromptSubmit", "session_id": "session-1", "turn_id": "turn-1", "cwd": str(project), "prompt": "TASK-0055"}
                )

        self.assertEqual(body["payload"]["nativeThreadTitle"], "Native name")
        self.assertEqual(body["payload"]["ticketDisplayTitle"], "[TASK-0055] Ticket name")
        self.assertEqual(body["payload"]["titleSource"], "native")

    def test_missing_telemetry_endpoint_still_binds_ticket_thread(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            self.write_ticket(project, "TASK-0055", "Thread titles")
            event = {
                "hook_event_name": "UserPromptSubmit",
                "session_id": "session-1",
                "turn_id": "turn-1",
                "cwd": str(project),
                "prompt": "TASK-0055",
            }
            with (
                patch.dict(
                    os.environ,
                    {
                        "CODEX_HOME": str(root / "codex"),
                        "FARPLANE_CONFIG_DISABLE": "1",
                    },
                    clear=True,
                ),
                patch("sys.stdin", io.StringIO(json.dumps(event))),
            ):
                self.assertEqual(farplane_console_ping.main(), 0)

            ticket_path = project / "tickets" / "TASK-0055" / "ticket.md"
            self.assertEqual(farplane_console_ping.ticket_thread_id(ticket_path), "session-1")

    def test_build_ping_preserves_subagent_identity_and_parent_session(self) -> None:
        with patch.dict(
            os.environ,
            {"AIKAGE_MACHINE_NAME": "Studio Mac", "FARPLANE_CONFIG_DISABLE": "1"},
            clear=True,
        ):
            body = farplane_console_ping.build_ping(
                {
                    "hook_event_name": "SubagentStart",
                    "session_id": "parent-session",
                    "turn_id": "turn-2",
                    "agent_id": "child-thread",
                    "agent_type": "reviewer",
                    "title": "Review office presence",
                    "cwd": "/Users/kenji/Farplane UI",
                }
            )

        self.assertEqual(body["hookType"], "SubagentStart")
        self.assertEqual(body["sessionId"], "parent-session")
        self.assertEqual(body["payload"]["threadId"], "child-thread")
        self.assertEqual(body["payload"]["parentThreadId"], "parent-session")
        self.assertEqual(body["payload"]["agentType"], "reviewer")
        self.assertEqual(body["payload"]["threadTitle"], "Review office presence")
        self.assertIsNone(body["payload"]["nativeThreadTitle"])
        self.assertIsNone(body["payload"]["ticketId"])
        self.assertTrue(body["payload"]["isEphemeral"])

    def test_eval_runtime_classification_skips_telemetry(self) -> None:
        with patch.dict(
            os.environ,
            {
                "FARPLANE_CODEX_RUNTIME_KIND": "ephemeral",
                "FARPLANE_CODEX_RUNTIME_PURPOSE": "eval",
            },
            clear=True,
        ):
            self.assertTrue(farplane_console_ping.should_skip_telemetry())


if __name__ == "__main__":
    unittest.main()
