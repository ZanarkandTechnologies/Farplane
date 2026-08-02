#!/usr/bin/env python3
"""Read X credentials from the injected process environment."""

from __future__ import annotations

import os


def load_runtime_values() -> dict[str, str]:
    return {key: value for key, value in os.environ.items() if key.startswith("FARPLANE_X_")}


def env_value(key: str, runtime_values: dict[str, str] | None = None) -> str | None:
    return os.environ.get(key) or (runtime_values or {}).get(key) or None
