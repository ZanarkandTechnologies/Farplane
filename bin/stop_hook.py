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
VALID_DECISIONS = {"done", "continue_same_ticket", "optional_upsell", "blocked"}
RALPH_RESULT_PATTERN = re.compile(r"^RALPH_RESULT:\s+status=.*$", re.MULTILINE)


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


def current_run_state_path(project_root: Path) -> Path:
    return project_root / ".ralph" / "state" / "current-run.json"


def load_current_run(project_root: Path) -> dict[str, object] | None:
    path = current_run_state_path(project_root)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


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


def parse_frontmatter(ticket_text: str) -> dict[str, str]:
    if not ticket_text.startswith("---\n"):
        return {}
    parts = ticket_text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}
    data: dict[str, str] = {}
    for line in parts[0][4:].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
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
        "phase": frontmatter.get("phase", ""),
        "acceptance_gaps": unchecked_items(sections.get("Acceptance Criteria", [])),
        "evidence_gaps": unchecked_items(sections.get("Evidence", [])),
        "blockers": blocked_items(sections.get("Blockers", [])),
    }


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

    ticket_files = sorted((home / "tickets" / "building").glob("TASK-*.md"))
    review_files = sorted((home / "tickets" / "review").glob("TASK-*.md"))
    all_ticket_files = ticket_files + review_files
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

    if len(all_ticket_files) == 1:
        return load_ticket(all_ticket_files[0])

    return None


def extract_ralph_result(message: str) -> str | None:
    matches = RALPH_RESULT_PATTERN.findall(message)
    return matches[-1].strip() if matches else None


def run_ralph_judge(base: Path, ticket: dict[str, object], worker_result: str, current_run: dict[str, object] | None = None) -> dict[str, object] | None:
    current_phase = str((current_run or {}).get("phase") or ticket["phase"] or "building")
    try:
        completed = subprocess.run(
            [
                sys.executable,
                str(base / "bin" / "ralph_judge.py"),
                "--ticket",
                str(ticket["path"]),
                "--phase",
                current_phase,
                "--worker-result",
                worker_result,
            ],
            text=True,
            capture_output=True,
            check=False,
            cwd=base,
            timeout=classifier_timeout_secs(),
        )
    except subprocess.TimeoutExpired:
        return None
    if completed.returncode != 0:
        return None
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


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


def default_speak(decision: str, ticket: dict[str, object] | None, reason: str) -> str:
    if decision == "continue_same_ticket":
        ticket_id = str(ticket["ticket_id"]) if ticket else "current ticket"
        return f"Continuing {ticket_id}. {reason}"
    if decision == "blocked":
        return f"Stopping for review. {reason}"
    if decision == "optional_upsell":
        return "Stopping after an optional follow-up suggestion"
    return "Task completed successfully"


def classifier_prompt(message: str, ticket: dict[str, object]) -> str:
    ticket_id = str(ticket["ticket_id"])
    acceptance_gaps = list(ticket["acceptance_gaps"])
    evidence_gaps = list(ticket["evidence_gaps"])
    blockers = list(ticket["blockers"])

    ticket_snapshot = {
        "ticket_id": ticket_id,
        "acceptance_gaps": acceptance_gaps,
        "evidence_gaps": evidence_gaps,
        "blockers": blockers,
    }

    return (
        "You are a stop-hook classifier for an autonomous coding agent.\n"
        "This is a classification-only task. Do not propose work, ask questions, or expand scope.\n\n"
        "Classify the latest assistant message into one of these decisions:\n"
        "- done\n"
        "- continue_same_ticket\n"
        "- optional_upsell\n"
        "- blocked\n\n"
        "Hard policy:\n"
        "- Continue only when the next step is clearly required to finish the same ticket.\n"
        "- Optional upsells like 'if you want' or scope expansion must stop.\n"
        "- Continue must stay within the listed unchecked acceptance/evidence items.\n"
        "- If ambiguous, do not continue.\n"
        "- If blockers exist, choose blocked.\n\n"
        "Return JSON only.\n\n"
        f"Latest assistant message:\n{message}\n\n"
        "Active ticket snapshot:\n"
        f"{json.dumps(ticket_snapshot, ensure_ascii=True, indent=2)}\n\n"
        "Output requirements:\n"
        "- decision: one enum value\n"
        "- reason: short operator-facing explanation\n"
        "- continuation_message: required only if decision is continue_same_ticket; it should be a direct continuation instruction\n"
        "- speak: one short sentence to say aloud\n"
    )


def classifier_command(output_path: Path) -> list[str]:
    command = [
        "codex",
        "exec",
        "--ephemeral",
        "--skip-git-repo-check",
        "-C",
        "/tmp",
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


def parse_classifier_output(output_path: Path) -> dict[str, str] | None:
    try:
        payload = json.loads(output_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None

    if not isinstance(payload, dict):
        return None

    decision = payload.get("decision")
    reason = payload.get("reason")
    speak = payload.get("speak")
    continuation_message = payload.get("continuation_message", "")

    if not isinstance(decision, str) or decision not in VALID_DECISIONS:
        return None
    if not isinstance(reason, str) or not reason.strip():
        return None
    if not isinstance(speak, str) or not speak.strip():
        return None
    if not isinstance(continuation_message, str):
        return None

    return {
        "decision": decision,
        "reason": reason.strip(),
        "continuation_message": continuation_message.strip(),
        "speak": speak.strip(),
    }


def run_classifier(message: str, ticket: dict[str, object]) -> dict[str, str] | None:
    with tempfile.NamedTemporaryFile(
        prefix="codexter-stop-hook-",
        suffix=".json",
        delete=False,
    ) as temp_output:
        output_path = Path(temp_output.name)

    try:
        try:
            completed = subprocess.run(
                classifier_command(output_path),
                input=classifier_prompt(message, ticket),
                text=True,
                capture_output=True,
                check=False,
                timeout=classifier_timeout_secs(),
            )
        except subprocess.TimeoutExpired:
            return None
        if completed.returncode != 0:
            return None
        return parse_classifier_output(output_path)
    finally:
        output_path.unlink(missing_ok=True)


def main() -> int:
    payload, raw_payload = read_payload()
    home = codexter_home()
    project_root = project_root_from_payload(payload)
    base = runtime_root(home, project_root)
    current_run = load_current_run(project_root) if project_root is not None else None
    raw_message = payload.get("last_assistant_message") or ""
    message = raw_message if isinstance(raw_message, str) else ""
    ralph_result = extract_ralph_result(message or raw_payload)

    if not env_enabled() and current_run is None and ralph_result is None:
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
    if (ralph_mode_enabled or current_run is not None or ralph_result is not None) and ralph_result:
        verdict = run_ralph_judge(base, ticket, ralph_result, current_run)
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
            return 0
        decision = str(verdict.get("decision", ""))
        next_phase = str(verdict.get("next_phase", ""))
        reason = str(verdict.get("reason", "")).strip() or "ralph verdict available"
        orchestrator_message = str(verdict.get("orchestrator_message", "")).strip() or reason
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
        if decision in {"repeat_ralphplan", "repeat_ralph"}:
            announce_message(orchestrator_message)
            if payload.get("stop_hook_active"):
                announce_message("Stopping after one Ralph-assisted continuation pass")
                return 0
            json.dump({"decision": "block", "reason": orchestrator_message}, sys.stdout)
            sys.stdout.write("\n")
            return 0
        if decision == "block_ticket":
            announce_message(f"Stopping for review. {reason}")
            return 0
        if decision in {"advance_ticket", "complete_ticket"}:
            announce_message(f"Ralph phase accepted. Next: {next_phase or 'none'}")
            return 0
        announce_message(f"Stopping for operator review. {reason}")
        return 0

    blockers = list(ticket["blockers"])
    if blockers:
        announce_message(f"Stopping for review. Ticket blocker recorded: {blockers[0]}")
        return 0

    verdict = run_classifier(message, ticket)
    if verdict is None:
        append_hook_log(
            base,
            {
                "timestamp": now_iso(),
                "mode": "legacy",
                "ticket_id": str(ticket["ticket_id"]),
                "outcome": "judge_unavailable",
            },
        )
        announce_message("Stop check unavailable. Stopping safely.")
        return 0

    decision = verdict["decision"]
    reason = verdict["reason"]
    speak = verdict["speak"]
    continuation_message = verdict["continuation_message"]
    append_hook_log(
        base,
        {
            "timestamp": now_iso(),
            "mode": "legacy",
            "ticket_id": str(ticket["ticket_id"]),
            "decision": decision,
            "reason": reason,
        },
    )

    if payload.get("stop_hook_active") and decision == "continue_same_ticket":
        announce_message("Stopping after one assisted continuation pass")
        return 0

    gaps = list(ticket["acceptance_gaps"]) + list(ticket["evidence_gaps"])
    if decision == "continue_same_ticket":
        if not gaps:
            announce_message("Task completed successfully")
            return 0
        if not continuation_message:
            continuation_message = build_reason(ticket)
        announce_message(speak or default_speak(decision, ticket, reason))
        json.dump({"decision": "block", "reason": continuation_message}, sys.stdout)
        sys.stdout.write("\n")
        return 0

    announce_message(speak or default_speak(decision, ticket, reason))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
