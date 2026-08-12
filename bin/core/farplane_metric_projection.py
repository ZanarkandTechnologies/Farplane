"""Metric-observation normalization and window projections for Farplane snapshots."""

from __future__ import annotations

from datetime import date as date_type
from datetime import datetime, timedelta, timezone
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def parse_metric_observation_datetime(value: Any) -> datetime | None:
    """Parse a complete observation date/timestamp without accepting trailing junk."""
    raw = str(value or "").strip()
    if not raw:
        return None
    try:
        if len(raw) == 10:
            parsed_date = date_type.fromisoformat(raw)
            return datetime.combine(parsed_date, datetime.min.time(), tzinfo=timezone.utc)
        if raw.endswith("Z"):
            raw = raw[:-1] + "+00:00"
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def metric_observation_date(value: Any, timezone_name: str) -> date_type | None:
    raw = str(value or "").strip()
    if not raw:
        return None
    if len(raw) == 10:
        try:
            return date_type.fromisoformat(raw)
        except ValueError:
            return None
    parsed = parse_metric_observation_datetime(raw)
    if parsed is None:
        return None
    try:
        zone = ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError:
        return None
    return parsed.astimezone(zone).date()


def projection_window(
    snapshot_date: str | None,
    window_start: str | None = None,
    window_end: str | None = None,
    timezone_name: str = "UTC",
) -> dict[str, Any]:
    """Resolve one inclusive calendar window and its preceding equal window."""
    try:
        ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(f"unknown metric projection timezone: {timezone_name}") from exc
    end_raw = window_end or snapshot_date or datetime.now(ZoneInfo(timezone_name)).date().isoformat()
    start_raw = window_start or end_raw
    try:
        start = date_type.fromisoformat(start_raw)
        end = date_type.fromisoformat(end_raw)
    except ValueError as exc:
        raise ValueError("metric projection windows must use YYYY-MM-DD dates") from exc
    if start > end:
        raise ValueError("metric projection window_start must be on or before window_end")
    window_days = (end - start).days + 1
    previous_end = start - timedelta(days=1)
    previous_start = previous_end - timedelta(days=window_days - 1)
    return {
        "start": start.isoformat(),
        "end": end.isoformat(),
        "timezone": timezone_name,
        "days": window_days,
        "previous_start": previous_start.isoformat(),
        "previous_end": previous_end.isoformat(),
    }


def unavailable_comparison(window: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "previous_start": window["previous_start"],
        "previous_end": window["previous_end"],
        "previous_value": None,
        "absolute_delta": None,
        "percent_delta": None,
        "progress_delta": None,
        "momentum": "unknown",
        "reason": reason,
    }


def metric_comparison(
    direction: Any,
    current_value: float | None,
    previous_value: float | None,
    window: dict[str, Any],
    *,
    current_complete: bool,
    previous_complete: bool,
) -> dict[str, Any]:
    normalized_direction = str(direction or "").strip().lower()
    if normalized_direction not in {"maximize", "minimize"}:
        return unavailable_comparison(window, "missing_or_invalid_direction")
    if not current_complete:
        return unavailable_comparison(window, "current_window_incomplete")
    if current_value is None:
        return unavailable_comparison(window, "no_current_window_observation")
    if not previous_complete:
        return unavailable_comparison(window, "previous_window_incomplete")
    if previous_value is None:
        return unavailable_comparison(window, "no_previous_window_observation")
    absolute_delta = current_value - previous_value
    progress_factor = 1.0 if normalized_direction == "maximize" else -1.0
    progress_delta = absolute_delta * progress_factor
    percent_delta = None if previous_value == 0 else (absolute_delta / abs(previous_value)) * 100
    momentum = "improving" if progress_delta > 0 else "worsening" if progress_delta < 0 else "flat"
    return {
        "previous_start": window["previous_start"],
        "previous_end": window["previous_end"],
        "previous_value": previous_value,
        "absolute_delta": absolute_delta,
        "percent_delta": percent_delta,
        "progress_delta": progress_delta,
        "momentum": momentum,
        "reason": "previous_value_zero" if previous_value == 0 else None,
    }


def window_observations(
    observations: list[dict[str, Any]],
    start: date_type,
    end: date_type,
    timezone_name: str,
    *,
    statuses: set[str] | None = None,
) -> list[dict[str, Any]]:
    accepted_statuses = statuses or {"available"}
    output: list[dict[str, Any]] = []
    for observation_row in observations:
        observed_date = metric_observation_date(observation_row.get("date"), timezone_name)
        if observed_date is None or not start <= observed_date <= end:
            continue
        if str(observation_row.get("status") or "available") not in accepted_statuses:
            continue
        output.append(observation_row)
    return output


def canonical_metric_observations(
    observations: list[dict[str, Any]],
    timezone_name: str,
    metric_type: str,
) -> list[dict[str, Any]]:
    """Collapse identical daily facts and surface conflicting facts as gaps."""
    grouped: dict[date_type | None, list[dict[str, Any]]] = {}
    for row in observations:
        grouped.setdefault(metric_observation_date(row.get("date"), timezone_name), []).append(row)
    output: list[dict[str, Any]] = []
    for observed_date, rows in grouped.items():
        if observed_date is None:
            output.extend(rows)
            continue
        available = [
            row
            for row in rows
            if str(row.get("status") or "available") == "available"
            and (
                isinstance(row.get("value"), str) and bool(row["value"].strip())
                if metric_type == "markdown"
                else isinstance(row.get("value"), (int, float))
            )
        ]
        distinct_values = (
            {str(row["value"]).strip() for row in available}
            if metric_type == "markdown"
            else {float(row["value"]) for row in available}
        )
        if len(distinct_values) > 1:
            output.extend(row for row in rows if str(row.get("status") or "available") != "available")
            output.append(
                {
                    "metric_id": str(rows[0].get("metric_id") or ""),
                    "date": observed_date.isoformat(),
                    "value": None,
                    "status": "source_gap",
                    "payload": {
                        "reason": "conflicting_daily_observations",
                        "values": sorted(distinct_values),
                    },
                }
            )
            continue
        if available:
            output.append(max(available, key=lambda row: str(row.get("date") or "")))
        output.extend(row for row in rows if str(row.get("status") or "available") != "available")
    return sorted(output, key=lambda row: str(row.get("date") or ""))


def distribution_account_for_current_metric(
    metric_def: dict[str, Any],
    observations: list[dict[str, Any]],
    current_observed_at: str | None,
) -> dict[str, str] | None:
    """Keep an observed owned-account identity on distribution cards without inferring it."""
    if metric_def.get("leverage") != "distribution" or not current_observed_at:
        return None
    for row in reversed(observations):
        if str(row.get("date") or "") != current_observed_at:
            continue
        payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
        account = payload.get("distribution_account") if isinstance(payload.get("distribution_account"), dict) else {}
        platform = str(account.get("platform") or "").strip().lower()
        account_id = str(account.get("account_id") or "").strip()
        label = str(account.get("label") or "").strip()
        if platform and account_id and label:
            return {"platform": platform, "account_id": account_id, "label": label}
    return None


def aggregate_metric_window(
    metric_type: str,
    observations: list[dict[str, Any]],
    start: date_type,
    end: date_type,
    timezone_name: str,
) -> dict[str, Any]:
    if metric_type in {"stock", "markdown"}:
        available = [
            row
            for row in observations
            if str(row.get("status") or "available") == "available"
            and (observed_date := metric_observation_date(row.get("date"), timezone_name)) is not None
            and observed_date <= end
        ]
    else:
        available = window_observations(observations, start, end, timezone_name)
    gaps = window_observations(
        observations,
        start,
        end,
        timezone_name,
        statuses={"source_gap", "not_applicable", "blocked"},
    )
    numeric = [row for row in available if isinstance(row.get("value"), (int, float))]
    markdown = [
        row for row in available if isinstance(row.get("value"), str) and bool(row["value"].strip())
    ]
    if metric_type == "flow":
        value = sum(float(row["value"]) for row in numeric) if numeric else None
        observed_at = max((str(row.get("date") or "") for row in numeric), default=None)
    elif metric_type == "stock":
        latest = max(numeric, key=lambda row: str(row.get("date") or ""), default=None)
        value = float(latest["value"]) if latest else None
        observed_at = str(latest.get("date") or "") if latest else None
    elif metric_type == "markdown":
        latest = max(markdown, key=lambda row: str(row.get("date") or ""), default=None)
        value = str(latest["value"]).strip() if latest else None
        observed_at = str(latest.get("date") or "") if latest else None
    else:
        value = None
        observed_at = None
    populated = markdown if metric_type == "markdown" else numeric
    return {
        "value": value,
        "observed_at": observed_at,
        "available_count": len(populated),
        "source_gap_count": len(gaps),
        "complete": not gaps,
        "status": "partial" if populated and gaps else "available" if populated else "source_gap" if gaps else "missing",
    }
