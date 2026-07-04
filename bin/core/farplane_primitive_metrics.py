#!/usr/bin/env python3
"""Core primitive metric reducers for Farplane project packages."""

from __future__ import annotations

import argparse
import calendar
import json
import sqlite3
from dataclasses import dataclass
from datetime import date as date_type
from datetime import datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any

import yaml

try:
    from farplane_metric_schema import MetricObservation, metric_observation, write_metric_batch
except ImportError:  # pragma: no cover - package import path used by tests
    from bin.core.farplane_metric_schema import MetricObservation, metric_observation, write_metric_batch


OBSERVATION_ROOT = Path(".farplane/metrics/observations")
DAILY_METRICS_ROOT = Path(".farplane/metrics/daily")
ASSOCIATION_PATH = Path(".farplane/state/ticket-thread-associations.jsonl")


@dataclass(frozen=True)
class Window:
    start: datetime
    end: datetime

    @property
    def date(self) -> str:
        return self.start.date().isoformat()


@dataclass(frozen=True)
class TicketFilters:
    kpi_reward: str | set[str] | None = None
    status: str | None = None


@dataclass(frozen=True)
class TicketRecord:
    ticket_id: str
    path: Path
    relative_path: str
    phase: str
    status: str
    created_at: datetime | None
    updated_at: datetime | None
    completed_at: datetime | None
    closed_at: datetime | None
    kpi_rewards: tuple[str, ...]
    has_completion_proof: bool

    @property
    def is_complete(self) -> bool:
        return self.phase == "complete" or self.status in {"done", "rejected"}

    @property
    def is_terminal(self) -> bool:
        return self.phase in {"complete", "failed"} or self.status in {"done", "failed", "rejected"}


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_iso_datetime(value: Any) -> datetime | None:
    if value in {None, ""}:
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
        return datetime.combine(parsed_date, time.min, tzinfo=timezone.utc)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def parse_epoch_datetime(value: Any) -> datetime | None:
    if value in {None, ""}:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return parse_iso_datetime(value)
    if number <= 0:
        return None
    if number > 10_000_000_000:
        number = number / 1000.0
    return datetime.fromtimestamp(number, tz=timezone.utc)


def window_for_date(date_value: str) -> Window:
    parsed = date_type.fromisoformat(date_value)
    start = datetime.combine(parsed, time.min, tzinfo=timezone.utc)
    return Window(start=start, end=start + timedelta(days=1))


def in_window(value: datetime | None, window: Window) -> bool:
    return value is not None and window.start <= value < window.end


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
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


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


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


def parse_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text:
        return {}
    raw = text.split("\n---\n", 1)[0][4:]
    try:
        loaded = yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def parse_ticket_kpi_rewards(markdown: str) -> tuple[list[str], list[str]]:
    reward = markdown_heading_section(markdown, "Reward")
    if not reward:
        return [], ["missing_reward_section"]
    payload = parse_fenced_yaml_from_section(reward)
    raw_rewards = payload.get("kpi_rewards")
    if not isinstance(raw_rewards, list):
        return [], ["missing_kpi_rewards"]
    kpi_ids: list[str] = []
    gaps: list[str] = []
    for index, raw_reward in enumerate(raw_rewards):
        if not isinstance(raw_reward, dict):
            gaps.append(f"invalid_kpi_reward:{index}")
            continue
        kpi_id = str(raw_reward.get("kpi_id") or "").strip()
        if not kpi_id:
            gaps.append(f"missing_kpi_id:{index}")
            continue
        kpi_ids.append(kpi_id)
    return kpi_ids, gaps


def ticket_has_completion_proof(markdown: str) -> bool:
    done = markdown_heading_section(markdown, "Done / Proof") or markdown_heading_section(markdown, "Done")
    lowered = done.lower()
    return any(
        token in lowered
        for token in ("passed", "proof", "evidence", "artifact", "artifacts/", "review", "receipt", "verification")
    )


def iter_ticket_files(project_root: Path) -> list[Path]:
    roots = [project_root / "tickets", project_root / "tickets" / "archive"]
    tickets: list[Path] = []
    for root in roots:
        if root.exists():
            tickets.extend(root.glob("TASK-*/ticket.md"))
    return sorted(set(tickets))


def load_tickets(project_root: Path) -> tuple[list[TicketRecord], list[str]]:
    tickets: list[TicketRecord] = []
    gaps: list[str] = []
    for path in iter_ticket_files(project_root):
        markdown = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(path)
        if not fm:
            gaps.append(f"{path.relative_to(project_root)}:missing_frontmatter")
            continue
        rewards, reward_gaps = parse_ticket_kpi_rewards(markdown)
        rel_path = str(path.relative_to(project_root))
        gaps.extend(f"{rel_path}:{gap}" for gap in reward_gaps if gap != "missing_reward_section")
        ticket_id = str(fm.get("ticket_id") or path.parent.name)
        tickets.append(
            TicketRecord(
                ticket_id=ticket_id,
                path=path,
                relative_path=rel_path,
                phase=str(fm.get("phase") or ""),
                status=str(fm.get("status") or ""),
                created_at=parse_iso_datetime(fm.get("created_at")),
                updated_at=parse_iso_datetime(fm.get("updated_at")),
                completed_at=parse_iso_datetime(fm.get("completed_at")),
                closed_at=parse_iso_datetime(fm.get("closed_at")),
                kpi_rewards=tuple(rewards),
                has_completion_proof=ticket_has_completion_proof(markdown),
            )
        )
    return tickets, gaps


def completion_time(ticket: TicketRecord) -> datetime | None:
    return ticket.completed_at or ticket.closed_at or ticket.updated_at


def ticket_touched_in_window(ticket: TicketRecord, window: Window) -> bool:
    return any(
        in_window(value, window)
        for value in (ticket.created_at, ticket.updated_at, ticket.completed_at, ticket.closed_at)
    )


def fetch_tickets(
    project_root: Path,
    window: Window,
    filters: TicketFilters | None = None,
) -> dict[str, Any]:
    filters = filters or TicketFilters()
    tickets, gaps = load_tickets(project_root)
    selected: list[TicketRecord] = []
    for ticket in tickets:
        if filters.status and ticket.status != filters.status and ticket.phase != filters.status:
            continue
        if filters.kpi_reward == "exists" and not ticket.kpi_rewards:
            continue
        if isinstance(filters.kpi_reward, str) and filters.kpi_reward not in {"exists", ""}:
            if filters.kpi_reward not in ticket.kpi_rewards:
                continue
        if isinstance(filters.kpi_reward, set) and not (set(ticket.kpi_rewards) & filters.kpi_reward):
            continue
        if not ticket_touched_in_window(ticket, window):
            continue
        selected.append(ticket)
    return {
        "tickets": [ticket_payload(ticket) for ticket in selected],
        "gaps": gaps,
    }


def ticket_payload(ticket: TicketRecord) -> dict[str, Any]:
    return {
        "ticket_id": ticket.ticket_id,
        "path": ticket.relative_path,
        "phase": ticket.phase,
        "status": ticket.status,
        "created_at": ticket.created_at.isoformat() if ticket.created_at else None,
        "updated_at": ticket.updated_at.isoformat() if ticket.updated_at else None,
        "completed_at": completion_time(ticket).isoformat() if completion_time(ticket) else None,
        "kpi_rewards": list(ticket.kpi_rewards),
        "has_completion_proof": ticket.has_completion_proof,
    }


def reading(value: float | int | None, status: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "value": value,
        "status": status,
        "payload": payload or {},
    }


def load_bindings(project_root: Path) -> dict[str, Any]:
    path = project_root / "farplane" / "bindings.yaml"
    if not path.exists():
        return {}
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def metric_recipes(project_root: Path) -> dict[str, dict[str, Any]]:
    raw = load_bindings(project_root).get("metrics")
    if not isinstance(raw, dict):
        return {}
    return {str(key): value if isinstance(value, dict) else {} for key, value in raw.items()}


def configured_monthly_ai_spend(project_root: Path) -> float | None:
    bindings = load_bindings(project_root)
    candidates = [
        bindings.get("spend_model"),
        bindings.get("operating_expenses"),
        bindings.get("costs"),
    ]
    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue
        raw = (
            candidate.get("monthly_ai_spend")
            or candidate.get("monthly_ai_subscription_spend")
            or candidate.get("ai_monthly_spend")
        )
        if isinstance(raw, (int, float)):
            return float(raw)
        if isinstance(raw, str):
            try:
                return float(raw.replace("$", "").replace(",", "").strip())
            except ValueError:
                continue
    return None


def kpis_for_product(metric_recipe_map: dict[str, dict[str, Any]], product_id: str) -> set[str]:
    return {
        metric_id
        for metric_id, recipe in metric_recipe_map.items()
        if str(recipe.get("product") or "").strip() == product_id
    }


def ticket_counts(project_root: Path, window: Window) -> tuple[dict[str, Any], list[TicketRecord], list[str]]:
    tickets, gaps = load_tickets(project_root)
    created = [ticket for ticket in tickets if in_window(ticket.created_at, window)]
    completed = [ticket for ticket in tickets if ticket.is_complete and in_window(completion_time(ticket), window)]
    attributed = [ticket for ticket in tickets if ticket_touched_in_window(ticket, window) and ticket.kpi_rewards]
    touched = [ticket for ticket in tickets if ticket_touched_in_window(ticket, window)]
    status = "available" if tickets else "source_gap"
    ratio = round(len(attributed) / len(touched), 4) if touched else 0
    return (
        {
            "tickets_created_count": reading(len(created), status, {"tickets": [ticket_payload(ticket) for ticket in created], "gaps": []}),
            "tickets_completed_count": reading(
                len(completed),
                status,
                {"tickets": [ticket_payload(ticket) for ticket in completed], "gaps": []},
            ),
            "tickets_with_kpi_reward_count": reading(
                len(attributed),
                status,
                {"tickets": [ticket_payload(ticket) for ticket in attributed], "gaps": []},
            ),
            "kpi_attributed_ticket_ratio": reading(
                ratio,
                "available",
                {
                    "attributed": len(attributed),
                    "total_touched": len(touched),
                    "empty_window": not touched,
                    "gaps": [],
                },
            ),
        },
        tickets,
        gaps,
    )


def ticket_count_by_kpi(tickets: list[TicketRecord], window: Window) -> dict[str, dict[str, Any]]:
    by_kpi: dict[str, list[TicketRecord]] = {}
    for ticket in tickets:
        if not ticket_touched_in_window(ticket, window):
            continue
        for kpi_id in ticket.kpi_rewards:
            by_kpi.setdefault(kpi_id, []).append(ticket)
    return {
        kpi_id: reading(
            len(items),
            "available",
            {"tickets": [ticket_payload(ticket) for ticket in items], "gaps": []},
        )
        for kpi_id, items in sorted(by_kpi.items())
    }


def ticket_count_by_kpi_with_status(
    tickets: list[TicketRecord],
    window: Window,
    status_filter: str,
) -> dict[str, dict[str, Any]]:
    by_kpi: dict[str, list[TicketRecord]] = {}
    total: list[TicketRecord] = []
    for ticket in tickets:
        if ticket.status != status_filter and ticket.phase != status_filter:
            continue
        if not ticket_touched_in_window(ticket, window):
            continue
        if ticket.kpi_rewards:
            total.append(ticket)
        for kpi_id in ticket.kpi_rewards:
            by_kpi.setdefault(kpi_id, []).append(ticket)
    output = {
        kpi_id: reading(
            len(items),
            "available",
            {
                "status_filter": status_filter,
                "tickets": [ticket_payload(ticket) for ticket in items],
                "gaps": [],
            },
        )
        for kpi_id, items in sorted(by_kpi.items())
    }
    output["_total"] = reading(
        len(total),
        "available",
        {
            "status_filter": status_filter,
            "tickets": [ticket_payload(ticket) for ticket in total],
            "gaps": [],
        },
    )
    return output


def ticket_count_by_product(
    tickets: list[TicketRecord],
    window: Window,
    metric_recipe_map: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    product_ids = sorted({str(recipe.get("product") or "").strip() for recipe in metric_recipe_map.values() if recipe.get("product")})
    output: dict[str, dict[str, Any]] = {}
    for product_id in product_ids:
        kpi_ids = kpis_for_product(metric_recipe_map, product_id)
        items = [
            ticket
            for ticket in tickets
            if ticket_touched_in_window(ticket, window) and set(ticket.kpi_rewards) & kpi_ids
        ]
        completed = [ticket for ticket in items if ticket.is_complete]
        proofed = [ticket for ticket in completed if ticket.has_completion_proof]
        output[product_id] = reading(
            len(items),
            "available",
            {
                "kpi_ids": sorted(kpi_ids),
                "tickets": [ticket_payload(ticket) for ticket in items],
                "completed_ticket_count": len(completed),
                "proofed_ticket_count": len(proofed),
                "gaps": [],
            },
        )
    return output


def thread_rows_from_sqlite(codex_home: Path, project_root: Path, window: Window) -> tuple[list[dict[str, Any]], list[str]]:
    db_path = codex_home / "sqlite" / "state_5.sqlite"
    if not db_path.exists():
        return [], [f"missing:{db_path}"]
    try:
        con = sqlite3.connect(db_path)
        con.row_factory = sqlite3.Row
        rows = [dict(row) for row in con.execute("select * from threads")]
        edge_rows = [dict(row) for row in con.execute("select * from thread_spawn_edges")]
    except sqlite3.Error as exc:
        return [], [f"sqlite_error:{exc}"]
    finally:
        try:
            con.close()
        except UnboundLocalError:
            pass

    project_path = str(project_root.resolve())
    child_ids = {str(row.get("child_thread_id")) for row in edge_rows if row.get("child_thread_id")}
    selected: list[dict[str, Any]] = []
    for row in rows:
        if str(row.get("cwd") or "") != project_path:
            continue
        created = parse_epoch_datetime(row.get("created_at_ms") or row.get("created_at"))
        updated = parse_epoch_datetime(row.get("updated_at_ms") or row.get("updated_at"))
        if not (in_window(created, window) or in_window(updated, window)):
            continue
        row["created_at_iso"] = created.isoformat() if created else None
        row["updated_at_iso"] = updated.isoformat() if updated else None
        row["is_subagent"] = str(row.get("id")) in child_ids or bool(row.get("agent_role"))
        selected.append(row)
    return selected, []


def token_usage_zero() -> dict[str, int]:
    return {
        "input": 0,
        "cached_input": 0,
        "output": 0,
        "reasoning_output": 0,
        "total": 0,
    }


def add_usage(total: dict[str, int], usage: dict[str, Any]) -> None:
    total["input"] += int(usage.get("input_tokens") or 0)
    total["cached_input"] += int(usage.get("cached_input_tokens") or 0)
    total["output"] += int(usage.get("output_tokens") or 0)
    total["reasoning_output"] += int(usage.get("reasoning_output_tokens") or 0)
    total["total"] += int(usage.get("total_tokens") or 0)


def event_timestamp(row: dict[str, Any]) -> datetime | None:
    return parse_iso_datetime(row.get("timestamp") or row.get("ts") or row.get("created_at") or row.get("date"))


def session_id_from_path(path: Path) -> str:
    stem = path.stem
    marker = "-"
    if marker in stem:
        return stem.rsplit(marker, 1)[-1]
    return stem


def fetch_codex_thread_usage(codex_home: Path, project_root: Path, window: Window) -> dict[str, Any]:
    thread_rows, gaps = thread_rows_from_sqlite(codex_home, project_root, window)
    thread_ids = {str(row.get("id")) for row in thread_rows if row.get("id")}
    tokens = token_usage_zero()
    user_message_count = 0
    assistant_message_count = 0
    tool_event_count = 0
    turn_count = 0
    event_times: list[datetime] = []
    session_root = codex_home / "sessions"
    if not session_root.exists():
        gaps.append(f"missing:{session_root}")

    for path in sorted(session_root.glob("**/*.jsonl")) if session_root.exists() else []:
        session_id = session_id_from_path(path)
        rows = read_jsonl(path)
        session_cwd = ""
        for row in rows:
            payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
            if row.get("type") == "session_meta":
                session_cwd = str(payload.get("cwd") or payload.get("workspace") or session_cwd)
                session_id = str(payload.get("id") or payload.get("session_id") or payload.get("thread_id") or session_id)
        if thread_ids and session_id not in thread_ids:
            continue
        if not thread_ids and session_cwd and session_cwd != str(project_root.resolve()):
            continue
        for row in rows:
            ts = event_timestamp(row)
            if ts is not None and not in_window(ts, window):
                continue
            if ts is not None:
                event_times.append(ts)
            payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
            payload_type = str(payload.get("type") or "")
            if payload_type == "token_count":
                info = payload.get("info") if isinstance(payload.get("info"), dict) else {}
                last_usage = info.get("last_token_usage") if isinstance(info.get("last_token_usage"), dict) else {}
                add_usage(tokens, last_usage)
                continue
            row_type = str(row.get("type") or "")
            role = str(payload.get("role") or payload.get("actor") or "").lower()
            if payload_type in {"task_started", "user_message"} or role == "user":
                user_message_count += 1
                turn_count += 1
            elif payload_type in {"assistant_message", "agent_message"} or role == "assistant":
                assistant_message_count += 1
            elif "tool" in payload_type or payload_type in {"function_call", "function_call_output"} or row_type == "tool_event":
                tool_event_count += 1

    if not tokens["total"]:
        tokens["total"] = sum(int(row.get("tokens_used") or 0) for row in thread_rows)
    span_minutes = 0.0
    if event_times:
        span_minutes = max((max(event_times) - min(event_times)).total_seconds() / 60.0, 0.0)
    else:
        spans = []
        for row in thread_rows:
            created = parse_iso_datetime(row.get("created_at_iso"))
            updated = parse_iso_datetime(row.get("updated_at_iso"))
            if created and updated:
                spans.append(max((updated - created).total_seconds() / 60.0, 0.0))
        span_minutes = sum(spans)

    status = "available" if thread_rows or event_times or not gaps else "source_gap"
    return {
        "value": len(thread_rows),
        "status": status,
        "payload": {
            "thread_count": len(thread_rows),
            "subagent_thread_count": len([row for row in thread_rows if row.get("is_subagent")]),
            "turn_count": turn_count,
            "user_message_count": user_message_count,
            "assistant_message_count": assistant_message_count,
            "tool_event_count": tool_event_count,
            "tokens": tokens,
            "span_minutes": round(span_minutes, 2),
            "gaps": gaps,
        },
    }


def estimate_ai_burn(window: Window, thread_usage: dict[str, Any], monthly_spend: float | None) -> dict[str, Any]:
    if monthly_spend is None:
        return reading(None, "source_gap", {"gaps": ["missing_spend_model"], "mode": "subscription_allocation"})
    days = calendar.monthrange(window.start.year, window.start.month)[1]
    window_days = max((window.end - window.start).total_seconds() / 86400.0, 1.0)
    value = round((monthly_spend / days) * window_days, 4)
    payload = {
        "mode": "subscription_allocation",
        "monthly_spend": monthly_spend,
        "allocated_window_days": window_days,
        "basis": "calendar_day_v1",
        "thread_count": thread_usage.get("payload", {}).get("thread_count"),
        "gaps": [],
    }
    return reading(value, "available", payload)


def normalize_observed_at(value: Any) -> str:
    parsed = parse_epoch_datetime(value) or parse_iso_datetime(value)
    return parsed.isoformat().replace("+00:00", "Z") if parsed else now_utc()


def association_row_from_source(source: dict[str, Any], input_path: Path, project_root: Path, source_event_key: str) -> dict[str, Any] | None:
    ticket_id = str(source.get("ticketId") or source.get("ticket_id") or "").strip()
    thread_id = str(source.get("threadId") or source.get("thread_id") or source.get("sessionId") or source.get("session_id") or "").strip()
    if not ticket_id or not thread_id:
        return None
    ticket_path = str(source.get("inputRef") or source.get("ticketPath") or f"tickets/{ticket_id}/ticket.md")
    observed = source.get("updatedAt") or source.get("updated_at") or source.get("timestamp") or source.get("created_at")
    return {
        "ticket_id": ticket_id,
        "ticket_path": ticket_path,
        "session_id": str(source.get("sessionId") or source.get("session_id") or thread_id),
        "thread_id": thread_id,
        "observed_at": normalize_observed_at(observed),
        "source": "mine_input",
        "source_event_key": source_event_key or str(input_path.relative_to(project_root)),
        "confidence": "completion_only",
    }


def backfill_ticket_thread_associations(project_root: Path, mine_runs_root: Path, output_path: Path, write: bool = True) -> dict[str, Any]:
    existing = read_jsonl(output_path)
    rows_by_key: dict[tuple[str, str, str], dict[str, Any]] = {}
    for row in existing:
        key = (str(row.get("ticket_id") or ""), str(row.get("thread_id") or row.get("session_id") or ""), str(row.get("source_event_key") or ""))
        if key[0] and key[1]:
            rows_by_key[key] = row
    gaps: list[str] = []
    input_paths = sorted(mine_runs_root.glob("**/input.json")) if mine_runs_root.exists() else []
    if not input_paths:
        gaps.append(f"missing_or_empty:{mine_runs_root}")
    added = 0
    for input_path in input_paths:
        payload = read_json(input_path)
        sources = payload.get("sources")
        if not isinstance(sources, list):
            continue
        source_event_key = str(payload.get("sourceEventKey") or "")
        for source in sources:
            if not isinstance(source, dict):
                continue
            row = association_row_from_source(source, input_path, project_root, source_event_key)
            if row is None:
                continue
            key = (row["ticket_id"], row["thread_id"], row["source_event_key"])
            if key not in rows_by_key:
                added += 1
            rows_by_key[key] = row
    rows = sorted(rows_by_key.values(), key=lambda row: (str(row.get("ticket_id")), str(row.get("observed_at")), str(row.get("thread_id"))))
    if write:
        write_jsonl(output_path, rows)
    return {
        "value": len(rows),
        "status": "available" if rows else "source_gap",
        "payload": {
            "path": str(output_path),
            "existing_count": len(existing),
            "added_count": added,
            "total_count": len(rows),
            "confidence": "completion_only",
            "gaps": gaps,
        },
    }


def ticket_thread_link_coverage(tickets: list[TicketRecord], window: Window, association_rows: list[dict[str, Any]]) -> dict[str, Any]:
    completed = [ticket for ticket in tickets if ticket.is_complete and in_window(completion_time(ticket), window)]
    associated_ids = {str(row.get("ticket_id")) for row in association_rows}
    linked = [ticket for ticket in completed if ticket.ticket_id in associated_ids]
    value = round(len(linked) / len(completed), 4) if completed else 0
    return reading(
        value,
        "available",
        {
            "associated_completed_tickets": len(linked),
            "completed_tickets": len(completed),
            "empty_window": not completed,
            "gaps": [],
        },
    )


def observation_rows_for_date(project_root: Path, date_value: str) -> list[dict[str, Any]]:
    root = project_root / OBSERVATION_ROOT
    if not root.exists():
        return []
    rows: list[dict[str, Any]] = []
    for path in sorted(root.glob(f"*/{date_value}.json")):
        payload = read_json(path)
        source_id = str(payload.get("source_id") or path.parent.name)
        raw_rows = payload.get("observations")
        if isinstance(raw_rows, list):
            for row in raw_rows:
                if isinstance(row, dict):
                    rows.append({**row, "source_id": row.get("source_id") or source_id})
    return rows


def content_views_total(project_root: Path, date_value: str) -> dict[str, Any]:
    component_ids = ["instagram_views", "x_views", "github_views"]
    latest_by_metric: dict[str, dict[str, Any]] = {}
    root = project_root / OBSERVATION_ROOT
    if not root.exists():
        rows = []
    else:
        rows = []
        for path in sorted(root.glob("*/*.json")):
            if path.stem > date_value:
                continue
            payload = read_json(path)
            source_id = str(payload.get("source_id") or path.parent.name)
            raw_rows = payload.get("observations")
            if isinstance(raw_rows, list):
                for row in raw_rows:
                    if isinstance(row, dict):
                        rows.append({**row, "source_id": row.get("source_id") or source_id})
    for row in rows:
        metric_id = str(row.get("metric_id") or "")
        if metric_id not in component_ids:
            continue
        if str(row.get("status") or "available") != "available":
            continue
        value = row.get("value")
        if not isinstance(value, (int, float)):
            continue
        row_date = str(row.get("date") or "")
        previous = latest_by_metric.get(metric_id)
        if previous is None or row_date > str(previous.get("date") or ""):
            latest_by_metric[metric_id] = row
    components = [
        {
            "metric_id": metric_id,
            "date": str(row.get("date") or ""),
            "value": float(row.get("value")),
            "source_id": row.get("source_id"),
        }
        for metric_id, row in sorted(latest_by_metric.items())
    ]
    if not components:
        return reading(
            None,
            "source_gap",
            {
                "components": [],
                "missing_components": component_ids,
                "gaps": ["no_component_view_observations"],
                "as_of_date": date_value,
            },
        )
    seen = {str(component["metric_id"]) for component in components}
    return reading(
        sum(float(component["value"]) for component in components),
        "available",
        {
            "components": components,
            "missing_components": [metric_id for metric_id in component_ids if metric_id not in seen],
            "as_of_date": date_value,
            "component_policy": "latest_available_on_or_before_date",
            "gaps": [],
        },
    )


def primitive_snapshot(
    project_root: Path,
    date_value: str,
    codex_home: Path,
    monthly_spend: float | None,
    write: bool = True,
    ticket_status: str | None = None,
) -> dict[str, Any]:
    project_root = project_root.resolve()
    window = window_for_date(date_value)
    metric_recipe_map = metric_recipes(project_root)
    effective_monthly_spend = monthly_spend if monthly_spend is not None else configured_monthly_ai_spend(project_root)
    ticket_basics, tickets, ticket_gaps = ticket_counts(project_root, window)
    by_kpi = ticket_count_by_kpi(tickets, window)
    if ticket_status:
        by_kpi_status = ticket_count_by_kpi_with_status(tickets, window, ticket_status)
    else:
        by_kpi_status = {}
    by_product = ticket_count_by_product(tickets, window, metric_recipe_map)
    thread_usage = fetch_codex_thread_usage(codex_home.expanduser(), project_root, window)
    burn = estimate_ai_burn(window, thread_usage, effective_monthly_spend)
    association_path = project_root / ASSOCIATION_PATH
    association = backfill_ticket_thread_associations(project_root, project_root / ".farplane" / "mine" / "runs", association_path, write=write)
    association_rows = read_jsonl(association_path) if write else []
    coverage = ticket_thread_link_coverage(tickets, window, association_rows)
    distribution_reach = content_views_total(project_root, date_value)
    diagnostic_gaps = [
        *ticket_gaps,
        *association.get("payload", {}).get("gaps", []),
    ]
    source_gaps = [
        *thread_usage.get("payload", {}).get("gaps", []),
        *burn.get("payload", {}).get("gaps", []),
        *coverage.get("payload", {}).get("gaps", []),
    ]
    payload = {
        "ok": True,
        "schema_version": 1,
        "generated_at": now_utc(),
        "project_root": str(project_root),
        "date": date_value,
        "window": {"start": window.start.isoformat(), "end": window.end.isoformat()},
        "primitives": {
            **ticket_basics,
            "ticket_count_by_kpi": by_kpi,
            "ticket_count_by_product": by_product,
            "codex_thread_usage": thread_usage,
            "ai_burn_estimate": burn,
            "content_views_total": {"evidence_distribution_reach": distribution_reach},
            "ticket_thread_association_backfill": association,
            "ticket_thread_link_coverage": coverage,
        },
        "diagnostics": {
            "ticket_parse_gaps": sorted(set(str(gap) for gap in ticket_gaps if gap)),
            "non_warning_gaps": sorted(set(str(gap) for gap in diagnostic_gaps if gap)),
        },
        "source_gaps": sorted(set(str(gap) for gap in source_gaps if gap)),
        "paths": {
            "daily_metrics": str(project_root / DAILY_METRICS_ROOT / f"{date_value}.json"),
            "observation_root": str(project_root / OBSERVATION_ROOT),
            "ticket_thread_associations": str(association_path),
        },
    }
    if ticket_status:
        payload["primitives"][f"ticket_count_by_kpi_status:{ticket_status}"] = by_kpi_status
    if write:
        write_primitive_outputs(project_root, date_value, payload)
    return payload


def write_primitive_outputs(project_root: Path, date_value: str, payload: dict[str, Any]) -> None:
    daily_path = project_root / DAILY_METRICS_ROOT / f"{date_value}.json"
    write_json(daily_path, payload)
    primitives = payload.get("primitives") if isinstance(payload.get("primitives"), dict) else {}
    for primitive_id, primitive_payload in primitives.items():
        write_json(project_root / OBSERVATION_ROOT / primitive_id / f"{date_value}.json", primitive_payload if isinstance(primitive_payload, dict) else {})
        observations = primitive_observations(primitive_id, primitive_payload, date_value)
        gaps = primitive_gaps(primitive_payload)
        write_metric_batch(
            project_root,
            primitive_id,
            date_value,
            observations,
            gaps=gaps,
            status=batch_status(observations, gaps),
        )


def primitive_gaps(payload: Any) -> list[str]:
    if isinstance(payload, dict):
        gaps = payload.get("payload", {}).get("gaps") if isinstance(payload.get("payload"), dict) else payload.get("gaps")
        if isinstance(gaps, list):
            return [str(gap) for gap in gaps if gap]
    return []


def batch_status(observations: list[MetricObservation], gaps: list[str]) -> str:
    if any(observation.status == "available" for observation in observations):
        return "partial" if gaps else "available"
    if any(observation.status == "blocked" for observation in observations):
        return "blocked"
    return "source_gap"


def primitive_observations(primitive_id: str, primitive_payload: Any, date_value: str) -> list[MetricObservation]:
    if not isinstance(primitive_payload, dict):
        return []
    if "value" in primitive_payload or "status" in primitive_payload:
        return [
            metric_observation(
                primitive_id,
                date_value,
                primitive_payload.get("value"),
                normalize_status(primitive_payload.get("status")),
                primitive_payload.get("payload") if isinstance(primitive_payload.get("payload"), dict) else {},
            )
        ]
    observations: list[MetricObservation] = []
    for key, value in sorted(primitive_payload.items(), key=lambda item: str(item[0])):
        if not isinstance(value, dict) or ("value" not in value and "status" not in value):
            continue
        metric_id = f"{primitive_id}:{key}" if primitive_id == "ticket_count_by_product" else str(key)
        observations.append(
            metric_observation(
                metric_id,
                date_value,
                value.get("value"),
                normalize_status(value.get("status")),
                value.get("payload") if isinstance(value.get("payload"), dict) else {},
            )
        )
    return observations


def normalize_status(value: Any) -> str:
    raw = str(value or "available")
    return raw if raw in {"available", "source_gap", "not_applicable", "blocked"} else "source_gap"


def run_primitives(args: argparse.Namespace) -> int:
    project_root = Path(args.project_root).expanduser().resolve()
    date_value = args.date or datetime.now(timezone.utc).date().isoformat()
    payload = primitive_snapshot(
        project_root=project_root,
        date_value=date_value,
        codex_home=Path(args.codex_home).expanduser(),
        monthly_spend=args.monthly_spend,
        write=not args.no_write,
        ticket_status=getattr(args, "ticket_status", None),
    )
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        gap_count = len(payload.get("source_gaps", []))
        print(f"primitive metrics {date_value}: {len(payload.get('primitives', {}))} groups, {gap_count} source gaps")
    return 0
