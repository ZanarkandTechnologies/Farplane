#!/usr/bin/env python3
"""Validate Farplane project framework file conventions."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bin.validators.template_usage import TemplateUsageError, normalize_template_uses


TEXT_SUFFIXES = {
    ".json",
    ".jsonl",
    ".md",
    ".py",
    ".sh",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
SKIP_PREFIXES = (
    ".git/",
    ".farplane/",
    "docs/archive/",
    "node_modules/",
    "tickets/archive/",
)
SECRET_VALUE_RE = re.compile(
    r"(?i)\b(api[_-]?key|access[_-]?token|secret|password)\b\s*[:=]\s*[\"']?[A-Za-z0-9_./+=-]{8,}"
)
RETIRED_INTEGRATIONS_REF = "farplane/" + "integrations.md"
PRODUCTS_REQUIRED_HEADINGS = (
    "## Team Archetype",
    "## Operating Flywheel",
    "## Primary Products",
    "## Supporting Products",
    "## Autonomous Project Types",
    "## Product Selection Notes",
    "## Pulse Refill Guidance",
)
HARNESS_REQUIRED_HEADINGS = (
    "## Mission",
    "## Human Thesis",
    "## Operating Principles",
    "## Static Leverage Commitments",
    "## Non-Tradeoffs",
    "## Agent Authority",
    "## Change Rule",
    "## Charter-Level Operating Loop",
    "## File Boundaries",
)


def tracked_files(root: Path) -> list[Path]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=root,
            check=True,
            capture_output=True,
            text=False,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return sorted(
            path.relative_to(root)
            for path in root.rglob("*")
            if path.is_file() and ".git" not in path.parts
        )

    return [Path(raw.decode("utf-8")) for raw in result.stdout.split(b"\0") if raw]


def should_scan(path: Path) -> bool:
    path_string = path.as_posix()
    if any(path_string.startswith(prefix) for prefix in SKIP_PREFIXES):
        return False
    return path.suffix in TEXT_SUFFIXES


def validate_pm_manifest(root: Path, pm_manifest: Path) -> list[str]:
    errors: list[str] = []
    rel_path = pm_manifest.relative_to(root).as_posix()

    try:
        data = json.loads(pm_manifest.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{rel_path} must be valid JSON: {exc.msg}."]

    if not isinstance(data, dict):
        return [f"{rel_path} must be a JSON object."]

    expected_top_level = {"version", "name", "role", "threads"}
    missing = sorted(expected_top_level - set(data))
    extra = sorted(set(data) - expected_top_level)
    if missing:
        errors.append(f"{rel_path} missing required keys: {', '.join(missing)}.")
    if extra:
        errors.append(f"{rel_path} has unsupported keys: {', '.join(extra)}.")

    if data.get("version") != 1:
        errors.append(f"{rel_path} version must be 1.")
    if not isinstance(data.get("name"), str) or not data.get("name", "").strip():
        errors.append(f"{rel_path} name must be a non-empty string.")
    if data.get("role") != "founder_operator":
        errors.append(f"{rel_path} role must be founder_operator.")

    threads = data.get("threads")
    if not isinstance(threads, dict):
        errors.append(f"{rel_path} threads must be an object.")
        return errors

    expected_thread_keys = {"chats", "automations"}
    missing_thread_keys = sorted(expected_thread_keys - set(threads))
    extra_thread_keys = sorted(set(threads) - expected_thread_keys)
    if missing_thread_keys:
        errors.append(f"{rel_path} threads missing required keys: {', '.join(missing_thread_keys)}.")
    if extra_thread_keys:
        errors.append(f"{rel_path} threads has unsupported keys: {', '.join(extra_thread_keys)}.")

    for key in sorted(expected_thread_keys):
        values = threads.get(key)
        if not isinstance(values, list):
            errors.append(f"{rel_path} threads.{key} must be a list of thread ID strings.")
            continue
        if any(not isinstance(value, str) or not value.strip() for value in values):
            errors.append(f"{rel_path} threads.{key} must contain only non-empty strings.")
        if len(values) != len(set(values)):
            errors.append(f"{rel_path} threads.{key} must not contain duplicate thread IDs.")

    return errors


def validate_framework_manifest(root: Path, framework_manifest: Path) -> list[str]:
    rel_path = framework_manifest.relative_to(root).as_posix()
    errors: list[str] = []

    try:
        data = json.loads(framework_manifest.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{rel_path} must be valid JSON: {exc.msg}."]

    if not isinstance(data, dict):
        return [f"{rel_path} must be a JSON object."]

    if data.get("schema") != "farplane_project":
        errors.append(f"{rel_path} schema must be farplane_project.")
    if not isinstance(data.get("spec_version"), str) or not data.get("spec_version", "").strip():
        errors.append(f"{rel_path} spec_version must be a non-empty string.")
    try:
        template_uses = normalize_template_uses(data, rel_path, include_legacy=False)
    except TemplateUsageError as exc:
        errors.append(str(exc))
        template_uses = {}
    if not template_uses.get("farplane-framework"):
        errors.append(f"{rel_path} template_uses.farplane-framework must be a non-empty string.")

    project = data.get("project")
    if not isinstance(project, dict):
        errors.append(f"{rel_path} project must be an object.")
    else:
        for field in ("name", "description", "archetype"):
            if not isinstance(project.get(field), str) or not project.get(field, "").strip():
                errors.append(f"{rel_path} project.{field} must be a non-empty string.")

    for key in ("standard", "optional"):
        section = data.get(key)
        if not isinstance(section, dict):
            errors.append(f"{rel_path} {key} must be an object.")
            continue
        for list_key in ("tracked", "ignored"):
            values = section.get(list_key)
            if not isinstance(values, list):
                errors.append(f"{rel_path} {key}.{list_key} must be a list.")
                continue
            bad_values = [value for value in values if not isinstance(value, str) or not value.strip()]
            if bad_values:
                errors.append(f"{rel_path} {key}.{list_key} must contain only non-empty strings.")
            if len(values) != len(set(values)):
                errors.append(f"{rel_path} {key}.{list_key} must not contain duplicate paths.")

    required_paths = {
        "AGENTS.md",
        "PROJECT_RULES.md",
        "ARCHITECTURE.md",
        "farplane/README.md",
        "farplane/manifest.json",
        "farplane/harness.md",
        "farplane/goals.md",
        "farplane/products.md",
        "farplane/automations.md",
        "farplane/bindings.md",
        "farplane/evals.md",
        "tickets/templates/ticket.md",
        ".farplane/state/run-ledger.json",
    }
    standard = data.get("standard") if isinstance(data.get("standard"), dict) else {}
    paths = set()
    for list_key in ("tracked", "ignored"):
        values = standard.get(list_key)
        if isinstance(values, list):
            paths.update(value for value in values if isinstance(value, str))
    missing_paths = sorted(required_paths - paths)
    if missing_paths:
        errors.append(f"{rel_path} missing required standard paths: {', '.join(missing_paths)}.")

    tracked = set(standard.get("tracked", [])) if isinstance(standard.get("tracked"), list) else set()
    ignored = set(standard.get("ignored", [])) if isinstance(standard.get("ignored"), list) else set()
    overlap = sorted(tracked & ignored)
    if overlap:
        errors.append(f"{rel_path} paths cannot be both tracked and ignored: {', '.join(overlap)}.")

    for path_ref in sorted(tracked):
        path = root / path_ref
        if path_ref.endswith("/"):
            if not path.is_dir():
                errors.append(f"{rel_path} standard.tracked path is missing or not a directory: {path_ref}.")
        elif not path.exists():
            errors.append(f"{rel_path} standard.tracked path is missing: {path_ref}.")

    for path_ref in sorted(ignored):
        path = root / path_ref
        if path_ref.endswith("/"):
            if not path.is_dir():
                errors.append(f"{rel_path} standard.ignored path is missing or not a directory: {path_ref}.")
        elif not path.exists():
            errors.append(f"{rel_path} standard.ignored path is missing: {path_ref}.")

    return errors


def validate_products_file(root: Path, products_file: Path) -> list[str]:
    rel_path = products_file.relative_to(root).as_posix()
    text = products_file.read_text(encoding="utf-8")
    errors: list[str] = []

    if "kind: project-products" not in text[:700]:
        errors.append(f"{rel_path} must use front matter kind: project-products.")
    if "framework_template_version:" not in text[:700]:
        errors.append(f"{rel_path} must declare framework_template_version in front matter.")

    missing_headings = [heading for heading in PRODUCTS_REQUIRED_HEADINGS if heading not in text]
    if missing_headings:
        errors.append(f"{rel_path} missing required headings: {', '.join(missing_headings)}.")

    if "## Primary Products" in text and "| Product | Audience | Artifact Examples | Reward Signals | Owner Skills |" not in text:
        errors.append(f"{rel_path} Primary Products must use the standard product table columns.")

    return errors


def validate_harness_file(root: Path, harness_file: Path) -> list[str]:
    rel_path = harness_file.relative_to(root).as_posix()
    text = harness_file.read_text(encoding="utf-8")
    errors: list[str] = []

    if "kind: project-harness" not in text[:700]:
        errors.append(f"{rel_path} must use front matter kind: project-harness.")
    if "framework_template_version:" not in text[:700]:
        errors.append(f"{rel_path} must declare framework_template_version in front matter.")

    if "```harness-program" in text:
        errors.append(
            f"{rel_path} must not use fenced harness-program DSL; use YAML front matter plus Markdown charter sections."
        )

    missing_headings = [heading for heading in HARNESS_REQUIRED_HEADINGS if heading not in text]
    if missing_headings:
        errors.append(f"{rel_path} missing required static-charter headings: {', '.join(missing_headings)}.")

    if "## Static Leverage Commitments" in text and "| Commitment | Why It Compounds | Evidence To Seek | Pivot Signal |" not in text:
        errors.append(f"{rel_path} Static Leverage Commitments must use the standard commitment table columns.")

    return errors


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    framework_dir = root / "farplane"
    framework_manifest = framework_dir / "manifest.json"
    automations = framework_dir / "automations.md"
    bindings = framework_dir / "bindings.md"
    harness = framework_dir / "harness.md"
    products = framework_dir / "products.md"
    duplicate_project_charter = framework_dir / "project.md"
    pm_manifest = framework_dir / "pm.json"
    retired_integrations = framework_dir / "integrations.md"
    retired_steer_config = framework_dir / "steer.config.toml"
    retired_steer_state = root / ".farplane/state/steer-scheduler.json"

    if not framework_dir.exists():
        return errors

    if not framework_manifest.exists():
        errors.append("farplane/manifest.json is required for Farplane project manifests.")
    else:
        errors.extend(validate_framework_manifest(root, framework_manifest))

    if retired_integrations.exists():
        errors.append(f"{RETIRED_INTEGRATIONS_REF} is retired; use farplane/bindings.md.")
    if retired_steer_config.exists():
        errors.append("farplane/steer.config.toml is retired; use farplane/automations.md.")
    if retired_steer_state.exists():
        errors.append(".farplane/state/steer-scheduler.json is retired; Codex automation cadence owns scheduling.")
    if duplicate_project_charter.exists():
        errors.append(
            "farplane/project.md would duplicate the active static charter; use farplane/harness.md "
            "unless a versioned framework migration replaces it."
        )

    if not automations.exists():
        errors.append("farplane/automations.md is required for reviewable Codex automation prompts.")

    if not harness.exists():
        errors.append("farplane/harness.md is required for the static human charter.")
    else:
        errors.extend(validate_harness_file(root, harness))

    if not products.exists():
        errors.append("farplane/products.md is required for project product catalogs.")
    else:
        errors.extend(validate_products_file(root, products))

    if pm_manifest.exists():
        errors.extend(validate_pm_manifest(root, pm_manifest))

    if bindings.exists():
        text = bindings.read_text(encoding="utf-8")
        if "kind: project-bindings" not in text[:500]:
            errors.append("farplane/bindings.md must use front matter kind: project-bindings.")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if SECRET_VALUE_RE.search(line):
                errors.append(
                    f"farplane/bindings.md:{line_number} looks like it stores a secret value; "
                    "bindings are non-secret coordinates only."
                )

    for path in sorted(framework_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if "framework_template_version:" not in text[:700]:
            errors.append(
                f"{path.relative_to(root)} must declare framework_template_version in front matter."
            )

    for rel_path in tracked_files(root):
        if not should_scan(rel_path):
            continue
        full_path = root / rel_path
        if not full_path.exists():
            continue
        try:
            text = full_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if RETIRED_INTEGRATIONS_REF in text:
            errors.append(
                f"{rel_path}: references retired {RETIRED_INTEGRATIONS_REF}; use farplane/bindings.md."
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()

    errors = validate(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Farplane project file conventions OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
