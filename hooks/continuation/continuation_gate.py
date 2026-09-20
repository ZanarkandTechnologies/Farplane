#!/usr/bin/env python3
"""Independent Stop nudge; no Goal completion authority or persisted task state."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import subprocess

ROOT = Path(__file__).resolve().parents[2]
for directory in (ROOT / "bin" / "runtime", ROOT / "bin" / "core", ROOT / "hooks"):
    sys.path.insert(0, str(directory))

from continuation import evaluate_stop  # noqa: E402
from runtime_config import load_runtime_env  # noqa: E402
from skill_suggestion import _provider_config  # noqa: E402


def run_gate(payload: dict, *, credential_child: bool = False) -> dict | None:
    env = load_runtime_env()
    provider = _provider_config(env)
    if provider and not env.get(provider["api_key_env"], "").strip() and not credential_child:
        # Global hooks may run in any project. Credential scope belongs to this
        # installed Farplane source, never the caller's working directory.
        try:
            child = subprocess.run(
                [str(ROOT / "bin" / "farplane"), "run", "--", sys.executable,
                 str(Path(__file__).resolve()), "--credential-child"],
                cwd=ROOT, input=json.dumps(payload), capture_output=True,
                text=True, timeout=4,
            )
            if child.returncode == 0 and child.stdout.strip():
                result = json.loads(child.stdout)
                if isinstance(result, dict) and result.get("decision") == "block":
                    return result
        except (OSError, subprocess.TimeoutExpired, ValueError):
            pass
        # Never expose provider/setup errors as feedback to unrelated tasks.
        return None
    return evaluate_stop(payload, environ=env)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        if isinstance(payload, dict):
            result = run_gate(payload, credential_child="--credential-child" in sys.argv[1:])
            if result:
                print(json.dumps(result, separators=(",", ":")))
    except Exception:
        # A hook outage must never strand a conversation.
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
