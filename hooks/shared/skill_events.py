"""Skill invocation and request rows for the bunker's `skill-invocation-listener` hook stream.

One row per fact, posted to the Convex site's `/telemetry/hooks` (the lifecycle ping's ingress):
- `skill_invoked` (hookType PostToolUse): a skill actually loaded; skill heat counts these.
- `skill_requested` (hookType UserPromptSubmit): a prompt named the skill; heat keeps it separate.
Convex drops a repeated `eventKey`, so a replayed hook payload never counts twice.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

CORE_DIR = Path(__file__).resolve().parents[2] / "bin" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))
from farplane_convex import telemetry_project_id  # noqa: E402
from runtime_config import read_config_value  # noqa: E402

HOOK_NAME = "skill-invocation-listener"
HOOK_TYPES = {"skill_invoked": "PostToolUse", "skill_requested": "UserPromptSubmit"}


def plugin_and_name(ref: str) -> tuple[str, str]:
    """`farplane:commit` -> (`farplane`, `commit`); a bare name has no plugin."""
    plugin, _, name = ref.strip().rpartition(":")
    return plugin, name


def project_root(cwd: str) -> Path | None:
    if not cwd.strip():
        return None
    start = Path(cwd).expanduser()
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
    return start


def skill_event_row(
    *,
    kind: str,
    skill: str,
    session_id: str,
    anchor: str,
    cwd: str,
    source: str,
    runtime: str,
    plugin: str = "",
    tool_name: str = "",
    skill_path: str = "",
    turn_id: str = "",
) -> dict[str, object]:
    """The `/telemetry/hooks` body; `anchor` (turn or tool-use id) makes the dedup key."""
    root = project_root(cwd)
    return {
        "hookName": HOOK_NAME,
        "hookType": HOOK_TYPES[kind],
        "projectId": telemetry_project_id(root) if root else None,
        "sessionId": session_id or None,
        "eventKey": f"{HOOK_NAME}:{kind}:{session_id}:{anchor}:{plugin}:{skill}" if session_id and anchor else None,
        "payload": {
            "eventType": kind,
            "skillId": skill,
            "plugin": plugin or None,
            "skillPath": skill_path or None,
            "toolName": tool_name or None,
            "source": source,
            "runtime": runtime,
            "sessionId": session_id or None,
            "turnId": turn_id or None,
            "cwd": str(root) if root else None,
            "label": "Skill tool call" if source == "skill_tool" else "Read skill MD" if source == "skill_read" else "Prompt named skill",
        },
    }


def skip_telemetry() -> bool:
    """Eval and judge runs never count as use (same rule as the lifecycle ping)."""
    purpose = os.getenv("FARPLANE_CODEX_RUNTIME_PURPOSE", "").strip().lower()
    kind = os.getenv("FARPLANE_CODEX_RUNTIME_KIND", "").strip().lower()
    return purpose == "eval" or (kind == "ephemeral" and purpose in {"eval", "judge", "baseline"})


def endpoint() -> str:
    explicit = read_config_value("FARPLANE_TELEMETRY_HOOKS_URL")
    if explicit:
        return explicit
    site = read_config_value("FARPLANE_CONVEX_SITE_URL")
    return f"{site.rstrip('/')}/telemetry/hooks" if site else ""


def post_skill_event(row: dict[str, object]) -> bool:
    """Send one row; False when unconfigured or refused. Never raises, never blocks a turn."""
    url = endpoint()
    if not url or skip_telemetry():
        return False
    headers = {"content-type": "application/json"}
    token = read_config_value("FARPLANE_TELEMETRY_TOKEN")
    if token:
        headers["x-farplane-telemetry-token"] = token
    body = {key: value for key, value in row.items() if value is not None}
    body["payload"] = {key: value for key, value in dict(row["payload"]).items() if value is not None}
    request = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=2) as response:
            return 200 <= response.status < 300
    except Exception as exc:  # noqa: BLE001 - telemetry must never fail the hook
        reason = getattr(exc, "code", None) or type(exc).__name__
        print(f"farplane: skill telemetry not delivered ({reason})", file=sys.stderr)
        return False


PROMPT_SKILL_PATTERN = re.compile(r"(?<![\w$])\$([a-z][a-z0-9-]*)")


def prompt_names_skill(prompt: str) -> bool:
    """A `$name` in the prompt: Codex injects that skill itself, so the turn already has its skill."""
    return bool(PROMPT_SKILL_PATTERN.search(prompt or ""))
