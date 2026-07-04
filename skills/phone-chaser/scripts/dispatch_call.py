#!/usr/bin/env python3
"""Dispatch a Farplane Phone Chaser call through LiveKit."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CORE_DIR = ROOT / "bin" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from runtime_config import load_runtime_env  # noqa: E402


DEFAULT_URGENCY = "normal"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--message", required=True, help="Short reminder text to speak.")
    parser.add_argument(
        "--phone-number",
        help="Recipient in E.164 format. Defaults to FARPLANE_REMINDER_PHONE.",
    )
    parser.add_argument(
        "--agent-name",
        help="LiveKit agent name. Defaults to FARPLANE_PHONE_REMINDER_AGENT_NAME.",
    )
    parser.add_argument("--urgency", default=DEFAULT_URGENCY)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print sanitized dispatch metadata without placing a call.",
    )
    return parser.parse_args()


def env_value(env: dict[str, str], key: str) -> str:
    return str(env.get(key) or os.environ.get(key) or "").strip()


def require_value(label: str, value: str) -> str:
    if not value:
        raise SystemExit(f"missing required {label}")
    return value


def sanitize_phone(phone_number: str) -> str:
    if len(phone_number) <= 4:
        return "****"
    return f"...{phone_number[-4:]}"


def summarize_message(message: str) -> str:
    collapsed = " ".join(message.split())
    if len(collapsed) <= 100:
        return collapsed
    return f"{collapsed[:97]}..."


def build_payload(args: argparse.Namespace, env: dict[str, str]) -> tuple[str, str, dict[str, str]]:
    phone_number = args.phone_number or env_value(env, "FARPLANE_REMINDER_PHONE")
    agent_name = args.agent_name or env_value(env, "FARPLANE_PHONE_REMINDER_AGENT_NAME")
    require_value("phone number", phone_number)
    require_value("agent name", agent_name)
    message = require_value("message", str(args.message or "").strip())

    metadata = {
        "phone_number": phone_number,
        "message": message,
        "urgency": str(args.urgency or DEFAULT_URGENCY).strip() or DEFAULT_URGENCY,
    }
    return agent_name, phone_number, metadata


def dispatch(agent_name: str, metadata: dict[str, str]) -> subprocess.CompletedProcess[str]:
    cmd = [
        "lk",
        "dispatch",
        "create",
        "--new-room",
        "--agent-name",
        agent_name,
        "--metadata",
        json.dumps(metadata, separators=(",", ":")),
    ]
    return subprocess.run(
        cmd,
        cwd=ROOT / "farplane" / "phone-chaser",
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def main() -> int:
    args = parse_args()
    env = load_runtime_env()
    agent_name, phone_number, metadata = build_payload(args, env)

    sanitized = {
        "agent_name": agent_name,
        "phone_number": sanitize_phone(phone_number),
        "urgency": metadata["urgency"],
        "message_summary": summarize_message(metadata["message"]),
    }

    if args.dry_run:
        print(json.dumps({"dry_run": True, **sanitized}, indent=2))
        return 0

    result = dispatch(agent_name, metadata)
    print(json.dumps({"dry_run": False, **sanitized}, indent=2))
    print(result.stdout.rstrip())
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
