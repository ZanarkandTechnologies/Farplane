#!/usr/bin/env python3
"""Lint complete typed skill-package contracts and their graph inputs."""

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
    normalize_skill_ensemble,
    normalize_skill_frontmatter,
    parse_skill_ensemble,
    parse_skill_frontmatter,
)


class FrontmatterLintError(ValueError):
    """Raised when one skill contract would make the artifact graph ambiguous."""


RETIRED_FRONTMATTER_FIELDS = {
    "eval": "is derived from the canonical evals/evals.json file",
    "qa_checklist": "was retired; put normal guardrails in Todo List Rule/Assert blocks",
}


def load_skill_contracts(root: Path) -> list[tuple[Path, dict[str, Any]]]:
    """Load each package's required, minimal frontmatter contract from ``SKILL.md``."""

    rows: list[tuple[Path, dict[str, Any]]] = []
    for skill_path in sorted((root / "skills").glob("*/SKILL.md")):
        try:
            raw = parse_skill_frontmatter(skill_path)
            retired = sorted(set(raw).intersection(RETIRED_FRONTMATTER_FIELDS))
            if retired:
                details = "; ".join(
                    f"{field} {RETIRED_FRONTMATTER_FIELDS[field]}" for field in retired
                )
                raise FrontmatterLintError(f"{skill_path}: retired frontmatter field(s): {details}")
            rows.append((skill_path, normalize_skill_frontmatter(raw, skill_path)))
        except FrontmatterError as exc:
            raise FrontmatterLintError(str(exc)) from exc
    return rows


def validate_retired_skill_surfaces(root: Path) -> None:
    """Reject the QA sidecar pattern so a future migration cannot restore it silently."""

    sidecars = sorted((root / "skills").glob("*/qa_checklist.md"))
    if sidecars:
        paths = ", ".join(str(path.relative_to(root)) for path in sidecars)
        raise FrontmatterLintError(
            "qa_checklist.md was retired; move its guardrails into SKILL.md Todo List "
            f"Rule/Assert blocks, evals, validators, or review: {paths}"
        )


def load_skill_ensembles(root: Path) -> list[tuple[Path, dict[str, Any]]]:
    """Load optional persona sidecars through the same typed package linter."""

    rows: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted((root / "skills").glob("*/ensemble.yaml")):
        if not (path.parent / "SKILL.md").is_file():
            raise FrontmatterLintError(
                f"{path}: ensemble sidecar requires its package's SKILL.md"
            )
        try:
            rows.append((path, normalize_skill_ensemble(parse_skill_ensemble(path), path)))
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


def ensemble_contract_report(rows: list[tuple[Path, dict[str, Any]]]) -> dict[str, int]:
    """Summarize validated package-local ensemble coverage without projecting prompts."""

    ensembles = [metadata for _path, metadata in rows]
    return {
        "ensemble_packages": len(ensembles),
        "ensemble_personas": sum(len(ensemble["personas"]) for ensemble in ensembles),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Farplane repository root")
    parser.add_argument("--report", action="store_true", help="print unresolved external or unadmitted inputs")
    args = parser.parse_args()

    try:
        rows = load_skill_contracts(args.root.resolve())
        validate_retired_skill_surfaces(args.root.resolve())
        report = artifact_contract_report(rows)
        report.update(ensemble_contract_report(load_skill_ensembles(args.root.resolve())))
    except FrontmatterLintError as exc:
        print(f"skill frontmatter invalid: {exc}", file=sys.stderr)
        return 1

    print(
        "skill frontmatter OK "
        f"({len(rows)} skills, {report['capabilities']} capabilities, "
        f"{report['artifact_dependencies']} directed artifact dependencies, "
        f"{report['ensemble_packages']} ensembles / {report['ensemble_personas']} personas)"
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
