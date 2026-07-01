#!/usr/bin/env python3
"""Generate Farplane KPI source snapshots and UI-ready metric series."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date as date_type
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


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
    unit: str
    display: str


@dataclass(frozen=True)
class SourceBinding:
    source_id: str
    enabled: bool
    source_type: str
    fetch: str
    path_or_account: str
    raw_snapshot_dir: str


@dataclass(frozen=True)
class SnapshotResult:
    date: str
    ui_snapshot_path: Path
    source_snapshot_paths: list[Path]
    metric_count: int
    source_gap_count: int


def today_utc() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def parse_bool(value: str) -> bool:
    return value.strip().lower() == "true"


def parse_target(value: str) -> float | None:
    raw = value.strip()
    if not raw or raw.lower() in {"null", "none", "source_gap"}:
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def parse_markdown_table(text: str, heading: str) -> list[dict[str, str]]:
    marker = f"## {heading}"
    start = text.find(marker)
    if start == -1:
        return []
    section = text[start + len(marker) :]
    next_heading = section.find("\n## ")
    if next_heading != -1:
        section = section[:next_heading]
    lines = [line.strip() for line in section.splitlines() if line.strip().startswith("|")]
    if len(lines) < 3:
        return []
    headers = [cell.strip() for cell in lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in lines[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != len(headers):
            continue
        rows.append(dict(zip(headers, cells, strict=True)))
    return rows


def parse_fenced_yaml(text: str, heading: str) -> dict[str, Any]:
    marker = f"## {heading}"
    start = text.find(marker)
    if start == -1:
        return {}
    section = text[start + len(marker) :]
    next_heading = section.find("\n## ")
    if next_heading != -1:
        section = section[:next_heading]
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


def label_from_metric(metric_id: str) -> str:
    return metric_id.replace("_", " ").capitalize()


def parse_kpi_item(item: Any) -> tuple[str, dict[str, Any]]:
    if isinstance(item, str):
        return item, {}
    if isinstance(item, dict):
        if "id" in item:
            metric_id = str(item["id"])
            return metric_id, {key: value for key, value in item.items() if key != "id"}
        if len(item) == 1:
            metric_id, meta = next(iter(item.items()))
            return str(metric_id), meta if isinstance(meta, dict) else {}
    return "", {}


def load_metric_definitions_from_yaml(project_root: Path) -> list[MetricDefinition]:
    goals_payload = parse_fenced_yaml((project_root / "farplane" / "goals.md").read_text(encoding="utf-8"), "Goals")
    goals = goals_payload.get("goals")
    if not isinstance(goals, dict):
        return []
    provider_by_metric = provider_map_by_metric(project_root)
    seen: set[str] = set()
    metrics: list[MetricDefinition] = []
    for axis, axis_payload in goals.items():
        if not isinstance(axis_payload, dict):
            continue
        smart_goals = axis_payload.get("smart_goals") or []
        if not isinstance(smart_goals, list):
            continue
        for smart_goal in smart_goals:
            if not isinstance(smart_goal, dict):
                continue
            for raw_item in smart_goal.get("kpis") or []:
                metric_id, meta = parse_kpi_item(raw_item)
                if not metric_id or metric_id in seen:
                    continue
                seen.add(metric_id)
                metrics.append(
                    MetricDefinition(
                        metric_id=metric_id,
                        label=str(meta.get("label") or label_from_metric(metric_id)),
                        axis=str(axis),
                        product=str(meta.get("product") or ""),
                        source_id=str(meta.get("source") or provider_by_metric.get(metric_id, "")),
                        aggregation="point",
                        cumulative=False,
                        target=parse_target(str(meta.get("target", ""))),
                        unit=str(meta.get("unit") or ""),
                        display="reading",
                    )
                )
    return metrics


def load_metric_definitions(project_root: Path) -> list[MetricDefinition]:
    yaml_metrics = load_metric_definitions_from_yaml(project_root)
    if yaml_metrics:
        return yaml_metrics
    rows = parse_markdown_table((project_root / "farplane" / "goals.md").read_text(encoding="utf-8"), "Tracked KPIs")
    metrics: list[MetricDefinition] = []
    for row in rows:
        metric_id = row.get("Metric", "").strip()
        aggregation = row.get("Aggregation", "").strip()
        if not metric_id or aggregation not in {"point", "daily"}:
            continue
        metrics.append(
            MetricDefinition(
                metric_id=metric_id,
                label=row.get("Label", metric_id).strip() or metric_id,
                axis=row.get("Axis", "").strip(),
                product=row.get("Product", "").strip(),
                source_id=row.get("Source", "").strip(),
                aggregation=aggregation,
                cumulative=parse_bool(row.get("Cumulative", "false")),
                target=parse_target(row.get("Target", "")),
                unit=row.get("Unit", "").strip(),
                display=row.get("Display", "").strip() or "line",
            )
        )
    return metrics


def load_provider_bindings(project_root: Path) -> dict[str, SourceBinding]:
    payload = parse_fenced_yaml((project_root / "farplane" / "bindings.md").read_text(encoding="utf-8"), "Metric Providers")
    providers = payload.get("metric_providers")
    if not isinstance(providers, dict):
        return {}
    bindings: dict[str, SourceBinding] = {}
    for source_id, provider in providers.items():
        if not isinstance(provider, dict):
            continue
        path = str(provider.get("path") or provider.get("writes") or "")
        source_type = str(provider.get("provider") or ("skill_snapshot" if provider.get("skill") else "local_json"))
        fetch = str(provider.get("skill") or provider.get("provider") or "farplane_metrics")
        raw_dir = str(provider.get("raw_snapshot_dir") or f".farplane/metrics/source-snapshots/{source_id}")
        bindings[str(source_id)] = SourceBinding(
            source_id=str(source_id),
            enabled=True,
            source_type=source_type,
            fetch=fetch,
            path_or_account=path,
            raw_snapshot_dir=raw_dir,
        )
    return bindings


def provider_map_by_metric(project_root: Path) -> dict[str, str]:
    payload = parse_fenced_yaml((project_root / "farplane" / "bindings.md").read_text(encoding="utf-8"), "Metric Providers")
    providers = payload.get("metric_providers")
    if not isinstance(providers, dict):
        return {}
    mapping: dict[str, str] = {}
    for source_id, provider in providers.items():
        if not isinstance(provider, dict):
            continue
        for metric_id in provider.get("provides") or []:
            mapping[str(metric_id)] = str(source_id)
    return mapping


def load_source_bindings(project_root: Path) -> dict[str, SourceBinding]:
    provider_bindings = load_provider_bindings(project_root)
    if provider_bindings:
        return provider_bindings
    rows = parse_markdown_table(
        (project_root / "farplane" / "bindings.md").read_text(encoding="utf-8"),
        "Metric Source Bindings",
    )
    bindings: dict[str, SourceBinding] = {}
    for row in rows:
        source_id = row.get("Source", "").strip()
        if not source_id:
            continue
        bindings[source_id] = SourceBinding(
            source_id=source_id,
            enabled=parse_bool(row.get("Enabled", "false")),
            source_type=row.get("Type", "").strip(),
            fetch=row.get("Fetch", "").strip(),
            path_or_account=row.get("Path Or Account", "").strip(),
            raw_snapshot_dir=row.get("Raw Snapshot Dir", "").strip(),
        )
    return bindings


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


def row_date(row: dict[str, Any]) -> str:
    raw = row.get("ts") or row.get("created_at") or row.get("date") or ""
    return str(raw)[:10]


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
    marker = f"## {heading}"
    start = markdown.find(marker)
    if start == -1:
        return ""
    section = markdown[start + len(marker) :]
    next_heading = section.find("\n## ")
    if next_heading != -1:
        section = section[:next_heading]
    return section.strip()


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


def fetch_manual_source(project_root: Path, binding: SourceBinding, snapshot_date: str) -> dict[str, Any]:
    path = project_root / binding.path_or_account
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
    return fetch_manual_source(project_root, binding, snapshot_date)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_historical_observations(project_root: Path) -> list[dict[str, Any]]:
    root = project_root / ".farplane" / "metrics" / "source-snapshots"
    observations: list[dict[str, Any]] = []
    if not root.exists():
        return observations
    for path in sorted(root.glob("*/*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        raw = payload.get("observations") if isinstance(payload, dict) else None
        if isinstance(raw, list):
            observations.extend(item for item in raw if isinstance(item, dict))
    return observations


def build_metric_snapshot(metric: MetricDefinition, observations: list[dict[str, Any]]) -> dict[str, Any]:
    metric_obs = sorted(
        [obs for obs in observations if obs.get("metric_id") == metric.metric_id and obs.get("status", "available") == "available"],
        key=lambda obs: str(obs.get("date", "")),
    )
    series: list[dict[str, Any]] = []
    running = 0.0
    hit_at: str | None = None
    hit_value: float | None = None
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
        comparison_value = value
        if metric.aggregation == "daily" and metric.cumulative:
            running += value
            point["cumulative"] = running
            comparison_value = running
        else:
            point["current"] = value
        if metric.target is not None and hit_at is None and comparison_value >= metric.target:
            hit_at = str(obs.get("date"))
            hit_value = comparison_value
        series.append(point)
    current = series[-1]["value"] if series else None
    return {
        "metric_id": metric.metric_id,
        "label": metric.label,
        "axis": metric.axis,
        "product": metric.product,
        "source_id": metric.source_id,
        "aggregation": metric.aggregation,
        "cumulative": metric.cumulative,
        "target": metric.target,
        "unit": metric.unit,
        "display": metric.display,
        "status": "available" if series else "source_gap",
        "current": current,
        "series": series,
        "target_hit": {"hit_at": hit_at, "hit_value": hit_value} if hit_at else None,
    }


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
            raw_dir = project_root / ".farplane" / "metrics" / "source-snapshots" / source_id
        else:
            payload = fetch_source(project_root, binding, date_value)
            payload["date"] = date_value
            raw_dir = project_root / binding.raw_snapshot_dir
        path = raw_dir / f"{date_value}.json"
        write_json(path, payload)
        source_paths.append(path)

    observations = load_historical_observations(project_root)
    metric_payloads = [build_metric_snapshot(metric, observations) for metric in metrics]
    source_gap_count = len([metric for metric in metric_payloads if metric["status"] == "source_gap"])
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
                "reason": "no available observation for metric",
            }
            for metric in metric_payloads
            if metric["status"] == "source_gap"
        ],
    }
    dated_ui = project_root / ".farplane" / "metrics" / "ui" / f"{date_value}.json"
    latest_ui = project_root / ".farplane" / "metrics" / "ui" / "latest.json"
    write_json(dated_ui, ui_payload)
    write_json(latest_ui, ui_payload)
    return SnapshotResult(date_value, latest_ui, source_paths, len(metric_payloads), source_gap_count)


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
