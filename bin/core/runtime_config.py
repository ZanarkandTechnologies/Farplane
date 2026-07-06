"""Farplane runtime config loading.

Inputs: process env, ~/.farplane/config.toml, and ~/.codex/config.toml.
Outputs: a merged env dict for Farplane Core commands and hooks.
Side effects: read-only filesystem access, except hydrate_process_env mutates
os.environ at process boundaries.

Precedence is process env, then private Farplane config, then rendered Codex
adapter config. `~/.farplane/config.toml` is a local fallback/cache, not the
canonical source for secrets when a runtime injector such as Doppler is present.
"""

from __future__ import annotations

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


def saved_runtime_env(env: Mapping[str, str] | None = None) -> dict[str, str]:
    source = env if env is not None else os.environ
    if str(source.get(DISABLE_ENV) or "").strip() == "1":
        return {}

    root = farplane_home(source)
    config_toml = _read_toml_object(root / "config.toml")
    values: dict[str, str] = {}
    values.update(_structured_runtime_env(config_toml, config_toml))
    values.update(_iter_env_strings(config_toml))
    return values


def _structured_runtime_env(config: Mapping[str, object], secrets: Mapping[str, object]) -> dict[str, str]:
    aliases = {
        "FARPLANE_TELEMETRY_TOKEN": _first_object_string_at(
            secrets,
            [["convex", "telemetry_token"]],
        ),
        "FARPLANE_MESHY_API_KEY": _first_object_string_at(
            secrets,
            [["integrations", "meshy_api_key"]],
        ),
        "MESHY_API_KEY": _first_object_string_at(
            secrets,
            [["integrations", "meshy_api_key"]],
        ),
        "NOTION_TOKEN": _first_object_string_at(
            secrets, [["integrations", "notion_token"]]
        ),
        "REF_API_KEY": _first_object_string_at(secrets, [["integrations", "ref_api_key"]]),
        "CODEX_APP_SERVER_URL": (
            _first_object_string_at(
                config,
                [["env", "CODEX_APP_SERVER_URL"]],
            )
            or _first_object_string_at(
                config,
                [["runtime", "codex_app_server_url"]],
            )
        ),
        "FARPLANE_STATE_BASE": (
            _first_object_string_at(config, [["env", "FARPLANE_STATE_BASE"]])
            or _first_object_string_at(config, [["runtime", "state_base"]])
        ),
        "FARPLANE_CONVEX_SITE_URL": (
            _first_object_string_at(
                config,
                [["env", "FARPLANE_CONVEX_SITE_URL"]],
            )
            or _first_object_string_at(config, [["convex", "site_url"]])
        ),
        "CONVEX_URL": (
            _first_object_string_at(config, [["env", "CONVEX_URL"]])
            or _first_object_string_at(config, [["convex", "client_url"]])
        ),
        "VITE_CONVEX_URL": (
            _first_object_string_at(config, [["env", "VITE_CONVEX_URL"]])
            or _first_object_string_at(config, [["convex", "client_url"]])
        ),
        "LIVEKIT_URL": _first_object_string_at(
            secrets, [["livekit", "url"]]
        ),
        "LIVEKIT_API_KEY": _first_object_string_at(
            secrets, [["livekit", "api_key"]]
        ),
        "LIVEKIT_API_SECRET": _first_object_string_at(
            secrets, [["livekit", "api_secret"]]
        ),
        "LIVEKIT_PHONE_NUMBER": _first_object_string_at(
            config, [["livekit", "phone_number"], ["phone_reminder", "caller_number"]]
        ),
        "LIVEKIT_PHONE_NUMBER_ID": _first_object_string_at(
            config, [["livekit", "phone_number_id"]]
        ),
        "LIVEKIT_SIP_DISPATCH_RULE_ID": _first_object_string_at(
            config, [["livekit", "sip_dispatch_rule_id"]]
        ),
        "LIVEKIT_SIP_TRUNK_ID": _first_object_string_at(
            secrets,
            [
                ["livekit", "sip_outbound_trunk_id"],
                ["livekit", "sip", "outbound_trunk_id"],
            ],
        ),
        "LIVEKIT_SIP_NUMBER": _first_object_string_at(
            config,
            [
                ["livekit", "sip_outbound_number"],
                ["livekit", "sip", "outbound_number"],
                ["phone_reminder", "caller_number"],
                ["livekit", "phone_number"],
            ],
        ),
        "LIVEKIT_SIP_OUTBOUND_ADDRESS": _first_object_string_at(
            secrets,
            [
                ["livekit", "sip_outbound_address"],
                ["livekit", "sip", "outbound_address"],
            ],
        ),
        "LIVEKIT_SIP_AUTH_USERNAME": _first_object_string_at(
            secrets,
            [
                ["livekit", "sip_auth_username"],
                ["livekit", "sip", "auth_username"],
            ],
        ),
        "LIVEKIT_SIP_AUTH_PASSWORD": _first_object_string_at(
            secrets,
            [
                ["livekit", "sip_auth_password"],
                ["livekit", "sip", "auth_password"],
            ],
        ),
        "TELNYX_API_KEY": _first_object_string_at(
            secrets,
            [
                ["livekit", "sip", "telnyx_api_key"],
                ["integrations", "telnyx_api_key"],
            ],
        ),
        "FISH_API_KEY": _first_object_string_at(
            secrets, [["fish_audio", "api_key"]]
        ),
        "FISH_AUDIO_REFERENCE_ID": _first_object_string_at(
            config, [["fish_audio", "reference_id"]]
        ),
        "FISH_AUDIO_MODEL": _first_object_string_at(
            config, [["fish_audio", "model"]]
        ),
        "FISH_AUDIO_LATENCY_MODE": _first_object_string_at(
            config, [["fish_audio", "latency_mode"]]
        ),
        "FARPLANE_REMINDER_PHONE": _first_object_string_at(
            config, [["phone_reminder", "recipient_phone"]]
        ),
        "FARPLANE_PHONE_REMINDER_AGENT_NAME": _first_object_string_at(
            config, [["phone_reminder", "agent_name"]]
        ),
    }
    return {key: value for key, value in aliases.items() if value}


def read_config_value(name: str, env: Mapping[str, str] | None = None) -> str:
    source = env if env is not None else os.environ
    return str(source.get(name) or "").strip() or saved_runtime_env(source).get(name, "")


def load_runtime_env(base_env: Mapping[str, str] | None = None) -> dict[str, str]:
    process_env = dict(base_env if base_env is not None else os.environ)
    if str(process_env.get(DISABLE_ENV) or "").strip() == "1":
        return process_env

    merged: dict[str, str] = {}
    rendered_toml_env = _iter_env_strings(
        _read_toml_object(codex_home(process_env) / "config.toml")
    )
    merged.update(rendered_toml_env)
    merged.update(saved_runtime_env(process_env))
    merged.update(process_env)
    return merged


def hydrate_process_env() -> None:
    os.environ.update(load_runtime_env(os.environ))
