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
"""

import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from notify import announce_message


TICKET_ID_PATTERN = re.compile(r"\bTASK-\d{4}\b")
SECTION_PATTERN = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
CHECKBOX_PATTERN = re.compile(r"^- \[( |x)\]\s+(.*)$")
RALPH_RESULT_PATTERN = re.compile(r"^RALPH_RESULT:\s+status=.*$", re.MULTILINE)
PARSED_RESULT_PATTERN = re.compile(
    r"^RALPH_RESULT:\s+status=(?P<status>[A-Za-z0-9_-]+)\s+next=(?P<next>[A-Za-z0-9_-]+)(?:\s+reason=(?P<reason>.*))?$"
)
ALLOWED_PHASES = {"planning", "building", "documenting"}
ROLE_ACTIONS = {
    "continue_same_ticket",
    "route_to_orchestrator",
    "block_for_user",
    "next_ticket",
    "stop",
}


def env_enabled() -> bool:
    legacy = os.environ.get("CODEXTER_ASSISTED_CONTINUATION", "").lower() in {
        "1",
        "true",
        "yes",
        "on",
    }
    ralph = os.environ.get("CODEXTER_RALPH_HOOK", "").lower() in {
        "1",
        "true",
        "yes",
        "on",
    }
    return legacy or ralph


def has_project_runtime_context(project_root: Path | None) -> bool:
    if project_root is None:
        return False
    return (project_root / ".ralph").exists() or (project_root / "tickets").exists()


def has_explicit_ticket_selector() -> bool:
    return bool(
        os.environ.get("RALPH_TICKET", "").strip()
        or os.environ.get("CODEXTER_ACTIVE_TICKET", "").strip()
    )


def hook_enabled_for_context(
    project_root: Path | None,
    current_run: dict[str, object] | None,
    ralph_result: str | None,
) -> bool:
    # Keep the env flag as an explicit override, but auto-activate when the
    # hook is clearly running inside a Codexter/Ralph context.
    return (
        env_enabled()
        or current_run is not None
        or ralph_result is not None
        or has_explicit_ticket_selector()
        or has_project_runtime_context(project_root)
    )


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
    for key in ("cwd", "workdir", "current_working_directory"):
        raw = payload.get(key)
        if isinstance(raw, str) and raw.strip():
            path = Path(raw).expanduser()
            if path.exists():
                return path.resolve()
    for raw_fallback in (os.environ.get("PWD", "").strip(), str(Path.cwd())):
        if not raw_fallback:
            continue
        candidate = Path(raw_fallback).expanduser()
        if candidate.exists() and ((candidate / ".ralph").exists() or (candidate / "tickets").exists()):
            return candidate.resolve()
    return None


def runtime_root(home: Path, project_root: Path | None) -> Path:
    if project_root is not None and (project_root / "bin" / "stop_hook.py").exists():
        return project_root
    return home


def schema_path() -> Path:
    return Path(__file__).with_name("stop_hook_output.schema.json")


def agent_prompt_path(base: Path, name: str) -> Path:
    return base / "agents" / f"{name}.md"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def append_hook_log(base: Path, payload: dict[str, object]) -> None:
    log_dir = base / ".ralph" / "logs"
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
    return project_root / ".ralph" / "state" / "current-run.json"


def load_current_run(project_root: Path) -> dict[str, object] | None:
    path = current_run_state_path(project_root)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


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
    merged_current = dict(current_run)
    merged_current.update(updates)
    merged_current["updated_at"] = str(updates.get("updated_at") or now_iso())
    write_json(current_run_state_path(project_root), merged_current)

    run_state = merged_current.get("run_state")
    if isinstance(run_state, str) and run_state.strip():
        run_state_path = resolve_runtime_path(project_root, run_state)
        existing_run_state = {}
        try:
            existing_payload = json.loads(run_state_path.read_text(encoding="utf-8"))
            if isinstance(existing_payload, dict):
                existing_run_state = existing_payload
        except (FileNotFoundError, json.JSONDecodeError):
            existing_run_state = {}
        existing_run_state.update(updates)
        existing_run_state["updated_at"] = merged_current["updated_at"]
        write_json(run_state_path, existing_run_state)

    return merged_current


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
        "next_action": str(frontmatter.get("next_action", "")).strip(),
        "last_verification": str(frontmatter.get("last_verification", "")).strip(),
        "linked_docs": list(frontmatter.get("linked_docs", [])) if isinstance(frontmatter.get("linked_docs", []), list) else [],
        "acceptance_gaps": unchecked_items(sections.get("Acceptance Criteria", [])),
        "evidence_gaps": unchecked_items(sections.get("Evidence", [])),
        "blockers": blocked_items(sections.get("Blockers", [])),
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
    explicit_path = os.environ.get("RALPH_TICKET", "").strip()
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


def extract_ralph_result(message: str) -> str | None:
    matches = RALPH_RESULT_PATTERN.findall(message)
    return matches[-1].strip() if matches else None


def parse_ralph_result(line: str) -> dict[str, str]:
    match = PARSED_RESULT_PATTERN.match(line.strip())
    if not match:
        raise ValueError("invalid RALPH_RESULT line")
    return {
        "status": match.group("status"),
        "next": match.group("next"),
        "reason": (match.group("reason") or "").strip(),
    }


def ralph_verdict(
    *,
    ticket_id: str,
    current_phase: str,
    decision: str,
    next_phase: str,
    reason: str,
    orchestrator_message: str,
    evidence_ok: bool,
    missing_evidence: list[str] | None = None,
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
    if blockers:
        payload["blockers"] = blockers
    return payload


def decide_ralph_transition(current_phase: str, ticket: dict[str, object], worker_result: dict[str, str]) -> dict[str, object]:
    ticket_id = str(ticket["ticket_id"])
    blockers = list(ticket["blockers"])
    acceptance_gaps = list(ticket["acceptance_gaps"])
    evidence_gaps = list(ticket["evidence_gaps"])
    status = worker_result["status"]
    next_value = worker_result["next"]
    reason_suffix = worker_result["reason"]

    if blockers:
        return ralph_verdict(
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
        return ralph_verdict(
            ticket_id=ticket_id,
            current_phase=current_phase,
            decision="block_ticket",
            next_phase="none",
            reason=reason,
            orchestrator_message=f"stop {ticket_id} and surface blocker",
            evidence_ok=False,
        )

    if status in {"continue_ralphplan", "continue_ralph"}:
        next_phase = current_phase if next_value in {"planning", "building", "none"} else next_value
        return ralph_verdict(
            ticket_id=ticket_id,
            current_phase=current_phase,
            decision="repeat_ralphplan" if current_phase == "planning" else "repeat_ralph",
            next_phase=next_phase,
            reason=reason_suffix or "skill requires another bounded pass",
            orchestrator_message=f"rerun {ticket_id} in {next_phase}",
            evidence_ok=False,
        )

    if status == "plan_ready":
        return ralph_verdict(
            ticket_id=ticket_id,
            current_phase=current_phase,
            decision="advance_ticket",
            next_phase="building",
            reason=reason_suffix or "plan is present",
            orchestrator_message=f"advance {ticket_id} to building",
            evidence_ok=not evidence_gaps,
        )

    if status == "done":
        missing = acceptance_gaps + evidence_gaps
        if missing:
            return ralph_verdict(
                ticket_id=ticket_id,
                current_phase=current_phase,
                decision="repeat_ralph",
                next_phase="building",
                reason="ticket marked done but required proof remains incomplete",
                orchestrator_message=f"rerun {ticket_id} in building and resolve missing proof",
                evidence_ok=False,
                missing_evidence=missing,
            )
        return ralph_verdict(
            ticket_id=ticket_id,
            current_phase=current_phase,
            decision="complete_ticket",
            next_phase="done",
            reason=reason_suffix or "ticket appears complete",
            orchestrator_message=f"mark {ticket_id} complete",
            evidence_ok=True,
        )

    if status == "build_complete":
        missing = acceptance_gaps + evidence_gaps
        if missing:
            return ralph_verdict(
                ticket_id=ticket_id,
                current_phase=current_phase,
                decision="repeat_ralph",
                next_phase="building",
                reason=reason_suffix or "evidence is incomplete",
                orchestrator_message=f"rerun {ticket_id} in building with explicit missing evidence coverage",
                evidence_ok=False,
                missing_evidence=missing,
            )
        return ralph_verdict(
            ticket_id=ticket_id,
            current_phase=current_phase,
            decision="complete_ticket",
            next_phase="done",
            reason=reason_suffix or "build plus evidence appear complete",
            orchestrator_message=f"mark {ticket_id} complete",
            evidence_ok=True,
        )

    if status == "docs_complete":
        missing = acceptance_gaps + evidence_gaps
        if missing:
            return ralph_verdict(
                ticket_id=ticket_id,
                current_phase=current_phase,
                decision="repeat_ralph",
                next_phase="building",
                reason="documentation completed but required proof remains incomplete",
                orchestrator_message=f"rerun {ticket_id} in building and resolve missing proof",
                evidence_ok=False,
                missing_evidence=missing,
            )
        return ralph_verdict(
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
        return ralph_verdict(
            ticket_id=ticket_id,
            current_phase=current_phase,
            decision="escalate_to_operator",
            next_phase="none",
            reason="unable to determine safe next phase",
            orchestrator_message=f"inspect {ticket_id} manually",
            evidence_ok=not evidence_gaps,
        )

    return ralph_verdict(
        ticket_id=ticket_id,
        current_phase=current_phase,
        decision="advance_ticket",
        next_phase=next_phase,
        reason=reason_suffix or f"worker returned status {status}",
        orchestrator_message=f"advance {ticket_id} to {next_phase}",
        evidence_ok=not evidence_gaps,
    )


def run_ralph_judge(ticket: dict[str, object], worker_result: str, current_run: dict[str, object] | None = None) -> dict[str, object] | None:
    current_phase = str((current_run or {}).get("phase") or ticket["phase"] or "building")
    try:
        parsed = parse_ralph_result(worker_result)
    except ValueError:
        return None
    return decide_ralph_transition(current_phase, ticket, parsed)


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
    if os.environ.get("CODEXTER_RALPH_TMUX_DRY_RUN", "").lower() in {"1", "true", "yes", "on"}:
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


def build_missing_ralph_result_reason(ticket: dict[str, object], current_run: dict[str, object] | None) -> str:
    ticket_id = str(ticket["ticket_id"])
    current_phase = str(ticket["phase"] or (current_run or {}).get("phase") or "building")
    return (
        f"Continue {ticket_id} in {current_phase}. The last assistant message implied more same-ticket work "
        "but ended without an explicit RALPH_RESULT line. Continue the same ticket, update repo/ticket state, "
        "and finish with a RALPH_RESULT."
    )


def skill_name_for_phase(phase: str) -> str:
    mapping = {
        "planning": "ralplan",
        "building": "ralph",
        "documenting": "docs-closeout",
    }
    return mapping.get(phase, "ralph")


def build_live_followup_reason(phase: str, orchestrator_message: str, ticket: dict[str, object]) -> str:
    skill_name = skill_name_for_phase(phase)
    return (
        "Continue the current live Codex lane.\n\n"
        f"Follow-up reason: {orchestrator_message}\n\n"
        f"Run the `{skill_name}` skill on ticket `{ticket['ticket_id']}`.\n"
        "Resolve ticket context from the active ticket state first, then update the ticket itself with any new evidence, blockers, handoff, "
        "next action, and verification before you stop.\n"
    )


def summarize_ralph_hook(ticket_id: str, decision: str, next_phase: str, reason: str) -> str:
    if decision in {"repeat_ralphplan", "repeat_ralph"}:
        target = next_phase or "same-phase"
        return f"Ralph repeat: {ticket_id} -> {target} ({reason})"
    if decision == "advance_ticket":
        target = next_phase or "next-phase"
        return f"Ralph advance: {ticket_id} -> {target} ({reason})"
    if decision == "complete_ticket":
        return f"Ralph complete: {ticket_id} ({reason})"
    if decision == "block_ticket":
        return f"Ralph blocked: {ticket_id} ({reason})"
    return f"Ralph review: {ticket_id} ({reason})"


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


def role_command(base: Path, output_path: Path) -> list[str]:
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
        "-c",
        'developer_instructions=""',
        "--output-schema",
        str(schema_path()),
        "--output-last-message",
        str(output_path),
        "-",
    ]

    model = os.environ.get("CODEXTER_STOP_HOOK_MODEL", "").strip()
    if model:
        command[2:2] = ["-m", model]

    return command


def parse_role_output(output_path: Path) -> dict[str, str] | None:
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

    return {
        "action": action,
        "reason": reason.strip(),
        "continuation_message": continuation_message.strip(),
        "speak": speak.strip(),
        "next_ticket_id": next_ticket_id.strip(),
        "next_phase": next_phase.strip(),
    }


def run_role(base: Path, prompt: str) -> dict[str, str] | None:
    with tempfile.NamedTemporaryFile(
        prefix="codexter-stop-hook-",
        suffix=".json",
        delete=False,
    ) as temp_output:
        output_path = Path(temp_output.name)

    try:
        try:
            completed = subprocess.run(
                role_command(base, output_path),
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


def role_prompt_from_file(base: Path, role_name: str, context_label: str, payload: dict[str, object]) -> str:
    instructions = agent_prompt_path(base, role_name).read_text(encoding="utf-8").strip()
    return (
        f"{instructions}\n\n"
        f"{context_label}:\n"
        f"{json.dumps(payload, ensure_ascii=True, indent=2)}\n"
    )


def reviewer_prompt(
    base: Path,
    message: str,
    ticket: dict[str, object],
    current_run: dict[str, object] | None,
    verdict: dict[str, object] | None,
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
        "verdict": verdict or {},
    }
    return role_prompt_from_file(
        base,
        "reviewer",
        "Context",
        {
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
    return role_prompt_from_file(base, "orchestrator", "Context", payload)


def continue_hook_response(
    *,
    payload: dict[str, object],
    ticket: dict[str, object],
    continuation_message: str,
    hook_summary: str,
    announce: str,
) -> int:
    if payload.get("stop_hook_active"):
        announce_message("Stopping after one Ralph-assisted continuation pass")
        return emit_stop_payload(
            continue_value=False,
            stop_reason="Stopping after one Ralph-assisted continuation pass",
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
    role_output = run_role(base, orchestrator_prompt(base, ticket, verdict, board_snapshot(home, project_root)))
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
    current_run = load_current_run(project_root) if project_root is not None else None
    payload_session_id = payload.get("session_id")
    if (
        project_root is not None
        and current_run is not None
        and isinstance(payload_session_id, str)
        and payload_session_id.strip()
    ):
        current_run = persist_runtime_update(
            project_root,
            current_run,
            {"session_id": payload_session_id.strip()},
        )
    raw_message = payload.get("last_assistant_message") or ""
    message = raw_message if isinstance(raw_message, str) else ""
    ralph_result = extract_ralph_result(message or raw_payload)

    if not hook_enabled_for_context(project_root, current_run, ralph_result):
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

    ralph_mode_enabled = os.environ.get("CODEXTER_RALPH_HOOK", "").lower() in {
        "1",
        "true",
        "yes",
        "on",
    }
    ralph_runtime_active = (
        ralph_mode_enabled
        or current_run is not None
        or ralph_result is not None
        or has_explicit_ticket_selector()
    )
    live_interactive_lane = (
        isinstance(payload_session_id, str)
        and bool(payload_session_id.strip())
        and os.environ.get("CODEXTER_RALPH_TMUX_DRY_RUN", "").lower() not in {"1", "true", "yes", "on"}
    )
    if not ralph_runtime_active:
        return 0

    if ralph_runtime_active and ralph_result:
        verdict = run_ralph_judge(ticket, ralph_result, current_run)
        if verdict is None:
            append_hook_log(
                base,
                {
                    "timestamp": now_iso(),
                    "mode": "ralph",
                    "ticket_id": str(ticket["ticket_id"]),
                    "phase": str(ticket["phase"] or ""),
                    "worker_result": ralph_result,
                    "outcome": "judge_unavailable",
                },
            )
            announce_message("Ralph stop check unavailable. Stopping safely.")
            return emit_stop_payload(system_message="Stop hook: Ralph judge unavailable; stopping safely.")
        decision = str(verdict.get("decision", ""))
        next_phase = str(verdict.get("next_phase", ""))
        reason = str(verdict.get("reason", "")).strip() or "ralph verdict available"
        orchestrator_message = str(verdict.get("orchestrator_message", "")).strip() or reason
        hook_summary = summarize_ralph_hook(str(ticket["ticket_id"]), decision, next_phase, reason)
        if project_root is not None and current_run is not None:
            state_updates: dict[str, object] = {
                "last_worker_result": ralph_result,
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
                "mode": "ralph",
                "ticket_id": str(ticket["ticket_id"]),
                "phase": str(ticket["phase"] or ""),
                "worker_result": ralph_result,
                "decision": decision,
                "next_phase": next_phase,
                "reason": reason,
            },
        )
        current_phase = str((current_run or {}).get("phase") or ticket["phase"] or "building")
        if decision in {"repeat_ralphplan", "repeat_ralph"}:
            target_phase = next_phase if next_phase in {"planning", "building", "documenting"} else str(ticket["phase"] or "building")
            if live_interactive_lane:
                continuation_message = build_live_followup_reason(target_phase, orchestrator_message, ticket)
                return continue_hook_response(
                    payload=payload,
                    ticket=ticket,
                    continuation_message=continuation_message,
                    hook_summary=hook_summary,
                    announce=f"Continuing {ticket['ticket_id']} in the live Ralph lane.",
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
                        "mode": "ralph",
                        "ticket_id": str(ticket["ticket_id"]),
                        "event": "spawn_followup",
                        "followup": followup,
                    },
                )
                announce_message(f"spawned next ralph pass in {followup.get('tmux_pane') or followup.get('tmux_window')}")
                return emit_stop_payload(system_message=f"Stop hook: {hook_summary}")
            return continue_hook_response(
                payload=payload,
                ticket=ticket,
                continuation_message=orchestrator_message,
                hook_summary=hook_summary,
                announce=orchestrator_message,
            )
        if decision == "block_ticket":
            announce_message(f"Stopping for review. {reason}")
            return emit_stop_payload(system_message=f"Stop hook: {hook_summary}")
        if decision in {"advance_ticket", "complete_ticket"}:
            if decision == "advance_ticket" and current_phase == "planning" and next_phase == "building":
                target_phase = next_phase if next_phase in {"planning", "building", "documenting"} else str(ticket["phase"] or "building")
                if live_interactive_lane:
                    continuation_message = build_live_followup_reason(target_phase, orchestrator_message, ticket)
                    return continue_hook_response(
                        payload=payload,
                        ticket=ticket,
                        continuation_message=continuation_message,
                        hook_summary=hook_summary,
                        announce=f"Advancing {ticket['ticket_id']} inside the live Ralph lane.",
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
                            "mode": "ralph",
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
                    announce=f"Ralph phase accepted. Next: {next_phase or 'none'}",
                )

            review = run_role(base, reviewer_prompt(base, message, ticket, current_run, verdict))
            if review is None:
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

            review_action = review["action"]
            review_reason = review["reason"]
            review_summary = summarize_role_action(str(ticket["ticket_id"]), "reviewer", review_action, review_reason)
            append_hook_log(
                base,
                {
                    "timestamp": now_iso(),
                    "mode": "reviewer",
                    "ticket_id": str(ticket["ticket_id"]),
                    "action": review_action,
                    "reason": review_reason,
                },
            )
            current_run = publish_hook_status(project_root, current_run, decision=review_action, summary=review_summary)
            if review_action == "continue_same_ticket":
                continuation_message = review["continuation_message"] or build_reason(ticket)
                return continue_hook_response(
                    payload=payload,
                    ticket=ticket,
                    continuation_message=continuation_message,
                    hook_summary=review_summary,
                    announce=review["speak"] or review_reason,
                )
            if review_action == "route_to_orchestrator":
                return run_orchestrator_decision(
                    base=base,
                    home=home,
                    project_root=project_root,
                    payload=payload,
                    current_run=current_run,
                    ticket=ticket,
                    verdict=verdict,
                )
            announce_message(review["speak"] or review_reason)
            return emit_stop_payload(system_message=f"Stop hook: {review_summary}")
        announce_message(f"Stopping for operator review. {reason}")
        return emit_stop_payload(system_message=f"Stop hook: {hook_summary}")

    if ralph_runtime_active and not ralph_result:
        review = run_role(base, reviewer_prompt(base, message, ticket, current_run, None))
        if review is None:
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
            return emit_stop_payload(system_message="Stop hook: reviewer unavailable; stopping safely.")

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
            continuation_message = review["continuation_message"] or build_missing_ralph_result_reason(ticket, current_run)
            return continue_hook_response(
                payload=payload,
                ticket=ticket,
                continuation_message=continuation_message,
                hook_summary=proposal_summary,
                announce=review["speak"] or f"Continuing {ticket['ticket_id']}. Missing RALPH_RESULT in Ralph mode.",
            )

        if proposal_action == "route_to_orchestrator":
            return run_orchestrator_decision(
                base=base,
                home=home,
                project_root=project_root,
                payload=payload,
                current_run=current_run,
                ticket=ticket,
                verdict=None,
            )

        announce_message(review["speak"] or proposal_reason)
        return emit_stop_payload(system_message=f"Stop hook: {proposal_summary}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
