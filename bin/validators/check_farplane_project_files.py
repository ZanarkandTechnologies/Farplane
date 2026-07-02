#!/usr/bin/env python3
"""Validate Farplane project framework file conventions."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tomllib
import hashlib
from pathlib import Path

import yaml

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
    "node_modules/",
    "tickets/archive/",
)
SECRET_VALUE_RE = re.compile(
    r"(?i)\b(api[_-]?key|access[_-]?token|secret|password)\b\s*[:=]\s*[\"']?[A-Za-z0-9_./+=-]{8,}"
)
RETIRED_INTEGRATIONS_REF = "farplane/" + "integrations.md"
PRODUCTS_REQUIRED_HEADINGS = (
    "## Team",
    "## Products",
    "## Work Lanes",
    "## Constraints",
)
HARNESS_REQUIRED_HEADINGS = (
    "## Mission",
    "## Human Thesis",
    "## Operating Principles",
    "## Static Leverage Commitments",
    "## Non-Tradeoffs",
    "## Allocation Guardrails",
    "## Agent Authority",
    "## Change Rule",
)
AUTOMATION_RUNTIME_STATE_KEYS = {
    "last_run",
    "last_run_at",
    "last_status",
    "last_error",
    "next_run",
    "run_count",
    "run_ids",
    "runs",
    "memory",
}
ALLOWED_SUPPORT_PRODUCT_IDS = {
    "adoption",
    "cross_product_autonomy",
    "project_control",
}


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
        "farplane/ops-memory.md",
        "farplane/automations.toml",
        "farplane/bindings.yaml",
        "farplane/hooks.json",
        ".agents/skills/README.md",
        "tickets/templates/ticket.md",
        ".farplane/state/run-ledger.json",
        ".farplane/project/ui/",
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

    if "## Team" in text and "| Field | Value |" not in text:
        errors.append(f"{rel_path} Team must use the standard field/value table columns.")
    if "## Products" in text and "| ID | Product | Audience | Output | Reward |" not in text:
        errors.append(f"{rel_path} Products must use the standard product table columns.")
    if "## Work Lanes" in text and "| Lane | Default Weight | Purpose |" not in text:
        errors.append(f"{rel_path} Work Lanes must use the standard lane table columns.")

    return errors


def validate_hooks_file(root: Path, hooks_file: Path) -> list[str]:
    rel_path = hooks_file.relative_to(root).as_posix()
    errors: list[str] = []

    try:
        data = json.loads(hooks_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{rel_path} must be valid JSON: {exc.msg}."]

    if not isinstance(data, dict):
        return [f"{rel_path} must be a JSON object."]
    if data.get("version") != 1:
        errors.append(f"{rel_path} version must be 1.")
    hooks = data.get("hooks")
    if not isinstance(hooks, dict):
        errors.append(f"{rel_path} hooks must be an object.")
        return errors

    file_growth = hooks.get("file_growth")
    if file_growth is not None:
        if not isinstance(file_growth, dict):
            errors.append(f"{rel_path} hooks.file_growth must be an object when present.")
        elif "rules" in file_growth and not isinstance(file_growth.get("rules"), list):
            errors.append(f"{rel_path} hooks.file_growth.rules must be a list when present.")

    return errors


def validate_automations_toml(root: Path, automations_file: Path) -> list[str]:
    rel_path = automations_file.relative_to(root).as_posix()
    errors: list[str] = []
    try:
        data = tomllib.loads(automations_file.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        return [f"{rel_path} must be valid TOML: {exc}."]

    if not isinstance(data, dict):
        return [f"{rel_path} must be a TOML object."]
    if data.get("schema") != "farplane_project_automations":
        errors.append(f"{rel_path} schema must be farplane_project_automations.")
    if data.get("framework_template_version") != "1.0.0":
        errors.append(f"{rel_path} framework_template_version must be 1.0.0.")

    top_runtime_keys = sorted(AUTOMATION_RUNTIME_STATE_KEYS & set(data))
    if top_runtime_keys:
        errors.append(f"{rel_path} must not store runtime state keys: {', '.join(top_runtime_keys)}.")

    automations = data.get("automations")
    if not isinstance(automations, list) or not automations:
        errors.append(f"{rel_path} automations must be a non-empty array of tables.")
        return errors

    seen_ids: set[str] = set()
    for index, automation in enumerate(automations, start=1):
        prefix = f"{rel_path} automations[{index}]"
        if not isinstance(automation, dict):
            errors.append(f"{prefix} must be a table.")
            continue

        runtime_keys = sorted(AUTOMATION_RUNTIME_STATE_KEYS & set(automation))
        if runtime_keys:
            errors.append(f"{prefix} must not store runtime state keys: {', '.join(runtime_keys)}.")

        for key in ("id", "name", "kind", "status", "prompt"):
            if not isinstance(automation.get(key), str) or not automation.get(key, "").strip():
                errors.append(f"{prefix}.{key} must be a non-empty string.")

        automation_id = automation.get("id")
        if isinstance(automation_id, str) and automation_id.strip():
            if automation_id in seen_ids:
                errors.append(f"{rel_path} automation id must be unique: {automation_id}.")
            seen_ids.add(automation_id)

        if automation.get("kind") not in {"heartbeat", "cron"}:
            errors.append(f"{prefix}.kind must be heartbeat or cron.")
        if automation.get("status") not in {"active", "paused"}:
            errors.append(f"{prefix}.status must be active or paused.")

        target = automation.get("target")
        if not isinstance(target, dict):
            errors.append(f"{prefix}.target must be a table with workspace or thread_id.")
        elif not any(isinstance(target.get(key), str) and target.get(key, "").strip() for key in ("workspace", "thread_id")):
            errors.append(f"{prefix}.target must include workspace or thread_id.")

        schedule = automation.get("schedule")
        if not isinstance(schedule, dict):
            errors.append(f"{prefix}.schedule must be a table.")
            continue

        schedule_type = schedule.get("type")
        if schedule_type not in {"interval", "active_hours_interval", "daily", "weekly", "monthly"}:
            errors.append(f"{prefix}.schedule.type is unsupported.")
        if schedule_type in {"daily", "weekly", "monthly", "active_hours_interval"}:
            if not isinstance(schedule.get("timezone"), str) or not schedule.get("timezone", "").strip():
                errors.append(f"{prefix}.schedule.timezone must be a non-empty string.")
        if schedule_type in {"daily", "weekly", "monthly"}:
            if not isinstance(schedule.get("time"), str) or not schedule.get("time", "").strip():
                errors.append(f"{prefix}.schedule.time must be a non-empty string.")
        if schedule_type == "weekly":
            days = schedule.get("days")
            if not isinstance(days, list) or not days or any(not isinstance(day, str) or not day for day in days):
                errors.append(f"{prefix}.schedule.days must be a non-empty list of day strings.")
        if schedule_type == "monthly" and not isinstance(schedule.get("day_of_month"), int):
            errors.append(f"{prefix}.schedule.day_of_month must be an integer.")
        if schedule_type in {"interval", "active_hours_interval"} and not isinstance(schedule.get("interval_minutes"), int):
            errors.append(f"{prefix}.schedule.interval_minutes must be an integer.")

    return errors


def validate_bindings_file(root: Path, bindings_file: Path) -> list[str]:
    rel_path = bindings_file.relative_to(root).as_posix()
    errors: list[str] = []
    try:
        data = yaml.safe_load(bindings_file.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        return [f"{rel_path} must be valid YAML: {exc}."]

    if not isinstance(data, dict):
        return [f"{rel_path} must be a YAML object."]
    if data.get("kind") != "project-bindings":
        errors.append(f"{rel_path} must declare kind: project-bindings.")
    if "framework_template_version" not in data:
        errors.append(f"{rel_path} must declare framework_template_version.")
    if not isinstance(data.get("project"), dict):
        errors.append(f"{rel_path} project must be an object.")
    if "metrics" in data and not isinstance(data.get("metrics"), dict):
        errors.append(f"{rel_path} metrics must be an object when present.")

    for line_number, line in enumerate(bindings_file.read_text(encoding="utf-8").splitlines(), start=1):
        if SECRET_VALUE_RE.search(line):
            errors.append(
                f"{rel_path}:{line_number} looks like it stores a secret value; "
                "bindings are non-secret coordinates only."
            )
    return errors


def markdown_heading_section(markdown: str, heading: str) -> str:
    target = f"## {heading}"
    lines = markdown.splitlines()
    start: int | None = None
    for index, line in enumerate(lines):
        if line.strip() == target:
            start = index + 1
            break
    if start is None:
        return ""
    end = len(lines)
    for index in range(start, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return "\n".join(lines[start:end]).strip()


def parse_fenced_yaml_from_section(section: str) -> dict:
    fence_start = section.find("```yaml")
    if fence_start == -1:
        return {}
    yaml_start = section.find("\n", fence_start)
    if yaml_start == -1:
        return {}
    fence_end = section.find("```", yaml_start + 1)
    if fence_end == -1:
        return {}
    try:
        loaded = yaml.safe_load(section[yaml_start + 1 : fence_end]) or {}
    except yaml.YAMLError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def parse_markdown_table(section: str) -> list[dict[str, str]]:
    rows: list[list[str]] = []
    for raw in section.splitlines():
        line = raw.strip()
        if not line.startswith("|") or "---" in line:
            continue
        rows.append([cell.strip() for cell in line.strip("|").split("|")])
    if len(rows) < 2:
        return []
    headers = [header.lower().replace(" ", "_") for header in rows[0]]
    return [
        {headers[index]: cells[index] if index < len(cells) else "" for index in range(len(headers))}
        for cells in rows[1:]
    ]


def load_goal_kpi_ids(goals_file: Path) -> set[str]:
    if not goals_file.exists():
        return set()
    text = goals_file.read_text(encoding="utf-8")
    payload = parse_fenced_yaml_from_section(markdown_heading_section(text, "Goals"))
    goals = payload.get("goals") if isinstance(payload.get("goals"), dict) else {}
    kpi_ids: set[str] = set()
    for axis_payload in goals.values():
        if not isinstance(axis_payload, dict):
            continue
        for smart_goal in axis_payload.get("smart_goals") or []:
            if not isinstance(smart_goal, dict):
                continue
            for raw_kpi in smart_goal.get("kpis") or []:
                if isinstance(raw_kpi, dict):
                    kpi_id = str(raw_kpi.get("id") or "").strip()
                else:
                    kpi_id = str(raw_kpi).strip()
                if kpi_id:
                    kpi_ids.add(kpi_id)
    return kpi_ids


def load_binding_metrics(bindings_file: Path) -> dict[str, dict]:
    if not bindings_file.exists():
        return {}
    try:
        data = yaml.safe_load(bindings_file.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return {}
    metrics = data.get("metrics") if isinstance(data, dict) else {}
    if not isinstance(metrics, dict):
        return {}
    return {str(metric_id): recipe if isinstance(recipe, dict) else {} for metric_id, recipe in metrics.items()}


def load_product_ids(products_file: Path) -> set[str]:
    if not products_file.exists():
        return set()
    text = products_file.read_text(encoding="utf-8")
    rows = parse_markdown_table(markdown_heading_section(text, "Products"))
    return {row.get("id", "").strip() for row in rows if row.get("id", "").strip()}


def sha256_file(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def validate_snapshot_freshness(root: Path, snapshot_path: Path) -> list[str]:
    if not snapshot_path.exists():
        return []
    try:
        snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{snapshot_path.relative_to(root)} must be valid JSON: {exc.msg}."]
    sources = snapshot.get("sources") if isinstance(snapshot, dict) else None
    if not isinstance(sources, list):
        return [f"{snapshot_path.relative_to(root)} sources must be a list when snapshot exists."]
    errors: list[str] = []
    for source in sources:
        if not isinstance(source, dict) or not source.get("path") or not source.get("hash"):
            continue
        path = root / str(source["path"])
        current_hash = sha256_file(path)
        if current_hash and current_hash != source.get("hash"):
            errors.append(f"{snapshot_path.relative_to(root)} is stale for {source['path']}; regenerate project snapshot.")
    return errors


def validate_cross_file_contract(root: Path) -> list[str]:
    goals_file = root / "farplane" / "goals.md"
    bindings_file = root / "farplane" / "bindings.yaml"
    products_file = root / "farplane" / "products.md"
    metrics = load_binding_metrics(bindings_file)
    goal_kpis = load_goal_kpi_ids(goals_file)
    product_ids = load_product_ids(products_file)
    errors: list[str] = []

    missing_metric_recipes = sorted(kpi_id for kpi_id in goal_kpis if kpi_id not in metrics)
    if missing_metric_recipes:
        errors.append(f"farplane/goals.md KPI ids lack bindings.yaml metric recipes: {', '.join(missing_metric_recipes)}.")

    allowed_products = product_ids | ALLOWED_SUPPORT_PRODUCT_IDS
    unknown_products = sorted(
        {
            str(recipe.get("product")).strip()
            for recipe in metrics.values()
            if recipe.get("product") and str(recipe.get("product")).strip() not in allowed_products
        }
    )
    if unknown_products:
        errors.append(f"farplane/bindings.yaml metric products are not in products.md: {', '.join(unknown_products)}.")

    errors.extend(validate_snapshot_freshness(root, root / ".farplane" / "project" / "ui" / "latest.json"))
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
    automations_toml = framework_dir / "automations.toml"
    bindings = framework_dir / "bindings.yaml"
    harness = framework_dir / "harness.md"
    products = framework_dir / "products.md"
    hooks = framework_dir / "hooks.json"
    retired_file_growth_hook = framework_dir / "file-growth-hook.json"
    duplicate_project_charter = framework_dir / "project.md"
    pm_manifest = framework_dir / "pm.json"
    retired_bindings_markdown = framework_dir / "bindings.md"
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
        errors.append(f"{RETIRED_INTEGRATIONS_REF} is retired; use farplane/bindings.yaml.")
    if retired_bindings_markdown.exists():
        errors.append("farplane/bindings.md is retired; use farplane/bindings.yaml.")
    if retired_steer_config.exists():
        errors.append("farplane/steer.config.toml is retired; use farplane/automations.toml.")
    if retired_steer_state.exists():
        errors.append(".farplane/state/steer-scheduler.json is retired; Codex automation cadence owns scheduling.")
    if retired_file_growth_hook.exists():
        errors.append("farplane/file-growth-hook.json is retired; use farplane/hooks.json.")
    if duplicate_project_charter.exists():
        errors.append(
            "farplane/project.md would duplicate the active static charter; use farplane/harness.md "
            "unless a versioned framework migration replaces it."
        )

    if not automations_toml.exists():
        errors.append("farplane/automations.toml is required for full Codex automation configs.")
    else:
        errors.extend(validate_automations_toml(root, automations_toml))

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

    if not hooks.exists():
        errors.append("farplane/hooks.json is required for declarative Farplane hook config.")
    else:
        errors.extend(validate_hooks_file(root, hooks))

    if not bindings.exists():
        errors.append("farplane/bindings.yaml is required for project bindings.")
    else:
        errors.extend(validate_bindings_file(root, bindings))

    errors.extend(validate_cross_file_contract(root))

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
                f"{rel_path}: references retired {RETIRED_INTEGRATIONS_REF}; use farplane/bindings.yaml."
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
