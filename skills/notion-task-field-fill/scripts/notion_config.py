#!/usr/bin/env python3
"""Load the canonical Notion token for notion-task-field-fill scripts."""

from __future__ import annotations

import os
from typing import Mapping


def notion_token(env: Mapping[str, str] | None = None) -> str:
    source = env if env is not None else os.environ
    return str(source.get("NOTION_TOKEN") or "").strip()


def require_notion_token(env: Mapping[str, str] | None = None) -> str:
    value = notion_token(env)
    if not value:
        raise RuntimeError(
            "Missing Notion token. Run through `farplane run -- <command>` "
            "or Doppler, or export NOTION_TOKEN for this run."
        )
    return value


def notion_api_env(env: Mapping[str, str] | None = None) -> dict[str, str]:
    return {"NOTION_TOKEN": require_notion_token(env)}
