#!/usr/bin/env python3
"""Lint path-owned document frontmatter contracts in docs/."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bin.core.document_contract import (  # noqa: E402
    DocumentContractError,
    validate_document_frontmatter,
)
from bin.core.skill_contract import FrontmatterError, parse_markdown_frontmatter  # noqa: E402


def lint_docs_frontmatter(root: Path) -> tuple[dict[str, int], list[str]]:
    """Return typed document-frontmatter counts and their parse/contract errors."""

    checked: dict[str, int] = {}
    errors: list[str] = []
    for path in sorted((root / "docs").rglob("*.md")):
        try:
            metadata = parse_markdown_frontmatter(path)
        except (FrontmatterError, OSError, UnicodeDecodeError) as exc:
            errors.append(str(exc))
            continue
        if metadata is not None:
            try:
                contract_name = validate_document_frontmatter(metadata, path, root)
            except DocumentContractError as exc:
                errors.append(str(exc))
                continue
            checked[contract_name] = checked.get(contract_name, 0) + 1
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
    summary = ", ".join(f"{kind}={count}" for kind, count in sorted(checked.items()))
    print(f"document frontmatter contracts OK ({summary})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
