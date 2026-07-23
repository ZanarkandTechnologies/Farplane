#!/usr/bin/env python3
"""Materialize validated Plan Next Wave calls into generic filesystem tickets."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml


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
    if not isinstance(arguments, dict) or not arguments:
        raise ValueError("skill call arguments must be a non-empty object")
    if not isinstance(objective, dict) or not objective:
        raise ValueError("skill call objective_contribution must be a non-empty object")

    timestamp = created_at or datetime.now(UTC).isoformat()
    call_receipt: dict[str, Any] = {
        "call_id": call_id,
        "skill_ref": skill_ref,
        "arguments": arguments,
    }
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
