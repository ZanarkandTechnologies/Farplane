from __future__ import annotations

import argparse
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
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
            ui_repo = Path(tmp) / "Farplane-UI"
            (ui_repo / "cli").mkdir(parents=True)
            (ui_repo / "cli" / "farplane-cli.ts").write_text("// test fixture\n", encoding="utf-8")
            (ui_repo / "package.json").write_text(
                json.dumps({"scripts": {"shell": "tsx cli/farplane-cli.ts", "ui": "vite"}}),
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
        self.assertEqual(args.timezone, "UTC")

    def test_ticket_finalize_owns_issue_lifecycle_and_accepts_media(self) -> None:
        args = farplane.build_parser().parse_args(
            [
                "ticket",
                "finalize",
                "TASK-0001",
                "--media",
                "proof.png",
                "--media",
                "demo.mp4",
            ]
        )

        self.assertEqual("TASK-0001", args.ticket_id)
        self.assertEqual(["proof.png", "demo.mp4"], args.media)

    def test_ticket_finalize_requires_no_github_issue_url(self) -> None:
        args = farplane.build_parser().parse_args(["ticket", "finalize", "TASK-0001"])

        self.assertEqual([], args.media)

    def test_ticket_finalize_rejects_retired_github_issue_url_argument(self) -> None:
        with self.assertRaises(SystemExit) as raised:
            farplane.build_parser().parse_args(
                ["ticket", "finalize", "TASK-0001", "--github-issue-url", "https://github.com/acme/repo/issues/1"]
            )

        self.assertEqual(2, raised.exception.code)

    def test_ticket_close_is_not_a_cli_subcommand(self) -> None:
        with self.assertRaises(SystemExit) as raised:
            farplane.build_parser().parse_args(["ticket", "close", "TASK-0001"])

        self.assertEqual(2, raised.exception.code)


if __name__ == "__main__":
    unittest.main()
