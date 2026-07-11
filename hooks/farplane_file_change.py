#!/usr/bin/env python3
"""Installed PostToolUse boundary for Core-owned file events and mining."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[1] / "bin" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from farplane_file_events import find_project_root
from farplane_mining import handle_file_change


def handle_payload(payload: dict[str, Any], project_root: Path | None = None) -> dict[str, Any]:
    root = project_root or find_project_root(
        str(payload.get("cwd") or payload.get("project_path") or payload.get("projectPath") or os.getcwd())
    )
    return handle_file_change(payload, root)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            return 0
        result = handle_payload(payload)
        if os.getenv("FARPLANE_FILE_EVENT_DEBUG") == "1":
            print(json.dumps(result, indent=2, sort_keys=True), file=sys.stderr)
    except Exception as exc:
        # Hooks must not block the operator. Durable events already appended to
        # the outbox remain retryable by the next invocation or manual drain.
        print(f"farplane file event: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
