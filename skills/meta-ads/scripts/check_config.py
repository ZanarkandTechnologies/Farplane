#!/usr/bin/env python3
"""Check Meta Ads CLI credential readiness without exposing credentials."""

from __future__ import annotations

import json
import os
import shutil


CLI = "meta-ads-open-cli"
TOKEN_KEY = "META_ADS_ACCESS_TOKEN"


def main() -> int:
    token_ready = bool(os.environ.get(TOKEN_KEY))
    cli_ready = shutil.which(CLI) is not None
    read_ready = token_ready and cli_ready
    # This owner has no mutation capability. Keep the standard readiness field
    # explicit so no caller can interpret a valid read token as write approval.
    publish_ready = False
    payload: dict[str, object] = {
        "skill": "meta-ads",
        # For a read-only owner, ``ready`` means every capability it exposes is
        # ready. It is intentionally independent of the unavailable publish
        # branch above.
        "ready": read_ready,
        "read_ready": read_ready,
        "publish_ready": publish_ready,
        "redacted": True,
    }
    if not read_ready:
        missing: dict[str, list[str]] = {}
        if not token_ready:
            missing["read_all_of"] = [TOKEN_KEY]
        if not cli_ready:
            missing["runtime_all_of"] = [CLI]
        payload["missing"] = missing
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if read_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
