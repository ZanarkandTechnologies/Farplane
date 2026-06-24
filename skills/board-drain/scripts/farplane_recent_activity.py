#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable
try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None  # type: ignore[assignment]


DEFAULT_ACTIVE_EVENT_TYPES = (
    "turn_start",
    "turn_end",
    "hook_result",
    "learning_window_updated",
    "learning_review_launched",
)


def clean_env(value: str | None) -> str:
    cleaned = value.strip() if isinstance(value, str) else ""
    if cleaned.startswith("__") and cleaned.endswith("__"):
        return ""
    return cleaned


def codex_config_value(key: str, config_path: Path | None = None) -> str:
    if tomllib is None:
        return ""
    path = config_path or (Path.home() / ".codex" / "config.toml")
    if not path.exists():
        return ""
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return ""
    value = data.get(key)
    if not isinstance(value, str):
        env = data.get("env")
        value = env.get(key) if isinstance(env, dict) else ""
    return clean_env(value)


def console_activity_url(explicit_url: str, site_url: str) -> str:
    if explicit_url:
        return explicit_url
    if not site_url:
        return ""
    return urllib.parse.urljoin(site_url.rstrip("/") + "/", "api/activity/recent")


def parse_timestamp(raw: object) -> datetime | None:
    if not isinstance(raw, str) or not raw.strip():
        return None
    normalized = raw.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def event_files(project_root: Path) -> list[Path]:
    event_dir = project_root / ".farplane" / "events"
    if not event_dir.exists():
        return []
    return sorted(path for path in event_dir.glob("*.jsonl") if path.is_file() and path.name != "failed-sync.jsonl")


def load_local_recent_events(
    project_root: Path,
    *,
    now: datetime,
    window_minutes: int,
    active_event_types: Iterable[str],
) -> list[dict[str, object]]:
    cutoff = now.astimezone(timezone.utc) - timedelta(minutes=window_minutes)
    active_type_set = {event_type for event_type in active_event_types if event_type}
    recent: list[dict[str, object]] = []
    for path in event_files(project_root):
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            if not raw_line.strip():
                continue
            try:
                payload = json.loads(raw_line)
            except json.JSONDecodeError:
                continue
            if not isinstance(payload, dict):
                continue
            event_type = payload.get("event_type")
            if active_type_set and event_type not in active_type_set:
                continue
            timestamp = parse_timestamp(payload.get("timestamp"))
            if timestamp is None or timestamp < cutoff or timestamp > now:
                continue
            recent.append(payload)
    return recent


def summarize_local_recent_activity(
    project_root: Path,
    *,
    window_minutes: int = 60,
    now: datetime | None = None,
    active_event_types: Iterable[str] = DEFAULT_ACTIVE_EVENT_TYPES,
) -> dict[str, object]:
    effective_now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    recent = load_local_recent_events(
        project_root,
        now=effective_now,
        window_minutes=window_minutes,
        active_event_types=active_event_types,
    )
    latest = recent[-1] if recent else None
    return {
        "ok": True,
        "provider": "local_events",
        "active": bool(recent),
        "windowMinutes": window_minutes,
        "checkedAt": int(effective_now.timestamp() * 1000),
        "eventCount": len(recent),
        "latestEvent": latest or None,
        "checkedFiles": [str(path) for path in event_files(project_root)],
        "activeEventTypes": list(active_event_types),
    }


def summarize_console_recent_activity(
    *,
    activity_url: str,
    key: str,
    project_root: Path,
    project_name: str,
    project_directory: str,
    window_minutes: int,
    timeout_seconds: float,
) -> dict[str, object]:
    if not activity_url:
        return {
            "ok": False,
            "provider": "farplane_console",
            "active": False,
            "error": "missing_activity_url",
            "hint": "set FARPLANE_ACTIVITY_RECENT_URL or FARPLANE_CONVEX_SITE_URL",
        }
    if not key:
        return {
            "ok": False,
            "provider": "farplane_console",
            "active": False,
            "error": "missing_key",
            "hint": "set FARPLANE_CONSOLE_KEY or FARPLANE_TELEMETRY_TOKEN",
        }

    query = {
        "windowMinutes": str(window_minutes),
        "projectName": project_name or project_root.name,
        "projectDirectory": project_directory or str(project_root),
    }
    url_parts = urllib.parse.urlsplit(activity_url)
    merged_query = urllib.parse.urlencode({**dict(urllib.parse.parse_qsl(url_parts.query)), **query})
    request_url = urllib.parse.urlunsplit((url_parts.scheme, url_parts.netloc, url_parts.path, merged_query, url_parts.fragment))
    request = urllib.request.Request(
        request_url,
        headers={
            "accept": "application/json",
            "authorization": f"Bearer {key}",
            "x-farplane-telemetry-token": key,
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        return {
            "ok": False,
            "provider": "farplane_console",
            "active": False,
            "error": f"http_{error.code}",
        }
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        return {
            "ok": False,
            "provider": "farplane_console",
            "active": False,
            "error": str(error),
        }

    if not isinstance(payload, dict):
        return {
            "ok": False,
            "provider": "farplane_console",
            "active": False,
            "error": "invalid_response",
        }

    payload["provider"] = "farplane_console"
    return payload


def summarize_recent_activity(
    project_root: Path,
    *,
    window_minutes: int = 60,
    activity_url: str = "",
    key: str = "",
    project_name: str = "",
    project_directory: str = "",
    timeout_seconds: float = 2.0,
    allow_local_fallback: bool = False,
    now: datetime | None = None,
    active_event_types: Iterable[str] = DEFAULT_ACTIVE_EVENT_TYPES,
) -> dict[str, object]:
    console_summary = summarize_console_recent_activity(
        activity_url=activity_url,
        key=key,
        project_root=project_root,
        project_name=project_name,
        project_directory=project_directory,
        window_minutes=window_minutes,
        timeout_seconds=timeout_seconds,
    )
    if console_summary.get("ok") or not allow_local_fallback:
        return console_summary

    local_summary = summarize_local_recent_activity(
        project_root,
        window_minutes=window_minutes,
        now=now,
        active_event_types=active_event_types,
    )
    local_summary["fallbackReason"] = console_summary.get("error", "console_unavailable")
    return local_summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Report recent Farplane project activity through Farplane Console.")
    parser.add_argument("--project-root", default=".", help="Farplane project root. Defaults to cwd.")
    parser.add_argument("--window-minutes", type=int, default=60, help="Lookback window in minutes. Defaults to 60.")
    parser.add_argument("--activity-url", default="", help="Explicit Farplane Console /api/activity/recent URL.")
    parser.add_argument("--site-url", default="", help="Farplane Console Convex site URL used to build /api/activity/recent.")
    parser.add_argument("--key", default="", help="Farplane Console ingest key. Defaults to environment variables.")
    parser.add_argument("--project-name", default="", help="Project name filter. Defaults to project root folder.")
    parser.add_argument("--project-directory", default="", help="Project directory filter. Defaults to project root path.")
    parser.add_argument("--timeout-seconds", type=float, default=2.0)
    parser.add_argument(
        "--allow-local-fallback",
        action="store_true",
        help="Use local .farplane event logs only when the Console endpoint is unavailable.",
    )
    parser.add_argument(
        "--active-event-types",
        default=",".join(DEFAULT_ACTIVE_EVENT_TYPES),
        help="Comma-separated event_type values that count as local fallback activity.",
    )
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    project_root = Path(args.project_root).expanduser().resolve()
    site_url = (
        clean_env(args.site_url)
        or clean_env(os.getenv("FARPLANE_CONVEX_SITE_URL"))
        or clean_env(os.getenv("CONVEX_SITE_URL"))
        or codex_config_value("FARPLANE_CONVEX_SITE_URL")
        or codex_config_value("CONVEX_SITE_URL")
    )
    activity_url = (
        clean_env(args.activity_url)
        or clean_env(os.getenv("FARPLANE_ACTIVITY_RECENT_URL"))
        or codex_config_value("FARPLANE_ACTIVITY_RECENT_URL")
    )
    key = (
        clean_env(args.key)
        or clean_env(os.getenv("FARPLANE_CONSOLE_KEY"))
        or clean_env(os.getenv("FARPLANE_TELEMETRY_TOKEN"))
        or codex_config_value("FARPLANE_CONSOLE_KEY")
        or codex_config_value("FARPLANE_TELEMETRY_TOKEN")
    )
    event_types = [item.strip() for item in args.active_event_types.split(",") if item.strip()]
    summary = summarize_recent_activity(
        project_root,
        window_minutes=args.window_minutes,
        activity_url=console_activity_url(activity_url, site_url),
        key=key,
        project_name=clean_env(args.project_name) or project_root.name,
        project_directory=clean_env(args.project_directory) or str(project_root),
        timeout_seconds=args.timeout_seconds,
        allow_local_fallback=args.allow_local_fallback,
        active_event_types=event_types,
    )
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    elif summary.get("active"):
        latest = summary.get("latestEvent")
        event_type = latest.get("eventType") if isinstance(latest, dict) else ""
        received_at = latest.get("receivedAt") if isinstance(latest, dict) else ""
        print(f"active: {summary.get('eventCount', 0)} events in {summary.get('windowMinutes', args.window_minutes)}m; latest {event_type} at {received_at}")
    elif summary.get("ok"):
        print(f"idle: no matching Console activity in {summary.get('windowMinutes', args.window_minutes)}m")
    else:
        print(f"unknown: {summary.get('error', 'activity_check_failed')}")
    return 0 if summary.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
