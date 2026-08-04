#!/usr/bin/env python3
"""Materialize validated Plan Next Wave calls into generic filesystem tickets."""

from __future__ import annotations

import argparse
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml


def _read_skill_admission_contract(project_root: Path, skill_ref: str) -> dict[str, Any] | None:
    for base in (project_root / ".agents" / "skills", project_root / "skills"):
        path = base / skill_ref / "SKILL.md"
        if not path.is_file():
            continue
        parts = path.read_text(encoding="utf-8").split("---", 2)
        if len(parts) != 3:
            return None
        metadata = yaml.safe_load(parts[1]) or {}
        planner = metadata.get("planner_contract") if isinstance(metadata, dict) else None
        contract = planner.get("admission_contract") if isinstance(planner, dict) else None
        return contract if isinstance(contract, dict) else None
    return None


def _open_lifecycle_refs(project_root: Path, skill_ref: str, contract: dict[str, Any]) -> list[str]:
    releases = {str(value).strip().lower() for value in contract.get("release_states", [])}
    open_until = str(contract.get("open_until") or "").strip()
    refs: list[str] = []
    for path in sorted((project_root / "tickets").glob("TASK-*/ticket.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        if not re.search(rf"(?m)^skill_ref:\s*['\"]?{re.escape(skill_ref)}['\"]?\s*$", text):
            continue
        parts = text.split("---", 2)
        metadata = yaml.safe_load(parts[1]) if len(parts) == 3 else {}
        if isinstance(metadata, dict) and metadata.get("admission_state") == "held_not_admitted":
            continue
        status = str(metadata.get("status") or "").strip().lower() if isinstance(metadata, dict) else ""
        if status in releases:
            continue
        progress = path.with_name("progress.md")
        progress_text = progress.read_text(encoding="utf-8", errors="replace") if progress.exists() else ""
        if open_until and re.search(
            rf"(?m)^\s*(?:phase|status):\s*['\"]?{re.escape(open_until)}['\"]?\s*$",
            progress_text,
        ):
            continue
        refs.append(str(path.relative_to(project_root)))
    return refs


def _required_text(row: dict[str, Any], field: str) -> str:
    value = row.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"skill call {field} must be a non-empty string")
    return value.strip()


def materialize_skill_call(
    project_root: Path,
    ticket_id: str,
    call: dict[str, Any],
    *,
    created_at: str | None = None,
) -> Path:
    """Write one generic ticket while preserving bindings and no workflow prose."""
    if not ticket_id.startswith("TASK-"):
        raise ValueError("ticket_id must start with TASK-")
    call_id = _required_text(call, "call_id")
    title = _required_text(call, "title")
    skill_ref = _required_text(call, "skill_ref")
    expected_artifact = _required_text(call, "expected_artifact")
    arguments = call.get("arguments")
    objective = call.get("objective_contribution")
    admission = call.get("admission")
    admission_contract = _read_skill_admission_contract(project_root, skill_ref)
    if not isinstance(arguments, dict) or not arguments:
        raise ValueError("skill call arguments must be a non-empty object")
    if not isinstance(objective, dict) or not objective:
        raise ValueError("skill call objective_contribution must be a non-empty object")
    if admission_contract and admission is None:
        raise ValueError("selected skill requires a validated admission receipt")
    if admission is not None:
        if not isinstance(admission, dict) or admission.get("decision") != "admit":
            raise ValueError("skill call admission must be a validated admit decision")
        if not admission_contract:
            raise ValueError("skill call admission has no matching selected-skill contract")
        open_refs = _open_lifecycle_refs(project_root, skill_ref, admission_contract)
        receipt_refs = admission.get("open_lifecycle_refs")
        if not isinstance(receipt_refs, list) or sorted(receipt_refs) != sorted(open_refs):
            raise ValueError("skill call admission is stale; open lifecycle receipt changed")
        max_open = admission_contract.get("max_open_lifecycles")
        if isinstance(max_open, bool) or not isinstance(max_open, int) or max_open < 1:
            raise ValueError("selected skill admission max_open_lifecycles must be a positive integer")
        if len(open_refs) >= max_open:
            raise ValueError("skill call admission is stale; lifecycle capacity is full: " + ", ".join(open_refs))

    timestamp = created_at or datetime.now(UTC).isoformat()
    call_receipt: dict[str, Any] = {
        "call_id": call_id,
        "skill_ref": skill_ref,
        "arguments": arguments,
    }
    if admission is not None:
        call_receipt["admission"] = admission
    if isinstance(call.get("area_id"), str) and call["area_id"].strip():
        call_receipt["area_id"] = call["area_id"].strip()
    call_receipt["expected_artifact"] = expected_artifact

    path = project_root / "tickets" / ticket_id / "ticket.md"
    if path.exists():
        raise FileExistsError(f"refusing to overwrite {path}")
    path.parent.mkdir(parents=True, exist_ok=False)
    frontmatter = {
        "template_id": "ticket-template",
        "template_version": "0.2.3",
        "ticket_id": ticket_id,
        "title": title,
        "status": "todo",
        "priority": "medium",
        "created_at": timestamp,
        "updated_at": timestamp,
    }
    lifecycle = call.get("lifecycle")
    if isinstance(lifecycle, dict) and "due_at" in lifecycle:
        frontmatter["due_at"] = lifecycle["due_at"]
    body = "\n".join(
        [
            "---",
            yaml.safe_dump(frontmatter, sort_keys=False).strip(),
            "---",
            "",
            f"# {ticket_id}: {title}",
            "",
            "## Summary",
            "",
            f"Invoke `{skill_ref}` with the bound inputs below to produce {expected_artifact}.",
            "",
            "## Planned Skill Call",
            "",
            "```yaml",
            yaml.safe_dump(call_receipt, sort_keys=False).strip(),
            "```",
            "",
            "## Objective Contribution",
            "",
            "```yaml",
            yaml.safe_dump({"objective_contribution": objective}, sort_keys=False).strip(),
            "```",
            "",
            "## Done / Proof",
            "",
            f"- [ ] `{skill_ref}` completes its own workflow and produces the expected artifact.",
            "- [ ] Ticket-local QA and independent review evidence are linked.",
            "",
            "## State",
            "",
            "- Pulse materialized this ticket from a validated Plan Next Wave call.",
            "- The selected skill owns execution procedure; no workflow was copied here.",
            "",
        ]
    )
    path.write_text(body, encoding="utf-8")
    return path


def materialize_admitted_calls(
    project_root: Path,
    response: dict[str, Any],
    ticket_ids: list[str],
    *,
    created_at: str | None = None,
) -> list[Path]:
    calls = response.get("proposed_skill_calls")
    decision = response.get("decision")
    if not isinstance(calls, list) or not isinstance(decision, dict):
        raise ValueError("validated response must contain proposed_skill_calls and decision")
    admitted = decision.get("admitted_call_ids")
    if not isinstance(admitted, list) or len(admitted) != len(ticket_ids):
        raise ValueError("ticket_ids must map one-to-one to admitted_call_ids")
    by_id = {call.get("call_id"): call for call in calls if isinstance(call, dict)}
    paths: list[Path] = []
    for call_id, ticket_id in zip(admitted, ticket_ids, strict=True):
        call = by_id.get(call_id)
        if not isinstance(call, dict):
            raise ValueError(f"admitted call {call_id!r} is missing")
        paths.append(materialize_skill_call(project_root, ticket_id, call, created_at=created_at))
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--response", type=Path, required=True)
    parser.add_argument("--ticket-id", action="append", required=True)
    parser.add_argument("--created-at")
    args = parser.parse_args()
    response = json.loads(args.response.read_text(encoding="utf-8"))
    paths = materialize_admitted_calls(
        args.project_root.resolve(), response, args.ticket_id, created_at=args.created_at
    )
    print(json.dumps({"tickets": [str(path) for path in paths]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
