#!/usr/bin/env python3
"""Core-owned metric refresh planning and deterministic metric reducers.

These helpers return metric readings for `.farplane/metrics` without owning a
review cadence, writing dashboard projections, or fetching external APIs.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date as date_type
from datetime import timedelta
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bin.core.farplane_metric_shared import (
    iter_ticket_files,
    markdown_heading_section,
    parse_iso_datetime,
    parse_ticket_frontmatter,
    read_jsonl,
    read_jsonl_glob,
    row_date,
    ticket_completion_date,
    ticket_has_acceptance_evidence,
    ticket_has_completion_proof,
    ticket_is_complete,
)

try:
    from bin.core.farplane_metric_schema import observation_from_reading, write_metric_batch
except ImportError:  # pragma: no cover
    observation_from_reading = None
    write_metric_batch = None


def resolve_refresh_plan(
    metrics_file: Path,
    requested_metric_ids: list[str],
    date: str,
    fresh_metric_ids: set[str] | None = None,
) -> dict[str, Any]:
    """Resolve prompt jobs; the calling workflow executes and records them."""
    fresh = fresh_metric_ids or set()
    try:
        config = yaml.safe_load(metrics_file.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        return {"date": date, "refresh_groups": [], "skipped_metric_ids": [], "source_gaps": [f"invalid_metrics_config:{exc}"]}
    metrics = config.get("metrics") if isinstance(config, dict) else {}
    refreshers = config.get("refreshers") if isinstance(config, dict) else {}
    metrics = metrics if isinstance(metrics, dict) else {}
    refreshers = refreshers if isinstance(refreshers, dict) else {}
    jobs: dict[str, dict[str, Any]] = {}
    skipped: list[str] = []
    gaps: list[str] = []
    for metric_id in requested_metric_ids:
        if metric_id in fresh:
            skipped.append(metric_id)
            continue
        definition = metrics.get(metric_id)
        if not isinstance(definition, dict):
            gaps.append(f"unknown_metric:{metric_id}")
            continue
        refresh_ref = str(definition.get("refresh_ref") or "").strip()
        inline = str(definition.get("refresh") or "").strip()
        if bool(refresh_ref) == bool(inline):
            gaps.append(f"invalid_refresh_owner:{metric_id}")
            continue
        metric_type = str(definition.get("type") or "")
        if inline:
            jobs[f"metric:{metric_id}"] = {
                "refresh_id": f"metric:{metric_id}",
                "refresh": inline.replace("<YYYY-MM-DD>", date),
                "provides": [metric_id],
                "requested_metric_ids": [metric_id],
                "metric_types": {metric_id: metric_type},
            }
            continue
        refresher = refreshers.get(refresh_ref)
        if not isinstance(refresher, dict) or not str(refresher.get("refresh") or "").strip():
            gaps.append(f"missing_refresher:{metric_id}:{refresh_ref}")
            continue
        job = jobs.setdefault(
            refresh_ref,
            {
                "refresh_id": refresh_ref,
                "refresh": str(refresher["refresh"]).replace("<YYYY-MM-DD>", date),
                "provides": list(refresher.get("provides") or []),
                "requested_metric_ids": [],
                "metric_types": {},
            },
        )
        job["requested_metric_ids"].append(metric_id)
        job["metric_types"][metric_id] = metric_type
    return {"date": date, "refresh_groups": list(jobs.values()), "skipped_metric_ids": skipped, "source_gaps": gaps}


def record_refresh_result(project_root: Path, date: str, job: dict[str, Any], readings: dict[str, Any]) -> dict[str, Any]:
    """Normalize one agent-executed group result into flat metric observations."""
    if observation_from_reading is None or write_metric_batch is None:
        raise RuntimeError("Farplane metric schema is unavailable")
    observations = []
    gaps: list[str] = []
    for metric_id in job.get("requested_metric_ids", []):
        reading = readings.get(metric_id)
        metric_types = job.get("metric_types") if isinstance(job.get("metric_types"), dict) else {}
        metric_type = str(metric_types.get(metric_id) or "")
        if not isinstance(reading, dict):
            gaps.append(f"missing_refresh_output:{metric_id}")
            reading = {
                "status": "source_gap",
                "payload": {"reason": f"missing_{metric_type or 'metric'}_refresh_output"},
            }
        observations.append(
            observation_from_reading(
                metric_id,
                date,
                reading,
                {"refresh_id": job.get("refresh_id")},
                metric_type,
            )
        )
    path = write_metric_batch(project_root, str(job.get("refresh_id") or "metric_refresh"), date, observations, gaps=gaps, payload={"requested_metric_ids": job.get("requested_metric_ids", [])})
    return {"path": str(path), "observation_metric_ids": [row.metric_id for row in observations], "source_gaps": gaps}










def content_row_date(row: dict[str, Any]) -> str | None:
    parsed = parse_iso_datetime(row.get("published_at"))
    return parsed.date().isoformat() if parsed else None


def select_content_metric_targets(
    content_ledger: Path,
    platform: str,
    kpi_key: str,
    date: str,
    window_days: int = 7,
) -> dict[str, Any]:
    """select_content_metric_targets(content_ledger, platform, kpi_key, date, window_days) -> fetch target packet."""
    if not content_ledger.exists():
        return {"status": "source_gap", "external_ids": [], "items": [], "payload": {"gaps": [f"missing:{content_ledger}"]}}
    until = date_type.fromisoformat(date) + timedelta(days=1)
    since = until - timedelta(days=window_days)
    rows = []
    for row in read_jsonl(content_ledger):
        if row.get("platform") != platform:
            continue
        if row.get("status") != "posted":
            continue
        if kpi_key not in (row.get("kpis") if isinstance(row.get("kpis"), list) else []):
            continue
        published_date = content_row_date(row)
        if published_date is None:
            continue
        parsed_date = date_type.fromisoformat(published_date)
        if since <= parsed_date < until:
            rows.append(row)
    external_ids = [
        str(row["external_id"])
        for row in rows
        if isinstance(row.get("external_id"), str) and row.get("external_id")
    ]
    if platform == "instagram":
        fetch_command = f"python3 skills/instagram-account/scripts/fetch_metrics.py --date {date} " + " ".join(
            f"--media-id {content_id}" for content_id in external_ids
        )
    elif platform == "x":
        fetch_command = f"python3 skills/x-account/scripts/fetch_metrics.py --date {date} " + " ".join(
            f"--tweet-id {content_id}" for content_id in external_ids
        )
    else:
        fetch_command = ""
    return {
        "status": "available" if external_ids else "source_gap",
        "external_ids": external_ids,
        "items": rows,
        "payload": {
            "platform": platform,
            "kpi_key": kpi_key,
            "window_days": window_days,
            "since_date": since.isoformat(),
            "until_date": until.isoformat(),
            "fetch_command": fetch_command,
            "gaps": [] if external_ids else ["no_posted_content_targets_for_window"],
        },
    }




def parse_fenced_yaml_from_section(section: str) -> dict[str, Any]:
    fence_start = section.find("```yaml")
    if fence_start == -1:
        return {}
    yaml_start = section.find("\n", fence_start)
    fence_end = section.find("```", yaml_start + 1)
    if yaml_start == -1 or fence_end == -1:
        return {}
    loaded = yaml.safe_load(section[yaml_start + 1 : fence_end]) or {}
    return loaded if isinstance(loaded, dict) else {}














def nonempty(value: Any) -> bool:
    return value is not None and str(value).strip() != ""


def string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def parse_ticket_kpi_rewards(markdown: str) -> tuple[list[dict[str, Any]], list[str]]:
    reward = markdown_heading_section(markdown, "Reward")
    if not reward:
        return [], ["missing_reward_section"]
    payload = parse_fenced_yaml_from_section(reward)
    raw_rewards = payload.get("kpi_rewards")
    if not isinstance(raw_rewards, list):
        return [], ["missing_kpi_rewards"]
    rewards: list[dict[str, Any]] = []
    gaps: list[str] = []
    seen_reward_ids: set[str] = set()
    for index, raw_reward in enumerate(raw_rewards):
        if not isinstance(raw_reward, dict):
            gaps.append(f"invalid_kpi_reward:{index}")
            continue
        kpi_id = str(raw_reward.get("kpi_id") or "").strip()
        reward_id = str(raw_reward.get("reward_id") or "").strip()
        expected_reward = str(raw_reward.get("expected_reward") or "").strip()
        if not reward_id:
            gaps.append(f"missing_reward_id:{index}")
            continue
        if reward_id in seen_reward_ids:
            gaps.append(f"duplicate_reward_id:{index}:{reward_id}")
            continue
        seen_reward_ids.add(reward_id)
        if not kpi_id:
            gaps.append(f"missing_kpi_id:{index}")
            continue
        rewards.append(
            {
                "reward_id": reward_id,
                "kpi_id": kpi_id,
                "expected_reward": expected_reward,
                "actual_result": raw_reward.get("actual_result"),
                "decision": str(raw_reward.get("decision") or "").strip().lower(),
                "evaluated_at": str(raw_reward.get("evaluated_at") or "").strip(),
                "evaluation_key": str(raw_reward.get("evaluation_key") or "").strip(),
                "supersedes_evaluation_key": str(
                    raw_reward.get("supersedes_evaluation_key") or ""
                ).strip(),
                "evidence_refs": string_list(raw_reward.get("evidence_refs")),
            }
        )
    return rewards, gaps


def accepted_reward(reward: dict[str, Any], *, has_acceptance_evidence: bool) -> bool:
    """Return whether one canonical Reward row is realized accepted value."""

    return (
        reward.get("decision") == "accept"
        and nonempty(reward.get("actual_result"))
        and parse_iso_datetime(reward.get("evaluated_at")) is not None
        and bool(reward.get("evidence_refs"))
        and has_acceptance_evidence
    )


def count_ticket_kpi_rewards(ticket_dir: Path, date: str, kpi_key: str) -> dict[str, Any]:
    """count_ticket_kpi_rewards(ticket_dir, date, kpi_key) -> MetricReading."""
    count = 0
    tickets: list[dict[str, str]] = []
    gaps: list[str] = []
    root = ticket_dir.resolve()
    for ticket in iter_ticket_files(root):
        markdown = ticket.read_text(encoding="utf-8")
        fm = parse_ticket_frontmatter(ticket)
        if not fm or not ticket_is_complete(fm):
            continue
        if ticket_completion_date(fm, date) != date:
            continue
        relative_ticket = str(ticket.relative_to(root.parent if root.name == "tickets" else root))
        rewards, reward_gaps = parse_ticket_kpi_rewards(markdown)
        gaps.extend(f"{relative_ticket}:{gap}" for gap in reward_gaps)
        if not rewards:
            continue
        if not ticket_has_completion_proof(markdown):
            gaps.append(f"{relative_ticket}:missing_completion_proof")
            continue
        has_acceptance_evidence = ticket_has_acceptance_evidence(ticket, markdown)
        for reward in rewards:
            if reward["kpi_id"] != kpi_key:
                continue
            decision = reward.get("decision")
            if decision == "kill":
                continue
            if not accepted_reward(
                reward,
                has_acceptance_evidence=has_acceptance_evidence,
            ):
                if decision in {"", "monitor"}:
                    gaps.append(
                        f"{relative_ticket}:unresolved_reward:{reward['reward_id']}"
                    )
                elif decision == "accept" and not has_acceptance_evidence:
                    gaps.append(
                        f"{relative_ticket}:missing_acceptance_evidence:{reward['reward_id']}"
                    )
                else:
                    gaps.append(
                        f"{relative_ticket}:invalid_accept_evidence:{reward['reward_id']}"
                    )
                continue
            count += 1
            tickets.append(
                {
                    "ticket_id": fm.get("ticket_id") or ticket.parent.name,
                    "ticket": relative_ticket,
                    "reward_id": reward["reward_id"],
                    "expected_reward": reward.get("expected_reward", ""),
                    "actual_result": str(reward.get("actual_result") or ""),
                    "evaluated_at": reward.get("evaluated_at", ""),
                    "evidence_refs": reward.get("evidence_refs", []),
                }
            )
            # This primitive is a completed-ticket count by KPI. Multiple
            # accepted horizons for the same ticket/KPI remain evidence on the
            # ticket and do not inflate the daily ticket count.
            break
    return {
        "value": count,
        "status": "available" if count or not gaps else "source_gap",
        "payload": {"tickets": tickets, "gaps": gaps},
    }


from bin.core.farplane_metric_autonomy import (  # noqa: E402
    calculate_autonomy_savings,
    calculate_autonomy_time_ratio,
    calculate_ticket_intervention_metrics,
)
if __name__ == "__main__":
    from bin.core.farplane_metric_cli import main

    raise SystemExit(main())
