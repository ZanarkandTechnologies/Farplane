#!/usr/bin/env python3
"""Read-only selector for Codexter filesystem tickets."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


TICKET_ID_RE = re.compile(r"^TASK-\d{4}$")
PRIORITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}
PHASE_ACTIONS = {
    "building": ("start_impl", "impl"),
    "documenting": ("start_closeout", "close-ticket"),
    "planning": ("start_planning", "impl-plan"),
}
PHASE_RANK = {"building": 0, "documenting": 1, "planning": 2}
TERMINAL_STATUSES = {"blocked", "done", "failed"}


@dataclass(frozen=True)
class TicketCard:
    ticket_id: str
    path: str
    phase: str
    status: str
    priority: str
    depends_on: list[str]
    blocked_by: list[str]
    ready: bool
    approval_required: bool
    claimed_by: str
    next_action: str
    archived: bool
    dependency_waivers: list[str]


@dataclass(frozen=True)
class Eligibility:
    ticket_id: str
    eligible: bool
    reason: str
    action: str
    recommended_skill: str
    needs_human: bool


def parse_scalar(raw: str) -> object:
    value = raw.strip()
    if value == "[]":
        return []
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}, text
    raw_frontmatter = parts[0][4:]
    body = parts[1]
    data: dict[str, object] = {}
    lines = raw_frontmatter.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if ":" not in line:
            index += 1
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        if value == "":
            items: list[str] = []
            index += 1
            while index < len(lines) and lines[index].startswith("  - "):
                items.append(lines[index][4:].strip())
                index += 1
            data[key] = items if items else ""
            continue
        data[key] = parse_scalar(value)
        index += 1
    return data, body


def as_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def as_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() == "true"
    return False


def dependency_waivers(body: str) -> list[str]:
    waivers: set[str] = set()
    for line in body.splitlines():
        lowered = line.lower()
        if "waiv" not in lowered:
            continue
        for ticket_id in re.findall(r"TASK-\d{4}", line):
            waivers.add(ticket_id)
    return sorted(waivers)


def load_ticket_card(path: Path, root: Path, *, archived: bool) -> TicketCard:
    frontmatter, body = parse_frontmatter(path.read_text(encoding="utf-8"))
    ticket_id = str(frontmatter.get("ticket_id") or path.parent.name).strip()
    return TicketCard(
        ticket_id=ticket_id,
        path=str(path.relative_to(root)),
        phase=str(frontmatter.get("phase") or "").strip(),
        status=str(frontmatter.get("status") or "").strip(),
        priority=str(frontmatter.get("priority") or "medium").strip(),
        depends_on=as_list(frontmatter.get("depends_on")),
        blocked_by=as_list(frontmatter.get("blocked_by")),
        ready=as_bool(frontmatter.get("ready")),
        approval_required=as_bool(frontmatter.get("approval_required")),
        claimed_by=str(frontmatter.get("claimed_by") or "").strip(),
        next_action=str(frontmatter.get("next_action") or "").strip(),
        archived=archived,
        dependency_waivers=dependency_waivers(body),
    )


def iter_ticket_paths(root: Path) -> Iterable[tuple[Path, bool]]:
    tickets_dir = root / "tickets"
    for path in sorted(tickets_dir.glob("TASK-*/ticket.md")):
        if path.is_file():
            yield path, False
    for path in sorted((tickets_dir / "archive").glob("TASK-*/ticket.md")):
        if path.is_file():
            yield path, True


def load_board(root: Path) -> list[TicketCard]:
    resolved = root.resolve()
    return [load_ticket_card(path, resolved, archived=archived) for path, archived in iter_ticket_paths(resolved)]


def dependency_is_satisfied(dep: str, active_by_id: dict[str, TicketCard], archived_complete: set[str]) -> bool:
    if dep in archived_complete:
        return True
    card = active_by_id.get(dep)
    if card is None:
        return False
    return card.status == "done" or card.phase == "complete"


def eligible(card: TicketCard, board: list[TicketCard]) -> Eligibility:
    action, skill = PHASE_ACTIONS.get(card.phase, ("stop", ""))
    if card.archived:
        return Eligibility(card.ticket_id, False, "ticket is archived", "stop", "", False)
    if not TICKET_ID_RE.match(card.ticket_id):
        return Eligibility(card.ticket_id, False, "invalid ticket id", "stop", "", False)
    if card.status in TERMINAL_STATUSES or card.phase in {"complete", "failed"}:
        return Eligibility(card.ticket_id, False, f"terminal state phase={card.phase} status={card.status}", "stop", "", False)
    if card.approval_required:
        return Eligibility(card.ticket_id, False, "approval required", "stop", "", True)
    if not card.ready:
        return Eligibility(card.ticket_id, False, "ready is false", "stop", "", False)
    if card.blocked_by:
        return Eligibility(card.ticket_id, False, "blocked by " + ", ".join(card.blocked_by), "stop", "", False)
    if card.claimed_by:
        return Eligibility(card.ticket_id, False, f"claimed by {card.claimed_by}", "stop", "", False)
    if card.phase not in PHASE_ACTIONS:
        return Eligibility(card.ticket_id, False, f"unsupported phase {card.phase}", "stop", "", False)

    active_by_id = {item.ticket_id: item for item in board if not item.archived}
    archived_complete = {item.ticket_id for item in board if item.archived or item.status == "done" or item.phase == "complete"}
    unresolved = [
        dep
        for dep in card.depends_on
        if dep not in card.dependency_waivers and not dependency_is_satisfied(dep, active_by_id, archived_complete)
    ]
    if unresolved:
        return Eligibility(card.ticket_id, False, "unresolved dependencies: " + ", ".join(unresolved), "stop", "", False)

    return Eligibility(card.ticket_id, True, f"eligible for {skill}", action, skill, False)


def sort_key(card: TicketCard) -> tuple[int, int, str]:
    return (
        PHASE_RANK.get(card.phase, 99),
        PRIORITY_RANK.get(card.priority.lower(), 50),
        card.ticket_id,
    )


def select_next_ticket(board: list[TicketCard]) -> dict[str, object]:
    active = [card for card in board if not card.archived]
    eligibilities = {card.ticket_id: eligible(card, board) for card in active}
    eligible_cards = [card for card in active if eligibilities[card.ticket_id].eligible]
    skipped = [
        asdict(eligibilities[card.ticket_id])
        for card in sorted(active, key=lambda item: item.ticket_id)
        if not eligibilities[card.ticket_id].eligible
    ]
    if not eligible_cards:
        human_gates = [item for item in skipped if item.get("needs_human")]
        reason = "human gate required" if human_gates else "no eligible tickets"
        return {
            "status": "stop",
            "selected_ticket_id": None,
            "selected_path": None,
            "action": "stop",
            "recommended_skill": None,
            "reason": reason,
            "skipped": skipped,
        }

    selected = sorted(eligible_cards, key=sort_key)[0]
    selected_eligibility = eligibilities[selected.ticket_id]
    return {
        "status": "selected",
        "selected_ticket_id": selected.ticket_id,
        "selected_path": selected.path,
        "action": selected_eligibility.action,
        "recommended_skill": selected_eligibility.recommended_skill,
        "reason": selected_eligibility.reason,
        "selected": asdict(selected),
        "skipped": skipped,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Select the next Ralph-eligible ticket without mutating the board.")
    parser.add_argument("--root", default=".", help="Repository root containing tickets/")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = select_next_ticket(load_board(Path(args.root)))
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        selected = result.get("selected_ticket_id") or "none"
        print(f"RALPH_SELECTOR_RESULT: status={result['status']} selected={selected} reason={result['reason']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
