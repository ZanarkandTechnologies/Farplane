#!/usr/bin/env python3
"""Check private Instagram account env configuration without printing secrets."""

from __future__ import annotations

import json
import os
from pathlib import Path


REQUIRED_FOR_READ = ["FARPLANE_INSTAGRAM_ACCESS_TOKEN", "FARPLANE_INSTAGRAM_BUSINESS_ACCOUNT_ID"]
OPTIONAL_FOR_PUBLISH = ["FARPLANE_META_APP_ID", "FARPLANE_META_APP_SECRET"]


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
    read_ready = all(present(key, file_values) for key in REQUIRED_FOR_READ)
    publish_ready = read_ready and all(present(key, file_values) for key in OPTIONAL_FOR_PUBLISH)
    payload = {
        "platform": "instagram",
        "env_file": str(env_path),
        "env_file_exists": env_path.exists(),
        "read_ready": read_ready,
        "publish_ready": publish_ready,
        "missing_read": [key for key in REQUIRED_FOR_READ if not present(key, file_values)],
        "missing_publish": [key for key in OPTIONAL_FOR_PUBLISH if not present(key, file_values)],
        "redacted": True,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if read_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
