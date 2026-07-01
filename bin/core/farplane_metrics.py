#!/usr/bin/env python3
"""Compile Farplane KPI observations into UI-ready metric series."""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import date as date_type
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

OBSERVATION_SNAPSHOTS_DIR = Path(".farplane/metrics/observations")
DAILY_METRICS_DIR = Path(".farplane/metrics/daily")


@dataclass(frozen=True)
class MetricDefinition:
    metric_id: str
    label: str
    axis: str
    product: str
    source_id: str
    aggregation: str
    cumulative: bool
    target: float | None
    target_direction: str
    unit: str
    display: str
    pinned: bool


@dataclass(frozen=True)
class SourceBinding:
    source_id: str
    enabled: bool
    source_type: str
    fetch: str
    path_or_account: str
    raw_snapshot_dir: str
    config: dict[str, Any]


@dataclass(frozen=True)
class SnapshotResult:
    date: str
    ui_snapshot_path: Path
    source_snapshot_paths: list[Path]
    metric_count: int
    source_gap_count: int


def today_utc() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def parse_target(value: str) -> float | None:
    raw = value.strip()
    if not raw or raw.lower() in {"null", "none", "source_gap"}:
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def normalize_target_direction(value: Any) -> str:
    raw = str(value or "").strip().lower()
    if raw in {"below", "at_most", "max", "lte", "<=", "under"}:
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


def parse_fenced_yaml(text: str, heading: str) -> dict[str, Any]:
    section = markdown_heading_section(text, heading)
    if not section:
        return {}
    fence_start = section.find("```yaml")
    if fence_start == -1:
        return {}
    yaml_start = section.find("\n", fence_start)
    if yaml_start == -1:
        return {}
    fence_end = section.find("```", yaml_start + 1)
    if fence_end == -1:
        return {}
    raw = section[yaml_start + 1 : fence_end]
    loaded = yaml.safe_load(raw) or {}
    return loaded if isinstance(loaded, dict) else {}


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
    loaded = yaml.safe_load(section[yaml_start + 1 : fence_end]) or {}
    return loaded if isinstance(loaded, dict) else {}


def label_from_metric(metric_id: str) -> str:
    return metric_id.replace("_", " ").capitalize()


def load_bindings_config(project_root: Path) -> dict[str, Any]:
    text = (project_root / "farplane" / "bindings.md").read_text(encoding="utf-8")
    return parse_fenced_yaml(text, "Project Config")


def load_goals_config(project_root: Path) -> dict[str, Any]:
    path = project_root / "farplane" / "goals.md"
    if not path.exists():
        return {}
    return parse_fenced_yaml(path.read_text(encoding="utf-8"), "Goals")


def parse_kpi_target(raw_item: Any, goal_id: str) -> tuple[str, dict[str, Any]] | None:
    if isinstance(raw_item, str):
        return raw_item, {"goal_id": goal_id}
    if not isinstance(raw_item, dict):
        return None
    if "id" in raw_item:
        metric_id = str(raw_item.get("id") or "").strip()
        if not metric_id:
            return None
        return metric_id, {
            "goal_id": goal_id,
            "target": raw_item.get("target"),
            "direction": raw_item.get("direction") or raw_item.get("comparator") or raw_item.get("operator"),
            "window": raw_item.get("window"),
        }
    if len(raw_item) == 1:
        metric_id, meta = next(iter(raw_item.items()))
        if not isinstance(meta, dict):
            return str(metric_id), {"goal_id": goal_id}
        return str(metric_id), {
            "goal_id": goal_id,
            "target": meta.get("target"),
            "direction": meta.get("direction") or meta.get("comparator") or meta.get("operator"),
            "window": meta.get("window"),
        }
    return None


def goal_kpi_targets(project_root: Path) -> dict[str, dict[str, Any]]:
    payload = load_goals_config(project_root)
    goals = payload.get("goals")
    if not isinstance(goals, dict):
        return {}
    targets: dict[str, dict[str, Any]] = {}
    for axis, axis_payload in goals.items():
        if not isinstance(axis_payload, dict):
            continue
        smart_goals = axis_payload.get("smart_goals")
        if not isinstance(smart_goals, list):
            continue
        for smart_goal in smart_goals:
            if not isinstance(smart_goal, dict):
                continue
            goal_id = str(smart_goal.get("id") or axis)
            for raw_item in smart_goal.get("kpis") or []:
                parsed = parse_kpi_target(raw_item, goal_id)
                if parsed is None:
                    continue
                metric_id, meta = parsed
                if "target" not in meta or meta.get("target") in {None, ""}:
                    targets.setdefault(metric_id, meta)
                    continue
                targets[metric_id] = meta
    return targets


def recipe_metric_definitions(project_root: Path) -> list[MetricDefinition]:
    payload = load_bindings_config(project_root)
    raw_metrics = payload.get("metrics")
    if not isinstance(raw_metrics, dict):
        return []
    kpi_targets = goal_kpi_targets(project_root)
    metrics: list[MetricDefinition] = []
    for metric_id, raw_recipe in raw_metrics.items():
        recipe = raw_recipe if isinstance(raw_recipe, dict) else {}
        raw_source = recipe.get("observation")
        source_id = str(raw_source.get("id") or metric_id) if isinstance(raw_source, dict) else str(metric_id)
        kind = str(recipe.get("kind") or recipe.get("aggregation") or "point")
        if kind == "daily_count":
            aggregation = "daily"
            cumulative = True
        else:
            aggregation = "daily" if kind == "daily" else "point"
            cumulative = bool(recipe.get("cumulative", False))
        goal_target = kpi_targets.get(str(metric_id), {})
        raw_target = goal_target.get("target") if "target" in goal_target else recipe.get("target", "")
        target_direction = normalize_target_direction(goal_target.get("direction") or recipe.get("target_direction"))
        metrics.append(
            MetricDefinition(
                metric_id=str(metric_id),
                label=str(recipe.get("label") or label_from_metric(str(metric_id))),
                axis="",
                product=str(recipe.get("product") or ""),
                source_id=source_id,
                aggregation=aggregation,
                cumulative=cumulative,
                target=parse_target(str(raw_target)),
                target_direction=target_direction,
                unit=str(recipe.get("unit") or ""),
                display=str(recipe.get("display") or "reading"),
                pinned=bool(recipe.get("pinned", False)),
            )
        )
    return metrics


def load_metric_definitions(project_root: Path) -> list[MetricDefinition]:
    return recipe_metric_definitions(project_root)


def load_provider_bindings(project_root: Path) -> dict[str, SourceBinding]:
    payload = load_bindings_config(project_root)
    metrics = payload.get("metrics")
    providers: dict[str, Any] = {}
    if isinstance(metrics, dict):
        for metric_id, recipe in metrics.items():
            if not isinstance(recipe, dict):
                continue
            raw_source = recipe.get("observation")
            if not isinstance(raw_source, dict):
                continue
            source_id = str(raw_source.get("id") or metric_id)
            providers.setdefault(source_id, raw_source)
    if not isinstance(providers, dict):
        return {}
    bindings: dict[str, SourceBinding] = {}
    for source_id, provider in providers.items():
        if not isinstance(provider, dict):
            continue
        path = str(provider.get("path") or provider.get("repo") or provider.get("writes") or "")
        source_type = str(provider.get("route") or provider.get("provider") or ("skill_snapshot" if provider.get("skill") else "local_json"))
        fetch = str(provider.get("skill") or provider.get("route") or provider.get("provider") or "farplane_metrics")
        raw_dir = str(provider.get("raw_snapshot_dir") or OBSERVATION_SNAPSHOTS_DIR / source_id)
        bindings[str(source_id)] = SourceBinding(
            source_id=str(source_id),
            enabled=True,
            source_type=source_type,
            fetch=fetch,
            path_or_account=path,
            raw_snapshot_dir=raw_dir,
            config=provider,
        )
    return bindings


def load_source_bindings(project_root: Path) -> dict[str, SourceBinding]:
    return load_provider_bindings(project_root)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            raw = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(raw, dict):
            rows.append(raw)
    return rows


def read_jsonl_glob(project_root: Path, pattern: str) -> list[dict[str, Any]]:
    paths = sorted(project_root.glob(pattern))
    rows: list[dict[str, Any]] = []
    for path in paths:
        rows.extend(read_jsonl(path))
    return rows


def row_date(row: dict[str, Any]) -> str:
    raw = row.get("ts") or row.get("timestamp") or row.get("created_at") or row.get("date") or ""
    parsed = parse_iso_datetime(raw)
    return parsed.date().isoformat() if parsed else str(raw)[:10]


def observation(metric_id: str, snapshot_date: str, value: float, evidence: list[str]) -> dict[str, Any]:
    return {
        "metric_id": metric_id,
        "date": snapshot_date,
        "value": value,
        "status": "available",
        "evidence_refs": evidence,
    }


def metric_reading_to_observation(metric_id: str, reading: Any, snapshot_date: str, evidence: list[str]) -> dict[str, Any] | None:
    if isinstance(reading, dict):
        value = reading.get("value")
        items = reading.get("items")
        gaps = reading.get("gaps")
    else:
        value = reading
        items = None
        gaps = None
    if not isinstance(value, (int, float)):
        return None
    payload = observation(metric_id, snapshot_date, float(value), evidence)
    if isinstance(items, list):
        payload["items"] = items
    if isinstance(gaps, list):
        payload["gaps"] = gaps
    return payload


def observations_from_metrics_map(raw: dict[str, Any], snapshot_date: str, evidence: list[str]) -> list[dict[str, Any]]:
    metrics = raw.get("metrics")
    if not isinstance(metrics, dict):
        return []
    observations: list[dict[str, Any]] = []
    for metric_id, reading in metrics.items():
        obs = metric_reading_to_observation(str(metric_id), reading, snapshot_date, evidence)
        if obs is not None:
            observations.append(obs)
    return observations


def fetch_reward_ledger(project_root: Path, binding: SourceBinding, snapshot_date: str) -> dict[str, Any]:
    path = project_root / binding.path_or_account
    rows = [row for row in read_jsonl(path) if row_date(row) and row_date(row) <= snapshot_date]
    accepted = [
        row
        for row in rows
        if row.get("outcome") in {"positive", "partial_positive"} and row.get("evidence")
    ]
    harness = [
        row
        for row in accepted
        if any(
            str(ref).startswith(("skills/", "bin/", "docs/", "farplane/", "qa/"))
            for ref in row.get("evidence", [])
        )
    ]
    proof = [
        row
        for row in accepted
        if "proof" in str(row.get("reason", "")).lower()
        or "review" in str(row.get("reason", "")).lower()
        or any("review" in str(ref).lower() or "receipt" in str(ref).lower() for ref in row.get("evidence", []))
    ]
    evidence = [binding.path_or_account]
    return {
        "source_id": binding.source_id,
        "status": "available" if path.exists() else "source_gap",
        "observations": [
            observation("accepted_output_events", snapshot_date, float(len(accepted)), evidence),
            observation("accepted_harness_improvements", snapshot_date, float(len(harness)), evidence),
            observation("proof_closure_events", snapshot_date, float(len(proof)), evidence),
        ],
        "gaps": [] if path.exists() else [f"missing:{binding.path_or_account}"],
    }


def fetch_decision_ledger(project_root: Path, binding: SourceBinding, snapshot_date: str) -> dict[str, Any]:
    path = project_root / binding.path_or_account
    rows = [row for row in read_jsonl(path) if row_date(row) and row_date(row) <= snapshot_date]
    execute_count = len([row for row in rows if row.get("action") == "execute_ready_tickets"])
    planning_count = len([row for row in rows if row.get("action") == "request_planning"])
    evidence = [binding.path_or_account]
    return {
        "source_id": binding.source_id,
        "status": "available" if path.exists() else "source_gap",
        "observations": [
            observation("pulse_execute_count", snapshot_date, float(execute_count), evidence),
            observation("pulse_request_planning_count", snapshot_date, float(planning_count), evidence),
        ],
        "gaps": [] if path.exists() else [f"missing:{binding.path_or_account}"],
    }


def parse_ticket_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text:
        return {}
    raw = text.split("\n---\n", 1)[0][4:]
    values: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line or line.startswith("  - "):
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"')
    return values


def iter_ticket_files(project_root: Path) -> list[Path]:
    roots = [project_root / "tickets", project_root / "tickets" / "archive"]
    tickets: list[Path] = []
    for root in roots:
        if root.exists():
            tickets.extend(root.glob("TASK-*/ticket.md"))
    return sorted(set(tickets))


def fetch_ticket_board(project_root: Path, binding: SourceBinding, snapshot_date: str) -> dict[str, Any]:
    tickets = sorted((project_root / "tickets").glob("TASK-*/ticket.md"))
    ready_unclaimed = 0
    stale_claims = 0
    current_date = date_type.fromisoformat(snapshot_date)
    for ticket in tickets:
        fm = parse_ticket_frontmatter(ticket)
        if not fm:
            continue
        if fm.get("phase") == "complete" or fm.get("status") in {"done", "failed"}:
            continue
        ready = fm.get("ready") == "true"
        approval_free = fm.get("approval_required") == "false"
        claimed = bool(fm.get("claimed_by"))
        human_gate = "review" in fm.get("next_action", "").lower() or "feedback" in fm.get("next_action", "").lower()
        if ready and approval_free and not claimed and not human_gate:
            ready_unclaimed += 1
        updated = fm.get("updated_at", "")[:10]
        if claimed and ready and updated:
            try:
                age_days = (current_date - date_type.fromisoformat(updated)).days
            except ValueError:
                age_days = 0
            if age_days >= 2:
                stale_claims += 1
    return {
        "source_id": binding.source_id,
        "status": "available",
        "observations": [
            observation("ready_unclaimed_ticket_count", snapshot_date, float(ready_unclaimed), [binding.path_or_account]),
            observation("stale_claim_count", snapshot_date, float(stale_claims), [binding.path_or_account]),
        ],
        "gaps": [],
    }


def fetch_eval_summary(project_root: Path, binding: SourceBinding, snapshot_date: str) -> dict[str, Any]:
    path = project_root / binding.path_or_account
    if not path.exists():
        return {"source_id": binding.source_id, "status": "source_gap", "observations": [], "gaps": [f"missing:{binding.path_or_account}"]}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"source_id": binding.source_id, "status": "source_gap", "observations": [], "gaps": [f"invalid_json:{binding.path_or_account}"]}
    rows = raw if isinstance(raw, list) else []
    eligible = [row for row in rows if isinstance(row, dict) and str(row.get("created_at", ""))[:10] <= snapshot_date]
    if not eligible:
        return {"source_id": binding.source_id, "status": "source_gap", "observations": [], "gaps": ["no_eval_summary_for_window"]}
    latest = sorted(eligible, key=lambda row: str(row.get("created_at", "")))[-1]
    value = latest.get("pass_rate")
    if not isinstance(value, (int, float)):
        return {"source_id": binding.source_id, "status": "source_gap", "observations": [], "gaps": ["latest_eval_missing_pass_rate"]}
    return {
        "source_id": binding.source_id,
        "status": "available",
        "observations": [observation("latest_eval_pass_rate", snapshot_date, float(value), [binding.path_or_account])],
        "gaps": [],
    }


def section_text(markdown: str, heading: str) -> str:
    return markdown_heading_section(markdown, heading)


def ticket_completion_date(fm: dict[str, str], snapshot_date: str) -> str:
    for key in ("completed_at", "closed_at", "updated_at"):
        raw = fm.get(key, "")
        parsed = parse_iso_datetime(raw)
        if parsed:
            return parsed.date().isoformat()
    return snapshot_date


def ticket_has_completion_proof(markdown: str) -> bool:
    done = section_text(markdown, "Done / Proof") or section_text(markdown, "Done")
    if not done:
        return False
    lowered = done.lower()
    proof_tokens = (
        "passed",
        "proof",
        "evidence",
        "artifact",
        "artifacts/",
        "review",
        "receipt",
        "verification",
    )
    return any(token in lowered for token in proof_tokens)


def parse_ticket_kpi_rewards(markdown: str) -> tuple[list[dict[str, str]], list[str]]:
    reward = section_text(markdown, "Reward")
    if not reward:
        return [], ["missing_reward_section"]
    payload = parse_fenced_yaml_from_section(reward)
    raw_rewards = payload.get("kpi_rewards")
    if not isinstance(raw_rewards, list):
        return [], ["missing_kpi_rewards"]
    rewards: list[dict[str, str]] = []
    gaps: list[str] = []
    for index, raw_reward in enumerate(raw_rewards):
        if not isinstance(raw_reward, dict):
            gaps.append(f"invalid_kpi_reward:{index}")
            continue
        kpi_id = str(raw_reward.get("kpi_id") or "").strip()
        expected_reward = str(raw_reward.get("expected_reward") or "").strip()
        if not kpi_id:
            gaps.append(f"missing_kpi_id:{index}")
            continue
        rewards.append({"kpi_id": kpi_id, "expected_reward": expected_reward})
    return rewards, gaps


def count_runway_decision_rows(section: str) -> int:
    decisions = {"continue", "narrow", "pause", "instrument", "stop", "escalate_to_revenue"}
    count = 0
    for raw in section.splitlines():
        line = raw.strip()
        if not line.startswith("|") or "---" in line or "Active project" in line:
            continue
        cells = [cell.strip(" `") for cell in line.strip("|").split("|")]
        if any(cell in decisions for cell in cells):
            count += 1
    return count


def fetch_runway_review_notes(project_root: Path, binding: SourceBinding, snapshot_date: str) -> dict[str, Any]:
    root = project_root / binding.path_or_account
    if not root.exists():
        return {"source_id": binding.source_id, "status": "source_gap", "observations": [], "gaps": [f"missing:{binding.path_or_account}"]}
    reports = sorted(path for path in root.glob("*.md") if path.name[:10] <= snapshot_date)
    reports_with_review = 0
    project_decisions = 0
    evidence: list[str] = []
    for report in reports:
        text = report.read_text(encoding="utf-8")
        runway = section_text(text, "Budget / Runway Review")
        if not runway:
            continue
        reports_with_review += 1
        project_decisions += count_runway_decision_rows(runway)
        evidence.append(str(report.relative_to(project_root)))
    if not reports_with_review:
        return {
            "source_id": binding.source_id,
            "status": "source_gap",
            "observations": [],
            "gaps": ["no_budget_runway_review_in_weekly_reports"],
        }
    return {
        "source_id": binding.source_id,
        "status": "available",
        "observations": [
            observation("weekly_runway_review_count", snapshot_date, float(reports_with_review), evidence),
            observation("projects_with_runway_decisions", snapshot_date, float(project_decisions), evidence),
        ],
        "gaps": [],
    }


def fetch_ticket_reward_feedback(project_root: Path, binding: SourceBinding, snapshot_date: str) -> dict[str, Any]:
    metric_sources = {metric.metric_id: metric.source_id for metric in load_metric_definitions(project_root)}
    ticket_reward_metrics = {
        metric_id for metric_id, source_id in metric_sources.items() if source_id == binding.source_id
    }
    counts: dict[str, float] = {}
    items_by_kpi: dict[str, list[dict[str, str]]] = {}
    gaps: list[str] = []

    for ticket in iter_ticket_files(project_root):
        markdown = ticket.read_text(encoding="utf-8")
        fm = parse_ticket_frontmatter(ticket)
        if not fm:
            continue
        if fm.get("phase") != "complete" and fm.get("status") != "done":
            continue
        completed_date = ticket_completion_date(fm, snapshot_date)
        if completed_date != snapshot_date:
            continue
        relative_ticket = str(ticket.relative_to(project_root))
        rewards, reward_gaps = parse_ticket_kpi_rewards(markdown)
        if reward_gaps:
            gaps.extend(f"{relative_ticket}:{gap}" for gap in reward_gaps)
        if not rewards:
            continue
        if not ticket_has_completion_proof(markdown):
            gaps.append(f"{relative_ticket}:missing_completion_proof")
            continue
        ticket_id = fm.get("ticket_id") or ticket.parent.name
        for reward in rewards:
            kpi_id = reward["kpi_id"]
            if kpi_id not in ticket_reward_metrics:
                configured_source = metric_sources.get(kpi_id, "unconfigured")
                gaps.append(f"{relative_ticket}:reward_attribution_not_metric_value:{kpi_id}:{configured_source}")
                continue
            counts[kpi_id] = counts.get(kpi_id, 0.0) + 1.0
            items_by_kpi.setdefault(kpi_id, []).append(
                {
                    "ticket_id": ticket_id,
                    "ticket": relative_ticket,
                    "expected_reward": reward.get("expected_reward", ""),
                }
            )

    observations: list[dict[str, Any]] = []
    for kpi_id in sorted(counts):
        payload = observation(kpi_id, snapshot_date, counts[kpi_id], [binding.path_or_account])
        payload["items"] = items_by_kpi.get(kpi_id, [])
        observations.append(payload)

    return {
        "source_id": binding.source_id,
        "status": "available" if observations else "source_gap",
        "observations": observations,
        "gaps": gaps if gaps else ([] if observations else ["no_completed_ticket_kpi_rewards_for_date"]),
    }


def run_gh_api(endpoint: str) -> tuple[Any | None, str | None]:
    try:
        result = subprocess.run(
            ["gh", "api", endpoint],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, str(exc)
    if result.returncode != 0:
        return None, result.stderr.strip() or result.stdout.strip() or f"gh_api_exit:{result.returncode}"
    try:
        return json.loads(result.stdout), None
    except json.JSONDecodeError as exc:
        return None, f"invalid_gh_json:{exc}"


def github_traffic_value(payload: dict[str, Any], row_key: str, field: str, snapshot_date: str) -> float | None:
    rows = payload.get(row_key)
    if isinstance(rows, list):
        for row in rows:
            if isinstance(row, dict) and str(row.get("timestamp", ""))[:10] == snapshot_date:
                value = row.get(field)
                return float(value) if isinstance(value, (int, float)) else None
    value = payload.get(field)
    return float(value) if isinstance(value, (int, float)) else None


def fetch_github_repo_feedback(project_root: Path, binding: SourceBinding, snapshot_date: str) -> dict[str, Any]:
    repo = binding.path_or_account.strip()
    evidence = [f"github:{repo}"] if repo else []
    if not repo or "/" not in repo:
        return {
            "source_id": binding.source_id,
            "status": "source_gap",
            "observations": [],
            "gaps": ["missing_github_repo_binding"],
        }

    observations: list[dict[str, Any]] = []
    gaps: list[str] = []

    repo_payload, repo_error = run_gh_api(f"repos/{repo}")
    if isinstance(repo_payload, dict):
        for metric_id, field in {
            "github_stars": "stargazers_count",
            "github_forks": "forks_count",
        }.items():
            value = repo_payload.get(field)
            if isinstance(value, (int, float)):
                observations.append(observation(metric_id, snapshot_date, float(value), evidence))
    else:
        gaps.append(f"github_repo:{repo_error or 'unavailable'}")

    open_issues, open_issues_error = run_gh_api(f"repos/{repo}/issues?state=open&per_page=100")
    if isinstance(open_issues, list):
        issues = [item for item in open_issues if isinstance(item, dict) and "pull_request" not in item]
        observations.append(observation("github_open_issues", snapshot_date, float(len(issues)), evidence))
    elif isinstance(repo_payload, dict) and isinstance(repo_payload.get("open_issues_count"), (int, float)):
        observations.append(observation("github_open_issues", snapshot_date, float(repo_payload["open_issues_count"]), evidence))
        gaps.append(f"github_open_issues_fallback_includes_prs:{open_issues_error or 'unavailable'}")
    else:
        gaps.append(f"github_open_issues:{open_issues_error or 'unavailable'}")

    open_prs, open_pr_error = run_gh_api(f"repos/{repo}/pulls?state=open&per_page=100")
    if isinstance(open_prs, list):
        observations.append(observation("github_open_prs", snapshot_date, float(len(open_prs)), evidence))
    else:
        gaps.append(f"github_open_prs:{open_pr_error or 'unavailable'}")

    closed_prs, closed_pr_error = run_gh_api(f"repos/{repo}/pulls?state=closed&per_page=100")
    if isinstance(closed_prs, list):
        merged = [
            item
            for item in closed_prs
            if isinstance(item, dict) and str(item.get("merged_at") or "")[:10] == snapshot_date
        ]
        observations.append(observation("github_merged_prs", snapshot_date, float(len(merged)), evidence))
    else:
        gaps.append(f"github_merged_prs:{closed_pr_error or 'unavailable'}")

    views, views_error = run_gh_api(f"repos/{repo}/traffic/views")
    if isinstance(views, dict):
        count = github_traffic_value(views, "views", "count", snapshot_date)
        if count is not None:
            observations.append(observation("github_views", snapshot_date, float(count), evidence))
    else:
        gaps.append(f"github_views:{views_error or 'unavailable'}")

    clones, clones_error = run_gh_api(f"repos/{repo}/traffic/clones")
    if isinstance(clones, dict):
        uniques = github_traffic_value(clones, "clones", "uniques", snapshot_date)
        if uniques is not None:
            observations.append(observation("github_unique_cloners", snapshot_date, float(uniques), evidence))
    else:
        gaps.append(f"github_unique_cloners:{clones_error or 'unavailable'}")

    return {
        "source_id": binding.source_id,
        "status": "available" if observations else "source_gap",
        "observations": observations,
        "gaps": gaps,
    }


def estimate_human_attention_minutes(times: list[datetime]) -> float:
    if not times:
        return 0.0
    ordered = sorted(times)
    total = 5.0
    for previous, current in zip(ordered, ordered[1:], strict=False):
        gap_minutes = max((current - previous).total_seconds() / 60.0, 1.0)
        total += min(gap_minutes, 30.0)
    return round(total, 2)


def accepted_reward_count(rows: list[dict[str, Any]], snapshot_date: str) -> int:
    return len(
        [
            row
            for row in rows
            if row_date(row) == snapshot_date
            and row.get("outcome") in {"positive", "partial_positive"}
            and row.get("evidence")
        ]
    )


def fetch_autonomy_time_feedback(project_root: Path, binding: SourceBinding, snapshot_date: str) -> dict[str, Any]:
    event_pattern = ".farplane/events/*.jsonl"
    spawned_path = project_root / ".farplane" / "automation" / "spawned-threads.jsonl"
    rewards_path = project_root / ".farplane" / "automation" / "rewards.jsonl"
    evidence = [event_pattern, ".farplane/automation/spawned-threads.jsonl", ".farplane/automation/rewards.jsonl"]
    gaps: list[str] = []

    event_root = project_root / ".farplane" / "events"
    event_rows = read_jsonl_glob(project_root, event_pattern)
    if not event_root.exists():
        gaps.append("missing:.farplane/events")

    spawned_rows = read_jsonl(spawned_path)
    if not spawned_path.exists():
        gaps.append("missing:.farplane/automation/spawned-threads.jsonl")

    reward_rows = read_jsonl(rewards_path)
    if not rewards_path.exists():
        gaps.append("missing:.farplane/automation/rewards.jsonl")

    spawned_thread_ids = {str(row.get("thread_id") or row.get("session_id")) for row in spawned_rows if row.get("thread_id") or row.get("session_id")}
    human_times_by_session: dict[str, list[datetime]] = {}
    for row in event_rows:
        if row_date(row) != snapshot_date:
            continue
        if str(row.get("event_type") or row.get("type") or "") not in {"turn_start", "user_prompt", "prompt"}:
            continue
        session_id = str(row.get("session_id") or row.get("thread_id") or "unknown")
        if session_id in spawned_thread_ids:
            continue
        parsed = parse_iso_datetime(row.get("ts") or row.get("timestamp") or row.get("created_at") or row.get("date"))
        if parsed is None:
            continue
        human_times_by_session.setdefault(session_id, []).append(parsed)

    spawned_today: dict[str, datetime] = {}
    latest_by_thread: dict[str, datetime] = {}
    rewarded_threads: set[str] = set()
    for row in spawned_rows:
        thread_id = str(row.get("thread_id") or row.get("session_id") or "")
        if not thread_id:
            continue
        parsed = parse_iso_datetime(row.get("ts") or row.get("timestamp") or row.get("created_at") or row.get("date"))
        if parsed is None:
            continue
        if row_date(row) == snapshot_date and str(row.get("status") or row.get("event") or "spawned") in {"spawned", "created", "started"}:
            spawned_today.setdefault(thread_id, parsed)
        if parsed.date().isoformat() <= snapshot_date:
            latest_by_thread[thread_id] = max(parsed, latest_by_thread.get(thread_id, parsed))
        if row_date(row) == snapshot_date and str(row.get("status") or row.get("event") or "").startswith("rewarded"):
            rewarded_threads.add(thread_id)

    autonomous_minutes = 0.0
    for thread_id, start in spawned_today.items():
        end = latest_by_thread.get(thread_id, start)
        elapsed = max((end - start).total_seconds() / 60.0, 0.0)
        autonomous_minutes += elapsed if elapsed > 0 else 30.0

    human_prompt_count = sum(len(times) for times in human_times_by_session.values())
    human_active_threads = len(human_times_by_session)
    human_minutes = sum(estimate_human_attention_minutes(times) for times in human_times_by_session.values())
    autonomous_thread_count = len(spawned_today)
    accepted_today = accepted_reward_count(reward_rows, snapshot_date)
    output_per_human_prompt = accepted_today / human_prompt_count if human_prompt_count else 0.0
    auto_time_ratio = autonomous_minutes / human_minutes if human_minutes else (autonomous_minutes if autonomous_minutes else 0.0)

    observations = [
        observation("human_prompt_count", snapshot_date, float(human_prompt_count), evidence),
        observation("human_active_thread_count", snapshot_date, float(human_active_threads), evidence),
        observation("human_attention_minutes_estimated", snapshot_date, round(float(human_minutes), 2), evidence),
        observation("autonomous_thread_count", snapshot_date, float(autonomous_thread_count), evidence),
        observation("autonomous_worker_elapsed_minutes", snapshot_date, round(float(autonomous_minutes), 2), evidence),
        observation("rewarded_autonomous_thread_count", snapshot_date, float(len(rewarded_threads)), evidence),
        observation("auto_time_ratio", snapshot_date, round(float(auto_time_ratio), 4), evidence),
        observation("output_per_human_prompt", snapshot_date, round(float(output_per_human_prompt), 4), evidence),
    ]
    all_inputs_missing = len(gaps) == 3
    return {
        "source_id": binding.source_id,
        "status": "source_gap" if all_inputs_missing else "available",
        "observations": [] if all_inputs_missing else observations,
        "gaps": gaps,
    }


def ticket_is_complete(fm: dict[str, str]) -> bool:
    return fm.get("phase") == "complete" or fm.get("status") == "done"


def load_ticket_thread_associations(project_root: Path, binding: SourceBinding) -> tuple[list[dict[str, Any]], list[str]]:
    configured_paths = binding.config.get("paths") if isinstance(binding.config.get("paths"), dict) else {}
    path_values = [
        configured_paths.get("associations"),
        binding.config.get("path"),
        ".farplane/state/ticket-thread-associations.jsonl",
        ".farplane/automation/spawned-threads.jsonl",
    ]
    rows: list[dict[str, Any]] = []
    gaps: list[str] = []
    seen_paths: set[Path] = set()
    for raw_path in path_values:
        if not raw_path:
            continue
        path = project_root / str(raw_path)
        if path in seen_paths:
            continue
        seen_paths.add(path)
        if not path.exists():
            gaps.append(f"missing:{str(raw_path)}")
            continue
        if path.suffix == ".json":
            try:
                loaded = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                gaps.append(f"invalid_json:{str(raw_path)}")
                continue
            raw_rows = loaded if isinstance(loaded, list) else loaded.get("associations") if isinstance(loaded, dict) else []
            if isinstance(raw_rows, list):
                rows.extend(row for row in raw_rows if isinstance(row, dict))
            continue
        rows.extend(read_jsonl(path))
    association_rows = [row for row in rows if row.get("ticket_id") and (row.get("thread_id") or row.get("session_id"))]
    if not association_rows and rows:
        gaps.append("no_ticket_thread_associations")
    return association_rows, gaps


def is_human_turn(row: dict[str, Any]) -> bool:
    actor = str(row.get("actor") or row.get("role") or row.get("source") or "").lower()
    if actor in {"assistant", "system", "automation", "tool"}:
        return False
    event_type = str(row.get("event_type") or row.get("type") or row.get("event") or "").lower()
    if event_type not in {"turn_start", "user_prompt", "prompt", "message"}:
        return False
    if str(row.get("is_initial_request") or "").lower() == "true":
        return False
    return actor in {"", "user", "human", "operator"} or "user" in actor or "human" in actor


def fetch_ticket_intervention_feedback(project_root: Path, binding: SourceBinding, snapshot_date: str) -> dict[str, Any]:
    completed_tickets: dict[str, tuple[Path, str, datetime]] = {}
    gaps: list[str] = []
    for ticket in iter_ticket_files(project_root):
        fm = parse_ticket_frontmatter(ticket)
        if not fm or not ticket_is_complete(fm):
            continue
        completed_date = ticket_completion_date(fm, snapshot_date)
        if completed_date != snapshot_date:
            continue
        completed_at = parse_iso_datetime(fm.get("completed_at") or fm.get("closed_at") or fm.get("updated_at") or snapshot_date)
        if completed_at is None:
            gaps.append(f"{ticket.relative_to(project_root)}:missing_completion_time")
            continue
        ticket_id = fm.get("ticket_id") or ticket.parent.name
        completed_tickets[ticket_id] = (ticket, str(ticket.relative_to(project_root)), completed_at)

    associations, association_gaps = load_ticket_thread_associations(project_root, binding)
    gaps.extend(association_gaps)
    if completed_tickets and not associations:
        gaps.append("missing_ticket_thread_association_source")

    associations_by_ticket: dict[str, list[dict[str, Any]]] = {}
    for row in associations:
        associations_by_ticket.setdefault(str(row.get("ticket_id")), []).append(row)

    event_pattern = ".farplane/events/*.jsonl"
    event_rows = read_jsonl_glob(project_root, event_pattern)
    if not (project_root / ".farplane" / "events").exists():
        gaps.append("missing:.farplane/events")

    total_interventions = 0
    intervention_free = 0
    counted_tickets = 0
    items: list[dict[str, Any]] = []
    evidence = [event_pattern, ".farplane/state/ticket-thread-associations.jsonl", ".farplane/automation/spawned-threads.jsonl"]

    for ticket_id, (ticket_path, relative_ticket, completed_at) in completed_tickets.items():
        ticket_associations = associations_by_ticket.get(ticket_id, [])
        if not ticket_associations:
            gaps.append(f"{relative_ticket}:missing_ticket_thread_association")
            continue
        thread_ids = {
            str(row.get("thread_id") or row.get("session_id"))
            for row in ticket_associations
            if row.get("thread_id") or row.get("session_id")
        }
        if len(thread_ids) != 1:
            gaps.append(f"{relative_ticket}:ambiguous_ticket_thread_association")
            continue
        association = ticket_associations[0]
        started_at = parse_iso_datetime(
            association.get("execution_started_at")
            or association.get("started_at")
            or association.get("created_at")
            or association.get("timestamp")
            or association.get("ts")
        )
        if started_at is None:
            gaps.append(f"{relative_ticket}:missing_execution_start")
            continue
        thread_id = next(iter(thread_ids))
        turn_count = 0
        for row in event_rows:
            if str(row.get("thread_id") or row.get("session_id") or "") != thread_id:
                continue
            if not is_human_turn(row):
                continue
            event_time = parse_iso_datetime(row.get("ts") or row.get("timestamp") or row.get("created_at") or row.get("date"))
            if event_time is None:
                continue
            if started_at < event_time <= completed_at:
                turn_count += 1
        counted_tickets += 1
        total_interventions += turn_count
        if turn_count == 0:
            intervention_free += 1
        items.append(
            {
                "ticket_id": ticket_id,
                "ticket": relative_ticket,
                "intervention_turns": turn_count,
                "execution_started_at": started_at.isoformat(),
                "completed_at": completed_at.isoformat(),
            }
        )

    observations: list[dict[str, Any]] = []
    if counted_tickets:
        rate = intervention_free / counted_tickets
        for metric_id, value in {
            "ticket_intervention_turn_count": float(total_interventions),
            "intervention_free_ticket_count": float(intervention_free),
            "auto_completion_rate": round(float(rate), 4),
        }.items():
            payload = observation(metric_id, snapshot_date, value, evidence)
            payload["items"] = items
            observations.append(payload)

    return {
        "source_id": binding.source_id,
        "status": "available" if observations else "source_gap",
        "observations": observations,
        "gaps": gaps if gaps else ([] if observations else ["no_completed_tickets_with_thread_associations_for_date"]),
    }


def fetch_manual_source(project_root: Path, binding: SourceBinding, snapshot_date: str) -> dict[str, Any]:
    if binding.source_type == "missing":
        setup_hint = binding.config.get("setup_hint") if isinstance(binding.config, dict) else None
        gaps = [f"source_not_configured:{binding.source_id}"]
        if setup_hint:
            gaps.append(f"setup_hint:{setup_hint}")
        return {"source_id": binding.source_id, "status": "source_gap", "observations": [], "gaps": gaps}
    if not binding.path_or_account:
        return {
            "source_id": binding.source_id,
            "status": "source_gap",
            "observations": [],
            "gaps": [f"missing_source_path:{binding.source_id}"],
        }
    path = project_root / binding.path_or_account
    if path.is_dir():
        return {
            "source_id": binding.source_id,
            "status": "source_gap",
            "observations": [],
            "gaps": [f"source_path_is_directory:{binding.source_id}:{binding.path_or_account}"],
        }
    if not path.exists():
        return {
            "source_id": binding.source_id,
            "status": "source_gap",
            "observations": [],
            "gaps": [f"source_not_available:{binding.source_id}"],
        }
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"source_id": binding.source_id, "status": "source_gap", "observations": [], "gaps": [f"invalid_json:{binding.path_or_account}"]}
    compact_observations = observations_from_metrics_map(raw if isinstance(raw, dict) else {}, snapshot_date, [binding.path_or_account])
    if compact_observations:
        return {
            "source_id": binding.source_id,
            "source": raw.get("source") or binding.source_id,
            "status": "available",
            "observations": compact_observations,
            "metrics": raw.get("metrics"),
            "gaps": raw.get("gaps") if isinstance(raw.get("gaps"), list) else [],
        }
    if isinstance(raw, dict) and raw.get("status") in {"blocked", "source_gap"}:
        return {
            "source_id": binding.source_id,
            "source": raw.get("source") or binding.source_id,
            "status": raw.get("status"),
            "observations": [],
            "metrics": raw.get("metrics"),
            "gaps": raw.get("gaps") if isinstance(raw.get("gaps"), list) else [f"source_not_available:{binding.source_id}"],
        }
    raw_observations = raw.get("observations") if isinstance(raw, dict) else None
    observations = [item for item in raw_observations if isinstance(item, dict)] if isinstance(raw_observations, list) else []
    filtered = [item for item in observations if item.get("date") == snapshot_date]
    return {
        "source_id": binding.source_id,
        "status": "available" if filtered else "source_gap",
        "observations": filtered,
        "gaps": [] if filtered else [f"no_reading_for_date:{binding.source_id}"],
    }


def fetch_source(project_root: Path, binding: SourceBinding, snapshot_date: str) -> dict[str, Any]:
    if binding.source_id == "pulse_reward_ledger":
        return fetch_reward_ledger(project_root, binding, snapshot_date)
    if binding.source_id == "pulse_decision_ledger":
        return fetch_decision_ledger(project_root, binding, snapshot_date)
    if binding.source_id == "ticket_board":
        return fetch_ticket_board(project_root, binding, snapshot_date)
    if binding.source_id == "eval_summary_index":
        return fetch_eval_summary(project_root, binding, snapshot_date)
    if binding.source_id == "runway_review_notes":
        return fetch_runway_review_notes(project_root, binding, snapshot_date)
    if binding.source_id == "ticket_reward_feedback":
        return fetch_ticket_reward_feedback(project_root, binding, snapshot_date)
    if binding.source_id == "github_repo_feedback":
        return fetch_github_repo_feedback(project_root, binding, snapshot_date)
    if binding.source_id == "autonomy_time_feedback":
        return fetch_autonomy_time_feedback(project_root, binding, snapshot_date)
    if binding.source_id == "ticket_intervention_feedback":
        return fetch_ticket_intervention_feedback(project_root, binding, snapshot_date)
    return fetch_manual_source(project_root, binding, snapshot_date)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_daily_metric_files(project_root: Path) -> list[Path]:
    root = project_root / DAILY_METRICS_DIR
    if not root.exists():
        return []
    return sorted(root.glob("*.json"))


def daily_metric_reading_to_observation(metric_id: str, reading: Any, snapshot_date: str) -> dict[str, Any] | None:
    if isinstance(reading, dict):
        status = str(reading.get("status") or "available")
        value = reading.get("value")
        payload = reading.get("payload")
    else:
        status = "available"
        value = reading
        payload = None
    if status != "available":
        return {
            "metric_id": metric_id,
            "date": snapshot_date,
            "value": None,
            "status": status,
            "payload": payload,
        }
    if not isinstance(value, (int, float)):
        return None
    obs = observation(metric_id, snapshot_date, float(value), [])
    obs["source_id"] = metric_id
    if isinstance(payload, dict):
        obs["payload"] = payload
    return obs


def load_daily_metric_observations(project_root: Path) -> list[dict[str, Any]]:
    observations: list[dict[str, Any]] = []
    for path in load_daily_metric_files(project_root):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if not isinstance(payload, dict):
            continue
        snapshot_date = str(payload.get("date") or path.stem)
        metrics = payload.get("metrics")
        if not isinstance(metrics, dict):
            continue
        for metric_id, reading in metrics.items():
            obs = daily_metric_reading_to_observation(str(metric_id), reading, snapshot_date)
            if obs is not None:
                observations.append(obs)
    return observations


def load_observation_snapshot_files(project_root: Path) -> list[Path]:
    paths: list[Path] = []
    root = project_root / OBSERVATION_SNAPSHOTS_DIR
    if root.exists():
        paths.extend(sorted(root.glob("*/*.json")))
    return paths


def load_historical_observations(project_root: Path) -> list[dict[str, Any]]:
    observations: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in load_daily_metric_observations(project_root):
        identity = json.dumps(item, sort_keys=True)
        if identity in seen:
            continue
        seen.add(identity)
        observations.append(item)
    for path in load_observation_snapshot_files(project_root):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        source_id = payload.get("source_id") if isinstance(payload, dict) else None
        raw = payload.get("observations") if isinstance(payload, dict) else None
        if isinstance(raw, list):
            for item in raw:
                if not isinstance(item, dict):
                    continue
                if source_id and not item.get("source_id"):
                    item = {**item, "source_id": source_id}
                identity = json.dumps(item, sort_keys=True)
                if identity in seen:
                    continue
                seen.add(identity)
                observations.append(item)
    return observations


def build_metric_snapshot(metric: MetricDefinition, observations: list[dict[str, Any]]) -> dict[str, Any]:
    def matches_metric_source(obs: dict[str, Any]) -> bool:
        return (
            obs.get("metric_id") == metric.metric_id
            and (
                not obs.get("source_id")
                or not metric.source_id
                or metric.source_id == metric.metric_id
                or obs.get("source_id") == metric.source_id
            )
        )

    metric_obs = sorted(
        [
            obs
            for obs in observations
            if matches_metric_source(obs) and obs.get("status", "available") == "available"
        ],
        key=lambda obs: str(obs.get("date", "")),
    )
    metric_gaps = sorted(
        [
            obs
            for obs in observations
            if matches_metric_source(obs) and obs.get("status", "available") != "available"
        ],
        key=lambda obs: str(obs.get("date", "")),
    )
    series: list[dict[str, Any]] = []
    running = 0.0
    hit_at: str | None = None
    hit_value: float | None = None
    target_direction = normalize_target_direction(metric.target_direction)
    for obs in metric_obs:
        try:
            value = float(obs.get("value"))
        except (TypeError, ValueError):
            continue
        point: dict[str, Any] = {"date": obs.get("date"), "value": value}
        if series:
            point["daily_diff"] = value - float(series[-1]["value"])
        else:
            point["daily_diff"] = None
        if "items" in obs:
            point["items"] = obs["items"]
        if "payload" in obs:
            point["payload"] = obs["payload"]
        comparison_value = value
        if metric.aggregation == "daily" and metric.cumulative:
            running += value
            point["cumulative"] = running
            comparison_value = running
        else:
            point["current"] = value
        target_hit = (
            comparison_value >= metric.target
            if target_direction == "above"
            else comparison_value <= metric.target
        ) if metric.target is not None else False
        if target_hit and hit_at is None:
            hit_at = str(obs.get("date"))
            hit_value = comparison_value
        series.append(point)
    current = series[-1]["value"] if series else None
    best_daily = max((float(point["value"]) for point in series), default=None)
    latest_gap = metric_gaps[-1] if metric_gaps else None
    source_gaps = []
    if latest_gap:
        gap: dict[str, Any] = {
            "date": latest_gap.get("date"),
            "status": latest_gap.get("status"),
            "reason": latest_gap.get("status"),
        }
        if "payload" in latest_gap:
            gap["payload"] = latest_gap["payload"]
        source_gaps.append(gap)
    elif not series:
        source_gaps.append({"reason": "no available observation for metric"})
    return {
        "metric_id": metric.metric_id,
        "label": metric.label,
        "axis": metric.axis,
        "product": metric.product,
        "source_id": metric.source_id,
        "aggregation": metric.aggregation,
        "cumulative": metric.cumulative,
        "target": metric.target,
        "target_direction": target_direction,
        "unit": metric.unit,
        "display": metric.display,
        "pinned": metric.pinned,
        "status": "available" if series else str(latest_gap.get("status") if latest_gap else "source_gap"),
        "current": current,
        "series": series,
        "best_daily": best_daily,
        "source_gaps": source_gaps,
        "target_hit": {"hit_at": hit_at, "hit_value": hit_value} if hit_at else None,
    }


def write_ui_metric_snapshot(
    project_root: Path,
    date_value: str,
    metrics: list[MetricDefinition],
    observations: list[dict[str, Any]],
    source_paths: list[Path],
) -> SnapshotResult:
    metric_payloads = [build_metric_snapshot(metric, observations) for metric in metrics]
    source_gap_count = len([metric for metric in metric_payloads if metric["status"] != "available"])
    ui_payload = {
        "schema_version": 1,
        "project": "Farplane",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "snapshot_date": date_value,
        "metrics": metric_payloads,
        "source_gaps": [
            {
                "metric_id": metric["metric_id"],
                "source_id": metric["source_id"],
                "reason": metric["source_gaps"][0]["reason"],
            }
            for metric in metric_payloads
            if metric["status"] != "available"
        ],
        "daily_metrics_root": str(project_root / DAILY_METRICS_DIR),
    }
    dated_ui = project_root / ".farplane" / "metrics" / "ui" / f"{date_value}.json"
    latest_ui = project_root / ".farplane" / "metrics" / "ui" / "latest.json"
    write_json(dated_ui, ui_payload)
    write_json(latest_ui, ui_payload)
    return SnapshotResult(date_value, latest_ui, source_paths, len(metric_payloads), source_gap_count)


def compile_metric_snapshots(project_root: Path, snapshot_date: str | None = None) -> SnapshotResult:
    project_root = project_root.resolve()
    date_value = snapshot_date or today_utc()
    metrics = load_metric_definitions(project_root)
    observations = load_historical_observations(project_root)
    return write_ui_metric_snapshot(project_root, date_value, metrics, observations, [])


def generate_metric_snapshots(project_root: Path, snapshot_date: str | None = None) -> SnapshotResult:
    project_root = project_root.resolve()
    date_value = snapshot_date or today_utc()
    metrics = load_metric_definitions(project_root)
    bindings = load_source_bindings(project_root)
    source_paths: list[Path] = []

    for source_id in sorted({metric.source_id for metric in metrics}):
        binding = bindings.get(source_id)
        if not binding:
            payload = {"source_id": source_id, "date": date_value, "status": "source_gap", "observations": [], "gaps": ["missing_source_binding"]}
            raw_dir = project_root / OBSERVATION_SNAPSHOTS_DIR / source_id
        else:
            payload = fetch_source(project_root, binding, date_value)
            payload["date"] = date_value
            raw_dir = project_root / binding.raw_snapshot_dir
        for obs in payload.get("observations") or []:
            if isinstance(obs, dict):
                obs.setdefault("source_id", source_id)
        path = raw_dir / f"{date_value}.json"
        write_json(path, payload)
        source_paths.append(path)

    observations = load_historical_observations(project_root)
    return write_ui_metric_snapshot(project_root, date_value, metrics, observations, source_paths)


def run_snapshot(args: argparse.Namespace) -> int:
    result = generate_metric_snapshots(Path(args.project_root), args.date)
    payload = {
        "ok": True,
        "date": result.date,
        "ui_snapshot": str(result.ui_snapshot_path),
        "source_snapshots": [str(path) for path in result.source_snapshot_paths],
        "metric_count": result.metric_count,
        "source_gap_count": result.source_gap_count,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"wrote {result.ui_snapshot_path} ({result.metric_count} metrics, {result.source_gap_count} source gaps)")
    return 0


def run_compile(args: argparse.Namespace) -> int:
    result = compile_metric_snapshots(Path(args.project_root), args.date)
    payload = {
        "ok": True,
        "date": result.date,
        "ui_snapshot": str(result.ui_snapshot_path),
        "daily_metrics_root": str(Path(args.project_root).resolve() / DAILY_METRICS_DIR),
        "metric_count": result.metric_count,
        "source_gap_count": result.source_gap_count,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"compiled {result.ui_snapshot_path} ({result.metric_count} metrics, {result.source_gap_count} source gaps)")
    return 0
