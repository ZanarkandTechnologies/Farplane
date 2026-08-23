"""Run selected static-lint contracts without permitting projection writes."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from .models import LintContext, LintResult, LintSpec
from .registry import LintRegistry


WRITE_ARGUMENTS = frozenset({"--write", "--fix", "--update", "--generate"})


def _run_command(spec: LintSpec, context: LintContext) -> LintResult:
    assert spec.command is not None
    command = spec.command(context)
    forbidden = sorted(set(command) & WRITE_ARGUMENTS)
    if forbidden:
        return LintResult(spec.check_id, False, f"lint registry rejected write arguments: {', '.join(forbidden)}")
    try:
        completed = subprocess.run(command, cwd=context.root, text=True, capture_output=True, check=False)
    except OSError as exc:
        return LintResult(spec.check_id, False, str(exc))
    output = "\n".join(part.strip() for part in (completed.stdout, completed.stderr) if part.strip())
    return LintResult(spec.check_id, completed.returncode == 0, output)


def lint(registry: LintRegistry, context: LintContext, scope: str) -> list[LintResult]:
    """Run selected read-only lint checks in stable registry order."""

    results: list[LintResult] = []
    for spec in registry.select(scope=scope, changed_paths=context.paths if context.changed else None):
        results.append(spec.run(context) if spec.run is not None else _run_command(spec, context))
    return results


def lint_ticket(root: Path, path: Path) -> LintResult:
    """Run the static portion of one ticket's contract, without lifecycle proof."""

    try:
        relative_path = path.resolve().relative_to(root.resolve())
    except ValueError:
        return LintResult("ticket_static_contract", False, "ticket path must be inside the project")
    if not path.is_file():
        return LintResult("ticket_static_contract", False, f"ticket file does not exist: {relative_path}")
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from tickets.scripts.check_ticket_metadata import validate_ticket

    errors = validate_ticket(path.resolve())
    return LintResult("ticket_static_contract", not errors, "\n".join(errors) or "ticket metadata OK")


def payload(*, scope: str, changed: bool, checks: list[LintResult]) -> dict[str, Any]:
    ok = all(check.ok for check in checks)
    return {
        "ok": ok,
        "scope": scope,
        "changed": changed,
        "summary": (
            f"farplane lint passed: scope={scope} checks={len(checks)}"
            if ok
            else f"farplane lint failed: scope={scope}"
        ),
        "checks": [
            {"id": check.check_id, "ok": check.ok, "output": check.output}
            for check in checks
        ],
    }


def render_payload(data: dict[str, Any], *, as_json: bool) -> None:
    if as_json:
        print(json.dumps(data, indent=2, sort_keys=True))
        return
    print(data["summary"])
    for result in data["checks"]:
        status = "pass" if result["ok"] else "fail"
        print(f"[{status}] {result['id']}")
        if result["output"]:
            print(result["output"])
