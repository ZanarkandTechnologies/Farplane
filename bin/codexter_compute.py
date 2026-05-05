#!/usr/bin/env python3
"""Compute admission policy for Codexter work items."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from codexter_boards import COMPUTE_TARGETS


LOCAL_COMPUTE_TARGETS = ("local_shared", "local_worktree")
FUTURE_COMPUTE_TARGETS = ("symphony", "codex_cloud")
PHASES_WITHOUT_HUMAN_GATE = ("planning",)


class ComputePolicyError(ValueError):
    """Raised when compute policy cannot be evaluated."""


class ComputeWorkItem(Protocol):
    identifier: str
    approval_required: bool
    blocked_by: tuple[str, ...]
    depends_on: tuple[str, ...]
    status: str
    compute_target: str | None


@dataclass(frozen=True)
class ComputeCapability:
    target: str
    implemented: bool
    isolation: str
    requires_worktree: bool
    requires_external_runner: bool
    requires_runtime_record: bool
    setup_hint: str
    handoff: str

    def public_dict(self) -> dict[str, Any]:
        return {
            "target": self.target,
            "implemented": self.implemented,
            "isolation": self.isolation,
            "requiresWorktree": self.requires_worktree,
            "requiresExternalRunner": self.requires_external_runner,
            "requiresRuntimeRecord": self.requires_runtime_record,
            "setupHint": self.setup_hint,
            "handoff": self.handoff,
        }


@dataclass(frozen=True)
class ComputeDecision:
    target: str
    reason: str
    allowed: bool
    blockers: tuple[str, ...]
    blocker_codes: tuple[str, ...]
    runtime_record_path: str | None
    runtime_hints: tuple[str, ...]
    required_setup: tuple[str, ...]
    handoff: str
    capability: ComputeCapability

    def public_dict(self) -> dict[str, Any]:
        return {
            "target": self.target,
            "reason": self.reason,
            "allowed": self.allowed,
            "blockers": list(self.blockers),
            "blockerCodes": list(self.blocker_codes),
            "runtimeRecordPath": self.runtime_record_path,
            "runtimeHints": list(self.runtime_hints),
            "requiredSetup": list(self.required_setup),
            "handoff": self.handoff,
            "capability": self.capability.public_dict(),
        }


CAPABILITIES: dict[str, ComputeCapability] = {
    "local_shared": ComputeCapability(
        target="local_shared",
        implemented=True,
        isolation="current checkout",
        requires_worktree=False,
        requires_external_runner=False,
        requires_runtime_record=False,
        setup_hint="normal Codex session in the current checkout",
        handoff="route to the selected Codexter phase skill in this workspace",
    ),
    "local_worktree": ComputeCapability(
        target="local_worktree",
        implemented=True,
        isolation="ticket-scoped isolated checkout",
        requires_worktree=True,
        requires_external_runner=False,
        requires_runtime_record=True,
        setup_hint=(
            "prepare .harness/state/tickets/<ticket>.runtime.json with "
            "bin/ticket_runtime.py ensure or pr-runtime"
        ),
        handoff="route to the selected Codexter phase skill after the runtime record exists",
    ),
    "symphony": ComputeCapability(
        target="symphony",
        implemented=False,
        isolation="external Symphony-managed workspace",
        requires_worktree=False,
        requires_external_runner=True,
        requires_runtime_record=False,
        setup_hint="requires a Symphony integration shim and external scheduler",
        handoff="external runner must launch normal Codex with Codexter installed",
    ),
    "codex_cloud": ComputeCapability(
        target="codex_cloud",
        implemented=False,
        isolation="Codex cloud task workspace",
        requires_worktree=False,
        requires_external_runner=True,
        requires_runtime_record=False,
        setup_hint="requires a cloud task adapter and proof packet handoff",
        handoff="external cloud adapter must launch normal Codex with Codexter installed",
    ),
}


def runtime_record_path(ticket_id: str, root: Path) -> Path:
    return root / ".harness" / "state" / "tickets" / f"{ticket_id}.runtime.json"


def select_compute(
    item: ComputeWorkItem,
    *,
    envelope_compute_target: str | None,
    phase: str,
    workflow_default: str,
    workflow_allowed: tuple[str, ...],
    root: Path,
    resolved_dependencies: tuple[str, ...] = (),
) -> ComputeDecision:
    target = envelope_compute_target or item.compute_target or workflow_default or "local_shared"
    blockers: list[str] = []
    blocker_codes: list[str] = []
    runtime_hints: list[str] = []
    required_setup: list[str] = []
    runtime_path: str | None = None

    if target not in COMPUTE_TARGETS:
        capability = ComputeCapability(
            target=target,
            implemented=False,
            isolation="unknown",
            requires_worktree=False,
            requires_external_runner=False,
            requires_runtime_record=False,
            setup_hint="choose one of local_shared, local_worktree, symphony, or codex_cloud",
            handoff="none",
        )
        blockers.append(f"unknown compute target: {target}")
        blocker_codes.append("unknown_target")
    else:
        capability = CAPABILITIES[target]

    if target not in workflow_allowed:
        blockers.append(f"compute target {target} is not allowed by WORKFLOW.md")
        blocker_codes.append("disallowed_by_workflow")

    if target in FUTURE_COMPUTE_TARGETS:
        blockers.append(
            f"compute target {target} requires a future external adapter and is not implemented locally"
        )
        blocker_codes.append("unsupported_target")

    if phase not in PHASES_WITHOUT_HUMAN_GATE:
        if item.approval_required:
            blockers.append("ticket requires approval before non-planning execution")
            blocker_codes.append("approval_required")
        if item.blocked_by:
            blockers.append(f"ticket has blockers: {', '.join(item.blocked_by)}")
            blocker_codes.append("blocked_ticket")
        if item.status == "blocked":
            blockers.append("ticket status is blocked")
            blocker_codes.append("blocked_ticket")
        unresolved = tuple(dep for dep in item.depends_on if dep not in resolved_dependencies)
        if unresolved:
            blockers.append(f"ticket has unresolved dependencies: {', '.join(unresolved)}")
            blocker_codes.append("dependency_unmet")

    if target == "local_worktree":
        runtime_path_obj = runtime_record_path(item.identifier, root)
        runtime_path = str(runtime_path_obj)
        runtime_hints.append("local_worktree requires an existing ticket runtime record")
        required_setup.append(
            "python3 bin/ticket_runtime.py ensure "
            f"--ticket {item.identifier} "
            "--checkout-mode worktree "
            "--runtime-mode branch-runtime "
            "--create-worktree --json"
        )
        if not runtime_path_obj.exists():
            blockers.append(f"missing local_worktree runtime record: {runtime_path_obj}")
            blocker_codes.append("missing_worktree_runtime")

    if target == "local_shared":
        runtime_hints.append("runs in the current checkout; no runtime record required")

    if target in FUTURE_COMPUTE_TARGETS:
        runtime_hints.append(capability.setup_hint)

    seen_codes: list[str] = []
    for code in blocker_codes:
        if code not in seen_codes:
            seen_codes.append(code)

    allowed = not blockers
    reason = "allowed compute target" if allowed else "; ".join(blockers)
    return ComputeDecision(
        target=target,
        reason=reason,
        allowed=allowed,
        blockers=tuple(blockers),
        blocker_codes=tuple(seen_codes),
        runtime_record_path=runtime_path,
        runtime_hints=tuple(runtime_hints),
        required_setup=tuple(required_setup),
        handoff=capability.handoff,
        capability=capability,
    )
