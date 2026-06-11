#!/usr/bin/env python3
"""
Validate a narrow set of high-value harness invariants.

This checker intentionally stays small and remediation-focused. It backstops a
few repo-critical rules that have already proven easy to drift in prompts/docs,
without trying to lint every surface in the repo.
"""

from __future__ import annotations

import argparse
import tomllib
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
        relative_path="docs/specs/invocation-and-adapters.md",
        required_substrings=(
            "Public docs should describe `.farplane/` as the canonical live runtime root.",
            "There is no separate public retired execution surface anymore.",
        ),
        forbidden_substrings=(
            ".ralph/",
            ".omx/",
        ),
        remediation=(
            "keep invocation/runtime docs on the live Farplane contract: "
            "`.farplane/` is canonical and retired runtime paths belong only "
            "in historical surfaces"
        ),
    ),
    HarnessRule(
        relative_path="bin/README.md",
        required_substrings=(
            "raw `session_id` should stay runtime-only",
            ".farplane/state/current-run.json",
        ),
        remediation=(
            "document runtime identity as runtime-only and keep public runtime "
            "examples on `.farplane/` surfaces"
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
            "Result summary:",
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
                    f"{rule.relative_path}: contains forbidden retired-path text: {snippet!r} | "
                    f"remediation: {rule.remediation}"
                )
    errors.extend(validate_agent_roles(root))
    return errors


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
    agent_count = len(list((root / "agents").glob("*.toml")))
    print(
        f"harness invariants OK ({len(RULES)} files checked, {agent_count} agents, "
        f"{rule_count} rules)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
