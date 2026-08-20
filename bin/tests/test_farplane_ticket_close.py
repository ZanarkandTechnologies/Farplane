from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = ROOT / "bin" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

import farplane_ticket_close as close_module
from farplane_event_store import pending_events
from farplane_ticket_close import TicketFinalizeError, finalize_ticket


PROJECT_REPO = "acme/farplane"
ISSUE_URL = f"https://github.com/{PROJECT_REPO}/issues/17"
def expected_issue_body(ticket_id: str = "TASK-0001") -> str:
    return (
        "## Before\n\n- Completed tickets only had a local archive.\n\n"
        "## After\n\n- The completed behavior is recorded in one project issue.\n\n"
        "## Example\n\n- Finalize the ticket and find its proof in the created issue.\n\n"
        "## Key decisions\n\n- In: create and close the terminal GitHub issue.\n\n"
        "## Proof\n\n- Checks: 1/1 completion items checked.\n\n"
        f"<!-- farplane-ticket-id:{ticket_id} -->\n"
    )
def no_signal_runner(command: list[str], prompt: str, cwd: Path, timeout: int):
    output = Path(command[command.index("--output-last-message") + 1])
    output.write_text(
        json.dumps(
            {
                "status": "no_signal",
                "summary": "No actionable issue found.",
                "material_findings": [],
                "source_gaps": [],
            }
        ),
        encoding="utf-8",
    )
    return subprocess.CompletedProcess(command, 0, stdout="", stderr="")


class GitHubFixture:
    def __init__(
        self,
        *,
        ticket_id: str = "TASK-0001",
        media_digests: tuple[str, ...] = (),
        state: str = "CLOSED",
        body: str | None = None,
        comments: list[dict[str, str]] | None = None,
        exists: bool = True,
        issue_url: str = ISSUE_URL,
        state_reason: str | None = None,
    ) -> None:
        self.calls: list[list[str]] = []
        self.exists = exists
        self.issue = {
            "number": 17,
            "title": f"[{ticket_id}] Close fixture",
            "state": state,
            "stateReason": state_reason if state_reason is not None else ("COMPLETED" if state == "CLOSED" else ""),
            "body": body if body is not None else expected_issue_body(ticket_id),
            "comments": comments
            if comments is not None
            else [
                {
                    "body": (
                        f"<!-- farplane-ticket-media:{ticket_id}:{digest} -->\n"
                        f"![proof](https://github.com/user-attachments/assets/{index:08d}-0000-0000-0000-000000000000)"
                    ),
                    "url": f"{ISSUE_URL}#issuecomment-{index}",
                }
                for index, digest in enumerate(media_digests, start=1)
            ],
            "closedAt": "2026-08-01T07:00:00Z" if state == "CLOSED" else "",
            "url": issue_url,
        }

    def __call__(self, command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
        self.calls.append(command)
        if command[:2] == ["gh", "api"]:
            api_issue = {**self.issue, "html_url": self.issue["url"]}
            return subprocess.CompletedProcess(
                command,
                0,
                stdout=json.dumps([[api_issue]] if self.exists else [[]]),
                stderr="",
            )
        if command[:3] == ["gh", "issue", "create"]:
            body_path = Path(command[command.index("--body-file") + 1])
            self.issue.update(
                {
                    "title": command[command.index("--title") + 1],
                    "body": body_path.read_text(encoding="utf-8"),
                    "state": "OPEN",
                    "stateReason": "",
                    "closedAt": "",
                }
            )
            self.exists = True
            return subprocess.CompletedProcess(command, 0, stdout=f"{self.issue['url']}\n", stderr="")
        if command[:3] == ["gh", "issue", "edit"]:
            body_path = Path(command[command.index("--body-file") + 1])
            self.issue["title"] = command[command.index("--title") + 1]
            self.issue["body"] = body_path.read_text(encoding="utf-8")
            return subprocess.CompletedProcess(command, 0, stdout=f"{self.issue['url']}\n", stderr="")
        if command[:3] == ["gh", "issue", "close"]:
            self.issue["state"] = "CLOSED"
            self.issue["stateReason"] = "COMPLETED"
            self.issue["closedAt"] = "2026-08-01T07:00:00Z"
            return subprocess.CompletedProcess(command, 0, stdout="", stderr="")
        if command[:3] == ["gh", "issue", "view"]:
            payload = self.issue
        else:
            return subprocess.CompletedProcess(command, 1, stdout="", stderr="unexpected command")
        return subprocess.CompletedProcess(command, 0, stdout=json.dumps(payload), stderr="")


def write_project(root: Path, *, program_ref: str = "core:ticket-completion-learning@1.3.0") -> Path:
    farplane = root / "farplane"
    farplane.mkdir()
    (farplane / "bindings.yaml").write_text(
        "kind: project-bindings\n"
        "project:\n"
        "  id: close-test\n"
        "integrations:\n"
        "  github:\n"
        f"    repo: {PROJECT_REPO}\n"
        "event_routes:\n"
        "  - route_id: completion-learning\n"
        "    event_name: farplane.ticket.completed\n"
        f"    program_ref: {program_ref}\n",
        encoding="utf-8",
    )
    ticket = root / "tickets" / "TASK-0001" / "ticket.md"
    ticket.parent.mkdir(parents=True)
    ticket.write_text(
        "---\n"
        "ticket_id: TASK-0001\n"
        "title: Close fixture\n"
        "status: active\n"
        "claimed_by: codex-test\n"
        "created_at: 2026-07-18T00:00:00Z\n"
        "updated_at: 2026-07-18T00:00:00Z\n"
        "---\n\n# TASK-0001\n\n"
        "## Summary\n\nFinalize a completed ticket.\n\n"
        "## Scope\n\n- In: create and close the terminal GitHub issue.\n\n"
        "## Delta\n\n"
        "> **Before:** Completed tickets only had a local archive.\n>\n"
        "> **After:** The completed behavior is recorded in one project issue.\n>\n"
        "> **Example:** Finalize the ticket and find its proof in the created issue.\n\n"
        "## Done\n\n- [x] Finalization is verified.\n",
        encoding="utf-8",
    )
    return ticket


def write_media(root: Path) -> tuple[Path, str]:
    media = root / "tickets" / "TASK-0001" / "artifacts" / "final.png"
    media.parent.mkdir(parents=True)
    media.write_bytes(b"final visual proof")
    return media, hashlib.sha256(media.read_bytes()).hexdigest()


class TicketCloseTests(unittest.TestCase):
    def test_close_verifies_mines_indexes_deletes_and_retries_idempotently(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            media, digest = write_media(root)
            github = GitHubFixture(media_digests=(digest,))

            first = finalize_ticket(
                root,
                "task-0001",
                [media.relative_to(root).as_posix()],
                codex_runner=no_signal_runner,
                github_runner=github,
            )
            second = finalize_ticket(
                root,
                "TASK-0001",
                [media.relative_to(root).as_posix()],
                codex_runner=no_signal_runner,
                github_runner=github,
            )

            rows = [json.loads(line) for line in (root / "tickets" / "archive-index.jsonl").read_text().splitlines()]
            self.assertFalse(ticket.parent.exists())
            self.assertFalse((root / "tickets" / "archive" / "TASK-0001").exists())
            self.assertEqual(first["status"], "closed")
            self.assertEqual(second["status"], "already_closed")
            self.assertTrue(second["local_packet_deleted"])
            self.assertEqual(first["event_id"], second["event_id"])
            self.assertEqual(first["runs"][0]["run_id"], second["runs"][0]["run_id"])
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["schema_version"], 1)
            self.assertEqual(rows[0]["storage"], "github_issue")
            self.assertEqual(rows[0]["status"], "done")
            self.assertEqual(rows[0]["github_issue_url"], ISSUE_URL)
            self.assertEqual(rows[0]["media_comment_urls"], [f"{ISSUE_URL}#issuecomment-1"])
            self.assertEqual(pending_events(root), [])
            self.assertEqual(len(github.calls), 3)
            self.assertEqual(
                github.calls[1],
                [
                    "gh",
                    "issue",
                    "view",
                    "17",
                    "--repo",
                    PROJECT_REPO,
                    "--json",
                    "number,title,state,stateReason,body,comments,closedAt,url",
                ],
            )

    def test_missing_or_invalid_configured_repository_blocks_without_remote_or_local_mutation(self) -> None:
        for label, github_config in (
            ("missing", "  github: {}\n"),
            ("invalid", "  github:\n    repo: https://github.com/acme/farplane\n"),
        ):
            with self.subTest(label=label), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                ticket = write_project(root)
                bindings = root / "farplane" / "bindings.yaml"
                text = bindings.read_text(encoding="utf-8")
                text = text.replace(f"  github:\n    repo: {PROJECT_REPO}\n", github_config)
                bindings.write_text(text, encoding="utf-8")
                github = GitHubFixture()

                with self.assertRaisesRegex(TicketFinalizeError, "github_repo_not_configured"):
                    finalize_ticket(root, "TASK-0001", github_runner=github)

                self.assertIn("status: active", ticket.read_text(encoding="utf-8"))
                self.assertEqual(github.calls, [])
                self.assertFalse((root / "tickets" / "archive-index.jsonl").exists())

    def test_missing_media_marker_blocks_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            media, _ = write_media(root)
            github = GitHubFixture(media_digests=())
            with self.assertRaisesRegex(TicketFinalizeError, "marker"):
                finalize_ticket(root, "TASK-0001", [media], github_runner=github)
            self.assertIn("status: active", ticket.read_text())
            self.assertFalse((root / "tickets" / "archive-index.jsonl").exists())

    def test_marker_only_media_comment_blocks_without_deleting_packet(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            media, digest = write_media(root)
            github = GitHubFixture(
                comments=[
                    {
                        "body": f"<!-- farplane-ticket-media:TASK-0001:{digest} -->",
                        "url": f"{ISSUE_URL}#issuecomment-1",
                    }
                ]
            )

            with self.assertRaisesRegex(TicketFinalizeError, "github_issue_media_attachment_missing"):
                finalize_ticket(root, "TASK-0001", [media], github_runner=github)

            self.assertTrue(ticket.is_file())
            self.assertIn("status: active", ticket.read_text())
            self.assertFalse((root / "tickets" / "archive-index.jsonl").exists())

    def test_closed_stale_issue_content_blocks_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            body = (
                "## Before\n\nProblem.\n\n"
                "## After\n\nResult.\n\n"
                "## Example\n\nExample.\n\n"
                "## Proof\n\nChecks passed.\n\n"
                "<!-- farplane-ticket-id:TASK-0001 -->"
            )

            with self.assertRaisesRegex(TicketFinalizeError, "github_issue_closed_content_mismatch"):
                finalize_ticket(root, "TASK-0001", github_runner=GitHubFixture(body=body))

            self.assertIn("status: active", ticket.read_text())
            self.assertFalse((root / "tickets" / "archive-index.jsonl").exists())

    def test_mining_failure_retains_terminal_local_packet_and_skips_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root, program_ref="core:missing-program@9.9.9")
            github = GitHubFixture()

            receipt = finalize_ticket(
                root,
                "TASK-0001",
                codex_runner=no_signal_runner,
                github_runner=github,
            )

            self.assertFalse(receipt["ok"])
            self.assertEqual(receipt["mining_status"], "pending")
            self.assertEqual(receipt["phase"], "mining_pending")
            self.assertTrue(receipt["event_id"])
            self.assertTrue(ticket.is_file())
            self.assertIn("status: done", ticket.read_text())
            self.assertNotIn("claimed_by:", ticket.read_text())
            self.assertFalse((root / "tickets" / "archive-index.jsonl").exists())
            self.assertEqual(len(pending_events(root)), 1)

    def test_archive_index_conflict_rejects_before_remote_or_local_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            index = root / "tickets" / "archive-index.jsonl"
            index.write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-0001",
                        "github_issue_url": "https://github.com/acme/private-ticket-archive/issues/99",
                    }
                )
                + "\n"
            )
            github = GitHubFixture()

            with self.assertRaisesRegex(TicketFinalizeError, "archive_index_without_closure_receipt"):
                finalize_ticket(root, "TASK-0001", github_runner=github)

            self.assertIn("status: active", ticket.read_text())
            self.assertEqual(github.calls, [])

    def test_terminal_or_index_write_failure_retains_local_packet(self) -> None:
        for failure_path in ("ticket.md", "archive-index.jsonl"):
            with self.subTest(failure_path=failure_path), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                ticket = write_project(root)
                github = GitHubFixture()
                original_atomic_write = close_module._atomic_write_text

                def fail_selected(path: Path, text: str) -> None:
                    if path.name == failure_path:
                        raise OSError(f"write failed: {failure_path}")
                    original_atomic_write(path, text)

                with mock.patch("farplane_ticket_close._atomic_write_text", side_effect=fail_selected):
                    with self.assertRaisesRegex(OSError, "write failed"):
                        finalize_ticket(
                            root,
                            "TASK-0001",
                            codex_runner=no_signal_runner,
                            github_runner=github,
                        )

                self.assertTrue(ticket.is_file())
                self.assertFalse((root / "tickets" / "archive-index.jsonl").exists())
                if failure_path == "ticket.md":
                    self.assertIn("status: active", ticket.read_text())
                else:
                    self.assertIn("status: done", ticket.read_text())
                    receipt = json.loads(
                        (root / ".farplane" / "tickets" / "closures" / "TASK-0001.json").read_text()
                    )
                    self.assertEqual(receipt["phase"], "mined")

    def test_delete_failure_occurs_after_index_and_retries_without_new_mining_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            github = GitHubFixture()

            with mock.patch("farplane_ticket_close.shutil.rmtree", side_effect=OSError("delete failed")):
                with self.assertRaisesRegex(OSError, "delete failed"):
                    finalize_ticket(
                        root,
                        "TASK-0001",
                        codex_runner=no_signal_runner,
                        github_runner=github,
                    )

            indexed_receipt = json.loads(
                (root / ".farplane" / "tickets" / "closures" / "TASK-0001.json").read_text()
            )
            rows_before = (root / "tickets" / "archive-index.jsonl").read_text().splitlines()
            self.assertEqual(indexed_receipt["phase"], "indexed")
            self.assertFalse(indexed_receipt["local_packet_deleted"])
            self.assertTrue(ticket.is_file())
            self.assertEqual(len(rows_before), 1)

            retried = finalize_ticket(
                root,
                "TASK-0001",
                codex_runner=no_signal_runner,
                github_runner=github,
            )
            rows_after = (root / "tickets" / "archive-index.jsonl").read_text().splitlines()
            self.assertEqual(retried["status"], "already_closed")
            self.assertEqual(retried["event_id"], indexed_receipt["event_id"])
            self.assertEqual(retried["runs"], indexed_receipt["runs"])
            self.assertFalse(ticket.parent.exists())
            self.assertEqual(rows_before, rows_after)

    def test_non_success_terminal_ticket_is_not_mutated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_project(root)
            ticket.write_text(ticket.read_text().replace("status: active", "status: rejected"))

            with self.assertRaisesRegex(TicketFinalizeError, "non_success_terminal_status"):
                finalize_ticket(root, "TASK-0001", github_runner=GitHubFixture())
            self.assertIn("status: rejected", ticket.read_text())


if __name__ == "__main__":
    unittest.main()
