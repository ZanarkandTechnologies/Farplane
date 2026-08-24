#!/usr/bin/env python3
from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_DIR = str((ROOT / "bin" / "runtime").resolve())
if RUNTIME_DIR not in sys.path:
    sys.path.insert(0, RUNTIME_DIR)

import notify


class NotifyTests(unittest.TestCase):
    def test_runtime_guard_silences_notifier_invoked_through_codex_home_link(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = Path(tmp)
            bin_dir = codex_home / "bin"
            bin_dir.mkdir()
            (bin_dir / "notify.py").symlink_to(ROOT / "bin" / "notify.py")
            (bin_dir / "_compat.py").symlink_to(ROOT / "bin" / "_compat.py")
            (codex_home / ".farplane-notify-disabled").write_text("disabled\n", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(bin_dir / "notify.py"), json.dumps({"type": "agent-turn-complete"})],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            self.assertEqual(result.stderr, "")

    def test_runtime_guard_silences_already_configured_notifier(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = Path(tmp)
            (codex_home / ".farplane-notify-disabled").write_text("disabled\n", encoding="utf-8")

            with (
                patch.dict(os.environ, {"FARPLANE_NOTIFY_HOME": str(codex_home)}),
                patch.object(sys, "argv", ["notify.py", json.dumps({"type": "agent-turn-complete"})]),
                patch.object(notify, "announce_message") as announce_message,
            ):
                result = notify.main()

            self.assertEqual(result, 0)
            announce_message.assert_not_called()

    def test_announce_message_fallback_keeps_stdout_clean(self) -> None:
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()

        with (
            patch.object(notify, "play_macos_sound", return_value=1),
            patch.object(notify, "speak_macos", return_value=1),
            patch.object(notify, "speak_espeak_ng", return_value=1),
            patch.object(notify, "speak_windows_tts", return_value=1),
            redirect_stdout(stdout_buffer),
            redirect_stderr(stderr_buffer),
        ):
            result = notify.announce_message("Task completed successfully")

        self.assertEqual(result, 0)
        self.assertEqual(stdout_buffer.getvalue(), "")
        self.assertEqual(stderr_buffer.getvalue(), "\a")


if __name__ == "__main__":
    unittest.main()
