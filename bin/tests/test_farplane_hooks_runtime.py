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
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from hooks.farplane_local_event import capture_local_events


MANAGED_HOOK_FILES = (
    "farplane_console_ping.py",
    "farplane_file_change.py",
    "farplane_local_event.py",
)


def link_codex_home(codex_home: Path) -> None:
    (codex_home / "hooks").mkdir(parents=True, exist_ok=True)
    (codex_home / "bin").mkdir(parents=True, exist_ok=True)
    (codex_home / "hooks.json").symlink_to(ROOT / "hooks.json")
    (codex_home / "bin" / "capture_user_turn.py").symlink_to(ROOT / "bin" / "capture_user_turn.py")
    for hook_name in MANAGED_HOOK_FILES:
        (codex_home / "hooks" / hook_name).symlink_to(ROOT / "hooks" / hook_name)


class FarplaneHooksRuntimeTests(unittest.TestCase):
    def test_hooks_list_and_doctor_enumerate_every_core_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = Path(tmp) / "codex-home"
            link_codex_home(codex_home)

            listed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "bin" / "farplane.py"),
                    "hooks",
                    "list",
                    "--target",
                    str(codex_home),
                    "--json",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(listed.returncode, 0, listed.stderr)
            payload = json.loads(listed.stdout)
            self.assertTrue(payload["ok"])
            commands = payload["commands"]
            self.assertGreaterEqual(len(commands), 5)
            command_text = "\n".join(row["command"] for row in commands)
            self.assertNotIn("FARPLANE_UI_REPO", command_text)
            self.assertNotIn("node_modules/.bin/tsx", command_text)
            self.assertTrue(any(row["target"].endswith("farplane_local_event.py") for row in commands))

            doctor = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "bin" / "farplane.py"),
                    "hooks",
                    "doctor",
                    "--target",
                    str(codex_home),
                    "--json",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(doctor.returncode, 0, doctor.stderr)
            self.assertTrue(json.loads(doctor.stdout)["ok"])

    def test_hooks_doctor_rejects_missing_managed_command_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = Path(tmp) / "codex-home"
            link_codex_home(codex_home)
            (codex_home / "hooks" / "farplane_local_event.py").unlink()

            doctor = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "bin" / "farplane.py"),
                    "hooks",
                    "doctor",
                    "--target",
                    str(codex_home),
                    "--json",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(doctor.returncode, 1)
            payload = json.loads(doctor.stdout)
            self.assertFalse(payload["ok"])
            self.assertTrue(any("target_missing" in issue for issue in payload["issues"]))

    def test_local_event_hook_captures_skill_invocation_without_ui(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            payload = {
                "hook_event_name": "PostToolUse",
                "tool_name": "Bash",
                "cwd": str(root),
                "session_id": "session-1",
                "tool_input": {"command": "sed -n '1,20p' skills/goal-advisor/SKILL.md"},
            }

            first = capture_local_events(payload, root)
            second = capture_local_events(payload, root)

            self.assertEqual(len(first["captured_event_ids"]), 1)
            self.assertEqual(second["captured_event_ids"], [])
            jsonl = root / ".farplane" / "events" / "hook-telemetry.jsonl"
            self.assertEqual(len(jsonl.read_text(encoding="utf-8").splitlines()), 1)

    def test_hooks_test_runs_cookbook_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp) / "project"
            receipt_dir = Path(tmp) / "receipts"
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "bin" / "farplane.py"),
                    "hooks",
                    "test",
                    "--project-root",
                    str(project_root),
                    "--receipt-dir",
                    str(receipt_dir),
                    "--json",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(len(payload["runIds"]), 2)
            self.assertTrue(payload["healthyDoctor"]["ok"])
            self.assertFalse(payload["brokenDoctor"]["ok"])
            self.assertTrue(Path(payload["receiptPath"]).is_file())
            self.assertTrue(Path(payload["errorReceipt"]["path"]).is_file())


if __name__ == "__main__":
    unittest.main()
