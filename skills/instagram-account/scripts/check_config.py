#!/usr/bin/env python3
"""Check injected Instagram Login credentials without printing secrets."""

from __future__ import annotations

import json
from runtime_env import load_runtime_values, env_value


REQUIRED_FOR_READ = ["FARPLANE_INSTAGRAM_LOGIN_ACCESS_TOKEN"]
USER_ID_KEYS = ["FARPLANE_INSTAGRAM_BUSINESS_ACCOUNT_ID", "FARPLANE_INSTAGRAM_LOGIN_USER_ID"]


def present(key: str, runtime_values: dict[str, str]) -> bool:
    return bool(env_value(key, runtime_values))


def main() -> int:
    runtime_values = load_runtime_values()
    read_ready = all(present(key, runtime_values) for key in REQUIRED_FOR_READ)
    user_id_ready = any(present(key, runtime_values) for key in USER_ID_KEYS)
    publish_ready = read_ready and user_id_ready
    ready = read_ready and publish_ready
    payload = {
        "skill": "instagram-account",
        "ready": ready,
        "read_ready": read_ready,
        "publish_ready": publish_ready,
        "redacted": True,
    }
    if not ready:
        payload["missing"] = {}
        if not read_ready:
            payload["missing"]["read_all_of"] = REQUIRED_FOR_READ
        if not user_id_ready:
            payload["missing"]["publish_any_of"] = USER_ID_KEYS
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
