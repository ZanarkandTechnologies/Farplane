"""Autonomy and intervention metric reducers used by Farplane Core."""

from __future__ import annotations

import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from bin.core.farplane_metric_shared import (
    iter_ticket_files,
    parse_iso_datetime,
    parse_ticket_frontmatter,
    read_jsonl,
    read_jsonl_glob,
    row_date,
    ticket_has_acceptance_evidence,
    ticket_has_completion_proof,
    ticket_is_complete,
)

def estimate_human_attention_minutes(times: list[datetime]) -> float:
    if not times:
        return 0.0
    ordered = sorted(times)
    total = 5.0
    for previous, current in zip(ordered, ordered[1:], strict=False):
        gap = max((current - previous).total_seconds() / 60.0, 1.0)
        total += min(gap, 30.0)
    return round(total, 2)


def accepted_reward_count(rows: list[dict[str, Any]], date: str) -> int:
    return len(
        [
            row
            for row in rows
            if row_date(row) == date and row.get("outcome") in {"positive", "partial_positive"} and row.get("evidence")
        ]
    )


def reward_ticket_ids(rows: list[dict[str, Any]], date: str) -> set[str]:
    ids: set[str] = set()
    for row in rows:
        if row_date(row) != date or row.get("outcome") not in {"positive", "partial_positive"}:
            continue
        evidence = row.get("evidence")
        if not isinstance(evidence, list):
            continue
        for ref in evidence:
            match = re.search(r"\b(TASK-\d{4})\b", str(ref))
            if match:
                ids.add(match.group(1))
    return ids


def calculate_autonomy_time_ratio(runtime_dir: Path, date: str) -> dict[str, Any]:
    """calculate_autonomy_time_ratio(runtime_dir, date) -> MetricReading."""
    root = runtime_dir.resolve()
    event_rows = read_jsonl_glob(root, "events/*.jsonl")
    association_rows = read_jsonl(root / "state" / "ticket-thread-associations.jsonl")
    reward_rows = read_jsonl(root / "automation" / "rewards.jsonl")
    gaps = []
    if not (root / "events").exists():
        gaps.append("missing:events")
    if not (root / "state" / "ticket-thread-associations.jsonl").exists():
        gaps.append("missing:state/ticket-thread-associations.jsonl")
    if not (root / "automation" / "rewards.jsonl").exists():
        gaps.append("missing:automation/rewards.jsonl")
    if len(gaps) == 3:
        return {"value": None, "status": "source_gap", "payload": {"gaps": gaps}}

    autonomous_thread_ids = {
        str(row.get("thread_id") or row.get("session_id"))
        for row in association_rows
        if row.get("thread_id") or row.get("session_id")
    }


    human_times_by_session: dict[str, list[datetime]] = {}
    for row in event_rows:
        if row_date(row) != date:
            continue
        if str(row.get("event_type") or row.get("type") or "") not in {"turn_start", "user_prompt", "prompt"}:
            continue
        session_id = str(row.get("session_id") or row.get("thread_id") or "unknown")
        if session_id in autonomous_thread_ids:
            continue
        parsed = parse_iso_datetime(row.get("ts") or row.get("timestamp") or row.get("created_at") or row.get("date"))
        if parsed is not None:
            human_times_by_session.setdefault(session_id, []).append(parsed)

    started_today: dict[str, datetime] = {}
    latest_by_thread: dict[str, datetime] = {}
    ticket_ids_by_thread: dict[str, set[str]] = {}
    for row in association_rows:
        thread_id = str(row.get("thread_id") or row.get("session_id") or "")
        ticket_id = str(row.get("ticket_id") or "")
        started = parse_iso_datetime(row.get("execution_started_at") or row.get("started_at") or row.get("created_at") or row.get("timestamp") or row.get("ts"))
        observed = parse_iso_datetime(row.get("observed_at") or row.get("updated_at") or row.get("created_at") or row.get("timestamp") or row.get("ts"))
        if not thread_id:
            continue
        if ticket_id:
            ticket_ids_by_thread.setdefault(thread_id, set()).add(ticket_id)
        if started and started.date().isoformat() == date:
            started_today.setdefault(thread_id, started)
        if observed and observed.date().isoformat() <= date:
            latest_by_thread[thread_id] = max(observed, latest_by_thread.get(thread_id, observed))

    rewarded_ticket_ids = reward_ticket_ids(reward_rows, date)
    rewarded_threads = {
        thread_id
        for thread_id, ticket_ids in ticket_ids_by_thread.items()
        if ticket_ids & rewarded_ticket_ids
    }

    autonomous_minutes = 0.0
    intervals: list[tuple[datetime, datetime]] = []
    accepted_minutes = 0.0
    for thread_id, start in started_today.items():
        end = latest_by_thread.get(thread_id, start)
        elapsed = max((end - start).total_seconds() / 60.0, 0.0)
        effective_elapsed = elapsed if elapsed > 0 else 30.0
        effective_end = end if elapsed > 0 else start + timedelta(minutes=30)
        autonomous_minutes += effective_elapsed
        intervals.append((start, effective_end))
        if thread_id in rewarded_threads:
            accepted_minutes += effective_elapsed
    union_minutes = 0.0
    for start, end in sorted(intervals):
        if not intervals:
            break
        if union_minutes == 0.0:
            current_start, current_end = start, end
            union_minutes = max((current_end - current_start).total_seconds() / 60.0, 0.0)
            continue
        if start > current_end:
            current_start, current_end = start, end
            union_minutes += max((end - start).total_seconds() / 60.0, 0.0)
        elif end > current_end:
            union_minutes += max((end - current_end).total_seconds() / 60.0, 0.0)
            current_end = end
    human_prompt_count = sum(len(times) for times in human_times_by_session.values())
    human_active_threads = len(human_times_by_session)
    human_minutes = sum(estimate_human_attention_minutes(times) for times in human_times_by_session.values())
    accepted_today = accepted_reward_count(reward_rows, date)
    ratio = autonomous_minutes / human_minutes if human_minutes else (autonomous_minutes if autonomous_minutes else 0.0)
    potential_saved_minutes = max(accepted_minutes - human_minutes, 0.0)
    if started_today and not rewarded_threads:
        gaps.append("missing:accepted_thread_runtime_attribution")
    gaps.extend(["source_gap:waiting_for_human_hours", "source_gap:unproductive_agent_hours"])
    return {
        "value": round(float(ratio), 4),
        "status": "available",
        "payload": {
            "human_prompt_count": human_prompt_count,
            "human_active_thread_count": human_active_threads,
            "human_attention_minutes_estimated": round(float(human_minutes), 2),
            "autonomous_thread_count": len(started_today),
            "autonomous_worker_elapsed_minutes": round(float(autonomous_minutes), 2),
            "clone_hours": round(float(autonomous_minutes / 60.0), 4),
            "concurrent_agent_wall_hours": round(float(union_minutes / 60.0), 4),
            "accepted_clone_hours": round(float(accepted_minutes / 60.0), 4) if rewarded_threads else None,
            "nonaccepted_clone_hours": None,
            "potential_human_time_saved_hours_estimated": round(float(potential_saved_minutes / 60.0), 4) if rewarded_threads else None,
            "formula": "max(accepted_clone_hours - human_attention_hours_estimated, 0)",
            "concurrency_policy": "clone_hours sum parallel intervals; concurrent_agent_wall_hours uses their union",
            "confidence": "estimated",
            "rewarded_autonomous_thread_count": len(rewarded_threads),
            "output_per_human_prompt": round(float(accepted_today / human_prompt_count), 4) if human_prompt_count else 0.0,
            "gaps": gaps,
        },
    }


def calculate_autonomy_savings(ticket_dir: Path, runtime_dir: Path, date: str, baseline_reasonable_hours: float | None = None, baseline_max_hours: float | None = None) -> dict[str, Any]:
    """Project accepted/nonaccepted clone hours through ticket proof and TAS-A."""
    attention = calculate_autonomy_time_ratio(runtime_dir, date)
    human_minutes = float(attention.get("payload", {}).get("human_attention_minutes_estimated") or 0.0)
    by_ticket: dict[str, list[dict[str, Any]]] = {}
    for row in read_jsonl(runtime_dir / "state" / "ticket-thread-associations.jsonl"):
        if row.get("ticket_id"):
            by_ticket.setdefault(str(row["ticket_id"]), []).append(row)
    accepted_minutes = nonaccepted_minutes = 0.0
    intervals: list[tuple[datetime, datetime]] = []
    terminal_count = attributed_count = 0
    items: list[dict[str, Any]] = []
    gaps: list[str] = []
    for ticket in iter_ticket_files(ticket_dir.resolve()):
        fm = parse_ticket_frontmatter(ticket)
        status = str(fm.get("status") or "").lower()
        completed = parse_iso_datetime(fm.get("completed_at") or fm.get("closed_at") or fm.get("updated_at"))
        if status not in {"done", "failed", "rejected"} or completed is None or completed.date().isoformat() != date:
            continue
        terminal_count += 1
        ticket_id = str(fm.get("ticket_id") or ticket.parent.name)
        rows = by_ticket.get(ticket_id, [])
        thread_ids = {str(row.get("thread_id") or row.get("session_id")) for row in rows if row.get("thread_id") or row.get("session_id")}
        starts = [parse_iso_datetime(row.get("execution_started_at") or row.get("started_at") or row.get("created_at") or row.get("timestamp") or row.get("ts")) for row in rows]
        starts = [value for value in starts if value is not None]
        if len(thread_ids) != 1 or not starts or completed <= min(starts):
            gaps.append(f"{ticket_id}:missing_or_ambiguous_runtime_attribution")
            continue
        start = min(starts)
        minutes = (completed - start).total_seconds() / 60.0
        markdown = ticket.read_text(encoding="utf-8")
        accepted = status == "done" and ticket_has_completion_proof(markdown) and ticket_has_acceptance_evidence(ticket, markdown)
        accepted_minutes += minutes if accepted else 0.0
        nonaccepted_minutes += 0.0 if accepted else minutes
        attributed_count += 1
        intervals.append((start, completed))
        items.append({"ticket_id": ticket_id, "thread_id": next(iter(thread_ids)), "minutes": round(minutes, 2), "accepted": accepted})
    union_minutes = 0.0
    current_end: datetime | None = None
    for start, end in sorted(intervals):
        if current_end is None or start > current_end:
            union_minutes += (end - start).total_seconds() / 60.0
            current_end = end
        elif end > current_end:
            union_minutes += (end - current_end).total_seconds() / 60.0
            current_end = end
    if terminal_count and not attributed_count:
        gaps.append("missing:accepted_runtime_attribution")
    coverage = attributed_count / terminal_count if terminal_count else None
    saved_minutes = max(accepted_minutes - human_minutes, 0.0) if attributed_count else None
    return {"value": round(saved_minutes / 60.0, 4) if saved_minutes is not None else None, "status": "available" if saved_minutes is not None else "source_gap", "payload": {"clone_hours": round((accepted_minutes + nonaccepted_minutes) / 60.0, 4), "concurrent_agent_wall_hours": round(union_minutes / 60.0, 4), "accepted_clone_hours": round(accepted_minutes / 60.0, 4), "nonaccepted_clone_hours": round(nonaccepted_minutes / 60.0, 4), "human_attention_hours_estimated": round(human_minutes / 60.0, 4), "potential_human_time_saved_hours_estimated": round(saved_minutes / 60.0, 4) if saved_minutes is not None else None, "attribution_coverage": round(coverage, 4) if coverage is not None else None, "baseline_provenance": {"reasonable_hours_per_day": baseline_reasonable_hours, "max_hours_per_day": baseline_max_hours, "source": "operator_provided" if baseline_reasonable_hours is not None or baseline_max_hours is not None else "not_provided"}, "formula": "max(accepted_clone_hours - human_attention_hours_estimated, 0)", "items": items, "gaps": gaps}}


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


def calculate_ticket_intervention_metrics(ticket_dir: Path, runtime_dir: Path, date: str) -> dict[str, Any]:
    """calculate_ticket_intervention_metrics(ticket_dir, runtime_dir, date) -> daily metrics map."""
    completed: dict[str, tuple[Path, str, datetime]] = {}
    gaps: list[str] = []
    ticket_root = ticket_dir.resolve()
    for ticket in iter_ticket_files(ticket_root):
        fm = parse_ticket_frontmatter(ticket)
        if not fm or not ticket_is_complete(fm):
            continue
        completed_at = parse_iso_datetime(fm.get("completed_at") or fm.get("closed_at") or fm.get("updated_at"))
        if completed_at is None or completed_at.date().isoformat() != date:
            continue
        markdown = ticket.read_text(encoding="utf-8")
        if not ticket_has_completion_proof(markdown):
            gaps.append(f"{ticket.parent.name}:missing_completion_proof")
            continue
        ticket_id = fm.get("ticket_id") or ticket.parent.name
        relative_ticket = str(ticket.relative_to(ticket_root.parent if ticket_root.name == "tickets" else ticket_root))
        completed[ticket_id] = (ticket, relative_ticket, completed_at)

    runtime_root = runtime_dir.resolve()
    association_rows = read_jsonl(runtime_root / "state" / "ticket-thread-associations.jsonl")
    if not association_rows:
        gaps.append("missing_ticket_thread_association_source")
    event_rows = read_jsonl_glob(runtime_root, "events/*.jsonl")
    if not (runtime_root / "events").exists():
        gaps.append("missing:events")

    associations_by_ticket: dict[str, list[dict[str, Any]]] = {}
    for row in association_rows:
        ticket_id = str(row.get("ticket_id") or "")
        if ticket_id:
            associations_by_ticket.setdefault(ticket_id, []).append(row)

    counted_tickets = 0
    intervention_free = 0
    total_interventions = 0
    items: list[dict[str, Any]] = []
    for ticket_id, (_ticket_path, relative_ticket, completed_at) in completed.items():
        associations = associations_by_ticket.get(ticket_id, [])
        if not associations:
            gaps.append(f"{relative_ticket}:missing_ticket_thread_association")
            continue
        thread_ids = {str(row.get("thread_id") or row.get("session_id")) for row in associations if row.get("thread_id") or row.get("session_id")}
        if len(thread_ids) != 1:
            gaps.append(f"{relative_ticket}:ambiguous_ticket_thread_association")
            continue
        association = associations[0]
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
            if event_time is not None and started_at < event_time <= completed_at:
                turn_count += 1
        counted_tickets += 1
        total_interventions += turn_count
        if turn_count == 0:
            intervention_free += 1
        items.append({"ticket_id": ticket_id, "ticket": relative_ticket, "intervention_turns": turn_count})

    if counted_tickets == 0:
        empty_payload = {"tickets": [], "gaps": gaps, "empty_window": True}
        return {
            "auto_completion_rate": {"value": None, "status": "not_applicable", "payload": empty_payload},
            "intervention_free_ticket_count": {"value": 0, "status": "available", "payload": empty_payload},
            "ticket_intervention_turn_count": {"value": 0, "status": "available", "payload": empty_payload},
        }
    payload = {"tickets": items, "gaps": gaps}
    return {
        "auto_completion_rate": {"value": round(float(intervention_free / counted_tickets), 4), "status": "available", "payload": payload},
        "intervention_free_ticket_count": {"value": intervention_free, "status": "available", "payload": payload},
        "ticket_intervention_turn_count": {"value": total_interventions, "status": "available", "payload": payload},
    }
