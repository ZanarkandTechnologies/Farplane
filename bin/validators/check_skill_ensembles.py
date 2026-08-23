#!/usr/bin/env python3
"""Lint typed package-local ensemble persona contracts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bin.core.skill_contract import (  # noqa: E402
    FrontmatterError,
    normalize_skill_ensemble,
    parse_skill_ensemble,
)


def load_skill_ensembles(root: Path) -> list[tuple[Path, dict[str, object]]]:
    """Load every declared ensemble sidecar below ``skills/``."""

    rows: list[tuple[Path, dict[str, object]]] = []
    for path in sorted((root / "skills").glob("*/ensemble.yaml")):
        try:
            rows.append((path, normalize_skill_ensemble(parse_skill_ensemble(path), path)))
        except FrontmatterError as exc:
            raise ValueError(str(exc)) from exc
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Farplane repository root")
    args = parser.parse_args()

    try:
        rows = load_skill_ensembles(args.root.resolve())
    except ValueError as exc:
        print(f"skill ensemble invalid: {exc}", file=sys.stderr)
        return 1

    personas = sum(len(row["personas"]) for _path, row in rows)
    print(f"skill ensembles OK ({len(rows)} packages, {personas} personas)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
