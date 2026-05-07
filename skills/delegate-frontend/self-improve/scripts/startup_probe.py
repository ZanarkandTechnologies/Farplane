#!/usr/bin/env python3
"""Build or execute a minimal Pi/Kimi startup probe for delegate-frontend."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import phase_prompt_compiler


def project_root() -> Path:
    return Path(__file__).resolve().parents[4]


def build_probe_command(args: argparse.Namespace, prompt_path: Path) -> list[str]:
    command = [
        "python3",
        "bin/delegate_cli_agent.py",
        "run",
        "--profile",
        args.profile,
        "--checkout",
        "shared",
        "--thinking",
        args.thinking,
        "--run-id",
        args.run_id,
        "--artifact-dir",
        str(args.artifact_dir),
        "--prompt-file",
        str(prompt_path),
        "--expect-output",
        args.probe_output,
        "--first-write-timeout-seconds",
        str(args.first_write_timeout_seconds),
        "--timeout-seconds",
        str(args.timeout_seconds),
        "--json",
    ]
    if args.dry_run:
        command.append("--dry-run")
    return command


def write_probe_prompt(args: argparse.Namespace, prompt_path: Path) -> None:
    prompt_args = argparse.Namespace(
        phase="startup",
        brief=(
            "This is a startup health probe only. Create the probe output, write "
            "one sentence saying the CLI reached first-write, then stop."
        ),
        brief_file="",
        owned_output=[args.probe_output],
        handoff_path=str(Path(args.artifact_dir) / "handoff.md"),
        recipe_id="cinematic-industrial-scroll",
        taste_profile_id="terminal-mission-control",
        effect_stack_id="video-frame-sequence-scroll-scrub",
        acceptance=[],
        output="",
    )
    prompt = phase_prompt_compiler.compile_prompt(prompt_args)
    prompt_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_path.write_text(prompt, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default="frontend-pi-kimi")
    parser.add_argument("--run-id", default="delegate-frontend-startup-probe")
    parser.add_argument("--probe-output", default="")
    parser.add_argument("--artifact-dir", default="")
    # MEM-0086: low thinking crossed first-write reliably where the default
    # high-thinking startup probe produced only a session file.
    parser.add_argument("--thinking", default="low")
    parser.add_argument("--first-write-timeout-seconds", type=int, default=90)
    parser.add_argument("--timeout-seconds", type=int, default=150)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def resolve_paths(args: argparse.Namespace, root: Path) -> None:
    if not args.probe_output:
        args.probe_output = f".harness/delegate-frontend/startup-probes/{args.run_id}/PROBE.md"
    artifact_dir = Path(args.artifact_dir or root / ".harness" / "external-cli" / "runs" / args.run_id).expanduser()
    if not artifact_dir.is_absolute():
        artifact_dir = root / artifact_dir
    args.artifact_dir = artifact_dir


def main() -> int:
    args = parse_args()
    root = project_root()
    resolve_paths(args, root)
    prompt_path = args.artifact_dir / "startup-probe-prompt.md"
    write_probe_prompt(args, prompt_path)
    command = build_probe_command(args, prompt_path)
    payload = {
        "run_id": args.run_id,
        "prompt_path": str(prompt_path),
        "probe_output": args.probe_output,
        "artifact_dir": str(args.artifact_dir),
        "command": command,
        "mode": "execute" if args.execute else "plan",
        "dry_run": bool(args.dry_run),
    }
    if args.execute:
        completed = subprocess.run(
            command,
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
        payload["exit_code"] = completed.returncode
        payload["stdout"] = completed.stdout
        payload["stderr"] = completed.stderr
        try:
            delegate_result = json.loads(completed.stdout)
        except json.JSONDecodeError:
            delegate_result = {}
        if isinstance(delegate_result, dict):
            payload["delegate_status"] = delegate_result.get("status", "")
            payload["delegate_exit_code"] = delegate_result.get("exit_code")
            payload["first_write_path"] = delegate_result.get("first_write_path", "")
            payload["session_files"] = delegate_result.get("session_files", [])
            if delegate_result.get("status") == "failed":
                payload["exit_code"] = int(delegate_result.get("exit_code") or 1)
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(json.dumps(payload, sort_keys=True))
    return int(payload.get("exit_code", 0))


if __name__ == "__main__":
    raise SystemExit(main())
