from __future__ import annotations

import sys
import unittest
from pathlib import Path


BIN_DIR = Path(__file__).resolve().parents[1]
if str(BIN_DIR) not in sys.path:
    sys.path.insert(0, str(BIN_DIR))

import farplane


class FarplaneCliParserTests(unittest.TestCase):
    def test_ticket_close_binds_verified_github_issue_url(self) -> None:
        args = farplane.build_parser().parse_args(
            [
                "ticket",
                "close",
                "TASK-0001",
                "--github-issue-url",
                "https://github.com/acme/repo/issues/1",
            ]
        )

        self.assertEqual("TASK-0001", args.ticket_id)
        self.assertEqual("https://github.com/acme/repo/issues/1", args.github_issue_url)

    def test_ticket_close_requires_github_issue_url(self) -> None:
        with self.assertRaises(SystemExit) as raised:
            farplane.build_parser().parse_args(["ticket", "close", "TASK-0001"])

        self.assertEqual(2, raised.exception.code)


if __name__ == "__main__":
    unittest.main()
