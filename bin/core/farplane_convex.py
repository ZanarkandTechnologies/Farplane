"""Farplane's client for the bunker's Convex deployment (Farplane-UI-v2/convex): metric readings in, telemetry events out.

- Site routes (POST + JSON, `x-farplane-telemetry-token`) on FARPLANE_CONVEX_SITE_URL: `/metrics/readings`,
  `/metrics/latest`, `/metrics/history`.
- Public queries through `/api/query` on the deployment URL (CONVEX_URL): the telemetry `events` table,
  hook rows (`source: hook`) and runtime rows (`source: runtime`).

Settings resolve through `runtime_config.load_runtime_env`. Errors name the route and status, never the token.
"""

from __future__ import annotations

import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping
from urllib import error, request

try:
    from runtime_config import load_runtime_env
except ImportError:  # pragma: no cover - package import path used by tests
    from bin.core.runtime_config import load_runtime_env

TOKEN_HEADER = "x-farplane-telemetry-token"
TIMEOUT_SECS = 20.0
READINGS_BATCH = 200  # the deployment's MAX_BATCH per `/metrics/readings` call
# Runtime rows (`/ingest`) are this team's activity log; the hook rows come from the lifecycle hook.
TELEMETRY_TEAM = "farplane"
RUNTIME_AGENT = "farplane-runtime"
LIFECYCLE_HOOK = "farplane-console-ping"
HUMAN_PROMPT_EVENTS = {"turn_start", "user_prompt", "prompt"}
HOOK_WINDOW_MAX_DAYS = 90
HOOK_ROW_LIMIT = 5000
RUNTIME_PAGE = 300
RUNTIME_MAX_PAGES = 100


class ConvexUnavailable(RuntimeError):
    """Convex isn't configured or didn't answer; the message says which, without secrets."""


def convex_settings(env: Mapping[str, str] | None = None) -> dict[str, str]:
    merged = load_runtime_env(env)
    return {
        "site_url": str(merged.get("FARPLANE_CONVEX_SITE_URL") or "").strip().rstrip("/"),
        "deployment_url": str(merged.get("CONVEX_URL") or "").strip().rstrip("/"),
        "token": str(merged.get("FARPLANE_TELEMETRY_TOKEN") or "").strip(),
    }


def _post_json(url: str, label: str, body: Mapping[str, Any], headers: Mapping[str, str]) -> Any:
    data = json.dumps(dict(body)).encode("utf-8")
    req = request.Request(url, data=data, headers={"Content-Type": "application/json", **headers}, method="POST")
    try:
        with request.urlopen(req, timeout=TIMEOUT_SECS) as response:
            raw = response.read()
    except error.HTTPError as exc:
        reason = ""
        try:
            answer = json.loads(exc.read() or b"{}")
            reason = str(answer.get("error") or answer.get("errorMessage") or "") if isinstance(answer, dict) else ""
        except (ValueError, OSError):
            pass
        raise ConvexUnavailable(f"{label}: HTTP {exc.code}{': ' + reason[:200] if reason else ''}") from None
    except (error.URLError, TimeoutError, OSError) as exc:
        reason = getattr(exc, "reason", None) or exc
        raise ConvexUnavailable(f"{label}: unreachable ({str(reason)[:200]})") from None
    try:
        return json.loads(raw or b"null")
    except ValueError:
        raise ConvexUnavailable(f"{label}: answer is not JSON") from None


def site_post(path: str, body: Mapping[str, Any], settings: Mapping[str, str] | None = None) -> Any:
    """POST a token-checked site route; returns its `result`."""
    config = settings or convex_settings()
    if not config["site_url"]:
        raise ConvexUnavailable("FARPLANE_CONVEX_SITE_URL is not set")
    if not config["token"]:
        raise ConvexUnavailable("FARPLANE_TELEMETRY_TOKEN is not set")
    answer = _post_json(f"{config['site_url']}{path}", path, body, {TOKEN_HEADER: config["token"]})
    if not isinstance(answer, dict) or not answer.get("ok"):
        reason = answer.get("error") if isinstance(answer, dict) else "unexpected answer"
        raise ConvexUnavailable(f"{path}: refused ({str(reason)[:200]})")
    return answer.get("result")


def convex_query(function: str, args: Mapping[str, Any], settings: Mapping[str, str] | None = None) -> Any:
    """Run a public query (`module/path:name`) through the deployment's `/api/query`."""
    config = settings or convex_settings()
    if not config["deployment_url"]:
        raise ConvexUnavailable("CONVEX_URL is not set")
    answer = _post_json(
        f"{config['deployment_url']}/api/query",
        function,
        {"path": function, "args": dict(args), "format": "json"},
        {},
    )
    if not isinstance(answer, dict) or answer.get("status") != "success":
        reason = answer.get("errorMessage") if isinstance(answer, dict) else "unexpected answer"
        raise ConvexUnavailable(f"{function}: failed ({str(reason)[:200]})")
    return answer.get("value")


# --- Metric readings -------------------------------------------------------------------------------


def push_readings(readings: list[dict[str, Any]], settings: Mapping[str, str] | None = None) -> dict[str, int]:
    """Record readings in batches; the same project + metric + at replaces, so reruns are safe."""
    config = settings or convex_settings()
    totals = {"sent": 0, "inserted": 0, "updated": 0}
    for start in range(0, len(readings), READINGS_BATCH):
        batch = readings[start : start + READINGS_BATCH]
        result = site_post("/metrics/readings", {"readings": batch}, config) or {}
        totals["sent"] += len(batch)
        totals["inserted"] += int(result.get("inserted") or 0)
        totals["updated"] += int(result.get("updated") or 0)
    return totals


def latest_readings(project: str | None = None, settings: Mapping[str, str] | None = None) -> list[dict[str, Any]]:
    result = site_post("/metrics/latest", {"project": project} if project else {}, settings)
    return result if isinstance(result, list) else []


def to_ms(value: Any) -> int | None:
    """Epoch ms for an ISO date or datetime (a bare date is midnight UTC), or None."""
    raw = str(value or "").strip()
    if not raw:
        return None
    try:
        parsed = datetime.fromisoformat(raw[:-1] + "+00:00" if raw.endswith("Z") else raw)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return int(parsed.timestamp() * 1000)


def project_slug(name: str) -> str:
    """The company.json slug the bunker matches floors by: lower-case, non-alphanumerics hyphenated."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


# --- Telemetry events ------------------------------------------------------------------------------


def telemetry_project_id(project_root: Path) -> str:
    """The `projectId` the lifecycle hook writes for a checkout (`codex-proj-<path slug>`)."""
    slug = re.sub(r"[^a-z0-9_.:-]+", "-", str(project_root).lower())
    slug = re.sub(r"-+", "-", slug).strip("-")
    return f"codex-proj-{(slug or 'unknown')[:120]}"


def _iso(ms: Any) -> str:
    return datetime.fromtimestamp(float(ms) / 1000, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def _hook_prompt_row(row: Mapping[str, Any]) -> dict[str, Any] | None:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    if str(payload.get("eventType") or "") not in HUMAN_PROMPT_EVENTS or not isinstance(row.get("eventAt"), (int, float)):
        return None
    return {
        "event_type": str(payload.get("eventType")),
        "session_id": str(row.get("sessionId") or payload.get("sessionId") or ""),
        "turn_id": str(payload.get("turnId") or ""),
        "timestamp": _iso(row["eventAt"]),
        "actor": "user",
        "telemetry_source": "hook",
    }


def _runtime_prompt_row(row: Mapping[str, Any]) -> dict[str, Any] | None:
    if str(row.get("activityType") or "") not in HUMAN_PROMPT_EVENTS or not isinstance(row.get("occurredAt"), (int, float)):
        return None
    try:
        detail = json.loads(str(row.get("detail") or "{}"))
    except ValueError:
        detail = {}
    return {
        "event_type": str(row.get("activityType")),
        "session_id": str(row.get("sessionKey") or ""),
        "turn_id": str(detail.get("turnId") or "") if isinstance(detail, dict) else "",
        "timestamp": _iso(row["occurredAt"]),
        "actor": "user",
        "telemetry_source": "runtime",
    }


def _dedupe(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """One row per human turn: the hook and the runtime both record the same prompt."""
    seen: set[tuple[str, str]] = set()
    out: list[dict[str, Any]] = []
    for row in sorted(rows, key=lambda item: (to_ms(item["timestamp"]) or 0, item["telemetry_source"] != "hook")):
        key = (row["session_id"], row["turn_id"] or row["timestamp"][:19])
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def read_human_prompts(
    project_root: Path,
    since: datetime,
    settings: Mapping[str, str] | None = None,
    now: datetime | None = None,
) -> tuple[list[dict[str, Any]], list[str]]:
    """Human prompt events of one checkout since `since`, from Convex hook and runtime rows.

    Returns (rows, gaps). Raises ConvexUnavailable when the deployment can't be read.
    """
    config = settings or convex_settings()
    project_id = telemetry_project_id(project_root)
    since_ms = int(since.timestamp() * 1000)
    current = now or datetime.now(timezone.utc)
    gaps: list[str] = []
    days = max(1, math.ceil((current - since).total_seconds() / 86400) + 1)
    if days > HOOK_WINDOW_MAX_DAYS:
        gaps.append(f"telemetry_window:convex keeps hook reads to {HOOK_WINDOW_MAX_DAYS} days")
    hook_rows = convex_query(
        "modules/hookTelemetry/queries:listHookTelemetryEvents",
        {
            "projectId": project_id,
            "hookName": LIFECYCLE_HOOK,
            "hookType": "UserPromptSubmit",
            "rangeDays": min(days, HOOK_WINDOW_MAX_DAYS),
            "limit": HOOK_ROW_LIMIT,
        },
        config,
    ) or []
    if len(hook_rows) >= HOOK_ROW_LIMIT and min(row.get("eventAt", 0) for row in hook_rows) > since_ms:
        gaps.append(f"telemetry_truncated:hook rows capped at {HOOK_ROW_LIMIT}")
    rows = [row for row in map(_hook_prompt_row, hook_rows) if row and to_ms(row["timestamp"]) >= since_ms]

    before: float | None = None
    for _ in range(RUNTIME_MAX_PAGES):
        args: dict[str, Any] = {"teamId": TELEMETRY_TEAM, "projectId": project_id, "limit": RUNTIME_PAGE}
        if before:
            args["beforeTs"] = before
        page = convex_query("modules/telemetry/queries:getTeamActivityFeed", args, config) or {}
        events = page.get("events") if isinstance(page, dict) else []
        for event in events or []:
            if isinstance(event.get("occurredAt"), (int, float)) and event["occurredAt"] >= since_ms:
                row = _runtime_prompt_row(event)
                if row:
                    rows.append(row)
        oldest = min((event.get("occurredAt", 0) for event in events or []), default=0)
        before = page.get("nextBeforeTs") if isinstance(page, dict) else None
        if not page.get("hasMore") or not before or oldest < since_ms:
            break
    else:
        gaps.append(f"telemetry_truncated:runtime rows beyond {RUNTIME_MAX_PAGES} pages")
    return _dedupe(rows), gaps


def telemetry_gap(exc: Exception) -> str:
    return f"telemetry_unavailable:convex events ({exc})"
