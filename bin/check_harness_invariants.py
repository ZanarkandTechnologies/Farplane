#!/usr/bin/env python3
"""
Validate a narrow set of high-value harness invariants.

This checker intentionally stays small and remediation-focused. It backstops a
few repo-critical rules that have already proven easy to drift in prompts/docs,
without trying to lint every surface in the repo.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


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
            "project-local context for developing Codexter itself.",
            "templates/global/AGENTS.md",
            "Prefer `.harness/` for live runtime state.",
        ),
        remediation=(
            "keep root AGENTS repo-local, point install policy at "
            "`templates/global/AGENTS.md`, and preserve `.harness/` as the "
            "live runtime root"
        ),
    ),
    HarnessRule(
        relative_path="docs/specs/runtime-surface.md",
        required_substrings=(
            "Public docs should describe `.harness/` as the canonical live runtime root.",
            "There is no separate public legacy execution surface anymore.",
        ),
        forbidden_substrings=(
            ".ralph/",
            ".omx/",
        ),
        remediation=(
            "keep runtime-surface docs on the live Codexter contract: "
            "`.harness/` is canonical and legacy `.ralph/` / `.omx/` paths "
            "belong only in historical surfaces"
        ),
    ),
    HarnessRule(
        relative_path="bin/README.md",
        required_substrings=(
            "raw `session_id` should stay runtime-only",
            ".harness/state/current-run.json",
        ),
        remediation=(
            "document runtime identity as runtime-only and keep public runtime "
            "examples on `.harness/` surfaces"
        ),
    ),
    HarnessRule(
        relative_path="tickets/README.md",
        required_substrings=(
            "do not store raw transport-level runtime ids such as `session_id` in ticket frontmatter",
            "claimed_by: agent-03  # optional active session claim alias",
        ),
        remediation=(
            "keep tickets human-facing only: `claimed_by` is allowed, raw "
            "`session_id` values are not"
        ),
    ),
    HarnessRule(
        relative_path="tickets/templates/ticket.md",
        required_substrings=(
            "claimed_by:",
            "Do not store raw `session_id` values in ticket frontmatter.",
        ),
        remediation=(
            "keep the ticket template aligned with the ticket/runtime identity split"
        ),
    ),
)


def validate_root(root: Path) -> list[str]:
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
                    f"{rule.relative_path}: contains forbidden legacy text: {snippet!r} | "
                    f"remediation: {rule.remediation}"
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
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    errors = validate_root(root)
    if errors:
        for error in errors:
            print(error)
        return 1

    rule_count = sum(
        len(rule.required_substrings) + len(rule.forbidden_substrings)
        for rule in RULES
    )
    print(f"harness invariants OK ({len(RULES)} files checked, {rule_count} rules)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
