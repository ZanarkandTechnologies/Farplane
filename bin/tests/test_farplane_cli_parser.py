from __future__ import annotations

import argparse
import io
import json
import os
import sys
import tempfile
import unittest
import unittest.mock
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch


BIN_DIR = Path(__file__).resolve().parents[1]
if str(BIN_DIR) not in sys.path:
    sys.path.insert(0, str(BIN_DIR))

import farplane
import farplane_cli_hooks
import farplane_cli_ui
from farplane_cli_base import CliConfig


class FarplaneCliParserTests(unittest.TestCase):
    def test_extension_youtube_accepts_only_supported_actions(self) -> None:
        parser = farplane.build_parser()

        for action in ("start", "status", "doctor", "stop"):
            with self.subTest(action=action):
                args = parser.parse_args(["extension", "youtube", action, "--dry-run", "--json"])

                self.assertEqual(args.extension_action, action)
                self.assertTrue(args.dry_run)
                self.assertTrue(args.json)
                self.assertIs(args.func, farplane_cli_ui.run_extension_youtube)

        with self.assertRaises(SystemExit) as raised:
            parser.parse_args(["extension", "youtube", "restart"])

        self.assertEqual(2, raised.exception.code)

    def test_extension_youtube_resolves_ui_and_uses_doppler_runner(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ui_repo = Path(tmp) / "Farplane-UI-v2"
            (ui_repo / "cli").mkdir(parents=True)
            (ui_repo / "cli" / "farplane-cli.ts").write_text("// test fixture\n", encoding="utf-8")
            (ui_repo / "package.json").write_text(
                json.dumps({"scripts": {"shell": "tsx cli/farplane-cli.ts", "dev:bunker": "vite"}}),
                encoding="utf-8",
            )
            config = CliConfig(
                ui_repo_path=ui_repo,
                codex_home=ui_repo / ".codex",
                created_at=None,
                updated_at=None,
            )
            args = argparse.Namespace(extension_action="status", dry_run=False, json=True)

            with (
                patch.object(farplane_cli_ui, "load_config", return_value=config),
                patch.object(farplane_cli_ui, "run_with_doppler_command", return_value=17) as runner,
            ):
                result = farplane_cli_ui.run_extension_youtube(args)

        self.assertEqual(17, result)
        runner.assert_called_once_with(
            ["npm", "run", "shell", "--", "extension", "youtube", "status", "--json"],
            ui_repo.resolve(),
            dry_run=False,
        )

    def test_doppler_dry_run_prints_only_cwd_and_wrapped_argv(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            output = io.StringIO()

            with (
                patch.object(farplane_cli_hooks.shutil, "which", return_value="/usr/local/bin/doppler"),
                patch.object(farplane_cli_hooks, "doppler_configured", return_value=True) as configured,
                patch.dict(os.environ, {"FARPLANE_TEST_SECRET": "never-print-this-value"}),
                redirect_stdout(output),
            ):
                result = farplane_cli_hooks.run_with_doppler_command(
                    ["npm", "run", "shell", "--", "extension", "youtube", "start"],
                    cwd,
                    dry_run=True,
                )

        self.assertEqual(0, result)
        configured.assert_called_once_with(cwd)
        payload = json.loads(output.getvalue())
        self.assertEqual(str(cwd), payload["cwd"])
        self.assertEqual(
            ["doppler", "run", "--", "npm", "run", "shell", "--", "extension", "youtube", "start"],
            payload["command"],
        )
        self.assertNotIn("never-print-this-value", output.getvalue())

    def test_project_snapshot_supplies_projection_window_defaults(self) -> None:
        args = farplane.build_parser().parse_args(["project", "snapshot"])

        self.assertIsNone(args.window_start)
        self.assertIsNone(args.window_end)
        # Dates and windows are this machine's (docs/farplane-framework/cli.md), never UTC by default.
        with unittest.mock.patch.dict(os.environ, {"TZ": "Asia/Kuala_Lumpur"}):
            local = farplane.build_parser().parse_args(["project", "snapshot"])
        self.assertEqual(local.timezone, "Asia/Kuala_Lumpur")

    def test_a_group_without_its_subcommand_lists_its_subcommands(self) -> None:
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), unittest.mock.patch.object(sys, "stderr", err):
            code = farplane.main(["farplane", "metrics"])
        self.assertEqual(code, 2)
        self.assertIn("refresh", out.getvalue())
        self.assertIn("choose a subcommand", err.getvalue())

    def test_retired_ticket_close_commands_are_not_cli_subcommands(self) -> None:
        for argv in (
            ["ticket", "close", "TASK-0001"],
            ["ticket", "finalize", "TASK-0001"],
            ["mining", "ticket", "TASK-0001"],
        ):
            with self.subTest(argv=argv), redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    farplane.build_parser().parse_args(argv)
                self.assertEqual(2, raised.exception.code)


if __name__ == "__main__":
    unittest.main()
