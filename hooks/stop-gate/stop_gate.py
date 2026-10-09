#!/usr/bin/env python3
"""The one blocking Stop gate: length, then continuation, then response format.

Each stop returns at most one block. Length is deterministic and runs first;
continuation and format share one Jev request. No completion authority.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
for directory in (ROOT / "bin" / "runtime", ROOT / "bin" / "core", ROOT / "hooks"):
    sys.path.insert(0, str(directory))

from continuation import evaluate_stop  # noqa: E402
from runtime_config import load_runtime_env  # noqa: E402
from hook_delivery import report_gate_block  # noqa: E402
from skill_suggestion import _provider_config  # noqa: E402

sys.path.insert(0, str(ROOT / "hooks" / "response-length"))
from final_response_gate import (  # noqa: E402
    configured_max_prose_lines, configured_max_prose_words, gate_response,
)
import response_format  # noqa: E402

CHECKS_ENV = "FARPLANE_STOP_CHECKS"
ALL_CHECKS = frozenset({"length", "continuation", "format"})


def configured_checks(env: dict[str, str]) -> frozenset[str]:
    raw = env.get(CHECKS_ENV)
    if raw is None:
        return ALL_CHECKS
    return frozenset(part.strip() for part in raw.split(",")) & ALL_CHECKS


def jev_gate(payload: dict, checks: frozenset[str], env: dict[str, str], *,
             credential_child: bool = False) -> dict | None:
    provider = _provider_config(env)
    if provider and not env.get(provider["api_key_env"], "").strip() and not credential_child:
        # Global hooks may run in any project. Credential scope belongs to this
        # installed Farplane source, never the caller's working directory.
        try:
            child = subprocess.run(
                [str(ROOT / "bin" / "farplane"), "run", "--", sys.executable,
                 str(Path(__file__).resolve()), "--credential-child"],
                cwd=ROOT, input=json.dumps(payload), capture_output=True,
                text=True, timeout=4, env={**os.environ, CHECKS_ENV: ",".join(sorted(checks))},
            )
            if child.returncode == 0 and child.stdout.strip():
                result = json.loads(child.stdout)
                if isinstance(result, dict) and result.get("decision") == "block":
                    return result
        except (OSError, subprocess.TimeoutExpired, ValueError):
            pass
        # Never expose provider/setup errors as feedback to unrelated tasks.
        return None
    return evaluate_stop(payload, environ=env, checks=checks)


def run_gate(payload: dict, *, credential_child: bool = False) -> dict | None:
    env = load_runtime_env()
    checks = configured_checks(env)
    if "length" in checks and not credential_child:
        result = gate_response(payload, configured_max_prose_words(env),
                               configured_max_prose_lines(env))
        if result:
            return result
    if checks & {"continuation", "format"}:
        return jev_gate(payload, checks - {"length"}, env, credential_child=credential_child)
    return None


def gate_name(reason: str) -> str:
    if response_format.TAG in reason:
        return "response-format"
    if "farplane-continuation" in reason:
        return "continuation"
    return "response-length"


def main() -> int:
    credential_child = "--credential-child" in sys.argv[1:]
    try:
        payload = json.load(sys.stdin)
        if isinstance(payload, dict):
            result = run_gate(payload, credential_child=credential_child)
            if result:
                if not credential_child:
                    report_gate_block(payload, gate_name(result["reason"]))
                print(json.dumps(result, separators=(",", ":")))
    except Exception:
        # A hook outage must never strand a conversation.
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
