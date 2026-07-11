"""Allowlisted Farplane-wide and owner-local ticket validation checks."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import time
from pathlib import Path

try:
    from validation.models import CheckMode, CheckResult, CheckSpec, ValidationContext
    from validation.registry import CheckRegistry
except ImportError:  # package import during tests
    from bin.core.validation.models import CheckMode, CheckResult, CheckSpec, ValidationContext
    from bin.core.validation.registry import CheckRegistry


def _result(check_id: str, mode: CheckMode, returncode: int, output: str, started: float) -> CheckResult:
    return CheckResult(
        check_id=check_id,
        mode=mode,
        status="pass" if returncode == 0 else "fail",
        output=output.strip(),
        duration_ms=round((time.monotonic() - started) * 1000),
    )


def command_check(check_id: str, argv: tuple[str, ...]):
    def run(context: ValidationContext, mode: CheckMode) -> CheckResult:
        started = time.monotonic()
        try:
            completed = subprocess.run(
                list(argv),
                cwd=context.root,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
                timeout=300,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return _result(check_id, mode, 1, str(exc), started)
        return _result(check_id, mode, completed.returncode, completed.stdout, started)

    return run


def ticket_metadata_check(context: ValidationContext, mode: CheckMode) -> CheckResult:
    started = time.monotonic()
    module_path = context.root / "tickets" / "scripts" / "check_ticket_metadata.py"
    spec = importlib.util.spec_from_file_location("farplane_ticket_metadata", module_path)
    if spec is None or spec.loader is None:
        return _result("ticket.metadata", mode, 1, f"could not load {module_path}", started)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    errors = module.validate_ticket(context.ticket)
    return _result("ticket.metadata", mode, 1 if errors else 0, "\n".join(errors) or "ticket metadata OK", started)


def visual_companion_check(context: ValidationContext, mode: CheckMode) -> CheckResult:
    started = time.monotonic()
    script = context.root / "skills" / "impl-plan" / "scripts" / "validate_visual_companion.py"
    completed = subprocess.run(
        ["python3", str(script), str(context.ticket)],
        cwd=context.root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return _result("ticket.visual-companion", mode, completed.returncode, completed.stdout, started)


def _latest_result_passes(root: Path) -> bool:
    paths = sorted(root.rglob("result.json")) if root.is_dir() else []
    if not paths:
        return False
    try:
        payload = json.loads(paths[-1].read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    verdict = str(payload.get("verdict") or payload.get("status") or "").lower()
    return verdict in {"pass", "passed", "ok"}


def _review_passes(path: Path) -> bool:
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text:
        return False
    frontmatter = text.split("\n---\n", 1)[0][4:]
    fields: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields.get("verdict", "").lower() == "pass" and fields.get("overall_tas", "").upper() == "TAS-A"


def completion_evidence_check(context: ValidationContext, mode: CheckMode) -> CheckResult:
    started = time.monotonic()
    text = context.ticket.read_text(encoding="utf-8")
    artifacts = context.ticket.parent / "artifacts"
    errors: list[str] = []
    if re.search(r"^requires_qa:\s*true\s*$", text, re.M) and not _latest_result_passes(artifacts / "qa"):
        errors.append("requires_qa=true but no passing QA result.json exists")
    if re.search(r"^requires_demo:\s*true\s*$", text, re.M) and not _latest_result_passes(artifacts / "demo"):
        errors.append("requires_demo=true but no passing demo result.json exists")
    if "reviewer" in text.lower():
        review_path = artifacts / "review" / "completion-review.md"
        if not _review_passes(review_path):
            errors.append("reviewer completion is required but completion-review.md is missing or not pass/TAS-A")
    return _result(
        "ticket.completion-evidence",
        mode,
        1 if errors else 0,
        "\n".join(errors) or "completion evidence OK",
        started,
    )


def build_registry() -> CheckRegistry:
    registry = CheckRegistry()
    specs = (
        CheckSpec("ticket.metadata", ticket_metadata_check),
        CheckSpec("ticket.completion-evidence", completion_evidence_check),
        CheckSpec("ticket.visual-companion", visual_companion_check),
        CheckSpec("skills.check", command_check("skills.check", ("python3", "skills/skill-maintenance/scripts/check_skills.py"))),
        CheckSpec("docs.refs", command_check("docs.refs", ("python3", "bin/validators/check_doc_refs.py"))),
        CheckSpec("docs.contracts", command_check("docs.contracts", ("python3", "bin/validators/check_doc_parity.py"))),
        CheckSpec("docs.features", command_check("docs.features", ("python3", "docs/features/validate_features.py"))),
        CheckSpec("docs.sources", command_check("docs.sources", ("python3", "docs/sources/validate_sources.py"))),
        CheckSpec("templates.check", command_check("templates.check", ("python3", "bin/validators/sync_template_registry.py", "--check"))),
        CheckSpec("project.check", command_check("project.check", ("python3", "bin/validators/check_farplane_project_files.py"))),
        CheckSpec("harness.check", command_check("harness.check", ("python3", "bin/validators/check_harness_invariants.py"))),
    )
    for spec in specs:
        registry.register(spec)
    return registry
