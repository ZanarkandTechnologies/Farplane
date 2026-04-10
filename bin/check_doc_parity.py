#!/usr/bin/env python3
"""
Validate the narrow structural parity contract for Codexter's canonical
knowledge-base entrypoints.

This validator is intentionally small. It exists to catch high-signal drift in
the docs the repo treats as its entry surfaces, not to lint all Markdown or
judge the quality of narrative explanations. See MEM-0013.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class FileRule:
    relative_path: str
    required_substrings: tuple[str, ...] = ()
    forbidden_substrings: tuple[str, ...] = ()


RULES: tuple[FileRule, ...] = (
    FileRule(
        relative_path="README.md",
        required_substrings=(
            "Architecture map: [ARCHITECTURE.md]",
            "Feature inventory: [harness-techniques.md]",
            "Review scoring: [skills/review/README.md]",
            "Active queue: [tickets]",
        ),
        forbidden_substrings=(
            "Active queue: none currently",
        ),
    ),
    FileRule(
        relative_path="ARCHITECTURE.md",
        required_substrings=(
            "## Canonical Surfaces",
            "README.md",
            "tickets/README.md",
            "skills/review/references/review-rubric-index.md",
        ),
    ),
    FileRule(
        relative_path="docs/specs/README.md",
        required_substrings=(
            "`ARCHITECTURE.md`",
            "doc-governance.md` - structural versus narrative doc-audit policy",
            "harness-techniques.md` - current-state feature and technique inventory",
            "## Doc Gardening Loop",
            "python3 bin/check_doc_parity.py",
            "python3 tickets/scripts/check_ticket_metadata.py",
            "codex exec",
        ),
    ),
    FileRule(
        relative_path="docs/specs/harness-techniques.md",
        required_substrings=(
            "repo's current-state feature inventory",
            "`ARCHITECTURE.md`",
            "`tickets/README.md`",
            "Mechanical knowledge-base entrypoint checks",
            "Doc-governance workflow for narrative drift",
        ),
    ),
    FileRule(
        relative_path="docs/specs/doc-governance.md",
        required_substrings=(
            "## Structural Checks",
            "python3 bin/check_doc_parity.py",
            "## Narrative Audit",
            "codex exec",
        ),
    ),
    FileRule(
        relative_path="tickets/README.md",
        required_substrings=(
            "- `Review Packet`",
            "python3 tickets/scripts/check_ticket_metadata.py",
            "the ticket is the canonical durable progress surface",
        ),
    ),
)


def validate_root(root: Path) -> list[str]:
    errors: list[str] = []
    for rule in RULES:
        path = root / rule.relative_path
        if not path.is_file():
            errors.append(f"{rule.relative_path}: missing file")
            continue

        text = path.read_text(encoding="utf-8")
        for snippet in rule.required_substrings:
            if snippet not in text:
                errors.append(f"{rule.relative_path}: missing required text: {snippet!r}")
        for snippet in rule.forbidden_substrings:
            if snippet in text:
                errors.append(f"{rule.relative_path}: contains forbidden stale text: {snippet!r}")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate canonical doc parity for the current repo."
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
    print(f"structural doc parity OK ({len(RULES)} files checked, {rule_count} rules)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
