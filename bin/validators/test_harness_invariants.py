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

## Operating model

- Prefer `.farplane/` for live runtime state.

## Context budget

## Local boundaries

## Durable truth

## Map

## Stop and surface a decision
"""

GLOBAL_AGENTS_TEXT = """\
<!-- AUTONOMY DIRECTIVE - DO NOT REMOVE -->
EXECUTE TASKS TO COMPLETION WITHOUT ASKING FOR PERMISSION.

## Autonomy And Authority

## Decision And Grounding

- Evaluate the user's premise independently before choosing whether to agree.
- Do not begin with agreement, praise, or validation.
- Express agreement only after stating the supporting reason.

## Correction, Work, And Proof

## Response Contract

## Context Routing

## Task State And Artifacts

## Skills And Delegation

## Local Workbench And Safety
"""

AGENT_KERNEL_TEXT = """\
# Agent Kernel

<!-- BEGIN AGENT_KERNEL_FEATURE_INVENTORY -->
| ID | Surface | Required section | Behavior group |
| --- | --- | --- | --- |
| `AK-G01` | `templates/global/AGENTS.md` | `## Autonomy And Authority` | authority |
| `AK-G02` | `templates/global/AGENTS.md` | `## Decision And Grounding` | decisions |
| `AK-G03` | `templates/global/AGENTS.md` | `## Correction, Work, And Proof` | proof |
| `AK-G04` | `templates/global/AGENTS.md` | `## Response Contract` | response |
| `AK-G05` | `templates/global/AGENTS.md` | `## Context Routing` | context |
| `AK-G06` | `templates/global/AGENTS.md` | `## Task State And Artifacts` | state |
| `AK-G07` | `templates/global/AGENTS.md` | `## Skills And Delegation` | skills |
| `AK-G08` | `templates/global/AGENTS.md` | `## Local Workbench And Safety` | workbench |
| `AK-P01` | `AGENTS.md` | `## Operating model` | model |
| `AK-P02` | `AGENTS.md` | `## Context budget` | context |
| `AK-P03` | `AGENTS.md` | `## Local boundaries` | boundaries |
| `AK-P04` | `AGENTS.md` | `## Durable truth` | truth |
| `AK-P05` | `AGENTS.md` | `## Map` | map |
| `AK-P06` | `AGENTS.md` | `## Stop and surface a decision` | decisions |
<!-- END AGENT_KERNEL_FEATURE_INVENTORY -->

global_independent_reasoning_before_agreement_01
"""

GLOBAL_AGENTS_QA_TEXT = """\
## Agent Kernel Feature Fidelity Gate

Read docs/systems/agent-kernel.md. Then every documented behavior group must remain implemented.
"""

CONSOLIDATE_SKILL_TEXT = """\
# Consolidate

Load the Agent Kernel inventory at docs/systems/agent-kernel.md and apply the
Feature Fidelity Gate in docs/templates/global-agents-qa-checklist.md. Keep
every documented behavior and every surviving or added AGENTS section. Run
python3 bin/validators/check_harness_invariants.py.
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
        write_file(root / "templates/global/AGENTS.md", GLOBAL_AGENTS_TEXT)
        write_file(root / "docs/systems/agent-kernel.md", AGENT_KERNEL_TEXT)
        write_file(
            root / "docs/templates/global-agents-qa-checklist.md",
            GLOBAL_AGENTS_QA_TEXT,
        )
        write_file(root / "skills/consolidate/SKILL.md", CONSOLIDATE_SKILL_TEXT)
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

    def test_validator_fails_when_independent_reasoning_contract_is_weakened(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.build_repo(root)
            write_file(
                root / "templates/global/AGENTS.md",
                GLOBAL_AGENTS_TEXT.replace(
                    "- Do not begin with agreement, praise, or validation.\n", ""
                ),
            )
            result = self.run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Do not begin with agreement", result.stdout)

    def test_validator_rejects_reasoning_contract_hidden_in_comment(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.build_repo(root)
            write_file(
                root / "templates/global/AGENTS.md",
                GLOBAL_AGENTS_TEXT.replace(
                    "- Do not begin with agreement, praise, or validation.",
                    "<!-- - Do not begin with agreement, praise, or validation. -->",
                ),
            )
            result = self.run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("active Decision And Grounding section", result.stdout)

    def test_validator_fails_when_agents_section_is_undocumented(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.build_repo(root)
            write_file(
                root / "templates/global/AGENTS.md",
                GLOBAL_AGENTS_TEXT + "\n## Hidden New Policy\n",
            )
            result = self.run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("undocumented Agent Kernel section", result.stdout)

    def test_validator_fails_when_documented_section_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.build_repo(root)
            write_file(
                root / "templates/global/AGENTS.md",
                GLOBAL_AGENTS_TEXT.replace("## Context Routing\n", ""),
            )
            result = self.run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("documented feature section", result.stdout)

    def test_validator_ignores_example_headings_inside_fences(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.build_repo(root)
            write_file(
                root / "templates/global/AGENTS.md",
                GLOBAL_AGENTS_TEXT + "\n```markdown\n## Example Only\n```\n",
            )
            result = self.run_validator(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

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
