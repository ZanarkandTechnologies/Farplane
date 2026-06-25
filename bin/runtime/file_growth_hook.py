#!/usr/bin/env python3
"""Codex PostToolUse hook for compacting overgrown configured files.

The hook is deliberately mechanical:
- detect likely changed files from the PostToolUse payload
- match them against configured project-relative glob rules
- count lines
- when a file exceeds its rule, ask `codex exec --ephemeral` for compacted text
- write the replacement atomically and append a JSONL log row
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_CONFIG = {
    "enabled": True,
    "model": "gpt-5.4-mini",
    "timeout_seconds": 90,
    "rules": [
        {
            "name": "project-memory",
            "patterns": ["memory.mb", "docs/MEMORY.md", "farplane/project-memory.md"],
            "max_lines": 500,
            "target_lines": 180,
            "action": "summarize_in_place",
        }
    ],
}

WRITE_TOOL_RE = re.compile(r"(bash|apply_patch|edit|write|create|delete|multi)", re.I)
MAX_CHANGED_FILES = 16
MAX_PROMPT_CHARS = 42_000


@dataclass(frozen=True)
class Rule:
    name: str
    patterns: tuple[str, ...]
    max_lines: int
    target_lines: int
    action: str


def is_record(value: Any) -> bool:
    return isinstance(value, dict)


def as_str(value: Any, limit: int = 1000) -> str | None:
    if not isinstance(value, str):
        return None
    cleaned = value.strip()
    return cleaned[:limit] if cleaned else None


def load_json_file(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except Exception:
        return None


def file_growth_config(raw: Any) -> dict[str, Any] | None:
    if not is_record(raw):
        return None
    hooks = raw.get("hooks")
    if is_record(hooks) and is_record(hooks.get("file_growth")):
        return dict(hooks["file_growth"])
    return None


def merge_config(project_root: Path) -> dict[str, Any]:
    config = dict(DEFAULT_CONFIG)
    tracked = file_growth_config(load_json_file(project_root / "farplane" / "hooks.json"))
    local = load_json_file(project_root / ".farplane" / "hooks" / "file-growth.json")
    for candidate in (tracked, local):
        if not is_record(candidate):
            continue
        config.update({key: value for key, value in candidate.items() if key != "rules"})
        if isinstance(candidate.get("rules"), list):
            config["rules"] = candidate["rules"]

    env_patterns = os.environ.get("FARPLANE_FILE_GROWTH_PATTERNS", "").strip()
    env_max_lines = os.environ.get("FARPLANE_FILE_GROWTH_MAX_LINES", "").strip()
    if env_patterns:
        max_lines = int(env_max_lines) if env_max_lines.isdigit() else 500
        config["rules"] = [
            {
                "name": "env-override",
                "patterns": [entry.strip() for entry in re.split(r"[\n,]", env_patterns) if entry.strip()],
                "max_lines": max_lines,
                "target_lines": max(40, int(max_lines * 0.4)),
                "action": "summarize_in_place",
            }
        ]
    return config


def parse_rules(config: dict[str, Any]) -> list[Rule]:
    rules: list[Rule] = []
    for index, raw_rule in enumerate(config.get("rules") or []):
        if not is_record(raw_rule):
            continue
        patterns = raw_rule.get("patterns")
        if not isinstance(patterns, list):
            continue
        normalized_patterns = tuple(
            str(pattern).strip().replace("\\", "/") for pattern in patterns if str(pattern).strip()
        )
        if not normalized_patterns:
            continue
        max_lines = int(raw_rule.get("max_lines") or 500)
        target_lines = int(raw_rule.get("target_lines") or max(40, int(max_lines * 0.4)))
        rules.append(
            Rule(
                name=str(raw_rule.get("name") or f"rule-{index + 1}"),
                patterns=normalized_patterns,
                max_lines=max_lines,
                target_lines=target_lines,
                action=str(raw_rule.get("action") or "summarize_in_place"),
            )
        )
    return rules


def event_name(payload: dict[str, Any]) -> str:
    return (
        as_str(payload.get("hook_event_name"), 120)
        or as_str(payload.get("event"), 120)
        or as_str(payload.get("hookEventName"), 120)
        or "PostToolUse"
    )


def tool_name(payload: dict[str, Any]) -> str:
    return (
        as_str(payload.get("toolName"), 120)
        or as_str(payload.get("tool_name"), 120)
        or as_str(payload.get("tool"), 120)
        or "unknown"
    )


def project_root_from_payload(payload: dict[str, Any]) -> Path:
    raw = (
        as_str(payload.get("cwd"), 2000)
        or as_str(payload.get("projectPath"), 2000)
        or as_str(payload.get("project_path"), 2000)
        or os.getcwd()
    )
    return Path(raw).expanduser().resolve()


def extract_patch_paths(text: str) -> list[str]:
    paths: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^\*\*\* (?:Add|Update|Delete) File:\s+(.+)$", line)
        if match:
            paths.append(match.group(1).strip())
    return paths


def shell_tokens(command: str) -> list[str]:
    token_re = re.compile(r'"([^"]+)"|\'([^\']+)\'|`([^`]+)`|(&&|\|\||>>|[;&|<>])|([^\s;&|<>]+)')
    tokens: list[str] = []
    for match in token_re.finditer(command):
        token = next(group for group in match.groups() if group is not None)
        token = re.sub(r"^[({\[]+|[),;\]}]+$", "", token.strip())
        if token:
            tokens.append(token)
    return tokens


def is_shell_boundary(token: str) -> bool:
    return token in {";", "&&", "||", "|", "<", ">", ">>"}


def extract_paths_from_command(command: str) -> list[str]:
    paths: set[str] = set()
    tokens = shell_tokens(command)
    for index, token in enumerate(tokens):
        lowered = token.lower()
        if lowered in {">", ">>"} and index + 1 < len(tokens):
            paths.add(tokens[index + 1])
            continue
        if lowered in {"tee", "touch", "rm", "unlink"}:
            for candidate in tokens[index + 1 :]:
                if is_shell_boundary(candidate):
                    break
                if not candidate.startswith("-"):
                    paths.add(candidate)
            continue
        if lowered in {"mv", "cp"}:
            for candidate in tokens[index + 1 :]:
                if is_shell_boundary(candidate):
                    break
                if not candidate.startswith("-"):
                    paths.add(candidate)
    return sorted(paths)


PATH_KEYS = {
    "path",
    "file",
    "filepath",
    "file_path",
    "filename",
    "target",
    "targetpath",
    "target_path",
}
RECURSE_KEYS = {
    "files",
    "paths",
    "changedfiles",
    "changed_files",
    "edits",
    "toolinput",
    "tool_input",
    "input",
    "parameters",
    "args",
    "cmd",
    "command",
    "toolresponse",
    "tool_response",
    "output",
}


def extract_likely_paths(value: Any, depth: int = 0) -> list[str]:
    if depth > 5:
        return []
    if isinstance(value, str):
        return [*extract_patch_paths(value), *extract_paths_from_command(value)]
    if isinstance(value, list):
        paths: list[str] = []
        for entry in value:
            if isinstance(entry, str):
                paths.append(entry)
            paths.extend(extract_likely_paths(entry, depth + 1))
        return paths
    if not isinstance(value, dict):
        return []

    paths = []
    for key, child in value.items():
        normalized_key = re.sub(r"[^a-z_]", "", key.lower())
        if normalized_key in PATH_KEYS:
            if isinstance(child, str):
                paths.append(child)
            elif isinstance(child, list):
                paths.extend(entry for entry in child if isinstance(entry, str))
            continue
        if normalized_key in RECURSE_KEYS:
            paths.extend(extract_likely_paths(child, depth + 1))
    return paths


def normalize_relative_path(candidate: str, project_root: Path) -> str | None:
    cleaned = candidate.strip().strip("'\"` ,:")
    if not cleaned or re.match(r"^[a-z]+://", cleaned, re.I):
        return None
    cleaned = re.sub(r":\d+(?::\d+)?$", "", cleaned)
    absolute = Path(cleaned).expanduser()
    if not absolute.is_absolute():
        absolute = project_root / absolute
    try:
        relative = absolute.resolve().relative_to(project_root)
    except ValueError:
        return None
    text = relative.as_posix()
    return text if text and text != "." else None


def changed_files(payload: dict[str, Any], project_root: Path) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()
    for candidate in extract_likely_paths(payload):
        relative = normalize_relative_path(candidate, project_root)
        if relative and relative not in seen:
            seen.add(relative)
            normalized.append(relative)
        if len(normalized) >= MAX_CHANGED_FILES:
            break
    return normalized


def matching_rule(relative_path: str, rules: list[Rule]) -> Rule | None:
    for rule in rules:
        for pattern in rule.patterns:
            if fnmatch.fnmatch(relative_path, pattern):
                return rule
    return None


def count_lines(path: Path) -> int:
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        return sum(1 for _ in handle)


def build_prompt(file_path: str, content: str, rule: Rule, line_count: int) -> str:
    clipped = content[:MAX_PROMPT_CHARS]
    return f"""Compact this project memory file in place.

File: {file_path}
Current lines: {line_count}
Target lines: <= {rule.target_lines}

Rules:
- Return only the complete replacement file content.
- Preserve durable facts, decisions, constraints, and open todos.
- Merge duplicates and remove low-value repetition.
- Keep enough detail that future agents can resume without chat history.
- Do not add commentary, markdown fences, or a preface unless it belongs in the file.
- Keep ASCII unless the source file requires non-ASCII.

<file>
{clipped}
</file>
"""


def normalize_replacement(raw: str) -> str:
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z0-9_-]*\n", "", text)
        text = re.sub(r"\n```$", "", text)
    return text.strip() + "\n"


def summarize_with_codex(project_root: Path, relative_path: str, content: str, rule: Rule, config: dict[str, Any]) -> str | None:
    fake = os.environ.get("FARPLANE_FILE_GROWTH_FAKE_SUMMARY")
    if fake:
        return fake.rstrip() + "\n"

    with tempfile.TemporaryDirectory(prefix="farplane-file-growth-") as temp_dir:
        output_path = Path(temp_dir) / "last-message.txt"
        output_path.write_text("", encoding="utf-8")
        args = [
            "codex",
            "exec",
            "--ephemeral",
            "--cd",
            str(project_root),
            "--output-last-message",
            str(output_path),
        ]
        model = str(config.get("model") or "").strip()
        if model:
            args.extend(["--model", model])
        env = dict(os.environ)
        env["FARPLANE_FILE_GROWTH_HOOK_ACTIVE"] = "1"
        subprocess.run(
            args,
            input=build_prompt(relative_path, content, rule, count_text_lines(content)),
            text=True,
            cwd=str(project_root),
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=int(config.get("timeout_seconds") or 90),
            check=True,
        )
        return normalize_replacement(output_path.read_text(encoding="utf-8", errors="replace"))


def count_text_lines(value: str) -> int:
    if not value:
        return 0
    return value.count("\n") + (0 if value.endswith("\n") else 1)


def write_atomic(path: Path, content: str) -> None:
    temp = path.with_name(f".{path.name}.file-growth.tmp")
    temp.write_text(content, encoding="utf-8")
    temp.replace(path)


def log_row(project_root: Path, row: dict[str, Any]) -> None:
    row = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), **row}
    log_path = project_root / ".farplane" / "logs" / "file-growth-hook.jsonl"
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
    except Exception:
        fallback = Path("/tmp/farplane-file-growth-hook.jsonl")
        with fallback.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def handle_payload(payload: dict[str, Any]) -> list[dict[str, Any]]:
    project_root = project_root_from_payload(payload)
    rows: list[dict[str, Any]] = []
    if os.environ.get("FARPLANE_FILE_GROWTH_HOOK_ACTIVE") == "1":
        row = {"event": "skip", "reason": "recursive_hook_guard", "project_root": str(project_root)}
        log_row(project_root, row)
        return [row]
    if not re.search(r"post.*tool.*use", event_name(payload), re.I):
        row = {"event": "skip", "reason": "not_post_tool_use", "project_root": str(project_root)}
        log_row(project_root, row)
        return [row]
    if not WRITE_TOOL_RE.search(tool_name(payload)):
        row = {"event": "skip", "reason": "not_write_tool", "tool": tool_name(payload), "project_root": str(project_root)}
        log_row(project_root, row)
        return [row]

    config = merge_config(project_root)
    if config.get("enabled") is False:
        row = {"event": "skip", "reason": "disabled", "project_root": str(project_root)}
        log_row(project_root, row)
        return [row]

    rules = parse_rules(config)
    for relative_path in changed_files(payload, project_root):
        rule = matching_rule(relative_path, rules)
        if rule is None:
            row = {"event": "skip_file", "reason": "no_matching_rule", "path": relative_path}
            log_row(project_root, row)
            rows.append(row)
            continue
        absolute_path = project_root / relative_path
        if not absolute_path.is_file():
            row = {"event": "skip_file", "reason": "not_a_file", "path": relative_path, "rule": rule.name}
            log_row(project_root, row)
            rows.append(row)
            continue
        line_count = count_lines(absolute_path)
        if line_count <= rule.max_lines:
            row = {
                "event": "skip_file",
                "reason": "below_threshold",
                "path": relative_path,
                "rule": rule.name,
                "line_count": line_count,
                "max_lines": rule.max_lines,
            }
            log_row(project_root, row)
            rows.append(row)
            continue
        if rule.action != "summarize_in_place":
            row = {"event": "skip_file", "reason": "unsupported_action", "path": relative_path, "rule": rule.name}
            log_row(project_root, row)
            rows.append(row)
            continue

        before = absolute_path.read_text(encoding="utf-8", errors="replace")
        try:
            replacement = summarize_with_codex(project_root, relative_path, before, rule, config)
            if not replacement:
                raise RuntimeError("empty_summary")
            write_atomic(absolute_path, replacement)
            after_lines = count_lines(absolute_path)
            row = {
                "event": "summarized",
                "path": relative_path,
                "rule": rule.name,
                "line_count_before": line_count,
                "line_count_after": after_lines,
                "max_lines": rule.max_lines,
                "target_lines": rule.target_lines,
            }
        except Exception as error:
            row = {
                "event": "error",
                "path": relative_path,
                "rule": rule.name,
                "line_count": line_count,
                "error": str(error)[:500],
            }
        log_row(project_root, row)
        rows.append(row)

    if not rows:
        row = {"event": "skip", "reason": "no_changed_files_detected", "project_root": str(project_root)}
        log_row(project_root, row)
        rows.append(row)
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print JSON rows for manual probes")
    args = parser.parse_args(argv)
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
        rows = handle_payload(payload if isinstance(payload, dict) else {})
        if args.json:
            print(json.dumps({"ok": True, "rows": rows}, indent=2))
    except Exception as error:
        project_root = Path(os.getcwd()).resolve()
        log_row(project_root, {"event": "error", "error": str(error)[:500]})
        if args.json:
            print(json.dumps({"ok": False, "error": str(error)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
