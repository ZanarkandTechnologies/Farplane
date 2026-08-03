#!/usr/bin/env python3
"""Scaffold and run harness-native evals for Codex and Claude."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence


DEFAULT_MAX_PARALLEL_TASKS = 2
TASK_FILES = {
    "harness": "harness_tasks.json",
    "agents-md": "agents_md_tasks.json",
}
ALL_SCOPES = ("harness", "agents-md", "skills")
SKILL_EVAL_TASK_FILE = Path("evals/evals.json")
REQUIRED_EVAL_FILES = (
    "run_evals.py",
    "config.json",
    "contexts/agi-toy-shop.md",
    "prompts/agent.md",
    "prompts/judge.md",
    "schemas/behavior-report.schema.json",
    "tasks/harness_tasks.json",
    "tasks/agents_md_tasks.json",
)
BEHAVIOR_REPORT_VERDICTS = {"pass", "fail", "blocked"}
BEHAVIOR_CHECKPOINT_STATUSES = {"done", "skipped", "blocked"}
RELIABILITY_COMPATIBILITY_FIELDS = (
    "harness",
    "judge_harness",
    "skill_context",
    "compare_baseline",
    "behavior_trace",
    "scopes",
    "task_files",
)
IMAGE_SUFFIXES = {".avif", ".gif", ".jpeg", ".jpg", ".png", ".svg", ".webp"}


class EvalError(ValueError):
    """Raised when eval input, command execution, or judge output is invalid."""


@dataclass(frozen=True)
class EvalTask:
    id: str
    title: str
    context: str
    query: str
    reference_points: tuple[str, ...]
    files: tuple[str, ...]
    tags: tuple[str, ...]
    notes: str
    required_successful_command_regexes: tuple[str, ...]


@dataclass(frozen=True)
class CommandResult:
    text: str
    returncode: int
    raw_stdout: str
    raw_stderr: str
    duration_ms: int
    total_tokens: int | None


@dataclass(frozen=True)
class EvalConfig:
    default_context: str
    default_context_file: str


def script_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_eval_dir(harness: str, target_root: Path) -> Path:
    if harness in {"codex", "claude"}:
        return target_root / ".farplane" / "evals"
    raise EvalError("custom harness requires --eval-dir")


def read_text(path: Path) -> str:
    try:
        return path.read_text()
    except FileNotFoundError as exc:
        raise EvalError(f"file not found: {path}") from exc


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError as exc:
        raise EvalError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise EvalError(f"{path}: invalid JSON: {exc}") from exc


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def read_json_lines(text: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for line in text.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict):
            events.append(event)
    return events


def extract_total_tokens(raw_stdout: str) -> int | None:
    """Read the last available total-token value from a JSONL harness stream."""
    total: int | None = None
    for event in read_json_lines(raw_stdout):
        usage = event.get("usage")
        if not isinstance(usage, dict):
            continue
        explicit = usage.get("total_tokens")
        if isinstance(explicit, int):
            total = explicit
            continue
        input_tokens = usage.get("input_tokens")
        output_tokens = usage.get("output_tokens")
        if isinstance(input_tokens, int) and isinstance(output_tokens, int):
            total = input_tokens + output_tokens
    return total


def parse_json_object(text: str) -> dict[str, Any] | None:
    stripped = text.strip()
    if not stripped:
        return None
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    try:
        value = json.loads(stripped)
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def validate_json_schema(value: Any, schema: Any, path: str = "$") -> list[str]:
    """Validate the compact JSON Schema subset used by behavior reports."""
    if not isinstance(schema, dict):
        return [f"{path}: schema must be an object"]
    errors: list[str] = []
    expected_type = schema.get("type")
    type_map = {
        "object": dict,
        "array": list,
        "string": str,
        "number": (int, float),
        "integer": int,
        "boolean": bool,
        "null": type(None),
    }
    if isinstance(expected_type, str) and expected_type in type_map:
        expected_python = type_map[expected_type]
        valid_type = isinstance(value, expected_python)
        if expected_type in {"number", "integer"} and isinstance(value, bool):
            valid_type = False
        if not valid_type:
            return [f"{path}: expected {expected_type}"]
    if "enum" in schema and value not in schema.get("enum", []):
        errors.append(f"{path}: value is not in enum")
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: value does not match const")
    if isinstance(value, dict):
        required = schema.get("required", [])
        if isinstance(required, list):
            for key in required:
                if isinstance(key, str) and key not in value:
                    errors.append(f"{path}: missing required property {key}")
        properties = schema.get("properties", {})
        if isinstance(properties, dict):
            for key, child_schema in properties.items():
                if key in value:
                    errors.extend(validate_json_schema(value[key], child_schema, f"{path}.{key}"))
        if schema.get("additionalProperties") is False and isinstance(properties, dict):
            for key in value.keys() - properties.keys():
                errors.append(f"{path}: unexpected property {key}")
    if isinstance(value, list):
        if isinstance(schema.get("minItems"), int) and len(value) < schema["minItems"]:
            errors.append(f"{path}: expected at least {schema['minItems']} items")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(validate_json_schema(item, item_schema, f"{path}[{index}]"))
    return errors


def snapshot_files(root: Path, excluded_root: Path) -> dict[str, tuple[int, int]]:
    ignored_names = {".git", "node_modules", "__pycache__", ".venv", "venv"}
    snapshot: dict[str, tuple[int, int]] = {}
    root = root.resolve()
    excluded_root = excluded_root.resolve()
    for current, dirs, files in os.walk(root):
        current_path = Path(current).resolve()
        dirs[:] = [
            name
            for name in dirs
            if name not in ignored_names
            and not (current_path / name).resolve().is_relative_to(excluded_root)
        ]
        if current_path.is_relative_to(excluded_root):
            continue
        for name in files:
            path = current_path / name
            try:
                stat = path.stat()
                relative = path.resolve().relative_to(root).as_posix()
            except (FileNotFoundError, ValueError):
                continue
            snapshot[relative] = (stat.st_size, stat.st_mtime_ns)
    return snapshot


def snapshot_delta(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> dict[str, list[str]]:
    return {
        "created": sorted(after.keys() - before.keys()),
        "modified": sorted(path for path in before.keys() & after.keys() if before[path] != after[path]),
        "deleted": sorted(before.keys() - after.keys()),
    }


def require_string(raw: dict[str, Any], field: str, path: Path) -> str:
    value = raw.get(field)
    if not isinstance(value, str) or not value.strip():
        raise EvalError(f"{path}: {field} must be a non-empty string")
    return value.strip()


def load_eval_config(eval_dir: Path) -> EvalConfig:
    config_path = eval_dir / "config.json"
    if not config_path.exists():
        return EvalConfig(default_context="", default_context_file="")
    raw = read_json(config_path)
    if not isinstance(raw, dict):
        raise EvalError(f"{config_path}: config must be a JSON object")
    inline_context = str(raw.get("default_context", "")).strip()
    context_file = str(raw.get("default_context_file", "")).strip()
    if inline_context and context_file:
        raise EvalError(f"{config_path}: use default_context or default_context_file, not both")
    if context_file:
        context_path = (config_path.parent / context_file).resolve()
        if not context_path.is_relative_to(config_path.parent.resolve()):
            raise EvalError(f"{config_path}: default_context_file must stay inside eval dir")
        return EvalConfig(default_context=read_text(context_path).strip(), default_context_file=context_file)
    return EvalConfig(default_context=inline_context, default_context_file="")


def task_context(raw: dict[str, Any], default_context: str) -> str:
    if "context" not in raw:
        return default_context
    return str(raw.get("context", "")).strip()


def normalize_task_rows(
    raw: Any,
    path: Path,
    task_ids: set[str] | None = None,
) -> list[dict[str, Any]]:
    if isinstance(raw, list):
        if not task_ids:
            return raw
        return [item for item in raw if isinstance(item, dict) and str(item.get("id", "")) in task_ids]
    if isinstance(raw, dict) and isinstance(raw.get("evals"), list):
        rows: list[dict[str, Any]] = []
        for item in raw["evals"]:
            if not isinstance(item, dict):
                raise EvalError(f"{path}: each eval must be an object")
            if task_ids and str(item.get("id", "")) not in task_ids:
                continue
            metadata = item.get("metadata", {})
            farplane = metadata.get("farplane", {}) if isinstance(metadata, dict) else {}
            if not isinstance(farplane, dict):
                farplane = {}
            assertions = item.get("assertions")
            if not assertions and isinstance(item.get("expected_output"), str):
                assertions = [item["expected_output"]]
            row = {
                "id": str(item.get("id", "")),
                "title": farplane.get("title") or item.get("expected_output") or str(item.get("id", "")),
                "query": item.get("prompt"),
                "reference_points": assertions,
                "files": item.get("files", []),
                "tags": farplane.get("tags", []),
                "notes": farplane.get("notes", ""),
            }
            behavior_requirements = farplane.get("behavior_requirements", {})
            if isinstance(behavior_requirements, dict):
                row["behavior_requirements"] = behavior_requirements
            if "context" in farplane:
                row["context"] = farplane["context"]
            rows.append(row)
        return rows
    raise EvalError(f"{path}: task file must contain a JSON list or an Agent Skills evals object")


def load_tasks(
    path: Path,
    limit: int | None = None,
    default_context: str = "",
    task_ids: set[str] | None = None,
    target_root: Path | None = None,
) -> list[EvalTask]:
    raw = read_json(path)
    raw = normalize_task_rows(raw, path, task_ids=task_ids)
    tasks: list[EvalTask] = []
    for item in raw:
        if not isinstance(item, dict):
            raise EvalError(f"{path}: each task must be an object")
        refs = item.get("reference_points")
        if not isinstance(refs, list) or not refs or not all(isinstance(ref, str) and ref.strip() for ref in refs):
            raise EvalError(f"{path}: task {item.get('id', '<unknown>')} reference_points must be non-empty strings")
        tags = item.get("tags", [])
        if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
            raise EvalError(f"{path}: task {item.get('id', '<unknown>')} tags must be strings")
        files = item.get("files", [])
        if not isinstance(files, list) or not all(isinstance(file, str) and file.strip() for file in files):
            raise EvalError(f"{path}: task {item.get('id', '<unknown>')} files must be non-empty strings")
        resolved_root = (target_root or path.parent).resolve()
        normalized_files: list[str] = []
        for file in files:
            relative = Path(file.strip())
            if relative.is_absolute():
                raise EvalError(f"{path}: task {item.get('id', '<unknown>')} file must be target-root relative: {file}")
            source = (resolved_root / relative).resolve()
            if not source.is_relative_to(resolved_root):
                raise EvalError(f"{path}: task {item.get('id', '<unknown>')} file escapes target root: {file}")
            if not source.is_file():
                raise EvalError(f"{path}: task {item.get('id', '<unknown>')} file not found: {file}")
            normalized_files.append(relative.as_posix())
        behavior_requirements = item.get("behavior_requirements", {})
        if not isinstance(behavior_requirements, dict):
            raise EvalError(
                f"{path}: task {item.get('id', '<unknown>')} behavior_requirements must be an object"
            )
        command_regexes = behavior_requirements.get("required_successful_command_regexes", [])
        if not isinstance(command_regexes, list) or not all(
            isinstance(pattern, str) and pattern.strip() for pattern in command_regexes
        ):
            raise EvalError(
                f"{path}: task {item.get('id', '<unknown>')} required_successful_command_regexes must be non-empty strings"
            )
        for pattern in command_regexes:
            try:
                re.compile(pattern)
            except re.error as exc:
                raise EvalError(
                    f"{path}: task {item.get('id', '<unknown>')} invalid command regex {pattern!r}: {exc}"
                ) from exc
        tasks.append(
            EvalTask(
                id=require_string(item, "id", path),
                title=require_string(item, "title", path),
                context=task_context(item, default_context),
                query=require_string(item, "query", path),
                reference_points=tuple(ref.strip() for ref in refs),
                files=tuple(normalized_files),
                tags=tuple(tag.strip() for tag in tags if tag.strip()),
                notes=str(item.get("notes", "")).strip(),
                required_successful_command_regexes=tuple(
                    pattern.strip() for pattern in command_regexes
                ),
            )
        )
    return tasks[:limit] if limit else tasks


def resolve_skill_task_paths(target_root: Path) -> list[Path]:
    skills_dir = target_root / "skills"
    if not skills_dir.exists():
        return []
    paths: list[Path] = []
    for skill_dir in sorted(path for path in skills_dir.iterdir() if path.is_dir()):
        eval_file = skill_dir / SKILL_EVAL_TASK_FILE
        if eval_file.is_file():
            paths.append(eval_file)
    return paths


def normalize_skill_selector(selector: str) -> str:
    value = selector.strip().strip("/")
    if not value:
        raise EvalError("--skill values must be non-empty")
    parts = Path(value).parts
    if len(parts) >= 4 and parts[-2:] == SKILL_EVAL_TASK_FILE.parts and parts[-4] == "skills":
        return parts[-3]
    if len(parts) >= 2 and parts[-2] == "skills":
        return parts[-1]
    return value


def expand_skill_selectors(selectors: Sequence[str]) -> set[str]:
    expanded: set[str] = set()
    for selector in selectors:
        expanded.update(normalize_skill_selector(part) for part in selector.split(",") if part.strip())
    return expanded


def skill_name_for_task_path(path: Path, target_root: Path) -> str | None:
    try:
        relative = path.resolve().relative_to(target_root.resolve())
    except ValueError:
        return None
    parts = relative.parts
    if len(parts) == 4 and parts[0] == "skills" and parts[2:] == SKILL_EVAL_TASK_FILE.parts:
        return parts[1]
    return None


def filter_skill_task_paths(paths: Sequence[Path], target_root: Path, selectors: Sequence[str]) -> list[Path]:
    wanted = expand_skill_selectors(selectors)
    if not wanted:
        return list(paths)
    available: dict[str, Path] = {}
    for path in paths:
        skill_name = skill_name_for_task_path(path, target_root)
        if skill_name:
            available[skill_name] = path
    missing = sorted(wanted - set(available))
    if missing:
        available_text = ", ".join(sorted(available)) or "none"
        raise EvalError(f"requested skill evals not found: {', '.join(missing)}; available: {available_text}")
    return [available[name] for name in sorted(wanted)]


def selected_scopes(args: argparse.Namespace) -> tuple[tuple[str, ...], bool]:
    scopes: list[str] = []
    if args.harness_evals:
        scopes.append("harness")
    if args.agents_md:
        scopes.append("agents-md")
    if args.skills or args.skill:
        scopes.append("skills")
    if scopes:
        return tuple(dict.fromkeys(scopes)), True
    return ALL_SCOPES, False


def resolve_task_paths(
    eval_dir: Path,
    tasks: str | None,
    scopes: Sequence[str],
    target_root: Path,
    require_scopes: bool = False,
) -> list[Path]:
    if tasks:
        return [Path(tasks)]
    paths: list[Path] = []
    for scope in scopes:
        if scope == "skills":
            skill_paths = resolve_skill_task_paths(target_root)
            if skill_paths:
                paths.extend(skill_paths)
            elif require_scopes:
                raise EvalError(f"no skill eval task files found under {target_root / 'skills'}/*/{SKILL_EVAL_TASK_FILE.as_posix()}")
            continue
        if scope not in TASK_FILES:
            raise EvalError(f"unknown eval scope: {scope}")
        path = eval_dir / "tasks" / TASK_FILES[scope]
        if path.exists():
            paths.append(path)
        elif require_scopes:
            raise EvalError(f"requested eval scope {scope} is missing task file: {path}")
    if not paths:
        scope_text = ", ".join(scopes) or "none"
        raise EvalError(f"no eval task files found for scopes: {scope_text}")
    return paths


def skill_context_for_task_file(path: Path, target_root: Path) -> str:
    """Return the owning SKILL.md context for a skill-local eval file."""
    resolved_path = path.resolve()
    resolved_root = target_root.resolve()
    try:
        relative = resolved_path.relative_to(resolved_root)
    except ValueError:
        return ""
    skill_name = skill_name_for_task_path(resolved_path, resolved_root)
    if not skill_name:
        return ""
    skill_path = resolved_root / "skills" / skill_name / "SKILL.md"
    if not skill_path.exists():
        return ""
    return (
        f"Skill under evaluation: {skill_name}\n"
        f"Source file: {skill_path.relative_to(resolved_root)}\n\n"
        "Skill context:\n\n"
        f"{read_text(skill_path).strip()}"
    )


def compose_task_context(default_context: str, skill_context: str) -> str:
    parts = [part.strip() for part in (default_context, skill_context) if part and part.strip()]
    return "\n\n---\n\n".join(parts)


def load_task_suite(
    paths: Sequence[Path],
    limit: int | None = None,
    default_context: str = "",
    target_root: Path | None = None,
    task_ids: set[str] | None = None,
    native_skill_context: bool = False,
) -> list[EvalTask]:
    loaded: list[EvalTask] = []
    resolved_root = target_root.resolve() if target_root else Path.cwd().resolve()
    for path in paths:
        skill_context = "" if native_skill_context else skill_context_for_task_file(path, resolved_root)
        loaded.extend(
            load_tasks(
                path,
                default_context=compose_task_context(default_context, skill_context),
                task_ids=task_ids,
                target_root=resolved_root,
            )
        )
    if task_ids:
        loaded = [task for task in loaded if task.id in task_ids]
        missing = sorted(task_ids - {task.id for task in loaded})
        if missing:
            raise EvalError(f"requested task ids not found: {', '.join(missing)}")
    return loaded[:limit] if limit else loaded


def uses_native_skill_context(harness: str, agent_profile: str | None) -> bool:
    return harness == "codex" and bool(agent_profile)


def task_to_json(task: EvalTask) -> str:
    payload = {
        "id": task.id,
        "title": task.title,
        "query": task.query,
        "reference_points": list(task.reference_points),
        "files": list(task.files),
        "tags": list(task.tags),
        "notes": task.notes,
    }
    if task.context:
        payload["context"] = task.context
    return json.dumps(payload, indent=2)


def render_template(template: str, task: EvalTask, answer: str = "") -> str:
    rendered = template
    context_block = f"Context:\n{task.context}\n\n" if task.context else ""
    replacements = {
        "{context}": task.context,
        "{context_block}": context_block,
        "{query}": task.query,
        "{task_json}": task_to_json(task),
        "{answer}": answer,
        "{reference_points}": json.dumps(list(task.reference_points), indent=2),
    }
    for placeholder, value in replacements.items():
        rendered = rendered.replace(placeholder, value)
    return rendered


def stage_task_files(task: EvalTask, target_root: Path, task_dir: Path) -> EvalTask:
    if not task.files:
        return task
    fixture_root = task_dir / "fixtures"
    manifest: list[str] = []
    for relative_text in task.files:
        relative = Path(relative_text)
        source = (target_root / relative).resolve()
        destination = fixture_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        destination.chmod(0o444)
        manifest.append(f"- {relative.as_posix()}: {destination.resolve()}")
    fixture_context = (
        "Eval fixture files (staged read-only copies; use these paths instead of live source files):\n"
        + "\n".join(manifest)
    )
    context = compose_task_context(task.context, fixture_context)
    return EvalTask(
        id=task.id,
        title=task.title,
        context=context,
        query=task.query,
        reference_points=task.reference_points,
        files=task.files,
        tags=task.tags,
        notes=task.notes,
        required_successful_command_regexes=task.required_successful_command_regexes,
    )


def build_job_id(label: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "-", label.strip().lower()).strip("-") or "run"
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"{stamp}-{safe}"


def extract_json_object(text: str) -> dict[str, Any]:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", stripped, flags=re.DOTALL)
        if not match:
            raise EvalError("judge output did not contain a JSON object")
        parsed = json.loads(match.group(0))
    if not isinstance(parsed, dict):
        raise EvalError("judge output JSON must be an object")
    return parsed


def strings_in_json(value: Any) -> list[str]:
    strings: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            strings.append(str(key))
            strings.extend(strings_in_json(item))
    elif isinstance(value, list):
        for item in value:
            strings.extend(strings_in_json(item))
    elif isinstance(value, str):
        strings.append(value)
    return strings


def skill_event_match(event: Any, target_skill: str) -> bool:
    if not isinstance(event, dict):
        return False
    target = target_skill.strip().lower()
    if not target:
        return False
    lowered = [text.lower() for text in strings_in_json(event)]
    has_target = any(
        text == target
        or text.endswith(f"/{target}")
        or f'"{target}"' in text
        or f"name: {target}" in text
        or f"/skills/{target}/skill.md" in text
        for text in lowered
    )
    has_skill_marker = any("skill" in text for text in lowered)
    return has_target and has_skill_marker


def detect_skill_triggered(raw_stdout: str, target_skill: str) -> bool | None:
    """Return whether Codex JSONL shows the target skill loaded.

    The exact event payload can vary by Codex version, so this parser is
    intentionally conservative: JSONL with no skill event returns False, while
    non-JSON output returns None.
    """
    saw_json = False
    for line in raw_stdout.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        try:
            event = json.loads(stripped)
        except json.JSONDecodeError:
            continue
        saw_json = True
        if skill_event_match(event, target_skill):
            return True
    return False if saw_json else None


def normalize_judge(raw: dict[str, Any]) -> dict[str, Any]:
    verdict = str(raw.get("verdict", "")).strip().upper()
    legacy_verdicts = {
        "PASS": "A",
        "PARTIAL": "B",
        "FAIL": "D",
        "BLOCKED": "D",
    }
    verdict = legacy_verdicts.get(verdict, verdict)
    if verdict not in {"A", "B", "C", "D"}:
        verdict = "A" if bool(raw.get("pass", False)) else "D"
    rubric = raw.get("rubric", {})
    if not isinstance(rubric, dict):
        rubric = {}
    return {
        "verdict": verdict,
        "pass": bool(raw.get("pass", verdict == "A")),
        "rubric": rubric,
        "reference_point_results": raw.get("reference_point_results", []),
        "reason": str(raw.get("reason", "")).strip(),
        "raw": raw,
    }


def run_custom_command(command_template: str, prompt: str, output_file: Path, cwd: Path) -> CommandResult:
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".md") as prompt_file:
        prompt_file.write(prompt)
        prompt_path = Path(prompt_file.name)
    command = command_template.format(
        prompt_file=str(prompt_path),
        output_file=str(output_file),
        cwd=str(cwd),
    )
    try:
        started_at = time.perf_counter()
        completed = subprocess.run(
            shlex.split(command),
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )
        duration_ms = round((time.perf_counter() - started_at) * 1000)
    finally:
        prompt_path.unlink(missing_ok=True)
    text = output_file.read_text() if output_file.exists() else completed.stdout
    return CommandResult(
        text=text,
        returncode=completed.returncode,
        raw_stdout=completed.stdout,
        raw_stderr=completed.stderr,
        duration_ms=duration_ms,
        total_tokens=extract_total_tokens(completed.stdout),
    )


def codex_extra_args(extra_args: Sequence[str], profile: str | None = None) -> list[str]:
    args: list[str] = []
    if profile:
        profile = profile.strip()
        if not re.fullmatch(r"[A-Za-z0-9_-]+", profile):
            raise EvalError("--profile values may contain only letters, numbers, hyphens, and underscores")
        args.extend(["--profile", profile])
    args.extend(extra_args)
    # Eval isolation is a runner invariant, not an optional profile concern.
    # Keep this tail last so user arguments cannot re-enable hooks/notify or
    # accidentally persist agent, judge, or baseline sessions.
    args.extend(["--ephemeral", "--disable", "hooks", "-c", "notify=[]"])
    return args


def run_codex(
    prompt: str,
    output_file: Path,
    cwd: Path,
    extra_args: Sequence[str],
    profile: str | None = None,
) -> CommandResult:
    command = [
        "codex",
        "exec",
        "--json",
        "-C",
        str(cwd),
        "-o",
        str(output_file),
        *codex_extra_args(extra_args, profile),
        "-",
    ]
    started_at = time.perf_counter()
    completed = subprocess.run(command, input=prompt, text=True, capture_output=True, check=False)
    duration_ms = round((time.perf_counter() - started_at) * 1000)
    text = output_file.read_text() if output_file.exists() else completed.stdout
    return CommandResult(
        text=text,
        returncode=completed.returncode,
        raw_stdout=completed.stdout,
        raw_stderr=completed.stderr,
        duration_ms=duration_ms,
        total_tokens=extract_total_tokens(completed.stdout),
    )


def run_claude(prompt: str, output_file: Path, cwd: Path, extra_args: Sequence[str]) -> CommandResult:
    command = ["claude", "-p", "--output-format", "text", *extra_args, prompt]
    started_at = time.perf_counter()
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    duration_ms = round((time.perf_counter() - started_at) * 1000)
    output_file.write_text(completed.stdout)
    return CommandResult(
        text=completed.stdout,
        returncode=completed.returncode,
        raw_stdout=completed.stdout,
        raw_stderr=completed.stderr,
        duration_ms=duration_ms,
        total_tokens=extract_total_tokens(completed.stdout),
    )


def run_harness(
    harness: str,
    prompt: str,
    output_file: Path,
    cwd: Path,
    command_template: str | None,
    extra_args: Sequence[str],
    profile: str | None = None,
) -> CommandResult:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    if profile and harness != "codex":
        raise EvalError("--agent-profile and --judge-profile require the codex harness")
    if command_template:
        return run_custom_command(command_template, prompt, output_file, cwd)
    if harness == "codex":
        return run_codex(prompt, output_file, cwd, extra_args, profile)
    if harness == "claude":
        return run_claude(prompt, output_file, cwd, extra_args)
    raise EvalError("custom harness requires a command template")


def task_detail_path(job_dir: Path, task_id: str) -> Path:
    return job_dir / "tasks" / f"{task_id}.json"


def behavior_event_summary(events: list[dict[str, Any]]) -> dict[str, Any]:
    thread_id = ""
    usage: dict[str, Any] = {}
    commands: list[dict[str, Any]] = []
    message_count = 0
    for event in events:
        if event.get("type") == "thread.started" and isinstance(event.get("thread_id"), str):
            thread_id = event["thread_id"]
        if event.get("type") == "turn.completed" and isinstance(event.get("usage"), dict):
            usage = event["usage"]
        item = event.get("item")
        if not isinstance(item, dict):
            continue
        if item.get("type") == "agent_message":
            message_count += 1
        if item.get("type") == "command_execution" and event.get("type") == "item.completed":
            commands.append(
                {
                    "command": item.get("command"),
                    "exit_code": item.get("exit_code"),
                    "status": item.get("status"),
                }
            )
    return {
        "thread_id": thread_id,
        "event_count": len(events),
        "agent_message_count": message_count,
        "command_count": len(commands),
        "failed_command_count": sum(1 for command in commands if command.get("exit_code") not in {0, None}),
        "commands": commands,
        "usage": usage,
    }


def score_required_successful_commands(
    patterns: Sequence[str], event_summary: dict[str, Any]
) -> dict[str, Any]:
    commands = event_summary.get("commands", [])
    successful = [
        str(command.get("command") or "")
        for command in commands
        if isinstance(command, dict)
        and command.get("exit_code") == 0
        and command.get("status") == "completed"
    ]
    results = [
        {
            "regex": pattern,
            "matched": any(re.search(pattern, command) for command in successful),
        }
        for pattern in patterns
    ]
    return {
        "required": len(results),
        "matched": sum(1 for result in results if result["matched"]),
        "results": results,
    }


def resolve_declared_artifacts(report: dict[str, Any] | None, target_root: Path) -> dict[str, list[str]]:
    declared = report.get("artifacts", []) if isinstance(report, dict) else []
    if not isinstance(declared, list):
        return {"declared": [], "present": [], "missing_or_unsafe": ["artifacts must be an array"]}
    present: list[str] = []
    missing: list[str] = []
    normalized: list[str] = []
    root = target_root.resolve()
    for item in declared:
        if not isinstance(item, str) or not item.strip():
            missing.append(str(item))
            continue
        candidate = Path(item.strip())
        path = candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()
        try:
            relative = path.relative_to(root).as_posix()
        except ValueError:
            missing.append(f"unsafe:{item}")
            continue
        normalized.append(relative)
        if path.exists():
            present.append(relative)
        else:
            missing.append(relative)
    return {"declared": normalized, "present": present, "missing_or_unsafe": missing}


def score_checkpoints(report: dict[str, Any] | None) -> dict[str, Any]:
    checkpoints = report.get("checkpoints", []) if isinstance(report, dict) else []
    if not isinstance(checkpoints, list):
        return {"total": 0, "done": 0, "skipped": 0, "blocked": 0, "invalid": 1}
    counts = {"total": len(checkpoints), "done": 0, "skipped": 0, "blocked": 0, "invalid": 0}
    for checkpoint in checkpoints:
        if not isinstance(checkpoint, dict):
            counts["invalid"] += 1
            continue
        status = checkpoint.get("status")
        name = checkpoint.get("name")
        evidence = checkpoint.get("evidence")
        if (
            status not in BEHAVIOR_CHECKPOINT_STATUSES
            or not isinstance(name, str)
            or not name.strip()
            or (status == "done" and (not isinstance(evidence, str) or not evidence.strip()))
        ):
            counts["invalid"] += 1
            continue
        counts[str(status)] += 1
    return counts


def build_behavior_trace(
    result: CommandResult,
    prompt_path: Path,
    answer_path: Path,
    task_dir: Path,
    target_root: Path,
    before_snapshot: dict[str, tuple[int, int]],
    prefix: str,
    schema_path: Path | None,
    required_successful_command_regexes: Sequence[str],
) -> dict[str, Any]:
    events_path = task_dir / f"{prefix}events.jsonl"
    events_path.write_text(result.raw_stdout)
    events = read_json_lines(result.raw_stdout)
    final_output = answer_path.read_text() if answer_path.exists() else result.text
    final_report = parse_json_object(final_output)
    behavior_report_keys = {"target", "persona", "checkpoints", "artifacts", "deviations", "verdict"}
    is_behavior_report = isinstance(final_report, dict) and behavior_report_keys.issubset(final_report)
    schema_errors: list[str] = []
    schema_copy_path = ""
    if schema_path:
        schema = read_json(schema_path)
        schema_copy = task_dir / f"{prefix}output_schema.json"
        schema_copy.write_text(json.dumps(schema, indent=2) + "\n")
        schema_copy_path = str(schema_copy)
        schema_errors = validate_json_schema(final_report, schema) if final_report is not None else ["$: final output is not a JSON object"]
    event_summary = behavior_event_summary(events)
    command_requirements = score_required_successful_commands(
        required_successful_command_regexes, event_summary
    )
    artifacts = resolve_declared_artifacts(final_report if is_behavior_report else None, target_root)
    checkpoints = score_checkpoints(final_report if is_behavior_report else None)
    after_snapshot = snapshot_files(target_root, task_dir)
    file_delta = snapshot_delta(before_snapshot, after_snapshot)
    report_verdict = final_report.get("verdict") if is_behavior_report else None
    failures: list[str] = []
    if result.returncode != 0:
        failures.append(f"agent exited {result.returncode}")
    if not final_output.strip():
        failures.append("final output is empty")
    if schema_errors:
        failures.append("output schema validation failed")
    missing_commands = [
        result["regex"]
        for result in command_requirements["results"]
        if not result["matched"]
    ]
    if missing_commands:
        failures.append(
            "required successful command evidence missing: " + ", ".join(missing_commands)
        )
    if is_behavior_report:
        if report_verdict not in BEHAVIOR_REPORT_VERDICTS:
            failures.append("behavior report verdict must be pass, fail, or blocked")
        if checkpoints["invalid"]:
            failures.append("one or more checkpoints are invalid")
        if artifacts["missing_or_unsafe"]:
            failures.append("one or more declared artifacts are missing or unsafe")
    verdict = "fail" if failures else str(report_verdict or "pass")
    trace_path = task_dir / f"{prefix}behavior_trace.json"
    trace = {
        "schema_version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "verdict": verdict,
        "failures": failures,
        "returncode": result.returncode,
        "prompt_path": str(prompt_path),
        "events_path": str(events_path),
        "stdout_path": str(task_dir / f"{prefix}agent_stdout.log"),
        "stderr_path": str(task_dir / f"{prefix}agent_stderr.log"),
        "final_output_path": str(answer_path),
        "output_schema_path": schema_copy_path,
        "schema_validation": {"requested": bool(schema_path), "pass": not schema_errors, "errors": schema_errors},
        "event_summary": event_summary,
        "command_requirement_score": command_requirements,
        "checkpoint_score": checkpoints,
        "artifact_inventory": {**artifacts, "observed_file_delta": file_delta},
        "behavior_report_detected": is_behavior_report,
        "final_output_format": "json_object" if final_report is not None else "text_or_other_json",
        "final_report": final_report,
    }
    write_json(trace_path, trace)
    return {**trace, "trace_path": str(trace_path)}


def normalize_assertion_results(judge: dict[str, Any]) -> list[dict[str, Any]]:
    results = judge.get("reference_point_results", [])
    if not isinstance(results, list):
        return []
    normalized: list[dict[str, Any]] = []
    for result in results:
        if not isinstance(result, dict):
            continue
        text = str(result.get("reference_point") or result.get("text") or result.get("label") or "").strip()
        if not text:
            continue
        passed = bool(result.get("met", result.get("passed", result.get("status") == "pass")))
        normalized.append(
            {
                "text": text,
                "passed": passed,
                "evidence": str(result.get("reason") or result.get("evidence") or "").strip(),
            }
        )
    return normalized


def write_agent_skills_artifacts(
    task_dir: Path,
    variant: str,
    answer_text: str,
    judge: dict[str, Any],
    duration_ms: int,
    total_tokens: int | None,
) -> dict[str, Any]:
    """Write the Agent Skills-shaped timing, grading, and output artifacts."""
    variant_dir = task_dir / variant
    outputs_dir = variant_dir / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    (outputs_dir / "agent_answer.txt").write_text(answer_text)
    timing = {"duration_ms": duration_ms, "total_tokens": total_tokens}
    assertion_results = normalize_assertion_results(judge)
    passed = sum(1 for result in assertion_results if result["passed"])
    grading = {
        "assertion_results": assertion_results,
        "summary": {
            "passed": passed,
            "failed": len(assertion_results) - passed,
            "total": len(assertion_results),
            "pass_rate": round(passed / len(assertion_results), 4) if assertion_results else None,
        },
        "judge": {
            "verdict": judge.get("verdict"),
            "pass": judge.get("pass"),
            "reason": judge.get("reason"),
        },
    }
    write_json(variant_dir / "timing.json", timing)
    write_json(variant_dir / "grading.json", grading)
    return {"timing": timing, "grading": grading, "artifact_dir": str(variant_dir)}


def run_agent_and_judge(
    task: EvalTask,
    args: argparse.Namespace,
    task_dir: Path,
    agent_template: str,
    judge_template: str,
    agent_profile: str | None,
    prefix: str = "",
) -> dict[str, Any]:
    task_dir.mkdir(parents=True, exist_ok=True)
    task = stage_task_files(task, Path(args.target_root).resolve(), task_dir)
    agent_prompt = render_template(agent_template, task)
    agent_prompt_path = task_dir / f"{prefix}agent_prompt.md"
    agent_answer_path = task_dir / f"{prefix}agent_answer.txt"
    agent_prompt_path.write_text(agent_prompt)
    before_snapshot = snapshot_files(Path(args.target_root).resolve(), task_dir) if args.behavior_trace else {}
    agent_extra_args = list(args.agent_extra_arg)
    schema_path = Path(args.behavior_output_schema).resolve() if args.behavior_output_schema else None
    if args.behavior_trace and schema_path and args.harness == "codex" and not args.agent_command_template:
        agent_extra_args.extend(["--output-schema", str(schema_path)])
    agent_result = run_harness(
        args.harness,
        agent_prompt,
        agent_answer_path,
        Path(args.target_root).resolve(),
        args.agent_command_template,
        agent_extra_args,
        agent_profile,
    )
    behavior_trace = None
    if args.behavior_trace:
        behavior_trace = build_behavior_trace(
            agent_result,
            agent_prompt_path,
            agent_answer_path,
            task_dir,
            Path(args.target_root).resolve(),
            before_snapshot,
            prefix,
            schema_path,
            task.required_successful_command_regexes,
        )
    judge_result: CommandResult | None = None
    if agent_result.returncode != 0:
        judge = {
            "verdict": "D",
            "pass": False,
            "rubric": {},
            "reference_point_results": [],
            "reason": f"agent command failed with exit code {agent_result.returncode}",
        }
    else:
        judge_prompt = render_template(judge_template, task, answer=agent_result.text)
        judge_prompt_path = task_dir / f"{prefix}judge_prompt.md"
        judge_answer_path = task_dir / f"{prefix}judge_answer.txt"
        judge_prompt_path.write_text(judge_prompt)
        judge_result = run_harness(
            args.judge_harness or args.harness,
            judge_prompt,
            judge_answer_path,
            Path(args.target_root).resolve(),
            args.judge_command_template,
            args.judge_extra_arg,
            args.judge_profile,
        )
        if judge_result.returncode != 0:
            judge = {
                "verdict": "D",
                "pass": False,
                "rubric": {},
                "reference_point_results": [],
                "reason": f"judge command failed with exit code {judge_result.returncode}",
                "raw_response": judge_result.text,
            }
        else:
            judge = normalize_judge(extract_json_object(judge_result.text))
            judge["raw_response"] = judge_result.text
            (task_dir / f"{prefix}judge_stdout.log").write_text(judge_result.raw_stdout)
            (task_dir / f"{prefix}judge_stderr.log").write_text(judge_result.raw_stderr)
    (task_dir / f"{prefix}agent_stdout.log").write_text(agent_result.raw_stdout)
    (task_dir / f"{prefix}agent_stderr.log").write_text(agent_result.raw_stderr)
    duration_ms = agent_result.duration_ms + (judge_result.duration_ms if judge_result else 0)
    token_values = [value for value in (agent_result.total_tokens, judge_result.total_tokens if judge_result else None) if value is not None]
    total_tokens = sum(token_values) if token_values else None
    variant = prefix.rstrip("_") or "candidate"
    artifacts = write_agent_skills_artifacts(
        task_dir,
        variant,
        agent_result.text,
        judge,
        duration_ms,
        total_tokens,
    )
    return {
        "profile": agent_profile,
        "agent": {
            "returncode": agent_result.returncode,
            "answer_path": str(agent_answer_path),
        },
        "judge": judge,
        **artifacts,
        "behavior_trace": behavior_trace,
        "raw_stdout": agent_result.raw_stdout,
    }


def comparison_delta(candidate: dict[str, Any], baseline: dict[str, Any] | None) -> str:
    if not baseline:
        return "baseline_skipped"
    candidate_pass = bool(candidate["judge"].get("pass", False)) and (
        not candidate.get("behavior_trace") or candidate["behavior_trace"].get("verdict") == "pass"
    )
    baseline_pass = bool(baseline["judge"].get("pass", False)) and (
        not baseline.get("behavior_trace") or baseline["behavior_trace"].get("verdict") == "pass"
    )
    if candidate_pass and not baseline_pass:
        return "candidate_wins"
    if baseline_pass and not candidate_pass:
        return "baseline_wins"
    return "tie"


def run_comparison_task(
    task: EvalTask,
    args: argparse.Namespace,
    job_dir: Path,
    agent_template: str,
    judge_template: str,
) -> dict[str, Any]:
    task_dir = job_dir / "tasks" / task.id
    target_skill = args.target_skill.strip()
    candidate = run_agent_and_judge(
        task,
        args,
        task_dir,
        agent_template,
        judge_template,
        args.agent_profile,
        "candidate_",
    )
    skill_triggered = detect_skill_triggered(candidate.pop("raw_stdout"), target_skill)
    candidate["skill_triggered"] = skill_triggered
    baseline = None
    if skill_triggered is True:
        baseline = run_agent_and_judge(
            task,
            args,
            task_dir,
            agent_template,
            judge_template,
            args.baseline_agent_profile,
            "baseline_",
        )
        baseline.pop("raw_stdout", None)
    delta = comparison_delta(candidate, baseline)
    detail = {
        "schema_version": 2,
        "task": json.loads(task_to_json(task)),
        "run_config": {
            "harness": args.harness,
            "judge_harness": args.judge_harness or args.harness,
            "agent_profile": args.agent_profile,
            "baseline_agent_profile": args.baseline_agent_profile,
            "target_skill": target_skill,
            "compare_baseline": True,
        },
        "candidate": candidate,
        "baseline": baseline or {"skipped": True, "reason": "skill did not trigger"},
        "comparison": {
            "delta": delta,
            "skill_value": delta == "candidate_wins",
        },
    }
    write_json(task_detail_path(job_dir, task.id), detail)
    write_json(task_dir / "comparison.json", detail["comparison"])
    return {
        "task_id": task.id,
        "title": task.title,
        "verdict": candidate["judge"].get("verdict", "fail"),
        "pass": bool(candidate["judge"].get("pass", False))
        and (not args.behavior_trace or candidate["behavior_trace"]["verdict"] == "pass"),
        "reason": candidate["judge"].get("reason", ""),
        "skill_triggered": skill_triggered,
        "comparison_delta": delta,
        "candidate_metrics": candidate["timing"],
        "baseline_metrics": baseline["timing"] if baseline else None,
        "baseline_pass": bool(baseline and baseline["judge"].get("pass", False))
        and (not args.behavior_trace or baseline["behavior_trace"]["verdict"] == "pass"),
        "behavior_verdict": candidate["behavior_trace"]["verdict"] if candidate["behavior_trace"] else None,
        "behavior_trace_path": candidate["behavior_trace"]["trace_path"] if candidate["behavior_trace"] else None,
        "detail_path": str(task_detail_path(job_dir, task.id)),
    }


def run_single_task(
    task: EvalTask,
    args: argparse.Namespace,
    job_dir: Path,
    agent_template: str,
    judge_template: str,
) -> dict[str, Any]:
    task_dir = job_dir / "tasks" / task.id
    result = run_agent_and_judge(
        task,
        args,
        task_dir,
        agent_template,
        judge_template,
        args.agent_profile,
    )
    result.pop("raw_stdout", None)
    detail = {
        "schema_version": 2,
        "task": json.loads(task_to_json(task)),
        "run_config": {
            "harness": args.harness,
            "judge_harness": args.judge_harness or args.harness,
            "agent_profile": args.agent_profile,
            "judge_profile": args.judge_profile,
        },
        "agent": result["agent"],
        "behavior_trace": result["behavior_trace"],
        "judge": result["judge"],
        "candidate": {
            "agent": result["agent"],
            "judge": result["judge"],
            "timing": result["timing"],
            "grading": result["grading"],
            "artifact_dir": result["artifact_dir"],
            "behavior_trace": result["behavior_trace"],
        },
    }
    write_json(task_detail_path(job_dir, task.id), detail)
    return {
        "task_id": task.id,
        "title": task.title,
        "verdict": result["judge"].get("verdict", "fail"),
        "pass": result["judge"]["pass"]
        and (not args.behavior_trace or result["behavior_trace"]["verdict"] == "pass"),
        "reason": result["judge"]["reason"],
        "candidate_metrics": result["timing"],
        "behavior_verdict": result["behavior_trace"]["verdict"] if result["behavior_trace"] else None,
        "behavior_trace_path": result["behavior_trace"]["trace_path"] if result["behavior_trace"] else None,
        "detail_path": str(task_detail_path(job_dir, task.id)),
    }


def run_task(
    task: EvalTask,
    args: argparse.Namespace,
    eval_dir: Path,
    job_dir: Path,
    agent_template: str,
    judge_template: str,
) -> dict[str, Any]:
    if args.compare_baseline:
        return run_comparison_task(task, args, job_dir, agent_template, judge_template)
    return run_single_task(task, args, job_dir, agent_template, judge_template)


def update_index(runs_dir: Path, summary: dict[str, Any]) -> None:
    index_path = runs_dir / "index.json"
    existing = read_json(index_path) if index_path.exists() else []
    if not isinstance(existing, list):
        existing = []
    compact = {
        "schema_version": summary.get("schema_version", 1),
        "job_id": summary["job_id"],
        "label": summary["label"],
        "created_at": summary["created_at"],
        "task_count": summary["task_count"],
        "pass_rate": summary["pass_rate"],
        "verdict_counts": summary["verdict_counts"],
        "harness": summary["harness"],
    }
    write_json(index_path, [compact, *[row for row in existing if row.get("job_id") != summary["job_id"]]])


def mean_metric(rows: list[dict[str, Any]], variant: str, field: str) -> float | None:
    values: list[float] = []
    for row in rows:
        metrics = row.get(f"{variant}_metrics")
        if isinstance(metrics, dict) and isinstance(metrics.get(field), (int, float)):
            values.append(float(metrics[field]))
    return round(sum(values) / len(values), 4) if values else None


def build_benchmark(rows: list[dict[str, Any]], compare_baseline: bool) -> dict[str, Any]:
    candidate_pass_rate = round(sum(1 for row in rows if row.get("pass")) / len(rows), 4) if rows else 0
    candidate = {
        "pass_rate": {"mean": candidate_pass_rate, "stddev": 0.0},
        "duration_ms": {"mean": mean_metric(rows, "candidate", "duration_ms"), "stddev": 0.0},
        "total_tokens": {"mean": mean_metric(rows, "candidate", "total_tokens"), "stddev": 0.0},
    }
    benchmark: dict[str, Any] = {
        "schema_version": 2,
        "repetitions": 1,
        "run_summary": {"candidate": candidate},
    }
    if not compare_baseline:
        return benchmark
    comparable = [row for row in rows if isinstance(row.get("baseline_metrics"), dict)]
    baseline_pass_rate = (
        round(
            sum(1 for row in comparable if row.get("baseline_pass") is True)
            / len(comparable),
            4,
        )
        if comparable
        else None
    )
    baseline = {
        "pass_rate": {"mean": baseline_pass_rate, "stddev": 0.0},
        "duration_ms": {"mean": mean_metric(rows, "baseline", "duration_ms"), "stddev": 0.0},
        "total_tokens": {"mean": mean_metric(rows, "baseline", "total_tokens"), "stddev": 0.0},
    }
    benchmark["run_summary"]["baseline"] = baseline
    benchmark["run_summary"]["delta"] = {
        field: (
            candidate[field]["mean"] - baseline[field]["mean"]
            if isinstance(candidate[field]["mean"], (int, float))
            and isinstance(baseline[field]["mean"], (int, float))
            else None
        )
        for field in ("pass_rate", "duration_ms", "total_tokens")
    }
    return benchmark


def inspect_eval_setup(harness: str, target_root: Path, eval_dir: str | None) -> tuple[Path, list[str]]:
    resolved_eval_dir = Path(eval_dir).resolve() if eval_dir else default_eval_dir(harness, target_root.resolve())
    missing = [relative for relative in REQUIRED_EVAL_FILES if not (resolved_eval_dir / relative).exists()]
    return resolved_eval_dir, missing


def command_status(args: argparse.Namespace) -> int:
    eval_dir, missing = inspect_eval_setup(args.harness, Path(args.target_root), args.eval_dir)
    if missing:
        print(f"Eval setup missing in {eval_dir}")
        for relative in missing:
            print(f"- {relative}")
        print("")
        print(f"Initialize it with: python3 skills/eval/scripts/run_evals.py init --harness {args.harness} --target-root {Path(args.target_root).resolve()}")
        return 1
    print(f"Eval setup ready in {eval_dir}")
    return 0


def load_reliability_summary(path: Path) -> dict[str, Any]:
    raw = read_json(path)
    if not isinstance(raw, dict):
        raise EvalError(f"{path}: summary must be a JSON object")
    tasks = raw.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        raise EvalError(f"{path}: summary tasks must be a non-empty list")
    if raw.get("task_count") != len(tasks):
        raise EvalError(f"{path}: task_count does not match tasks")
    for field in RELIABILITY_COMPATIBILITY_FIELDS:
        if field not in raw:
            raise EvalError(f"{path}: missing comparison metadata field {field}")
    for field in ("harness", "judge_harness", "skill_context"):
        if not isinstance(raw[field], str) or not raw[field].strip():
            raise EvalError(f"{path}: comparison metadata field {field} must be a non-empty string")
    for field in ("compare_baseline", "behavior_trace"):
        if not isinstance(raw[field], bool):
            raise EvalError(f"{path}: comparison metadata field {field} must be boolean")
    for field in ("scopes", "task_files"):
        if not isinstance(raw[field], list) or not raw[field] or not all(
            isinstance(value, str) and value.strip() for value in raw[field]
        ):
            raise EvalError(f"{path}: comparison metadata field {field} must be non-empty strings")
    if "comparison_metadata" in raw and not isinstance(raw["comparison_metadata"], dict):
        raise EvalError(f"{path}: comparison_metadata must be an object")
    seen: set[str] = set()
    for index, row in enumerate(tasks):
        if not isinstance(row, dict):
            raise EvalError(f"{path}: task at index {index} must be an object")
        task_id = row.get("task_id")
        title = row.get("title")
        verdict = row.get("verdict")
        behavior_verdict = row.get("behavior_verdict")
        if not isinstance(task_id, str) or not task_id.strip():
            raise EvalError(f"{path}: task at index {index} needs a non-empty task_id")
        if task_id in seen:
            raise EvalError(f"{path}: duplicate task_id {task_id}")
        seen.add(task_id)
        if not isinstance(title, str) or not title.strip():
            raise EvalError(f"{path}: task {task_id} needs a non-empty title")
        if not isinstance(verdict, str) or not verdict.strip():
            raise EvalError(f"{path}: task {task_id} needs a non-empty verdict")
        if behavior_verdict not in {"pass", "fail", "blocked"}:
            raise EvalError(f"{path}: task {task_id} needs behavior_verdict pass, fail, or blocked")
    return raw


def count_values(values: Sequence[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def rate(count: int, total: int) -> float:
    return round(count / total, 4) if total else 0.0


def inspect_fixture_evidence(eval_file: Path, target_root: Path) -> dict[str, Any]:
    raw = read_json(eval_file)
    rows = normalize_task_rows(raw, eval_file)
    task_reports: list[dict[str, Any]] = []
    tension_counts: dict[str, int] = {}
    for row in rows:
        task_id = str(row.get("id", ""))
        source_row = next(
            (
                item
                for item in (raw.get("evals", []) if isinstance(raw, dict) else raw)
                if isinstance(item, dict) and str(item.get("id", "")) == task_id
            ),
            {},
        )
        assertions = source_row.get("assertions", []) if isinstance(source_row, dict) else []
        expectation_parts = [str(source_row.get("expected_output", ""))]
        if isinstance(assertions, list):
            expectation_parts.extend(str(item) for item in assertions)
        expectation = " ".join(expectation_parts).lower()
        requires_image = bool(re.search(r"\b(screenshot|screenshots|image|images|visual evidence)\b", expectation))
        files = [str(item) for item in row.get("files", [])]
        image_files = [item for item in files if Path(item).suffix.lower() in IMAGE_SUFFIXES]
        missing_files = [item for item in files if not (target_root / item).is_file()]
        if missing_files:
            raise EvalError(f"{eval_file}: task {task_id} fixture files not found: {', '.join(missing_files)}")
        classification = "not_required"
        if requires_image and image_files:
            classification = "supported"
        elif requires_image:
            prompt = str(source_row.get("prompt", "")).lower()
            intentional = "no screenshot" in prompt or "without screenshot" in expectation
            classification = (
                "intentional_missing_evidence_control"
                if intentional
                else "potential_fixture_evaluator_tension"
            )
        tension_counts[classification] = tension_counts.get(classification, 0) + 1
        task_reports.append(
            {
                "task_id": task_id,
                "requires_image_evidence": requires_image,
                "image_files": image_files,
                "missing_files": missing_files,
                "classification": classification,
            }
        )
    return {
        "eval_file": str(eval_file),
        "task_count": len(task_reports),
        "classification_counts": dict(sorted(tension_counts.items())),
        "tasks": task_reports,
    }


def build_reliability_report(
    summaries: Sequence[tuple[Path, dict[str, Any]]],
    fixture_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if len(summaries) < 2:
        raise EvalError("reliability requires at least two summary.json paths")
    first_path, first = summaries[0]
    expected_metadata = {field: first[field] for field in RELIABILITY_COMPATIBILITY_FIELDS}
    first_tasks = {str(row["task_id"]): str(row["title"]) for row in first["tasks"]}
    has_extended_metadata = "comparison_metadata" in first
    for path, summary in summaries[1:]:
        metadata = {field: summary[field] for field in RELIABILITY_COMPATIBILITY_FIELDS}
        if metadata != expected_metadata:
            unequal = [field for field in RELIABILITY_COMPATIBILITY_FIELDS if metadata[field] != expected_metadata[field]]
            raise EvalError(f"{path}: incompatible comparison metadata: {', '.join(unequal)}")
        tasks = {str(row["task_id"]): str(row["title"]) for row in summary["tasks"]}
        if tasks != first_tasks:
            raise EvalError(f"{path}: incompatible task id/title set compared with {first_path}")
        if ("comparison_metadata" in summary) != has_extended_metadata:
            raise EvalError(f"{path}: incompatible comparison_metadata availability")
        if has_extended_metadata and summary["comparison_metadata"] != first["comparison_metadata"]:
            raise EvalError(f"{path}: incompatible comparison_metadata")

    per_case: list[dict[str, Any]] = []
    disagreement_flags: list[dict[str, Any]] = []
    strict_values: list[str] = []
    behavior_values: list[str] = []
    exact_suite_count = 0
    for _, summary in summaries:
        rows = {str(row["task_id"]): row for row in summary["tasks"]}
        run_strict = [str(rows[task_id]["verdict"]) for task_id in first_tasks]
        strict_values.extend(run_strict)
        behavior_values.extend(str(rows[task_id]["behavior_verdict"]) for task_id in first_tasks)
        if all(value == "A" for value in run_strict):
            exact_suite_count += 1

    for task_id, title in first_tasks.items():
        strict = [str(next(row for row in summary["tasks"] if row["task_id"] == task_id)["verdict"]) for _, summary in summaries]
        behavior = [str(next(row for row in summary["tasks"] if row["task_id"] == task_id)["behavior_verdict"]) for _, summary in summaries]
        strict_a_count = sum(value == "A" for value in strict)
        behavior_pass_count = sum(value == "pass" for value in behavior)
        case_report = {
            "task_id": task_id,
            "title": title,
            "strict_grade_counts": count_values(strict),
            "strict_a_count": strict_a_count,
            "strict_a_rate": rate(strict_a_count, len(strict)),
            "behavior_verdict_counts": count_values(behavior),
            "behavior_pass_count": behavior_pass_count,
            "behavior_pass_rate": rate(behavior_pass_count, len(behavior)),
        }
        per_case.append(case_report)
        if behavior_pass_count == len(behavior) and strict_a_count != len(strict):
            disagreement_flags.append(
                {
                    "kind": "behavior_stable_strict_grade_variance",
                    "task_id": task_id,
                    "strict_a_count": strict_a_count,
                    "behavior_pass_count": behavior_pass_count,
                }
            )

    strict_a_count = sum(value == "A" for value in strict_values)
    behavior_pass_count = sum(value == "pass" for value in behavior_values)
    if behavior_pass_count != len(behavior_values):
        promotion_verdict = "fail"
    elif strict_a_count == len(strict_values):
        promotion_verdict = "stable_pass"
    else:
        promotion_verdict = "unstable"
    if not has_extended_metadata:
        disagreement_flags.append(
            {
                "kind": "legacy_comparison_metadata_gap",
                "detail": "summaries predate recorded model/profile/prompt hashes; explicit inputs assert equality for those unrecorded settings",
            }
        )

    report: dict[str, Any] = {
        "schema_version": 1,
        "kind": "eval_reliability",
        "input_summaries": [str(path) for path, _ in summaries],
        "comparison_metadata": first.get("comparison_metadata", expected_metadata),
        "run_count": len(summaries),
        "task_count": len(first_tasks),
        "strict_grade": {
            "verdict_counts": count_values(strict_values),
            "a_count": strict_a_count,
            "total": len(strict_values),
            "a_rate": rate(strict_a_count, len(strict_values)),
        },
        "behavior": {
            "verdict_counts": count_values(behavior_values),
            "pass_count": behavior_pass_count,
            "total": len(behavior_values),
            "pass_rate": rate(behavior_pass_count, len(behavior_values)),
        },
        "exact_suite": {
            "strict_a_pass_count": exact_suite_count,
            "total": len(summaries),
            "pass_rate": rate(exact_suite_count, len(summaries)),
        },
        "per_case": per_case,
        "disagreement_flags": disagreement_flags,
        "promotion_verdict": promotion_verdict,
    }
    if fixture_report is not None:
        report["fixture_evidence_contract"] = fixture_report
    return report


def command_reliability(args: argparse.Namespace) -> int:
    summaries = [(Path(value).resolve(), load_reliability_summary(Path(value).resolve())) for value in args.summaries]
    fixture_report = None
    if args.eval_file:
        fixture_report = inspect_fixture_evidence(Path(args.eval_file).resolve(), Path(args.target_root).resolve())
    report = build_reliability_report(summaries, fixture_report)
    if args.output:
        output = Path(args.output).resolve()
        write_json(output, report)
        print(f"Wrote {output}")
    else:
        print(json.dumps(report, indent=2))
    return 0 if report["promotion_verdict"] == "stable_pass" else 1


def command_run(args: argparse.Namespace) -> int:
    target_root = Path(args.target_root).resolve()
    eval_dir = Path(args.eval_dir).resolve() if args.eval_dir else default_eval_dir(args.harness, target_root)
    eval_config = load_eval_config(eval_dir)
    scopes, explicit_scopes = selected_scopes(args)
    task_paths = resolve_task_paths(eval_dir, args.tasks, scopes, target_root, require_scopes=explicit_scopes)
    task_paths = filter_skill_task_paths(task_paths, target_root, args.skill)
    if args.compare_baseline:
        if args.harness != "codex" and not args.agent_command_template:
            raise EvalError("--compare-baseline requires codex harness or a custom agent command template")
        if not args.baseline_agent_profile and not args.agent_command_template:
            raise EvalError("--compare-baseline requires --baseline-agent-profile for codex runs")
        selected = expand_skill_selectors(args.skill)
        if len(selected) != 1:
            raise EvalError("--compare-baseline requires exactly one --skill")
        args.target_skill = next(iter(selected))
    if args.behavior_output_schema and not args.behavior_trace:
        raise EvalError("--behavior-output-schema requires --behavior-trace")
    if args.behavior_output_schema and not Path(args.behavior_output_schema).resolve().is_file():
        raise EvalError(f"behavior output schema not found: {Path(args.behavior_output_schema).resolve()}")
    if args.behavior_trace and args.max_parallel_tasks != 1:
        raise EvalError("--behavior-trace requires --max-parallel-tasks 1 for attributable file inventory")
    native_skill_context = args.compare_baseline or uses_native_skill_context(args.harness, args.agent_profile)
    tasks = load_task_suite(
        task_paths,
        args.limit,
        default_context=eval_config.default_context,
        target_root=target_root,
        task_ids=set(args.task_id),
        native_skill_context=native_skill_context,
    )
    if args.max_parallel_tasks < 1:
        raise EvalError("--max-parallel-tasks must be at least 1")
    agent_template = read_text(Path(args.agent_prompt or eval_dir / "prompts" / "agent.md"))
    judge_template = read_text(Path(args.judge_prompt or eval_dir / "prompts" / "judge.md"))
    runs_dir = Path(args.runs_dir).resolve() if args.runs_dir else eval_dir / "runs"
    job_id = build_job_id(args.label)
    job_dir = runs_dir / job_id
    (job_dir / "tasks").mkdir(parents=True, exist_ok=True)
    created_at = datetime.now(timezone.utc).isoformat()
    summary_tasks: list[dict[str, Any] | None] = [None] * len(tasks)
    max_workers = min(args.max_parallel_tasks, len(tasks)) or 1
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_index = {
            executor.submit(run_task, task, args, eval_dir, job_dir, agent_template, judge_template): index
            for index, task in enumerate(tasks)
        }
        for future in as_completed(future_to_index):
            index = future_to_index[future]
            summary_tasks[index] = future.result()
    rows = [row for row in summary_tasks if row is not None]
    pass_rate = round(sum(1 for row in rows if row["pass"]) / len(rows), 2) if rows else 0
    verdict_counts: dict[str, int] = {}
    for row in rows:
        verdict = str(row["verdict"])
        verdict_counts[verdict] = verdict_counts.get(verdict, 0) + 1
    comparison_counts: dict[str, int] = {}
    skill_trigger_counts: dict[str, int] = {}
    if args.compare_baseline:
        for row in rows:
            delta = str(row.get("comparison_delta", "unknown"))
            comparison_counts[delta] = comparison_counts.get(delta, 0) + 1
            triggered = row.get("skill_triggered")
            trigger_key = "unknown" if triggered is None else str(bool(triggered)).lower()
            skill_trigger_counts[trigger_key] = skill_trigger_counts.get(trigger_key, 0) + 1
    summary = {
        "schema_version": 2,
        "job_id": job_id,
        "label": args.label,
        "created_at": created_at,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "harness": args.harness,
        "judge_harness": args.judge_harness or args.harness,
        "scopes": ["custom"] if args.tasks else list(scopes),
        "default_context_file": eval_config.default_context_file,
        "skill_context": "native" if native_skill_context else "inline",
        "compare_baseline": bool(args.compare_baseline),
        "behavior_trace": bool(args.behavior_trace),
        "task_files": [str(path) for path in task_paths],
        "task_count": len(rows),
        "pass_rate": pass_rate,
        "verdict_counts": verdict_counts,
        "tasks": rows,
        "comparison_metadata": {
            "agent_profile": args.agent_profile,
            "judge_profile": args.judge_profile,
            "baseline_agent_profile": args.baseline_agent_profile,
            "max_parallel_tasks": args.max_parallel_tasks,
            "agent_extra_args": list(args.agent_extra_arg),
            "judge_extra_args": list(args.judge_extra_arg),
            "agent_prompt_sha256": sha256_text(agent_template),
            "judge_prompt_sha256": sha256_text(judge_template),
            "behavior_output_schema_sha256": (
                sha256_text(read_text(Path(args.behavior_output_schema).resolve()))
                if args.behavior_output_schema
                else None
            ),
            "agent_command_template_sha256": (
                sha256_text(args.agent_command_template) if args.agent_command_template else None
            ),
            "judge_command_template_sha256": (
                sha256_text(args.judge_command_template) if args.judge_command_template else None
            ),
            "task_file_sha256": {
                str(path): sha256_text(read_text(path)) for path in task_paths
            },
        },
    }
    if args.behavior_trace:
        behavior_verdict_counts: dict[str, int] = {}
        for row in rows:
            verdict = str(row.get("behavior_verdict", "unknown"))
            behavior_verdict_counts[verdict] = behavior_verdict_counts.get(verdict, 0) + 1
        summary["behavior_verdict_counts"] = behavior_verdict_counts
    if args.compare_baseline:
        triggered_count = skill_trigger_counts.get("true", 0)
        summary["comparison_counts"] = comparison_counts
        summary["skill_trigger_counts"] = skill_trigger_counts
        summary["skill_trigger_rate"] = round(triggered_count / len(rows), 2) if rows else 0
    benchmark = build_benchmark(rows, bool(args.compare_baseline))
    summary["benchmark_path"] = str(job_dir / "benchmark.json")
    write_json(job_dir / "benchmark.json", benchmark)
    write_json(job_dir / "summary.json", summary)
    update_index(runs_dir, summary)
    print(f"Wrote {job_dir}")
    return 0 if all(row["pass"] for row in rows) else 1


def copy_template(src: Path, dest: Path, force: bool) -> None:
    if dest.exists() and not force:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)


def command_init(args: argparse.Namespace) -> int:
    target_root = Path(args.target_root).resolve()
    eval_dir = Path(args.eval_dir).resolve() if args.eval_dir else default_eval_dir(args.harness, target_root)
    templates = script_root() / "templates"
    copy_template(templates / "config.json", eval_dir / "config.json", args.force)
    copy_template(templates / "contexts" / "agi-toy-shop.md", eval_dir / "contexts" / "agi-toy-shop.md", args.force)
    copy_template(templates / "harness_tasks.json", eval_dir / "tasks" / "harness_tasks.json", args.force)
    copy_template(templates / "agents_md_tasks.json", eval_dir / "tasks" / "agents_md_tasks.json", args.force)
    copy_template(templates / "agent.md", eval_dir / "prompts" / "agent.md", args.force)
    copy_template(templates / "judge.md", eval_dir / "prompts" / "judge.md", args.force)
    copy_template(templates / "behavior-report.schema.json", eval_dir / "schemas" / "behavior-report.schema.json", args.force)
    copy_template(templates / "README.md", eval_dir / "README.md", args.force)
    copy_template(Path(__file__).resolve(), eval_dir / "run_evals.py", args.force)
    (eval_dir / "runs").mkdir(parents=True, exist_ok=True)
    print(f"Initialized {eval_dir}")
    print("")
    print("Next steps:")
    print(f"  1. Edit {eval_dir / 'tasks' / 'harness_tasks.json'} or {eval_dir / 'tasks' / 'agents_md_tasks.json'} with one important task.")
    print("  2. Use tags/notes to mark whether a task is skill, workflow, or system-prompt level.")
    print(f"  3. Run: python3 {eval_dir / 'run_evals.py'} run --harness {args.harness} --label baseline --limit 1")
    print("  4. Inspect run artifacts in Farplane UI Eval OS.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create .farplane/evals")
    init_parser.add_argument("--harness", choices=["codex", "claude", "custom"], required=True)
    init_parser.add_argument("--target-root", default=".")
    init_parser.add_argument("--eval-dir")
    init_parser.add_argument("--force", action="store_true")
    init_parser.set_defaults(func=command_init)

    status_parser = subparsers.add_parser("status", help="Check whether eval files are installed")
    status_parser.add_argument("--harness", choices=["codex", "claude", "custom"], required=True)
    status_parser.add_argument("--target-root", default=".")
    status_parser.add_argument("--eval-dir")
    status_parser.set_defaults(func=command_status)

    reliability_parser = subparsers.add_parser(
        "reliability",
        help="Reduce two or more comparable summary.json files into a promotion reliability report.",
    )
    reliability_parser.add_argument("summaries", nargs="+")
    reliability_parser.add_argument("--eval-file", help="Optional eval manifest to inspect for image-evidence fixture tension.")
    reliability_parser.add_argument("--target-root", default=".")
    reliability_parser.add_argument("--output")
    reliability_parser.set_defaults(func=command_reliability)

    run_parser = subparsers.add_parser("run", help="Run eval tasks")
    run_parser.add_argument("--harness", choices=["codex", "claude", "custom"], required=True)
    run_parser.add_argument("--judge-harness", choices=["codex", "claude", "custom"])
    run_parser.add_argument("--target-root", default=".")
    run_parser.add_argument("--eval-dir")
    run_parser.add_argument("--tasks")
    run_parser.add_argument("--harness-evals", action="store_true", help="Run only .farplane/evals/tasks/harness_tasks.json.")
    run_parser.add_argument("--agents-md", action="store_true", help="Run only .farplane/evals/tasks/agents_md_tasks.json.")
    run_parser.add_argument("--skills", action="store_true", help="Run all skills/*/evals/evals.json files.")
    run_parser.add_argument(
        "--skill",
        action="append",
        default=[],
        help="Run selected skill-local eval files. Implies --skills unless --tasks is provided; accepts a skill name, skills/name, or skills/name/evals/evals.json. May be passed multiple times or comma-separated.",
    )
    run_parser.add_argument("--agent-prompt")
    run_parser.add_argument("--judge-prompt")
    run_parser.add_argument("--label", required=True)
    run_parser.add_argument("--limit", type=int, default=0)
    run_parser.add_argument("--max-parallel-tasks", type=int, default=DEFAULT_MAX_PARALLEL_TASKS)
    run_parser.add_argument("--runs-dir")
    run_parser.add_argument("--agent-command-template")
    run_parser.add_argument("--judge-command-template")
    run_parser.add_argument("--agent-profile", help="Codex config profile for agent runs, loaded with codex exec --profile.")
    run_parser.add_argument("--judge-profile", help="Codex config profile for judge runs, loaded with codex exec --profile.")
    run_parser.add_argument("--compare-baseline", action="store_true", help="Run selected skill evals in native skill mode, record whether the target skill triggered, and run a baseline profile only after a trigger.")
    run_parser.add_argument("--baseline-agent-profile", help="Codex config profile for baseline agent runs when --compare-baseline is set.")
    run_parser.add_argument(
        "--behavior-trace",
        action="store_true",
        help="Preserve a scored agent behavior trace: exact prompt, Codex JSONL events, logs, checkpoints, artifacts, usage, and final output.",
    )
    run_parser.add_argument(
        "--behavior-output-schema",
        help="Optional JSON schema for the final behavior report; passed to Codex and validated in the preserved trace.",
    )
    run_parser.add_argument("--agent-extra-arg", action="append", default=[])
    run_parser.add_argument("--judge-extra-arg", action="append", default=[])
    run_parser.add_argument(
        "--task-id",
        action="append",
        default=[],
        help="Run only the selected task id. May be passed multiple times.",
    )
    run_parser.set_defaults(func=command_run)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.func(args))
    except EvalError as exc:
        print(f"eval error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
