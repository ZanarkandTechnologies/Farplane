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
        "--metadata-file",
        help="JSON file with additional bounded metadata such as review_context and review_callback.",
    )
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


def load_metadata_file(path_value: str | None) -> dict[str, object]:
    if not path_value:
        return {}
    path = Path(path_value).expanduser().resolve()
    with path.open("r", encoding="utf-8") as handle:
        parsed = json.load(handle)
    if not isinstance(parsed, dict):
        raise SystemExit("metadata file must contain a JSON object")
    validate_metadata_file(parsed)
    return parsed


def validate_metadata_file(metadata: dict[str, object]) -> None:
    allowed_top_level = {"message", "review_context", "review_callback", "call_id"}
    unknown = sorted(set(metadata) - allowed_top_level)
    if unknown:
        raise SystemExit(f"metadata file contains unsupported fields: {', '.join(unknown)}")

    review_context = metadata.get("review_context")
    if review_context is not None:
        if not isinstance(review_context, dict):
            raise SystemExit("review_context must be an object")
        allowed_context = {
            "title",
            "objective",
            "produced",
            "why_it_matters",
            "decision_question",
            "approve_effect",
            "revision_examples",
            "limits",
        }
        unknown_context = sorted(set(review_context) - allowed_context)
        if unknown_context:
            raise SystemExit(f"review_context contains unsupported fields: {', '.join(unknown_context)}")

    review_callback = metadata.get("review_callback")
    if review_callback is not None:
        if not isinstance(review_callback, dict):
            raise SystemExit("review_callback must be an object")
        allowed_callback = {"review_id", "webhook_url", "capability"}
        unknown_callback = sorted(set(review_callback) - allowed_callback)
        if unknown_callback:
            raise SystemExit(f"review_callback contains unsupported fields: {', '.join(unknown_callback)}")


def sanitize_review_metadata(metadata: dict[str, object]) -> dict[str, object]:
    review_context = metadata.get("review_context")
    callback = metadata.get("review_callback")
    return {
        "has_review_context": isinstance(review_context, dict),
        "review_id": callback.get("review_id") if isinstance(callback, dict) else None,
        "has_review_webhook": bool(callback.get("webhook_url")) if isinstance(callback, dict) else False,
        "has_review_capability": bool(callback.get("capability")) if isinstance(callback, dict) else False,
    }


def build_payload(args: argparse.Namespace, env: dict[str, str]) -> tuple[str, str, dict[str, object]]:
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
    metadata.update(load_metadata_file(args.metadata_file))
    return agent_name, phone_number, metadata


def dispatch(agent_name: str, metadata: dict[str, object]) -> subprocess.CompletedProcess[str]:
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
        "message_summary": summarize_message(str(metadata["message"])),
        "review": sanitize_review_metadata(metadata),
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
