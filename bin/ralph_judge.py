#!/usr/bin/env python3
"""
RALPH JUDGE
===========
Purpose

Read one ticket plus one worker result line and emit a conservative verdict
for the next Ralph transition.

KEY CONCEPTS:
- tickets are the canonical execution contract
- run-state is runtime-only
- judge decides; it does not implement

USAGE:
- python3 bin/ralph_judge.py --ticket <path> --phase <phase> --worker-result "<RALPH_RESULT...>"

MEMORY REFERENCES:
- MEM-0001
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SECTION_PATTERN = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
CHECKBOX_PATTERN = re.compile(r"^- \[( |x)\]\s+(.*)$")
RESULT_PATTERN = re.compile(
    r"^RALPH_RESULT:\s+status=(?P<status>[A-Za-z0-9_-]+)\s+next=(?P<next>[A-Za-z0-9_-]+)(?:\s+reason=(?P<reason>.*))?$"
)

ALLOWED_PHASES = {
    "planning",
    "building",
    "documenting",
}


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
        if stripped and stripped.lower() not in {"none", "- none"}:
            items.append(stripped.lstrip("-").strip())
    return items


def load_ticket(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    sections = parse_sections(text)
    ticket_id_match = re.search(r"\bTASK-\d{4}\b", text) or re.search(r"\bTASK-\d{4}\b", path.name)
    ticket_id = ticket_id_match.group(0) if ticket_id_match else path.stem
    return {
        "ticket_id": ticket_id,
        "acceptance_gaps": unchecked_items(sections.get("Acceptance Criteria", [])),
        "evidence_gaps": unchecked_items(sections.get("Evidence", [])),
        "blockers": blocked_items(sections.get("Blockers", [])),
    }


def parse_result_line(line: str) -> dict[str, str]:
    match = RESULT_PATTERN.match(line.strip())
    if not match:
      raise ValueError("invalid RALPH_RESULT line")
    return {
        "status": match.group("status"),
        "next": match.group("next"),
        "reason": (match.group("reason") or "").strip(),
    }


def verdict(
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


def decide(current_phase: str, ticket: dict[str, object], worker_result: dict[str, str]) -> dict[str, object]:
    ticket_id = str(ticket["ticket_id"])
    blockers = list(ticket["blockers"])
    acceptance_gaps = list(ticket["acceptance_gaps"])
    evidence_gaps = list(ticket["evidence_gaps"])
    status = worker_result["status"]
    next_value = worker_result["next"]
    reason_suffix = worker_result["reason"]

    if blockers:
        return verdict(
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
        return verdict(
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
        return verdict(
            ticket_id=ticket_id,
            current_phase=current_phase,
            decision="repeat_ralphplan" if current_phase == "planning" else "repeat_ralph",
            next_phase=next_phase,
            reason=reason_suffix or "skill requires another bounded pass",
            orchestrator_message=f"rerun {ticket_id} in {next_phase}",
            evidence_ok=False,
        )

    if status == "plan_ready":
        return verdict(
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
            return verdict(
                ticket_id=ticket_id,
                current_phase=current_phase,
                decision="repeat_ralph",
                next_phase="building",
                reason="ticket marked done but required proof remains incomplete",
                orchestrator_message=f"rerun {ticket_id} in building and resolve missing proof",
                evidence_ok=False,
                missing_evidence=missing,
            )
        return verdict(
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
            return verdict(
                ticket_id=ticket_id,
                current_phase=current_phase,
                decision="repeat_ralph",
                next_phase="building",
                reason=reason_suffix or "evidence is incomplete",
                orchestrator_message=f"rerun {ticket_id} in building with explicit missing evidence coverage",
                evidence_ok=False,
                missing_evidence=missing,
            )
        return verdict(
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
            return verdict(
                ticket_id=ticket_id,
                current_phase=current_phase,
                decision="repeat_ralph",
                next_phase="building",
                reason="documentation completed but required proof remains incomplete",
                orchestrator_message=f"rerun {ticket_id} in building and resolve missing proof",
                evidence_ok=False,
                missing_evidence=missing,
            )
        return verdict(
            ticket_id=ticket_id,
            current_phase=current_phase,
            decision="complete_ticket",
            next_phase="done",
            reason=reason_suffix or "documentation phase complete",
            orchestrator_message=f"mark {ticket_id} complete",
            evidence_ok=True,
        )

    # Default conservative path: trust a successful status that maps to a next phase.
    next_phase = next_value if next_value in ALLOWED_PHASES or next_value in {"done", "none"} else "none"
    if next_phase == "none":
        return verdict(
            ticket_id=ticket_id,
            current_phase=current_phase,
            decision="escalate_to_operator",
            next_phase="none",
            reason="unable to determine safe next phase",
            orchestrator_message=f"inspect {ticket_id} manually",
            evidence_ok=not evidence_gaps,
        )

    return verdict(
        ticket_id=ticket_id,
        current_phase=current_phase,
        decision="advance_ticket",
        next_phase=next_phase,
        reason=reason_suffix or f"worker returned status {status}",
        orchestrator_message=f"advance {ticket_id} to {next_phase}",
        evidence_ok=not evidence_gaps,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticket", required=True)
    parser.add_argument("--phase", required=True, choices=sorted(ALLOWED_PHASES))
    parser.add_argument("--worker-result", required=True)
    args = parser.parse_args()

    ticket = load_ticket(Path(args.ticket))
    worker_result = parse_result_line(args.worker_result)
    payload = decide(args.phase, ticket, worker_result)
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
