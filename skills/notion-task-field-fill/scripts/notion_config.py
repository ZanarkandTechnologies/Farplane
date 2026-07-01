#!/usr/bin/env python3
"""Load the canonical Notion API key for notion-task-field-fill scripts."""

from __future__ import annotations

import os
import tomllib
from pathlib import Path
from typing import Mapping


def farplane_config_path(env: Mapping[str, str] | None = None) -> Path:
    source = env if env is not None else os.environ
    root = (
        source.get("FARPLANE_STATE_DIR")
        or source.get("FARPLANE_CONFIG_HOME")
        or source.get("FARPLANE_HOME")
        or str(Path.home() / ".farplane")
    )
    return Path(root).expanduser() / "config.toml"


def _object_string_at(row: Mapping[str, object], path_parts: list[str]) -> str:
    current: object = row
    for part in path_parts:
        if not isinstance(current, dict):
            return ""
        current = current.get(part)
    return current.strip() if isinstance(current, str) else ""


def _read_toml(path: Path) -> dict[str, object]:
    try:
        parsed = tomllib.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def notion_api_key(env: Mapping[str, str] | None = None) -> str:
    source = env if env is not None else os.environ
    explicit = str(source.get("NOTION_API_KEY") or "").strip()
    if explicit:
        return explicit
    config = _read_toml(farplane_config_path(source))
    return _object_string_at(config, ["integrations", "notion_api_key"])


def require_notion_api_key(env: Mapping[str, str] | None = None) -> str:
    value = notion_api_key(env)
    if not value:
        raise RuntimeError(
            "Missing Notion API key. Set [integrations].notion_api_key in "
            "~/.farplane/config.toml or export NOTION_API_KEY for this run."
        )
    return value


def notion_api_env(env: Mapping[str, str] | None = None) -> dict[str, str]:
    return {"NOTION_API_KEY": require_notion_api_key(env)}
