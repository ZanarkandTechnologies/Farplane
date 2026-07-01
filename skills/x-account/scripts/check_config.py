#!/usr/bin/env python3
"""Check private X account config without printing secret values."""

from __future__ import annotations

import json
from social_config import farplane_config_path, load_config_values, env_value


APP_ONLY_READ = ["FARPLANE_X_BEARER_TOKEN"]
OAUTH2_USER_READ = ["FARPLANE_X_OAUTH2_ACCESS_TOKEN"]
OAUTH2_REFRESH = ["FARPLANE_X_OAUTH2_CLIENT_ID", "FARPLANE_X_OAUTH2_CLIENT_SECRET", "FARPLANE_X_OAUTH2_REFRESH_TOKEN"]
OAUTH1_USER_CONTEXT = [
    "FARPLANE_X_ACCESS_TOKEN",
    "FARPLANE_X_ACCESS_TOKEN_SECRET",
    "FARPLANE_X_API_KEY",
    "FARPLANE_X_API_KEY_SECRET",
]


def present(key: str, config_values: dict[str, str]) -> bool:
    return bool(env_value(key, config_values))


def main() -> int:
    config_path = farplane_config_path()
    config_values = load_config_values()
    app_only_ready = all(present(key, config_values) for key in APP_ONLY_READ)
    oauth2_ready = all(present(key, config_values) for key in OAUTH2_USER_READ)
    oauth2_refresh_ready = oauth2_ready and all(present(key, config_values) for key in OAUTH2_REFRESH)
    oauth1_ready = all(present(key, config_values) for key in OAUTH1_USER_CONTEXT)
    read_ready = app_only_ready or oauth2_ready
    deep_ready = oauth2_ready or oauth1_ready
    payload = {
        "platform": "x",
        "config_file": str(config_path),
        "config_file_exists": config_path.exists(),
        "app_only_read_ready": app_only_ready,
        "oauth2_user_read_ready": oauth2_ready,
        "oauth2_refresh_ready": oauth2_refresh_ready,
        "oauth1_user_context_ready": oauth1_ready,
        "read_ready": read_ready,
        "deep_ready": deep_ready,
        "publish_ready": deep_ready,
        "missing_app_only_read": [key for key in APP_ONLY_READ if not present(key, config_values)],
        "missing_oauth2_user_read": [key for key in OAUTH2_USER_READ if not present(key, config_values)],
        "missing_oauth2_refresh": [key for key in OAUTH2_REFRESH if not present(key, config_values)],
        "missing_oauth1_user_context": [key for key in OAUTH1_USER_CONTEXT if not present(key, config_values)],
        "redacted": True,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if read_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
