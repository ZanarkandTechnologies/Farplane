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
- MEM-0056
"""

import json
import os
import re
import secrets
import subprocess
import sys
import tempfile
import tomllib
from datetime import datetime, timezone
from pathlib import Path

from notify import announce_message
from runtime_telemetry import emit_hook_telemetry
from user_turn import (
    append_conversation_assistant_response,
    build_runtime_claim,
    explicit_run_state_selector as resolve_explicit_run_state_selector,
    iter_active_ticket_files,
    load_last_user_turn as load_persisted_last_user_turn,
    load_current_run as load_selected_runtime_state,
    load_runtime_claim as load_persisted_runtime_claim,
    persist_runtime_update as persist_selected_runtime_update,
    project_root_from_payload as resolve_project_root_from_payload,
    recent_conversation_windows,
    mark_skill_opportunity_review_launched,
    resolve_ticket_path_by_id,
    should_review_skill_opportunities,
    skill_opportunity_application_dir,
    ticket_artifact_root,
    ticket_id_from_path,
    tickets_dir as user_turn_tickets_dir,
)


TICKET_ID_PATTERN = re.compile(r"\bTASK-\d{4}\b")
SECTION_PATTERN = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
CHECKBOX_PATTERN = re.compile(r"^- \[( |x)\]\s+(.*)$")
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
ARTIFACT_PATH_PATTERN = re.compile(
    r"(?P<path>(?:^|[\s(])(?:/?(?:[^)\s`]*?/)?tickets/(?:artifacts/[^)\s`]+|TASK-\d{4}/artifacts/[^)\s`]+|archive/TASK-\d{4}/artifacts/[^)\s`]+)))"
)
IMPL_RESULT_PATTERN = re.compile(r"^IMPL_RESULT:\s+status=.*$", re.MULTILINE)
PARSED_IMPL_RESULT_PATTERN = re.compile(
    r"^IMPL_RESULT:\s+status=(?P<status>[A-Za-z0-9_-]+)\s+next=(?P<next>[A-Za-z0-9_-]+)(?:\s+reason=(?P<reason>.*))?$"
)
COMPLETION_PASSWORD_PATTERN = re.compile(
    r"^COMPLETION_PASSWORD:\s*(?P<password>CR-[0-9A-Z]+)\s*$",
    re.MULTILINE,
)
ALLOWED_PHASES = {"planning", "building", "documenting"}
ROLE_ACTIONS = {
    "continue_same_ticket",
    "route_to_orchestrator",
    "block_for_user",
    "next_ticket",
    "stop",
}
PASS_FAIL_VALUES = {"pass", "fail"}
INTENT_ALIGNMENT_STATES = {"aligned", "soft_mismatch", "hard_mismatch", "unknown"}
IMPL_LOOPABLE_PHASES = {"building"}
COMPLETION_REVIEW_VERDICTS = {"pass", "revise", "block"}


def env_enabled() -> bool:
    return os.environ.get("CODEXTER_IMPL_HOOK", "").lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


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
    if skill_name and skill_name not in {"impl", "qa", "demo"}:
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
    if action == "advance_execution_phase":
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


def emit_stop_passthrough(*, system_message: str | None = None) -> int:
    return emit_stop_payload(
        continue_value=True,
        system_message=system_message,
    )


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


def ticket_repo_root(ticket_path: Path) -> Path:
    current = ticket_path.resolve().parent
    for candidate in (current, *current.parents):
        if candidate.name == "tickets":
            return candidate.parent
    return ticket_path.resolve().parents[1]


def parse_updated_at(raw: object) -> datetime | None:
    if not isinstance(raw, str) or not raw.strip():
        return None
    try:
        parsed = datetime.fromisoformat(raw.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed.astimezone().replace(second=0, microsecond=0)


def parse_timestamp(raw: object) -> datetime | None:
    if not isinstance(raw, str) or not raw.strip():
        return None
    try:
        parsed = datetime.fromisoformat(raw.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed.astimezone()


def normalize_artifact_reference(ticket_path: Path, raw: str) -> Path | None:
    cleaned = raw.strip().strip("<>").strip()
    if not cleaned:
        return None
    if cleaned.startswith("/"):
        path_text = cleaned
    else:
        path_text = str((ticket_repo_root(ticket_path) / cleaned).resolve())
    if re.match(r"^/.+:\d+$", path_text):
        path_text = path_text.rsplit(":", 1)[0]
    candidate = Path(path_text)
    return candidate


def extract_artifact_references(ticket_path: Path, lines: list[str]) -> list[str]:
    refs: list[str] = []
    text = "\n".join(lines)
    for match in MARKDOWN_LINK_PATTERN.finditer(text):
        target = match.group(1).strip()
        if "tickets/" in target and "/artifacts/" in target:
            refs.append(target)
    for match in ARTIFACT_PATH_PATTERN.finditer(text):
        target = match.group("path").strip()
        if target.startswith("("):
            target = target[1:]
        if "tickets/" in target and "/artifacts/" in target:
            refs.append(target)
    normalized: list[str] = []
    seen: set[str] = set()
    for raw in refs:
        candidate = normalize_artifact_reference(ticket_path, raw)
        if candidate is None:
            continue
        resolved = str(candidate.resolve())
        if resolved in seen:
            continue
        seen.add(resolved)
        normalized.append(resolved)
    return normalized


def artifact_root_for_ticket(ticket_path: Path, ticket_id: str) -> Path:
    return ticket_artifact_root(ticket_repo_root(ticket_path), ticket_path, ticket_id)


def collect_artifact_files(root_path: Path) -> list[str]:
    if not root_path.exists():
        return []
    files: list[str] = []
    for path in sorted(root_path.rglob("*")):
        if path.is_file():
            files.append(str(path.resolve()))
    return files


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
    fallback_ticket_id = ticket_id_from_path(ticket_path) or extract_ticket_id(ticket_path.name) or ticket_path.stem
    ticket_id = extract_ticket_id(text) or fallback_ticket_id
    artifact_root = artifact_root_for_ticket(ticket_path, ticket_id).resolve()
    linked_artifacts = extract_artifact_references(ticket_path, sections.get("Evidence", []))
    artifact_files = collect_artifact_files(artifact_root)
    missing_artifacts = [path for path in linked_artifacts if not Path(path).exists()]
    return {
        "path": ticket_path,
        "text": text,
        "ticket_id": ticket_id,
        "title": str(frontmatter.get("title", "")).strip(),
        "phase": str(frontmatter.get("phase", "")).strip(),
        "status": str(frontmatter.get("status", "")).strip(),
        "ready": bool(frontmatter.get("ready", False)),
        "approval_required": bool(frontmatter.get("approval_required", False)),
        "requires_qa": bool(frontmatter.get("requires_qa", True)),
        "requires_demo": bool(frontmatter.get("requires_demo", False)),
        "depends_on": list(frontmatter.get("depends_on", [])) if isinstance(frontmatter.get("depends_on", []), list) else [],
        "frontmatter_blocked_by": list(frontmatter.get("blocked_by", [])) if isinstance(frontmatter.get("blocked_by", []), list) else [],
        "updated_at": str(frontmatter.get("updated_at", "")).strip(),
        "next_action": str(frontmatter.get("next_action", "")).strip(),
        "last_verification": str(frontmatter.get("last_verification", "")).strip(),
        "acceptance_gaps": unchecked_items(sections.get("Acceptance Criteria", [])),
        "evidence_gaps": unchecked_items(sections.get("Evidence", [])),
        "blockers": blocked_items(sections.get("Blockers", [])),
        "artifact_root": artifact_root,
        "linked_artifacts": linked_artifacts,
        "missing_artifacts": missing_artifacts,
        "artifact_files": artifact_files,
    }


def ticket_root(home: Path, project_root: Path | None) -> Path:
    return user_turn_tickets_dir(project_root or home)


def resolve_ticket_by_id(home: Path, project_root: Path | None, ticket_id: str) -> dict[str, object] | None:
    if not ticket_id.strip():
        return None
    ticket_file = resolve_ticket_path_by_id(project_root or home, ticket_id)
    return load_ticket(ticket_file) if ticket_file is not None else None


def board_snapshot(home: Path, project_root: Path | None) -> list[dict[str, object]]:
    snapshot: list[dict[str, object]] = []
    for ticket_file in iter_active_ticket_files(project_root or home):
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
                candidate = resolve_ticket_path_by_id(project_root, ticket_id.strip())
                if candidate is not None and candidate.is_file():
                    return load_ticket(candidate)

    root = project_root or home
    all_ticket_files = iter_active_ticket_files(root)
    if not all_ticket_files:
        return None

    mentioned_ticket = extract_ticket_id(message)
    if mentioned_ticket:
        for ticket_file in all_ticket_files:
            if ticket_file.name.startswith(mentioned_ticket):
                return load_ticket(ticket_file)

    explicit_ticket = os.environ.get("CODEXTER_ACTIVE_TICKET", "").strip()
    if explicit_ticket:
        candidate = resolve_ticket_path_by_id(root, explicit_ticket)
        if candidate is not None and candidate in all_ticket_files:
            return load_ticket(candidate)

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
    if status in {"continue_impl", "build_complete", "done", "qa_complete", "demo_complete"}:
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
    requested_execution_phase = str(last_user_turn.get("requested_execution_phase") or "").strip()
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
    observed_execution_phase = current_execution_phase(current_run) if observed_phase == "building" else ""
    if parsed_result is not None:
        if parsed_result["status"] == "qa_complete":
            observed_execution_phase = "qa"
        elif parsed_result["status"] == "demo_complete":
            observed_execution_phase = "demo"

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

    if (
        expected_phase == "building"
        and requested_execution_phase in {"impl", "qa", "demo"}
        and observed_execution_phase
        and requested_execution_phase != observed_execution_phase
    ):
        observed_status = parsed_result["status"] if parsed_result is not None else "unknown"
        continuation_message = (
            f"Continue {ticket_id} and satisfy the current-turn execution phase captured at start of turn: {summary}. "
            f"The assistant ended with `{observed_status}` for `{observed_execution_phase}`, but this turn requested `{requested_execution_phase}`. "
            f"Stay on the same ticket, run the `{requested_execution_phase}` phase, update artifacts, and finish with a matching `IMPL_RESULT`."
        )
        return {
            "state": "soft_mismatch",
            "reason": f"captured turn expects execution phase {requested_execution_phase}, but the assistant produced {observed_execution_phase}",
            "turn_id": turn_id,
            "summary": summary,
            "expected_phase": expected_phase,
            "observed_phase": observed_phase,
            "continuation_message": continuation_message,
            "announce": f"Re-running {ticket_id}. The last pass drifted from the requested {requested_execution_phase} phase.",
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
    next_execution_phase: str | None = None,
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
    if next_execution_phase:
        payload["next_execution_phase"] = next_execution_phase
    if missing_evidence:
        payload["missing_evidence"] = missing_evidence
    if review_gate_failures:
        payload["review_gate_failures"] = review_gate_failures
    if blockers:
        payload["blockers"] = blockers
    return payload


def evidence_artifact_gate(ticket: dict[str, object]) -> tuple[bool, str, list[str]]:
    failures: list[str] = []
    updated_at = parse_updated_at(ticket.get("updated_at"))
    artifact_root = ticket.get("artifact_root")
    linked_artifacts = list(ticket.get("linked_artifacts") or [])
    missing_artifacts = list(ticket.get("missing_artifacts") or [])
    artifact_files = list(ticket.get("artifact_files") or [])

    if not linked_artifacts:
        failures.append("linked_artifacts=missing")
    for item in missing_artifacts:
        failures.append(f"missing_artifact={item}")
    if not artifact_files:
        failures.append("artifact_root=empty")

    artifact_root_str = str(artifact_root) if isinstance(artifact_root, Path) else ""
    if linked_artifacts and artifact_root_str and not any(path.startswith(artifact_root_str) for path in linked_artifacts):
        failures.append("linked_artifacts=outside_ticket_root")

    if updated_at is not None:
        existing_artifacts = [Path(path) for path in linked_artifacts if Path(path).exists()]
        if existing_artifacts:
            newest_artifact = max(
                datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).astimezone()
                for path in existing_artifacts
            )
            if newest_artifact.replace(second=0, microsecond=0) < updated_at:
                failures.append("linked_artifacts=stale")

    if failures:
        return False, "evidence artifact gates are not passing", failures

    return True, "", []


def current_execution_phase(current_run: dict[str, object] | None) -> str:
    phase = str((current_run or {}).get("execution_phase") or "").strip().lower()
    return phase if phase in {"impl", "qa", "demo"} else "impl"


def execution_requirements(ticket: dict[str, object], current_run: dict[str, object] | None) -> dict[str, object]:
    runtime_requirements = (current_run or {}).get("phase_requirements")
    if isinstance(runtime_requirements, dict) and runtime_requirements:
        return dict(runtime_requirements)
    artifact_root = ticket.get("artifact_root")
    artifact_root_str = str(artifact_root) if isinstance(artifact_root, Path) else ""
    requirements: dict[str, object] = {
        "impl": {
            "completion_statuses": ["build_complete", "done"],
            "artifact_root": artifact_root_str,
        }
    }
    if bool((current_run or {}).get("requires_qa", ticket.get("requires_qa", True))):
        requirements["qa"] = {
            "artifact_root": str(Path(artifact_root_str) / "qa") if artifact_root_str else "",
            "result_glob": "**/result.json",
            "required_verdict": "pass",
        }
    if bool((current_run or {}).get("requires_demo", ticket.get("requires_demo", False))):
        requirements["demo"] = {
            "artifact_root": str(Path(artifact_root_str) / "demo") if artifact_root_str else "",
            "result_glob": "**/result.json",
            "required_verdict": "pass",
        }
    return requirements


def linked_artifacts_for_phase(ticket: dict[str, object], phase_name: str) -> list[str]:
    marker = f"/{phase_name}/"
    return [path for path in list(ticket.get("linked_artifacts") or []) if marker in path]


def latest_phase_result(ticket: dict[str, object], current_run: dict[str, object] | None, phase_name: str) -> tuple[dict[str, object] | None, list[str]]:
    requirements = execution_requirements(ticket, current_run)
    requirement = requirements.get(phase_name)
    if not isinstance(requirement, dict):
        return None, [f"phase_requirement={phase_name}:missing"]
    artifact_root = str(requirement.get("artifact_root") or "").strip()
    result_glob = str(requirement.get("result_glob") or "**/result.json").strip() or "**/result.json"
    if not artifact_root:
        return None, [f"{phase_name}_artifact_root=missing"]
    root_path = Path(artifact_root)
    if not root_path.exists():
        return None, [f"{phase_name}_artifact_root=missing"]
    matches = sorted(
        [path for path in root_path.glob(result_glob) if path.is_file()],
        key=lambda item: item.stat().st_mtime,
        reverse=True,
    )
    if not matches:
        return None, [f"{phase_name}_result=missing"]
    result_path = matches[0]
    try:
        payload = json.loads(result_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None, [f"{phase_name}_result=invalid_json"]
    if not isinstance(payload, dict):
        return None, [f"{phase_name}_result=invalid_shape"]
    payload = dict(payload)
    payload["_path"] = str(result_path.resolve())
    return payload, []


def phase_result_gate(ticket: dict[str, object], current_run: dict[str, object] | None, phase_name: str) -> tuple[bool, str, list[str], dict[str, object] | None]:
    payload, failures = latest_phase_result(ticket, current_run, phase_name)
    if payload is None:
        return False, f"{phase_name} result gates are not passing", failures, None

    requirements = execution_requirements(ticket, current_run)
    requirement = requirements.get(phase_name) if isinstance(requirements.get(phase_name), dict) else {}
    required_verdict = str((requirement or {}).get("required_verdict") or "pass").strip()
    result_path = str(payload.get("_path") or "").strip()
    verdict = str(payload.get("verdict") or "").strip()
    artifacts = payload.get("artifacts")
    phase = str(payload.get("phase") or "").strip()
    ticket_id = str(payload.get("ticket_id") or "").strip()
    updated_at = parse_updated_at(ticket.get("updated_at"))
    failures = []

    if phase and phase != phase_name:
        failures.append(f"{phase_name}_result_phase={phase}")
    if ticket_id and ticket_id != str(ticket["ticket_id"]):
        failures.append(f"{phase_name}_result_ticket_id={ticket_id}")
    if verdict != required_verdict:
        failures.append(f"{phase_name}_verdict={verdict or 'missing'}")
    if not isinstance(artifacts, list) or not artifacts:
        failures.append(f"{phase_name}_artifacts=missing")
    else:
        for item in artifacts:
            if not isinstance(item, str) or not item.strip():
                failures.append(f"{phase_name}_artifacts=invalid")
                break
    linked_artifacts = linked_artifacts_for_phase(ticket, phase_name)
    if not linked_artifacts:
        failures.append(f"{phase_name}_linked_artifacts=missing")
    elif result_path and result_path not in linked_artifacts and not any(result_path.startswith(str(Path(path).resolve()).rsplit("/", 1)[0]) for path in linked_artifacts):
        failures.append(f"{phase_name}_result=unlinked")
    if updated_at is not None and result_path:
        result_time = datetime.fromtimestamp(Path(result_path).stat().st_mtime, timezone.utc).astimezone().replace(second=0, microsecond=0)
        if result_time < updated_at:
            failures.append(f"{phase_name}_result=stale")

    if failures:
        return False, f"{phase_name} result gates are not passing", failures, payload

    return True, "", [], payload


def completion_review_receipt_paths(paths: list[str]) -> list[str]:
    return [
        path
        for path in paths
        if "/review/" in path and path.endswith(".json") and "completion-receipt" in Path(path).name
    ]


def generate_completion_review_nonce() -> str:
    return "CR-" + secrets.token_hex(3).upper()


def extract_completion_password(message: str) -> str:
    if not message.strip():
        return ""
    match = COMPLETION_PASSWORD_PATTERN.search(message)
    if match is None:
        return ""
    return str(match.group("password") or "").strip()


def build_completion_review_request(
    ticket: dict[str, object],
    current_run: dict[str, object] | None,
    last_user_turn: dict[str, object] | None,
) -> dict[str, object]:
    linked_artifacts = [str(item) for item in list(ticket.get("linked_artifacts") or []) if isinstance(item, str)]
    return {
        "ticket_id": str(ticket["ticket_id"]),
        "nonce": generate_completion_review_nonce(),
        "requested_at": now_iso(),
        "artifact_root": str(ticket.get("artifact_root") or ""),
        "execution_phase": current_execution_phase(current_run),
        "last_user_turn_summary": str((last_user_turn or {}).get("summary") or "").strip(),
        "required_artifacts": linked_artifacts[:12],
        "reason": "run visible completion review",
    }


def build_completion_review_request_message(
    ticket: dict[str, object],
    request: dict[str, object],
    *,
    failure_reason: str = "",
    password_failure_reason: str = "",
) -> str:
    ticket_id = str(ticket["ticket_id"])
    nonce = str(request.get("nonce") or "").strip()
    artifacts = [
        f"- `{item}`"
        for item in request.get("required_artifacts", [])
        if isinstance(item, str) and item.strip()
    ]
    artifact_block = "\n".join(artifacts) if artifacts else "- linked ticket-scoped artifacts already on the ticket"
    failure_parts = [item.strip() for item in (password_failure_reason, failure_reason) if item.strip()]
    if failure_parts:
        reason_prefix = "Stop hook validated the phase and artifact gates, but " + " and ".join(failure_parts) + ".\n\n"
    else:
        reason_prefix = "Stop hook validated the phase and artifact gates, but final completion still needs visible reviewer signoff.\n\n"
    return (
        f"Continue {ticket_id} in building.\n\n"
        + reason_prefix
        + "Call the completion reviewer now. Use the `review` skill against the active ticket, hand it this one-time password, then write "
        f"`tickets/{ticket_id}/artifacts/review/<timestamp>-completion-receipt.json` with this exact nonce: `{nonce}`.\n\n"
        "Required receipt fields:\n"
        "- `receipt_type`: `completion_review`\n"
        f"- `ticket_id`: `{ticket_id}`\n"
        f"- `nonce`: `{nonce}`\n"
        "- `reviewed_at`: ISO timestamp\n"
        "- `reviewer_mode`: `visible_review_lane`\n"
        "- `reviewed_artifacts`: array of artifact paths you judged\n"
        "- `verdict`: `pass|revise|block`\n"
        "- `satisfies_user_query`: boolean\n"
        "- `user_query_reason`: concrete reason\n"
        "- `obvious_next_step`: concrete next step or empty string\n"
        "- `review_artifact`: path to the main linked review artifact\n\n"
        "Artifacts this receipt should cover:\n"
        f"{artifact_block}\n\n"
        "Link the receipt from the ticket `Evidence` section and finish your next final response with both:\n"
        f"- `COMPLETION_PASSWORD: {nonce}`\n"
        "- `IMPL_RESULT: status=done next=building reason=completion review receipt written`"
    )


def build_completion_password_retry_message(
    ticket: dict[str, object],
    nonce: str,
    *,
    password_failure_reason: str,
) -> str:
    ticket_id = str(ticket["ticket_id"])
    return (
        f"Continue {ticket_id} in building.\n\n"
        f"Stop hook validated the linked completion review receipt, but {password_failure_reason.strip()}.\n\n"
        "Do not rerun completion review. Keep the existing linked receipt and resend your next final response with both:\n"
        f"- `COMPLETION_PASSWORD: {nonce}`\n"
        "- `IMPL_RESULT: status=done next=building reason=completion review receipt written`"
    )


def load_completion_review_receipt(path: Path) -> dict[str, object] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict):
        return None
    receipt = dict(payload)
    receipt["_path"] = str(path.resolve())
    return receipt


def completion_review_password_gate(
    pending_nonce: str,
    message: str,
) -> tuple[bool, str, list[str], str]:
    observed = extract_completion_password(message)
    if not observed:
        return False, "completion review password is missing from the final response", ["completion_review_password=missing"], ""
    if observed != pending_nonce:
        return (
            False,
            "completion review password does not match the requested nonce",
            [f"completion_review_password=mismatch:{observed}"],
            observed,
        )
    return True, "", [], observed


def completion_review_receipt_gate(
    ticket: dict[str, object],
    current_run: dict[str, object] | None,
) -> tuple[bool, str, list[str], dict[str, object] | None]:
    failures: list[str] = []
    pending_nonce = str((current_run or {}).get("completion_review_nonce") or "").strip()
    if not pending_nonce:
        return False, "completion review receipt gates are not passing", ["completion_review_nonce=missing"], None

    linked_artifacts = [str(item) for item in list(ticket.get("linked_artifacts") or []) if isinstance(item, str)]
    requested_at = parse_timestamp((current_run or {}).get("completion_review_requested_at"))
    required_artifacts = [
        str(item)
        for item in list((current_run or {}).get("completion_review_required_artifacts") or [])
        if isinstance(item, str) and item.strip()
    ]
    if not required_artifacts:
        required_artifacts = [
            item
            for item in linked_artifacts
            if "/review/" not in item or "completion-receipt" not in Path(item).name
        ]
    linked_paths = completion_review_receipt_paths(linked_artifacts)
    artifact_paths = completion_review_receipt_paths([str(item) for item in list(ticket.get("artifact_files") or []) if isinstance(item, str)])

    if not linked_paths:
        if artifact_paths:
            failures.append(f"completion_review_receipt=unlinked:{artifact_paths[-1]}")
        else:
            failures.append("completion_review_receipt=missing")
        return False, "completion review receipt gates are not passing", failures, None

    candidates: list[dict[str, object]] = []
    for raw_path in linked_paths:
        receipt = load_completion_review_receipt(Path(raw_path))
        if receipt is None:
            failures.append(f"completion_review_receipt=invalid_json:{raw_path}")
            continue
        candidates.append(receipt)

    matching = [item for item in candidates if str(item.get("nonce") or "").strip() == pending_nonce]
    if not matching:
        if candidates:
            observed = str(candidates[-1].get("nonce") or "").strip() or "missing"
            failures.append(f"completion_review_nonce=mismatch:{observed}")
        else:
            failures.append("completion_review_receipt=missing")
        return False, "completion review receipt gates are not passing", failures, None

    receipt = max(
        matching,
        key=lambda item: Path(str(item["_path"])).stat().st_mtime,
    )
    receipt_path = Path(str(receipt["_path"]))
    artifact_root = ticket.get("artifact_root")
    artifact_root_path = artifact_root if isinstance(artifact_root, Path) else None
    ticket_id = str(receipt.get("ticket_id") or "").strip()
    verdict = str(receipt.get("verdict") or "").strip()
    receipt_type = str(receipt.get("receipt_type") or "").strip()
    reviewer_mode = str(receipt.get("reviewer_mode") or "").strip()
    review_artifact = str(receipt.get("review_artifact") or "").strip()
    user_query_reason = str(receipt.get("user_query_reason") or "").strip()
    obvious_next_step = str(receipt.get("obvious_next_step") or "").strip()
    reviewed_artifacts = receipt.get("reviewed_artifacts")
    satisfies_user_query = receipt.get("satisfies_user_query")
    receipt_time = parse_timestamp(receipt.get("reviewed_at"))
    if receipt_time is None:
        receipt_time = datetime.fromtimestamp(receipt_path.stat().st_mtime, timezone.utc).astimezone()
    ticket_updated_at = parse_updated_at(ticket.get("updated_at"))

    if receipt_type != "completion_review":
        failures.append(f"completion_review_receipt_type={receipt_type or 'missing'}")
    if ticket_id != str(ticket["ticket_id"]):
        failures.append(f"completion_review_ticket_id={ticket_id or 'missing'}")
    if reviewer_mode != "visible_review_lane":
        failures.append(f"completion_review_reviewer_mode={reviewer_mode or 'missing'}")
    if verdict not in COMPLETION_REVIEW_VERDICTS:
        failures.append(f"completion_review_verdict={verdict or 'missing'}")
    elif verdict != "pass":
        failures.append(f"completion_review_verdict={verdict}")
    if not isinstance(reviewed_artifacts, list) or not reviewed_artifacts:
        failures.append("completion_review_reviewed_artifacts=missing")
    elif any(not isinstance(item, str) or not item.strip() for item in reviewed_artifacts):
        failures.append("completion_review_reviewed_artifacts=invalid")
    else:
        reviewed_artifact_paths = {
            str(Path(str(item)).expanduser().resolve())
            for item in reviewed_artifacts
            if isinstance(item, str) and item.strip()
        }
        for item in reviewed_artifacts:
            candidate = Path(str(item)).expanduser()
            if not candidate.exists():
                failures.append(f"completion_review_reviewed_artifact=missing:{candidate}")
                continue
            resolved_candidate = candidate.resolve()
            if artifact_root_path is not None and not str(resolved_candidate).startswith(str(artifact_root_path.resolve())):
                failures.append(f"completion_review_reviewed_artifact=outside_ticket_root:{resolved_candidate}")
        for item in required_artifacts:
            candidate = Path(item).expanduser()
            resolved_candidate = str(candidate.resolve()) if candidate.exists() else str(candidate)
            if resolved_candidate not in reviewed_artifact_paths:
                failures.append(f"completion_review_required_artifact=unreviewed:{resolved_candidate}")
    if not isinstance(satisfies_user_query, bool):
        failures.append("completion_review_satisfies_user_query=missing")
    elif not satisfies_user_query:
        failures.append("completion_review_satisfies_user_query=false")
    if not review_artifact:
        failures.append("completion_review_review_artifact=missing")
    else:
        review_artifact_path = Path(review_artifact).expanduser()
        if not review_artifact_path.exists():
            failures.append(f"completion_review_review_artifact=missing:{review_artifact_path}")
        else:
            resolved_review_artifact = str(review_artifact_path.resolve())
            if artifact_root_path is not None and not resolved_review_artifact.startswith(str(artifact_root_path.resolve())):
                failures.append(f"completion_review_review_artifact=outside_ticket_root:{resolved_review_artifact}")
            if resolved_review_artifact not in linked_artifacts:
                failures.append(f"completion_review_review_artifact=unlinked:{resolved_review_artifact}")
    if requested_at is not None and receipt_time.replace(second=0, microsecond=0) < requested_at.replace(second=0, microsecond=0):
        failures.append("completion_review_receipt=stale")
    if ticket_updated_at is not None and receipt_time.replace(second=0, microsecond=0) < ticket_updated_at:
        failures.append("completion_review_receipt=stale")
    if not satisfies_user_query and user_query_reason:
        failures.append(f"completion_review_user_query_reason={user_query_reason}")
    if verdict in {"revise", "block"} and obvious_next_step:
        failures.append(f"completion_review_next_step={obvious_next_step}")

    if failures:
        return False, "completion review receipt gates are not passing", failures, receipt

    return True, "", [], receipt


def validate_reviewer_gate(review: dict[str, object]) -> tuple[bool, str, list[str]]:
    missing: list[str] = []
    required_scalar_fields = (
        "overall_score",
        "evidence_quality",
        "integration_readiness",
        "traceability",
        "freshness",
        "qa_quality",
        "demo_quality",
        "stakeholder_readiness",
        "stakeholder_readiness_reason",
        "best_demo_artifact",
        "storyline_gaps",
        "user_intent_impression",
        "user_intent_mismatch_reason",
        "obvious_next_step_exists",
        "next_step_safe",
        "obvious_next_step",
        "user_would_expect_more",
        "rerun_required",
        "blocking_findings",
    )
    for field in required_scalar_fields:
        if field not in review:
            missing.append(field)

    if missing:
        return False, "completion-reviewer omitted required completion-gate fields", [f"missing gate field: {item}" for item in missing]

    failures: list[str] = []
    for field in (
        "evidence_quality",
        "integration_readiness",
        "traceability",
        "freshness",
        "qa_quality",
        "demo_quality",
        "stakeholder_readiness",
        "user_intent_impression",
    ):
        if review.get(field) != "pass":
            failures.append(f"{field}={review.get(field)}")
    mismatch_reason = str(review.get("user_intent_mismatch_reason") or "").strip()
    stakeholder_reason = str(review.get("stakeholder_readiness_reason") or "").strip()
    best_demo_artifact = str(review.get("best_demo_artifact") or "").strip()
    if review.get("user_intent_impression") == "fail":
        if mismatch_reason:
            failures.append(f"user_intent_mismatch_reason={mismatch_reason}")
        else:
            failures.append("user_intent_mismatch_reason=missing")
    elif mismatch_reason:
        failures.append("user_intent_mismatch_reason=unexpected")

    if review.get("stakeholder_readiness") == "fail":
        if stakeholder_reason:
            failures.append(f"stakeholder_readiness_reason={stakeholder_reason}")
        else:
            failures.append("stakeholder_readiness_reason=missing")
    elif stakeholder_reason:
        failures.append("stakeholder_readiness_reason=unexpected")

    if review.get("demo_quality") == "pass":
        if not best_demo_artifact:
            failures.append("best_demo_artifact=missing")
    elif best_demo_artifact:
        failures.append("best_demo_artifact=unexpected")

    storyline_gaps = review.get("storyline_gaps", [])
    if isinstance(storyline_gaps, list):
        if review.get("stakeholder_readiness") == "pass" and storyline_gaps:
            failures.append("storyline_gaps=unexpected")
        for item in storyline_gaps:
            if isinstance(item, str) and item.strip():
                failures.append(f"storyline_gap={item.strip()}")

    obvious_next_step_exists = bool(review.get("obvious_next_step_exists"))
    next_step_safe = bool(review.get("next_step_safe"))
    obvious_next_step = str(review.get("obvious_next_step") or "").strip()
    user_would_expect_more = bool(review.get("user_would_expect_more"))

    if obvious_next_step_exists:
        if obvious_next_step:
            failures.append(f"obvious_next_step={obvious_next_step}")
        else:
            failures.append("obvious_next_step=missing")
    elif obvious_next_step:
        failures.append("obvious_next_step=unexpected")

    if user_would_expect_more:
        failures.append("user_would_expect_more=true")

    if next_step_safe and not obvious_next_step_exists:
        failures.append("next_step_safe=unexpected")

    if bool(review.get("rerun_required")):
        failures.append("rerun_required=true")

    blocking_findings = review.get("blocking_findings", [])
    if isinstance(blocking_findings, list):
        for item in blocking_findings:
            if isinstance(item, str) and item.strip():
                failures.append(f"blocking_finding={item.strip()}")

    if failures:
        return False, "completion-reviewer completion gates are not passing", failures

    return True, "", []


def decide_impl_transition(current_phase: str, ticket: dict[str, object], worker_result: dict[str, str], current_run: dict[str, object] | None = None) -> dict[str, object]:
    ticket_id = str(ticket["ticket_id"])
    blockers = list(ticket["blockers"])
    acceptance_gaps = list(ticket["acceptance_gaps"])
    evidence_gaps = list(ticket["evidence_gaps"])
    status = worker_result["status"]
    next_value = worker_result["next"]
    reason_suffix = worker_result["reason"]
    execution_phase = current_execution_phase(current_run)
    phase_requirements = execution_requirements(ticket, current_run)
    qa_required = "qa" in phase_requirements
    demo_required = "demo" in phase_requirements

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

    if current_phase == "building" and execution_phase == "impl" and status in {"build_complete", "done", "docs_complete"}:
        if qa_required:
            return impl_verdict(
                ticket_id=ticket_id,
                current_phase=current_phase,
                decision="advance_execution_phase",
                next_phase="building",
                next_execution_phase="qa",
                reason=reason_suffix or "implementation is ready for QA",
                orchestrator_message=f"continue {ticket_id} in qa and produce ticket-scoped proof artifacts",
                evidence_ok=False,
            )
        if demo_required:
            return impl_verdict(
                ticket_id=ticket_id,
                current_phase=current_phase,
                decision="advance_execution_phase",
                next_phase="building",
                next_execution_phase="demo",
                reason=reason_suffix or "implementation is ready for demo",
                orchestrator_message=f"continue {ticket_id} in demo and produce demo artifacts",
                evidence_ok=False,
            )

    if current_phase == "building" and execution_phase == "qa" and status in {"qa_complete", "build_complete", "done"}:
        qa_ok, qa_reason, qa_failures, _ = phase_result_gate(ticket, current_run, "qa")
        if not qa_ok:
            return impl_verdict(
                ticket_id=ticket_id,
                current_phase=current_phase,
                decision="repeat_impl",
                next_phase="building",
                next_execution_phase="qa",
                reason=qa_reason,
                orchestrator_message=f"continue {ticket_id} in qa and resolve qa artifact failures",
                evidence_ok=False,
                review_gate_failures=qa_failures,
            )
        if demo_required:
            return impl_verdict(
                ticket_id=ticket_id,
                current_phase=current_phase,
                decision="advance_execution_phase",
                next_phase="building",
                next_execution_phase="demo",
                reason=reason_suffix or "qa passed and demo is required",
                orchestrator_message=f"continue {ticket_id} in demo and produce demo artifacts",
                evidence_ok=False,
            )
        return impl_verdict(
            ticket_id=ticket_id,
            current_phase=current_phase,
            decision="complete_ticket",
            next_phase="done",
            reason=reason_suffix or "qa passed",
            orchestrator_message=f"mark {ticket_id} complete",
            evidence_ok=True,
        )

    if current_phase == "building" and execution_phase == "demo" and status in {"demo_complete", "build_complete", "done"}:
        demo_ok, demo_reason, demo_failures, _ = phase_result_gate(ticket, current_run, "demo")
        if not demo_ok:
            return impl_verdict(
                ticket_id=ticket_id,
                current_phase=current_phase,
                decision="repeat_impl",
                next_phase="building",
                next_execution_phase="demo",
                reason=demo_reason,
                orchestrator_message=f"continue {ticket_id} in demo and resolve demo artifact failures",
                evidence_ok=False,
                review_gate_failures=demo_failures,
            )
        return impl_verdict(
            ticket_id=ticket_id,
            current_phase=current_phase,
            decision="complete_ticket",
            next_phase="done",
            reason=reason_suffix or "demo passed",
            orchestrator_message=f"mark {ticket_id} complete",
            evidence_ok=True,
        )

    if status == "done":
        artifact_ok, artifact_reason, artifact_failures = evidence_artifact_gate(ticket)
        if not artifact_ok:
            return impl_verdict(
                ticket_id=ticket_id,
                current_phase=current_phase,
                decision="repeat_impl",
                next_phase="building",
                reason=artifact_reason,
                orchestrator_message=f"rerun {ticket_id} in building and resolve evidence artifact failures",
                evidence_ok=False,
                review_gate_failures=artifact_failures,
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
        artifact_ok, artifact_reason, artifact_failures = evidence_artifact_gate(ticket)
        if not artifact_ok:
            return impl_verdict(
                ticket_id=ticket_id,
                current_phase=current_phase,
                decision="repeat_impl",
                next_phase="building",
                reason=artifact_reason,
                orchestrator_message=f"rerun {ticket_id} in building and resolve evidence artifact failures",
                evidence_ok=False,
                review_gate_failures=artifact_failures,
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
        artifact_ok, artifact_reason, artifact_failures = evidence_artifact_gate(ticket)
        if not artifact_ok:
            return impl_verdict(
                ticket_id=ticket_id,
                current_phase=current_phase,
                decision="repeat_impl",
                next_phase="building",
                reason=artifact_reason,
                orchestrator_message=f"rerun {ticket_id} in building and resolve evidence artifact failures",
                evidence_ok=False,
                review_gate_failures=artifact_failures,
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
    return decide_impl_transition(current_phase, ticket, parsed, current_run)


def spawn_tmux_followup(
    base: Path,
    ticket: dict[str, object],
    next_phase: str,
    current_run: dict[str, object] | None,
    reason: str,
    execution_phase: str = "",
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
    if execution_phase:
        cmd.extend(["--execution-phase", execution_phase])
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


def skill_name_for_phase(phase: str, execution_phase: str = "") -> str:
    if phase == "building" and execution_phase in {"qa", "demo"}:
        return execution_phase
    mapping = {
        "planning": "impl-plan",
        "building": "impl",
        "documenting": "close-ticket",
    }
    return mapping.get(phase, "impl")


def build_live_followup_reason(phase: str, orchestrator_message: str, ticket: dict[str, object], execution_phase: str = "") -> str:
    skill_name = skill_name_for_phase(phase, execution_phase)
    delegation_note = ""
    if phase == "building" and execution_phase == "qa":
        delegation_note = (
            "This live lane stays in coordinator mode for QA. Spawn the `qa-tester` subagent or lane to own browser "
            "driving, artifact capture, and ticket-scoped QA proof, and do not use `agent-browser` directly from this "
            "coordinating lane unless delegation is impossible.\n"
        )
    return (
        "Continue the current live Codex lane.\n\n"
        f"Follow-up reason: {orchestrator_message}\n\n"
        f"Run the `{skill_name}` skill on ticket `{ticket['ticket_id']}`.\n"
        f"{delegation_note}"
        "Resolve ticket context from the active ticket state first, then update the ticket itself with any new evidence, blockers, handoff, "
        "next action, and verification before you stop.\n"
    )


def summarize_impl_hook(ticket_id: str, decision: str, next_phase: str, reason: str) -> str:
    if decision in {"repeat_impl_plan", "repeat_impl"}:
        target = next_phase or "same-phase"
        return f"Impl repeat: {ticket_id} -> {target} ({reason})"
    if decision == "advance_execution_phase":
        target = next_phase or "building"
        return f"Impl advance execution: {ticket_id} -> {target} ({reason})"
    if decision == "advance_ticket":
        target = next_phase or "next-phase"
        return f"Impl advance: {ticket_id} -> {target} ({reason})"
    if decision == "complete_ticket":
        return f"Impl complete: {ticket_id} ({reason})"
    if decision == "block_ticket":
        return f"Impl blocked: {ticket_id} ({reason})"
    return f"Impl review: {ticket_id} ({reason})"


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


def skill_opportunity_review_enabled() -> bool:
    disabled_values = {"0", "false", "no", "off", "disabled"}
    apply_value = os.environ.get("CODEXTER_SKILL_OPPORTUNITY_APPLY", "").strip().lower()
    if apply_value in disabled_values:
        return False
    return True


def skill_opportunity_review_dry_run() -> bool:
    return os.environ.get("CODEXTER_SKILL_OPPORTUNITY_APPLY_DRY_RUN", "").lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def skill_opportunity_review_interval() -> int:
    raw = os.environ.get("CODEXTER_SKILL_OPPORTUNITY_APPLY_INTERVAL", "").strip()
    if not raw:
        return 10
    try:
        value = int(raw)
    except ValueError:
        return 10
    return value if value > 0 else 10


def skill_opportunity_recent_window_limit() -> int:
    raw = os.environ.get("CODEXTER_SKILL_OPPORTUNITY_RECENT_SESSIONS", "").strip()
    if not raw:
        return 5
    try:
        value = int(raw)
    except ValueError:
        return 5
    return value if value > 0 else 5


def safe_path_token(raw: str) -> str:
    token = re.sub(r"[^A-Za-z0-9._-]+", "-", raw.strip())
    return token.strip(".-") or "session"


def skill_opportunity_review_root(project_root: Path) -> Path:
    return skill_opportunity_application_dir(project_root)


def skill_opportunity_hooklet_result(
    *,
    status: str,
    reason: str,
    project_root: Path | None,
    session_id: str | None,
    trigger: dict[str, object] | None = None,
    review_run_path: str = "",
    pid: str = "",
) -> dict[str, object]:
    readiness = "ready" if bool((trigger or {}).get("due")) else "not_ready"
    artifacts = {
        "review_run_path": review_run_path,
        "pid": pid,
    }
    return {
        "name": "skill-opportunity-review",
        "status": status,
        "readiness": readiness,
        "reason": reason,
        "project_root": str(project_root) if project_root is not None else "",
        "session_id": session_id or "",
        "trigger": trigger or {},
        "artifacts": artifacts,
        "review_run_path": review_run_path,
        "pid": pid,
    }


def log_hooklet_result(base: Path, hooklet: dict[str, object]) -> None:
    append_hook_log(
        base,
        {
            "timestamp": now_iso(),
            "mode": "hooklet",
            "hooklet": hooklet.get("name", ""),
            "status": hooklet.get("status", ""),
            "readiness": hooklet.get("readiness", ""),
            "reason": hooklet.get("reason", ""),
            "project_root": hooklet.get("project_root", ""),
            "session_id": hooklet.get("session_id", ""),
            "trigger": hooklet.get("trigger", {}),
            "artifacts": hooklet.get("artifacts", {}),
        },
    )


def relative_paths(root: Path, pattern: str) -> list[str]:
    return sorted(
        str(path.relative_to(root))
        for path in root.glob(pattern)
        if path.is_file()
    )


def skill_opportunity_review_input(
    *,
    base: Path,
    project_root: Path,
    session_id: str,
    window: dict[str, object],
    trigger: dict[str, object],
    payload: dict[str, object],
) -> dict[str, object]:
    skill_paths = relative_paths(base, "skills/*/SKILL.md")
    recent_ticket_paths = relative_paths(base, "tickets/TASK-*/ticket.md")[-12:]
    source_project_skill_paths = [] if project_root == base else relative_paths(project_root, "skills/*/SKILL.md")
    source_project_ticket_paths = [] if project_root == base else relative_paths(project_root, "tickets/TASK-*/ticket.md")[-12:]
    dedupe_refs = {
        "skills": skill_paths,
        "feature_registry": "docs/features/registry.jsonl",
        "memory": "docs/MEMORY.md",
        "troubles": "docs/TROUBLES.md",
        "recent_tickets": recent_ticket_paths,
        "source_project_skills": source_project_skill_paths,
        "source_project_recent_tickets": source_project_ticket_paths,
        "notion_context": "/Users/kenjipcx/.codex/skills/notion-context/SKILL.md",
    }
    workflow_refs = {
        "source_to_feature": "skills/harness-scout/SKILL.md",
        "feature_options": "skills/advise/SKILL.md",
        "placement": "skills/harness-advisor/SKILL.md",
        "placement_todos": "skills/harness-advisor/todos.md",
        "policy_index": "docs/policies/README.md",
        "harness_doctrine": "docs/specs/harness-engineering-doctrine.md",
    }
    recent_windows = recent_conversation_windows(
        project_root,
        current_session_id=session_id,
        limit=skill_opportunity_recent_window_limit(),
    )
    if not any(str(item.get("session_id") or "") == session_id for item in recent_windows):
        recent_windows.insert(0, dict(window))
    raw_cwd = payload.get("cwd") or payload.get("workdir") or payload.get("current_working_directory")
    invocation_cwd = str(raw_cwd).strip() if isinstance(raw_cwd, str) and raw_cwd.strip() else ""
    status_context_cache = project_root / ".harness" / "state" / "notion-context" / "latest-status-context.md"
    workspace_context = {
        "current_project_name": project_root.name,
        "current_project_root": str(project_root),
        "hook_invocation_cwd": invocation_cwd,
        "codexter_home": str(base),
        "status_context_cache": str(status_context_cache),
        "status_context_cache_exists": status_context_cache.is_file(),
        "task_scope_default": "harness_self_improvement",
        "routing_hint": (
            "Use the current project as evidence for tagging and prioritization, "
            "but create tasks for reusable Codexter harness improvements unless "
            "the issue is purely project-local."
        ),
    }
    return {
        "schema_version": 1,
        "review_type": "skill_opportunity",
        "project_root": str(project_root),
        "session_id": session_id,
        "created_at": now_iso(),
        "trigger": trigger,
        "window": window,
        "recent_windows": recent_windows,
        "dedupe_refs": dedupe_refs,
        "workflow_refs": workflow_refs,
        "workspace_context": workspace_context,
        "notion_task_target": {
            "data_source_url": os.environ.get(
                "CODEXTER_SKILL_OPPORTUNITY_NOTION_TASKS_DATA_SOURCE",
                "collection://43a439fd-74c5-4b43-9afb-950f047e5d4f",
            ),
            "tag": os.environ.get("CODEXTER_SKILL_OPPORTUNITY_NOTION_TAG", "agent self improvement"),
            "default_status": os.environ.get("CODEXTER_SKILL_OPPORTUNITY_NOTION_STATUS", "Review"),
        },
        "payload_context": {
            "hook_event_name": payload.get("hook_event_name"),
            "cwd": invocation_cwd,
        },
        "instructions": [
            "Return JSON only.",
            "Create Notion approval tasks when the signal is clearly useful and specific enough.",
            "Do not update or create skill files directly.",
            "Do not write local files except the final JSON report emitted by the Codex CLI.",
            "Look for skill create/update opportunities, formula mentions, cheatsheets, recipes, and one unconventional speedup, but turn them into Notion task proposals.",
            "Use workflow_refs as the required local routing model: harness-scout for source-to-feature extraction, advise for comparing feature directions, and harness-advisor for placement.",
            "Use workspace_context to understand which project produced the signal and to tag/relate the Notion task when safe; default every clear signal to a reusable Codexter harness improvement.",
            "Review the current window first, then use recent_windows for cross-session complaints and repeated pain.",
            "Dedupe against existing skills, feature registry, memory, troubles, and recent tickets.",
        ],
    }


def skill_opportunity_apply_command(base: Path, report_path: Path, role_config: dict[str, str]) -> list[str]:
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
        "--output-last-message",
        str(report_path),
        "-",
    ]
    model = os.environ.get("CODEXTER_SKILL_OPPORTUNITY_APPLY_MODEL", "").strip() or role_config.get("model", "")
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


def maybe_launch_skill_opportunity_review(
    *,
    base: Path,
    project_root: Path | None,
    session_id: str | None,
    window: dict[str, object],
    payload: dict[str, object],
) -> dict[str, object]:
    if project_root is None:
        return skill_opportunity_hooklet_result(
            status="skipped",
            reason="missing project root",
            project_root=project_root,
            session_id=session_id,
        )
    if not session_id:
        return skill_opportunity_hooklet_result(
            status="skipped",
            reason="missing session id",
            project_root=project_root,
            session_id=session_id,
        )

    trigger = should_review_skill_opportunities(
        window,
        cadence=skill_opportunity_review_interval(),
    )
    if not bool(trigger.get("due")):
        return skill_opportunity_hooklet_result(
            status="skipped",
            reason=str(trigger.get("reason") or "not due"),
            project_root=project_root,
            session_id=session_id,
            trigger=trigger,
        )
    if not skill_opportunity_review_enabled():
        return skill_opportunity_hooklet_result(
            status="skipped",
            reason="skill opportunity review disabled",
            project_root=project_root,
            session_id=session_id,
            trigger=trigger,
        )

    timestamp = now_iso().replace(":", "").replace("+", "p")
    run_dir = skill_opportunity_review_root(project_root) / f"{timestamp}-{safe_path_token(session_id)}"
    run_dir.mkdir(parents=True, exist_ok=True)
    input_path = run_dir / "input.json"
    report_path = run_dir / "report.json"
    stdout_path = run_dir / "stdout.log"
    stderr_path = run_dir / "stderr.log"
    input_payload = skill_opportunity_review_input(
        base=base,
        project_root=project_root,
        session_id=session_id,
        window=window,
        trigger=trigger,
        payload=payload,
    )
    input_path.write_text(json.dumps(input_payload, indent=2) + "\n", encoding="utf-8")

    relative_run_path = str(run_dir.relative_to(project_root))
    if skill_opportunity_review_dry_run():
        report_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "reviewed_at": now_iso(),
                    "status": "dry_run",
                    "source_window": str(input_path.relative_to(project_root)),
                    "notion_tasks": [],
                    "decisions": [],
                    "formula_mentions": [],
                    "unconventional_speedup": {
                        "title": "dry run",
                        "rationale": "Notion task creation launch was intentionally not executed",
                    },
                    "dedupe_refs": input_payload["dedupe_refs"],
                    "risks": [],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        mark_skill_opportunity_review_launched(
            project_root,
            session_id,
            review_run_path=relative_run_path,
            current_window=window,
        )
        return skill_opportunity_hooklet_result(
            status="launched",
            reason="dry run",
            project_root=project_root,
            session_id=session_id,
            trigger=trigger,
            review_run_path=relative_run_path,
            pid="dry-run",
        )

    role_config = load_role_config(base, "skill-opportunity-applier")
    if role_config is None:
        return skill_opportunity_hooklet_result(
            status="failed",
            reason="missing skill-opportunity-applier role config",
            project_root=project_root,
            session_id=session_id,
            trigger=trigger,
            review_run_path=relative_run_path,
        )

    prompt = "Context:\n" + json.dumps(input_payload, ensure_ascii=True, indent=2) + "\n"
    prompt_path = run_dir / "prompt.json"
    prompt_path.write_text(prompt, encoding="utf-8")
    stdin_handle = prompt_path.open("r", encoding="utf-8")
    stdout_handle = stdout_path.open("w", encoding="utf-8")
    stderr_handle = stderr_path.open("w", encoding="utf-8")
    try:
        proc = subprocess.Popen(
            skill_opportunity_apply_command(base, report_path, role_config),
            stdin=stdin_handle,
            stdout=stdout_handle,
            stderr=stderr_handle,
            cwd=base,
            start_new_session=True,
        )
    except OSError as exc:
        stdin_handle.close()
        stdout_handle.close()
        stderr_handle.close()
        return skill_opportunity_hooklet_result(
            status="failed",
            reason=str(exc),
            project_root=project_root,
            session_id=session_id,
            trigger=trigger,
            review_run_path=relative_run_path,
        )
    stdin_handle.close()
    stdout_handle.close()
    stderr_handle.close()

    mark_skill_opportunity_review_launched(
        project_root,
        session_id,
        review_run_path=relative_run_path,
        current_window=window,
    )
    return skill_opportunity_hooklet_result(
        status="launched",
        reason="started detached skill opportunity proposer",
        project_root=project_root,
        session_id=session_id,
        trigger=trigger,
        review_run_path=relative_run_path,
        pid=str(proc.pid),
    )


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
    qa_quality = payload.get("qa_quality")
    demo_quality = payload.get("demo_quality")
    stakeholder_readiness = payload.get("stakeholder_readiness")
    stakeholder_readiness_reason = payload.get("stakeholder_readiness_reason")
    best_demo_artifact = payload.get("best_demo_artifact")
    storyline_gaps = payload.get("storyline_gaps")
    obvious_next_step_exists = payload.get("obvious_next_step_exists")
    next_step_safe = payload.get("next_step_safe")
    obvious_next_step = payload.get("obvious_next_step")
    user_would_expect_more = payload.get("user_would_expect_more")
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
    for value in (
        evidence_quality,
        integration_readiness,
        traceability,
        freshness,
        qa_quality,
        demo_quality,
        stakeholder_readiness,
        user_intent_impression,
    ):
        if value is not None and value not in PASS_FAIL_VALUES:
            return None
    if user_intent_mismatch_reason is not None and not isinstance(user_intent_mismatch_reason, str):
        return None
    if stakeholder_readiness_reason is not None and not isinstance(stakeholder_readiness_reason, str):
        return None
    if best_demo_artifact is not None and not isinstance(best_demo_artifact, str):
        return None
    for value in (obvious_next_step_exists, next_step_safe, user_would_expect_more):
        if value is not None and not isinstance(value, bool):
            return None
    if obvious_next_step is not None and not isinstance(obvious_next_step, str):
        return None
    if rerun_required is not None and not isinstance(rerun_required, bool):
        return None
    if blocking_findings is not None:
        if not isinstance(blocking_findings, list):
            return None
        if any(not isinstance(item, str) or not item.strip() for item in blocking_findings):
            return None
    if storyline_gaps is not None:
        if not isinstance(storyline_gaps, list):
            return None
        if any(not isinstance(item, str) or not item.strip() for item in storyline_gaps):
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
    if qa_quality is not None:
        parsed["qa_quality"] = qa_quality
    if demo_quality is not None:
        parsed["demo_quality"] = demo_quality
    if stakeholder_readiness is not None:
        parsed["stakeholder_readiness"] = stakeholder_readiness
    if stakeholder_readiness_reason is not None:
        parsed["stakeholder_readiness_reason"] = stakeholder_readiness_reason.strip()
    if best_demo_artifact is not None:
        parsed["best_demo_artifact"] = best_demo_artifact.strip()
    if storyline_gaps is not None:
        parsed["storyline_gaps"] = [str(item).strip() for item in storyline_gaps]
    if user_intent_impression is not None:
        parsed["user_intent_impression"] = user_intent_impression
    if user_intent_mismatch_reason is not None:
        parsed["user_intent_mismatch_reason"] = user_intent_mismatch_reason.strip()
    if obvious_next_step_exists is not None:
        parsed["obvious_next_step_exists"] = obvious_next_step_exists
    if next_step_safe is not None:
        parsed["next_step_safe"] = next_step_safe
    if obvious_next_step is not None:
        parsed["obvious_next_step"] = obvious_next_step.strip()
    if user_would_expect_more is not None:
        parsed["user_would_expect_more"] = user_would_expect_more
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
        "requires_qa": ticket["requires_qa"],
        "requires_demo": ticket["requires_demo"],
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
                "completion_claim_is_candidate_only": True,
                "execution_phase": current_execution_phase(current_run),
                "artifact_root": str(ticket["artifact_root"]),
                "linked_artifacts": ticket["linked_artifacts"],
                "missing_artifacts": ticket["missing_artifacts"],
                "artifact_files": ticket["artifact_files"][:20],
                "artifact_file_count": len(ticket["artifact_files"]),
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
    ticket: dict[str, object] | None,
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
    hook_event_name = str(payload.get("hook_event_name") or "").strip()
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
        if hook_event_name == "Stop":
            return emit_stop_passthrough(
                system_message="Stop hook: no Codexter runtime context; allowing stop."
            )
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

    if hook_event_name != "Stop":
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
        return emit_stop_passthrough(
            system_message="Stop hook: missing assistant message; allowing stop."
        )

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

    last_user_turn = (
        load_persisted_last_user_turn(project_root, current_run)
        if project_root is not None
        else None
    )
    if project_root is not None and resolved_session_id and isinstance(last_user_turn, dict) and last_user_turn:
        conversation_window = append_conversation_assistant_response(
            project_root,
            resolved_session_id,
            message,
            captured_at=now_iso(),
            source="stop_hook",
        )
        launch_result = maybe_launch_skill_opportunity_review(
            base=base,
            project_root=project_root,
            session_id=resolved_session_id,
            window=conversation_window,
            payload=payload,
        )
        log_hooklet_result(base, launch_result)
        if launch_result.get("status") != "skipped":
            append_hook_log(
                base,
                {
                    "timestamp": now_iso(),
                    "mode": "skill-opportunity-review",
                    "status": launch_result.get("status"),
                    "reason": launch_result.get("reason"),
                    "review_run_path": launch_result.get("review_run_path"),
                    "pid": launch_result.get("pid"),
                },
            )
    emit_hook_telemetry(
        event_type="stop_hook",
        hook_event_name="Stop",
        payload=payload,
        project_root=project_root,
        current_run=current_run,
        runtime_claim=runtime_claim,
        extra={
            "source": "stop_hook.py",
            "message_length": len(message),
            "last_user_turn_id": str((last_user_turn or {}).get("turn_id") or "").strip(),
            "intent_mode": str((last_user_turn or {}).get("intent_mode") or "").strip(),
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
        return emit_stop_passthrough(
            system_message="Stop hook: no active ticket resolved; allowing stop."
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
        return emit_stop_passthrough(
            system_message="Stop hook: impl runtime inactive; allowing stop."
        )

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
        next_execution_phase = str(verdict.get("next_execution_phase", "")).strip()
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
            if next_execution_phase:
                state_updates["execution_phase"] = next_execution_phase
                state_updates["skill_name"] = next_execution_phase
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
                "next_execution_phase": next_execution_phase,
                "reason": reason,
            },
        )
        current_phase = str((current_run or {}).get("phase") or ticket["phase"] or "building")
        execution_phase = str((current_run or {}).get("execution_phase") or current_execution_phase(current_run))
        if decision in {"repeat_impl_plan", "repeat_impl", "advance_execution_phase"}:
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
            target_execution_phase = next_execution_phase or execution_phase
            # Prefer a dedicated QA lane over reusing the live coordinator lane. See MEM-0069.
            if target_execution_phase == "qa":
                followup = spawn_tmux_followup(
                    base,
                    ticket,
                    target_phase,
                    current_run,
                    orchestrator_message,
                    target_execution_phase,
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
                    announce_message(
                        f"spawned delegated QA follow-up in {followup.get('tmux_pane') or followup.get('tmux_window')}"
                    )
                    return emit_stop_payload(system_message=f"Stop hook: {hook_summary}")
            if live_interactive_lane:
                continuation_message = build_live_followup_reason(target_phase, orchestrator_message, ticket, target_execution_phase)
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
                target_execution_phase,
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
                target_execution_phase = next_execution_phase or current_execution_phase(current_run)
                if live_interactive_lane:
                    continuation_message = build_live_followup_reason(target_phase, orchestrator_message, ticket, target_execution_phase)
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
                    target_execution_phase,
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

            if project_root is None or current_run is None:
                append_hook_log(
                    base,
                    {
                        "timestamp": now_iso(),
                        "mode": "completion-review",
                        "ticket_id": str(ticket["ticket_id"]),
                        "outcome": "runtime_state_missing",
                    },
                )
                current_run = persist_impl_loop_active(project_root, current_run, False)
                announce_message("Completion review requires active runtime state. Stopping safely.")
                return emit_stop_payload(system_message=f"Stop hook: {hook_summary}. Completion review runtime state missing.")

            pending_nonce = str(current_run.get("completion_review_nonce") or "").strip()
            if not pending_nonce:
                request = build_completion_review_request(ticket, current_run, last_user_turn)
                request_summary = f"completion-review-request: {ticket['ticket_id']} -> {request['nonce']}"
                current_run = persist_impl_loop_active(project_root, current_run, True)
                current_run = persist_runtime_update(
                    project_root,
                    current_run,
                    {
                        "completion_review_requested": True,
                        "completion_review_nonce": str(request["nonce"]),
                        "completion_review_requested_at": str(request["requested_at"]),
                        "completion_review_required_artifacts": list(request.get("required_artifacts") or []),
                        "completion_review_receipt_path": "",
                        "completion_review_receipt_status": "requested",
                        "status": "waiting_for_worker",
                    },
                )
                current_run = publish_hook_status(
                    project_root,
                    current_run,
                    decision="continue_same_ticket",
                    summary=request_summary,
                )
                append_hook_log(
                    base,
                    {
                        "timestamp": now_iso(),
                        "mode": "completion-review",
                        "ticket_id": str(ticket["ticket_id"]),
                        "action": "request_receipt",
                        "nonce": request["nonce"],
                        "required_artifacts": request["required_artifacts"],
                    },
                )
                return continue_hook_response(
                    payload=payload,
                    ticket=ticket,
                    continuation_message=build_completion_review_request_message(ticket, request),
                    hook_summary=request_summary,
                    announce=f"Visible completion review required for {ticket['ticket_id']}.",
                )

            password_ok, password_reason, password_failures, observed_password = completion_review_password_gate(
                pending_nonce,
                message,
            )
            if not password_ok:
                password_receipt_ok, _, _, password_receipt = completion_review_receipt_gate(ticket, current_run)
                password_receipt_path = str((password_receipt or {}).get("_path") or "").strip()
                if not impl_loop_allowed:
                    current_run = persist_impl_loop_active(project_root, current_run, False)
                    announce_message("Stopping safely. Same-ticket impl continuation is not active for this session.")
                    return emit_stop_payload(
                        continue_value=False,
                        stop_reason="completion review password requested without an active impl loop",
                        system_message=f"Stop hook: completion-review-password: {ticket['ticket_id']} -> continue_same_ticket ({password_reason})",
                    )
                current_run = persist_impl_loop_active(project_root, current_run, True)
                current_run = persist_runtime_update(
                    project_root,
                    current_run,
                    {
                        "completion_review_requested": True,
                        "completion_review_required_artifacts": list(
                            (current_run or {}).get("completion_review_required_artifacts") or []
                        ),
                        "completion_review_receipt_path": password_receipt_path,
                        "completion_review_receipt_status": "pass" if password_receipt_ok else "requested",
                        "status": "waiting_for_worker",
                    },
                )
                password_summary = f"completion-review-password: {ticket['ticket_id']} -> continue_same_ticket ({password_reason})"
                current_run = publish_hook_status(
                    project_root,
                    current_run,
                    decision="continue_same_ticket",
                    summary=password_summary,
                )
                append_hook_log(
                    base,
                    {
                        "timestamp": now_iso(),
                        "mode": "completion-review",
                        "ticket_id": str(ticket["ticket_id"]),
                        "nonce": pending_nonce,
                        "observed_password": observed_password,
                        "password_ok": False,
                        "receipt_ok": password_receipt_ok,
                        "receipt_path": password_receipt_path,
                        "failures": password_failures,
                    },
                )
                if password_receipt_ok:
                    continuation_message = build_completion_password_retry_message(
                        ticket,
                        pending_nonce,
                        password_failure_reason=password_reason,
                    )
                else:
                    request = {
                        "ticket_id": str(ticket["ticket_id"]),
                        "nonce": pending_nonce,
                        "required_artifacts": list(
                            (current_run or {}).get("completion_review_required_artifacts")
                            or ticket.get("linked_artifacts")
                            or []
                        )[:12],
                    }
                    continuation_message = build_completion_review_request_message(
                        ticket,
                        request,
                        password_failure_reason=password_reason,
                    )
                return continue_hook_response(
                    payload=payload,
                    ticket=ticket,
                    continuation_message=continuation_message,
                    hook_summary=password_summary,
                    announce=password_reason,
                )

            receipt_ok, receipt_reason, receipt_failures, receipt = completion_review_receipt_gate(ticket, current_run)
            receipt_path = str((receipt or {}).get("_path") or "").strip()
            receipt_summary = (
                f"completion-review-receipt: {ticket['ticket_id']} -> pass"
                if receipt_ok
                else f"completion-review-receipt: {ticket['ticket_id']} -> continue_same_ticket ({receipt_reason})"
            )
            append_hook_log(
                base,
                {
                    "timestamp": now_iso(),
                    "mode": "completion-review",
                    "ticket_id": str(ticket["ticket_id"]),
                    "nonce": pending_nonce,
                    "receipt_path": receipt_path,
                    "receipt_ok": receipt_ok,
                    "failures": receipt_failures,
                },
            )
            if not receipt_ok:
                if not impl_loop_allowed:
                    current_run = persist_impl_loop_active(project_root, current_run, False)
                    announce_message("Stopping safely. Same-ticket impl continuation is not active for this session.")
                    return emit_stop_payload(
                        continue_value=False,
                        stop_reason="completion review receipt requested without an active impl loop",
                        system_message=f"Stop hook: {receipt_summary}",
                    )
                current_run = persist_impl_loop_active(project_root, current_run, True)
                current_run = persist_runtime_update(
                    project_root,
                    current_run,
                    {
                        "completion_review_requested": True,
                        "completion_review_required_artifacts": list(
                            (current_run or {}).get("completion_review_required_artifacts") or []
                        ),
                        "completion_review_receipt_path": receipt_path,
                        "completion_review_receipt_status": "failed",
                        "status": "waiting_for_worker",
                    },
                )
                current_run = publish_hook_status(
                    project_root,
                    current_run,
                    decision="continue_same_ticket",
                    summary=receipt_summary,
                )
                request = {
                    "ticket_id": str(ticket["ticket_id"]),
                    "nonce": pending_nonce,
                    "required_artifacts": list(
                        (current_run or {}).get("completion_review_required_artifacts")
                        or ticket.get("linked_artifacts")
                        or []
                    )[:12],
                }
                failure_message = receipt_failures[0] if receipt_failures else receipt_reason
                continuation_message = build_completion_review_request_message(
                    ticket,
                    request,
                    failure_reason=f"the completion review receipt is still not acceptable ({failure_message})",
                )
                return continue_hook_response(
                    payload=payload,
                    ticket=ticket,
                    continuation_message=continuation_message,
                    hook_summary=receipt_summary,
                    announce=receipt_reason,
                )

            current_run = persist_impl_loop_active(project_root, current_run, False)
            current_run = persist_runtime_update(
                project_root,
                current_run,
                {
                    "completion_review_requested": False,
                    "completion_review_nonce": "",
                    "completion_review_requested_at": "",
                    "completion_review_required_artifacts": [],
                    "completion_review_receipt_path": receipt_path,
                    "completion_review_receipt_status": "pass",
                    "status": "complete",
                },
            )
            current_run = publish_hook_status(
                project_root,
                current_run,
                decision="route_to_orchestrator",
                summary=receipt_summary,
            )
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
        announce_message(f"Stopping for operator review. {reason}")
        return emit_stop_payload(system_message=f"Stop hook: {hook_summary}")

    if impl_runtime_active and not impl_result:
        review = run_role(
            base,
                "completion-reviewer",
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
                    system_message=f"Stop hook: completion-reviewer unavailable for {ticket['ticket_id']}",
                )
            current_run = persist_impl_loop_active(project_root, current_run, True)
            append_hook_log(
                base,
                {
                    "timestamp": now_iso(),
                    "mode": "completion-reviewer",
                    "ticket_id": str(ticket["ticket_id"]),
                    "outcome": "role_unavailable",
                },
            )
            continuation_message = build_missing_impl_result_reason(ticket, current_run)
            return continue_hook_response(
                payload=payload,
                ticket=ticket,
                continuation_message=continuation_message,
                hook_summary=f"completion-reviewer: {ticket['ticket_id']} -> continue_same_ticket (completion-reviewer unavailable)",
                announce=f"Continuing {ticket['ticket_id']}. Missing IMPL_RESULT in impl mode.",
            )

        proposal_action = review["action"]
        proposal_reason = review["reason"]
        proposal_summary = summarize_role_action(str(ticket["ticket_id"]), "completion-reviewer", proposal_action, proposal_reason)
        append_hook_log(
            base,
            {
                "timestamp": now_iso(),
                "mode": "completion-reviewer",
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

    return emit_stop_passthrough(
        system_message="Stop hook: no continuation action requested; allowing stop."
    )


if __name__ == "__main__":
    raise SystemExit(main())
