#!/usr/bin/env python3
"""
CODEXTER STOP HOOK
==================
Purpose

Decide whether a turn should stop or continue by running an ephemeral
Codex classification pass against the latest assistant message plus the
active ticket state.

KEY CONCEPTS:
- Assisted continuation is opt-in via environment flag.
- Continuation is bounded to one extra pass per stop chain.
- Final authority stays local even when the classification is model-backed.

USAGE:
- Invoked by Codex Stop hook with one JSON object on stdin.

MEMORY REFERENCES:
- MEM-0002
- MEM-0004
- MEM-0010
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import tomllib
from datetime import datetime, timezone
from pathlib import Path

from notify import announce_message
from user_turn import (
    build_runtime_claim,
    explicit_run_state_selector as resolve_explicit_run_state_selector,
    load_last_user_turn as load_persisted_last_user_turn,
    load_current_run as load_selected_runtime_state,
    load_runtime_claim as load_persisted_runtime_claim,
    persist_runtime_update as persist_selected_runtime_update,
    project_root_from_payload as resolve_project_root_from_payload,
)


TICKET_ID_PATTERN = re.compile(r"\bTASK-\d{4}\b")
SECTION_PATTERN = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
CHECKBOX_PATTERN = re.compile(r"^- \[( |x)\]\s+(.*)$")
REVIEW_PACKET_FIELD_PATTERN = re.compile(r"^- `(?P<key>[^`]+)`\s*(?P<value>.*)$")
IMPL_RESULT_PATTERN = re.compile(r"^IMPL_RESULT:\s+status=.*$", re.MULTILINE)
PARSED_IMPL_RESULT_PATTERN = re.compile(
    r"^IMPL_RESULT:\s+status=(?P<status>[A-Za-z0-9_-]+)\s+next=(?P<next>[A-Za-z0-9_-]+)(?:\s+reason=(?P<reason>.*))?$"
)
ALLOWED_PHASES = {"planning", "building", "documenting"}
ROLE_ACTIONS = {
    "continue_same_ticket",
    "route_to_orchestrator",
    "block_for_user",
    "next_ticket",
    "stop",
}
REVIEW_PACKET_REQUIRED_FIELDS = {
    "reviewed_at",
    "overall_verdict",
    "rerun_required",
    "evidence_quality",
    "integration_readiness",
    "traceability",
    "freshness",
    "hard_gate_failures",
    "blocking_findings",
    "next_action",
}
PASS_FAIL_VALUES = {"pass", "fail"}
REVIEW_VERDICTS = {"pass", "revise", "block"}
REVIEW_PACKET_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M %z"
INTENT_ALIGNMENT_STATES = {"aligned", "soft_mismatch", "hard_mismatch", "unknown"}
IMPL_LOOPABLE_PHASES = {"building"}


def env_enabled() -> bool:
    legacy = os.environ.get("CODEXTER_ASSISTED_CONTINUATION", "").lower() in {
        "1",
        "true",
        "yes",
        "on",
    }
    impl = os.environ.get("CODEXTER_IMPL_HOOK", "").lower() in {
        "1",
        "true",
        "yes",
        "on",
    }
    return legacy or impl


def has_project_runtime_context(project_root: Path | None) -> bool:
    if project_root is None:
        return False
    return (project_root / ".harness").exists() or (project_root / "tickets").exists()


def has_explicit_ticket_selector() -> bool:
    return bool(
        os.environ.get("IMPL_TICKET", "").strip()
        or os.environ.get("CODEXTER_ACTIVE_TICKET", "").strip()
    )


def hook_enabled_for_context(
    project_root: Path | None,
    current_run: dict[str, object] | None,
    impl_result: str | None,
) -> bool:
    # Keep the env flag as an explicit override, but auto-activate when the
    # hook is clearly running inside a Codexter/impl context.
    return (
        env_enabled()
        or current_run is not None
        or impl_result is not None
        or has_explicit_ticket_selector()
        or has_project_runtime_context(project_root)
    )


def impl_loop_flag_active(
    current_run: dict[str, object] | None,
    runtime_claim: dict[str, object] | None,
    session_id: str | None,
) -> bool:
    # MEM-0025: same-ticket impl continuation needs a dedicated session gate
    # in addition to claim ownership; tmux auto_continue is not enough.
    if current_run is None or not bool(current_run.get("impl_loop_active")):
        return False
    claim = runtime_claim if isinstance(runtime_claim, dict) else {}
    skill_name = str(claim.get("skill_name") or current_run.get("skill_name") or "").strip()
    if skill_name and skill_name != "impl":
        return False
    if session_id:
        claim_session_id = str(claim.get("session_id") or current_run.get("session_id") or "").strip()
        if claim_session_id and claim_session_id != session_id:
            return False
    return True


def ticket_is_impl_loopable(ticket: dict[str, object], current_run: dict[str, object] | None) -> bool:
    phase = str((current_run or {}).get("phase") or ticket.get("phase") or "").strip()
    status = str(ticket.get("status") or "").strip()
    return phase in IMPL_LOOPABLE_PHASES and status not in {"blocked", "done", "failed"}


def impl_loop_matches_ticket(
    ticket: dict[str, object],
    current_run: dict[str, object] | None,
    runtime_claim: dict[str, object] | None,
    session_id: str | None,
) -> bool:
    ticket_id = str(ticket.get("ticket_id") or "").strip()
    if not ticket_id:
        return False
    claim = runtime_claim if isinstance(runtime_claim, dict) else {}
    claim_ticket_id = str(claim.get("ticket_id") or (current_run or {}).get("ticket_id") or "").strip()
    if claim_ticket_id != ticket_id:
        return False
    if session_id:
        claim_session_id = str(claim.get("session_id") or (current_run or {}).get("session_id") or "").strip()
        if claim_session_id and claim_session_id != session_id:
            return False
    return True


def impl_loop_continuation_allowed(
    ticket: dict[str, object],
    current_run: dict[str, object] | None,
    runtime_claim: dict[str, object] | None,
    session_id: str | None,
) -> bool:
    return (
        impl_loop_flag_active(current_run, runtime_claim, session_id)
        and ticket_is_impl_loopable(ticket, current_run)
        and impl_loop_matches_ticket(ticket, current_run, runtime_claim, session_id)
    )


def next_impl_loop_active_for_action(action: str, *, next_phase: str = "", current_phase: str = "") -> bool:
    if action == "repeat_impl":
        return True
    if action == "advance_ticket" and next_phase == "building":
        return True
    if action == "continue_same_ticket" and current_phase == "building":
        return True
    return False


def read_payload() -> tuple[dict[str, object], str]:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return {}, raw
    return (data if isinstance(data, dict) else {}), raw


def codexter_home() -> Path:
    configured = os.environ.get("CODEXTER_HOME", "").strip()
    if configured:
        return Path(configured).expanduser().resolve()

    return Path(__file__).expanduser().absolute().parent.parent


def project_root_from_payload(payload: dict[str, object]) -> Path | None:
    return resolve_project_root_from_payload(payload)


def runtime_root(home: Path, project_root: Path | None) -> Path:
    if project_root is not None and (project_root / "bin" / "stop_hook.py").exists():
        return project_root
    return home


def schema_path() -> Path:
    return Path(__file__).with_name("stop_hook_output.schema.json")


def role_config_path(base: Path, name: str) -> Path:
    return base / "agents" / f"{name}.toml"


def load_role_config(base: Path, role_name: str) -> dict[str, str] | None:
    try:
        payload = tomllib.loads(role_config_path(base, role_name).read_text(encoding="utf-8"))
    except (FileNotFoundError, tomllib.TOMLDecodeError):
        return None

    if not isinstance(payload, dict):
        return None

    developer_instructions = payload.get("developer_instructions")
    if not isinstance(developer_instructions, str) or not developer_instructions.strip():
        return None

    parsed: dict[str, str] = {
        "developer_instructions": developer_instructions.strip(),
    }
    for key in ("model", "model_reasoning_effort"):
        value = payload.get(key)
        if value is None:
            continue
        if not isinstance(value, str) or not value.strip():
            return None
        parsed[key] = value.strip()
    return parsed


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def append_hook_log(base: Path, payload: dict[str, object]) -> None:
    log_dir = base / ".harness" / "logs"
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "stop-hook.jsonl"
        with log_file.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=True) + "\n")
    except OSError:
        fallback = Path("/tmp/codexter-stop-hook.jsonl")
        try:
            with fallback.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(payload, ensure_ascii=True) + "\n")
        except OSError:
            return


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def current_run_state_path(project_root: Path) -> Path:
    return project_root / ".harness" / "state" / "current-run.json"


def load_current_run(
    project_root: Path,
    *,
    session_id: str | None = None,
    explicit_run_state: str | None = None,
) -> dict[str, object] | None:
    return load_selected_runtime_state(
        project_root,
        session_id=session_id,
        explicit_run_state=explicit_run_state,
    )


def resolve_runtime_path(project_root: Path, raw: str) -> Path:
    candidate = Path(raw).expanduser()
    if candidate.is_absolute():
        return candidate
    return (project_root / candidate).resolve()


def persist_runtime_update(
    project_root: Path,
    current_run: dict[str, object],
    updates: dict[str, object],
) -> dict[str, object]:
    return persist_selected_runtime_update(project_root, current_run, updates)


def persist_impl_loop_active(
    project_root: Path | None,
    current_run: dict[str, object] | None,
    active: bool,
) -> dict[str, object] | None:
    if project_root is None or current_run is None:
        return current_run
    return persist_runtime_update(project_root, current_run, {"impl_loop_active": active})


def show_tmux_verdict(current_run: dict[str, object] | None, summary: str) -> None:
    if current_run is None:
        return
    target = current_run.get("tmux_pane") or current_run.get("tmux_session")
    if not isinstance(target, str) or not target.strip():
        return
    subprocess.run(
        ["tmux", "display-message", "-t", target, summary],
        text=True,
        capture_output=True,
        check=False,
    )


def publish_hook_status(
    project_root: Path | None,
    current_run: dict[str, object] | None,
    *,
    decision: str,
    summary: str,
) -> dict[str, object] | None:
    show_tmux_verdict(current_run, summary)
    if project_root is None or current_run is None:
        return current_run
    return persist_runtime_update(
        project_root,
        current_run,
        {
            "last_hook_decision": decision,
            "last_hook_summary": summary,
            "last_hook_timestamp": now_iso(),
        },
    )


def persist_intent_alignment(
    project_root: Path | None,
    current_run: dict[str, object] | None,
    alignment: dict[str, object],
) -> dict[str, object] | None:
    if project_root is None or current_run is None:
        return current_run
    return persist_runtime_update(
        project_root,
        current_run,
        {
            "last_intent_alignment": str(alignment.get("state") or "unknown"),
            "last_intent_alignment_reason": str(alignment.get("reason") or "").strip(),
            "last_intent_turn_id": str(alignment.get("turn_id") or "").strip(),
            "updated_at": now_iso(),
        },
    )


def emit_stop_payload(
    *,
    decision: str | None = None,
    reason: str | None = None,
    system_message: str | None = None,
    continue_value: bool | None = None,
    stop_reason: str | None = None,
) -> int:
    payload: dict[str, object] = {}
    if decision is not None:
        payload["decision"] = decision
    if reason is not None:
        payload["reason"] = reason
    if system_message:
        payload["systemMessage"] = system_message
    if continue_value is not None:
        payload["continue"] = continue_value
    if stop_reason:
        payload["stopReason"] = stop_reason
    if payload:
        json.dump(payload, sys.stdout)
        sys.stdout.write("\n")
    return 0


def classifier_timeout_secs() -> float:
    raw_value = os.environ.get("CODEXTER_STOP_HOOK_TIMEOUT_SECS", "").strip()
    if not raw_value:
        return 30.0

    try:
        parsed = float(raw_value)
    except ValueError:
        return 30.0

    return max(parsed, 1.0)


def parse_sections(ticket_text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    matches = list(SECTION_PATTERN.finditer(ticket_text))
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(ticket_text)
        sections[match.group(1).strip()] = ticket_text[start:end].splitlines()
    return sections


def unchecked_items(lines: list[str]) -> list[str]:
    items: list[str] = []
    for line in lines:
        match = CHECKBOX_PATTERN.match(line.strip())
        if match and match.group(1) == " ":
            items.append(match.group(2).strip())
    return items


def blocked_items(lines: list[str]) -> list[str]:
    items: list[str] = []
    for line in lines:
        stripped = line.strip()
        normalized = stripped.lower()
        if stripped and normalized not in {"- none", "none"}:
            items.append(stripped.lstrip("-").strip())
    return items


def parse_review_packet_value(raw: str) -> object:
    stripped = raw.strip()
    if not stripped:
        return ""
    lowered = stripped.lower()
    if lowered == "none":
        return "none"
    if stripped in {"true", "false"}:
        return stripped == "true"
    if stripped.startswith("[") or stripped.startswith("{"):
        try:
            return json.loads(stripped)
        except json.JSONDecodeError:
            return stripped
    try:
        return float(stripped)
    except ValueError:
        return stripped


def parse_reviewed_at(raw: object) -> datetime | None:
    if not isinstance(raw, str) or not raw.strip():
        return None
    try:
        parsed = datetime.strptime(raw.strip(), REVIEW_PACKET_TIMESTAMP_FORMAT)
    except ValueError:
        return None
    return parsed.replace(second=0, microsecond=0)


def parse_updated_at(raw: object) -> datetime | None:
    if not isinstance(raw, str) or not raw.strip():
        return None
    try:
        parsed = datetime.fromisoformat(raw.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed.astimezone().replace(second=0, microsecond=0)


def parse_review_packet(lines: list[str]) -> dict[str, object]:
    fields: dict[str, object] = {}
    errors: list[str] = []
    for line in lines:
        stripped = line.strip()
        match = REVIEW_PACKET_FIELD_PATTERN.match(stripped)
        if not match:
            continue
        key = match.group("key").strip().rstrip(":")
        value = parse_review_packet_value(match.group("value"))
        if key in {"rubrics_used", "hard_gate_failures", "blocking_findings"}:
            if value == "none":
                value = []
            elif isinstance(value, str):
                value = [value] if value else []
            if not isinstance(value, list):
                errors.append(f"{key} must be a list")
                continue
            if any(not isinstance(item, str) or not item.strip() for item in value):
                errors.append(f"{key} must contain non-empty strings")
                continue
        fields[key] = value

    missing = sorted(REVIEW_PACKET_REQUIRED_FIELDS - set(fields))

    overall_verdict = fields.get("overall_verdict")
    if overall_verdict is not None and overall_verdict not in REVIEW_VERDICTS:
        errors.append("overall_verdict must be pass|revise|block")

    rerun_required = fields.get("rerun_required")
    if rerun_required is not None and not isinstance(rerun_required, bool):
        errors.append("rerun_required must be true|false")

    for key in ("evidence_quality", "integration_readiness", "traceability", "freshness"):
        value = fields.get(key)
        if value is not None and value not in PASS_FAIL_VALUES:
            errors.append(f"{key} must be pass|fail")

    next_action = fields.get("next_action")
    if next_action is not None and (not isinstance(next_action, str) or not next_action.strip()):
        errors.append("next_action must be a non-empty string")

    reviewed_at = fields.get("reviewed_at")
    if reviewed_at is not None and parse_reviewed_at(reviewed_at) is None:
        errors.append("reviewed_at must match YYYY-MM-DD HH:mm ±ZZZZ")

    overall_score = fields.get("overall_score")
    if overall_score is not None and not isinstance(overall_score, (int, float)):
        errors.append("overall_score must be numeric when present")

    return {
        "fields": fields,
        "missing": missing,
        "errors": errors,
        "present": bool(lines),
        "valid": bool(lines) and not missing and not errors,
    }


def extract_ticket_id(text: str) -> str | None:
    match = TICKET_ID_PATTERN.search(text)
    return match.group(0) if match else None


def parse_frontmatter(ticket_text: str) -> dict[str, object]:
    if not ticket_text.startswith("---\n"):
        return {}
    parts = ticket_text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}
    data: dict[str, object] = {}
    lines = parts[0][4:].splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if ":" not in line:
            i += 1
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        if value == "":
            items: list[str] = []
            i += 1
            while i < len(lines) and lines[i].startswith("  - "):
                items.append(lines[i][4:].strip())
                i += 1
            data[key] = items
            continue
        if value == "[]":
            data[key] = []
        elif value in {"true", "false"}:
            data[key] = value == "true"
        else:
            data[key] = value
        i += 1
    return data


def load_ticket(ticket_path: Path) -> dict[str, object]:
    text = ticket_path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(text)
    sections = parse_sections(text)
    review_packet = parse_review_packet(sections.get("Review Packet", []))
    fallback_ticket_id = extract_ticket_id(ticket_path.name) or ticket_path.stem
    return {
        "path": ticket_path,
        "text": text,
        "ticket_id": extract_ticket_id(text) or fallback_ticket_id,
        "title": str(frontmatter.get("title", "")).strip(),
        "phase": str(frontmatter.get("phase", "")).strip(),
        "status": str(frontmatter.get("status", "")).strip(),
        "ready": bool(frontmatter.get("ready", False)),
        "approval_required": bool(frontmatter.get("approval_required", False)),
        "depends_on": list(frontmatter.get("depends_on", [])) if isinstance(frontmatter.get("depends_on", []), list) else [],
        "frontmatter_blocked_by": list(frontmatter.get("blocked_by", [])) if isinstance(frontmatter.get("blocked_by", []), list) else [],
        "updated_at": str(frontmatter.get("updated_at", "")).strip(),
        "next_action": str(frontmatter.get("next_action", "")).strip(),
        "last_verification": str(frontmatter.get("last_verification", "")).strip(),
        "linked_docs": list(frontmatter.get("linked_docs", [])) if isinstance(frontmatter.get("linked_docs", []), list) else [],
        "acceptance_gaps": unchecked_items(sections.get("Acceptance Criteria", [])),
        "evidence_gaps": unchecked_items(sections.get("Evidence", [])),
        "blockers": blocked_items(sections.get("Blockers", [])),
        "review_packet": review_packet["fields"],
        "review_packet_missing": review_packet["missing"],
        "review_packet_errors": review_packet["errors"],
        "review_packet_present": review_packet["present"],
        "review_packet_valid": review_packet["valid"],
    }


def ticket_root(home: Path, project_root: Path | None) -> Path:
    return (project_root or home) / "tickets"


def resolve_ticket_by_id(home: Path, project_root: Path | None, ticket_id: str) -> dict[str, object] | None:
    if not ticket_id.strip():
        return None
    for ticket_file in sorted(ticket_root(home, project_root).glob("TASK-*.md")):
        if ticket_file.name.startswith(ticket_id):
            return load_ticket(ticket_file)
    return None


def board_snapshot(home: Path, project_root: Path | None) -> list[dict[str, object]]:
    snapshot: list[dict[str, object]] = []
    for ticket_file in sorted(ticket_root(home, project_root).glob("TASK-*.md")):
        ticket = load_ticket(ticket_file)
        snapshot.append(
            {
                "ticket_id": ticket["ticket_id"],
                "title": ticket["title"],
                "phase": ticket["phase"],
                "status": ticket["status"],
                "ready": ticket["ready"],
                "approval_required": ticket["approval_required"],
                "depends_on": ticket["depends_on"],
                "blocked_by": ticket["frontmatter_blocked_by"],
                "next_action": ticket["next_action"],
                "last_verification": ticket["last_verification"],
            }
        )
    return snapshot


def resolve_ticket(home: Path, project_root: Path | None, message: str) -> dict[str, object] | None:
    # An explicit per-run selector must outrank ambient state so callers can
    # safely override stale current-run metadata. MEM-0004.
    explicit_path = os.environ.get("IMPL_TICKET", "").strip()
    if explicit_path:
        candidate = Path(explicit_path).expanduser()
        if not candidate.is_absolute() and project_root is not None:
            project_candidate = (project_root / explicit_path).resolve()
            if project_candidate.is_file():
                return load_ticket(project_candidate)
        if not candidate.is_absolute():
            candidate = (home / explicit_path).resolve()
        if candidate.is_file():
            return load_ticket(candidate)

    if project_root is not None:
        current_run = load_current_run(project_root)
        if current_run:
            ticket_path = current_run.get("ticket_path")
            if isinstance(ticket_path, str) and ticket_path.strip():
                candidate = Path(ticket_path).expanduser()
                if not candidate.is_absolute():
                    candidate = (project_root / ticket_path).resolve()
                if candidate.is_file():
                    return load_ticket(candidate)
            ticket_id = current_run.get("ticket_id")
            if isinstance(ticket_id, str) and ticket_id.strip():
                candidate = project_root / "tickets" / f"{ticket_id}.md"
                if candidate.is_file():
                    return load_ticket(candidate)

    ticket_root = (project_root or home) / "tickets"
    all_ticket_files = sorted(ticket_root.glob("TASK-*.md"))
    if not all_ticket_files:
        return None

    mentioned_ticket = extract_ticket_id(message)
    if mentioned_ticket:
        for ticket_file in all_ticket_files:
            if ticket_file.name.startswith(mentioned_ticket):
                return load_ticket(ticket_file)

    explicit_ticket = os.environ.get("CODEXTER_ACTIVE_TICKET", "").strip()
    if explicit_ticket:
        for ticket_file in all_ticket_files:
            if ticket_file.name.startswith(explicit_ticket):
                return load_ticket(ticket_file)

    active_files = [
        ticket_file
        for ticket_file in all_ticket_files
        if load_ticket(ticket_file)["status"] in {"review", "building"}
    ]
    if len(active_files) == 1:
        return load_ticket(active_files[0])

    if len(all_ticket_files) == 1:
        return load_ticket(all_ticket_files[0])

    return None


def extract_impl_result(message: str) -> str | None:
    matches = IMPL_RESULT_PATTERN.findall(message)
    return matches[-1].strip() if matches else None


def extract_grounding_summary(message: str) -> str | None:
    for line in message.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if not stripped.startswith("GROUNDING_SUMMARY:"):
            return None
        summary = stripped.partition(":")[2].strip()
        return summary or None
    return None


def parse_impl_result(line: str) -> dict[str, str]:
    match = PARSED_IMPL_RESULT_PATTERN.match(line.strip())
    if not match:
        raise ValueError("invalid IMPL_RESULT line")
    return {
        "status": match.group("status"),
        "next": match.group("next"),
        "reason": (match.group("reason") or "").strip(),
    }


def summarize_intent_alignment(ticket_id: str, alignment: dict[str, object]) -> str:
    state = str(alignment.get("state", "unknown"))
    reason = str(alignment.get("reason", "")).strip() or "no reason recorded"
    return f"intent-alignment: {ticket_id} -> {state} ({reason})"


def observed_phase_from_result(
    impl_result: str | None,
    *,
    current_phase: str,
) -> tuple[str | None, dict[str, str] | None]:
    if not impl_result:
        return None, None
    try:
        parsed = parse_impl_result(impl_result)
    except ValueError:
        return None, None

    status = parsed["status"]
    if status in {"continue_impl_plan", "plan_ready"}:
        return "planning", parsed
    if status == "docs_complete":
        return "documenting", parsed
    if status in {"continue_impl", "build_complete", "done"}:
        return "building", parsed
    if status == "blocked":
        return current_phase, parsed
    if parsed["next"] in ALLOWED_PHASES:
        return parsed["next"], parsed
    return current_phase, parsed


def classify_intent_alignment(
    *,
    last_user_turn: dict[str, object] | None,
    ticket: dict[str, object],
    message: str,
    impl_result: str | None,
    current_run: dict[str, object] | None,
) -> dict[str, object]:
    ticket_id = str(ticket["ticket_id"])
    if not last_user_turn:
        return {
            "state": "unknown",
            "reason": "no captured current-turn user intent is available",
            "turn_id": "",
            "summary": "",
            "expected_phase": "",
            "observed_phase": "",
            "continuation_message": "",
            "announce": "",
        }

    intent_mode = str(last_user_turn.get("intent_mode") or "unknown")
    requested_outcome = str(last_user_turn.get("requested_outcome") or "unknown")
    summary = str(last_user_turn.get("summary") or "").strip()
    turn_id = str(last_user_turn.get("turn_id") or "").strip()
    explicit_ticket_id = str(last_user_turn.get("explicit_ticket_id") or "").strip()
    hard_constraints = [
        str(item).strip()
        for item in last_user_turn.get("hard_constraints", [])
        if isinstance(item, str) and item.strip()
    ]

    if intent_mode == "unknown" or requested_outcome == "unknown" or not summary:
        return {
            "state": "unknown",
            "reason": "captured turn intent is incomplete or unknown",
            "turn_id": turn_id,
            "summary": summary,
            "expected_phase": "",
            "observed_phase": "",
            "continuation_message": "",
            "announce": "",
        }

    if explicit_ticket_id and explicit_ticket_id != ticket_id:
        return {
            "state": "hard_mismatch",
            "reason": f"captured turn targets {explicit_ticket_id}, but the resolved ticket is {ticket_id}",
            "turn_id": turn_id,
            "summary": summary,
            "expected_phase": "",
            "observed_phase": "",
            "continuation_message": "",
            "announce": f"Stopping {ticket_id}. Current-turn intent targets {explicit_ticket_id}.",
        }

    current_phase = str((current_run or {}).get("phase") or ticket["phase"] or "building")
    observed_phase, parsed_result = observed_phase_from_result(
        impl_result,
        current_phase=current_phase,
    )

    if "no_edits" in hard_constraints and parsed_result is not None:
        return {
            "state": "hard_mismatch",
            "reason": "the captured turn explicitly forbids edits, but the assistant produced an impl worker result",
            "turn_id": turn_id,
            "summary": summary,
            "expected_phase": "",
            "observed_phase": observed_phase or "",
            "continuation_message": "",
            "announce": f"Stopping {ticket_id}. The current turn asked for no edits.",
        }

    if "ticket_local_only" in hard_constraints:
        mentioned_ticket = extract_ticket_id(message)
        if mentioned_ticket and mentioned_ticket != ticket_id:
            return {
                "state": "hard_mismatch",
                "reason": f"the captured turn is ticket-local to {ticket_id}, but the assistant referenced {mentioned_ticket}",
                "turn_id": turn_id,
                "summary": summary,
                "expected_phase": "",
                "observed_phase": observed_phase or "",
                "continuation_message": "",
                "announce": f"Stopping {ticket_id}. The assistant drifted to {mentioned_ticket}.",
            }

    expected_phase = ""
    if intent_mode == "planning":
        expected_phase = "planning"
    elif intent_mode == "building":
        expected_phase = "building"
    elif intent_mode == "documenting":
        expected_phase = "documenting"
    elif intent_mode in {"question", "backlog"} and parsed_result is not None:
        return {
            "state": "hard_mismatch",
            "reason": f"the captured turn is {intent_mode}, but the assistant produced an impl worker result",
            "turn_id": turn_id,
            "summary": summary,
            "expected_phase": intent_mode,
            "observed_phase": observed_phase or "",
            "continuation_message": "",
            "announce": f"Stopping {ticket_id}. The current turn asked for {intent_mode}, not ticket execution.",
        }

    if expected_phase and observed_phase and expected_phase != observed_phase:
        observed_status = parsed_result["status"] if parsed_result is not None else "unknown"
        continuation_message = (
            f"Continue {ticket_id} and satisfy the current-turn intent captured at start of turn: {summary}. "
            f"The assistant ended with `{observed_status}` for `{observed_phase}`, but this turn requested `{expected_phase}` work. "
            f"Stay on the same ticket, produce the requested artifact, update the ticket state, and finish with a `IMPL_RESULT` aligned to `{expected_phase}`."
        )
        return {
            "state": "soft_mismatch",
            "reason": f"captured turn expects {expected_phase}, but the assistant produced {observed_phase}",
            "turn_id": turn_id,
            "summary": summary,
            "expected_phase": expected_phase,
            "observed_phase": observed_phase,
            "continuation_message": continuation_message,
            "announce": f"Re-running {ticket_id}. The last pass drifted from the current-turn intent.",
        }

    return {
        "state": "aligned",
        "reason": "captured turn intent matches the resolved ticket and observed phase",
        "turn_id": turn_id,
        "summary": summary,
        "expected_phase": expected_phase,
        "observed_phase": observed_phase or "",
        "continuation_message": "",
        "announce": "",
    }


def impl_verdict(
    *,
    ticket_id: str,
    current_phase: str,
    decision: str,
    next_phase: str,
    reason: str,
    orchestrator_message: str,
    evidence_ok: bool,
    missing_evidence: list[str] | None = None,
    review_gate_failures: list[str] | None = None,
    blockers: list[str] | None = None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "schema_version": "1.0",
        "ticket_id": ticket_id,
        "current_phase": current_phase,
        "decision": decision,
        "next_phase": next_phase,
        "reason": reason,
        "orchestrator_message": orchestrator_message,
        "evidence_ok": evidence_ok,
    }
    if missing_evidence:
        payload["missing_evidence"] = missing_evidence
    if review_gate_failures:
        payload["review_gate_failures"] = review_gate_failures
    if blockers:
        payload["blockers"] = blockers
    return payload


def review_packet_gate(ticket: dict[str, object]) -> tuple[bool, str, list[str]]:
    if not ticket["review_packet_present"]:
        return False, "review packet is missing", ["review packet missing"]

    packet_errors = list(ticket["review_packet_errors"])
    if packet_errors:
        return False, "review packet is malformed", packet_errors

    packet_missing = list(ticket["review_packet_missing"])
    if packet_missing:
        return False, "review packet is incomplete", [f"missing field: {item}" for item in packet_missing]

    packet = dict(ticket["review_packet"])
    failures: list[str] = []
    reviewed_at = parse_reviewed_at(packet.get("reviewed_at"))
    updated_at = parse_updated_at(ticket.get("updated_at"))

    if packet.get("overall_verdict") != "pass":
        failures.append(f"overall_verdict={packet.get('overall_verdict')}")
    if bool(packet.get("rerun_required")):
        failures.append("rerun_required=true")
    for key in ("evidence_quality", "integration_readiness", "traceability", "freshness"):
        if packet.get(key) != "pass":
            failures.append(f"{key}={packet.get(key)}")

    hard_gate_failures = packet.get("hard_gate_failures", [])
    if isinstance(hard_gate_failures, list):
        for item in hard_gate_failures:
            if isinstance(item, str) and item.strip():
                failures.append(f"hard_gate_failure={item.strip()}")

    blocking_findings = packet.get("blocking_findings", [])
    if isinstance(blocking_findings, list):
        for item in blocking_findings:
            if isinstance(item, str) and item.strip():
                failures.append(f"blocking_finding={item.strip()}")

    if reviewed_at is None:
        failures.append("reviewed_at=invalid")
    elif updated_at is not None and reviewed_at < updated_at:
        failures.append("reviewed_at=stale")

    if failures:
        return False, "review packet gates are not passing", failures

    return True, "", []


def validate_reviewer_gate(review: dict[str, object]) -> tuple[bool, str, list[str]]:
    missing: list[str] = []
    required_scalar_fields = (
        "overall_score",
        "evidence_quality",
        "integration_readiness",
        "traceability",
        "freshness",
        "user_intent_impression",
        "user_intent_mismatch_reason",
        "rerun_required",
        "blocking_findings",
    )
    for field in required_scalar_fields:
        if field not in review:
            missing.append(field)

    if missing:
        return False, "reviewer omitted required completion-gate fields", [f"missing gate field: {item}" for item in missing]

    failures: list[str] = []
    for field in ("evidence_quality", "integration_readiness", "traceability", "freshness", "user_intent_impression"):
        if review.get(field) != "pass":
            failures.append(f"{field}={review.get(field)}")
    mismatch_reason = str(review.get("user_intent_mismatch_reason") or "").strip()
    if review.get("user_intent_impression") == "fail":
        if mismatch_reason:
            failures.append(f"user_intent_mismatch_reason={mismatch_reason}")
        else:
            failures.append("user_intent_mismatch_reason=missing")
    elif mismatch_reason:
        failures.append("user_intent_mismatch_reason=unexpected")
    if bool(review.get("rerun_required")):
        failures.append("rerun_required=true")

    blocking_findings = review.get("blocking_findings", [])
    if isinstance(blocking_findings, list):
        for item in blocking_findings:
            if isinstance(item, str) and item.strip():
                failures.append(f"blocking_finding={item.strip()}")

    if failures:
        return False, "reviewer completion gates are not passing", failures

    return True, "", []


def decide_impl_transition(current_phase: str, ticket: dict[str, object], worker_result: dict[str, str]) -> dict[str, object]:
    ticket_id = str(ticket["ticket_id"])
    blockers = list(ticket["blockers"])
    acceptance_gaps = list(ticket["acceptance_gaps"])
    evidence_gaps = list(ticket["evidence_gaps"])
    status = worker_result["status"]
    next_value = worker_result["next"]
    reason_suffix = worker_result["reason"]

    if blockers:
        return impl_verdict(
            ticket_id=ticket_id,
            current_phase=current_phase,
            decision="block_ticket",
            next_phase="none",
            reason=f"ticket blocker recorded: {blockers[0]}",
            orchestrator_message=f"stop {ticket_id} and surface blocker",
            evidence_ok=False,
            blockers=blockers,
        )

    if status == "blocked":
        reason = reason_suffix or "worker reported blocked"
        return impl_verdict(
            ticket_id=ticket_id,
            current_phase=current_phase,
            decision="block_ticket",
            next_phase="none",
            reason=reason,
            orchestrator_message=f"stop {ticket_id} and surface blocker",
            evidence_ok=False,
        )

    if status in {"continue_impl_plan", "continue_impl"}:
        next_phase = current_phase if next_value in {"planning", "building", "none"} else next_value
        return impl_verdict(
            ticket_id=ticket_id,
            current_phase=current_phase,
            decision="repeat_impl_plan" if current_phase == "planning" else "repeat_impl",
            next_phase=next_phase,
            reason=reason_suffix or "skill requires another bounded pass",
            orchestrator_message=f"rerun {ticket_id} in {next_phase}",
            evidence_ok=False,
        )

    if status == "plan_ready":
        return impl_verdict(
            ticket_id=ticket_id,
            current_phase=current_phase,
            decision="advance_ticket",
            next_phase="building",
            reason=reason_suffix or "plan is present",
            orchestrator_message=f"advance {ticket_id} to building",
            evidence_ok=not evidence_gaps,
        )

    if status == "done":
        packet_ok, packet_reason, packet_failures = review_packet_gate(ticket)
        if not packet_ok:
            return impl_verdict(
                ticket_id=ticket_id,
                current_phase=current_phase,
                decision="repeat_impl",
                next_phase="building",
                reason=packet_reason,
                orchestrator_message=f"rerun {ticket_id} in building and resolve review packet failures",
                evidence_ok=False,
                review_gate_failures=packet_failures,
            )
        missing = acceptance_gaps + evidence_gaps
        if missing:
            return impl_verdict(
                ticket_id=ticket_id,
                current_phase=current_phase,
                decision="repeat_impl",
                next_phase="building",
                reason="ticket marked done but required proof remains incomplete",
                orchestrator_message=f"rerun {ticket_id} in building and resolve missing proof",
                evidence_ok=False,
                missing_evidence=missing,
            )
        return impl_verdict(
            ticket_id=ticket_id,
            current_phase=current_phase,
            decision="complete_ticket",
            next_phase="done",
            reason=reason_suffix or "ticket appears complete",
            orchestrator_message=f"mark {ticket_id} complete",
            evidence_ok=True,
        )

    if status == "build_complete":
        packet_ok, packet_reason, packet_failures = review_packet_gate(ticket)
        if not packet_ok:
            return impl_verdict(
                ticket_id=ticket_id,
                current_phase=current_phase,
                decision="repeat_impl",
                next_phase="building",
                reason=packet_reason,
                orchestrator_message=f"rerun {ticket_id} in building and resolve review packet failures",
                evidence_ok=False,
                review_gate_failures=packet_failures,
            )
        missing = acceptance_gaps + evidence_gaps
        if missing:
            return impl_verdict(
                ticket_id=ticket_id,
                current_phase=current_phase,
                decision="repeat_impl",
                next_phase="building",
                reason=reason_suffix or "evidence is incomplete",
                orchestrator_message=f"rerun {ticket_id} in building with explicit missing evidence coverage",
                evidence_ok=False,
                missing_evidence=missing,
            )
        return impl_verdict(
            ticket_id=ticket_id,
            current_phase=current_phase,
            decision="complete_ticket",
            next_phase="done",
            reason=reason_suffix or "build plus evidence appear complete",
            orchestrator_message=f"mark {ticket_id} complete",
            evidence_ok=True,
        )

    if status == "docs_complete":
        packet_ok, packet_reason, packet_failures = review_packet_gate(ticket)
        if not packet_ok:
            return impl_verdict(
                ticket_id=ticket_id,
                current_phase=current_phase,
                decision="repeat_impl",
                next_phase="building",
                reason=packet_reason,
                orchestrator_message=f"rerun {ticket_id} in building and resolve review packet failures",
                evidence_ok=False,
                review_gate_failures=packet_failures,
            )
        missing = acceptance_gaps + evidence_gaps
        if missing:
            return impl_verdict(
                ticket_id=ticket_id,
                current_phase=current_phase,
                decision="repeat_impl",
                next_phase="building",
                reason="documentation completed but required proof remains incomplete",
                orchestrator_message=f"rerun {ticket_id} in building and resolve missing proof",
                evidence_ok=False,
                missing_evidence=missing,
            )
        return impl_verdict(
            ticket_id=ticket_id,
            current_phase=current_phase,
            decision="complete_ticket",
            next_phase="done",
            reason=reason_suffix or "documentation phase complete",
            orchestrator_message=f"mark {ticket_id} complete",
            evidence_ok=True,
        )

    next_phase = next_value if next_value in ALLOWED_PHASES or next_value in {"done", "none"} else "none"
    if next_phase == "none":
        return impl_verdict(
            ticket_id=ticket_id,
            current_phase=current_phase,
            decision="escalate_to_operator",
            next_phase="none",
            reason="unable to determine safe next phase",
            orchestrator_message=f"inspect {ticket_id} manually",
            evidence_ok=not evidence_gaps,
        )

    return impl_verdict(
        ticket_id=ticket_id,
        current_phase=current_phase,
        decision="advance_ticket",
        next_phase=next_phase,
        reason=reason_suffix or f"worker returned status {status}",
        orchestrator_message=f"advance {ticket_id} to {next_phase}",
        evidence_ok=not evidence_gaps,
    )


def run_impl_judge(ticket: dict[str, object], worker_result: str, current_run: dict[str, object] | None = None) -> dict[str, object] | None:
    current_phase = str((current_run or {}).get("phase") or ticket["phase"] or "building")
    try:
        parsed = parse_impl_result(worker_result)
    except ValueError:
        return None
    return decide_impl_transition(current_phase, ticket, parsed)


def spawn_tmux_followup(
    base: Path,
    ticket: dict[str, object],
    next_phase: str,
    current_run: dict[str, object] | None,
    reason: str,
) -> dict[str, object] | None:
    if current_run is None:
        return None
    session = current_run.get("tmux_session")
    auto_continue = bool(current_run.get("auto_continue"))
    if not auto_continue or not isinstance(session, str) or not session:
        return None
    run_state = current_run.get("run_state")
    cmd = [
        sys.executable,
        str(base / "skills" / "impl" / "scripts" / "tmux_helper.py"),
        "followup",
        "--json",
        "--ticket",
        str(ticket["path"]),
        "--phase",
        next_phase,
        "--auto-continue",
    ]
    if isinstance(session, str) and session:
        cmd.extend(["--tmux-session", session])
    if isinstance(run_state, str) and run_state:
        cmd.extend(["--run-state", run_state])
    if reason:
        cmd.extend(["--reason", reason])
    # Bounded smoke evals can ask the follow-up launcher to stay in dry-run mode
    # so we can validate the tmux handoff without spawning a live Codex worker.
    if os.environ.get("CODEXTER_IMPL_TMUX_DRY_RUN", "").lower() in {"1", "true", "yes", "on"}:
        cmd.append("--dry-run")
    completed = subprocess.run(cmd, text=True, capture_output=True, check=False, cwd=base)
    if completed.returncode != 0:
        return None
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError:
        return None


def build_reason(ticket: dict[str, object]) -> str:
    acceptance_gaps = list(ticket["acceptance_gaps"])
    if acceptance_gaps:
        return (
            "Continue the current ticket and finish the remaining acceptance criteria: "
            + "; ".join(acceptance_gaps[:2])
        )

    evidence_gaps = list(ticket["evidence_gaps"])
    if evidence_gaps:
        return (
            "Continue the current ticket and finish the remaining verification/evidence: "
            + "; ".join(evidence_gaps[:2])
        )

    return "Continue the current ticket and finish the remaining same-ticket work."


def build_missing_impl_result_reason(ticket: dict[str, object], current_run: dict[str, object] | None) -> str:
    ticket_id = str(ticket["ticket_id"])
    current_phase = str(ticket["phase"] or (current_run or {}).get("phase") or "building")
    return (
        f"Continue {ticket_id} in {current_phase}. The last assistant message implied more same-ticket work "
        "but ended without an explicit IMPL_RESULT line. Continue the same ticket, update repo/ticket state, "
        "and finish with a IMPL_RESULT."
    )


def skill_name_for_phase(phase: str) -> str:
    mapping = {
        "planning": "impl-plan",
        "building": "impl",
        "documenting": "docs-closeout",
    }
    return mapping.get(phase, "impl")


def build_live_followup_reason(phase: str, orchestrator_message: str, ticket: dict[str, object]) -> str:
    skill_name = skill_name_for_phase(phase)
    return (
        "Continue the current live Codex lane.\n\n"
        f"Follow-up reason: {orchestrator_message}\n\n"
        f"Run the `{skill_name}` skill on ticket `{ticket['ticket_id']}`.\n"
        "Resolve ticket context from the active ticket state first, then update the ticket itself with any new evidence, blockers, handoff, "
        "next action, and verification before you stop.\n"
    )


def summarize_impl_hook(ticket_id: str, decision: str, next_phase: str, reason: str) -> str:
    if decision in {"repeat_impl_plan", "repeat_impl"}:
        target = next_phase or "same-phase"
        return f"Impl repeat: {ticket_id} -> {target} ({reason})"
    if decision == "advance_ticket":
        target = next_phase or "next-phase"
        return f"Impl advance: {ticket_id} -> {target} ({reason})"
    if decision == "complete_ticket":
        return f"Impl complete: {ticket_id} ({reason})"
    if decision == "block_ticket":
        return f"Impl blocked: {ticket_id} ({reason})"
    return f"Impl review: {ticket_id} ({reason})"


def summarize_legacy_hook(ticket_id: str, decision: str, reason: str) -> str:
    if decision == "continue_same_ticket":
        return f"Hook continue: {ticket_id} ({reason})"
    if decision == "done":
        return f"Hook done: {ticket_id} ({reason})"
    if decision == "blocked":
        return f"Hook blocked: {ticket_id} ({reason})"
    return f"Hook stop: {ticket_id} ({reason})"


def summarize_role_action(ticket_id: str, role: str, action: str, reason: str) -> str:
    return f"{role}: {ticket_id} -> {action} ({reason})"


def role_command(base: Path, output_path: Path, role_config: dict[str, str]) -> list[str]:
    command = [
        "codex",
        "exec",
        "--ephemeral",
        "--skip-git-repo-check",
        "-C",
        str(base),
        "--sandbox",
        "read-only",
        "--disable",
        "codex_hooks",
        "--color",
        "never",
        "-c",
        "notify=[]",
        "--output-schema",
        str(schema_path()),
        "--output-last-message",
        str(output_path),
        "-",
    ]

    model = os.environ.get("CODEXTER_STOP_HOOK_MODEL", "").strip() or role_config.get("model", "")
    if model:
        command[2:2] = ["-m", model]

    reasoning_effort = role_config.get("model_reasoning_effort", "")
    if reasoning_effort:
        command[2:2] = ["-c", f"model_reasoning_effort={json.dumps(reasoning_effort)}"]

    command[2:2] = [
        "-c",
        f"developer_instructions={json.dumps(role_config['developer_instructions'])}",
    ]

    return command


def parse_role_output(output_path: Path) -> dict[str, object] | None:
    try:
        payload = json.loads(output_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None

    if not isinstance(payload, dict):
        return None

    action = payload.get("action")
    reason = payload.get("reason")
    speak = payload.get("speak", "")
    continuation_message = payload.get("continuation_message", "")
    next_ticket_id = payload.get("next_ticket_id", "")
    next_phase = payload.get("next_phase", "")
    overall_score = payload.get("overall_score")
    evidence_quality = payload.get("evidence_quality")
    integration_readiness = payload.get("integration_readiness")
    traceability = payload.get("traceability")
    freshness = payload.get("freshness")
    user_intent_impression = payload.get("user_intent_impression")
    user_intent_mismatch_reason = payload.get("user_intent_mismatch_reason")
    rerun_required = payload.get("rerun_required")
    blocking_findings = payload.get("blocking_findings")

    if not isinstance(action, str) or action not in ROLE_ACTIONS:
        return None
    if not isinstance(reason, str) or not reason.strip():
        return None
    if not isinstance(speak, str):
        return None
    if not isinstance(continuation_message, str):
        return None
    if not isinstance(next_ticket_id, str):
        return None
    if not isinstance(next_phase, str):
        return None
    if overall_score is not None and not isinstance(overall_score, (int, float)):
        return None
    for value in (evidence_quality, integration_readiness, traceability, freshness, user_intent_impression):
        if value is not None and value not in PASS_FAIL_VALUES:
            return None
    if user_intent_mismatch_reason is not None and not isinstance(user_intent_mismatch_reason, str):
        return None
    if rerun_required is not None and not isinstance(rerun_required, bool):
        return None
    if blocking_findings is not None:
        if not isinstance(blocking_findings, list):
            return None
        if any(not isinstance(item, str) or not item.strip() for item in blocking_findings):
            return None

    parsed: dict[str, object] = {
        "action": action,
        "reason": reason.strip(),
        "continuation_message": continuation_message.strip(),
        "speak": speak.strip(),
        "next_ticket_id": next_ticket_id.strip(),
        "next_phase": next_phase.strip(),
    }
    if overall_score is not None:
        parsed["overall_score"] = float(overall_score)
    if evidence_quality is not None:
        parsed["evidence_quality"] = evidence_quality
    if integration_readiness is not None:
        parsed["integration_readiness"] = integration_readiness
    if traceability is not None:
        parsed["traceability"] = traceability
    if freshness is not None:
        parsed["freshness"] = freshness
    if user_intent_impression is not None:
        parsed["user_intent_impression"] = user_intent_impression
    if user_intent_mismatch_reason is not None:
        parsed["user_intent_mismatch_reason"] = user_intent_mismatch_reason.strip()
    if rerun_required is not None:
        parsed["rerun_required"] = rerun_required
    if blocking_findings is not None:
        parsed["blocking_findings"] = [str(item).strip() for item in blocking_findings]
    return parsed


def run_role(base: Path, role_name: str, prompt: str) -> dict[str, object] | None:
    role_config = load_role_config(base, role_name)
    if role_config is None:
        return None

    with tempfile.NamedTemporaryFile(
        prefix="codexter-stop-hook-",
        suffix=".json",
        delete=False,
    ) as temp_output:
        output_path = Path(temp_output.name)

    try:
        try:
            completed = subprocess.run(
                role_command(base, output_path, role_config),
                input=prompt,
                text=True,
                capture_output=True,
                check=False,
                timeout=classifier_timeout_secs(),
            )
        except subprocess.TimeoutExpired:
            return None
        if completed.returncode != 0:
            return None
        return parse_role_output(output_path)
    finally:
        output_path.unlink(missing_ok=True)


def role_prompt(context_label: str, payload: dict[str, object]) -> str:
    return f"{context_label}:\n{json.dumps(payload, ensure_ascii=True, indent=2)}\n"


def reviewer_prompt(
    message: str,
    ticket: dict[str, object],
    current_run: dict[str, object] | None,
    verdict: dict[str, object] | None,
    *,
    mode: str,
) -> str:
    ticket_snapshot = {
        "ticket_id": ticket["ticket_id"],
        "title": ticket["title"],
        "phase": ticket["phase"],
        "status": ticket["status"],
        "next_action": ticket["next_action"],
        "acceptance_gaps": ticket["acceptance_gaps"],
        "evidence_gaps": ticket["evidence_gaps"],
        "blockers": ticket["blockers"],
        "current_run": current_run or {},
        "claim": (current_run or {}).get("claim", {}),
        "last_user_turn": (current_run or {}).get("last_user_turn", {}),
        "last_intent_alignment": (current_run or {}).get("last_intent_alignment", ""),
        "last_intent_alignment_reason": (current_run or {}).get("last_intent_alignment_reason", ""),
        "last_intent_turn_id": (current_run or {}).get("last_intent_turn_id", ""),
        "verdict": verdict or {},
    }
    if mode == "completion_gate":
        ticket_snapshot.update(
            {
                "review_packet": ticket["review_packet"],
                "review_packet_missing": ticket["review_packet_missing"],
                "review_packet_errors": ticket["review_packet_errors"],
            }
        )
    return role_prompt(
        "Context",
        {
            "mode": mode,
            "latest_assistant_response": message,
            "ticket": ticket_snapshot,
        },
    )


def orchestrator_prompt(base: Path, ticket: dict[str, object], verdict: dict[str, object] | None, board: list[dict[str, object]]) -> str:
    payload = {
        "completed_ticket": {
            "ticket_id": ticket["ticket_id"],
            "title": ticket["title"],
            "phase": ticket["phase"],
            "status": ticket["status"],
            "next_action": ticket["next_action"],
            "last_verification": ticket["last_verification"],
        },
        "verdict": verdict or {},
        "board": board,
    }
    return role_prompt("Context", payload)


def continue_hook_response(
    *,
    payload: dict[str, object],
    ticket: dict[str, object],
    continuation_message: str,
    hook_summary: str,
    announce: str,
) -> int:
    if payload.get("stop_hook_active"):
        announce_message("Stopping after one impl-assisted continuation pass")
        return emit_stop_payload(
            continue_value=False,
            stop_reason="Stopping after one impl-assisted continuation pass",
            system_message=f"Stop hook: {hook_summary}. Already continued once.",
        )
    announce_message(announce)
    return emit_stop_payload(
        decision="block",
        reason=continuation_message,
        system_message=f"Stop hook: {hook_summary}",
    )


def run_orchestrator_decision(
    *,
    base: Path,
    home: Path,
    project_root: Path | None,
    payload: dict[str, object],
    current_run: dict[str, object] | None,
    ticket: dict[str, object],
    verdict: dict[str, object] | None,
) -> int:
    role_output = run_role(base, "orchestrator", orchestrator_prompt(base, ticket, verdict, board_snapshot(home, project_root)))
    if role_output is None:
        append_hook_log(
            base,
            {
                "timestamp": now_iso(),
                "mode": "orchestrator",
                "ticket_id": str(ticket["ticket_id"]),
                "outcome": "role_unavailable",
            },
        )
        announce_message("Stop-hook orchestrator unavailable. Stopping safely.")
        return emit_stop_payload(system_message="Stop hook: orchestrator unavailable; stopping safely.")

    action = role_output["action"]
    reason = role_output["reason"]
    speak = role_output["speak"] or reason
    hook_summary = summarize_role_action(str(ticket["ticket_id"]), "orchestrator", action, reason)
    append_hook_log(
        base,
        {
            "timestamp": now_iso(),
            "mode": "orchestrator",
            "ticket_id": str(ticket["ticket_id"]),
            "action": action,
            "reason": reason,
            "next_ticket_id": role_output["next_ticket_id"],
            "next_phase": role_output["next_phase"],
        },
    )
    current_run = publish_hook_status(project_root, current_run, decision=action, summary=hook_summary)

    if action == "stop":
        announce_message(speak)
        return emit_stop_payload(system_message=f"Stop hook: {hook_summary}")

    if action == "block_for_user":
        announce_message(speak)
        return emit_stop_payload(system_message=f"Stop hook: {hook_summary}")

    if action != "next_ticket":
        announce_message("Stop-hook orchestrator returned an unsupported action. Stopping safely.")
        return emit_stop_payload(system_message=f"Stop hook: {hook_summary}")

    next_ticket_id = role_output["next_ticket_id"]
    next_ticket = resolve_ticket_by_id(home, project_root, next_ticket_id)
    if next_ticket is None:
        announce_message(f"Next ticket {next_ticket_id or 'unknown'} could not be resolved.")
        return emit_stop_payload(system_message=f"Stop hook: {hook_summary}")

    next_phase = role_output["next_phase"] if role_output["next_phase"] in {"planning", "building", "documenting"} else "building"
    continuation_message = role_output["continuation_message"] or (
        f"Run the `{skill_name_for_phase(next_phase)}` skill on ticket `{next_ticket_id}` "
        f"and continue from its current state."
    )

    followup = spawn_tmux_followup(
        base,
        next_ticket,
        next_phase,
        current_run,
        continuation_message,
    )
    if followup is not None:
        append_hook_log(
            base,
            {
                "timestamp": now_iso(),
                "mode": "orchestrator",
                "ticket_id": str(ticket["ticket_id"]),
                "event": "spawn_followup",
                "followup": followup,
                "next_ticket_id": next_ticket_id,
                "next_phase": next_phase,
            },
        )
        announce_message(f"queued next ticket {next_ticket_id} in {followup.get('tmux_pane') or followup.get('tmux_window')}")
        return emit_stop_payload(system_message=f"Stop hook: {hook_summary}")

    return continue_hook_response(
        payload=payload,
        ticket=next_ticket,
        continuation_message=continuation_message,
        hook_summary=hook_summary,
        announce=speak,
    )


def main() -> int:
    payload, raw_payload = read_payload()
    home = codexter_home()
    project_root = project_root_from_payload(payload)
    base = runtime_root(home, project_root)
    payload_session_id = payload.get("session_id")
    resolved_session_id = payload_session_id.strip() if isinstance(payload_session_id, str) and payload_session_id.strip() else None
    explicit_run_state = resolve_explicit_run_state_selector(payload) or None
    current_run = (
        load_current_run(
            project_root,
            session_id=resolved_session_id,
            explicit_run_state=explicit_run_state,
        )
        if project_root is not None
        else None
    )
    if (
        project_root is not None
        and current_run is not None
        and resolved_session_id is not None
    ):
        current_run = persist_runtime_update(
            project_root,
            current_run,
            {"session_id": resolved_session_id},
        )
    runtime_claim = (
        load_persisted_runtime_claim(project_root, current_run)
        if project_root is not None
        else None
    )
    if (
        project_root is not None
        and current_run is not None
        and isinstance(runtime_claim, dict)
        and runtime_claim
        and current_run.get("claim") != runtime_claim
    ):
        current_run = persist_runtime_update(
            project_root,
            current_run,
            {"claim": runtime_claim},
        )
    raw_message = payload.get("last_assistant_message") or ""
    message = raw_message if isinstance(raw_message, str) else ""
    impl_result = extract_impl_result(message or raw_payload)

    if not hook_enabled_for_context(project_root, current_run, impl_result):
        return 0

    append_hook_log(
        base,
        {
            "timestamp": now_iso(),
            "mode": "debug",
            "event": "invocation",
            "argv": sys.argv,
            "raw_len": len(raw_payload),
            "raw_preview": raw_payload[:500],
            "payload_keys": sorted(payload.keys()),
            "cwd_from_payload": payload.get("cwd") or payload.get("workdir") or payload.get("current_working_directory"),
            "cwd_runtime": str(Path.cwd()),
        },
    )

    if payload.get("hook_event_name") != "Stop":
        return 0

    if not isinstance(message, str) or not message.strip():
        append_hook_log(
            base,
            {
                "timestamp": now_iso(),
                "mode": "debug",
                "event": "missing_last_assistant_message",
                "payload_keys": sorted(payload.keys()),
            },
        )
        return 0

    grounding_summary = extract_grounding_summary(message or raw_payload)
    if project_root is not None and current_run is not None and grounding_summary:
        current_run = persist_runtime_update(
            project_root,
            current_run,
            {
                "grounding_summary": grounding_summary,
                "last_checkpoint_at": now_iso(),
                "checkpoint_summary": grounding_summary,
                "updated_at": now_iso(),
            },
        )

    ticket = resolve_ticket(home, project_root, message)
    if ticket is None:
        append_hook_log(
            base,
            {
                "timestamp": now_iso(),
                "mode": "unresolved",
                "outcome": "ticket_not_resolved",
                "cwd": str(project_root) if project_root else None,
            },
        )
        return 0

    last_user_turn = (
        load_persisted_last_user_turn(project_root, current_run)
        if project_root is not None
        else None
    )
    impl_mode_enabled = os.environ.get("CODEXTER_IMPL_HOOK", "").lower() in {
        "1",
        "true",
        "yes",
        "on",
    }
    impl_loop_flag = impl_loop_flag_active(current_run, runtime_claim, resolved_session_id)
    impl_runtime_active = (
        impl_mode_enabled
        or impl_loop_flag
        or impl_result is not None
        or has_explicit_ticket_selector()
    )
    live_interactive_lane = (
        resolved_session_id is not None
        and os.environ.get("CODEXTER_IMPL_TMUX_DRY_RUN", "").lower() not in {"1", "true", "yes", "on"}
    )
    if not impl_runtime_active:
        return 0

    impl_loop_allowed = impl_loop_continuation_allowed(
        ticket,
        current_run,
        runtime_claim,
        resolved_session_id,
    )
    alignment = classify_intent_alignment(
        last_user_turn=last_user_turn,
        ticket=ticket,
        message=message,
        impl_result=impl_result,
        current_run=current_run,
    )
    current_run = persist_intent_alignment(project_root, current_run, alignment)
    hook_summary = summarize_intent_alignment(str(ticket["ticket_id"]), alignment)
    append_hook_log(
        base,
        {
            "timestamp": now_iso(),
            "mode": "intent-alignment",
            "ticket_id": str(ticket["ticket_id"]),
            "state": alignment.get("state"),
            "reason": alignment.get("reason"),
            "summary": alignment.get("summary"),
            "turn_id": alignment.get("turn_id"),
            "claim_ticket_id": str((runtime_claim or {}).get("ticket_id") or ""),
            "claim_run_id": str((runtime_claim or {}).get("run_id") or ""),
            "claim_session_id": str((runtime_claim or {}).get("session_id") or ""),
            "expected_phase": alignment.get("expected_phase"),
            "observed_phase": alignment.get("observed_phase"),
        },
    )

    if alignment.get("state") == "hard_mismatch":
        current_run = persist_impl_loop_active(project_root, current_run, False)
        current_run = publish_hook_status(project_root, current_run, decision="block_for_user", summary=hook_summary)
        announce_message(str(alignment.get("announce") or alignment.get("reason") or "Stopping for user review."))
        return emit_stop_payload(
            continue_value=False,
            stop_reason=str(alignment.get("reason") or "").strip() or "intent alignment hard mismatch",
            system_message=f"Stop hook: {hook_summary}",
        )

    if alignment.get("state") == "soft_mismatch":
        if not impl_loop_allowed:
            current_run = persist_impl_loop_active(project_root, current_run, False)
            announce_message("Stopping safely. Same-ticket impl continuation is not active for this session.")
            return emit_stop_payload(
                continue_value=False,
                stop_reason="impl loop continuation requested without an active session claim",
                system_message=f"Stop hook: {hook_summary}",
            )
        current_run = publish_hook_status(project_root, current_run, decision="continue_same_ticket", summary=hook_summary)
        return continue_hook_response(
            payload=payload,
            ticket=ticket,
            continuation_message=str(alignment.get("continuation_message") or "").strip()
            or build_reason(ticket),
            hook_summary=hook_summary,
            announce=str(alignment.get("announce") or alignment.get("reason") or "Continuing the same ticket."),
        )

    if impl_runtime_active and impl_result:
        verdict = run_impl_judge(ticket, impl_result, current_run)
        if verdict is None:
            current_run = persist_impl_loop_active(project_root, current_run, False)
            append_hook_log(
                base,
                {
                    "timestamp": now_iso(),
                    "mode": "impl",
                    "ticket_id": str(ticket["ticket_id"]),
                    "phase": str(ticket["phase"] or ""),
                    "worker_result": impl_result,
                    "outcome": "judge_unavailable",
                },
            )
            announce_message("Impl stop check unavailable. Stopping safely.")
            return emit_stop_payload(system_message="Stop hook: Impl judge unavailable; stopping safely.")
        decision = str(verdict.get("decision", ""))
        next_phase = str(verdict.get("next_phase", ""))
        reason = str(verdict.get("reason", "")).strip() or "impl verdict available"
        orchestrator_message = str(verdict.get("orchestrator_message", "")).strip() or reason
        hook_summary = summarize_impl_hook(str(ticket["ticket_id"]), decision, next_phase, reason)
        if project_root is not None and current_run is not None:
            state_updates: dict[str, object] = {
                "last_worker_result": impl_result,
                "last_judge_verdict": decision,
                "status": (
                    "complete"
                    if decision in {"complete_ticket", "block_ticket", "escalate_to_operator"}
                    else "waiting_for_worker"
                ),
            }
            if next_phase:
                state_updates["next_phase"] = next_phase
            current_run = persist_runtime_update(project_root, current_run, state_updates)
            current_run = publish_hook_status(project_root, current_run, decision=decision, summary=hook_summary)
        append_hook_log(
            base,
            {
                "timestamp": now_iso(),
                "mode": "impl",
                "ticket_id": str(ticket["ticket_id"]),
                "phase": str(ticket["phase"] or ""),
                "worker_result": impl_result,
                "decision": decision,
                "next_phase": next_phase,
                "reason": reason,
            },
        )
        current_phase = str((current_run or {}).get("phase") or ticket["phase"] or "building")
        if decision in {"repeat_impl_plan", "repeat_impl"}:
            if decision == "repeat_impl" and not impl_loop_allowed:
                current_run = persist_impl_loop_active(project_root, current_run, False)
                announce_message("Stopping safely. Repeat impl work is not active for this session.")
                return emit_stop_payload(
                    continue_value=False,
                    stop_reason="repeat_impl requested without an active impl session claim",
                    system_message=f"Stop hook: {hook_summary}",
                )
            current_run = persist_impl_loop_active(
                project_root,
                current_run,
                next_impl_loop_active_for_action(
                    decision,
                    next_phase=next_phase,
                    current_phase=current_phase,
                ),
            )
            target_phase = next_phase if next_phase in {"planning", "building", "documenting"} else str(ticket["phase"] or "building")
            if live_interactive_lane:
                continuation_message = build_live_followup_reason(target_phase, orchestrator_message, ticket)
                return continue_hook_response(
                    payload=payload,
                    ticket=ticket,
                    continuation_message=continuation_message,
                    hook_summary=hook_summary,
                    announce=f"Continuing {ticket['ticket_id']} in the live impl lane.",
                )
            followup = spawn_tmux_followup(
                base,
                ticket,
                target_phase,
                current_run,
                orchestrator_message,
            )
            if followup is not None:
                append_hook_log(
                    base,
                    {
                        "timestamp": now_iso(),
                        "mode": "impl",
                        "ticket_id": str(ticket["ticket_id"]),
                        "event": "spawn_followup",
                        "followup": followup,
                    },
                )
                announce_message(f"spawned next impl pass in {followup.get('tmux_pane') or followup.get('tmux_window')}")
                return emit_stop_payload(system_message=f"Stop hook: {hook_summary}")
            return continue_hook_response(
                payload=payload,
                ticket=ticket,
                continuation_message=orchestrator_message,
                hook_summary=hook_summary,
                announce=orchestrator_message,
            )
        if decision == "block_ticket":
            current_run = persist_impl_loop_active(project_root, current_run, False)
            announce_message(f"Stopping for review. {reason}")
            return emit_stop_payload(system_message=f"Stop hook: {hook_summary}")
        if decision in {"advance_ticket", "complete_ticket"}:
            if decision == "advance_ticket" and current_phase == "planning" and next_phase == "building":
                current_run = persist_impl_loop_active(project_root, current_run, True)
                target_phase = next_phase if next_phase in {"planning", "building", "documenting"} else str(ticket["phase"] or "building")
                if live_interactive_lane:
                    continuation_message = build_live_followup_reason(target_phase, orchestrator_message, ticket)
                    return continue_hook_response(
                        payload=payload,
                        ticket=ticket,
                        continuation_message=continuation_message,
                        hook_summary=hook_summary,
                        announce=f"Advancing {ticket['ticket_id']} inside the live impl lane.",
                    )
                followup = spawn_tmux_followup(
                    base,
                    ticket,
                    target_phase,
                    current_run,
                    orchestrator_message,
                )
                if followup is not None:
                    append_hook_log(
                        base,
                        {
                            "timestamp": now_iso(),
                            "mode": "impl",
                            "ticket_id": str(ticket["ticket_id"]),
                            "event": "spawn_followup",
                            "followup": followup,
                        },
                    )
                    announce_message(f"advanced to {next_phase} in {followup.get('tmux_pane') or followup.get('tmux_window')}")
                    return emit_stop_payload(system_message=f"Stop hook: {hook_summary}")
                return continue_hook_response(
                    payload=payload,
                    ticket=ticket,
                    continuation_message=orchestrator_message,
                    hook_summary=hook_summary,
                    announce=f"Impl phase accepted. Next: {next_phase or 'none'}",
                )

            review = run_role(
                base,
                "reviewer",
                reviewer_prompt(
                    message,
                    ticket,
                    current_run,
                    verdict,
                    mode="completion_gate",
                ),
            )
            if review is None:
                current_run = persist_impl_loop_active(project_root, current_run, False)
                append_hook_log(
                    base,
                    {
                        "timestamp": now_iso(),
                        "mode": "reviewer",
                        "ticket_id": str(ticket["ticket_id"]),
                        "outcome": "role_unavailable",
                    },
                )
                announce_message("Reviewer unavailable. Stopping safely.")
                return emit_stop_payload(system_message=f"Stop hook: {hook_summary}. Reviewer unavailable.")

            review_action = str(review["action"])
            review_reason = str(review["reason"])
            review_summary = summarize_role_action(str(ticket["ticket_id"]), "reviewer", review_action, review_reason)
            append_hook_log(
                base,
                {
                    "timestamp": now_iso(),
                    "mode": "reviewer",
                    "ticket_id": str(ticket["ticket_id"]),
                    "action": review_action,
                    "reason": review_reason,
                    "overall_score": review.get("overall_score"),
                    "evidence_quality": review.get("evidence_quality"),
                    "integration_readiness": review.get("integration_readiness"),
                    "traceability": review.get("traceability"),
                    "freshness": review.get("freshness"),
                    "rerun_required": review.get("rerun_required"),
                    "blocking_findings": review.get("blocking_findings", []),
                },
            )
            current_run = publish_hook_status(project_root, current_run, decision=review_action, summary=review_summary)
            reviewer_gate_ok, reviewer_gate_reason, reviewer_gate_failures = validate_reviewer_gate(review)
            if not reviewer_gate_ok:
                if not impl_loop_allowed:
                    current_run = persist_impl_loop_active(project_root, current_run, False)
                    announce_message("Stopping safely. Reviewer asked for same-ticket impl continuation without an active session claim.")
                    return emit_stop_payload(
                        continue_value=False,
                        stop_reason="reviewer requested same-ticket impl continuation without an active impl loop",
                        system_message=f"Stop hook: {review_summary}",
                    )
                current_run = persist_impl_loop_active(project_root, current_run, True)
                continuation_message = (
                    str(review.get("continuation_message", "")).strip()
                    or f"Continue {ticket['ticket_id']} in building and resolve reviewer gate failures: "
                    + "; ".join(reviewer_gate_failures[:2])
                )
                return continue_hook_response(
                    payload=payload,
                    ticket=ticket,
                    continuation_message=continuation_message,
                    hook_summary=review_summary,
                    announce=reviewer_gate_reason,
                )
            if review_action == "continue_same_ticket":
                if not impl_loop_allowed:
                    current_run = persist_impl_loop_active(project_root, current_run, False)
                    announce_message("Stopping safely. Same-ticket impl continuation is not active for this session.")
                    return emit_stop_payload(
                        continue_value=False,
                        stop_reason="continue_same_ticket requested without an active impl loop",
                        system_message=f"Stop hook: {review_summary}",
                    )
                current_run = persist_impl_loop_active(project_root, current_run, True)
                continuation_message = str(review.get("continuation_message", "")).strip() or build_reason(ticket)
                return continue_hook_response(
                    payload=payload,
                    ticket=ticket,
                    continuation_message=continuation_message,
                    hook_summary=review_summary,
                    announce=str(review.get("speak", "")).strip() or review_reason,
                )
            if review_action == "route_to_orchestrator":
                current_run = persist_impl_loop_active(project_root, current_run, False)
                return run_orchestrator_decision(
                    base=base,
                    home=home,
                    project_root=project_root,
                    payload=payload,
                    current_run=current_run,
                    ticket=ticket,
                    verdict=verdict,
                )
            current_run = persist_impl_loop_active(project_root, current_run, False)
            announce_message(str(review.get("speak", "")).strip() or review_reason)
            return emit_stop_payload(system_message=f"Stop hook: {review_summary}")
        current_run = persist_impl_loop_active(project_root, current_run, False)
        announce_message(f"Stopping for operator review. {reason}")
        return emit_stop_payload(system_message=f"Stop hook: {hook_summary}")

    if impl_runtime_active and not impl_result:
        review = run_role(
            base,
            "reviewer",
            reviewer_prompt(
                message,
                ticket,
                current_run,
                None,
                mode="missing_result_review",
            ),
        )
        if review is None:
            if not impl_loop_allowed:
                current_run = persist_impl_loop_active(project_root, current_run, False)
                announce_message("Stopping safely. Missing IMPL_RESULT and no active impl loop is owned by this session.")
                return emit_stop_payload(
                    continue_value=False,
                    stop_reason="missing IMPL_RESULT without an active impl loop",
                    system_message=f"Stop hook: reviewer unavailable for {ticket['ticket_id']}",
                )
            current_run = persist_impl_loop_active(project_root, current_run, True)
            append_hook_log(
                base,
                {
                    "timestamp": now_iso(),
                    "mode": "reviewer",
                    "ticket_id": str(ticket["ticket_id"]),
                    "outcome": "role_unavailable",
                },
            )
            continuation_message = build_missing_impl_result_reason(ticket, current_run)
            return continue_hook_response(
                payload=payload,
                ticket=ticket,
                continuation_message=continuation_message,
                hook_summary=f"reviewer: {ticket['ticket_id']} -> continue_same_ticket (reviewer unavailable)",
                announce=f"Continuing {ticket['ticket_id']}. Missing IMPL_RESULT in impl mode.",
            )

        proposal_action = review["action"]
        proposal_reason = review["reason"]
        proposal_summary = summarize_role_action(str(ticket["ticket_id"]), "reviewer", proposal_action, proposal_reason)
        append_hook_log(
            base,
            {
                "timestamp": now_iso(),
                "mode": "reviewer",
                "ticket_id": str(ticket["ticket_id"]),
                "action": proposal_action,
                "reason": proposal_reason,
            },
        )
        current_run = publish_hook_status(project_root, current_run, decision=proposal_action, summary=proposal_summary)

        if proposal_action == "continue_same_ticket":
            if not impl_loop_allowed:
                current_run = persist_impl_loop_active(project_root, current_run, False)
                announce_message("Stopping safely. Same-ticket impl continuation is not active for this session.")
                return emit_stop_payload(
                    continue_value=False,
                    stop_reason="missing-result continuation requested without an active impl loop",
                    system_message=f"Stop hook: {proposal_summary}",
                )
            current_run = persist_impl_loop_active(project_root, current_run, True)
            continuation_message = review["continuation_message"] or build_missing_impl_result_reason(ticket, current_run)
            return continue_hook_response(
                payload=payload,
                ticket=ticket,
                continuation_message=continuation_message,
                hook_summary=proposal_summary,
                announce=review["speak"] or f"Continuing {ticket['ticket_id']}. Missing IMPL_RESULT in impl mode.",
            )

        if proposal_action == "route_to_orchestrator":
            current_run = persist_impl_loop_active(project_root, current_run, False)
            return run_orchestrator_decision(
                base=base,
                home=home,
                project_root=project_root,
                payload=payload,
                current_run=current_run,
                ticket=ticket,
                verdict=None,
            )

        current_run = persist_impl_loop_active(project_root, current_run, False)
        announce_message(review["speak"] or proposal_reason)
        return emit_stop_payload(system_message=f"Stop hook: {proposal_summary}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
