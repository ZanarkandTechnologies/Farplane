#!/usr/bin/env python3
"""Lint the syntax and duplicate-key safety of every Markdown frontmatter block in docs/."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bin.core.skill_contract import FrontmatterError, parse_markdown_frontmatter  # noqa: E402


def lint_docs_frontmatter(root: Path) -> tuple[int, list[str]]:
    """Return the count of frontmatter-bearing docs and their syntax errors."""

    checked = 0
    errors: list[str] = []
    for path in sorted((root / "docs").rglob("*.md")):
        try:
            metadata = parse_markdown_frontmatter(path)
        except (FrontmatterError, OSError, UnicodeDecodeError) as exc:
            errors.append(str(exc))
            continue
        if metadata is not None:
            checked += 1
    return checked, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Farplane repository root")
    args = parser.parse_args()

    checked, errors = lint_docs_frontmatter(args.root.resolve())
    if errors:
        print("document frontmatter invalid:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"document frontmatter syntax OK ({checked} documents)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
