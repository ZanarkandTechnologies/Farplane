#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIN = ROOT / "bin"
if str(BIN) not in sys.path:
    sys.path.insert(0, str(BIN))

import delegate_cli_agent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Sync the curated frontend/media skill bundle into the Pi/Kimi profile."
    )
    parser.add_argument("--profile", default="frontend-pi-kimi")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    profile = delegate_cli_agent.load_profile(args.profile, ROOT)
    copied, settings, doctor = delegate_cli_agent.sync_profile_skills(profile, ROOT)
    payload = {
        "summary": f"sync {profile.name}: copied {len(copied)} skills",
        "profile": profile.name,
        "copied_skills": copied,
        "settings": str(settings),
        "skill_bundle": doctor["skill_bundle"],
        "doctor": doctor,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(payload["summary"])
        print(f"settings: {settings}")
        for path in copied:
            print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
