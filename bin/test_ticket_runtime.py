from __future__ import annotations

import json
import shlex
import sys
import tempfile
import time
import unittest
from unittest import mock
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import ticket_runtime


def wait_for_path(path: Path, timeout: float = 5.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if path.exists():
            return
        time.sleep(0.05)
    raise AssertionError(f"timed out waiting for {path}")


class TicketRuntimeTests(unittest.TestCase):
    def test_ensure_runtime_record_writes_ticket_scoped_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            record = ticket_runtime.ensure_runtime_record(
                ticket_id="TASK-0099",
                branch="pr-123",
                checkout_mode="shared",
                runtime_mode="shared",
                owner_session="agent-03",
                reason="single writer",
                reserve=(),
                frontend_url="",
                backend_url="",
                create_worktree=False,
                frontend_cmd="npm run dev",
                root=root,
            )
            path = ticket_runtime.runtime_record_path("TASK-0099", root)
            self.assertTrue(path.exists())
            loaded = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(record["ticket_id"], "TASK-0099")
            self.assertEqual(loaded["branch"], "pr-123")
            self.assertEqual(loaded["checkout_mode"], "shared")
            self.assertEqual(loaded["checkout_path"], str(root))
            self.assertEqual(loaded["commands"]["frontend_cmd"], "npm run dev")

    def test_ensure_runtime_record_reserves_ports_and_builds_targets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            record = ticket_runtime.ensure_runtime_record(
                ticket_id="TASK-0099",
                branch="feat/task-0099",
                checkout_mode="shared",
                runtime_mode="branch-runtime",
                owner_session="",
                reason="qa target",
                reserve=("frontend", "backend"),
                frontend_url="",
                backend_url="",
                create_worktree=False,
                root=root,
            )
            self.assertIn("frontend", record["ports"])
            self.assertIn("backend", record["ports"])
            self.assertEqual(
                record["targets"]["frontend_url"],
                f"http://127.0.0.1:{record['ports']['frontend']}",
            )
            self.assertEqual(
                record["targets"]["backend_url"],
                f"http://127.0.0.1:{record['ports']['backend']}",
            )

    def test_qa_payload_reads_declared_targets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket_runtime.ensure_runtime_record(
                ticket_id="TASK-0099",
                branch="pr-123",
                checkout_mode="shared",
                runtime_mode="shared",
                owner_session="",
                reason="qa target",
                reserve=(),
                frontend_url="http://127.0.0.1:3103",
                backend_url="http://127.0.0.1:4103",
                create_worktree=False,
                root=root,
            )
            payload = ticket_runtime.qa_payload("TASK-0099", root=root)
            self.assertEqual(payload["ticket_id"], "TASK-0099")
            self.assertEqual(payload["status"], "prepared")
            self.assertEqual(
                payload["open_targets"],
                {
                    "frontend_url": "http://127.0.0.1:3103",
                    "backend_url": "http://127.0.0.1:4103",
                },
            )
            self.assertTrue(payload["artifacts_path"].endswith("tickets/TASK-0099/artifacts/qa"))

    def test_up_launches_process_and_down_stops_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            marker = root / "frontend.marker"
            script = root / "hold.py"
            script.write_text(
                "\n".join(
                    [
                        "from pathlib import Path",
                        "import os",
                        "import time",
                        "Path(os.environ['MARKER']).write_text(f\"{os.getpid()}:{os.environ.get('PORT', '')}\", encoding='utf-8')",
                        "while True:",
                        "    time.sleep(0.2)",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            command = (
                f"MARKER={shlex.quote(str(marker))} "
                f"{shlex.quote(sys.executable)} {shlex.quote(str(script))}"
            )
            record = ticket_runtime.up_runtime_record(
                ticket_id="TASK-0099",
                branch="feat/task-0099",
                checkout_mode="shared",
                runtime_mode="branch-runtime",
                owner_session="agent-01",
                reason="qa target",
                reserve=("frontend",),
                frontend_url="",
                backend_url="",
                create_worktree=False,
                frontend_cmd=command,
                root=root,
            )
            wait_for_path(marker)
            pid = record["processes"]["frontend"]["pid"]
            self.assertTrue(ticket_runtime.process_alive(pid))
            self.assertTrue(record["processes"]["frontend"]["running"])
            self.assertIn("frontend_cmd", record["commands"])
            marker_text = marker.read_text(encoding="utf-8")
            self.assertTrue(marker_text.endswith(str(record["ports"]["frontend"])))

            status = ticket_runtime.status_payload("TASK-0099", root=root)
            self.assertTrue(status["processes"]["frontend"]["running"])

            stopped = ticket_runtime.down_runtime_record("TASK-0099", remove_worktree=False, root=root)
            self.assertFalse(stopped["processes"]["frontend"]["running"])
            self.assertFalse(ticket_runtime.process_alive(pid))
            ports_after = ticket_runtime.load_ports_state(root)
            self.assertEqual(ports_after["used"], {})
            qa_after = ticket_runtime.qa_payload("TASK-0099", root=root)
            self.assertEqual(qa_after["status"], "stopped")
            self.assertEqual(qa_after["open_targets"], {})

    def test_branch_compose_runs_up_and_down_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            up_marker = root / "compose-up.txt"
            down_marker = root / "compose-down.txt"
            up_cmd = (
                f"{shlex.quote(sys.executable)} -c "
                f"\"from pathlib import Path; Path({str(up_marker)!r}).write_text('up', encoding='utf-8')\""
            )
            down_cmd = (
                f"{shlex.quote(sys.executable)} -c "
                f"\"from pathlib import Path; Path({str(down_marker)!r}).write_text('down', encoding='utf-8')\""
            )

            record = ticket_runtime.up_runtime_record(
                ticket_id="TASK-0099",
                branch="feat/task-0099",
                checkout_mode="shared",
                runtime_mode="branch-compose",
                owner_session="agent-02",
                reason="compose qa",
                reserve=("frontend", "backend", "db"),
                frontend_url="",
                backend_url="",
                create_worktree=False,
                compose_up_cmd=up_cmd,
                compose_down_cmd=down_cmd,
                root=root,
            )

            self.assertTrue(up_marker.exists())
            self.assertTrue(record["processes"]["compose"]["running"])
            self.assertEqual(record["processes"]["compose"]["stage"], "up")

            stopped = ticket_runtime.down_runtime_record("TASK-0099", remove_worktree=False, root=root)
            self.assertTrue(down_marker.exists())
            self.assertFalse(stopped["processes"]["compose"]["running"])
            self.assertEqual(stopped["status"], "stopped")

    def test_worktree_mode_requires_existing_checkout_or_create(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(SystemExit):
                ticket_runtime.ensure_runtime_record(
                    ticket_id="TASK-0099",
                    branch="pr-123",
                    checkout_mode="worktree",
                    runtime_mode="branch-runtime",
                    owner_session="",
                    reason="isolated checkout",
                    reserve=(),
                    frontend_url="",
                    backend_url="",
                    create_worktree=False,
                    root=root,
                )

    def test_down_keeps_ports_when_stop_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            record = ticket_runtime.ensure_runtime_record(
                ticket_id="TASK-0099",
                branch="feat/task-0099",
                checkout_mode="shared",
                runtime_mode="branch-runtime",
                owner_session="",
                reason="qa target",
                reserve=("frontend",),
                frontend_url="",
                backend_url="",
                create_worktree=False,
                root=root,
            )
            record["status"] = "running"
            record["processes"] = {
                "frontend": {
                    "kind": "process",
                    "command": "npm run dev",
                    "pid": 424242,
                    "running": True,
                }
            }
            ticket_runtime.persist_runtime_record(record, root=root)
            with mock.patch("ticket_runtime.stop_process_group", return_value=False):
                stopped = ticket_runtime.down_runtime_record(
                    "TASK-0099", remove_worktree=False, root=root
                )
            self.assertEqual(stopped["status"], "stop_failed")
            self.assertTrue(stopped["processes"]["frontend"]["running"])
            ports_after = ticket_runtime.load_ports_state(root)
            self.assertIn(str(record["ports"]["frontend"]), ports_after["used"])

    def test_up_persists_launch_failure_after_stopping_existing_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            marker = root / "frontend.marker"
            script = root / "hold.py"
            script.write_text(
                "\n".join(
                    [
                        "from pathlib import Path",
                        "import os",
                        "import time",
                        "Path(os.environ['MARKER']).write_text('running', encoding='utf-8')",
                        "while True:",
                        "    time.sleep(0.2)",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            command = (
                f"MARKER={shlex.quote(str(marker))} "
                f"{shlex.quote(sys.executable)} {shlex.quote(str(script))}"
            )
            first = ticket_runtime.up_runtime_record(
                ticket_id="TASK-0099",
                branch="feat/task-0099",
                checkout_mode="shared",
                runtime_mode="branch-runtime",
                owner_session="agent-01",
                reason="qa target",
                reserve=("frontend",),
                frontend_url="",
                backend_url="",
                create_worktree=False,
                frontend_cmd=command,
                root=root,
            )
            wait_for_path(marker)
            first_pid = first["processes"]["frontend"]["pid"]
            with self.assertRaises(SystemExit):
                ticket_runtime.up_runtime_record(
                    ticket_id="TASK-0099",
                    branch="feat/task-0099",
                    checkout_mode="shared",
                    runtime_mode="branch-runtime",
                    owner_session="agent-01",
                    reason="qa target",
                    reserve=("frontend",),
                    frontend_url="",
                    backend_url="",
                    create_worktree=False,
                    frontend_cmd=f"{shlex.quote(sys.executable)} -c \"import sys; sys.exit(7)\"",
                    root=root,
                )
            failed = ticket_runtime.load_runtime_record("TASK-0099", root=root)
            self.assertEqual(failed["status"], "launch_failed")
            self.assertFalse(failed["processes"]["frontend"]["running"])
            self.assertFalse(ticket_runtime.process_alive(first_pid))


if __name__ == "__main__":
    unittest.main()
