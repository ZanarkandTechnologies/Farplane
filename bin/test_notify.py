#!/usr/bin/env python3
from __future__ import annotations

import io
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
BIN_DIR = str((ROOT / "bin").resolve())
if BIN_DIR not in sys.path:
    sys.path.insert(0, BIN_DIR)

import notify


class NotifyTests(unittest.TestCase):
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
