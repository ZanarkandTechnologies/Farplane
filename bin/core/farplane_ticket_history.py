#!/usr/bin/env python3
"""Project compact ticket history for adaptive planning and review."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import yaml

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
    for paragraph in (part.strip() for part in section.split("\n\n")):
        if paragraph and not paragraph.startswith("```"):
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


def scalar_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return str(value).strip()


def compact_rewards(markdown: str) -> list[dict[str, Any]]:
    payload = fenced_yaml(heading_section(markdown, "Reward"))
    raw_rows = payload.get("kpi_rewards")
    if not isinstance(raw_rows, list):
        return []
    rows: list[dict[str, Any]] = []
    for raw in raw_rows:
        if not isinstance(raw, dict):
            continue
        rows.append(
            {
                "reward_id": str(raw.get("reward_id") or "").strip(),
                "kpi_id": str(raw.get("kpi_id") or "").strip(),
                "expected_reward": raw.get("expected_reward"),
                "actual_result": raw.get("actual_result"),
                "decision": str(raw.get("decision") or "").strip().lower() or "pending",
                "check_in_at": scalar_text(raw.get("check_in_at")),
                "evaluated_at": scalar_text(raw.get("evaluated_at")),
                "evidence_refs": raw.get("evidence_refs")
                if isinstance(raw.get("evidence_refs"), list)
                else [],
            }
        )
    return rows


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
        planner_call = receipt.get("planner_call") if isinstance(receipt.get("planner_call"), dict) else {}
        action = str(row.get("action") or receipt.get("mode") or "").strip()
        admitted = receipt.get("admitted") if isinstance(receipt.get("admitted"), list) else []
        if action in {"plan_next_wave", "materialize_reserved_wave"}:
            ids.update(str(ticket_id).strip() for ticket_id in admitted if str(ticket_id).strip())
            for owner in (row, receipt, planner_call):
                for key in ("admitted_skill_calls", "admitted_specs"):
                    admissions = owner.get(key) if isinstance(owner.get(key), list) else []
                    ids.update(
                        str(admission.get("ticket_id") or "").strip()
                        for admission in admissions
                        if isinstance(admission, dict)
                        and str(admission.get("ticket_id") or "").strip()
                    )
            ticket_id = str(row.get("ticket_id") or "").strip()
            if ticket_id:
                ids.add(ticket_id)
    return ids


def planner_metadata_by_ticket(decisions: list[dict[str, Any]]) -> dict[str, dict[str, str]]:
    mapping: dict[str, dict[str, str]] = {}
    for row in decisions:
        receipt = row.get("pulse_receipt") if isinstance(row.get("pulse_receipt"), dict) else {}
        planner_call = receipt.get("planner_call") if isinstance(receipt.get("planner_call"), dict) else {}
        for owner in (row, receipt, planner_call):
            calls = owner.get("admitted_skill_calls") if isinstance(owner.get("admitted_skill_calls"), list) else []
            for call in calls:
                if not isinstance(call, dict):
                    continue
                ticket_id = str(call.get("ticket_id") or "").strip()
                skill_ref = str(call.get("skill_ref") or "").strip()
                area_id = str(call.get("area_id") or "").strip()
                if ticket_id:
                    metadata = mapping.setdefault(ticket_id, {})
                    if skill_ref:
                        metadata["skill_ref"] = skill_ref
                        metadata["skill_derivation"] = "planner_skill_call"
                    if area_id:
                        metadata["area_id"] = area_id
                        metadata["area_derivation"] = "planner_skill_call"

            # Explicit read-only projection for pre-v2 planner history.
            specs = owner.get("admitted_specs") if isinstance(owner.get("admitted_specs"), list) else []
            for spec in specs:
                if not isinstance(spec, dict):
                    continue
                ticket_id = str(spec.get("ticket_id") or "").strip()
                area_id = str(spec.get("area_id") or "").strip()
                if ticket_id:
                    metadata = mapping.setdefault(ticket_id, {})
                    if area_id and "area_id" not in metadata:
                        metadata["area_id"] = area_id
                        metadata["area_derivation"] = "historical_admitted_spec"
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


def closed_ticket_rows(root: Path) -> tuple[list[dict[str, Any]], list[str]]:
    """Read the compact local projection for tickets archived as GitHub issues."""

    path = root / "tickets" / "archive-index.jsonl"
    rows: list[dict[str, Any]] = []
    diagnostics: list[str] = []
    if not path.exists():
        return rows, diagnostics
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8", errors="replace").splitlines(), 1
    ):
        if not line.strip():
            continue
        try:
            loaded = json.loads(line)
        except json.JSONDecodeError:
            diagnostics.append(f"archive_index_invalid_json:{line_number}")
            continue
        if not isinstance(loaded, dict):
            diagnostics.append(f"archive_index_invalid_row:{line_number}")
            continue
        ticket_id = str(loaded.get("ticket_id") or "").strip().upper()
        issue_url = str(loaded.get("github_issue_url") or "").strip()
        if (
            not ticket_id
            or str(loaded.get("storage") or "") != "github_issue"
            or str(loaded.get("status") or "").strip().lower() != "done"
            or not issue_url
        ):
            diagnostics.append(f"archive_index_invalid_locator:{line_number}")
            continue
        rows.append({**loaded, "ticket_id": ticket_id, "github_issue_url": issue_url})
    return rows, diagnostics


def timestamp_key(row: dict[str, Any]) -> tuple[datetime, str]:
    raw = str(
        row.get("updated_at") or row.get("closed_at") or row.get("created_at") or ""
    ).strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        parsed = datetime.min.replace(tzinfo=timezone.utc)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc), str(row.get("ticket_id") or "")


def build_ticket_history(
    root: Path,
    *,
    limit: int | None = 20,
    sort: str = "recent",
    origins: set[str] | None = None,
    areas: set[str] | None = None,
    skills: set[str] | None = None,
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
    planner_metadata = planner_metadata_by_ticket(decisions)
    rows: list[dict[str, Any]] = []
    diagnostics: list[str] = []
    for path in ticket_paths(root, active_only):
        markdown = path.read_text(encoding="utf-8", errors="replace")
        frontmatter = read_frontmatter(markdown)
        ticket_id = str(frontmatter.get("ticket_id") or path.parent.name).strip()
        rewards = compact_rewards(markdown)
        kpi_ids = sorted({row["kpi_id"] for row in rewards if row["kpi_id"]})
        selected_area = planner_metadata.get(ticket_id, {}).get("area_id")
        selected_skill = planner_metadata.get(ticket_id, {}).get("skill_ref") or "unknown"
        area_refs = (
            [selected_area]
            if selected_area
            else sorted({area for kpi_id in kpi_ids for area in metric_areas.get(kpi_id, set())})
        )
        if not area_refs:
            area_refs = ["unknown"]
        try:
            relative = path.relative_to(root).as_posix()
        except ValueError:
            relative = str(path)
        rows.append(
            {
                "ticket_id": ticket_id,
                "path": relative,
                "storage": "local_archive" if "/archive/" in f"/{relative}" else "local_active",
                "title": str(frontmatter.get("title") or "").strip(),
                "status": str(frontmatter.get("status") or "").strip().lower(),
                "priority": str(frontmatter.get("priority") or "medium").strip().lower(),
                "created_at": scalar_text(frontmatter.get("created_at")),
                "updated_at": scalar_text(frontmatter.get("updated_at")),
                "creation_origin": "ai_planned" if ticket_id in ai_ids else "direct_or_unknown",
                "creation_reason": first_paragraph(heading_section(markdown, "Summary")),
                "area_refs": area_refs,
                "area_derivation": planner_metadata.get(ticket_id, {}).get("area_derivation")
                if selected_area
                else "kpi_binding_fallback",
                "skill_ref": selected_skill,
                "skill_derivation": planner_metadata.get(ticket_id, {}).get(
                    "skill_derivation", "unknown"
                ),
                "kpi_ids": kpi_ids,
                "rewards": rewards,
            }
        )

    if not active_only:
        indexed_rows, index_diagnostics = closed_ticket_rows(root)
        diagnostics.extend(index_diagnostics)
        local_ids = {str(row.get("ticket_id") or "") for row in rows}
        indexed_by_id: dict[str, dict[str, Any]] = {}
        conflicting_ids: set[str] = set()
        for indexed in indexed_rows:
            ticket_id = str(indexed["ticket_id"])
            if ticket_id in conflicting_ids:
                continue
            prior = indexed_by_id.get(ticket_id)
            if prior is not None and str(prior.get("github_issue_url")) != str(
                indexed.get("github_issue_url")
            ):
                diagnostics.append(f"archive_index_conflicting_ticket:{ticket_id}")
                indexed_by_id.pop(ticket_id, None)
                conflicting_ids.add(ticket_id)
                continue
            indexed_by_id[ticket_id] = indexed
        for ticket_id, indexed in indexed_by_id.items():
            if ticket_id in local_ids:
                continue
            selected_area = planner_metadata.get(ticket_id, {}).get("area_id")
            selected_skill = planner_metadata.get(ticket_id, {}).get("skill_ref") or "unknown"
            rows.append(
                {
                    "ticket_id": ticket_id,
                    "path": "tickets/archive-index.jsonl",
                    "storage": "github_issue",
                    "github_issue_url": str(indexed.get("github_issue_url") or ""),
                    "github_issue_number": indexed.get("github_issue_number"),
                    "media_comment_urls": indexed.get("media_comment_urls")
                    if isinstance(indexed.get("media_comment_urls"), list)
                    else [],
                    "event_id": str(indexed.get("event_id") or ""),
                    "runs": indexed.get("runs") if isinstance(indexed.get("runs"), list) else [],
                    "closed_at": scalar_text(indexed.get("closed_at")),
                    "title": str(indexed.get("title") or "").strip(),
                    "status": "done",
                    "priority": "medium",
                    "created_at": "",
                    "updated_at": scalar_text(indexed.get("closed_at")),
                    "creation_origin": "ai_planned" if ticket_id in ai_ids else "direct_or_unknown",
                    "creation_reason": "",
                    "area_refs": [selected_area] if selected_area else ["unknown"],
                    "area_derivation": planner_metadata.get(ticket_id, {}).get(
                        "area_derivation", "unknown"
                    ),
                    "skill_ref": selected_skill,
                    "skill_derivation": planner_metadata.get(ticket_id, {}).get(
                        "skill_derivation", "unknown"
                    ),
                    "kpi_ids": [],
                    "rewards": [],
                }
            )

    input_count = len(rows)
    if origins:
        rows = [row for row in rows if row["creation_origin"] in origins]
    if areas:
        rows = [row for row in rows if areas.intersection(row["area_refs"])]
    if skills:
        rows = [row for row in rows if row["skill_ref"] in skills]
    if statuses:
        rows = [row for row in rows if row["status"] in statuses]
    if kpis:
        rows = [row for row in rows if kpis.intersection(row["kpi_ids"])]
    if reward_decisions:
        rows = [
            row
            for row in rows
            if any(reward["decision"] in reward_decisions for reward in row["rewards"])
        ]
    filtered_count = len(rows)
    rows.sort(key=timestamp_key, reverse=sort == "recent")
    effective_limit = None if limit is None else max(0, limit)
    if effective_limit is not None:
        rows = rows[:effective_limit]
    return {
        "schema": "farplane.ticket_history_query.v2",
        "project_root": str(root),
        "query": {
            "limit": "all" if effective_limit is None else effective_limit,
            "sort": sort,
            "origins": sorted(origins or []),
            "areas": sorted(areas or []),
            "skills": sorted(skills or []),
            "statuses": sorted(statuses or []),
            "kpis": sorted(kpis or []),
            "reward_decisions": sorted(reward_decisions or []),
            "active_only": active_only,
        },
        "receipt": {
            "input_count": input_count,
            "filtered_count": filtered_count,
            "returned_count": len(rows),
            "exhausted": len(rows) == filtered_count,
        },
        "diagnostics": diagnostics,
        "area_distribution": dict(
            sorted(Counter(area for row in rows for area in row["area_refs"]).items())
        ),
        "skill_distribution": dict(
            sorted(Counter(row["skill_ref"] for row in rows).items())
        ),
        "origin_distribution": dict(
            sorted(Counter(row["creation_origin"] for row in rows).items())
        ),
        "rows": rows,
    }


def add_history_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--project-root", default=".")
    limit_group = parser.add_mutually_exclusive_group()
    limit_group.add_argument("--limit", type=int, default=20)
    limit_group.add_argument(
        "--all",
        action="store_true",
        dest="all_results",
        help="return every matched row with an exhaustion receipt",
    )
    parser.add_argument("--sort", choices=("recent", "oldest"), default="recent")
    parser.add_argument("--origin", action="append", choices=("ai_planned", "direct_or_unknown"))
    parser.add_argument("--area", action="append")
    parser.add_argument("--skill", action="append")
    parser.add_argument("--status", action="append")
    parser.add_argument("--kpi", action="append")
    parser.add_argument(
        "--reward-decision",
        action="append",
        choices=("pending", "accept", "kill", "monitor"),
    )
    parser.add_argument("--active-only", action="store_true")
    parser.add_argument("--json", action="store_true")


def history_from_args(args: argparse.Namespace) -> dict[str, Any]:
    return build_ticket_history(
        Path(args.project_root),
        limit=None if getattr(args, "all_results", False) else args.limit,
        sort=args.sort,
        origins=set(args.origin or []),
        areas=set(args.area or []),
        skills=set(args.skill or []),
        statuses={value.lower() for value in args.status or []},
        kpis=set(args.kpi or []),
        reward_decisions=set(args.reward_decision or []),
        active_only=args.active_only,
    )


def run_history(args: argparse.Namespace) -> int:
    payload = history_from_args(args)
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True, default=str))
        return 0
    receipt = payload["receipt"]
    print(
        "farplane ticket history: "
        f"{receipt['returned_count']} returned / {receipt['filtered_count']} matched / "
        f"{receipt['input_count']} scanned"
    )
    for row in payload["rows"]:
        decisions = ",".join(reward["decision"] for reward in row["rewards"]) or "no-reward"
        print(f"- {row['ticket_id']} [{row['status']}] {row['title']} ({decisions})")
    return 0
