#!/usr/bin/env python3
"""Private social account config loader for the Instagram account skill.

Reads runtime FARPLANE_INSTAGRAM_* / FARPLANE_META_* values first and uses
private ~/.farplane/config.toml as a fallback/cache without requiring social.env.
"""

from __future__ import annotations

import os
import tomllib
from pathlib import Path
from typing import Any


ENV_KEY_PATHS = {
    "FARPLANE_INSTAGRAM_USERNAME": ("social", "instagram", "username"),
    "FARPLANE_INSTAGRAM_API_MODE": ("social", "instagram", "api_mode"),
    "FARPLANE_INSTAGRAM_ACCESS_TOKEN": ("social", "instagram", "access_token"),
    "FARPLANE_INSTAGRAM_LOGIN_ACCESS_TOKEN": ("social", "instagram", "login_access_token"),
    "FARPLANE_INSTAGRAM_LOGIN_USER_ID": ("social", "instagram", "login_user_id"),
    "FARPLANE_INSTAGRAM_BUSINESS_ACCOUNT_ID": ("social", "instagram", "business_account_id"),
    "FARPLANE_META_APP_ID": ("social", "meta", "app_id"),
    "FARPLANE_META_APP_SECRET": ("social", "meta", "app_secret"),
    "FARPLANE_META_GRAPH_VERSION": ("social", "meta", "graph_version"),
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
