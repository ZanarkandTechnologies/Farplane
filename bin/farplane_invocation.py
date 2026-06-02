#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, fields, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from farplane_boards import (
    COMPUTE_TARGETS,
    BoardAdapterError,
    FileTicketAdapter,
    WorkItem,
    WorkItemSelector,
    normalize_ticket_id as normalize_board_ticket_id,
)
from farplane_compute import ComputeDecision, select_compute

PHASES = ("planning", "building", "qa", "review", "documenting")
MODES = ("local_codex", "local_ralph", "symphony_worker", "external_runner")
VERDICTS = ("pass", "revise", "block", "failed")
# MEM-0077: this helper validates invocation contracts and proof artifacts only;
# normal Codex plus installed skills remains the execution surface.


class InvocationError(ValueError):
    pass


@dataclass(frozen=True)
class WorkflowPolicy:
    path: str
    name: str
    version: int
    prompt_template: str
    board_adapter: str
    board_source: str
    active_phases: tuple[str, ...]
    terminal_statuses: tuple[str, ...]
    compute_default: str
    compute_allowed: tuple[str, ...]
    ticket_override_field: str
    routing: dict[str, str]
    quality: dict[str, Any]


@dataclass(frozen=True)
class FarplaneRunEnvelope:
    workflow_path: str
    work_item_id: str | None
    work_item_path: str | None
    compute_target: str | None
    phase: str
    mode: str
    requested_by: str
    requested_at: str
    proof_packet_path: str

    def public_dict(self) -> dict[str, Any]:
        return {
            "workflowPath": self.workflow_path,
            "workItemId": self.work_item_id,
            "workItemPath": self.work_item_path,
            "computeTarget": self.compute_target,
            "phase": self.phase,
            "mode": self.mode,
            "requestedBy": self.requested_by,
            "requestedAt": self.requested_at,
            "proofPacketPath": self.proof_packet_path,
        }


@dataclass(frozen=True)
class SkillRoute:
    phase: str
    skill_name: str
    ticket_path: str
    handoff_prompt: str
    requires_approval_before_build: bool

    def public_dict(self) -> dict[str, Any]:
        return {
            "phase": self.phase,
            "skillName": self.skill_name,
            "ticketPath": self.ticket_path,
            "handoffPrompt": self.handoff_prompt,
            "requiresApprovalBeforeBuild": self.requires_approval_before_build,
        }


@dataclass(frozen=True)
class InvocationPlan:
    run_id: str
    status: str
    envelope: FarplaneRunEnvelope
    workflow: WorkflowPolicy
    work_item: WorkItem
    compute: ComputeDecision
    route: SkillRoute | None
    proof_packet_path: str
    generated_at: str


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_ticket_id(value: str) -> str:
    try:
        return normalize_board_ticket_id(value)
    except BoardAdapterError as exc:
        raise InvocationError(str(exc)) from exc


def parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if value in {"true", "false"}:
        return value == "true"
    if value == "[]":
        return []
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(part.strip()) for part in inner.split(",")]
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def parse_yaml_map(raw: str) -> dict[str, Any]:
    root: dict[str, Any] = {}
    lines = raw.splitlines()
    stack: list[tuple[int, Any]] = [(-1, root)]
    for line_no, original in enumerate(lines, 1):
        if not original.strip() or original.lstrip().startswith("#"):
            continue
        indent = len(original) - len(original.lstrip(" "))
        stripped = original.strip()
        if stripped.startswith("- "):
            while stack and indent <= stack[-1][0]:
                stack.pop()
            parent = stack[-1][1]
            if not isinstance(parent, list):
                raise InvocationError(f"list item has no list parent in front matter line {line_no}")
            parent.append(parse_scalar(stripped[2:].strip()))
            continue
        if ":" not in stripped:
            raise InvocationError(f"invalid front matter line {line_no}: {original!r}")
        key, raw_value = stripped.split(":", 1)
        key = key.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if not isinstance(parent, dict):
            raise InvocationError(f"mapping entry has no map parent in front matter line {line_no}")
        value = raw_value.strip()
        if value == "":
            has_nested_child = False
            next_child_is_list = False
            for later in lines[line_no:]:
                if not later.strip() or later.lstrip().startswith("#"):
                    continue
                later_indent = len(later) - len(later.lstrip(" "))
                has_nested_child = later_indent > indent
                next_child_is_list = later_indent > indent and later.strip().startswith("- ")
                break
            if not has_nested_child:
                parent[key] = ""
                continue
            child: Any = [] if next_child_is_list else {}
            parent[key] = child
            stack.append((indent, child))
        else:
            parent[key] = parse_scalar(value)
    return root


def parse_frontmatter_markdown(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text.strip()
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        raise InvocationError("missing closing front matter marker")
    config = parse_yaml_map(parts[0][4:])
    if not isinstance(config, dict):
        raise InvocationError("front matter must be a map")
    return config, parts[1].strip()


def require_map(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise InvocationError(f"{label} must be a map")
    return value


def require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InvocationError(f"{label} must be a non-empty string")
    return value.strip()


def string_list(value: Any, label: str, default: tuple[str, ...]) -> tuple[str, ...]:
    if value is None:
        return default
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise InvocationError(f"{label} must be a list of strings")
    return tuple(item.strip() for item in value if item.strip())


def resolve_path(path: str | Path, root: Path) -> Path:
    candidate = Path(path).expanduser()
    if not candidate.is_absolute():
        candidate = root / candidate
    return candidate.resolve()


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def load_workflow(path: str | Path, root: Path | None = None) -> WorkflowPolicy:
    resolved_root = root or project_root()
    workflow_path = resolve_path(path, resolved_root)
    if not workflow_path.exists():
        raise InvocationError(f"workflow file not found: {workflow_path}")
    config, prompt = parse_frontmatter_markdown(workflow_path.read_text(encoding="utf-8"))
    workflow = require_map(config.get("workflow", {}), "workflow")
    board = require_map(config.get("board", {}), "board")
    compute = require_map(config.get("compute", {}), "compute")
    routing = require_map(config.get("routing", {}), "routing")
    quality = require_map(config.get("quality", {}), "quality")

    name = require_string(workflow.get("name"), "workflow.name")
    version = workflow.get("version", 1)
    if not isinstance(version, int) or version <= 0:
        raise InvocationError("workflow.version must be a positive integer")
    board_adapter = require_string(board.get("adapter"), "board.adapter")
    if board_adapter != "filesystem":
        raise InvocationError(f"unsupported board.adapter: {board_adapter}")
    board_source = require_string(board.get("source", "tickets/"), "board.source")
    compute_default = require_string(compute.get("default", "local_shared"), "compute.default")
    compute_allowed = string_list(
        compute.get("allowed"), "compute.allowed", default=("local_shared",)
    )
    for target in (compute_default, *compute_allowed):
        if target not in COMPUTE_TARGETS:
            raise InvocationError(f"unknown compute target in workflow: {target}")
    normalized_routing: dict[str, str] = {}
    for phase, skill in routing.items():
        phase_name = str(phase).strip()
        if phase_name not in PHASES:
            raise InvocationError(f"unknown routing phase: {phase_name}")
        normalized_routing[phase_name] = require_string(skill, f"routing.{phase_name}")
    if not normalized_routing:
        raise InvocationError("routing must define at least one phase")
    return WorkflowPolicy(
        path=str(workflow_path),
        name=name,
        version=version,
        prompt_template=prompt,
        board_adapter=board_adapter,
        board_source=board_source,
        active_phases=string_list(
            board.get("active_phases"), "board.active_phases", default=("planning", "building")
        ),
        terminal_statuses=string_list(
            board.get("terminal_statuses"), "board.terminal_statuses", default=("done", "failed")
        ),
        compute_default=compute_default,
        compute_allowed=compute_allowed,
        ticket_override_field=require_string(
            compute.get("ticket_override_field", "compute_target"),
            "compute.ticket_override_field",
        ),
        routing=normalized_routing,
        quality=quality,
    )


def load_work_item(
    *,
    work_item_id: str | None = None,
    work_item_path: str | None = None,
    board_source: str = "tickets/",
    root: Path | None = None,
) -> WorkItem:
    resolved_root = root or project_root()
    try:
        adapter = FileTicketAdapter(resolved_root, board_source)
        return adapter.read_work_item(
            WorkItemSelector(work_item_id=work_item_id, work_item_path=work_item_path)
        )
    except BoardAdapterError as exc:
        raise InvocationError(str(exc)) from exc


def envelope_value(payload: dict[str, Any], camel: str, snake: str, default: Any = None) -> Any:
    if camel in payload:
        return payload[camel]
    return payload.get(snake, default)


def parse_run_envelope(source: str | Path, root: Path | None = None) -> FarplaneRunEnvelope:
    resolved_root = root or project_root()
    if isinstance(source, Path):
        raw = source.read_text(encoding="utf-8")
    else:
        text = source.strip()
        candidate = resolve_path(text, resolved_root) if text and not text.startswith("{") else None
        if candidate and candidate.exists():
            raw = candidate.read_text(encoding="utf-8")
        else:
            raw = text
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise InvocationError(f"run envelope must be JSON or a JSON file path: {exc}") from exc
    if not isinstance(payload, dict):
        raise InvocationError("run envelope must be a JSON object")
    workflow_path = require_string(
        envelope_value(payload, "workflowPath", "workflow_path", "WORKFLOW.md"),
        "workflowPath",
    )
    phase = require_string(envelope_value(payload, "phase", "phase", "planning"), "phase")
    if phase not in PHASES:
        raise InvocationError(f"unknown phase: {phase}")
    mode = require_string(envelope_value(payload, "mode", "mode", "local_codex"), "mode")
    if mode not in MODES:
        raise InvocationError(f"unknown mode: {mode}")
    proof_packet_path = require_string(
        envelope_value(payload, "proofPacketPath", "proof_packet_path"),
        "proofPacketPath",
    )
    compute_target = envelope_value(payload, "computeTarget", "compute_target")
    if compute_target is not None:
        compute_target = require_string(compute_target, "computeTarget")
    work_item_id = envelope_value(payload, "workItemId", "work_item_id")
    work_item_path = envelope_value(payload, "workItemPath", "work_item_path")
    if work_item_id is not None:
        work_item_id = normalize_ticket_id(str(work_item_id))
    if work_item_path is not None:
        work_item_path = require_string(work_item_path, "workItemPath")
    if not work_item_id and not work_item_path:
        raise InvocationError("run envelope must include workItemId or workItemPath")
    return FarplaneRunEnvelope(
        workflow_path=workflow_path,
        work_item_id=work_item_id,
        work_item_path=work_item_path,
        compute_target=compute_target,
        phase=phase,
        mode=mode,
        requested_by=require_string(
            envelope_value(payload, "requestedBy", "requested_by", "local-operator"),
            "requestedBy",
        ),
        requested_at=require_string(
            envelope_value(payload, "requestedAt", "requested_at", now_iso()),
            "requestedAt",
        ),
        proof_packet_path=proof_packet_path,
    )


def build_run_id(item: WorkItem, phase: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{item.identifier.lower()}-{phase}-{stamp}"


def resolve_proof_path(path: str, item: WorkItem, root: Path) -> Path:
    resolved = resolve_path(path, root)
    allowed_roots = [
        (root / ".harness" / "results").resolve(),
        Path(item.artifacts_path).resolve(),
    ]
    if not any(is_under(resolved, allowed_root) for allowed_root in allowed_roots):
        raise InvocationError(
            "proofPacketPath must stay under .harness/results/ or the ticket artifacts directory"
        )
    if resolved.suffix != ".json":
        raise InvocationError("proofPacketPath must end in .json")
    return resolved


def route_phase(
    item: WorkItem, envelope: FarplaneRunEnvelope, policy: WorkflowPolicy
) -> SkillRoute | None:
    skill_name = policy.routing.get(envelope.phase)
    if not skill_name:
        return None
    prompt = (
        f"Use `${skill_name}` for {item.identifier}: {item.title}. "
        f"Ticket: {item.local_ticket_path}. Keep ticket evidence updated and write the requested ProofPacket."
    )
    return SkillRoute(
        phase=envelope.phase,
        skill_name=skill_name,
        ticket_path=item.local_ticket_path,
        handoff_prompt=prompt,
        requires_approval_before_build=envelope.phase != "planning" and item.approval_required,
    )


def prepare_invocation(
    envelope: FarplaneRunEnvelope, root: Path | None = None
) -> InvocationPlan:
    resolved_root = root or project_root()
    workflow = load_workflow(envelope.workflow_path, resolved_root)
    item = load_work_item(
        work_item_id=envelope.work_item_id,
        work_item_path=envelope.work_item_path,
        board_source=workflow.board_source,
        root=resolved_root,
    )
    proof_path = resolve_proof_path(envelope.proof_packet_path, item, resolved_root)
    compute = select_compute(
        item,
        envelope_compute_target=envelope.compute_target,
        phase=envelope.phase,
        workflow_default=workflow.compute_default,
        workflow_allowed=workflow.compute_allowed,
        root=resolved_root,
    )
    route = route_phase(item, envelope, workflow)
    blockers = list(compute.blockers)
    if route is None:
        blockers.append(f"no route configured for phase {envelope.phase}")
    status = "ready" if not blockers else "blocked"
    return InvocationPlan(
        run_id=build_run_id(item, envelope.phase),
        status=status,
        envelope=envelope,
        workflow=workflow,
        work_item=item,
        compute=compute,
        route=route,
        proof_packet_path=str(proof_path),
        generated_at=now_iso(),
    )


def dataclass_json(value: Any) -> Any:
    if hasattr(value, "public_dict"):
        return value.public_dict()
    if is_dataclass(value):
        return {
            item.name: dataclass_json(getattr(value, item.name))
            for item in fields(value)
            if getattr(value, item.name) is not None
        }
    if isinstance(value, tuple):
        return [dataclass_json(item) for item in value]
    if isinstance(value, dict):
        return {key: dataclass_json(item) for key, item in value.items()}
    return value


def build_proof_packet(
    *,
    plan: InvocationPlan,
    verdict: str,
    next_action: str,
    phase_status: str,
    artifacts: tuple[str, ...] = (),
    commands: tuple[str, ...] = (),
) -> dict[str, Any]:
    if verdict not in VERDICTS:
        raise InvocationError(f"invalid verdict: {verdict}")
    phase_result = {
        "status": phase_status,
        "skill": plan.route.skill_name if plan.route else None,
        "completedAt": now_iso(),
    }
    return {
        "schemaVersion": 1,
        "runId": plan.run_id,
        "workItem": {
            "source": plan.work_item.source,
            "id": plan.work_item.id,
            "identifier": plan.work_item.identifier,
            "title": plan.work_item.title,
            "path": plan.work_item.local_ticket_path,
            "url": plan.work_item.url,
        },
        "compute": dataclass_json(plan.compute),
        "phases": {plan.envelope.phase: phase_result},
        "artifacts": list(artifacts),
        "commands": list(commands),
        "verdict": verdict,
        "nextAction": next_action,
        "completedAt": now_iso(),
    }


def write_proof_packet(packet: dict[str, Any], path: str | Path) -> dict[str, Any]:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")
    return packet


def print_json(payload: Any) -> None:
    print(json.dumps(dataclass_json(payload), indent=2))


def build_envelope_from_args(args: argparse.Namespace) -> FarplaneRunEnvelope:
    ticket_id = normalize_ticket_id(args.ticket) if args.ticket else None
    proof_path = args.proof or f".harness/results/{(ticket_id or 'farplane').lower()}-{args.phase}.proof.json"
    return FarplaneRunEnvelope(
        workflow_path=args.workflow,
        work_item_id=ticket_id,
        work_item_path=args.ticket_path,
        compute_target=args.compute,
        phase=args.phase,
        mode=args.mode,
        requested_by=args.requested_by,
        requested_at=now_iso(),
        proof_packet_path=proof_path,
    )


def cmd_prepare(args: argparse.Namespace) -> int:
    root = resolve_path(args.root, Path.cwd())
    envelope = parse_run_envelope(args.envelope, root) if args.envelope else build_envelope_from_args(args)
    plan = prepare_invocation(envelope, root)
    print_json(plan)
    return 0 if plan.status == "ready" else 2


def cmd_write_proof(args: argparse.Namespace) -> int:
    root = resolve_path(args.root, Path.cwd())
    envelope = build_envelope_from_args(args)
    plan = prepare_invocation(envelope, root)
    packet = build_proof_packet(
        plan=plan,
        verdict=args.verdict,
        next_action=args.next_action,
        phase_status=args.phase_status,
        artifacts=tuple(args.artifact),
        commands=tuple(args.command_text),
    )
    write_proof_packet(packet, plan.proof_packet_path)
    print_json(packet)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate Farplane invocation contracts.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_common(target: argparse.ArgumentParser) -> None:
        target.add_argument("--root", default=".", help="Farplane project root")
        target.add_argument("--workflow", default="WORKFLOW.md")
        target.add_argument("--ticket", default="")
        target.add_argument("--ticket-path", default=None)
        target.add_argument("--phase", choices=PHASES, default="planning")
        target.add_argument("--compute", choices=COMPUTE_TARGETS, default=None)
        target.add_argument("--mode", choices=MODES, default="local_codex")
        target.add_argument("--requested-by", default="local-operator")
        target.add_argument("--proof", default="")

    prepare = subparsers.add_parser("prepare")
    add_common(prepare)
    prepare.add_argument("--envelope", default="", help="Inline JSON envelope or path to JSON")
    prepare.set_defaults(func=cmd_prepare)

    proof = subparsers.add_parser("write-proof")
    add_common(proof)
    proof.add_argument("--verdict", choices=VERDICTS, required=True)
    proof.add_argument("--next-action", required=True)
    proof.add_argument("--phase-status", default="completed")
    proof.add_argument("--artifact", action="append", default=[])
    proof.add_argument("--command-text", action="append", default=[])
    proof.set_defaults(func=cmd_write_proof)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return int(args.func(args))
    except InvocationError as exc:
        print(f"farplane invocation error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
