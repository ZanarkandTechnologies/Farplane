from __future__ import annotations

import json
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
BIN_DIR = ROOT / "bin"
if str(BIN_DIR) not in sys.path:
    sys.path.insert(0, str(BIN_DIR))

import farplane


class FarplaneNotifyCliTests(unittest.TestCase):
    def test_disable_removes_direct_farplane_notify(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = Path(tmp)
            (codex_home / "bin").mkdir()
            config = codex_home / "config.toml"
            config.write_text(
                f'model = "gpt-5.5"\nnotify = ["python3", "{codex_home / "bin" / "notify.py"}"]\n[features]\n',
                encoding="utf-8",
            )

            payload = farplane.set_notify_enabled(codex_home, False, dry_run=False)

            self.assertEqual(payload["status"], "disabled")
            self.assertNotIn("notify =", config.read_text(encoding="utf-8"))
            self.assertTrue(payload["backup"])

    def test_disable_preserves_wrapper_but_removes_previous_notify(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = Path(tmp)
            (codex_home / "bin").mkdir()
            previous = ["python3", str(codex_home / "bin" / "notify.py")]
            wrapped = ["SkyComputerUseClient", "turn-ended", "--previous-notify", json.dumps(previous)]
            config = codex_home / "config.toml"
            config.write_text(f"notify = {json.dumps(wrapped)}\n[features]\n", encoding="utf-8")

            payload = farplane.set_notify_enabled(codex_home, False, dry_run=False)
            parsed = farplane.parse_notify_command(config.read_text(encoding="utf-8"), config)

            self.assertEqual(payload["status"], "disabled")
            self.assertEqual(parsed, ["SkyComputerUseClient", "turn-ended"])

    def test_enable_restores_previous_notify_inside_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = Path(tmp)
            (codex_home / "bin").mkdir()
            wrapped = ["SkyComputerUseClient", "turn-ended", "--previous-notify"]
            config = codex_home / "config.toml"
            config.write_text(f"notify = {json.dumps(wrapped)}\n[features]\n", encoding="utf-8")

            payload = farplane.set_notify_enabled(codex_home, True, dry_run=False)
            parsed = farplane.parse_notify_command(config.read_text(encoding="utf-8"), config)

            self.assertEqual(payload["status"], "enabled")
            self.assertEqual(parsed[:3], ["SkyComputerUseClient", "turn-ended", "--previous-notify"])
            self.assertEqual(json.loads(parsed[3]), ["python3", str(codex_home / "bin" / "notify.py")])

    def test_enable_adds_previous_notify_to_plain_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = Path(tmp)
            (codex_home / "bin").mkdir()
            wrapped = ["SkyComputerUseClient", "turn-ended"]
            config = codex_home / "config.toml"
            config.write_text(f"notify = {json.dumps(wrapped)}\n[features]\n", encoding="utf-8")

            payload = farplane.set_notify_enabled(codex_home, True, dry_run=False)
            parsed = farplane.parse_notify_command(config.read_text(encoding="utf-8"), config)

            self.assertEqual(payload["status"], "enabled")
            self.assertEqual(parsed[:3], ["SkyComputerUseClient", "turn-ended", "--previous-notify"])
            self.assertEqual(json.loads(parsed[3]), ["python3", str(codex_home / "bin" / "notify.py")])

    def test_enable_refuses_to_overwrite_custom_notify(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = Path(tmp)
            config = codex_home / "config.toml"
            config.write_text('notify = ["node", "custom.js"]\n', encoding="utf-8")

            with self.assertRaises(farplane.CliError):
                farplane.set_notify_enabled(codex_home, True, dry_run=False)

    def test_notify_without_subcommand_defaults_to_status(self) -> None:
        with patch.object(farplane, "run_notify_status", return_value=0) as run_status:
            result = farplane.main(["farplane", "notify"])

        self.assertEqual(result, 0)
        run_status.assert_called_once()
        args = run_status.call_args.args[0]
        self.assertIsInstance(args, Namespace)
        self.assertIsNone(args.target)
        self.assertFalse(args.json)


if __name__ == "__main__":
    unittest.main()
