#!/usr/bin/env python3
"""Lint typed skill frontmatter and report declared artifact-contract coverage."""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bin.core.skill_contract import (  # noqa: E402
    FrontmatterError,
    normalize_skill_frontmatter,
    parse_skill_frontmatter,
)


class FrontmatterLintError(ValueError):
    """Raised when one skill contract would make the artifact graph ambiguous."""


def load_skill_frontmatter(root: Path) -> list[tuple[Path, dict[str, Any]]]:
    rows: list[tuple[Path, dict[str, Any]]] = []
    for skill_path in sorted((root / "skills").glob("*/SKILL.md")):
        try:
            raw = parse_skill_frontmatter(skill_path)
            rows.append((skill_path, normalize_skill_frontmatter(raw, skill_path)))
        except FrontmatterError as exc:
            raise FrontmatterLintError(str(exc)) from exc
    return rows


def artifact_contract_report(rows: list[tuple[Path, dict[str, Any]]]) -> dict[str, Any]:
    producers: dict[str, list[str]] = defaultdict(list)
    consumers: dict[str, list[str]] = defaultdict(list)
    capabilities = 0
    capability_kinds: dict[str, int] = defaultdict(int)

    for _path, metadata in rows:
        capability = metadata.get("capability")
        if not isinstance(capability, dict):
            capability_kinds["core"] += 1
            continue
        capabilities += 1
        capability_kinds[str(capability.get("kind", "invalid"))] += 1
        skill_id = str(metadata["name"])
        produces = capability.get("produces", [])
        consumes = capability.get("consumes", [])
        if isinstance(produces, list):
            for artifact_id in produces:
                producers[str(artifact_id)].append(skill_id)
        if isinstance(consumes, list):
            for artifact_id in consumes:
                consumers[str(artifact_id)].append(skill_id)

    duplicate_outputs = {
        artifact_id: owners
        for artifact_id, owners in sorted(producers.items())
        if len(owners) > 1
    }
    if duplicate_outputs:
        details = "; ".join(
            f"{artifact_id}: {', '.join(owners)}" for artifact_id, owners in duplicate_outputs.items()
        )
        raise FrontmatterLintError(
            "artifact IDs must have one producing skill so dependency direction stays unambiguous: "
            + details
        )

    linked_artifacts = sorted(set(producers).intersection(consumers))
    unresolved_inputs = {
        artifact_id: owners
        for artifact_id, owners in sorted(consumers.items())
        if artifact_id not in producers
    }
    return {
        "capabilities": capabilities,
        "capability_kinds": dict(sorted(capability_kinds.items())),
        "artifact_outputs": len(producers),
        "artifact_dependencies": len(linked_artifacts),
        "unresolved_inputs": unresolved_inputs,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Farplane repository root")
    parser.add_argument("--report", action="store_true", help="print unresolved external or unadmitted inputs")
    args = parser.parse_args()

    try:
        rows = load_skill_frontmatter(args.root.resolve())
        report = artifact_contract_report(rows)
    except FrontmatterLintError as exc:
        print(f"skill frontmatter invalid: {exc}", file=sys.stderr)
        return 1

    print(
        "skill frontmatter OK "
        f"({len(rows)} skills, {report['capabilities']} capabilities, "
        f"{report['artifact_dependencies']} directed artifact dependencies)"
    )
    print(
        "capability coverage: "
        + ", ".join(
            f"{kind}={count}" for kind, count in report["capability_kinds"].items()
        )
    )
    if args.report and report["unresolved_inputs"]:
        print("unresolved inputs are external or unadmitted artifact families:")
        for artifact_id, consumers in report["unresolved_inputs"].items():
            print(f"- {artifact_id}: {', '.join(consumers)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
