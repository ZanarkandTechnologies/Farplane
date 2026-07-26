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
from pydantic import BaseModel, ConfigDict, StrictBool, ValidationError, field_validator
from typing import Any, Literal

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bin.validators.template_usage import TemplateUsageError, normalize_template_uses
from bin.core.farplane_metric_schema import MetricObservationBatch
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
HARNESS_ALLOWED_TOP_LEVEL = {
    "kind",
    "status",
    "project",
    "created_at",
    "updated_at",
    "framework_template_version",
    "owner",
    "identity",
    "metric_refs",
    "planning",
    "areas",
    "feature_definition",
    "operating_principles",
    "stable_capabilities",
    "leverage_commitments",
    "constraints",
    "authority",
    "change_rule",
}
AREA_ALLOWED_FIELDS = {"description", "icp", "skill_refs", "metric_refs"}
ICP_ALLOWED_FIELDS = {
    "label",
    "description",
    "jobs_to_be_done",
    "pain_points",
    "evidence_bar",
}
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
ALLOWED_DIAGNOSTIC_METRIC_IDS = {
    "ai_burn_estimate",
    "codex_thread_usage",
    "kpi_attributed_ticket_ratio",
    "ticket_thread_association_backfill",
    "ticket_thread_link_coverage",
    "tickets_completed_count",
    "tickets_created_count",
    "tickets_with_kpi_reward_count",
}
ALLOWED_DIAGNOSTIC_SOURCE_IDS = {
    "autonomy_time_feedback",
    "github_repo_feedback",
    "pulse_decision_ledger",
    "pulse_reward_ledger",
    "ticket_board",
}


class StrictYamlModel(BaseModel):
    model_config = ConfigDict(extra="allow")


class MetricDefinitionModel(StrictYamlModel):
    type: Literal["flow", "stock"]
    unit: str
    direction: Literal["maximize", "minimize"]
    label: str | None = None
    description: str | None = None
    display: Literal["bar_plus_cumulative", "line", "reading"] | None = None
    pinned: StrictBool | None = None
    max_age_days: int | None = None
    guard: dict[str, Any] | None = None

    @field_validator("unit")
    @classmethod
    def non_empty_string(cls, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("must be a non-empty string")
        return value.strip()

    @field_validator("label", "description")
    @classmethod
    def optional_non_empty_string(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("must be a non-empty string when present")
        return value.strip() if value is not None else None


class MetricBindingModel(StrictYamlModel):
    refresh: str

    @field_validator("refresh")
    @classmethod
    def non_empty_refresh(cls, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("must be a non-empty string")
        return value.strip()


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
        "farplane/harness.yaml",
        "farplane/metrics.yaml",
        "farplane/automations.toml",
        "farplane/bindings.yaml",
        ".agents/skills/README.md",
        "tickets/templates/ticket.md",
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

    declared_paths = set(paths)
    optional = data.get("optional") if isinstance(data.get("optional"), dict) else {}
    for list_key in ("tracked", "ignored"):
        values = optional.get(list_key)
        if isinstance(values, list):
            declared_paths.update(value for value in values if isinstance(value, str))
    retired_paths = sorted(path for path in declared_paths if path.startswith(".farplane/reviews"))
    if retired_paths:
        errors.append(
            f"{rel_path} must not declare retired generic review paths: {', '.join(retired_paths)}; "
            "review evidence belongs in tickets/<ticket>/artifacts/."
        )

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
    heartbeat_records: list[tuple[str, str]] = []
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
        elif automation.get("kind") == "heartbeat":
            heartbeat_records.append(
                (
                    str(automation.get("id") or f"record-{index}"),
                    str(automation.get("prompt") or ""),
                )
            )
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

    if len(heartbeat_records) != 1:
        errors.append(
            f"{rel_path} must define exactly one heartbeat record for Work Pulse; "
            f"found {len(heartbeat_records)}."
        )
    elif "$pulse-update" not in heartbeat_records[0][1]:
        errors.append(
            f"{rel_path} heartbeat {heartbeat_records[0][0]} must invoke $pulse-update."
        )

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
    if "metrics" in data:
        errors.append(f"{rel_path} metrics is retired; semantic definitions belong in farplane/metrics.yaml.")
    if "metric_bindings" in data:
        errors.append(f"{rel_path} metric_bindings is retired; refresh prompts belong in farplane/metrics.yaml.")

    feed_scout = data.get("feed_scout")
    if feed_scout is not None:
        if not isinstance(feed_scout, dict):
            errors.append(f"{rel_path} feed_scout must be an object.")
        else:
            entities = feed_scout.get("entities", {})
            if not isinstance(entities, dict):
                errors.append(f"{rel_path} feed_scout.entities must be an object.")
                entities = {}
            for entity_id, entity in entities.items():
                prefix = f"{rel_path} feed_scout.entities.{entity_id}"
                if not isinstance(entity, dict):
                    errors.append(f"{prefix} must be an object.")
                    continue
                if "interest_prompt" in entity or "source_discovery_prompt" in entity:
                    errors.append(f"{prefix} uses a retired prompt field; use instructions.")
                instructions = entity.get("instructions")
                if instructions is not None and (
                    not isinstance(instructions, str) or not instructions.strip()
                ):
                    errors.append(f"{prefix}.instructions must be a non-empty string.")
                owned_sources = entity.get("owned_sources", {})
                if not isinstance(owned_sources, dict):
                    errors.append(f"{prefix}.owned_sources must be an object.")
                    continue
                for source_id, source in owned_sources.items():
                    source_prefix = f"{prefix}.owned_sources.{source_id}"
                    if not isinstance(source, dict):
                        errors.append(f"{source_prefix} must be an object.")
                        continue
                    if "kind" in source:
                        errors.append(
                            f"{source_prefix}.kind is redundant; encode source identity "
                            "in the source key and coordinates."
                        )
                    if "interest_prompt" in source or "source_discovery_prompt" in source:
                        errors.append(
                            f"{source_prefix} uses a retired prompt field; use instructions."
                        )
                    source_instructions = source.get("instructions")
                    if source_instructions is not None and (
                        not isinstance(source_instructions, str)
                        or not source_instructions.strip()
                    ):
                        errors.append(
                            f"{source_prefix}.instructions must be a non-empty string."
                        )

    integrations = data.get("integrations")
    integrations = integrations if isinstance(integrations, dict) else {}
    kanban = integrations.get("kanban")
    if kanban is not None:
        prefix = f"{rel_path} integrations.kanban"
        if not isinstance(kanban, dict):
            errors.append(f"{prefix} must be an object.")
        else:
            provider = kanban.get("provider")
            if provider not in {"filesystem_tickets", "notion"}:
                errors.append(f"{prefix}.provider must be filesystem_tickets or notion.")
            filesystem_policy = kanban.get("filesystem_ticket_policy")
            if filesystem_policy not in {"include", "exclude"}:
                errors.append(f"{prefix}.filesystem_ticket_policy must be include or exclude.")
            if provider == "filesystem_tickets":
                for field in ("tickets_dir", "archive_dir"):
                    value = kanban.get(field)
                    if not isinstance(value, str) or not value.strip() or Path(value).is_absolute() or ".." in Path(value).parts:
                        errors.append(f"{prefix}.{field} must be a safe project-relative path.")
            if provider == "notion":
                handle = kanban.get("task_source_handle")
                if not isinstance(handle, str) or not re.fullmatch(
                    r"[a-z][a-z0-9_-]*(?:\.[a-z][a-z0-9_-]*)+", handle.strip()
                ):
                    errors.append(f"{prefix}.task_source_handle must name a private handle alias.")
                if filesystem_policy != "exclude":
                    errors.append(f"{prefix}.filesystem_ticket_policy must be exclude for provider notion.")

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


def load_metrics(metrics_file: Path) -> dict[str, dict]:
    if not metrics_file.exists():
        return {}
    try:
        data = yaml.safe_load(metrics_file.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return {}
    metrics = data.get("metrics") if isinstance(data, dict) else {}
    if not isinstance(metrics, dict):
        return {}
    return {str(metric_id): recipe if isinstance(recipe, dict) else {} for metric_id, recipe in metrics.items()}


def read_yaml_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return {}
    return payload if isinstance(payload, dict) else {}


def load_metric_refreshers(metrics_file: Path) -> dict[str, dict]:
    payload = read_yaml_file(metrics_file)
    refreshers = payload.get("refreshers") if isinstance(payload, dict) else {}
    if not isinstance(refreshers, dict):
        return {}
    return {str(key): value if isinstance(value, dict) else {} for key, value in refreshers.items()}


def pydantic_path(error: dict) -> str:
    return ".".join(str(part) for part in error.get("loc", ()))


def validate_metrics_file(root: Path, metrics_file: Path) -> list[str]:
    rel_path = metrics_file.relative_to(root).as_posix()
    try:
        payload = yaml.safe_load(metrics_file.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        return [f"{rel_path} must be valid YAML: {exc}."]
    if not isinstance(payload, dict):
        return [f"{rel_path} must be a YAML object."]
    errors: list[str] = []
    if payload.get("kind") != "project-metrics":
        errors.append(f"{rel_path} must declare kind: project-metrics.")
    if "framework_template_version" not in payload:
        errors.append(f"{rel_path} must declare framework_template_version.")
    if not isinstance(payload.get("metrics"), dict):
        errors.append(f"{rel_path} metrics must be an object.")
    return errors


def validate_metric_definition_schema(metrics: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    allowed_types = {"flow", "stock"}
    allowed_displays = {"bar_plus_cumulative", "reading", "line"}
    for metric_id, definition in sorted(metrics.items()):
        prefix = f"farplane/metrics.yaml metrics.{metric_id}"
        refresh_ref = definition.get("refresh_ref")
        inline_refresh = definition.get("refresh")
        if bool(refresh_ref) == bool(inline_refresh):
            errors.append(f"{prefix} must declare exactly one of refresh_ref or refresh.")
        if "product" in definition:
            errors.append(f"{prefix}.product is retired; metrics are project-level definitions.")
        derived_or_projection_fields = sorted(
            field
            for field in (
                "aggregation",
                "alignment",
                "cadence",
                "compare",
                "cumulative",
                "formula",
                "kind",
                "timezone",
                "window",
                "windows",
            )
            if field in definition
        )
        if derived_or_projection_fields:
            errors.append(
                f"{prefix} uses unsupported derived/projection config: "
                f"{', '.join(derived_or_projection_fields)}; declare only type: "
                "flow|stock and let refreshers emit facts while Core derives window views."
            )
        if "max_age_days" in definition and (
            not isinstance(definition.get("max_age_days"), int) or definition.get("max_age_days", 0) < 1
        ):
            errors.append(f"{prefix}.max_age_days must be a positive integer.")
        guard = definition.get("guard")
        if guard is not None:
            if not isinstance(guard, dict):
                errors.append(f"{prefix}.guard must be an object.")
            else:
                if guard.get("operator") not in {"greater_than_or_equal", "less_than_or_equal"}:
                    errors.append(
                        f"{prefix}.guard.operator must be greater_than_or_equal or less_than_or_equal."
                    )
                if not isinstance(guard.get("threshold"), (int, float)):
                    errors.append(f"{prefix}.guard.threshold must be numeric.")
        try:
            MetricDefinitionModel.model_validate(definition)
        except ValidationError as exc:
            for error in exc.errors():
                field = pydantic_path(error)
                error_type = str(error.get("type") or "")
                if field in {"type", "unit", "direction"} and error_type in {
                    "missing",
                    "value_error",
                    "string_type",
                }:
                    errors.append(f"{prefix}.{field} must be a non-empty string.")
                elif field == "type" and error_type == "literal_error":
                    errors.append(f"{prefix}.type must be one of: {', '.join(sorted(allowed_types))}.")
                elif field == "direction" and error_type == "literal_error":
                    errors.append(f"{prefix}.direction must be maximize or minimize.")
                elif field in {"label", "description"}:
                    errors.append(f"{prefix}.{field} must be a non-empty string when present.")
                elif field == "display" and error_type == "literal_error":
                    errors.append(f"{prefix}.display must be one of: {', '.join(sorted(allowed_displays))}.")
                elif field == "pinned":
                    errors.append(f"{prefix}.pinned must be boolean when present.")
                else:
                    errors.append(f"{prefix}.{field}: {error.get('msg')}.")
    return errors


def validate_metric_refresh_schema(metrics: dict[str, dict], refreshers: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    for refresh_id, refresher in sorted(refreshers.items()):
        prefix = f"farplane/metrics.yaml refreshers.{refresh_id}"
        if not str(refresher.get("refresh") or "").strip():
            errors.append(f"{prefix}.refresh must be a non-empty string.")
        provides = refresher.get("provides")
        if not isinstance(provides, list) or not provides or not all(isinstance(item, str) and item.strip() for item in provides):
            errors.append(f"{prefix}.provides must be a non-empty metric-id list.")
            continue
        unknown = sorted(set(provides) - set(metrics))
        if unknown:
            errors.append(f"{prefix}.provides lacks metric definitions: {', '.join(unknown)}.")
    for metric_id, definition in sorted(metrics.items()):
        refresh_ref = str(definition.get("refresh_ref") or "").strip()
        if refresh_ref and refresh_ref not in refreshers:
            errors.append(f"farplane/metrics.yaml metrics.{metric_id}.refresh_ref is unknown: {refresh_ref}.")
        if refresh_ref and metric_id not in set(refreshers.get(refresh_ref, {}).get("provides") or []):
            errors.append(f"farplane/metrics.yaml refreshers.{refresh_ref}.provides must include {metric_id}.")
    return errors


def observation_batch_files(root: Path) -> list[Path]:
    observation_root = root / ".farplane" / "metrics" / "observations"
    return sorted(observation_root.glob("*/*.json")) if observation_root.exists() else []


def validate_metric_observation_files(root: Path, metrics: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    metric_ids = set(metrics)
    for path in observation_batch_files(root):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path.relative_to(root)} must be valid JSON: {exc.msg}.")
            continue
        if payload.get("schema_version") != 1:
            errors.append(f"{path.relative_to(root)} must declare schema_version: 1 MetricObservationBatch.")
            continue
        try:
            batch = MetricObservationBatch.model_validate(payload)
        except ValidationError as exc:
            for error in exc.errors():
                errors.append(f"{path.relative_to(root)} {pydantic_path(error)}: {error.get('msg')}.")
            continue
        seen: set[tuple[str, str]] = set()
        unknown_metric_ids: set[str] = set()
        duplicates: set[str] = set()
        for row in batch.observations:
            key = (row.metric_id, row.date)
            if key in seen:
                duplicates.add(f"{row.metric_id}@{row.date}")
            seen.add(key)
            if (
                batch.source_id not in ALLOWED_DIAGNOSTIC_SOURCE_IDS
                and row.metric_id not in metric_ids
                and ":" not in row.metric_id
                and row.metric_id not in ALLOWED_DIAGNOSTIC_METRIC_IDS
            ):
                unknown_metric_ids.add(row.metric_id)
        if duplicates:
            errors.append(
                f"{path.relative_to(root)} duplicates metric observations: {', '.join(sorted(duplicates))}."
            )
        if unknown_metric_ids:
            errors.append(
                f"{path.relative_to(root)} observation metric_ids lack metrics.yaml definitions: "
                f"{', '.join(sorted(unknown_metric_ids))}."
            )
    return errors


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
    goals_file = root / "farplane" / "goals.yaml"
    harness_file = root / "farplane" / "harness.yaml"
    metrics_file = root / "farplane" / "metrics.yaml"
    bindings_file = root / "farplane" / "bindings.yaml"
    metrics = load_metrics(metrics_file)
    refreshers = load_metric_refreshers(metrics_file)
    errors: list[str] = []
    if goals_file.exists():
        errors.append(
            "farplane/goals.yaml is retired; move the human charter and selected metric refs to harness.yaml, "
            "metric definitions to metrics.yaml, and temporary commitments to tickets."
        )
    if metrics_file.exists():
        errors.extend(validate_metrics_file(root, metrics_file))
    errors.extend(validate_metric_definition_schema(metrics))
    errors.extend(validate_metric_refresh_schema(metrics, refreshers))
    errors.extend(validate_metric_observation_files(root, metrics))
    metrics_payload = read_yaml_file(metrics_file)
    if "optimization" in metrics_payload:
        errors.append(
            "farplane/metrics.yaml optimization is retired; definitions own direction, freshness, and guard rules, "
            "while farplane/harness.yaml selects active objectives and guards."
        )
    harness = load_harness(harness_file)
    objective_rows, area_metric_rows, guard_ids = selected_metric_rows(harness)
    objective_ids = {
        str(row.get("metric_id") or "").strip()
        for row in objective_rows
        if str(row.get("metric_id") or "").strip()
    }
    area_metric_ids = {
        str(row.get("metric_id") or "").strip()
        for row in area_metric_rows
        if str(row.get("metric_id") or "").strip()
    }
    selected_ids = objective_ids | area_metric_ids | set(guard_ids) | problem_metric_ids(harness)
    planning_control_ids = objective_ids | set(guard_ids)
    unknown_selected_ids = sorted(selected_ids - set(metrics))
    if unknown_selected_ids:
        errors.append(
            "farplane/harness.yaml metric refs lack metrics.yaml definitions: "
            f"{', '.join(unknown_selected_ids)}."
        )
    metric_definitions_without_direction = sorted(
        metric_id
        for metric_id, definition in metrics.items()
        if definition.get("direction") not in {"maximize", "minimize"}
    )
    selected_definitions_without_freshness = sorted(
        metric_id
        for metric_id in planning_control_ids
        if metric_id in metrics
        and (not isinstance(metrics[metric_id].get("max_age_days"), int) or metrics[metric_id]["max_age_days"] < 1)
    )
    if metric_definitions_without_direction:
        errors.append(
            "farplane/metrics.yaml metric definitions must declare direction: "
            f"{', '.join(metric_definitions_without_direction)}."
        )
    if selected_definitions_without_freshness:
        errors.append(
            "farplane/metrics.yaml selected definitions must declare positive max_age_days: "
            f"{', '.join(selected_definitions_without_freshness)}."
        )
    selected_guard_ids = set(guard_ids)
    defined_guard_ids = {
        metric_id
        for metric_id, definition in metrics.items()
        if isinstance(definition.get("guard"), dict)
    }
    missing_guard_rules = sorted(selected_guard_ids - defined_guard_ids)
    unselected_guard_rules = sorted(defined_guard_ids - selected_guard_ids)
    if missing_guard_rules:
        errors.append(
            "farplane/harness.yaml guard refs lack metrics.yaml guard rules: "
            f"{', '.join(missing_guard_rules)}."
        )
    if unselected_guard_rules:
        errors.append(
            "farplane/metrics.yaml guard definitions must be selected by harness.yaml metric_refs.guards: "
            f"{', '.join(unselected_guard_rules)}."
        )


    selected_metrics_without_unit = sorted(
        kpi_id
        for kpi_id in selected_ids
        if kpi_id in metrics and not str(metrics[kpi_id].get("unit") or "").strip()
    )
    if selected_metrics_without_unit:
        errors.append(
            "farplane/metrics.yaml selected metric definitions lack unit: "
            f"{', '.join(selected_metrics_without_unit)}."
        )

    errors.extend(validate_snapshot_freshness(root, root / ".farplane" / "project" / "ui" / "latest.json"))
    return errors


def load_harness(harness_file: Path) -> dict[str, Any]:
    return read_yaml_file(harness_file)


def selected_metric_rows(
    harness: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    metric_refs = harness.get("metric_refs") if isinstance(harness.get("metric_refs"), dict) else {}
    project_rows = metric_refs.get("objectives") if isinstance(metric_refs.get("objectives"), list) else []
    objective_rows = [row for row in project_rows if isinstance(row, dict)]
    area_rows: list[dict[str, Any]] = []
    areas = harness.get("areas") if isinstance(harness.get("areas"), dict) else {}
    for area_id, area in areas.items():
        if not isinstance(area, dict):
            continue
        area_refs = area.get("metric_refs") if isinstance(area.get("metric_refs"), list) else []
        area_rows.extend(
            {**row, "area_id": str(area_id)}
            for row in area_refs
            if isinstance(row, dict)
        )
    guards = metric_refs.get("guards") if isinstance(metric_refs.get("guards"), list) else []
    return (
        objective_rows,
        area_rows,
        [str(metric_id).strip() for metric_id in guards if isinstance(metric_id, str) and metric_id.strip()],
    )


def problem_metric_ids(harness: dict[str, Any]) -> set[str]:
    identity = harness.get("identity") if isinstance(harness.get("identity"), dict) else {}
    problems = identity.get("problems") if isinstance(identity.get("problems"), list) else []
    return {
        metric_id.strip()
        for problem in problems
        if isinstance(problem, dict)
        for metric_id in (problem.get("metric_refs") if isinstance(problem.get("metric_refs"), list) else [])
        if isinstance(metric_id, str) and metric_id.strip()
    }


def project_skill_ids(root: Path) -> set[str]:
    ids: set[str] = set()
    registry = root / "docs" / "skills" / "registry.jsonl"
    if registry.exists():
        for line in registry.read_text(encoding="utf-8").splitlines():
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(row, dict) and isinstance(row.get("name"), str):
                ids.add(row["name"])
    for skill_path in (root / ".agents" / "skills").glob("*/SKILL.md"):
        ids.add(skill_path.parent.name)
    return ids


def validate_harness_file(root: Path, harness_file: Path) -> list[str]:
    rel_path = harness_file.relative_to(root).as_posix()
    payload = load_harness(harness_file)
    if not payload:
        return [f"{rel_path} must be a non-empty YAML object."]
    errors: list[str] = []
    is_draft = payload.get("status") == "draft"
    extra = sorted(set(payload) - HARNESS_ALLOWED_TOP_LEVEL)
    if extra:
        errors.append(f"{rel_path} has unsupported keys: {', '.join(extra)}.")
    if payload.get("kind") != "project-harness":
        errors.append(f"{rel_path} must declare kind: project-harness.")
    if not isinstance(payload.get("framework_template_version"), str):
        errors.append(f"{rel_path} must declare framework_template_version.")

    identity = payload.get("identity") if isinstance(payload.get("identity"), dict) else {}
    unsupported_identity = sorted(
        set(identity) - {"mission", "human_thesis", "north_star", "problems"}
    )
    if unsupported_identity:
        errors.append(
            f"{rel_path} identity has unsupported fields: {', '.join(unsupported_identity)}."
        )
    if "product_bets" in identity:
        errors.append(
            f"{rel_path} identity.product_bets is retired; bind stable identity.problems "
            "and keep mutable solution choices, order, deadlines, and proof on tickets."
        )
    if "goals" in payload:
        errors.append(
            f"{rel_path} goals is retired; keep objective metric movement in metric observations "
            "and mutable urgency, due dates, and proof on tickets."
        )
    for field in ("mission", "human_thesis", "north_star"):
        if not isinstance(identity.get(field), str) or not identity.get(field, "").strip():
            errors.append(f"{rel_path} identity.{field} must be a non-empty string.")

    raw_version = payload.get("framework_template_version")
    try:
        version_parts = tuple(int(part) for part in str(raw_version).split("."))
    except ValueError:
        version_parts = ()
    portfolio_required = version_parts >= (0, 5, 2)
    problems = identity.get("problems")
    problem_ids: list[str] = []
    if portfolio_required or problems is not None:
        if not isinstance(problems, list) or not problems:
            errors.append(f"{rel_path} identity.problems must be a non-empty list.")
            problems = []
        for index, problem in enumerate(problems):
            prefix = f"{rel_path} identity.problems[{index}]"
            if not isinstance(problem, dict):
                errors.append(f"{prefix} must be an object.")
                continue
            unsupported = sorted(set(problem) - {"id", "statement", "metric_refs", "measurement_gap"})
            if unsupported:
                errors.append(f"{prefix} has unsupported fields: {', '.join(unsupported)}.")
            raw_problem_id = problem.get("id")
            problem_id = raw_problem_id.strip() if isinstance(raw_problem_id, str) else ""
            if not problem_id:
                errors.append(f"{prefix}.id must be a non-empty string.")
            else:
                problem_ids.append(problem_id)
            if not isinstance(problem.get("statement"), str) or not problem.get("statement", "").strip():
                errors.append(f"{prefix}.statement must be a non-empty string.")
            metric_ids = problem.get("metric_refs")
            if not isinstance(metric_ids, list) or any(
                not isinstance(metric_id, str) or not metric_id.strip() for metric_id in metric_ids
            ):
                errors.append(f"{prefix}.metric_refs must be a list of non-empty strings.")
            elif len(metric_ids) != len(set(metric_ids)):
                errors.append(f"{prefix}.metric_refs must not contain duplicates.")
            if "measurement_gap" in problem and (
                not isinstance(problem.get("measurement_gap"), str)
                or not problem.get("measurement_gap", "").strip()
            ):
                errors.append(f"{prefix}.measurement_gap must be a non-empty string when present.")
    duplicate_problem_ids = sorted(
        {problem_id for problem_id in problem_ids if problem_ids.count(problem_id) > 1}
    )
    if duplicate_problem_ids:
        errors.append(f"{rel_path} identity problem IDs must be unique: {', '.join(duplicate_problem_ids)}.")

    refs = payload.get("metric_refs") if isinstance(payload.get("metric_refs"), dict) else {}
    if not isinstance(refs.get("objectives"), list) or not refs.get("objectives"):
        errors.append(f"{rel_path} metric_refs.objectives must be a non-empty list.")
    if not isinstance(refs.get("guards"), list):
        errors.append(f"{rel_path} metric_refs.guards must be a list.")

    objective_rows, _area_metric_rows, guard_ids = selected_metric_rows(payload)
    priorities: list[int] = []
    objective_ids: list[str] = []
    for index, row in enumerate(objective_rows):
        metric_id = str(row.get("metric_id") or "").strip()
        priority = row.get("priority")
        if not metric_id:
            errors.append(f"{rel_path} objective metric ref {index} must declare metric_id.")
        else:
            objective_ids.append(metric_id)
        if not isinstance(priority, int) or priority < 1:
            errors.append(f"{rel_path} objective metric ref {index}.priority must be a positive integer.")
        else:
            priorities.append(priority)
    duplicates = sorted({metric_id for metric_id in objective_ids if objective_ids.count(metric_id) > 1})
    if duplicates:
        errors.append(f"{rel_path} objective metric refs must be unique: {', '.join(duplicates)}.")
    if len(priorities) != len(set(priorities)):
        errors.append(f"{rel_path} objective priorities must be unique.")
    if len(guard_ids) != len(set(guard_ids)):
        errors.append(f"{rel_path} metric_refs.guards must not contain duplicates.")

    known_skills = project_skill_ids(root)
    planning = payload.get("planning")
    if not isinstance(planning, dict):
        errors.append(f"{rel_path} planning must be an object.")
    else:
        unsupported_planning = sorted(set(planning) - {"skill_refs"})
        if unsupported_planning:
            errors.append(
                f"{rel_path} planning has unsupported fields: {', '.join(unsupported_planning)}."
            )
        planning_skill_refs = planning.get("skill_refs")
        if (
            not isinstance(planning_skill_refs, list)
            or not planning_skill_refs
            or any(not isinstance(skill_id, str) or not skill_id.strip() for skill_id in planning_skill_refs)
        ):
            errors.append(f"{rel_path} planning.skill_refs must be a non-empty list of strings.")
        else:
            duplicate_planning_skills = sorted(
                {skill_id for skill_id in planning_skill_refs if planning_skill_refs.count(skill_id) > 1}
            )
            if duplicate_planning_skills:
                errors.append(
                    f"{rel_path} planning.skill_refs must be unique: {', '.join(duplicate_planning_skills)}."
                )
            dangling_planning_skills = sorted(
                skill_id for skill_id in planning_skill_refs if skill_id not in known_skills
            )
            if dangling_planning_skills:
                errors.append(
                    f"{rel_path} planning.skill_refs are unresolved: {', '.join(dangling_planning_skills)}."
                )

    areas = payload.get("areas") if isinstance(payload.get("areas"), dict) else {}
    if not areas:
        errors.append(f"{rel_path} areas must declare at least one planning area.")
    for area_id, area in areas.items():
        prefix = f"{rel_path} areas.{area_id}"
        if not isinstance(area, dict):
            errors.append(f"{prefix} must be an object.")
            continue
        unsupported = sorted(set(area) - AREA_ALLOWED_FIELDS)
        if unsupported:
            errors.append(f"{prefix} has controller or unsupported fields: {', '.join(unsupported)}.")
        if not isinstance(area.get("description"), str) or not area.get("description", "").strip():
            errors.append(f"{prefix}.description must be a non-empty string.")
        icp = area.get("icp")
        if not isinstance(icp, dict):
            if not is_draft:
                errors.append(f"{prefix}.icp must be an object.")
        else:
            unsupported_icp = sorted(set(icp) - ICP_ALLOWED_FIELDS)
            if unsupported_icp:
                errors.append(f"{prefix}.icp has unsupported fields: {', '.join(unsupported_icp)}.")
            for field in ("label", "description", "evidence_bar"):
                if not isinstance(icp.get(field), str) or not icp.get(field, "").strip():
                    errors.append(f"{prefix}.icp.{field} must be a non-empty string.")
            for field in ("jobs_to_be_done", "pain_points"):
                values = icp.get(field)
                if (
                    not isinstance(values, list)
                    or not values
                    or any(not isinstance(value, str) or not value.strip() for value in values)
                ):
                    errors.append(f"{prefix}.icp.{field} must be a non-empty list of strings.")
        skill_refs = area.get("skill_refs") if isinstance(area.get("skill_refs"), list) else []
        if not skill_refs and not is_draft:
            errors.append(f"{prefix}.skill_refs must be a non-empty list.")
        dangling = sorted(str(skill_id) for skill_id in skill_refs if str(skill_id) not in known_skills)
        if dangling:
            errors.append(f"{prefix}.skill_refs are unresolved: {', '.join(dangling)}.")
        if not isinstance(area.get("metric_refs"), list) or not area.get("metric_refs"):
            errors.append(f"{prefix}.metric_refs must be a non-empty list.")

    if not isinstance(payload.get("feature_definition"), dict):
        errors.append(f"{rel_path} feature_definition must be an object.")
    if not isinstance(payload.get("constraints"), dict):
        errors.append(f"{rel_path} constraints must be an object.")
    if not isinstance(payload.get("authority"), dict):
        errors.append(f"{rel_path} authority must be an object.")
    if not isinstance(payload.get("change_rule"), str) or not payload.get("change_rule", "").strip():
        errors.append(f"{rel_path} change_rule must be a non-empty string.")
    return errors


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    framework_dir = root / "farplane"
    framework_manifest = framework_dir / "manifest.json"
    automations_toml = framework_dir / "automations.toml"
    bindings = framework_dir / "bindings.yaml"
    metrics = framework_dir / "metrics.yaml"
    harness = framework_dir / "harness.yaml"
    retired_harness_markdown = framework_dir / "harness.md"
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
        errors.append("farplane/file-growth-hook.json is retired; remove the automatic file-growth hook config.")
    if duplicate_project_charter.exists():
        errors.append(
            "farplane/project.md would duplicate the active typed charter; use farplane/harness.yaml "
            "unless a versioned framework migration replaces it."
        )
    if retired_harness_markdown.exists():
        errors.append("farplane/harness.md is retired; use farplane/harness.yaml.")

    if not automations_toml.exists():
        errors.append("farplane/automations.toml is required for full Codex automation configs.")
    else:
        errors.extend(validate_automations_toml(root, automations_toml))

    if not harness.exists():
        errors.append("farplane/harness.yaml is required for the typed project charter.")
    else:
        errors.extend(validate_harness_file(root, harness))

    products_json = root / "farplane" / "products.json"
    products_dir = root / "farplane" / "products"
    if products_json.exists():
        errors.append("farplane/products.json is retired; objective metrics and tickets are the project primitives.")
    if products_dir.exists():
        errors.append("farplane/products/ is retired; keep reusable artifact workflows as skills.")

    if pm_manifest.exists():
        errors.extend(validate_pm_manifest(root, pm_manifest))

    if not bindings.exists():
        errors.append("farplane/bindings.yaml is required for project bindings.")
    else:
        errors.extend(validate_bindings_file(root, bindings))

    if not metrics.exists():
        errors.append("farplane/metrics.yaml is required for project metric definitions.")

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
