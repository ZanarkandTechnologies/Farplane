#!/usr/bin/env python3
"""Check injected X account credentials without printing secret values."""

from __future__ import annotations

import json
from runtime_env import load_runtime_values, env_value


APP_ONLY_READ = ["FARPLANE_X_BEARER_TOKEN"]
OAUTH2_USER_READ = ["FARPLANE_X_OAUTH2_ACCESS_TOKEN"]
OAUTH1_USER_CONTEXT = [
    "FARPLANE_X_ACCESS_TOKEN",
    "FARPLANE_X_ACCESS_TOKEN_SECRET",
    "FARPLANE_X_API_KEY",
    "FARPLANE_X_API_KEY_SECRET",
]


def present(key: str, runtime_values: dict[str, str]) -> bool:
    return bool(env_value(key, runtime_values))


def main() -> int:
    runtime_values = load_runtime_values()
    app_only_ready = all(present(key, runtime_values) for key in APP_ONLY_READ)
    oauth2_ready = all(present(key, runtime_values) for key in OAUTH2_USER_READ)
    oauth1_ready = all(present(key, runtime_values) for key in OAUTH1_USER_CONTEXT)
    read_ready = app_only_ready or oauth2_ready
    publish_ready = oauth2_ready or oauth1_ready
    ready = read_ready and publish_ready
    payload = {
        "skill": "x-account",
        "ready": ready,
        "read_ready": read_ready,
        "publish_ready": publish_ready,
        "redacted": True,
    }
    if not ready:
        payload["missing"] = {}
        if not read_ready:
            payload["missing"]["read_any_of"] = [APP_ONLY_READ, OAUTH2_USER_READ]
        if not publish_ready:
            payload["missing"]["publish_any_of"] = [OAUTH2_USER_READ, OAUTH1_USER_CONTEXT]
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
