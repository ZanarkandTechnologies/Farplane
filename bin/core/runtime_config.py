"""Farplane runtime config loading.

Inputs: ~/.farplane/config.toml, legacy ~/.farplane/config.json and
~/.farplane/secrets.json, ~/.codex/config.toml, optional
~/.codex/config.local.env, and process env.
Outputs: a merged env dict for Farplane Core commands and hooks.
Side effects: read-only filesystem access, except hydrate_process_env mutates
os.environ at process boundaries.
"""

from __future__ import annotations

import json
import os
import tomllib
from pathlib import Path
from typing import Mapping

DISABLE_ENV = "FARPLANE_CONFIG_DISABLE"


def farplane_home(env: Mapping[str, str] | None = None) -> Path:
    source = env if env is not None else os.environ
    configured = (source.get("FARPLANE_STATE_DIR") or source.get("FARPLANE_CONFIG_HOME") or "").strip()
    return Path(configured).expanduser() if configured else Path.home() / ".farplane"


def codex_home(env: Mapping[str, str] | None = None) -> Path:
    source = env if env is not None else os.environ
    configured = str(source.get("CODEX_HOME") or "").strip()
    return Path(configured).expanduser() if configured else Path.home() / ".codex"


def _read_json_object(path: Path) -> dict[str, object]:
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _read_toml_object(path: Path) -> dict[str, object]:
    try:
        parsed = tomllib.loads(path.read_text(encoding="utf-8"))
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


def _first_object_string_at(row: Mapping[str, object], paths: list[list[str]]) -> str:
    for path_parts in paths:
        value = _object_string_at(row, path_parts)
        if value:
            return value
    return ""


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
    config_toml = _read_toml_object(root / "config.toml")
    legacy_config = _read_json_object(root / "config.json")
    legacy_secrets = _read_json_object(root / "secrets.json")
    values: dict[str, str] = {}
    values.update(_structured_runtime_env(legacy_config, legacy_secrets))
    values.update(_iter_env_strings(legacy_config))
    values.update(_iter_env_strings(legacy_secrets))
    values.update(_structured_runtime_env(config_toml, config_toml))
    values.update(_iter_env_strings(config_toml))
    return values


def _structured_runtime_env(config: Mapping[str, object], secrets: Mapping[str, object]) -> dict[str, str]:
    aliases = {
        "FARPLANE_TELEMETRY_TOKEN": _first_object_string_at(
            secrets,
            [["convex", "telemetry_token"], ["convex", "telemetryToken"]],
        ),
        "FARPLANE_MESHY_API_KEY": _first_object_string_at(
            secrets,
            [["integrations", "meshy_api_key"], ["integrations", "meshyApiKey"]],
        ),
        "MESHY_API_KEY": _first_object_string_at(
            secrets,
            [["integrations", "meshy_api_key"], ["integrations", "meshyApiKey"]],
        ),
        "NOTION_API_KEY": _first_object_string_at(
            secrets,
            [["integrations", "notion_api_key"], ["integrations", "notionApiKey"]],
        ),
        "NOTION_TOKEN": (
            _first_object_string_at(secrets, [["env", "NOTION_TOKEN"], ["env", "NOTION_API_KEY"]])
            or _first_object_string_at(
                secrets,
                [
                    ["integrations", "notion_token"],
                    ["integrations", "notion_api_key"],
                    ["integrations", "notionApiKey"],
                ],
            )
        ),
        "REF_API_KEY": _first_object_string_at(secrets, [["integrations", "ref_api_key"]]),
        "CODEX_APP_SERVER_URL": (
            _first_object_string_at(
                config,
                [["env", "CODEX_APP_SERVER_URL"], ["env", "VITE_CODEX_APP_SERVER_URL"]],
            )
            or _first_object_string_at(
                config,
                [["runtime", "codex_app_server_url"], ["runtime", "codexAppServerUrl"]],
            )
        ),
        "FARPLANE_STATE_BASE": (
            _first_object_string_at(config, [["env", "FARPLANE_STATE_BASE"], ["env", "VITE_STATE_URL"]])
            or _first_object_string_at(config, [["runtime", "state_base"], ["runtime", "stateBase"]])
        ),
        "FARPLANE_CONVEX_SITE_URL": (
            _first_object_string_at(
                config,
                [["env", "FARPLANE_CONVEX_SITE_URL"], ["env", "CONVEX_SITE_URL"]],
            )
            or _first_object_string_at(config, [["convex", "site_url"], ["convex", "siteUrl"]])
        ),
        "CONVEX_URL": (
            _first_object_string_at(config, [["env", "CONVEX_URL"], ["env", "VITE_CONVEX_URL"]])
            or _first_object_string_at(config, [["convex", "client_url"], ["convex", "clientUrl"]])
        ),
        "VITE_CONVEX_URL": (
            _first_object_string_at(config, [["env", "VITE_CONVEX_URL"], ["env", "CONVEX_URL"]])
            or _first_object_string_at(config, [["convex", "client_url"], ["convex", "clientUrl"]])
        ),
    }
    return {key: value for key, value in aliases.items() if value}


def read_config_value(name: str, env: Mapping[str, str] | None = None) -> str:
    source = env if env is not None else os.environ
    return saved_runtime_env(source).get(name, "") or str(source.get(name) or "").strip()


def load_runtime_env(
    base_env: Mapping[str, str] | None = None,
    local_env_path: Path | None = None,
) -> dict[str, str]:
    merged = dict(base_env if base_env is not None else os.environ)
    rendered_toml_env = _iter_env_strings(
        _read_toml_object(codex_home(merged) / "config.toml")
    )
    for key, value in rendered_toml_env.items():
        merged.setdefault(key, value)
    if local_env_path is not None:
        for key, value in _read_env_file(local_env_path).items():
            merged.setdefault(key, value)
    merged.update(saved_runtime_env(merged))
    return merged


def hydrate_process_env(local_env_path: Path | None = None) -> None:
    os.environ.update(load_runtime_env(os.environ, local_env_path))
