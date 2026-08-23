#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "bin" / "validators" / "check_harness_invariants.py"
SUBPROCESS_TIMEOUT_SECONDS = 5


ROOT_AGENTS_TEXT = """\
# Farplane AGENTS.md

This file is the project-local context for developing Farplane itself.

The install-time global harness contract now lives at `templates/global/AGENTS.md` and is what `install.sh` links into the live Codex home as `~/.codex/AGENTS.md`.

## Local Operating Rules

- Prefer `.farplane/` for live runtime state.
"""

BIN_README_TEXT = """\
# Bin

- hook `session_id` for telemetry correlation
- ticket `thread_id` for the canonical one-ticket/one-task-thread join
- `UserPromptSubmit` no longer writes `.farplane/state/current-run.json`
"""

TICKETS_README_TEXT = """\
# Tickets

`status: active` requires a session-specific `claimed_by`

- a ticket may own one hook-written `thread_id`
"""

TICKET_TEMPLATE_TEXT = """\
`claimed_by` is present only while status=active

## Summary

## Contract Diagram

## Change Plan

## Done

## QA Strategy

- The hook may set one immutable `thread_id`; never store session_id here.
"""


def write_file(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text), encoding="utf-8")


class CheckHarnessInvariantsTest(unittest.TestCase):
    def build_repo(self, root: Path) -> None:
        write_file(root / "AGENTS.md", ROOT_AGENTS_TEXT)
        write_file(
            root / "agents" / "reviewer.toml",
            """\
name = "reviewer"
model = "gpt-5.5"
developer_instructions = "review"
""",
        )
        write_file(root / "bin/README.md", BIN_README_TEXT)
        write_file(root / "tickets/README.md", TICKETS_README_TEXT)
        write_file(root / "tickets/templates/ticket.md", TICKET_TEMPLATE_TEXT)

    def run_validator(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(root)],
            capture_output=True,
            text=True,
            check=False,
            timeout=SUBPROCESS_TIMEOUT_SECONDS,
        )

    def test_validator_passes_for_valid_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.build_repo(root)
            result = self.run_validator(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("harness invariants OK", result.stdout)

    def test_validator_fails_when_root_agents_loses_global_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.build_repo(root)
            write_file(
                root / "AGENTS.md",
                """\
# Farplane AGENTS.md

This file is generic instructions.
""",
            )
            result = self.run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("templates/global/AGENTS.md", result.stdout)
            self.assertIn("remediation", result.stdout)

    def test_validator_fails_when_ticket_template_drops_claim_alias_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.build_repo(root)
            write_file(
                root / "tickets/templates/ticket.md",
                """\
## Summary

## Contract Diagram

## Change Plan

## Done

## QA Strategy
""",
            )
            result = self.run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("claimed_by", result.stdout)

    def test_validator_fails_when_agent_role_missing_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.build_repo(root)
            write_file(
                root / "agents" / "reviewer.toml",
                """\
model = "gpt-5.5"
developer_instructions = "review"
""",
            )
            result = self.run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("agents/reviewer.toml", result.stdout)
            self.assertIn("missing non-empty `name`", result.stdout)

    def test_validator_fails_when_agent_role_name_does_not_match_filename(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.build_repo(root)
            write_file(
                root / "agents" / "reviewer.toml",
                """\
name = "not-reviewer"
model = "gpt-5.5"
developer_instructions = "review"
""",
            )
            result = self.run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("agents/reviewer.toml", result.stdout)
            self.assertIn("name` must match filename stem", result.stdout)


if __name__ == "__main__":
    unittest.main()
