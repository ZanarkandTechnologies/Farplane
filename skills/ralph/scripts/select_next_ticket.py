#!/usr/bin/env python3
"""Read-only selector for Codexter filesystem tickets."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
BIN_DIR = PROJECT_ROOT / "bin"
if str(BIN_DIR) not in sys.path:
    sys.path.insert(0, str(BIN_DIR))

from codexter_boards import BoardAdapterError, FileTicketAdapter, WorkItem
from codexter_compute import ComputeDecision, select_compute
from codexter_invocation import InvocationError, WorkflowPolicy, load_workflow


TICKET_ID_RE = re.compile(r"^TASK-\d{4}$")
PRIORITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}
DEFAULT_PHASE_ACTIONS = {
    "building": ("start_impl", "impl"),
    "documenting": ("start_closeout", "close-ticket"),
    "planning": ("start_planning", "impl-plan"),
}
PHASE_RANK = {"building": 0, "documenting": 1, "planning": 2}
TERMINAL_STATUSES = {"blocked", "done", "failed"}
DEFAULT_ACTIVE_PHASES = ("planning", "building", "documenting")
DEFAULT_COMPUTE_ALLOWED = ("local_shared", "local_worktree")


def archive_source_for_board_source(board_source: str) -> str:
    normalized = board_source.rstrip("/")
    if not normalized:
        return "archive"
    return f"{normalized}/archive"


@dataclass(frozen=True)
class RalphWorkflowPolicy:
    board_source: str = "tickets/"
    archive_source: str = "tickets/archive"
    active_phases: tuple[str, ...] = DEFAULT_ACTIVE_PHASES
    workflow_default_compute: str = "local_shared"
    workflow_allowed_compute: tuple[str, ...] = DEFAULT_COMPUTE_ALLOWED
    phase_actions: dict[str, tuple[str, str]] | None = None

    def action_for_phase(self, phase: str) -> tuple[str, str]:
        actions = self.phase_actions or DEFAULT_PHASE_ACTIONS
        return actions.get(phase, ("stop", ""))


@dataclass(frozen=True)
class RalphCandidate:
    item: WorkItem
    path: str
    archived: bool
    dependency_waivers: list[str]

    @property
    def ticket_id(self) -> str:
        return self.item.identifier

    @property
    def phase(self) -> str:
        return self.item.phase

    @property
    def status(self) -> str:
        return self.item.status

    @property
    def priority(self) -> str:
        return self.item.priority or "medium"

    @property
    def claimed_by(self) -> str:
        return str(self.item.metadata.get("claimed_by") or "").strip()

    @property
    def next_action(self) -> str:
        return str(self.item.metadata.get("next_action") or "").strip()

    def public_dict(self, *, compute: dict[str, object] | None = None) -> dict[str, object]:
        payload: dict[str, object] = {
            "ticket_id": self.ticket_id,
            "path": self.path,
            "phase": self.phase,
            "status": self.status,
            "priority": self.priority,
            "depends_on": list(self.item.depends_on),
            "blocked_by": list(self.item.blocked_by),
            "ready": self.item.ready,
            "approval_required": self.item.approval_required,
            "claimed_by": self.claimed_by,
            "next_action": self.next_action,
            "archived": self.archived,
            "dependency_waivers": self.dependency_waivers,
        }
        if compute is not None:
            payload["compute"] = compute
        return payload


@dataclass(frozen=True)
class RalphBoard:
    root: Path
    policy: RalphWorkflowPolicy
    active: list[RalphCandidate]
    archived: list[RalphCandidate]

    @property
    def all_candidates(self) -> list[RalphCandidate]:
        return [*self.active, *self.archived]

    @property
    def completed_ids(self) -> set[str]:
        return {
            candidate.ticket_id
            for candidate in self.all_candidates
            if candidate.archived
            or candidate.status == "done"
            or candidate.phase == "complete"
        }


@dataclass(frozen=True)
class Eligibility:
    ticket_id: str
    eligible: bool
    reason: str
    action: str
    recommended_skill: str
    needs_human: bool
    compute: dict[str, object] | None = None
    blocker_codes: list[str] | None = None
    required_setup: list[str] | None = None


def dependency_waivers(body: str) -> list[str]:
    waivers: set[str] = set()
    for line in body.splitlines():
        lowered = line.lower()
        if "waiv" not in lowered:
            continue
        for ticket_id in re.findall(r"TASK-\d{4}", line):
            waivers.add(ticket_id)
    return sorted(waivers)


def phase_actions_from_workflow(workflow: WorkflowPolicy) -> dict[str, tuple[str, str]]:
    actions: dict[str, tuple[str, str]] = {}
    for phase in DEFAULT_ACTIVE_PHASES:
        skill = workflow.routing.get(phase)
        default_action, _default_skill = DEFAULT_PHASE_ACTIONS[phase]
        if skill:
            actions[phase] = (default_action, skill)
    return actions or dict(DEFAULT_PHASE_ACTIONS)


def load_workflow_policy(root: Path) -> RalphWorkflowPolicy:
    workflow_path = root / "WORKFLOW.md"
    if not workflow_path.exists():
        return RalphWorkflowPolicy(phase_actions=dict(DEFAULT_PHASE_ACTIONS))
    workflow = load_workflow(workflow_path, root)
    return RalphWorkflowPolicy(
        board_source=workflow.board_source,
        archive_source=archive_source_for_board_source(workflow.board_source),
        active_phases=workflow.active_phases,
        workflow_default_compute=workflow.compute_default,
        workflow_allowed_compute=workflow.compute_allowed,
        phase_actions=phase_actions_from_workflow(workflow),
    )


def relative_ticket_path(path: str, root: Path) -> str:
    resolved_path = Path(path).resolve()
    resolved_root = root.resolve()
    try:
        return str(resolved_path.relative_to(resolved_root))
    except ValueError:
        return str(resolved_path)


def candidate_from_work_item(item: WorkItem, root: Path, *, archived: bool) -> RalphCandidate:
    return RalphCandidate(
        item=item,
        path=relative_ticket_path(item.local_ticket_path, root),
        archived=archived,
        dependency_waivers=dependency_waivers(item.description),
    )


def load_candidates(root: Path, source: str, *, archived: bool) -> list[RalphCandidate]:
    source_root = (root / source).resolve()
    if not source_root.exists():
        return []
    adapter = FileTicketAdapter(root, source)
    return [
        candidate_from_work_item(item, root, archived=archived)
        for item in adapter.list_candidates()
    ]


def load_board(root: Path, policy: RalphWorkflowPolicy | None = None) -> RalphBoard:
    resolved = root.resolve()
    effective_policy = policy or load_workflow_policy(resolved)
    active = load_candidates(resolved, effective_policy.board_source, archived=False)
    archived = load_candidates(resolved, effective_policy.archive_source, archived=True)
    return RalphBoard(root=resolved, policy=effective_policy, active=active, archived=archived)


def dependency_is_satisfied(
    dep: str, active_by_id: dict[str, RalphCandidate], completed_ids: set[str]
) -> bool:
    if dep in completed_ids:
        return True
    card = active_by_id.get(dep)
    if card is None:
        return False
    return card.status == "done" or card.phase == "complete"


def compute_for_candidate(
    candidate: RalphCandidate,
    board: RalphBoard,
    policy: RalphWorkflowPolicy,
) -> ComputeDecision:
    resolved_dependencies = tuple(
        dep
        for dep in candidate.item.depends_on
        if dep in candidate.dependency_waivers or dep in board.completed_ids
    )
    return select_compute(
        candidate.item,
        envelope_compute_target=None,
        phase=candidate.phase,
        workflow_default=policy.workflow_default_compute,
        workflow_allowed=policy.workflow_allowed_compute,
        root=board.root,
        resolved_dependencies=resolved_dependencies,
    )


def compute_requires_operator(compute: ComputeDecision) -> bool:
    operator_codes = {
        "disallowed_by_workflow",
        "missing_worktree_runtime",
        "unknown_target",
        "unsupported_target",
    }
    return any(code in operator_codes for code in compute.blocker_codes)


def eligible(candidate: RalphCandidate, board: RalphBoard) -> Eligibility:
    policy = board.policy
    action, skill = policy.action_for_phase(candidate.phase)
    card = candidate
    if card.archived:
        return Eligibility(card.ticket_id, False, "ticket is archived", "stop", "", False, None, [], [])
    if not TICKET_ID_RE.match(card.ticket_id):
        return Eligibility(card.ticket_id, False, "invalid ticket id", "stop", "", False, None, [], [])
    if card.status in TERMINAL_STATUSES or card.phase in {"complete", "failed"}:
        return Eligibility(
            card.ticket_id,
            False,
            f"terminal state phase={card.phase} status={card.status}",
            "stop",
            "",
            False,
            None,
            [],
            [],
        )
    if card.item.approval_required:
        return Eligibility(card.ticket_id, False, "approval required", "stop", "", True, None, [], [])
    if not card.item.ready:
        return Eligibility(card.ticket_id, False, "ready is false", "stop", "", False, None, [], [])
    if card.item.blocked_by:
        return Eligibility(
            card.ticket_id,
            False,
            "blocked by " + ", ".join(card.item.blocked_by),
            "stop",
            "",
            False,
            None,
            [],
            [],
        )
    if card.claimed_by:
        return Eligibility(card.ticket_id, False, f"claimed by {card.claimed_by}", "stop", "", False, None, [], [])
    if card.phase not in policy.active_phases:
        return Eligibility(
            card.ticket_id,
            False,
            f"unsupported phase {card.phase}",
            "stop",
            "",
            False,
            None,
            [],
            [],
        )
    if card.phase not in (policy.phase_actions or DEFAULT_PHASE_ACTIONS):
        return Eligibility(card.ticket_id, False, f"unsupported phase {card.phase}", "stop", "", False, None, [], [])

    active_by_id = {item.ticket_id: item for item in board.active}
    unresolved = [
        dep
        for dep in card.item.depends_on
        if dep not in card.dependency_waivers
        and not dependency_is_satisfied(dep, active_by_id, board.completed_ids)
    ]
    if unresolved:
        return Eligibility(
            card.ticket_id,
            False,
            "unresolved dependencies: " + ", ".join(unresolved),
            "stop",
            "",
            False,
            None,
            [],
            [],
        )

    compute = compute_for_candidate(card, board, policy)
    compute_payload = compute.public_dict()
    if not compute.allowed:
        return Eligibility(
            card.ticket_id,
            False,
            "compute blocked: " + compute.reason,
            "stop",
            "",
            compute_requires_operator(compute),
            compute_payload,
            list(compute.blocker_codes),
            list(compute.required_setup),
        )

    return Eligibility(
        card.ticket_id,
        True,
        f"eligible for {skill}",
        action,
        skill,
        False,
        compute_payload,
        list(compute.blocker_codes),
        list(compute.required_setup),
    )


def sort_key(card: RalphCandidate) -> tuple[int, int, str]:
    return (
        PHASE_RANK.get(card.phase, 99),
        PRIORITY_RANK.get(card.priority.lower(), 50),
        card.ticket_id,
    )


def select_next_ticket(board: RalphBoard) -> dict[str, object]:
    active = board.active
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
        "selected": selected.public_dict(compute=selected_eligibility.compute),
        "skipped": skipped,
    }


def selector_error_result(error: Exception) -> dict[str, object]:
    return {
        "status": "stop",
        "selected_ticket_id": None,
        "selected_path": None,
        "action": "stop",
        "recommended_skill": None,
        "reason": f"selector error: {error}",
        "skipped": [],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Select the next Ralph-eligible ticket without mutating the board.")
    parser.add_argument("--root", default=".", help="Repository root containing tickets/")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        result = select_next_ticket(load_board(Path(args.root)))
    except (BoardAdapterError, InvocationError) as exc:
        result = selector_error_result(exc)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        selected = result.get("selected_ticket_id") or "none"
        print(f"RALPH_SELECTOR_RESULT: status={result['status']} selected={selected} reason={result['reason']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
