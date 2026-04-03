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
"""

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from notify import announce_message


TICKET_ID_PATTERN = re.compile(r"\bTASK-\d{4}\b")
SECTION_PATTERN = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
CHECKBOX_PATTERN = re.compile(r"^- \[( |x)\]\s+(.*)$")
VALID_DECISIONS = {"done", "continue_same_ticket", "optional_upsell", "blocked"}


def is_enabled() -> bool:
    return os.environ.get("CODEXTER_ASSISTED_CONTINUATION", "").lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def read_payload() -> dict[str, object]:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def codexter_home() -> Path:
    configured = os.environ.get("CODEXTER_HOME", "").strip()
    if configured:
        return Path(configured).expanduser().resolve()

    return Path(__file__).expanduser().absolute().parent.parent


def schema_path() -> Path:
    return Path(__file__).with_name("stop_hook_output.schema.json")


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
        if stripped and stripped.lower() != "- none":
            items.append(stripped.lstrip("-").strip())
    return items


def extract_ticket_id(text: str) -> str | None:
    match = TICKET_ID_PATTERN.search(text)
    return match.group(0) if match else None


def load_ticket(ticket_path: Path) -> dict[str, object]:
    text = ticket_path.read_text(encoding="utf-8")
    sections = parse_sections(text)
    fallback_ticket_id = extract_ticket_id(ticket_path.name) or ticket_path.stem
    return {
        "path": ticket_path,
        "text": text,
        "ticket_id": extract_ticket_id(text) or fallback_ticket_id,
        "acceptance_gaps": unchecked_items(sections.get("Acceptance Criteria", [])),
        "evidence_gaps": unchecked_items(sections.get("Evidence", [])),
        "blockers": blocked_items(sections.get("Blockers", [])),
    }


def resolve_ticket(home: Path, message: str) -> dict[str, object] | None:
    building_dir = home / "tickets" / "building"
    ticket_files = sorted(building_dir.glob("TASK-*.md"))
    if not ticket_files:
        return None

    mentioned_ticket = extract_ticket_id(message)
    if mentioned_ticket:
        for ticket_file in ticket_files:
            if ticket_file.name.startswith(mentioned_ticket):
                return load_ticket(ticket_file)

    explicit_ticket = os.environ.get("CODEXTER_ACTIVE_TICKET", "").strip()
    if explicit_ticket:
        for ticket_file in ticket_files:
            if ticket_file.name.startswith(explicit_ticket):
                return load_ticket(ticket_file)

    if len(ticket_files) == 1:
        return load_ticket(ticket_files[0])

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
    payload = read_payload()
    if not is_enabled():
        return 0

    if payload.get("hook_event_name") != "Stop":
        return 0

    message = payload.get("last_assistant_message") or ""
    if not isinstance(message, str) or not message.strip():
        return 0

    ticket = resolve_ticket(codexter_home(), message)
    if ticket is None:
        return 0

    blockers = list(ticket["blockers"])
    if blockers:
        announce_message(f"Stopping for review. Ticket blocker recorded: {blockers[0]}")
        return 0

    verdict = run_classifier(message, ticket)
    if verdict is None:
        announce_message("Stop check unavailable. Stopping safely.")
        return 0

    decision = verdict["decision"]
    reason = verdict["reason"]
    speak = verdict["speak"]
    continuation_message = verdict["continuation_message"]

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
