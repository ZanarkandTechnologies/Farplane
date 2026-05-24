#!/usr/bin/env python3
"""Validate skill capability fixtures and route broken skills to repair tickets."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


CAPABILITY_KINDS = {
    "mcp_query",
    "local_script",
    "file_contract",
    "generated_registry",
    "external_connector",
}
RECOVERY_DECISIONS = {"continue", "fallback", "repair_ticket", "escalate", "no_action"}
PRIORITIES = {"low", "medium", "high"}
VALUE_COSTS = {"low", "medium", "high"}
VALUE_CONFIDENCE = {"low", "medium", "high"}
ACTION_POLICIES = {"auto_ticket", "recommend", "ask"}
FALLBACK_METHODS = {
    "exact_view_query",
    "mcp_data_source_query",
    "local_token_mcp_data_source_query",
    "connector_unavailable",
    "local_filesystem_board",
}
FORBIDDEN_ACTIONS = {
    "mutate_notion_status",
    "publish",
    "deploy",
    "spend_money",
    "destructive_cleanup",
}
TICKET_ID_RE = re.compile(r"^TASK-(\d{4})$")


class CapabilityError(ValueError):
    """Raised when a capability fixture is invalid."""


@dataclass(frozen=True)
class SkillCapability:
    skill: str
    operation: str
    kind: str
    expected: str
    observed_failure: str
    expected_recovery: tuple[str, ...]
    forbidden_actions: tuple[str, ...]
    fallback_methods: tuple[str, ...]
    priority_hint: str
    user_value_reason: str
    evidence_refs: tuple[str, ...]
    path: str

    @property
    def capability_id(self) -> str:
        return f"{self.skill}.{self.operation}"


@dataclass(frozen=True)
class SkillCapabilityResult:
    capability_id: str
    passed: bool
    decision: tuple[str, ...]
    errors: tuple[str, ...]
    fixture_path: str


@dataclass(frozen=True)
class SkillFailurePacket:
    skill: str
    operation: str
    invoked_from: str
    expected: str
    observed: str
    failure_class: str
    safe_local_fix_available: bool
    suggested_ticket_title: str
    suggested_owner_skill: str
    evidence_refs: tuple[str, ...]
    forbidden_actions: tuple[str, ...]


@dataclass(frozen=True)
class UserValueSignal:
    name: str
    goal_ref: str
    repeated_failure_count: int
    blocked_workflows: tuple[str, ...]
    affected_skills: tuple[str, ...]
    manual_intervention_cost: str
    confidence: str
    expected_action_policy: str
    path: str


@dataclass(frozen=True)
class UserValueResult:
    name: str
    action_policy: str
    passed: bool
    reasons: tuple[str, ...]
    fixture_path: str


def repo_root(start: Path) -> Path:
    for candidate in [start.resolve(), *start.resolve().parents]:
        if (candidate / "docs/skills/README.md").exists() and (candidate / "tickets").exists():
            return candidate
    raise CapabilityError("could not find Codexter repo root")


REPO_ROOT = repo_root(Path(__file__).resolve())


def read_json(path: Path) -> dict[str, Any]:
    try:
        raw = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise CapabilityError(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(raw, dict):
        raise CapabilityError(f"{path}: fixture must be a JSON object")
    return raw


def require_string(raw: dict[str, Any], field: str, path: Path) -> str:
    value = raw.get(field)
    if not isinstance(value, str) or not value.strip():
        raise CapabilityError(f"{path}: {field} must be a non-empty string")
    return value.strip()


def string_tuple(raw: dict[str, Any], field: str, path: Path) -> tuple[str, ...]:
    value = raw.get(field, [])
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise CapabilityError(f"{path}: {field} must be a list of non-empty strings")
    return tuple(item.strip() for item in value)


def validate_capability(raw: dict[str, Any], path: Path) -> SkillCapability:
    kind = require_string(raw, "kind", path)
    if kind not in CAPABILITY_KINDS:
        raise CapabilityError(f"{path}: unsupported kind: {kind}")
    expected_recovery = string_tuple(raw, "expected_recovery", path)
    unknown_recovery = sorted(set(expected_recovery) - RECOVERY_DECISIONS)
    if unknown_recovery:
        raise CapabilityError(f"{path}: unsupported expected_recovery: {unknown_recovery}")
    forbidden_actions = string_tuple(raw, "forbidden_actions", path)
    priority_hint = require_string(raw, "priority_hint", path)
    if priority_hint not in PRIORITIES:
        raise CapabilityError(f"{path}: priority_hint must be one of {sorted(PRIORITIES)}")
    unknown_forbidden = sorted(set(forbidden_actions) - FORBIDDEN_ACTIONS)
    if unknown_forbidden:
        raise CapabilityError(f"{path}: unsupported forbidden_actions: {unknown_forbidden}")
    fallback_methods = string_tuple(raw, "fallback_methods", path) if "fallback_methods" in raw else ()
    unknown_fallbacks = sorted(set(fallback_methods) - FALLBACK_METHODS)
    if unknown_fallbacks:
        raise CapabilityError(f"{path}: unsupported fallback_methods: {unknown_fallbacks}")
    return SkillCapability(
        skill=require_string(raw, "skill", path),
        operation=require_string(raw, "operation", path),
        kind=kind,
        expected=require_string(raw, "expected", path),
        observed_failure=str(raw.get("observed_failure", "")).strip(),
        expected_recovery=expected_recovery,
        forbidden_actions=forbidden_actions,
        fallback_methods=fallback_methods,
        priority_hint=priority_hint,
        user_value_reason=require_string(raw, "user_value_reason", path),
        evidence_refs=string_tuple(raw, "evidence_refs", path),
        path=str(path),
    )


def capability_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    tests_root = root / "tests"
    if tests_root.exists():
        paths.extend(
            path
            for path in tests_root.glob("*/*.json")
            if path.parent.name != "value-signals"
        )
    skills_root = root / "skills"
    if skills_root.exists():
        paths.extend(skills_root.glob("*/tests/*.json"))
    return sorted(paths)


def load_capabilities(root: Path) -> list[SkillCapability]:
    return [validate_capability(read_json(path), path) for path in capability_paths(root)]


def find_capability(root: Path, skill: str, operation: str) -> SkillCapability:
    for fixture in load_capabilities(root):
        if fixture.skill == skill and fixture.operation == operation:
            return fixture
    raise CapabilityError(f"no capability fixture found for {skill}.{operation}")


def score_capability(fixture: SkillCapability) -> SkillCapabilityResult:
    errors: list[str] = []
    if fixture.observed_failure and "repair_ticket" not in fixture.expected_recovery:
        errors.append("observed_failure is present but expected_recovery omits repair_ticket")
    if "fallback" in fixture.expected_recovery and not fixture.observed_failure:
        errors.append("fallback recovery should explain the observed failure")
    if "repair_ticket" in fixture.expected_recovery and not fixture.evidence_refs:
        errors.append("repair_ticket recovery requires evidence_refs")
    if "fallback" in fixture.expected_recovery and fixture.fallback_methods:
        if fixture.fallback_methods[-1] not in {"connector_unavailable", "local_filesystem_board"}:
            errors.append("fallback_methods should end with connector_unavailable or local_filesystem_board")
    passed = not errors
    return SkillCapabilityResult(
        capability_id=fixture.capability_id,
        passed=passed,
        decision=fixture.expected_recovery,
        errors=tuple(errors),
        fixture_path=fixture.path,
    )


def classify_failure(fixture: SkillCapability) -> str:
    text = fixture.observed_failure.lower()
    if "not found" in text and "query" in text:
        return "connector_contract_mismatch"
    if "auth" in text or "permission" in text:
        return "auth_or_permission"
    if "missing" in text or "not found" in text:
        return "tool_missing"
    if "wrapper gap" in text:
        return "wrapper_gap"
    return "stale_registry"


def failure_packet(fixture: SkillCapability, invoked_from: str) -> SkillFailurePacket:
    observed = fixture.observed_failure or "expected skill behavior did not pass sanity check"
    title = f"fix {fixture.skill} {fixture.operation} behavior"
    safe_local = "repair_ticket" in fixture.expected_recovery and classify_failure(fixture) not in {
        "auth_or_permission"
    }
    return SkillFailurePacket(
        skill=fixture.skill,
        operation=fixture.operation,
        invoked_from=invoked_from,
        expected=fixture.expected,
        observed=observed,
        failure_class=classify_failure(fixture),
        safe_local_fix_available=safe_local,
        suggested_ticket_title=title,
        suggested_owner_skill=fixture.skill,
        evidence_refs=fixture.evidence_refs,
        forbidden_actions=fixture.forbidden_actions,
    )


def slug_ticket_title(title: str) -> str:
    return title.replace("`", "").strip()


def next_ticket_id(tickets_root: Path) -> str:
    max_id = 0
    for path in tickets_root.glob("TASK-*"):
        match = TICKET_ID_RE.fullmatch(path.name)
        if match:
            max_id = max(max_id, int(match.group(1)))
    return f"TASK-{max_id + 1:04d}"


def ticket_contains_packet(path: Path, packet: SkillFailurePacket) -> bool:
    text = path.read_text()
    marker = f"skill={packet.skill}; operation={packet.operation}; failure_class={packet.failure_class}"
    return marker in text


def find_existing_repair_ticket(root: Path, packet: SkillFailurePacket) -> Path | None:
    for path in sorted((root / "tickets").glob("TASK-*/ticket.md")):
        if ticket_contains_packet(path, packet):
            return path
    return None


def render_repair_ticket(ticket_id: str, packet: SkillFailurePacket) -> str:
    refs = "\n".join(f"- `{ref}`" for ref in packet.evidence_refs)
    forbidden = ", ".join(f"`{action}`" for action in packet.forbidden_actions)
    title = slug_ticket_title(packet.suggested_ticket_title)
    return f"""---
ticket_id: {ticket_id}
title: {title}
phase: planning
status: review
owner: unassigned
claimed_by:
priority: high
depends_on: []
blocked_by: []
ready: false
approval_required: true
requires_qa: false
requires_demo: false
created_at: 2026-05-21T00:00:00+08:00
updated_at: 2026-05-21T00:00:00+08:00
next_action: review the skill failure packet and approve the repair plan
last_verification: generated by bin/check_skill_capabilities.py from a failed skill fixture
---

# {ticket_id}: {title}

## Summary
Repair `{packet.skill}.{packet.operation}` because it failed its advertised skill behavior.
The observed failure was `{packet.observed}`.

## Scope
- In:
  - update the owning skill, wrapper, registry, or tests needed to make the operation reliable
  - preserve a fallback when the external connector is unavailable
- Out:
  - forbidden actions: {forbidden}

## Skill Failure Packet
- `skill`: `{packet.skill}`
- `operation`: `{packet.operation}`
- `invoked_from`: `{packet.invoked_from}`
- `expected`: `{packet.expected}`
- `observed`: `{packet.observed}`
- `failure_class`: `{packet.failure_class}`
- `safe_local_fix_available`: `{packet.safe_local_fix_available}`
- `marker`: `skill={packet.skill}; operation={packet.operation}; failure_class={packet.failure_class}`

## Plan
- `Change:` repair the skill behavior or wrapper path that produced the failure.
- `Why:` users should not have to debug broken harness skills after invoking them.
- `Before -> After:` before, the skill fails and leaves the caller blocked; after, the skill either works or returns an explicit fallback/escalation.
- `Touch:` owning skill files, matching tests, and registry/docs if needed.
- `Inspect:` evidence refs below and the current skill implementation.
- `Signature delta:` to be filled by `impl-plan`.
- `Type Sketch:` to be filled by `impl-plan`.
- `Typed flow example:` to be filled by `impl-plan`.
- `Execution steps:` run `impl-plan`, implement the repair, run the capability checker, and run review.
- `Recommendation:` use the existing ticket pipeline; do not patch hidden state.
- `Blast radius:` skill callers and automations that depend on this operation.
- `Risks:` masking external connector outages as local skill success.

## Acceptance Criteria
- [ ] The skill operation either succeeds or returns a documented fallback/escalation.
- [ ] The matching skill capability fixture passes.
- [ ] The repair does not perform forbidden actions.

## Verification
- `Tests:` `python3 bin/check_skill_capabilities.py score --skill {packet.skill} --operation {packet.operation}`
- `Manual checks:` inspect fallback and forbidden-action handling.
- `Evidence required:` checker output and review artifact.

## Proof Contract
- `Metrics:`
  - `Primary metric:` skill_capability_sanity_pass_rate
  - `Direction:` higher
  - `Verify:` capability checker
  - `Guard:` ticket metadata check
  - `Min acceptable result:` fixture passes for `{packet.skill}.{packet.operation}`
  - `Autoresearch warranted:` no
  - `Autoresearch session:` none
- `Review Rubrics:`
  - `integration-readiness >= 4.0`
  - `evidence-quality >= 4.0`
- `Required Evidence:`
  - capability checker output
  - review result

## Refs
{refs}

## Evidence
- `Artifacts:`
- `Commands:`
- `Result summary:`

## Blockers
- none
"""


def write_repair_ticket(root: Path, packet: SkillFailurePacket) -> Path:
    existing = find_existing_repair_ticket(root, packet)
    if existing is not None:
        return existing
    ticket_id = next_ticket_id(root / "tickets")
    ticket_dir = root / "tickets" / ticket_id
    ticket_dir.mkdir(parents=True, exist_ok=False)
    ticket_path = ticket_dir / "ticket.md"
    ticket_path.write_text(render_repair_ticket(ticket_id, packet))
    return ticket_path


def value_signal_paths(root: Path) -> list[Path]:
    value_root = root / "tests" / "value-signals"
    if not value_root.exists():
        return []
    return sorted(value_root.glob("*.json"))


def validate_value_signal(raw: dict[str, Any], path: Path) -> UserValueSignal:
    cost = require_string(raw, "manual_intervention_cost", path)
    confidence = require_string(raw, "confidence", path)
    expected = require_string(raw, "expected_action_policy", path)
    if cost not in VALUE_COSTS:
        raise CapabilityError(f"{path}: unsupported manual_intervention_cost: {cost}")
    if confidence not in VALUE_CONFIDENCE:
        raise CapabilityError(f"{path}: unsupported confidence: {confidence}")
    if expected not in ACTION_POLICIES:
        raise CapabilityError(f"{path}: unsupported expected_action_policy: {expected}")
    repeated = raw.get("repeated_failure_count")
    if not isinstance(repeated, int) or repeated < 0:
        raise CapabilityError(f"{path}: repeated_failure_count must be a non-negative integer")
    return UserValueSignal(
        name=require_string(raw, "name", path),
        goal_ref=str(raw.get("goal_ref", "")).strip(),
        repeated_failure_count=repeated,
        blocked_workflows=string_tuple(raw, "blocked_workflows", path),
        affected_skills=tuple(str(item).strip() for item in raw.get("affected_skills", []) if str(item).strip()),
        manual_intervention_cost=cost,
        confidence=confidence,
        expected_action_policy=expected,
        path=str(path),
    )


def decide_value_policy(signal: UserValueSignal) -> tuple[str, tuple[str, ...]]:
    reasons: list[str] = []
    if signal.confidence == "high":
        reasons.append("high confidence")
    if signal.manual_intervention_cost == "high":
        reasons.append("high manual intervention cost")
    if signal.repeated_failure_count >= 2:
        reasons.append("repeated failure")
    if signal.affected_skills:
        reasons.append("known affected skill")

    if (
        signal.confidence == "high"
        and signal.manual_intervention_cost in {"medium", "high"}
        and (signal.repeated_failure_count >= 2 or signal.affected_skills)
    ):
        return "auto_ticket", tuple(reasons)
    if signal.confidence == "medium":
        return "recommend", tuple(reasons or ["medium confidence"])
    return "ask", tuple(reasons or ["low confidence or ambiguous priority"])


def score_value_signal(signal: UserValueSignal) -> UserValueResult:
    policy, reasons = decide_value_policy(signal)
    return UserValueResult(
        name=signal.name,
        action_policy=policy,
        passed=policy == signal.expected_action_policy,
        reasons=reasons,
        fixture_path=signal.path,
    )


def print_json(value: Any) -> None:
    if hasattr(value, "__dataclass_fields__"):
        value = asdict(value)
    elif isinstance(value, list):
        value = [asdict(item) if hasattr(item, "__dataclass_fields__") else item for item in value]
    print(json.dumps(value, indent=2, sort_keys=True))


def command_list(args: argparse.Namespace) -> int:
    fixtures = load_capabilities(REPO_ROOT)
    rows = [
        {
            "skill": fixture.skill,
            "operation": fixture.operation,
            "kind": fixture.kind,
            "priority_hint": fixture.priority_hint,
            "path": fixture.path,
        }
        for fixture in fixtures
    ]
    if args.json:
        print_json(rows)
    else:
        for row in rows:
            print(f"{row['skill']}.{row['operation']} ({row['kind']}) {row['path']}")
    return 0


def command_validate(_args: argparse.Namespace) -> int:
    capabilities = load_capabilities(REPO_ROOT)
    value_signals = [
        validate_value_signal(read_json(path), path)
        for path in value_signal_paths(REPO_ROOT)
    ]
    print(f"skill capability fixtures OK ({len(capabilities)} capabilities, {len(value_signals)} value signals)")
    return 0


def command_score(args: argparse.Namespace) -> int:
    fixture = find_capability(REPO_ROOT, args.skill, args.operation)
    result = score_capability(fixture)
    print_json(result)
    return 0 if result.passed else 1


def command_failure_packet(args: argparse.Namespace) -> int:
    fixture = find_capability(REPO_ROOT, args.skill, args.operation)
    packet = failure_packet(fixture, args.invoked_from)
    print_json(packet)
    return 0


def command_create_repair_ticket(args: argparse.Namespace) -> int:
    fixture = find_capability(REPO_ROOT, args.skill, args.operation)
    packet = failure_packet(fixture, args.invoked_from)
    if args.dry_run:
        ticket_id = next_ticket_id(REPO_ROOT / "tickets")
        print(render_repair_ticket(ticket_id, packet))
        return 0
    path = write_repair_ticket(REPO_ROOT, packet)
    print(path)
    return 0


def command_score_value(args: argparse.Namespace) -> int:
    paths = value_signal_paths(REPO_ROOT)
    if args.name:
        paths = [path for path in paths if path.stem == args.name or read_json(path).get("name") == args.name]
    if not paths:
        raise CapabilityError("no matching value signal fixtures")
    results = [
        score_value_signal(validate_value_signal(read_json(path), path))
        for path in paths
    ]
    print_json(results if len(results) != 1 else results[0])
    return 0 if all(result.passed for result in results) else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="list capability fixtures")
    list_parser.add_argument("--json", action="store_true")
    list_parser.set_defaults(func=command_list)

    validate_parser = subparsers.add_parser("validate", help="validate fixtures")
    validate_parser.set_defaults(func=command_validate)

    score_parser = subparsers.add_parser("score", help="score one capability fixture")
    score_parser.add_argument("--skill", required=True)
    score_parser.add_argument("--operation", required=True)
    score_parser.set_defaults(func=command_score)

    packet_parser = subparsers.add_parser("failure-packet", help="render a failure packet")
    packet_parser.add_argument("--skill", required=True)
    packet_parser.add_argument("--operation", required=True)
    packet_parser.add_argument("--invoked-from", default="other")
    packet_parser.set_defaults(func=command_failure_packet)

    repair_parser = subparsers.add_parser("create-repair-ticket", help="create or render a repair ticket")
    repair_parser.add_argument("--skill", required=True)
    repair_parser.add_argument("--operation", required=True)
    repair_parser.add_argument("--invoked-from", default="other")
    repair_parser.add_argument("--dry-run", action="store_true")
    repair_parser.set_defaults(func=command_create_repair_ticket)

    value_parser = subparsers.add_parser("score-value", help="score value-signal fixtures")
    value_parser.add_argument("--name")
    value_parser.set_defaults(func=command_score_value)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except CapabilityError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
