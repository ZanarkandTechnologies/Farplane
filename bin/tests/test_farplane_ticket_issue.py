from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from test_farplane_ticket_close import (
    ISSUE_URL,
    GitHubFixture,
    TicketFinalizeError,
    expected_issue_body,
    finalize_ticket,
    no_signal_runner,
    write_project,
)


class TicketIssueLifecycleTests(unittest.TestCase):
    def test_finalize_creates_and_closes_the_github_issue(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            github = GitHubFixture(exists=False)
            result = finalize_ticket(
                root,
                "TASK-0001",
                codex_runner=no_signal_runner,
                github_runner=github,
            )
            operations = ["list" if call[:2] == ["gh", "api"] else call[2] for call in github.calls]
            self.assertEqual(operations, ["list", "create", "view", "close", "view"])
            self.assertEqual(github.issue["state"], "CLOSED")
            self.assertIn("<!-- farplane-ticket-id:TASK-0001 -->", github.issue["body"])
            self.assertEqual(result["github_issue_url"], ISSUE_URL)
            self.assertFalse(ticket.parent.exists())

    def test_finalize_refreshes_stale_open_issue_before_closing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_project(root)
            stale = expected_issue_body().replace("one project issue", "an outdated issue")
            github = GitHubFixture(state="OPEN", body=stale)
            finalize_ticket(root, "TASK-0001", codex_runner=no_signal_runner, github_runner=github)
            operations = ["list" if call[:2] == ["gh", "api"] else call[2] for call in github.calls]
            self.assertEqual(operations, ["list", "edit", "view", "close", "view"])
            self.assertEqual(github.issue["body"], expected_issue_body())

    def test_issue_identity_enumeration_is_paginated_and_exhaustive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_project(root)
            github = GitHubFixture()
            finalize_ticket(root, "TASK-0001", codex_runner=no_signal_runner, github_runner=github)
            enumeration = github.calls[0]
            self.assertEqual(enumeration[:2], ["gh", "api"])
            self.assertIn("--paginate", enumeration)
            self.assertIn("--slurp", enumeration)
            self.assertIn("per_page=100", enumeration[4])

    def test_closed_issue_requires_completed_state_reason(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            with self.assertRaisesRegex(TicketFinalizeError, "state_reason_invalid"):
                finalize_ticket(
                    root,
                    "TASK-0001",
                    github_runner=GitHubFixture(state_reason="NOT_PLANNED"),
                )
            self.assertTrue(ticket.is_file())

    def test_public_repository_is_allowed_and_mismatched_issue_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            github = GitHubFixture()
            result = finalize_ticket(
                root,
                "TASK-0001",
                codex_runner=no_signal_runner,
                github_runner=github,
            )
            self.assertTrue(result["ok"])
            self.assertFalse(ticket.parent.exists())
            self.assertTrue(all(call[:3] != ["gh", "repo", "view"] for call in github.calls))

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            original = ticket.read_text()
            github = GitHubFixture(issue_url="https://github.com/acme/other/issues/17")
            with self.assertRaisesRegex(TicketFinalizeError, "repo_mismatch"):
                finalize_ticket(root, "TASK-0001", github_runner=github)
            self.assertEqual(ticket.read_text(), original)
            self.assertFalse((root / "tickets" / "archive-index.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
