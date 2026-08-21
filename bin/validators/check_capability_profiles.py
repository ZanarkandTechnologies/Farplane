#!/usr/bin/env python3
"""Validate one project's optional Project PM capability-profile policy."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = ROOT / "bin" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from farplane_capability_profiles import CapabilityProfileError, resolve_capability_profiles


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        payload = resolve_capability_profiles(Path(args.project_root))
    except CapabilityProfileError as exc:
        payload = {"ok": False, "error": str(exc)}
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif payload["ok"]:
        print(
            "capability profiles: ok "
            f"({payload['enforcement']['state']}, "
            f"{len(payload['catalog']['skill_ids'])} skills, "
            f"{len(payload['catalog']['mcp_server_ids'])} MCP servers)"
        )
    else:
        print(f"capability profiles: fail ({payload['error']})")
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
