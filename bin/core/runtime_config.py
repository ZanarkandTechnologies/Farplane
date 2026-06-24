"""Farplane runtime config loading.

Inputs: ~/.farplane/config.json, ~/.farplane/secrets.json, optional
~/.codex/config.local.env, and process env.
Outputs: a merged env dict for Farplane Core commands and hooks.
Side effects: read-only filesystem access, except hydrate_process_env mutates
os.environ at process boundaries.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Mapping

DISABLE_ENV = "FARPLANE_CONFIG_DISABLE"


def farplane_home(env: Mapping[str, str] | None = None) -> Path:
    source = env if env is not None else os.environ
    configured = (source.get("FARPLANE_STATE_DIR") or source.get("FARPLANE_CONFIG_HOME") or "").strip()
    return Path(configured).expanduser() if configured else Path.home() / ".farplane"


def _read_json_object(path: Path) -> dict[str, object]:
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _object_string_at(row: Mapping[str, object], path_parts: list[str]) -> str:
    current: object = row
    for part in path_parts:
        if not isinstance(current, dict):
            return ""
        current = current.get(part)
    return current.strip() if isinstance(current, str) else ""


def _iter_env_strings(row: Mapping[str, object]) -> dict[str, str]:
    env = row.get("env")
    if not isinstance(env, dict):
        return {}
    return {
        str(key): value.strip()
        for key, value in env.items()
        if isinstance(key, str) and isinstance(value, str) and value.strip()
    }


def _read_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        clean_key = key.strip()
        if clean_key:
            values[clean_key] = value.strip().strip("\"'")
    return values


def saved_runtime_env(env: Mapping[str, str] | None = None) -> dict[str, str]:
    source = env if env is not None else os.environ
    if str(source.get(DISABLE_ENV) or "").strip() == "1":
        return {}

    root = farplane_home(source)
    config = _read_json_object(root / "config.json")
    secrets = _read_json_object(root / "secrets.json")
    values: dict[str, str] = {}
    values.update(_iter_env_strings(config))
    values.update(_iter_env_strings(secrets))

    structured_aliases = {
        "FARPLANE_TELEMETRY_TOKEN": _object_string_at(secrets, ["convex", "telemetryToken"]),
        "FARPLANE_MESHY_API_KEY": _object_string_at(secrets, ["integrations", "meshyApiKey"]),
        "MESHY_API_KEY": _object_string_at(secrets, ["integrations", "meshyApiKey"]),
        "NOTION_API_KEY": _object_string_at(secrets, ["integrations", "notionApiKey"]),
        "NOTION_TOKEN": (
            _object_string_at(secrets, ["env", "NOTION_TOKEN"])
            or _object_string_at(secrets, ["env", "NOTION_API_KEY"])
            or _object_string_at(secrets, ["integrations", "notionApiKey"])
        ),
        "CODEX_APP_SERVER_URL": (
            _object_string_at(config, ["env", "CODEX_APP_SERVER_URL"])
            or _object_string_at(config, ["env", "VITE_CODEX_APP_SERVER_URL"])
            or _object_string_at(config, ["runtime", "codexAppServerUrl"])
        ),
        "FARPLANE_STATE_BASE": (
            _object_string_at(config, ["env", "FARPLANE_STATE_BASE"])
            or _object_string_at(config, ["env", "VITE_STATE_URL"])
            or _object_string_at(config, ["runtime", "stateBase"])
        ),
        "FARPLANE_CONVEX_SITE_URL": (
            _object_string_at(config, ["env", "FARPLANE_CONVEX_SITE_URL"])
            or _object_string_at(config, ["env", "CONVEX_SITE_URL"])
            or _object_string_at(config, ["convex", "siteUrl"])
        ),
    }
    for key, value in structured_aliases.items():
        if value:
            values[key] = value
    return values


def read_config_value(name: str, env: Mapping[str, str] | None = None) -> str:
    source = env if env is not None else os.environ
    return saved_runtime_env(source).get(name, "") or str(source.get(name) or "").strip()


def load_runtime_env(
    base_env: Mapping[str, str] | None = None,
    local_env_path: Path | None = None,
) -> dict[str, str]:
    merged = dict(base_env if base_env is not None else os.environ)
    if local_env_path is not None:
        for key, value in _read_env_file(local_env_path).items():
            merged.setdefault(key, value)
    merged.update(saved_runtime_env(merged))
    return merged


def hydrate_process_env(local_env_path: Path | None = None) -> None:
    os.environ.update(load_runtime_env(os.environ, local_env_path))
