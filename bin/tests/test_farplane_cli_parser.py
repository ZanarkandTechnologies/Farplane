from __future__ import annotations

import sys
import unittest
from pathlib import Path


BIN_DIR = Path(__file__).resolve().parents[1]
if str(BIN_DIR) not in sys.path:
    sys.path.insert(0, str(BIN_DIR))

import farplane


class FarplaneCliParserTests(unittest.TestCase):
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
