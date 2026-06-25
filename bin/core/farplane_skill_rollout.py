#!/usr/bin/env python3
"""Resolve Farplane skill rollout status for UI-facing CLI consumers."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


class SkillRolloutError(ValueError):
    """Raised when skill rollout inputs cannot be resolved safely."""


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SkillRolloutError(f"missing_json:{path}") from exc
    except json.JSONDecodeError as exc:
        raise SkillRolloutError(f"invalid_json:{path}:{exc}") from exc
    if not isinstance(value, dict):
        raise SkillRolloutError(f"invalid_json_shape:{path}:expected_object")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError as exc:
        raise SkillRolloutError(f"missing_jsonl:{path}") from exc
    for line_no, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SkillRolloutError(f"invalid_jsonl:{path}:{line_no}:{exc}") from exc
        if isinstance(row, dict):
            rows.append(row)
    return rows


def count_by(rows: list[dict[str, Any]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(str(row.get(field) or "") for row in rows).items()))


def normalized_skill_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "skillId": str(row.get("skill_id") or row.get("name") or ""),
        "path": str(row.get("path") or ""),
        "source": str(row.get("source") or ""),
        "tier": row.get("tier"),
        "templateVersion": str(row.get("template_version") or row.get("skill_template_version") or ""),
        "status": str(row.get("status") or ""),
        "eval": str(row.get("eval") or ""),
        "qaChecklist": str(row.get("qa_checklist") or ""),
        "skillUi": str(row.get("skill_ui") or ""),
        "hasChecklist": bool(row.get("has_checklist")),
    }


def normalized_template_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "templateId": str(row.get("template_id") or ""),
        "currentVersion": str(row.get("current_version") or ""),
        "featureRefs": list(row.get("feature_refs") or []),
        "targetBasis": str(row.get("target_basis") or ""),
        "consumerId": str(row.get("consumer_id") or ""),
        "consumerScope": str(row.get("consumer_scope") or ""),
        "path": str(row.get("path") or ""),
        "usedVersion": str(row.get("used_version") or ""),
        "status": str(row.get("status") or ""),
    }


def normalize_rollout_summary(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "totalSkills": int(summary.get("total_skills") or 0),
        "byStatus": dict(summary.get("by_status") or {}),
        "byTemplateVersion": dict(summary.get("by_template_version") or {}),
        "bySource": dict(summary.get("by_source") or {}),
    }


def build_counts(
    *,
    skill_rows: list[dict[str, Any]],
    template_rows: list[dict[str, Any]],
) -> dict[str, int]:
    by_status = Counter(str(row.get("status") or "") for row in skill_rows)
    return {
        "skills": len(skill_rows),
        "current": by_status.get("current", 0),
        "stale": by_status.get("stale", 0),
        "missing": by_status.get("missing", 0),
        "external": by_status.get("external", 0),
        "withEval": sum(1 for row in skill_rows if row.get("eval")),
        "withQaChecklist": sum(1 for row in skill_rows if row.get("qa_checklist")),
        "withSkillUi": sum(1 for row in skill_rows if row.get("skill_ui")),
        "withChecklist": sum(1 for row in skill_rows if row.get("has_checklist")),
        "templateRolloutRows": len(template_rows),
        "templateDriftItems": sum(1 for row in template_rows if row.get("status") != "current"),
    }


def resolve_skill_rollout_stats(
    *,
    standard_root: Path,
    registry_path: Path | None = None,
    intelligence_path: Path | None = None,
) -> dict[str, Any]:
    standard_root = standard_root.resolve()
    registry = registry_path or standard_root / "docs" / "skills" / "registry.jsonl"
    intelligence = (
        intelligence_path
        or standard_root / "skills" / "skill-maintenance" / "graph" / "skill-template-intelligence.json"
    )
    registry_rows = read_jsonl(registry)
    intelligence_payload = read_json(intelligence)
    raw_rollout = intelligence_payload.get("rollout")
    if not isinstance(raw_rollout, list):
        raise SkillRolloutError(f"invalid_rollout_shape:{intelligence}:rollout_expected_list")
    raw_template_rollout = intelligence_payload.get("template_rollout") or []
    if not isinstance(raw_template_rollout, list):
        raise SkillRolloutError(f"invalid_rollout_shape:{intelligence}:template_rollout_expected_list")

    raw_skill_rows = [row for row in raw_rollout if isinstance(row, dict)]
    raw_template_rows = [row for row in raw_template_rollout if isinstance(row, dict)]
    skill_rows = [normalized_skill_row(row) for row in raw_skill_rows]
    template_rows = [normalized_template_row(row) for row in raw_template_rows]
    current_template_version = str(intelligence_payload.get("current_template_version") or "")
    return {
        "schema": "farplane_skill_rollout",
        "schemaVersion": "0.1.0",
        "standardRoot": str(standard_root),
        "skillRegistryPath": str(registry),
        "intelligencePath": str(intelligence),
        "currentTemplateVersion": current_template_version,
        "counts": build_counts(skill_rows=raw_skill_rows, template_rows=raw_template_rows),
        "registryCounts": {
            "skills": len(registry_rows),
            "byTier": count_by(registry_rows, "tier"),
            "bySource": count_by(registry_rows, "source"),
        },
        "rolloutSummary": normalize_rollout_summary(
            intelligence_payload.get("rollout_summary")
            if isinstance(intelligence_payload.get("rollout_summary"), dict)
            else {}
        ),
        "skills": skill_rows,
        "templateRolloutSummary": intelligence_payload.get("template_rollout_summary")
        if isinstance(intelligence_payload.get("template_rollout_summary"), dict)
        else {},
        "templateRollout": template_rows,
    }


def print_summary(payload: dict[str, Any]) -> None:
    counts = payload["counts"]
    print(
        "farplane skill rollout: "
        f"{counts['current']}/{counts['skills']} current, "
        f"{counts['stale']} stale, "
        f"{counts['missing']} missing, "
        f"{counts['external']} external"
    )
    print(
        "templates: "
        f"{counts['templateRolloutRows']} consumer rows, "
        f"{counts['templateDriftItems']} drift items"
    )
    for row in payload["skills"][:10]:
        marker = row["status"] or "unknown"
        print(f"- {marker}: {row['skillId']} ({row['templateVersion'] or 'no-template'})")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command")
    scan = sub.add_parser("scan", help="Resolve skill rollout status for UI rendering.")
    scan.add_argument("--standard-root", default=str(Path(__file__).resolve().parents[2]))
    scan.add_argument("--registry", help="Skill registry JSONL path.")
    scan.add_argument("--intelligence", help="Skill template intelligence JSON path.")
    scan.add_argument("--json", action="store_true")
    scan.set_defaults(func=run_scan)
    return parser


def run_scan(args: argparse.Namespace) -> int:
    payload = resolve_skill_rollout_stats(
        standard_root=Path(args.standard_root).expanduser().resolve(),
        registry_path=Path(args.registry).expanduser().resolve() if args.registry else None,
        intelligence_path=Path(args.intelligence).expanduser().resolve() if args.intelligence else None,
    )
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print_summary(payload)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 0
    try:
        return int(args.func(args))
    except SkillRolloutError as exc:
        print(f"farplane skill rollout: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
