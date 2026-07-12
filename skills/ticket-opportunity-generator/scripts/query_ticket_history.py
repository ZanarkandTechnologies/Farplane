#!/usr/bin/env python3
"""Project compact ticket history for adaptive next-wave planning."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--sort", choices=("recent", "oldest"), default="recent")
    parser.add_argument("--origin", action="append", choices=("ai_planned", "direct_or_unknown"))
    parser.add_argument("--area", action="append")
    parser.add_argument("--status", action="append")
    parser.add_argument("--kpi", action="append")
    parser.add_argument("--reward-decision", action="append", choices=("pending", "accept", "kill", "monitor"))
    parser.add_argument("--active-only", action="store_true", help="Exclude tickets/archive history.")
    return parser.parse_args()


def read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def read_frontmatter(markdown: str) -> dict[str, Any]:
    if not markdown.startswith("---\n"):
        return {}
    parts = markdown.split("---\n", 2)
    if len(parts) < 3:
        return {}
    try:
        loaded = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def heading_section(markdown: str, heading: str) -> str:
    lines = markdown.splitlines()
    target = f"## {heading}"
    for start, line in enumerate(lines):
        if line.strip() != target:
            continue
        end = len(lines)
        for index in range(start + 1, len(lines)):
            if lines[index].startswith("## "):
                end = index
                break
        return "\n".join(lines[start + 1 : end]).strip()
    return ""


def first_paragraph(section: str) -> str:
    paragraphs = [part.strip() for part in section.split("\n\n") if part.strip()]
    for paragraph in paragraphs:
        if not paragraph.startswith("```"):
            return " ".join(line.strip() for line in paragraph.splitlines()).strip()
    return ""


def fenced_yaml(section: str) -> dict[str, Any]:
    start = section.find("```yaml")
    if start < 0:
        return {}
    body_start = section.find("\n", start)
    end = section.find("```", body_start + 1)
    if body_start < 0 or end < 0:
        return {}
    try:
        loaded = yaml.safe_load(section[body_start + 1 : end]) or {}
    except yaml.YAMLError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def compact_rewards(markdown: str) -> list[dict[str, Any]]:
    payload = fenced_yaml(heading_section(markdown, "Reward"))
    raw_rows = payload.get("kpi_rewards")
    if not isinstance(raw_rows, list):
        return []
    rows: list[dict[str, Any]] = []
    for raw in raw_rows:
        if not isinstance(raw, dict):
            continue
        decision = str(raw.get("decision") or "").strip().lower() or "pending"
        rows.append(
            {
                "reward_id": str(raw.get("reward_id") or "").strip(),
                "kpi_id": str(raw.get("kpi_id") or "").strip(),
                "expected_reward": raw.get("expected_reward"),
                "actual_result": raw.get("actual_result"),
                "decision": decision,
                "check_in_at": scalar_text(raw.get("check_in_at")),
                "evaluated_at": scalar_text(raw.get("evaluated_at")),
                "evidence_refs": raw.get("evidence_refs") if isinstance(raw.get("evidence_refs"), list) else [],
            }
        )
    return rows


def scalar_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return str(value).strip()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            loaded = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(loaded, dict):
            rows.append(loaded)
    return rows


def ai_planned_ticket_ids(decisions: list[dict[str, Any]]) -> set[str]:
    ids: set[str] = set()
    for row in decisions:
        receipt = row.get("pulse_receipt") if isinstance(row.get("pulse_receipt"), dict) else {}
        action = str(row.get("action") or receipt.get("mode") or "").strip()
        admitted = receipt.get("admitted") if isinstance(receipt.get("admitted"), list) else []
        if action == "plan_next_wave":
            ids.update(str(ticket_id).strip() for ticket_id in admitted if str(ticket_id).strip())
            ticket_id = str(row.get("ticket_id") or "").strip()
            if ticket_id:
                ids.add(ticket_id)
    return ids


def planner_areas_by_ticket(decisions: list[dict[str, Any]]) -> dict[str, str]:
    """Read the planner-selected area recorded beside admitted ticket IDs."""

    mapping: dict[str, str] = {}
    for row in decisions:
        receipt = row.get("pulse_receipt") if isinstance(row.get("pulse_receipt"), dict) else {}
        planner_call = receipt.get("planner_call") if isinstance(receipt.get("planner_call"), dict) else {}
        for owner in (row, planner_call):
            specs = owner.get("admitted_specs") if isinstance(owner.get("admitted_specs"), list) else []
            for spec in specs:
                if not isinstance(spec, dict):
                    continue
                ticket_id = str(spec.get("ticket_id") or "").strip()
                area_id = str(spec.get("area_id") or "").strip()
                if ticket_id and area_id:
                    mapping[ticket_id] = area_id
    return mapping


def area_metric_map(harness: dict[str, Any]) -> dict[str, set[str]]:
    areas = harness.get("areas") if isinstance(harness.get("areas"), dict) else {}
    mapping: dict[str, set[str]] = {}
    for area_id, area in areas.items():
        if not isinstance(area, dict):
            continue
        refs = area.get("metric_refs") if isinstance(area.get("metric_refs"), list) else []
        for ref in refs:
            metric_id = str(ref.get("metric_id") if isinstance(ref, dict) else ref).strip()
            if metric_id:
                mapping.setdefault(metric_id, set()).add(str(area_id))
    return mapping


def ticket_paths(root: Path, active_only: bool) -> list[Path]:
    paths = list((root / "tickets").glob("TASK-*/ticket.md"))
    if not active_only:
        paths.extend((root / "tickets" / "archive").glob("TASK-*/ticket.md"))
    return sorted(set(path.resolve() for path in paths))


def timestamp_key(row: dict[str, Any]) -> tuple[datetime, str]:
    raw = str(row.get("updated_at") or row.get("created_at") or "").strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        parsed = datetime.min.replace(tzinfo=timezone.utc)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc), str(row.get("ticket_id") or "")


def build_history(
    root: Path,
    *,
    limit: int = 20,
    sort: str = "recent",
    origins: set[str] | None = None,
    areas: set[str] | None = None,
    statuses: set[str] | None = None,
    kpis: set[str] | None = None,
    reward_decisions: set[str] | None = None,
    active_only: bool = False,
) -> dict[str, Any]:
    root = root.resolve()
    harness = read_yaml(root / "farplane" / "harness.yaml")
    metric_areas = area_metric_map(harness)
    decisions = load_jsonl(root / ".farplane" / "automation" / "decisions.jsonl")
    ai_ids = ai_planned_ticket_ids(decisions)
    planner_areas = planner_areas_by_ticket(decisions)
    rows: list[dict[str, Any]] = []
    for path in ticket_paths(root, active_only):
        markdown = path.read_text(encoding="utf-8", errors="replace")
        frontmatter = read_frontmatter(markdown)
        ticket_id = str(frontmatter.get("ticket_id") or path.parent.name).strip()
        rewards = compact_rewards(markdown)
        kpi_ids = sorted({row["kpi_id"] for row in rewards if row["kpi_id"]})
        selected_area = planner_areas.get(ticket_id)
        area_refs = (
            [selected_area]
            if selected_area
            else sorted({area for kpi_id in kpi_ids for area in metric_areas.get(kpi_id, set())})
        )
        if not area_refs:
            area_refs = ["unknown"]
        origin = "ai_planned" if ticket_id in ai_ids else "direct_or_unknown"
        try:
            relative = path.relative_to(root).as_posix()
        except ValueError:
            relative = str(path)
        rows.append(
            {
                "ticket_id": ticket_id,
                "path": relative,
                "title": str(frontmatter.get("title") or "").strip(),
                "status": str(frontmatter.get("status") or "").strip().lower(),
                "priority": str(frontmatter.get("priority") or "medium").strip().lower(),
                "created_at": scalar_text(frontmatter.get("created_at")),
                "updated_at": scalar_text(frontmatter.get("updated_at")),
                "creation_origin": origin,
                "creation_reason": first_paragraph(heading_section(markdown, "Summary")),
                "area_refs": area_refs,
                "area_derivation": "planner_receipt" if selected_area else "kpi_binding_fallback",
                "kpi_ids": kpi_ids,
                "rewards": rewards,
            }
        )

    input_count = len(rows)
    if origins:
        rows = [row for row in rows if row["creation_origin"] in origins]
    if areas:
        rows = [row for row in rows if areas.intersection(row["area_refs"])]
    if statuses:
        rows = [row for row in rows if row["status"] in statuses]
    if kpis:
        rows = [row for row in rows if kpis.intersection(row["kpi_ids"])]
    if reward_decisions:
        rows = [
            row for row in rows
            if any(reward["decision"] in reward_decisions for reward in row["rewards"])
        ]
    filtered_count = len(rows)
    rows.sort(key=timestamp_key, reverse=sort == "recent")
    rows = rows[: max(0, limit)]
    return {
        "schema": "farplane.ticket_history_query.v1",
        "project_root": str(root),
        "query": {
            "limit": max(0, limit),
            "sort": sort,
            "origins": sorted(origins or []),
            "areas": sorted(areas or []),
            "statuses": sorted(statuses or []),
            "kpis": sorted(kpis or []),
            "reward_decisions": sorted(reward_decisions or []),
            "active_only": active_only,
        },
        "receipt": {
            "input_count": input_count,
            "filtered_count": filtered_count,
            "returned_count": len(rows),
        },
        "area_distribution": dict(sorted(Counter(area for row in rows for area in row["area_refs"]).items())),
        "origin_distribution": dict(sorted(Counter(row["creation_origin"] for row in rows).items())),
        "rows": rows,
    }


def main() -> int:
    args = parse_args()
    payload = build_history(
        Path(args.project_root),
        limit=args.limit,
        sort=args.sort,
        origins=set(args.origin or []),
        areas=set(args.area or []),
        statuses={value.lower() for value in args.status or []},
        kpis=set(args.kpi or []),
        reward_decisions=set(args.reward_decision or []),
        active_only=args.active_only,
    )
    print(json.dumps(payload, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
