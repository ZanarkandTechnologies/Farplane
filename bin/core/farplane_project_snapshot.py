#!/usr/bin/env python3
"""Compile a read-only Farplane project snapshot for UI and intervals."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import tomllib
from datetime import date as date_type
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TypedDict

import yaml

try:
    from farplane_metric_schema import batch_path, read_metric_batches
except ImportError:  # pragma: no cover - package import path used by tests
    from bin.core.farplane_metric_schema import batch_path, read_metric_batches

try:
    from farplane_reports import build_report_registry
except ImportError:  # pragma: no cover - package import path used by tests
    from bin.core.farplane_reports import build_report_registry


PROJECT_SNAPSHOT_PATH = Path(".farplane/project/ui/latest.json")
DAILY_METRICS_DIR = Path(".farplane/metrics/daily")
REWARD_CONTRACT = "terminal_evidence_v1"
CONTENT_LEDGER_PATH = Path(".farplane/content/ledger.jsonl")
FEED_SCOUT_LATEST_FEED_PATH = Path(".farplane/feed-scout/daily/latest.json")
FEED_SCOUT_LATEST_REPORT_PATH = Path(".farplane/reports/feed-scout/latest.json")


class SourceGap(TypedDict):
    id: str
    severity: str
    owner: str
    message: str
    source_ref: dict[str, Any]


PRIMITIVE_CATALOG: dict[str, dict[str, Any]] = {
    "ticket_count_by_kpi": {
        "primitive_id": "ticket_count_by_kpi",
        "provider": "mechanical",
        "owner": "farplane-core",
        "command": "farplane metrics primitives --project-root <project> --date <YYYY-MM-DD> --json",
        "store_to": ".farplane/metrics/daily/<YYYY-MM-DD>.json",
        "required_inputs": ["tickets/**/ticket.md", "Reward.kpi_rewards[]"],
        "emits": ["value", "status", "payload.tickets", "payload.gaps"],
        "source_gap_policy": "Unrealized or evidence-incomplete Reward rows remain source gaps; terminal kills are known zero and declarations never count as accepted value.",
    },
    "kpi_attributed_ticket_ratio": {
        "primitive_id": "kpi_attributed_ticket_ratio",
        "provider": "mechanical",
        "owner": "farplane-core",
        "command": "farplane metrics primitives --project-root <project> --date <YYYY-MM-DD> --json",
        "store_to": ".farplane/metrics/daily/<YYYY-MM-DD>.json",
        "required_inputs": ["tickets/**/ticket.md", "Reward.kpi_rewards[]"],
        "emits": ["value", "status", "payload.attributed", "payload.total_touched"],
        "source_gap_policy": "Empty windows produce available zero readings, not source gaps.",
    },
    "codex_thread_usage": {
        "primitive_id": "codex_thread_usage",
        "provider": "mechanical",
        "owner": "farplane-core",
        "command": "farplane metrics primitives --project-root <project> --date <YYYY-MM-DD> --json",
        "store_to": ".farplane/metrics/observations/codex_thread_usage/<YYYY-MM-DD>.json",
        "required_inputs": ["~/.codex/sqlite/state_5.sqlite", "~/.codex/sessions/**/*.jsonl"],
        "emits": ["thread_count", "turn_count", "tokens", "span_minutes", "source_gaps"],
        "source_gap_policy": "Emit source_gap when local Codex stores are absent or unreadable.",
    },
    "ai_burn_estimate": {
        "primitive_id": "ai_burn_estimate",
        "provider": "mechanical",
        "owner": "farplane-core",
        "command": "farplane metrics primitives --project-root <project> --date <YYYY-MM-DD> --monthly-spend <amount> --json",
        "store_to": ".farplane/metrics/daily/<YYYY-MM-DD>.json",
        "required_inputs": ["codex_thread_usage", "explicit spend model"],
        "emits": ["value", "status", "payload.mode", "payload.gaps"],
        "source_gap_policy": "Emit source_gap when no CLI or bindings spend model is configured.",
    },
    "content_views_total": {
        "primitive_id": "content_views_total",
        "provider": "farplane-core",
        "owner": "farplane-core",
        "command": "python3 bin/farplane.py metrics primitives --project-root <project> --date <YYYY-MM-DD>",
        "store_to": ".farplane/metrics/observations/content_views_total/<YYYY-MM-DD>.json",
        "required_inputs": [".farplane/metrics/observations/*/<YYYY-MM-DD>.json"],
        "emits": ["evidence_distribution_reach", "payload.components", "payload.missing_components"],
        "source_gap_policy": "Emit source_gap when no same-day platform view component observations exist.",
    },
    "project_adoption": {
        "primitive_id": "project_adoption",
        "provider": "farplane-core",
        "owner": "farplane-core",
        "command": "python3 bin/farplane.py metrics primitives --project-root <project> --date <YYYY-MM-DD>",
        "store_to": ".farplane/metrics/observations/project_adoption/<YYYY-MM-DD>.json",
        "required_inputs": ["farplane/manifest.json", "nearby project farplane/manifest.json files", "nearby .farplane/automation/decisions.jsonl"],
        "emits": ["activated_external_projects", "payload.projects", "payload.excluded"],
        "source_gap_policy": "Emit source_gap when the standard manifest lacks a spec version; drifted or not-yet-activated nearby projects are excluded with reasons.",
    },
    "planner_ticket_quality": {
        "primitive_id": "planner_ticket_quality",
        "provider": "farplane-core",
        "owner": "farplane-core",
        "command": "python3 bin/farplane.py metrics primitives --project-root <project> --date <YYYY-MM-DD>",
        "store_to": ".farplane/metrics/observations/planner_ticket_quality/<YYYY-MM-DD>.json",
        "required_inputs": ["tickets/**/ticket.md", "Reward.kpi_rewards[]"],
        "emits": ["rejected_ai_ticket_count", "payload.tickets"],
        "source_gap_policy": "Empty windows emit available zero; rejected reward-bearing tickets retain ticket refs in payload.",
    },
    "ticket_thread_association_backfill": {
        "primitive_id": "ticket_thread_association_backfill",
        "provider": "mechanical",
        "owner": "farplane-core",
        "command": "farplane metrics primitives --project-root <project> --date <YYYY-MM-DD> --json",
        "store_to": ".farplane/state/ticket-thread-associations.jsonl",
        "required_inputs": [".farplane/mine/runs/**/input.json"],
        "emits": ["ticket_id", "thread_id", "source", "observed_at", "confidence"],
        "source_gap_policy": "Mine backfill emits confidence=completion_only and cannot satisfy post-start intervention metrics.",
    },
    "autonomy_time_feedback": {
        "primitive_id": "autonomy_time_feedback",
        "provider": "interval-update",
        "owner": "farplane-core",
        "command": "python3 skills/interval-update/scripts/metric_refresh.py autonomy-time-ratio --runtime-dir .farplane --date <YYYY-MM-DD>",
        "store_to": ".farplane/metrics/observations/autonomy_time_feedback/<YYYY-MM-DD>.json",
        "required_inputs": [".farplane/events/*.jsonl", ".farplane/automation/spawned-threads.jsonl", ".farplane/automation/rewards.jsonl"],
        "emits": ["auto_time_ratio", "human_attention_minutes_estimated", "autonomous_worker_elapsed_minutes"],
        "source_gap_policy": "Emit source_gap only when all runtime feedback sources are missing.",
    },
    "ticket_intervention_feedback": {
        "primitive_id": "ticket_intervention_feedback",
        "provider": "interval-update",
        "owner": "farplane-core",
        "command": "python3 skills/interval-update/scripts/metric_refresh.py ticket-intervention-metrics --ticket-dir tickets --runtime-dir .farplane --date <YYYY-MM-DD>",
        "store_to": ".farplane/metrics/observations/ticket_intervention_feedback/<YYYY-MM-DD>.json",
        "required_inputs": ["tickets/**/ticket.md", ".farplane/state/ticket-thread-associations.jsonl", ".farplane/events/*.jsonl"],
        "emits": ["auto_completion_rate", "intervention_free_ticket_count", "ticket_intervention_turn_count"],
        "source_gap_policy": "Emit source_gap when no completed ticket can be associated with its execution thread.",
    },
    "manual_source_gap": {
        "primitive_id": "manual_source_gap",
        "provider": "manual_or_external",
        "owner": "source-owner",
        "command": "none",
        "store_to": ".farplane/metrics/daily/<YYYY-MM-DD>.json",
        "required_inputs": ["provider-specific source"],
        "emits": ["source_gap"],
        "source_gap_policy": "Render unsupported external/provider recipes as explicit gaps until their owner writes readings.",
    },
}

DEFAULT_METRIC_DESCRIPTIONS: dict[str, str] = {
    "accepted_evidence_cycles": "Daily count of done tickets with an evidence-backed terminal accept Reward decision for this KPI and TAS-A/pass review evidence.",
    "accepted_harness_improvements": "Daily count of done tickets with an evidence-backed terminal accept Reward decision for this KPI and TAS-A/pass review evidence.",
    "auto_time_ratio": "Autonomous worker elapsed minutes divided by estimated human attention minutes for the day.",
    "evidence_distribution_reach": "Daily distribution reach rollup from available X, Instagram, GitHub, and content-ledger view readings.",
    "latest_eval_pass_rate": "Most recent eval summary pass rate available for the snapshot window.",
    "github_views": "Daily GitHub traffic views for the Farplane repository when traffic API access is available.",
    "auto_completion_rate": "Completed associated tickets with zero post-start human intervention turns divided by all completed associated tickets for the day.",
    "intervention_free_ticket_count": "Daily count of completed associated tickets with zero human turns after execution start.",
    "ticket_intervention_turn_count": "Daily count of human turns after execution start and before completion across completed associated tickets.",
    "todo_unclaimed_ticket_count": "Current count of unclaimed status=todo tickets with satisfied dependencies.",
    "x_followers": "Current follower count for the configured Farplane X account.",
    "x_views": "Daily aggregate X views for posted content selected from the content ledger.",
    "x_likes": "Daily aggregate X likes for posted content selected from the content ledger.",
    "instagram_followers": "Current follower count for the configured Farplane Instagram account.",
    "instagram_views": "Daily aggregate Instagram views for posted content selected from the content ledger.",
    "instagram_likes": "Daily aggregate Instagram likes for posted content selected from the content ledger.",
    "instagram_comments": "Daily aggregate Instagram comments for posted content selected from the content ledger.",
    "instagram_shares": "Daily aggregate Instagram shares for posted content selected from the content ledger.",
    "instagram_saves": "Daily aggregate Instagram saves for posted content selected from the content ledger.",
    "instagram_reach": "Daily aggregate Instagram reached accounts for posted content selected from the content ledger.",
    "instagram_total_interactions": "Daily aggregate Instagram interactions for posted content selected from the content ledger.",
    "instagram_avg_watch_time": "Average watch time for selected Instagram Reel content when the account API returns watch-time fields.",
    "instagram_total_watch_time": "Total watch time for selected Instagram Reel content when the account API returns watch-time fields.",
    "instagram_retention_score": "Instagram Reel retention score from watch-time and duration data when those fields are available.",
    "posts_published": "Daily count of content ledger rows posted on the snapshot date.",
}


SHARED_SHAPES: dict[str, list[str]] = {
    "source_ref": ["path", "pointer?", "kind?"],
    "source_gap": ["id", "severity", "owner", "message", "source_ref"],
    "metric_ref": ["metric_id", "label?", "primitive_id?", "latest_status?", "source_gap_ids[]"],
    "metric_series": ["metric_id", "status", "current", "series[]", "target_hit?", "source_gaps[]"],
    "content_metric": ["content_id", "platform?", "external_id?", "metrics[]"],
    "feed_scout_item": ["title", "summary", "canonical_url?", "platform?", "entity_group_id?", "rank?", "signal?", "actionability?"],
    "metric_primitive": ["primitive_id", "provider", "owner", "command", "store_to", "required_inputs[]", "emits[]", "source_gap_policy"],
    "ticket_ref": [
        "ticket_id",
        "path",
        "title",
        "status",
        "priority",
        "kpi_rewards[]",
        "reward_rows[]",
    ],
    "report_card": [
        "id",
        "ref",
        "path",
        "kind",
        "created_at",
        "ui_summary",
        "parent_ref?",
        "children_refs[]",
        "source_ref",
    ],
}


def metric_description(metric_id: str, recipe: dict[str, Any]) -> str:
    raw_description = recipe.get("description") or recipe.get("tooltip")
    if isinstance(raw_description, str) and raw_description.strip():
        return raw_description.strip()
    return DEFAULT_METRIC_DESCRIPTIONS.get(
        metric_id,
        f"{str(recipe.get('label') or metric_id).strip()} reading collected by the metric refresh recipe.",
    )


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def parse_target(value: Any) -> float | None:
    if value is None:
        return None
    raw = str(value).strip()
    if not raw or raw.lower() in {"none", "null", "source_gap"}:
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def normalize_target_direction(value: Any) -> str:
    raw = str(value or "").strip().lower()
    if raw in {"below", "at_most", "max", "lte", "<=", "under", "minimize", "less_than_or_equal"}:
        return "below"
    return "above"


def parse_iso_datetime(value: Any) -> datetime | None:
    if not value:
        return None
    raw = str(value).strip()
    if not raw:
        return None
    try:
        if raw.endswith("Z"):
            raw = raw[:-1] + "+00:00"
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        try:
            parsed_date = date_type.fromisoformat(raw[:10])
        except ValueError:
            return None
        return datetime.combine(parsed_date, datetime.min.time(), tzinfo=timezone.utc)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def sha256_file(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def parse_frontmatter(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text:
        return {}
    raw = text.split("\n---\n", 1)[0][4:]
    try:
        loaded = yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def source_record(project_root: Path, rel_path: str, kind: str) -> dict[str, Any]:
    path = project_root / rel_path
    frontmatter = parse_frontmatter(path)
    updated_at = frontmatter.get("updated_at")
    return {
        "id": rel_path.replace("/", ":"),
        "path": rel_path,
        "kind": kind,
        "status": "loaded" if path.exists() else "missing",
        "hash": sha256_file(path),
        "updated_at": str(updated_at) if updated_at is not None else None,
    }


def markdown_heading_section(markdown: str, heading: str) -> str:
    target = f"## {heading}"
    lines = markdown.splitlines()
    start: int | None = None
    for index, line in enumerate(lines):
        if line.strip() == target:
            start = index + 1
            break
    if start is None:
        return ""
    end = len(lines)
    for index in range(start, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return "\n".join(lines[start:end]).strip()


def parse_fenced_yaml_from_section(section: str) -> dict[str, Any]:
    fence_start = section.find("```yaml")
    if fence_start == -1:
        return {}
    yaml_start = section.find("\n", fence_start)
    if yaml_start == -1:
        return {}
    fence_end = section.find("```", yaml_start + 1)
    if fence_end == -1:
        return {}
    try:
        loaded = yaml.safe_load(section[yaml_start + 1 : fence_end]) or {}
    except yaml.YAMLError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def source_gap(gap_id: str, owner: str, message: str, path: str, severity: str = "source_gap") -> SourceGap:
    return {
        "id": gap_id,
        "severity": severity,
        "owner": owner,
        "message": message,
        "source_ref": {"path": path},
    }


def normalize_gap_id(value: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9_.:-]+", "_", value.strip())
    return normalized.strip("_") or "source_gap"


def gap_objects_from_strings(values: list[Any], owner: str, path: str) -> list[dict[str, Any]]:
    gaps: list[dict[str, Any]] = []
    for value in values:
        raw = str(value)
        gaps.append(source_gap(normalize_gap_id(raw), owner, raw, path))
    return gaps


def read_markdown(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def parse_markdown_table(section: str) -> list[dict[str, str]]:
    rows: list[list[str]] = []
    for raw in section.splitlines():
        line = raw.strip()
        if not line.startswith("|") or "---" in line:
            continue
        rows.append([cell.strip() for cell in line.strip("|").split("|")])
    if len(rows) < 2:
        return []
    headers = [header.lower().replace(" ", "_") for header in rows[0]]
    output: list[dict[str, str]] = []
    for cells in rows[1:]:
        output.append({headers[index]: cells[index] if index < len(cells) else "" for index in range(len(headers))})
    return output


def first_paragraph(section: str) -> str | None:
    lines = [line.strip() for line in section.splitlines() if line.strip()]
    return " ".join(lines) if lines else None


def markdown_bullets(section: str) -> list[str]:
    bullets: list[str] = []
    current: list[str] = []
    for raw in section.splitlines():
        line = raw.strip()
        if line.startswith("- "):
            if current:
                bullets.append(" ".join(current))
            current = [line[2:].strip()]
        elif current and line:
            current.append(line)
        elif current:
            bullets.append(" ".join(current))
            current = []
    if current:
        bullets.append(" ".join(current))
    return bullets


def load_bindings(project_root: Path) -> dict[str, Any]:
    return read_yaml(project_root / "farplane" / "bindings.yaml")


def load_metric_definitions(project_root: Path) -> dict[str, Any]:
    payload = read_yaml(project_root / "farplane" / "metrics.yaml")
    metrics = payload.get("metrics") if isinstance(payload, dict) else None
    return metrics if isinstance(metrics, dict) else {}


def load_harness_config(project_root: Path) -> dict[str, Any]:
    return read_yaml(project_root / "farplane" / "harness.yaml")


def load_metric_selection(project_root: Path) -> dict[str, Any]:
    harness = load_harness_config(project_root)
    refs = harness.get("metric_refs") if isinstance(harness.get("metric_refs"), dict) else {}
    raw_project_rows = refs.get("objectives") if isinstance(refs.get("objectives"), list) else []
    objective_rows = [
        {**row, "scope": "project"}
        for row in raw_project_rows
        if isinstance(row, dict) and row.get("metric_id")
    ]
    area_rows: list[dict[str, Any]] = []
    areas = harness.get("areas") if isinstance(harness.get("areas"), dict) else {}
    for area_id, area in areas.items():
        if not isinstance(area, dict):
            continue
        rows = area.get("metric_refs") if isinstance(area.get("metric_refs"), list) else []
        area_rows.extend(
            {**row, "scope": "area", "area_id": str(area_id)}
            for row in rows
            if isinstance(row, dict) and row.get("metric_id")
        )
    objective_rows.sort(key=lambda row: int(row.get("priority") or 999999))
    guard_ids = refs.get("guards") if isinstance(refs.get("guards"), list) else []
    return {
        "objectives": objective_rows,
        "area_metrics": area_rows,
        "guards": [
            {"metric_id": str(metric_id), "scope": "project"}
            for metric_id in guard_ids
            if isinstance(metric_id, str) and metric_id.strip()
        ],
    }


def load_metric_bindings(project_root: Path) -> dict[str, Any]:
    payload = load_bindings(project_root)
    bindings = payload.get("metric_bindings") if isinstance(payload, dict) else None
    return bindings if isinstance(bindings, dict) else {}


def parse_ticket_kpi_rewards(markdown: str) -> list[dict[str, Any]]:
    reward = markdown_heading_section(markdown, "Reward")
    payload = parse_fenced_yaml_from_section(reward)
    raw_rewards = payload.get("kpi_rewards")
    if not isinstance(raw_rewards, list):
        return []
    rewards: list[dict[str, Any]] = []
    seen_reward_ids: set[str] = set()
    for item in raw_rewards:
        if not isinstance(item, dict):
            continue
        reward_id = str(item.get("reward_id") or "").strip()
        kpi_id = str(item.get("kpi_id") or "").strip()
        if not reward_id or reward_id in seen_reward_ids or not kpi_id:
            continue
        seen_reward_ids.add(reward_id)
        evidence_refs = item.get("evidence_refs")
        rewards.append(
            {
                "reward_id": reward_id,
                "kpi_id": kpi_id,
                "expected_reward": str(item.get("expected_reward") or ""),
                "check_in_at": str(item.get("check_in_at") or ""),
                "actual_result": str(item.get("actual_result") or ""),
                "decision": str(item.get("decision") or "").strip().lower(),
                "evaluated_at": str(item.get("evaluated_at") or ""),
                "evaluation_key": str(item.get("evaluation_key") or ""),
                "supersedes_evaluation_key": str(
                    item.get("supersedes_evaluation_key") or ""
                ),
                "evidence_refs": [
                    str(ref) for ref in evidence_refs if str(ref).strip()
                ]
                if isinstance(evidence_refs, list)
                else [],
            }
        )
    return rewards


def collect_ticket_refs(project_root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    refs: list[dict[str, Any]] = []
    rewards: list[dict[str, Any]] = []
    for path in sorted((project_root / "tickets").glob("TASK-*/ticket.md")):
        markdown = read_markdown(path)
        fm = parse_frontmatter(path)
        ticket_id = str(fm.get("ticket_id") or path.parent.name)
        reward_rows = parse_ticket_kpi_rewards(markdown)
        kpi_ids = sorted({row["kpi_id"] for row in reward_rows})
        status = str(fm.get("status") or "").strip().lower()
        phase = str(fm.get("phase") or "").strip().lower()
        ticket_ref = {
            "ticket_id": ticket_id,
            "path": str(path.relative_to(project_root)),
            "title": str(fm.get("title") or path.parent.name),
            "status": status,
            "phase": phase,
            "priority": str(fm.get("priority") or "medium"),
            "kpi_rewards": kpi_ids,
            "reward_rows": reward_rows,
            "source_ref": {"path": str(path.relative_to(project_root))},
        }
        refs.append(ticket_ref)
        for reward in reward_rows:
            rewards.append(
                {
                    "ticket_id": ticket_id,
                    "ticket_status": status,
                    "ticket_phase": phase,
                    "ticket": ticket_ref["path"],
                    **reward,
                }
            )
    return refs, rewards


def load_content_items(project_root: Path) -> tuple[list[dict[str, Any]], list[str]]:
    path = project_root / ".farplane" / "content" / "ledger.jsonl"
    if not path.exists():
        return [], ["missing_content_ledger"]
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
    return rows, []


def load_automations(project_root: Path) -> tuple[list[dict[str, Any]], list[str]]:
    path = project_root / "farplane" / "automations.toml"
    if not path.exists():
        return [], ["missing_automations_toml"]
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError:
        return [], ["invalid_automations_toml"]
    automations = data.get("automations") if isinstance(data, dict) else []
    if not isinstance(automations, list):
        return [], ["invalid_automations_shape"]
    return [
        {
            "id": str(item.get("id") or ""),
            "name": str(item.get("name") or ""),
            "kind": str(item.get("kind") or ""),
            "status": str(item.get("status") or ""),
            "source_ref": {"path": "farplane/automations.toml"},
        }
        for item in automations
        if isinstance(item, dict)
    ], []


def path_from_config(value: Any, default: Path) -> Path:
    raw = str(value or "").strip()
    return Path(raw) if raw else default


def compact_source_ref(path: Path) -> dict[str, str]:
    return {"path": str(path)}


def normalize_feed_scout_items(raw_items: Any) -> list[dict[str, Any]]:
    return [item for item in raw_items if isinstance(item, dict)] if isinstance(raw_items, list) else []


def normalize_feed_scout_groups(raw_groups: Any) -> list[dict[str, Any]]:
    if isinstance(raw_groups, list):
        return [group for group in raw_groups if isinstance(group, dict)]
    if isinstance(raw_groups, dict):
        groups: list[dict[str, Any]] = []
        for group_id, group in sorted(raw_groups.items(), key=lambda item: str(item[0])):
            if isinstance(group, dict):
                groups.append({"group_id": str(group_id), **group})
        return groups
    return []


def load_feed_scout_snapshot(project_root: Path, bindings: dict[str, Any]) -> tuple[dict[str, Any], list[SourceGap]]:
    config = bindings.get("feed_scout") if isinstance(bindings.get("feed_scout"), dict) else {}
    enabled = bool(config.get("enabled")) if config else False
    ui_config = config.get("ui") if isinstance(config.get("ui"), dict) else {}
    latest_feed_path = path_from_config(ui_config.get("latest_feed"), FEED_SCOUT_LATEST_FEED_PATH)
    latest_report_path = path_from_config(config.get("latest_report"), FEED_SCOUT_LATEST_REPORT_PATH)
    feed_abs = project_root / latest_feed_path
    report_abs = project_root / latest_report_path
    gaps: list[SourceGap] = []

    feed_payload = read_json(feed_abs)
    report_payload = read_json(report_abs)
    if enabled and not feed_payload:
        gaps.append(
            source_gap(
                "missing_feed_scout_latest_feed",
                "news",
                f"Feed Scout is enabled but {latest_feed_path} is missing or invalid.",
                str(latest_feed_path),
            )
        )
    if enabled and not report_payload:
        gaps.append(
            source_gap(
                "missing_feed_scout_latest_report",
                "news",
                f"Feed Scout is enabled but {latest_report_path} is missing or invalid.",
                str(latest_report_path),
            )
        )

    feed_source_ref = compact_source_ref(latest_feed_path)
    report_source_ref = compact_source_ref(latest_report_path)
    summary = feed_payload.get("summary") if isinstance(feed_payload.get("summary"), dict) else {}
    items = normalize_feed_scout_items(feed_payload.get("items"))
    groups = normalize_feed_scout_groups(feed_payload.get("groups"))
    latest_feed = {
        "date": str(feed_payload.get("date") or ""),
        "generated_at": str(feed_payload.get("generated_at") or ""),
        "summary": summary,
        "items": items,
        "groups": groups,
        "source_gaps": normalize_feed_scout_items(feed_payload.get("source_gaps")),
        "source_ref": feed_source_ref,
    }
    latest_report = {
        "generated_at": str(report_payload.get("generated_at") or ""),
        "report_path": str(report_payload.get("report_path") or ""),
        "daily_feed_path": str(report_payload.get("daily_feed_path") or ""),
        "summary": report_payload.get("summary") if isinstance(report_payload.get("summary"), dict) else {},
        "source_gaps": normalize_feed_scout_items(report_payload.get("source_gaps")),
        "source_ref": report_source_ref,
    }
    source_gap_ids = [gap["id"] for gap in gaps]
    return (
        {
            "enabled": enabled,
            "config": {
                "cadence": str(config.get("cadence") or ""),
                "timezone": str(config.get("timezone") or ""),
                "daily_feed_root": str(config.get("daily_feed_root") or ""),
                "ledger": str(config.get("ledger") or ""),
                "proposal_ledger": str(config.get("proposal_ledger") or ""),
                "latest_feed": str(latest_feed_path),
                "latest_report": str(latest_report_path),
                "source_ref": {"path": "farplane/bindings.yaml", "pointer": "feed_scout"},
            },
            "summary": summary,
            "items": items,
            "groups": groups,
            "latest_feed": latest_feed,
            "latest_report": latest_report,
            "source_gap_ids": source_gap_ids,
        },
        gaps,
    )


def report_cards(project_root: Path) -> list[dict[str, Any]]:
    registry = build_report_registry(project_root)
    cards: list[dict[str, Any]] = []
    for report in registry.get("reports", [])[:20]:
        if not isinstance(report, dict):
            continue
        frontmatter = report.get("frontmatter") if isinstance(report.get("frontmatter"), dict) else {}
        path = str(report.get("path") or "")
        cards.append(
            {
                "id": str(report.get("ref") or Path(path).stem),
                "ref": str(report.get("ref") or ""),
                "path": path,
                "interval_id": frontmatter.get("interval_id"),
                "kind": str(report.get("kind") or ""),
                "created_at": str(report.get("created_at") or ""),
                "ui_summary": str(report.get("ui_summary") or ""),
                "parent_ref": report.get("parent_ref"),
                "children_refs": report.get("children_refs") if isinstance(report.get("children_refs"), list) else [],
                "source_ref": {"path": path},
            }
        )
    return cards


def proof_artifacts(project_root: Path) -> list[dict[str, Any]]:
    artifacts: list[dict[str, Any]] = []
    tickets_root = project_root / "tickets"
    ticket_roots = [
        *sorted(tickets_root.glob("TASK-*")),
        *sorted((tickets_root / "archive").glob("TASK-*")),
    ]
    for ticket_root in ticket_roots:
        artifact_root = ticket_root / "artifacts"
        if not artifact_root.is_dir():
            continue
        for path in sorted(artifact_root.rglob("*")):
            if path.is_file():
                rel = str(path.relative_to(project_root))
                artifacts.append({"id": path.stem, "path": rel, "source_ref": {"path": rel}})
    return artifacts


def eval_runs(project_root: Path) -> list[dict[str, Any]]:
    root = project_root / ".farplane" / "evals" / "runs"
    if not root.exists():
        return []
    return [
        {"id": path.stem, "path": str(path.relative_to(project_root)), "source_ref": {"path": str(path.relative_to(project_root))}}
        for path in sorted(root.glob("**/*"))
        if path.is_file()
    ][-20:]


def latest_primitives(project_root: Path, date_value: str | None) -> dict[str, Any]:
    daily_root = project_root / ".farplane" / "metrics" / "daily"
    if date_value:
        return read_json(daily_root / f"{date_value}.json")
    candidates = sorted(daily_root.glob("*.json")) if daily_root.exists() else []
    return read_json(candidates[-1]) if candidates else {}


def primitive_id_for_metric(metric_id: str, recipe: dict[str, Any]) -> str:
    refresh = str(recipe.get("refresh") or recipe.get("update_prompt") or "").lower()
    if "count_ticket_kpi_rewards" in refresh or "kpi_rewards" in refresh:
        return "ticket_count_by_kpi"
    if "calculate_autonomy_time_ratio" in refresh or metric_id == "auto_time_ratio":
        return "autonomy_time_feedback"
    if "calculate_ticket_intervention_metrics" in refresh or metric_id in {
        "auto_completion_rate",
        "intervention_free_ticket_count",
        "ticket_intervention_turn_count",
    }:
        return "ticket_intervention_feedback"
    if metric_id in {"codex_thread_count", "codex_turn_count", "codex_token_total", "codex_span_minutes"}:
        return "codex_thread_usage"
    if metric_id in {"ai_burn_estimate", "burn_per_thread", "burn_per_turn", "burn_per_token"}:
        return "ai_burn_estimate"
    if metric_id == "evidence_distribution_reach":
        return "content_views_total"
    if metric_id == "activated_external_projects":
        return "project_adoption"
    if metric_id == "rejected_ai_ticket_count":
        return "planner_ticket_quality"
    if metric_id == "kpi_attributed_ticket_ratio":
        return "kpi_attributed_ticket_ratio"
    return "manual_source_gap"


def metric_definitions(project_root: Path) -> tuple[dict[str, Any], list[str]]:
    raw_metrics = load_metric_definitions(project_root)
    selection = load_metric_selection(project_root)
    metric_bindings = load_metric_bindings(project_root)
    if not raw_metrics:
        return {}, ["missing:farplane/metrics.yaml#metrics"]
    definitions: dict[str, Any] = {}
    gaps = [
        f"missing:farplane/bindings.yaml#metric_bindings/{metric_id}"
        for metric_id in sorted(set(raw_metrics) - set(metric_bindings))
    ]
    objective_rows = selection.get("objectives") if isinstance(selection.get("objectives"), list) else []
    area_rows = selection.get("area_metrics") if isinstance(selection.get("area_metrics"), list) else []
    guard_rows = selection.get("guards") if isinstance(selection.get("guards"), list) else []
    objective_by_id = {
        str(row.get("metric_id")): row
        for row in objective_rows
        if isinstance(row, dict) and row.get("metric_id")
    }
    guard_by_id = {
        str(row.get("metric_id")): row
        for row in guard_rows
        if isinstance(row, dict) and row.get("metric_id")
    }
    areas_by_id: dict[str, list[dict[str, Any]]] = {}
    for row in area_rows:
        if not isinstance(row, dict) or not row.get("metric_id"):
            continue
        areas_by_id.setdefault(str(row["metric_id"]), []).append(row)
    for metric_id, raw_definition in raw_metrics.items():
        definition = raw_definition if isinstance(raw_definition, dict) else {}
        raw_binding = metric_bindings.get(metric_id)
        binding = raw_binding if isinstance(raw_binding, dict) else {}
        recipe = {**definition, **binding}
        primitive_id = primitive_id_for_metric(str(metric_id), recipe)
        kind = str(recipe.get("kind") or recipe.get("aggregation") or "point")
        if kind == "daily_count":
            aggregation = "daily"
            cumulative = True
        else:
            aggregation = "daily" if kind == "daily" else "point"
            cumulative = bool(recipe.get("cumulative", False))
        objective = objective_by_id.get(str(metric_id), {})
        area_selections = areas_by_id.get(str(metric_id), [])
        guard_ref = guard_by_id.get(str(metric_id), {})
        guard = definition.get("guard") if isinstance(definition.get("guard"), dict) and guard_ref else {}
        raw_target = guard.get("threshold") if "threshold" in guard else recipe.get("target")
        target_value = parse_target(raw_target)
        raw_direction = definition.get("direction") or guard.get("operator") or recipe.get("target_direction")
        target_direction = normalize_target_direction(raw_direction)
        target_unit = str(recipe.get("unit") or "")
        description = metric_description(str(metric_id), recipe)
        definitions[str(metric_id)] = {
            "metric_id": str(metric_id),
            "label": str(recipe.get("label") or str(metric_id).replace("_", " ").capitalize()),
            "description": description,
            "tooltip": description,
            "selection_role": "objective" if objective else "guard" if guard else "area" if area_selections else "observation",
            "selection": objective or guard_ref or (area_selections if area_selections else None),
            "direction": definition.get("direction"),
            "max_age_days": definition.get("max_age_days"),
            "guard": guard or None,
            "unit": target_unit,
            "display": str(recipe.get("display") or "reading"),
            "pinned": bool(recipe.get("pinned", False)),
            "kind": kind,
            "aggregation": aggregation,
            "cumulative": cumulative,
            "target": target_value,
            "target_direction": target_direction,
            "target_unit": target_unit,
            "target_spec": {
                "value": target_value,
                "direction": target_direction,
                "unit": target_unit,
            },
            "primitive_id": primitive_id,
            "refresh": recipe.get("refresh") or recipe.get("update_prompt") or "",
            "source_ref": {"path": "farplane/metrics.yaml", "pointer": f"/metrics/{metric_id}"},
            "binding_source_ref": {
                "path": "farplane/bindings.yaml",
                "pointer": f"/metric_bindings/{metric_id}",
            },
        }
    return definitions, gaps


def daily_metric_files(project_root: Path) -> list[Path]:
    root = project_root / DAILY_METRICS_DIR
    return sorted(root.glob("*.json")) if root.exists() else []


def canonical_batch_keys(project_root: Path, snapshot_date: str | None) -> set[tuple[str, str]]:
    root = project_root / ".farplane" / "metrics" / "observations"
    if not root.exists():
        return set()
    keys: set[tuple[str, str]] = set()
    for path in sorted(root.glob("*/*.json")):
        if snapshot_date and path.stem > snapshot_date:
            continue
        payload = read_json(path)
        if payload.get("schema_version") == 1:
            keys.add((str(payload.get("source_id") or path.parent.name), str(payload.get("date") or path.stem)))
    return keys


def reading_value(reading: Any) -> tuple[float | None, str, dict[str, Any] | None]:
    if isinstance(reading, dict):
        value = reading.get("value")
        status = str(reading.get("status") or "available")
        payload = reading.get("payload") if isinstance(reading.get("payload"), dict) else None
    else:
        value = reading
        status = "available"
        payload = None
    return (float(value) if isinstance(value, (int, float)) else None, status, payload)


def observation(metric_id: str, date_value: str, value: float | None, status: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    output: dict[str, Any] = {
        "metric_id": metric_id,
        "date": date_value,
        "value": value,
        "status": status,
    }
    if payload is not None:
        output["payload"] = payload
    return output


def daily_metric_reading_observation(metric_id: str, reading: Any, date_value: str) -> dict[str, Any] | None:
    value, status, payload = reading_value(reading)
    if status == "available" and value is None:
        return None
    return observation(metric_id, date_value, value, status, payload)


def nested_number(payload: dict[str, Any], keys: list[str]) -> float | None:
    current: Any = payload
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return float(current) if isinstance(current, (int, float)) else None


def primitive_metric_observation(
    metric_id: str,
    metric_def: dict[str, Any],
    primitives: dict[str, Any],
    date_value: str,
) -> dict[str, Any] | None:
    primitive_id = str(metric_def.get("primitive_id") or "")
    if primitive_id == "ticket_count_by_kpi":
        reading = primitives.get("ticket_count_by_kpi")
        if isinstance(reading, dict):
            if metric_id in reading:
                return daily_metric_reading_observation(metric_id, reading.get(metric_id), date_value)
            return observation(
                metric_id,
                date_value,
                0.0,
                "available",
                {
                    "tickets": [],
                    "gaps": [],
                    "empty_window": True,
                    "primitive_id": primitive_id,
                    "reward_contract": REWARD_CONTRACT,
                },
            )
    nested_reading = primitives.get(primitive_id)
    if isinstance(nested_reading, dict) and metric_id in nested_reading:
        return daily_metric_reading_observation(metric_id, nested_reading.get(metric_id), date_value)
    if primitive_id in {"kpi_attributed_ticket_ratio", "ticket_thread_link_coverage"}:
        reading = primitives.get(primitive_id)
        return daily_metric_reading_observation(metric_id, reading, date_value)
    if primitive_id == "codex_thread_usage":
        usage = primitives.get("codex_thread_usage") if isinstance(primitives.get("codex_thread_usage"), dict) else {}
        payload = usage.get("payload") if isinstance(usage.get("payload"), dict) else {}
        values = {
            "codex_thread_count": nested_number(payload, ["thread_count"]),
            "codex_turn_count": nested_number(payload, ["turn_count"]),
            "codex_token_total": nested_number(payload, ["tokens", "total"]),
            "codex_span_minutes": nested_number(payload, ["span_minutes"]),
        }
        if metric_id in values:
            status = str(usage.get("status") or ("available" if values[metric_id] is not None else "source_gap"))
            return observation(metric_id, date_value, values[metric_id], status, payload)
    if primitive_id == "ai_burn_estimate":
        burn = primitives.get("ai_burn_estimate") if isinstance(primitives.get("ai_burn_estimate"), dict) else {}
        burn_value, burn_status, burn_payload = reading_value(burn)
        usage = primitives.get("codex_thread_usage") if isinstance(primitives.get("codex_thread_usage"), dict) else {}
        usage_payload = usage.get("payload") if isinstance(usage.get("payload"), dict) else {}
        divisors = {
            "burn_per_thread": nested_number(usage_payload, ["thread_count"]),
            "burn_per_turn": nested_number(usage_payload, ["turn_count"]),
            "burn_per_token": nested_number(usage_payload, ["tokens", "total"]),
        }
        if metric_id == "ai_burn_estimate":
            return observation(metric_id, date_value, burn_value, burn_status, burn_payload)
        if metric_id in divisors:
            divisor = divisors[metric_id]
            value = round(burn_value / divisor, 6) if burn_value is not None and divisor else None
            status = burn_status if value is not None else "source_gap"
            payload = dict(burn_payload or {})
            payload["divisor"] = divisor
            return observation(metric_id, date_value, value, status, payload)
    direct = primitives.get(metric_id)
    if isinstance(direct, dict):
        return daily_metric_reading_observation(metric_id, direct, date_value)
    return None


def compatible_metric_observation(metric_def: dict[str, Any], obs: dict[str, Any]) -> bool:
    """Reject pre-v1 accepted-reward readings that counted declared intent."""

    if metric_def.get("primitive_id") != "ticket_count_by_kpi":
        return True
    payload = obs.get("payload") if isinstance(obs.get("payload"), dict) else {}
    return payload.get("reward_contract") == REWARD_CONTRACT


def daily_observations(project_root: Path, metric_defs: dict[str, Any], snapshot_date: str | None) -> list[dict[str, Any]]:
    observations: list[dict[str, Any]] = []
    canonical_keys = canonical_batch_keys(project_root, snapshot_date)
    for path in daily_metric_files(project_root):
        if snapshot_date and path.stem > snapshot_date:
            continue
        payload = read_json(path)
        date_value = str(payload.get("date") or path.stem)
        metrics = payload.get("metrics")
        if isinstance(metrics, dict):
            for metric_id, reading in metrics.items():
                obs = daily_metric_reading_observation(str(metric_id), reading, date_value)
                metric_def = metric_defs.get(str(metric_id), {})
                if obs is not None and compatible_metric_observation(metric_def, obs):
                    observations.append(obs)
        primitives = payload.get("primitives")
        if isinstance(primitives, dict):
            for metric_id, metric_def in metric_defs.items():
                primitive_id = str(metric_def.get("primitive_id") or "")
                if (primitive_id, date_value) in canonical_keys:
                    continue
                obs = primitive_metric_observation(metric_id, metric_def, primitives, date_value)
                if obs is not None and compatible_metric_observation(metric_def, obs):
                    observations.append(obs)
    return observations


def provider_observations(project_root: Path, metric_defs: dict[str, Any], snapshot_date: str | None) -> list[dict[str, Any]]:
    metric_ids = set(metric_defs)
    output: list[dict[str, Any]] = []
    for batch in read_metric_batches(project_root, snapshot_date):
        source_path = batch_path(project_root, batch.source_id, batch.date)
        source_ref = str(source_path.relative_to(project_root))
        for row in batch.observations:
            if row.metric_id not in metric_ids:
                continue
            payload = dict(row.payload)
            payload.setdefault("source_id", batch.source_id)
            payload.setdefault("source_path", source_ref)
            obs = observation(row.metric_id, row.date, row.value, row.status, payload)
            if compatible_metric_observation(metric_defs[row.metric_id], obs):
                output.append(obs)
    return output


def load_content_ledger_rows(project_root: Path) -> list[dict[str, Any]]:
    ledger_path = project_root / CONTENT_LEDGER_PATH
    if not ledger_path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in ledger_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(item, dict):
            rows.append(item)
    return rows


def ledger_content_observations(project_root: Path, snapshot_date: str | None) -> list[dict[str, Any]]:
    counts_by_date: dict[str, int] = {}
    for row in load_content_ledger_rows(project_root):
        if row.get("status") != "posted":
            continue
        parsed = parse_iso_datetime(row.get("published_at"))
        if parsed is None:
            continue
        date_value = parsed.date().isoformat()
        if snapshot_date and date_value > snapshot_date:
            continue
        counts_by_date[date_value] = counts_by_date.get(date_value, 0) + 1
    return [
        observation("posts_published", date_value, float(count), "available", {"source": str(CONTENT_LEDGER_PATH)})
        for date_value, count in sorted(counts_by_date.items())
    ]


def ledger_missing_observations(project_root: Path, metric_defs: dict[str, Any], snapshot_date: str | None) -> list[dict[str, Any]]:
    if (project_root / CONTENT_LEDGER_PATH).exists():
        return []
    date_value = snapshot_date or datetime.now(timezone.utc).date().isoformat()
    output: list[dict[str, Any]] = []
    for metric_id, metric_def in metric_defs.items():
        if ".farplane/content/ledger.jsonl" not in str(metric_def.get("refresh") or ""):
            continue
        output.append(
            observation(
                metric_id,
                date_value,
                None,
                "source_gap",
                {"gaps": ["missing:.farplane/content/ledger.jsonl"]},
            )
        )
    return output


def source_gap_reason(obs: dict[str, Any]) -> str:
    payload = obs.get("payload")
    if isinstance(payload, dict):
        reason = payload.get("reason")
        if isinstance(reason, str) and reason:
            return reason
        gaps = payload.get("gaps")
        if isinstance(gaps, list) and gaps:
            return str(gaps[0])
    return str(obs.get("status") or "source_gap")


def build_metric_card(
    metric_id: str,
    metric_def: dict[str, Any],
    observations: list[dict[str, Any]],
    snapshot_date: str | None = None,
) -> dict[str, Any]:
    metric_obs = sorted(
        [
            obs
            for obs in observations
            if obs.get("metric_id") == metric_id and obs.get("status", "available") == "available"
        ],
        key=lambda obs: str(obs.get("date", "")),
    )
    metric_gaps = sorted(
        [
            obs
            for obs in observations
            if obs.get("metric_id") == metric_id and obs.get("status", "available") != "available"
        ],
        key=lambda obs: str(obs.get("date", "")),
    )
    series: list[dict[str, Any]] = []
    running = 0.0
    hit_at: str | None = None
    hit_value: float | None = None
    target = metric_def.get("target")
    target_direction = normalize_target_direction(metric_def.get("target_direction"))
    target_unit = str(metric_def.get("target_unit") or metric_def.get("unit") or "")
    for obs in metric_obs:
        value = obs.get("value")
        if not isinstance(value, (int, float)):
            continue
        point: dict[str, Any] = {"date": obs.get("date"), "value": float(value)}
        point["daily_diff"] = float(value) - float(series[-1]["value"]) if series else None
        if isinstance(obs.get("payload"), dict):
            point["payload"] = obs["payload"]
        payload = obs.get("payload") if isinstance(obs.get("payload"), dict) else {}
        if isinstance(payload.get("items"), list):
            point["items"] = payload["items"]
        comparison_value = float(value)
        if metric_def.get("aggregation") == "daily" and metric_def.get("cumulative"):
            running += float(value)
            point["cumulative"] = running
            comparison_value = running
        else:
            point["current"] = float(value)
        target_hit = (
            comparison_value >= target
            if target_direction == "above"
            else comparison_value <= target
        ) if isinstance(target, (int, float)) else False
        if target_hit and hit_at is None:
            hit_at = str(obs.get("date"))
            hit_value = comparison_value
        series.append(point)
    latest_gap = metric_gaps[-1] if metric_gaps else None
    source_gaps: list[dict[str, Any]] = []
    if latest_gap:
        gap: dict[str, Any] = {
            "date": latest_gap.get("date"),
            "status": latest_gap.get("status"),
            "reason": source_gap_reason(latest_gap),
        }
        if isinstance(latest_gap.get("payload"), dict):
            gap["payload"] = latest_gap["payload"]
        source_gaps.append(gap)
    status = "available" if series else str(latest_gap.get("status") if latest_gap else "missing")
    max_age_days = metric_def.get("max_age_days") if isinstance(metric_def.get("max_age_days"), int) else None
    stale_reason: str | None = None
    if series and max_age_days:
        as_of = date_type.fromisoformat(snapshot_date) if snapshot_date else datetime.now(timezone.utc).date()
        observed_at = date_type.fromisoformat(str(series[-1].get("date"))[:10])
        age_days = (as_of - observed_at).days
        if age_days > max_age_days:
            status = "stale"
            stale_reason = f"latest observation is {age_days} days old; max_age_days={max_age_days}"
            source_gaps.append({"date": series[-1].get("date"), "status": "stale", "reason": stale_reason})
    return {
        "metric_id": metric_id,
        "label": metric_def.get("label") or metric_id,
        "description": metric_def.get("description") or "",
        "tooltip": metric_def.get("tooltip") or metric_def.get("description") or "",
        "primitive_id": metric_def.get("primitive_id"),
        "aggregation": metric_def.get("aggregation"),
        "cumulative": bool(metric_def.get("cumulative")),
        "target": target,
        "target_direction": target_direction,
        "target_unit": target_unit,
        "target_spec": {
            "value": target,
            "direction": target_direction,
            "unit": target_unit,
        },
        "unit": metric_def.get("unit") or "",
        "display": metric_def.get("display") or "reading",
        "pinned": bool(metric_def.get("pinned")),
        "status": status,
        "current": series[-1]["value"] if series and status == "available" else None,
        "series": series,
        "best_daily": max((float(point["value"]) for point in series), default=None),
        "source_gaps": source_gaps,
        "target_hit": {"hit_at": hit_at, "hit_value": hit_value} if hit_at else None,
        "source_ref": metric_def.get("source_ref"),
    }


def item_content_key(item: dict[str, Any]) -> str | None:
    for key in ("content_id", "id"):
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    platform = item.get("platform")
    external_id = item.get("external_id") or item.get("media_id") or item.get("tweet_id")
    if isinstance(platform, str) and platform.strip() and isinstance(external_id, str) and external_id.strip():
        return f"{platform.strip()}:{external_id.strip()}"
    if isinstance(external_id, str) and external_id.strip():
        return external_id.strip()
    url = item.get("url")
    return url.strip() if isinstance(url, str) and url.strip() else None


def merge_content_metadata(target: dict[str, Any], item: dict[str, Any]) -> None:
    for key in (
        "content_id",
        "id",
        "platform",
        "external_id",
        "url",
        "title",
        "caption",
        "kind",
        "media_type",
        "media_product_type",
        "campaign",
        "status",
        "published_at",
        "approval",
        "approval_ref",
        "kpis",
    ):
        value = item.get(key)
        if value not in (None, "") and key not in target:
            target[key] = value
    content_id = str(target.get("content_id") or "")
    if ":" in content_id:
        platform, external_id = content_id.split(":", 1)
        target.setdefault("platform", platform)
        target.setdefault("external_id", external_id)


def item_metric_value(item: dict[str, Any], fallback: float) -> float:
    for key in ("value", "metric_value", "count"):
        value = item.get(key)
        if isinstance(value, (int, float)):
            return float(value)
    metrics = item.get("metrics")
    if isinstance(metrics, dict):
        for value in metrics.values():
            if isinstance(value, (int, float)):
                return float(value)
    return fallback


def extract_content_items(point: dict[str, Any]) -> list[dict[str, Any]]:
    raw_items: Any = point.get("items")
    payload = point.get("payload")
    if raw_items is None and isinstance(payload, dict):
        raw_items = payload.get("items")
    if raw_items is None and isinstance(payload, dict):
        raw_items = payload.get("posts") or payload.get("content_items")
    return [item for item in raw_items if isinstance(item, dict)] if isinstance(raw_items, list) else []


def build_content_metric_cards(metric_cards: list[dict[str, Any]], ledger_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    content_by_id: dict[str, dict[str, Any]] = {}
    for row in ledger_rows:
        key = item_content_key(row)
        if not key:
            continue
        content = content_by_id.setdefault(key, {"content_id": key, "metrics": {}})
        merge_content_metadata(content, row)
    for metric in metric_cards:
        metric_id = str(metric.get("metric_id") or "")
        for point in metric.get("series") or []:
            if not isinstance(point, dict) or not isinstance(point.get("value"), (int, float)):
                continue
            for item in extract_content_items(point):
                key = item_content_key(item)
                if not key:
                    continue
                content = content_by_id.setdefault(key, {"content_id": key, "metrics": {}})
                merge_content_metadata(content, item)
                bucket = content["metrics"].setdefault(
                    metric_id,
                    {
                        "metric_id": metric_id,
                        "label": metric.get("label") or metric_id,
                        "unit": metric.get("unit") or "",
                        "series": [],
                    },
                )
                bucket["series"].append(
                    {
                        "date": point.get("date"),
                        "value": item_metric_value(item, float(point["value"])),
                    }
                )
    output: list[dict[str, Any]] = []
    for content in content_by_id.values():
        metric_entries = []
        for metric in content.get("metrics", {}).values():
            series = sorted(metric["series"], key=lambda point: str(point.get("date") or ""))
            metric_entries.append({**metric, "current": series[-1]["value"] if series else None, "series": series})
        content["metrics"] = sorted(metric_entries, key=lambda metric: str(metric.get("metric_id") or ""))
        output.append(content)
    return sorted(output, key=lambda item: (str(item.get("published_at") or ""), str(item.get("content_id") or "")))


def metric_projection(project_root: Path, metric_defs: dict[str, Any], snapshot_date: str | None) -> dict[str, Any]:
    observations = daily_observations(project_root, metric_defs, snapshot_date)
    observations.extend(provider_observations(project_root, metric_defs, snapshot_date))
    observations.extend(ledger_content_observations(project_root, snapshot_date))
    observations.extend(ledger_missing_observations(project_root, metric_defs, snapshot_date))
    metric_cards = [
        build_metric_card(metric_id, metric_def, observations, snapshot_date)
        for metric_id, metric_def in sorted(metric_defs.items())
    ]
    source_gaps = []
    for card in metric_cards:
        if not card.get("pinned") or card.get("status") in {"available", "not_applicable"}:
            continue
        first_gap = card["source_gaps"][0] if card.get("source_gaps") else {}
        reason = first_gap.get("reason") if isinstance(first_gap, dict) else None
        if card.get("primitive_id") == "content_views_total" and reason == "no_component_view_observations":
            continue
        source_gaps.append(
            {
                "id": f"metric_source_gap:{card['metric_id']}",
                "severity": "source_gap",
                "owner": "metrics",
                "message": str(reason or "no available observation for metric"),
                "source_ref": card.get("source_ref") or {"path": "farplane/metrics.yaml"},
            }
        )
    return {
        "series": metric_cards,
        "contents": build_content_metric_cards(metric_cards, load_content_ledger_rows(project_root)),
        "source_gaps": source_gaps,
    }


def load_project_snapshot(project_root: Path, snapshot_date: str | None = None) -> dict[str, Any]:
    project_root = project_root.resolve()
    manifest = read_json(project_root / "farplane" / "manifest.json")
    bindings = load_bindings(project_root)
    harness = load_harness_config(project_root)
    selection = load_metric_selection(project_root)
    metric_defs, metric_gaps = metric_definitions(project_root)
    metric_view = metric_projection(project_root, metric_defs, snapshot_date)
    metric_cards = metric_view["series"] if isinstance(metric_view.get("series"), list) else []
    metric_cards_by_id = {str(card.get("metric_id")): card for card in metric_cards if isinstance(card, dict)}
    latest = latest_primitives(project_root, snapshot_date)
    readings = latest.get("primitives") if isinstance(latest.get("primitives"), dict) else {}
    ticket_refs, kpi_rewards = collect_ticket_refs(project_root)
    content_items, content_gap_ids = load_content_items(project_root)
    automations, automation_gap_ids = load_automations(project_root)
    feed_scout, feed_scout_gaps = load_feed_scout_snapshot(project_root, bindings)
    reports = report_cards(project_root)
    proof_items = proof_artifacts(project_root)
    eval_items = eval_runs(project_root)
    sources = [
        source_record(project_root, "farplane/manifest.json", "project-manifest"),
        source_record(project_root, "farplane/harness.yaml", "project-harness"),
        source_record(project_root, "farplane/metrics.yaml", "project-metrics"),
        source_record(project_root, "farplane/bindings.yaml", "project-bindings"),
    ]
    source_gaps = [
        {
            "id": gap,
            "severity": "source_gap",
            "owner": "metrics",
            "message": gap,
            "source_ref": {
                "path": "farplane/metrics.yaml" if "metrics.yaml" in gap else "farplane/bindings.yaml"
            },
        }
        for gap in metric_gaps
    ]
    source_gaps.extend(gap_objects_from_strings(latest.get("source_gaps", []) if isinstance(latest.get("source_gaps"), list) else [], "metrics", ".farplane/metrics/daily/"))
    source_gaps.extend(gap for gap in metric_view.get("source_gaps", []) if isinstance(gap, dict))
    source_gaps.extend(source_gap(gap_id, "distribution", gap_id, ".farplane/content/ledger.jsonl") for gap_id in content_gap_ids)
    source_gaps.extend(source_gap(gap_id, "cadence", gap_id, "farplane/automations.toml") for gap_id in automation_gap_ids)
    source_gaps.extend(feed_scout_gaps)
    if not reports:
        source_gaps.append(source_gap("missing_recent_reports", "cadence", "No recent report cards found under .farplane/reports/.", ".farplane/reports/"))
    if not ticket_refs:
        source_gaps.append(source_gap("missing_ticket_refs", "kanban", "No active ticket refs found.", "tickets/"))
    if not eval_items:
        source_gaps.append(source_gap("missing_eval_runs", "proof", "No eval runs found under .farplane/evals/runs/.", ".farplane/evals/runs/"))
    if not proof_items:
        source_gaps.append(source_gap("missing_qa_artifacts", "proof", "No ticket-scoped proof artifacts found.", "tickets/**/artifacts/"))
    if not latest:
        source_gaps.append(
            {
                "id": "missing_primitive_metric_snapshot",
                "severity": "source_gap",
                "owner": "metrics",
                "message": "Run `farplane metrics primitives --project-root <project> --date <YYYY-MM-DD>`.",
                "source_ref": {"path": ".farplane/metrics/daily/"},
            }
        )
    project = manifest.get("project") if isinstance(manifest.get("project"), dict) else {}
    source_gap_ids = [gap["id"] for gap in source_gaps]
    distribution_gap_ids = [gap for gap in source_gap_ids if gap.startswith("missing_content")]
    cadence_gap_ids = [gap for gap in source_gap_ids if gap.startswith("missing_recent") or gap.startswith("missing_automations") or gap.startswith("invalid_automations")]
    kanban_gap_ids = [gap for gap in source_gap_ids if gap.startswith("missing_ticket")]
    proof_gap_ids = [gap for gap in source_gap_ids if gap.startswith("missing_eval") or gap.startswith("missing_qa")]
    news_gap_ids = [gap["id"] for gap in source_gaps if gap.get("owner") == "news"]
    feed_scout["source_gap_ids"] = news_gap_ids
    memory_refs = [
        {"id": "history", "path": "docs/HISTORY.md", "source_ref": {"path": "docs/HISTORY.md"}},
        {"id": "memory", "path": "docs/MEMORY.md", "source_ref": {"path": "docs/MEMORY.md"}},
        {"id": "troubles", "path": "docs/TROUBLES.md", "source_ref": {"path": "docs/TROUBLES.md"}},
        {"id": "lessons", "path": "docs/LESSONS.md", "source_ref": {"path": "docs/LESSONS.md"}},
    ]
    content_metric_ids = sorted(
        {
            str(metric.get("metric_id"))
            for content in metric_view.get("contents", [])
            if isinstance(content, dict)
            for metric in content.get("metrics", [])
            if isinstance(metric, dict) and metric.get("metric_id")
        }
    )
    pm_manifest = read_json(project_root / "farplane" / "pm.json")
    pm_threads = pm_manifest.get("threads") if isinstance(pm_manifest.get("threads"), dict) else {}
    identity = harness.get("identity") if isinstance(harness.get("identity"), dict) else {}
    constraints = harness.get("constraints") if isinstance(harness.get("constraints"), dict) else {}
    charter = {
        "mission": str(identity.get("mission") or ""),
        "human_thesis": str(identity.get("human_thesis") or ""),
        "north_star": str(identity.get("north_star") or ""),
        "operating_principles": harness.get("operating_principles") if isinstance(harness.get("operating_principles"), list) else [],
        "stable_capabilities": harness.get("stable_capabilities") if isinstance(harness.get("stable_capabilities"), list) else [],
        "non_tradeoffs": constraints.get("non_tradeoffs") if isinstance(constraints.get("non_tradeoffs"), list) else [],
        "areas": harness.get("areas") if isinstance(harness.get("areas"), dict) else {},
        "feature_definition": harness.get("feature_definition") if isinstance(harness.get("feature_definition"), dict) else {},
        "leverage_commitments": harness.get("leverage_commitments") if isinstance(harness.get("leverage_commitments"), list) else [],
    }
    return {
        "schema_version": 2,
        "generated_at": now_utc(),
        "project_root": str(project_root),
        "shared_shapes": SHARED_SHAPES,
        "project": {
            "id": str(bindings.get("project", {}).get("id") or project.get("name") or project_root.name).lower().replace(" ", "-"),
            "name": project.get("name") or project_root.name,
            "description": project.get("description") or "",
            "archetype": project.get("archetype") or "",
        },
        "sources": sources,
        "source_gaps": source_gaps,
        "metrics": {
            "selection": selection,
            "definitions": metric_defs,
            "primitives": PRIMITIVE_CATALOG,
            "readings": readings,
            "series": metric_cards,
            "contents": metric_view.get("contents") if isinstance(metric_view.get("contents"), list) else [],
            "latest": latest,
        },
        "tabs": {
            "overview": {
                "charter": charter,
                "selection": selection,
                "pinned_metrics": [metric_id for metric_id, metric in metric_defs.items() if metric.get("pinned")],
                "pinned_metric_cards": [
                    metric_cards_by_id[metric_id]
                    for metric_id, metric in metric_defs.items()
                    if metric.get("pinned") and metric_id in metric_cards_by_id
                ],
                "primitive_summary": readings,
                "source_gap_count": len(source_gaps),
                "source_gap_ids": source_gap_ids,
            },
            "objectives": {
                "selection": selection,
                "metric_cards": [
                    metric_cards_by_id[metric_id]
                    for metric_id in [
                        str(row.get("metric_id"))
                        for row in (selection.get("objectives") or []) + (selection.get("guards") or [])
                        if isinstance(row, dict) and row.get("metric_id")
                    ]
                    if metric_id in metric_cards_by_id
                ],
                "source_gap_ids": [
                    f"metric_source_gap:{metric_id}"
                    for metric_id in [
                        str(row.get("metric_id"))
                        for row in (selection.get("objectives") or []) + (selection.get("guards") or [])
                        if isinstance(row, dict) and row.get("metric_id")
                    ]
                    if metric_cards_by_id.get(metric_id, {}).get("status") not in {"available", "not_applicable"}
                ],
            },
            "distribution": {
                "content_items": content_items,
                "content_metric_cards": metric_view.get("contents") if isinstance(metric_view.get("contents"), list) else [],
                "content_metric_ids": content_metric_ids,
                "source_gap_ids": distribution_gap_ids,
            },
            "news": {
                "summary": feed_scout.get("summary") if isinstance(feed_scout.get("summary"), dict) else {},
                "items": feed_scout.get("items") if isinstance(feed_scout.get("items"), list) else [],
                "groups": feed_scout.get("groups") if isinstance(feed_scout.get("groups"), list) else [],
                "latest_report": feed_scout.get("latest_report") if isinstance(feed_scout.get("latest_report"), dict) else {},
                "feed_scout": feed_scout,
                "source_gap_ids": news_gap_ids,
            },
            "cadence": {
                "automations": automations,
                "pm_threads": pm_threads,
                "recent_reports": reports,
                "source_gap_ids": cadence_gap_ids,
            },
            "kanban": {
                "tickets": ticket_refs,
                "kpi_rewards": kpi_rewards,
                "blocked_count": len([ticket for ticket in ticket_refs if ticket.get("status") == "blocked"]),
                "review_count": len([ticket for ticket in ticket_refs if ticket.get("status") == "review"]),
                "source_gap_ids": kanban_gap_ids,
            },
            "proof": {
                "eval_runs": eval_items,
                "qa_artifacts": proof_items,
                "latest_eval_metric_id": "latest_eval_pass_rate",
                "source_gap_ids": proof_gap_ids,
            },
            "memory_reports": {
                "memory_refs": memory_refs,
                "report_cards": reports,
                "source_gap_ids": [],
            },
        },
    }


def write_project_ui_snapshot(snapshot: dict[str, Any], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = output_path.with_suffix(output_path.suffix + ".tmp")
    tmp.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(output_path)
    return output_path


def run_snapshot(args: argparse.Namespace) -> int:
    project_root = Path(args.project_root).expanduser().resolve()
    snapshot = load_project_snapshot(project_root, args.date)
    output_path = project_root / PROJECT_SNAPSHOT_PATH
    if not args.no_write:
        write_project_ui_snapshot(snapshot, output_path)
    payload = {
        "ok": True,
        "summary": f"wrote {output_path}",
        "snapshot_path": str(output_path),
        "source_gap_count": len(snapshot.get("source_gaps", [])),
        "snapshot": snapshot,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"project snapshot: {output_path} ({payload['source_gap_count']} source gaps)")
    return 0
