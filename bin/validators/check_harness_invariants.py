#!/usr/bin/env python3
"""
Validate a narrow set of high-value harness invariants.

This checker intentionally stays small and remediation-focused. It backstops a
few repo-critical rules that have already proven easy to drift in prompts/docs,
without trying to lint every surface in the repo.
"""

from __future__ import annotations

import argparse
import re
import tomllib
from dataclasses import dataclass
from pathlib import Path

try:
    from check_farplane_project_files import validate as validate_project_files
except ImportError:  # pragma: no cover - package import path for tests
    from bin.validators.check_farplane_project_files import validate as validate_project_files


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class HarnessRule:
    relative_path: str
    required_substrings: tuple[str, ...] = ()
    forbidden_substrings: tuple[str, ...] = ()
    remediation: str = ""


RULES: tuple[HarnessRule, ...] = (
    HarnessRule(
        relative_path="AGENTS.md",
        required_substrings=(
            "project-local context for developing Farplane itself.",
            "templates/global/AGENTS.md",
            "Prefer `.farplane/` for live runtime state.",
        ),
        remediation=(
            "keep root AGENTS repo-local, point install policy at "
            "`templates/global/AGENTS.md`, and preserve `.farplane/` as the "
            "live runtime root"
        ),
    ),
    HarnessRule(
        relative_path="templates/global/AGENTS.md",
        required_substrings=(
            "AUTONOMY DIRECTIVE - DO NOT REMOVE",
            "EXECUTE TASKS TO COMPLETION WITHOUT ASKING FOR PERMISSION",
        ),
        remediation=(
            "restore the Agent Kernel independent-reasoning contract: evaluate "
            "before agreement, never open with reflexive validation, and state "
            "the supporting reason before agreeing"
        ),
    ),
    HarnessRule(
        relative_path="docs/systems/agent-kernel.md",
        required_substrings=(
            "<!-- BEGIN AGENT_KERNEL_FEATURE_INVENTORY -->",
            "<!-- END AGENT_KERNEL_FEATURE_INVENTORY -->",
            "global_independent_reasoning_before_agreement_01",
        ),
        remediation=(
            "keep the canonical bidirectional AGENTS feature inventory and its "
            "high-risk behavior proof route in the Agent Kernel system owner"
        ),
    ),
    HarnessRule(
        relative_path="docs/templates/global-agents-qa-checklist.md",
        required_substrings=(
            "## Agent Kernel Feature Fidelity Gate",
            "docs/systems/agent-kernel.md",
            "every documented behavior group must remain",
        ),
        remediation=(
            "restore the bidirectional Agent Kernel feature-fidelity gate for "
            "every AGENTS edit, rewrite, or consolidation"
        ),
    ),
    HarnessRule(
        relative_path="skills/consolidate/SKILL.md",
        required_substrings=(
            "Agent Kernel",
            "Feature Fidelity Gate",
            "docs/systems/agent-kernel.md",
            "docs/templates/global-agents-qa-checklist.md",
            "every documented behavior",
            "every surviving or added AGENTS section",
            "python3 bin/validators/check_harness_invariants.py",
        ),
        remediation=(
            "require AGENTS consolidation to load the Agent Kernel inventory "
            "and apply the global AGENTS QA checklist before completion"
        ),
    ),
    HarnessRule(
        relative_path="bin/README.md",
        required_substrings=(
            "hook `session_id` for telemetry correlation",
            "ticket `thread_id` for the canonical one-ticket/one-task-thread join",
            "UserPromptSubmit` no longer writes `.farplane/state/current-run.json`",
        ),
        remediation=(
            "document the ticket-owned task-thread boundary and keep generic "
            "runtime session state on `.farplane/` surfaces"
        ),
    ),
    HarnessRule(
        relative_path="tickets/README.md",
        required_substrings=(
            "a ticket may own one hook-written `thread_id`",
            "`status: active` requires a session-specific `claimed_by`",
        ),
        remediation=(
            "keep exactly one persistent Codex task thread on a ticket while "
            "generic `session_id` values remain runtime-only"
        ),
    ),
    HarnessRule(
        relative_path="tickets/templates/ticket.md",
        required_substrings=(
            "`claimed_by` is present only while status=active",
            "## Summary",
            "## Contract Diagram",
            "## Change Plan",
            "## Done",
            "## QA Strategy",
        ),
        remediation=(
            "keep the ticket template aligned with the ticket/runtime identity "
            "split and compact ticket-as-program contract"
        ),
    ),
)


def validate_root(root: Path, *, include_project_contract: bool = True) -> list[str]:
    errors: list[str] = []
    for rule in RULES:
        path = root / rule.relative_path
        if not path.is_file():
            errors.append(
                f"{rule.relative_path}: missing file | remediation: {rule.remediation}"
            )
            continue

        text = path.read_text(encoding="utf-8")
        for snippet in rule.required_substrings:
            if snippet not in text:
                errors.append(
                    f"{rule.relative_path}: missing required text: {snippet!r} | "
                    f"remediation: {rule.remediation}"
                )
        for snippet in rule.forbidden_substrings:
            if snippet in text:
                errors.append(
                    f"{rule.relative_path}: contains forbidden retired-path text: {snippet!r} | "
                    f"remediation: {rule.remediation}"
                )
    errors.extend(validate_agent_roles(root))
    errors.extend(validate_agent_kernel_inventory(root))
    errors.extend(validate_neutral_reasoning_contract(root))
    if include_project_contract:
        errors.extend(validate_project_files(root))
    return errors


def validate_neutral_reasoning_contract(root: Path) -> list[str]:
    """Require the high-risk reasoning contract in active section prose."""

    relative_path = "templates/global/AGENTS.md"
    path = root / relative_path
    if not path.is_file():
        return []
    section = active_markdown_section(
        path.read_text(encoding="utf-8"), "## Decision And Grounding"
    )
    required = (
        "Evaluate the user's premise independently before choosing whether to agree",
        "Do not begin with agreement, praise, or validation",
        "Express agreement only after stating the supporting reason",
    )
    return [
        f"{relative_path}: active Decision And Grounding section is missing "
        f"required text: {snippet!r} | remediation: restore independent evaluation, "
        "the non-agreement opener, and reason-before-agreement in active prose"
        for snippet in required
        if snippet not in section
    ]


def active_markdown_section(text: str, heading: str) -> str:
    """Extract active prose for one H2, excluding comments and fenced examples."""

    uncommented = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    lines: list[str] = []
    in_section = False
    fence: str | None = None
    for line in uncommented.splitlines():
        stripped = line.lstrip()
        fence_match = re.match(r"^(`{3,}|~{3,})", stripped)
        if fence_match:
            marker = fence_match.group(1)[0]
            if fence is None:
                fence = marker
            elif fence == marker:
                fence = None
            continue
        if fence is not None:
            continue
        if line.strip() == heading:
            in_section = True
            continue
        if in_section and re.match(r"^##\s+\S", line):
            break
        if in_section:
            lines.append(line)
    return "\n".join(lines)


def validate_agent_kernel_inventory(root: Path) -> list[str]:
    """Keep the Agent Kernel inventory and both AGENTS surfaces bidirectional."""

    owner_path = root / "docs" / "systems" / "agent-kernel.md"
    if not owner_path.is_file():
        return []

    text = owner_path.read_text(encoding="utf-8")
    start_marker = "<!-- BEGIN AGENT_KERNEL_FEATURE_INVENTORY -->"
    end_marker = "<!-- END AGENT_KERNEL_FEATURE_INVENTORY -->"
    start = text.find(start_marker)
    end = text.find(end_marker)
    if start == -1 or end == -1 or end <= start:
        return [
            "docs/systems/agent-kernel.md: invalid Agent Kernel feature inventory "
            "markers | remediation: preserve one ordered BEGIN/END inventory block"
        ]

    rows: list[tuple[str, str, str]] = []
    errors: list[str] = []
    seen_ids: set[str] = set()
    seen_sections: set[tuple[str, str]] = set()
    for line in text[start + len(start_marker) : end].splitlines():
        if not re.match(r"^\|\s*`AK-[GP]\d+`\s*\|", line):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if len(cells) != 4:
            errors.append(
                "docs/systems/agent-kernel.md: malformed feature inventory row: "
                f"{line!r} | remediation: keep ID, surface, required section, and behavior group"
            )
            continue
        feature_id, surface, section, _behavior = cells
        if feature_id in seen_ids:
            errors.append(
                f"docs/systems/agent-kernel.md: duplicate feature ID {feature_id!r} | "
                "remediation: keep each Agent Kernel behavior group unique"
            )
            continue
        seen_ids.add(feature_id)
        section_key = (surface, section)
        if section_key in seen_sections:
            errors.append(
                f"docs/systems/agent-kernel.md: duplicate feature section {section!r} "
                f"for {surface} | remediation: keep one behavior-group row per AGENTS section"
            )
            continue
        seen_sections.add(section_key)
        rows.append((feature_id, surface, section))

    if not rows:
        errors.append(
            "docs/systems/agent-kernel.md: Agent Kernel feature inventory has no rows | "
            "remediation: document every level-two section in both AGENTS surfaces"
        )
        return errors

    tracked_surfaces = {"AGENTS.md", "templates/global/AGENTS.md"}
    documented = {(surface, section) for _feature_id, surface, section in rows}
    for _feature_id, surface, _section in rows:
        if surface not in tracked_surfaces:
            errors.append(
                f"docs/systems/agent-kernel.md: unsupported AGENTS surface {surface!r} | "
                "remediation: inventory only the root and global-template AGENTS surfaces"
            )

    implemented: set[tuple[str, str]] = set()
    for surface in tracked_surfaces:
        path = root / surface
        if not path.is_file():
            continue
        for section in level_two_headings(path.read_text(encoding="utf-8")):
            implemented.add((surface, section))

    for surface, section in sorted(documented - implemented):
        errors.append(
            f"docs/systems/agent-kernel.md: documented feature section {section!r} "
            f"is missing from {surface} | remediation: restore the section or record an "
            "accepted feature removal before updating the inventory"
        )
    for surface, section in sorted(implemented - documented):
        errors.append(
            f"{surface}: undocumented Agent Kernel section {section!r} | remediation: "
            "add it to docs/systems/agent-kernel.md or move the behavior to an existing owner"
        )
    return errors


def level_two_headings(text: str) -> list[str]:
    """Return real Markdown H2 headings while ignoring fenced examples."""

    headings: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        stripped = line.lstrip()
        fence_match = re.match(r"^(`{3,}|~{3,})", stripped)
        if fence_match:
            marker = fence_match.group(1)[0]
            if fence is None:
                fence = marker
            elif fence == marker:
                fence = None
            continue
        if fence is None and re.match(r"^##\s+\S", line):
            headings.append(line.strip())
    return headings


def validate_agent_roles(root: Path) -> list[str]:
    errors: list[str] = []
    agents_dir = root / "agents"
    if not agents_dir.is_dir():
        errors.append(
            "agents/: missing directory | remediation: keep canonical subagent role "
            "configs under `agents/*.toml`"
        )
        return errors

    for path in sorted(agents_dir.glob("*.toml")):
        relative_path = path.relative_to(root)
        try:
            payload = tomllib.loads(path.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as exc:
            errors.append(
                f"{relative_path}: invalid TOML: {exc} | remediation: keep agent "
                "role configs parseable TOML"
            )
            continue

        name = payload.get("name")
        if not isinstance(name, str) or not name.strip():
            errors.append(
                f"{relative_path}: missing non-empty `name` | remediation: set "
                f"`name = \"{path.stem}\"`"
            )
            continue

        if name.strip() != path.stem:
            errors.append(
                f"{relative_path}: `name` must match filename stem {path.stem!r} | "
                "remediation: keep role name and filename aligned"
            )

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate narrow high-value harness invariants."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="Repository root to validate (defaults to the current repo).",
    )
    parser.add_argument(
        "--skip-project-contract",
        action="store_true",
        help="Skip project-file checks when a composed lint route runs them separately.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    errors = validate_root(root, include_project_contract=not args.skip_project_contract)
    if errors:
        for error in errors:
            print(error)
        return 1

    rule_count = sum(
        len(rule.required_substrings) + len(rule.forbidden_substrings)
        for rule in RULES
    )
    agent_count = len(list((root / "agents").glob("*.toml")))
    print(
        f"harness invariants OK ({len(RULES)} files checked, {agent_count} agents, "
        f"{rule_count} rules, {'project files checked' if not args.skip_project_contract else 'project files delegated'})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
