#!/usr/bin/env python3
"""Resolve Work Pulse hard-guard freshness before planning.

``begin`` reads the configured guards and emits the refresh providers that the
Pulse must dispatch. ``finish`` reloads observations after that dispatch and
classifies the result. Refresh work is deliberately kept outside the ticket
portfolio; this helper only owns the deterministic lifecycle and receipt.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from datetime import date
from pathlib import Path
from typing import Any

import yaml


OPERATORS = {
    "less_than": lambda value, threshold: value < threshold,
    "less_than_or_equal": lambda value, threshold: value <= threshold,
    "greater_than": lambda value, threshold: value > threshold,
    "greater_than_or_equal": lambda value, threshold: value >= threshold,
    "equal": lambda value, threshold: value == threshold,
}


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected mapping: {path}")
    return value


def selected_guard_ids(harness: dict[str, Any]) -> list[str]:
    refs = harness.get("metric_refs") if isinstance(harness.get("metric_refs"), dict) else {}
    rows = refs.get("guards") if isinstance(refs.get("guards"), list) else []
    result: list[str] = []
    for row in rows:
        metric_id = row.get("metric_id") if isinstance(row, dict) else row
        if metric_id and str(metric_id) not in result:
            result.append(str(metric_id))
    return result


def latest_observation(project_root: Path, metric_id: str, through: str) -> dict[str, Any] | None:
    root = project_root / ".farplane" / "metrics" / "observations"
    found: list[dict[str, Any]] = []
    for path in sorted(root.glob("*/*.json")) if root.exists() else []:
        if path.stem > through:
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        rows = payload.get("observations") if isinstance(payload, dict) else None
        if not isinstance(rows, list):
            continue
        for row in rows:
            if isinstance(row, dict) and row.get("metric_id") == metric_id and str(row.get("date") or "") <= through:
                found.append(row)
    return max(found, key=lambda row: str(row.get("date") or ""), default=None)


def guard_state(project_root: Path, as_of: str) -> dict[str, Any]:
    metrics_doc = load_yaml(project_root / "farplane" / "metrics.yaml")
    harness = load_yaml(project_root / "farplane" / "harness.yaml")
    metrics = metrics_doc.get("metrics") if isinstance(metrics_doc.get("metrics"), dict) else {}
    refreshers = metrics_doc.get("refreshers") if isinstance(metrics_doc.get("refreshers"), dict) else {}
    rows: list[dict[str, Any]] = []
    refreshes: dict[str, dict[str, Any]] = {}
    target_date = date.fromisoformat(as_of)

    for metric_id in selected_guard_ids(harness):
        definition = metrics.get(metric_id) if isinstance(metrics.get(metric_id), dict) else None
        if definition is None:
            rows.append({"metric_id": metric_id, "state": "source_gap", "reason": "missing_metric_definition"})
            continue
        guard = definition.get("guard") if isinstance(definition.get("guard"), dict) else {}
        operator = str(guard.get("operator") or "")
        threshold = guard.get("threshold")
        observation = latest_observation(project_root, metric_id, as_of)
        reason = None
        state = "current"
        if observation is None:
            state, reason = "needs_refresh", "missing_observation"
        elif observation.get("status") != "available" or not isinstance(observation.get("value"), (int, float)):
            state, reason = "needs_refresh", f"observation_status:{observation.get('status') or 'missing'}"
        else:
            observed = date.fromisoformat(str(observation.get("date"))[:10])
            max_age = definition.get("max_age_days")
            if isinstance(max_age, int) and (target_date - observed).days > max_age:
                state, reason = "needs_refresh", f"stale:{(target_date - observed).days}d>{max_age}d"
        row = {
            "metric_id": metric_id,
            "state": state,
            "reason": reason,
            "observation": observation,
            "operator": operator,
            "threshold": threshold,
        }
        if state == "current":
            comparator = OPERATORS.get(operator)
            if comparator is None or not isinstance(threshold, (int, float)):
                row.update({"state": "source_gap", "reason": "invalid_guard_rule"})
            elif not comparator(float(observation["value"]), float(threshold)):
                row.update({"state": "failing", "reason": "guard_threshold_failed"})
        rows.append(row)
        if row["state"] == "needs_refresh":
            refresh_ref = str(definition.get("refresh_ref") or f"metric:{metric_id}")
            provider = refreshers.get(refresh_ref) if isinstance(refreshers.get(refresh_ref), dict) else {}
            instruction = definition.get("refresh") or provider.get("refresh")
            dispatch = refreshes.setdefault(
                refresh_ref,
                {"refresh_ref": refresh_ref, "instruction": instruction, "metric_ids": []},
            )
            dispatch["metric_ids"].append(metric_id)
    return {"as_of": as_of, "guards": rows, "refresh_dispatches": list(refreshes.values())}


def begin(project_root: Path, as_of: str) -> dict[str, Any]:
    state = guard_state(project_root, as_of)
    if any(row["state"] == "source_gap" for row in state["guards"]):
        status = "source_gap"
    elif any(row["state"] == "failing" for row in state["guards"]):
        status = "blocked_guard"
    elif state["refresh_dispatches"]:
        status = "refresh_required"
    else:
        status = "ready"
    return {**state, "status": status, "planner_allowed": status == "ready", "wave_slots_consumed": 0}


def finish(
    project_root: Path,
    as_of: str,
    dispatched_refs: list[str],
    required_refs: list[str] | None = None,
) -> dict[str, Any]:
    state = begin(project_root, as_of)
    required = {item["refresh_ref"] for item in state["refresh_dispatches"]}
    missing_dispatches = set(required_refs or []).difference(dispatched_refs)
    if missing_dispatches:
        status = "source_gap"
        reason = "required_refresh_not_dispatched"
    elif required:
        status = "source_gap"
        reason = "refresh_did_not_produce_current_observation"
    elif state["status"] == "blocked_guard":
        status, reason = "blocked_guard", "refreshed_guard_failed"
    elif state["status"] == "ready":
        status, reason = "ready", "guards_current_and_healthy"
    else:
        status, reason = "source_gap", "guard_preflight_unresolved"
    return {
        **state,
        "status": status,
        "reason": reason,
        "dispatched_refresh_refs": sorted(set(dispatched_refs)),
        "missing_dispatch_refs": sorted(missing_dispatches),
        "planner_allowed": status == "ready",
        "wave_slots_consumed": 0,
    }


def begin_planning_if_ready(
    project_root: Path,
    as_of: str,
    dispatched_refs: list[str],
    required_refs: list[str],
    planning_input: dict[str, Any],
    wave_size: int,
) -> dict[str, Any]:
    """Gate the planning fingerprint on a reloaded, healthy guard receipt."""

    receipt = finish(project_root, as_of, dispatched_refs, required_refs)
    if not receipt["planner_allowed"]:
        return {"preflight": receipt, "planning": None}
    module_path = Path(__file__).with_name("plan_wave_guard.py")
    spec = importlib.util.spec_from_file_location("pulse_plan_wave_guard", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load plan_wave_guard.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    guarded_input = {**planning_input, "guard_preflight": receipt}
    return {
        "preflight": receipt,
        "planning": module.begin_wave(project_root, guarded_input, wave_size),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("begin", "finish", "plan"))
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--date", required=True)
    parser.add_argument("--dispatched-ref", action="append", default=[])
    parser.add_argument("--required-ref", action="append", default=[])
    parser.add_argument("--planning-input", type=Path)
    parser.add_argument("--wave-size", type=int, default=5)
    args = parser.parse_args()
    if args.command == "begin":
        result = begin(args.project_root.resolve(), args.date)
    elif args.command == "finish":
        result = finish(args.project_root.resolve(), args.date, args.dispatched_ref, args.required_ref)
    else:
        if args.planning_input is None:
            parser.error("plan requires --planning-input")
        planning_input = json.loads(args.planning_input.read_text(encoding="utf-8"))
        if not isinstance(planning_input, dict):
            parser.error("--planning-input must contain a JSON object")
        result = begin_planning_if_ready(
            args.project_root.resolve(), args.date, args.dispatched_ref,
            args.required_ref, planning_input, args.wave_size,
        )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
