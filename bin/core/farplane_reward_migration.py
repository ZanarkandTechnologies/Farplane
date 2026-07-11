#!/usr/bin/env python3
"""One-time migration from score-shaped Reward rows to canonical decisions.

The migration is intentionally conservative: existing explicit canonical
decisions survive, but legacy scores never imply accept/kill/monitor. Missing
reward IDs are derived deterministically from KPI and original check-in time.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml


CANONICAL_FIELDS = (
    "reward_id",
    "kpi_id",
    "expected_reward",
    "check_in_at",
    "actual_result",
    "decision",
    "evaluated_at",
    "evaluation_key",
    "supersedes_evaluation_key",
    "evidence_refs",
)
REMOVED_FIELDS = {"reward_score", "reward_score_reason"}
VALID_DECISIONS = {"", "accept", "kill", "monitor"}
REWARD_SECTION = re.compile(r"(?ms)^## Reward\s*$.*?(?=^## |\Z)")
YAML_FENCE = re.compile(r"(?ms)```yaml\s*\n(.*?)```")


def slug(value: Any, fallback: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", str(value or "").strip().lower())
    return normalized.strip("-") or fallback


def row_fingerprint(row: dict[str, Any]) -> str:
    payload = {
        key: value
        for key, value in row.items()
        if key not in {"reward_id", *REMOVED_FIELDS}
    }
    encoded = json.dumps(payload, sort_keys=True, default=str, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def assign_reward_ids(rows: list[dict[str, Any]]) -> dict[int, str]:
    grouped: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for index, row in enumerate(rows):
        existing = str(row.get("reward_id") or "").strip()
        base = existing or "-".join(
            (
                slug(row.get("kpi_id"), "reward"),
                slug(row.get("check_in_at"), "unscheduled"),
            )
        )
        grouped[base].append((row_fingerprint(row), index))

    assigned: dict[int, str] = {}
    for base, candidates in sorted(grouped.items()):
        for position, (_, index) in enumerate(sorted(candidates), 1):
            assigned[index] = base if position == 1 else f"{base}-{position}"
    return assigned


def canonical_reward(row: dict[str, Any], reward_id: str) -> dict[str, Any]:
    raw_decision = str(row.get("decision") or "").strip().lower()
    decision = raw_decision if raw_decision in VALID_DECISIONS else ""
    evidence_refs = row.get("evidence_refs")
    if not isinstance(evidence_refs, list):
        evidence_refs = []
    canonical: dict[str, Any] = {
        "reward_id": reward_id,
        "kpi_id": row.get("kpi_id"),
        "expected_reward": row.get("expected_reward"),
        "check_in_at": row.get("check_in_at"),
        "actual_result": row.get("actual_result"),
        "decision": decision or None,
        "evaluated_at": row.get("evaluated_at"),
        "evaluation_key": row.get("evaluation_key"),
        "supersedes_evaluation_key": row.get("supersedes_evaluation_key"),
        "evidence_refs": [str(item) for item in evidence_refs if str(item).strip()],
    }
    # Preserve non-score extensions for a lossless one-time migration. Their
    # owning contract can remove them separately; current Reward readers ignore
    # them.
    for key, value in row.items():
        if key not in CANONICAL_FIELDS and key not in REMOVED_FIELDS:
            canonical[key] = value
    return canonical


def migrate_markdown(markdown: str) -> tuple[str, dict[str, int]]:
    section_match = REWARD_SECTION.search(markdown)
    if not section_match:
        return markdown, {"rows": 0, "unresolved": 0, "removed_scores": 0}
    section = section_match.group(0)
    fence_match = YAML_FENCE.search(section)
    if not fence_match:
        return markdown, {"rows": 0, "unresolved": 0, "removed_scores": 0}
    try:
        payload = yaml.safe_load(fence_match.group(1)) or {}
    except yaml.YAMLError:
        return markdown, {"rows": 0, "unresolved": 0, "removed_scores": 0}
    if not isinstance(payload, dict) or not isinstance(payload.get("kpi_rewards"), list):
        return markdown, {"rows": 0, "unresolved": 0, "removed_scores": 0}

    rows = [row for row in payload["kpi_rewards"] if isinstance(row, dict)]
    assigned = assign_reward_ids(rows)
    removed_scores = sum(bool(REMOVED_FIELDS.intersection(row)) for row in rows)
    migrated = [canonical_reward(row, assigned[index]) for index, row in enumerate(rows)]
    next_payload = {**payload, "kpi_rewards": migrated}
    rendered = yaml.safe_dump(next_payload, sort_keys=False, allow_unicode=True).rstrip()
    next_section = (
        section[: fence_match.start()]
        + "```yaml\n"
        + rendered
        + "\n```"
        + section[fence_match.end() :]
    )
    next_markdown = markdown[: section_match.start()] + next_section + markdown[section_match.end() :]
    return next_markdown, {
        "rows": len(migrated),
        "unresolved": sum(not row.get("decision") for row in migrated),
        "removed_scores": removed_scores,
    }


def ticket_paths(project_root: Path) -> list[Path]:
    return sorted(
        {
            *project_root.glob("tickets/TASK-*/ticket.md"),
            *project_root.glob("tickets/archive/TASK-*/ticket.md"),
        }
    )


def migrate_project(project_root: Path, *, write: bool) -> dict[str, Any]:
    changed: list[str] = []
    rows = unresolved = removed_scores = 0
    for path in ticket_paths(project_root):
        original = path.read_text(encoding="utf-8")
        migrated, stats = migrate_markdown(original)
        rows += stats["rows"]
        unresolved += stats["unresolved"]
        removed_scores += stats["removed_scores"]
        if migrated == original:
            continue
        changed.append(str(path.relative_to(project_root)))
        if write:
            path.write_text(migrated, encoding="utf-8")
    return {
        "write": write,
        "changed": changed,
        "changed_count": len(changed),
        "reward_rows": rows,
        "unresolved_rows": unresolved,
        "score_rows_removed": removed_scores,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = migrate_project(Path(args.project_root).resolve(), write=args.write)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
