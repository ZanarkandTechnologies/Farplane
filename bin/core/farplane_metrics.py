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


def load_metric_definitions(project_root: Path) -> list[MetricDefinition]:
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


def load_source_bindings(project_root: Path) -> dict[str, SourceBinding]:
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


def fetch_reward_ledger(project_root: Path, binding: SourceBinding, snapshot_date: str) -> dict[str, Any]:
    path = project_root / binding.path_or_account
    rows = [row for row in read_jsonl(path) if row_date(row) == snapshot_date]
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
    rows = [row for row in read_jsonl(path) if row_date(row) == snapshot_date]
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


def fetch_manual_source(project_root: Path, binding: SourceBinding, snapshot_date: str) -> dict[str, Any]:
    path = project_root / binding.path_or_account
    if not binding.enabled or not path.exists():
        return {
            "source_id": binding.source_id,
            "status": "source_gap",
            "observations": [],
            "gaps": [f"manual_source_not_configured:{binding.source_id}"],
        }
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"source_id": binding.source_id, "status": "source_gap", "observations": [], "gaps": [f"invalid_json:{binding.path_or_account}"]}
    raw_observations = raw.get("observations") if isinstance(raw, dict) else None
    observations = [item for item in raw_observations if isinstance(item, dict)] if isinstance(raw_observations, list) else []
    filtered = [item for item in observations if item.get("date") == snapshot_date]
    return {"source_id": binding.source_id, "status": "available", "observations": filtered, "gaps": []}


def fetch_source(project_root: Path, binding: SourceBinding, snapshot_date: str) -> dict[str, Any]:
    if binding.source_id == "pulse_reward_ledger":
        return fetch_reward_ledger(project_root, binding, snapshot_date)
    if binding.source_id == "pulse_decision_ledger":
        return fetch_decision_ledger(project_root, binding, snapshot_date)
    if binding.source_id == "ticket_board":
        return fetch_ticket_board(project_root, binding, snapshot_date)
    if binding.source_id == "eval_summary_index":
        return fetch_eval_summary(project_root, binding, snapshot_date)
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
        comparison_value = value
        if metric.aggregation == "daily" and metric.cumulative:
            running += value
            point["cumulative"] = running
            comparison_value = running
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
