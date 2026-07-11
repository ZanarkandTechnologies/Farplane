#!/usr/bin/env python3
"""Private social account config loader for the X account skill.

Reads runtime FARPLANE_X_* values first and uses private
~/.farplane/config.toml as a fallback/cache without requiring social.env.
"""

from __future__ import annotations

import os
import tomllib
from pathlib import Path
from typing import Any


ENV_KEY_PATHS = {
    "FARPLANE_X_BEARER_TOKEN": ("social", "x", "bearer_token"),
    "FARPLANE_X_OAUTH2_CLIENT_ID": ("social", "x", "oauth2_client_id"),
    "FARPLANE_X_OAUTH2_CLIENT_SECRET": ("social", "x", "oauth2_client_secret"),
    "FARPLANE_X_OAUTH2_ACCESS_TOKEN": ("social", "x", "oauth2_access_token"),
    "FARPLANE_X_OAUTH2_REFRESH_TOKEN": ("social", "x", "oauth2_refresh_token"),
    "FARPLANE_X_ACCESS_TOKEN": ("social", "x", "access_token"),
    "FARPLANE_X_ACCESS_TOKEN_SECRET": ("social", "x", "access_token_secret"),
    "FARPLANE_X_API_KEY": ("social", "x", "api_key"),
    "FARPLANE_X_API_KEY_SECRET": ("social", "x", "api_key_secret"),
    "FARPLANE_X_USER_ID": ("social", "x", "user_id"),
    "FARPLANE_X_USERNAME": ("social", "x", "username"),
}


def farplane_config_path() -> Path:
    root = os.environ.get("FARPLANE_STATE_DIR") or os.environ.get("FARPLANE_HOME")
    return Path(root).expanduser() / "config.toml" if root else Path.home() / ".farplane" / "config.toml"


def _read_config() -> dict[str, Any]:
    path = farplane_config_path()
    if not path.exists():
        return {}
    with path.open("rb") as handle:
        return tomllib.load(handle)


def _value_at(data: dict[str, Any], path: tuple[str, ...]) -> str | None:
    current: Any = data
    for part in path:
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    if isinstance(current, str):
        return current.strip() or None
    return str(current).strip() if current is not None else None


def load_config_values() -> dict[str, str]:
    data = _read_config()
    values: dict[str, str] = {}
    for key, path in ENV_KEY_PATHS.items():
        value = _value_at(data, path)
        if value:
            values[key] = value
    return values


def env_value(key: str, config_values: dict[str, str] | None = None) -> str | None:
    return os.environ.get(key) or (config_values or {}).get(key) or None
