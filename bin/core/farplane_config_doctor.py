"""Redacted Farplane runtime config hygiene checks."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tomllib
from pathlib import Path
from typing import Any, Callable

CONFIG_DOCTOR_REQUIRED_KEYS = ("REF_API_KEY", "NOTION_TOKEN")
CONFIG_DOCTOR_SECRET_KEYS = (
    "REF_API_KEY",
    "NOTION_TOKEN",
    "FARPLANE_TELEMETRY_TOKEN",
    "FARPLANE_CONSOLE_KEY",
    "LIVEKIT_API_KEY",
    "LIVEKIT_API_SECRET",
    "LIVEKIT_SIP_AUTH_PASSWORD",
    "TELNYX_API_KEY",
    "FISH_API_KEY",
    "FARPLANE_MESHY_API_KEY",
    "MESHY_API_KEY",
)
DOPPLER_COMMAND = ["doppler"]
SECRET_ASSIGNMENT_RE = re.compile(
    r"""(?ix)
    (?P<key>[A-Z0-9_]*(?:API[_-]?KEY|TOKEN|SECRET|PASSWORD)[A-Z0-9_]*)
    \s*[:=]\s*
    (?P<quote>["'])
    (?P<value>[^"']+)
    (?P=quote)
    """
)
SECRET_SCAN_SUFFIXES = {".env", ".json", ".md", ".py", ".sh", ".toml", ".yaml", ".yml"}
SECRET_SCAN_EXCLUDED_PARTS = {
    ".git",
    ".farplane",
    "__pycache__",
    "archive",
    "artifacts",
    "experiments",
    "node_modules",
    "tests",
}


def read_toml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        parsed = tomllib.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def object_string_at(row: dict[str, Any], path_parts: list[str]) -> str:
    current: Any = row
    for part in path_parts:
        if not isinstance(current, dict):
            return ""
        current = current.get(part)
    return current.strip() if isinstance(current, str) else ""


def first_object_string_at(row: dict[str, Any], paths: list[list[str]]) -> str:
    for path_parts in paths:
        value = object_string_at(row, path_parts)
        if value:
            return value
    return ""


def env_strings(row: dict[str, Any]) -> dict[str, str]:
    env = row.get("env")
    if not isinstance(env, dict):
        return {}
    return {
        str(key): value.strip()
        for key, value in env.items()
        if isinstance(key, str) and isinstance(value, str) and value.strip()
    }


def structured_config_value(key: str, config: dict[str, Any]) -> str:
    paths = {
        "FARPLANE_TELEMETRY_TOKEN": [["convex", "telemetry_token"]],
        "FARPLANE_MESHY_API_KEY": [["integrations", "meshy_api_key"]],
        "MESHY_API_KEY": [["integrations", "meshy_api_key"]],
        "NOTION_TOKEN": [["integrations", "notion_token"]],
        "REF_API_KEY": [["integrations", "ref_api_key"]],
        "FARPLANE_CONSOLE_KEY": [["env", "FARPLANE_CONSOLE_KEY"]],
        "LIVEKIT_API_KEY": [["livekit", "api_key"]],
        "LIVEKIT_API_SECRET": [["livekit", "api_secret"]],
        "LIVEKIT_SIP_AUTH_PASSWORD": [["livekit", "sip_auth_password"], ["livekit", "sip", "auth_password"]],
        "TELNYX_API_KEY": [["livekit", "sip", "telnyx_api_key"], ["integrations", "telnyx_api_key"]],
        "FISH_API_KEY": [["fish_audio", "api_key"]],
    }
    return first_object_string_at(config, paths.get(key, []))


def config_value_sources(
    key: str,
    process_env: dict[str, str],
    farplane_config: dict[str, Any],
    rendered_config: dict[str, Any],
) -> list[str]:
    sources: list[str] = []
    if process_env.get(key):
        sources.append("process_env")
    if structured_config_value(key, farplane_config) or env_strings(farplane_config).get(key):
        sources.append("~/.farplane/config.toml")
    if env_strings(rendered_config).get(key):
        sources.append("~/.codex/config.toml")
    return sources


def doppler_file(project_root: Path) -> Path | None:
    for name in ("doppler.yaml", "doppler.yml"):
        candidate = project_root / name
        if candidate.exists():
            return candidate
    return None


def _run_text(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=str(cwd), capture_output=True, text=True)


def parse_doppler_names(output: str) -> set[str]:
    names: set[str] = set()
    for line in output.splitlines():
        stripped = line.strip()
        if not stripped.startswith("│") or stripped.startswith("│ NAME"):
            continue
        parts = [part.strip() for part in stripped.strip("│").split("│")]
        if len(parts) != 1:
            continue
        name = parts[0]
        if name and set(name) != {"─"}:
            names.add(name)
    return names


def doppler_status(
    project_root: Path,
    runner: Callable[[list[str], Path], subprocess.CompletedProcess[str]] = _run_text,
) -> dict[str, Any]:
    path = doppler_file(project_root)
    available = shutil.which("doppler") is not None
    status: dict[str, Any] = {
        "declared": path is not None,
        "file": str(path) if path else None,
        "available": available,
        "configured": False,
        "project": "",
        "config": "",
        "secretNames": [],
        "secretNameCount": 0,
        "issues": [],
    }
    if path is not None and not available:
        status["issues"].append("doppler_not_installed")
        return status
    if not available:
        return status

    project = runner(["doppler", "configure", "get", "project", "--plain"], project_root)
    config = runner(["doppler", "configure", "get", "config", "--plain"], project_root)
    if project.returncode != 0 or config.returncode != 0 or not project.stdout.strip() or not config.stdout.strip():
        if path is not None:
            status["issues"].append("doppler_not_configured")
        return status

    status["configured"] = True
    status["project"] = project.stdout.strip()
    status["config"] = config.stdout.strip()
    names = runner(["doppler", "secrets", "--only-names"], project_root)
    if names.returncode != 0:
        status["issues"].append("doppler_secret_names_unavailable")
        return status
    parsed_names = sorted(parse_doppler_names(names.stdout))
    status["secretNames"] = parsed_names
    status["secretNameCount"] = len(parsed_names)
    return status


def file_mode_warning(path: Path) -> str | None:
    if not path.exists():
        return None
    mode = path.stat().st_mode & 0o777
    if mode & 0o077:
        return f"config_permissions_too_open:{path}:mode={mode:o}"
    return None


def looks_like_placeholder(value: str) -> bool:
    normalized = value.strip().lower()
    return (
        not normalized
        or normalized.startswith("__")
        or normalized.startswith("your_")
        or normalized.startswith("your-")
        or "placeholder" in normalized
        or normalized in {"changeme", "change-me", "example", "example-token", "test", "test-token"}
    )


def tracked_or_candidate_files(project_root: Path) -> list[Path]:
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=str(project_root),
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        result = None
    if result is not None and result.returncode == 0:
        return [project_root / line for line in result.stdout.splitlines() if line.strip()]
    return [path for path in project_root.rglob("*") if path.is_file()]


def scan_secret_literals(project_root: Path) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for path in tracked_or_candidate_files(project_root):
        try:
            rel = path.relative_to(project_root)
        except ValueError:
            continue
        if any(part in SECRET_SCAN_EXCLUDED_PARTS for part in rel.parts):
            continue
        if path.name.startswith("test_"):
            continue
        if path.suffix and path.suffix.lower() not in SECRET_SCAN_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            match = SECRET_ASSIGNMENT_RE.search(line)
            if not match or looks_like_placeholder(match.group("value")):
                continue
            candidates.append({"path": str(rel), "line": lineno, "key": match.group("key")})
    return candidates[:50]


def config_doctor(
    *,
    codex_home: Path,
    farplane_home: Path,
    project_root: Path,
    process_env: dict[str, str] | None = None,
    doppler_runner: Callable[[list[str], Path], subprocess.CompletedProcess[str]] = _run_text,
) -> dict[str, Any]:
    env = dict(os.environ if process_env is None else process_env)
    farplane_config_path = farplane_home / "config.toml"
    rendered_config_path = codex_home / "config.toml"
    farplane_config = read_toml(farplane_config_path)
    rendered_config = read_toml(rendered_config_path)
    keys: list[dict[str, Any]] = []
    missing_required: list[str] = []
    doppler = doppler_status(project_root, doppler_runner)
    doppler_names = set(doppler.get("secretNames", []))

    for key in CONFIG_DOCTOR_SECRET_KEYS:
        sources = config_value_sources(key, env, farplane_config, rendered_config)
        if key in doppler_names:
            sources.append("doppler")
        required = key in CONFIG_DOCTOR_REQUIRED_KEYS
        if required and not sources:
            missing_required.append(key)
        keys.append(
            {
                "key": key,
                "required": required,
                "configured": bool(sources),
                "effectiveSource": sources[0] if sources else None,
                "sources": sources,
            }
        )

    permission_warnings = [
        warning
        for warning in [file_mode_warning(farplane_config_path), file_mode_warning(rendered_config_path)]
        if warning
    ]
    leak_candidates = scan_secret_literals(project_root)
    doppler_path = shutil.which("doppler")
    issues = [
        *(f"missing_required_secret:{key}" for key in missing_required),
        *doppler["issues"],
        *permission_warnings,
        *(f"tracked_secret_candidate:{row['path']}:{row['line']}:{row['key']}" for row in leak_candidates),
    ]
    hints: list[str] = []
    if missing_required:
        hints.append("export missing keys or run through a secret injector, e.g. `doppler run -- farplane install`")
    if doppler.get("declared") and not doppler.get("configured"):
        hints.append("run `doppler login` and `doppler setup` from this project")
    elif not doppler_path:
        hints.append("optional: install/configure Doppler if you want managed secret injection")
    if permission_warnings:
        hints.append("tighten private config permissions, e.g. `chmod 600 ~/.farplane/config.toml ~/.codex/config.toml`")

    return {
        "ok": not issues,
        "summary": "runtime secret sources look healthy" if not issues else "runtime secret sources need attention",
        "precedence": ["process_env", "~/.farplane/config.toml", "~/.codex/config.toml"],
        "farplaneConfig": str(farplane_config_path),
        "codexConfig": str(rendered_config_path),
        "projectRoot": str(project_root),
        "doppler": {
            "available": bool(doppler_path),
            "path": doppler_path,
            "declared": doppler["declared"],
            "configured": doppler["configured"],
            "project": doppler["project"],
            "config": doppler["config"],
            "secretNameCount": doppler["secretNameCount"],
            "example": "doppler run -- farplane install",
        },
        "keys": keys,
        "permissionWarnings": permission_warnings,
        "trackedSecretCandidates": leak_candidates,
        "issues": issues,
        "hints": hints,
    }
