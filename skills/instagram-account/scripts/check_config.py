#!/usr/bin/env python3
"""Check private Instagram Login config without printing secrets."""

from __future__ import annotations

import json
from social_config import farplane_config_path, load_config_values, env_value


REQUIRED_FOR_READ = ["FARPLANE_INSTAGRAM_LOGIN_ACCESS_TOKEN"]
USER_ID_KEYS = ["FARPLANE_INSTAGRAM_BUSINESS_ACCOUNT_ID", "FARPLANE_INSTAGRAM_LOGIN_USER_ID"]
OPTIONAL_FOR_REFRESH_OR_APP = ["FARPLANE_META_APP_ID", "FARPLANE_META_APP_SECRET"]


def present(key: str, config_values: dict[str, str]) -> bool:
    return bool(env_value(key, config_values))


def main() -> int:
    config_path = farplane_config_path()
    config_values = load_config_values()
    read_ready = all(present(key, config_values) for key in REQUIRED_FOR_READ)
    user_id_ready = any(present(key, config_values) for key in USER_ID_KEYS)
    publish_ready = read_ready and user_id_ready
    app_ready = all(present(key, config_values) for key in OPTIONAL_FOR_REFRESH_OR_APP)
    payload = {
        "platform": "instagram",
        "api_mode": "instagram_login",
        "config_file": str(config_path),
        "config_file_exists": config_path.exists(),
        "read_ready": read_ready,
        "user_id_ready": user_id_ready,
        "publish_ready": publish_ready,
        "app_ready": app_ready,
        "missing_read": [key for key in REQUIRED_FOR_READ if not present(key, config_values)],
        "missing_user_id_any_of": [] if user_id_ready else USER_ID_KEYS,
        "missing_app": [key for key in OPTIONAL_FOR_REFRESH_OR_APP if not present(key, config_values)],
        "redacted": True,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if read_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
