#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "bin" / "check_harness_invariants.py"
SUBPROCESS_TIMEOUT_SECONDS = 5


ROOT_AGENTS_TEXT = """\
# Farplane AGENTS.md

This file is the project-local context for developing Farplane itself.

The install-time global harness contract now lives at `templates/global/AGENTS.md` and is what `install.sh` links into the live Codex home as `~/.codex/AGENTS.md`.

## Local Operating Rules

- Prefer `.farplane/` for live runtime state.
"""

INVOCATION_AND_ADAPTERS_TEXT = """\
# Invocation And Adapters

There is no separate public retired execution surface anymore.

## Runtime Surface

- Public docs should describe `.farplane/` as the canonical live runtime root.
"""

BIN_README_TEXT = """\
# Bin

- raw `session_id` should stay runtime-only
- `.farplane/state/current-run.json`
"""

TICKETS_README_TEXT = """\
# Tickets

claimed_by: agent-03  # optional active session claim alias

- do not store raw transport-level runtime ids such as `session_id` in ticket frontmatter
"""

TICKET_TEMPLATE_TEXT = """\
---
claimed_by:
---

## Summary

## Program

## Done / Proof

## State

- Do not store raw `session_id` values in ticket frontmatter.
"""


def write_file(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text), encoding="utf-8")


class CheckHarnessInvariantsTest(unittest.TestCase):
    def build_repo(self, root: Path) -> None:
        write_file(root / "AGENTS.md", ROOT_AGENTS_TEXT)
        write_file(
            root / "agents" / "completion-reviewer.toml",
            """\
name = "completion-reviewer"
model = "gpt-5.5"
developer_instructions = "review"
""",
        )
        write_file(root / "docs/specs/invocation-and-adapters.md", INVOCATION_AND_ADAPTERS_TEXT)
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

    def test_validator_fails_on_retired_runtime_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.build_repo(root)
            write_file(
                root / "docs/specs/invocation-and-adapters.md",
                INVOCATION_AND_ADAPTERS_TEXT + "\nLegacy note: `.ralph/state/current-run.json`\n",
            )
            result = self.run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("contains forbidden retired-path text", result.stdout)
            self.assertIn(".ralph/", result.stdout)

    def test_validator_fails_when_ticket_template_drops_claim_alias_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.build_repo(root)
            write_file(
                root / "tickets/templates/ticket.md",
                """\
## Summary

## Program

## Done / Proof

## State
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
                root / "agents" / "completion-reviewer.toml",
                """\
model = "gpt-5.5"
developer_instructions = "review"
""",
            )
            result = self.run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("agents/completion-reviewer.toml", result.stdout)
            self.assertIn("missing non-empty `name`", result.stdout)

    def test_validator_fails_when_agent_role_name_does_not_match_filename(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.build_repo(root)
            write_file(
                root / "agents" / "completion-reviewer.toml",
                """\
name = "not-completion-reviewer"
model = "gpt-5.5"
developer_instructions = "review"
""",
            )
            result = self.run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("agents/completion-reviewer.toml", result.stdout)
            self.assertIn("name` must match filename stem", result.stdout)


if __name__ == "__main__":
    unittest.main()
