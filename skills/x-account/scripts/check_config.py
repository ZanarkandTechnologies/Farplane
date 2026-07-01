#!/usr/bin/env python3
"""Check private X account env configuration without printing secret values."""

from __future__ import annotations

import json
import os
from pathlib import Path


APP_ONLY_READ = ["FARPLANE_X_BEARER_TOKEN"]
OAUTH2_USER_READ = ["FARPLANE_X_OAUTH2_ACCESS_TOKEN"]
OAUTH2_REFRESH = ["FARPLANE_X_OAUTH2_CLIENT_ID", "FARPLANE_X_OAUTH2_CLIENT_SECRET", "FARPLANE_X_OAUTH2_REFRESH_TOKEN"]
OAUTH1_USER_CONTEXT = [
    "FARPLANE_X_ACCESS_TOKEN",
    "FARPLANE_X_ACCESS_TOKEN_SECRET",
    "FARPLANE_X_API_KEY",
    "FARPLANE_X_API_KEY_SECRET",
]


def load_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :]
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def present(key: str, file_values: dict[str, str]) -> bool:
    return bool(os.environ.get(key) or file_values.get(key))


def main() -> int:
    env_path = Path.home() / ".codex" / "private" / "social.env"
    file_values = load_env_file(env_path)
    app_only_ready = all(present(key, file_values) for key in APP_ONLY_READ)
    oauth2_ready = all(present(key, file_values) for key in OAUTH2_USER_READ)
    oauth2_refresh_ready = oauth2_ready and all(present(key, file_values) for key in OAUTH2_REFRESH)
    oauth1_ready = all(present(key, file_values) for key in OAUTH1_USER_CONTEXT)
    read_ready = app_only_ready or oauth2_ready
    deep_ready = oauth2_ready or oauth1_ready
    payload = {
        "platform": "x",
        "env_file": str(env_path),
        "env_file_exists": env_path.exists(),
        "app_only_read_ready": app_only_ready,
        "oauth2_user_read_ready": oauth2_ready,
        "oauth2_refresh_ready": oauth2_refresh_ready,
        "oauth1_user_context_ready": oauth1_ready,
        "read_ready": read_ready,
        "deep_ready": deep_ready,
        "publish_ready": deep_ready,
        "missing_app_only_read": [key for key in APP_ONLY_READ if not present(key, file_values)],
        "missing_oauth2_user_read": [key for key in OAUTH2_USER_READ if not present(key, file_values)],
        "missing_oauth2_refresh": [key for key in OAUTH2_REFRESH if not present(key, file_values)],
        "missing_oauth1_user_context": [key for key in OAUTH1_USER_CONTEXT if not present(key, file_values)],
        "redacted": True,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if read_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
