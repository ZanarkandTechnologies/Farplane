#!/usr/bin/env python3
"""Run a one-shot Codex exec behavior test and preserve the event stream."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


VERDICTS = {"pass", "fail", "blocked"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cwd", default=".", help="Working directory for the child Codex run.")
    parser.add_argument("--prompt-file", required=True, help="Prompt markdown/text file for the child agent.")
    parser.add_argument("--out", required=True, help="Directory where artifacts should be written.")
    parser.add_argument("--schema-file", help="Optional JSON schema for the child final response.")
    parser.add_argument("--model", help="Optional Codex model override.")
    parser.add_argument(
        "--persist-session",
        action="store_true",
        help="Do not pass --ephemeral, allowing the Codex session to be resumed.",
    )
    return parser.parse_args()


def read_events(path: Path) -> list[dict[str, object]]:
    events: list[dict[str, object]] = []
    if not path.exists():
        return events
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            events.append(parsed)
    return events


def parse_final_report(text: str) -> dict[str, object] | None:
    stripped = text.strip()
    if not stripped:
        return None
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if len(lines) >= 3 and lines[0].startswith("```") and lines[-1].startswith("```"):
            stripped = "\n".join(lines[1:-1]).strip()
    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, dict) else None


def score_verdict(returncode: int, last_message: str, final_report: dict[str, object] | None) -> str:
    if returncode != 0 or not last_message.strip():
        return "fail"
    if final_report is None:
        return "fail"
    verdict = final_report.get("verdict")
    if isinstance(verdict, str) and verdict in VERDICTS:
        return verdict
    return "fail"


def summarize(events: list[dict[str, object]], last_message_path: Path, returncode: int) -> dict[str, object]:
    thread_id = ""
    commands: list[dict[str, object]] = []
    messages: list[str] = []
    usage: dict[str, object] = {}
    for event in events:
        if event.get("type") == "thread.started":
            value = event.get("thread_id")
            if isinstance(value, str):
                thread_id = value
        if event.get("type") == "turn.completed":
            maybe_usage = event.get("usage")
            if isinstance(maybe_usage, dict):
                usage = maybe_usage
        item = event.get("item")
        if not isinstance(item, dict):
            continue
        if item.get("type") == "agent_message":
            text = item.get("text")
            if isinstance(text, str):
                messages.append(text)
        if item.get("type") == "command_execution" and event.get("type") == "item.completed":
            commands.append(
                {
                    "command": item.get("command"),
                    "exit_code": item.get("exit_code"),
                    "status": item.get("status"),
                }
            )
    last_message = last_message_path.read_text(encoding="utf-8") if last_message_path.exists() else ""
    final_report = parse_final_report(last_message)
    return {
        "schema_version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "returncode": returncode,
        "thread_id": thread_id,
        "event_count": len(events),
        "agent_message_count": len(messages),
        "command_count": len(commands),
        "commands": commands,
        "usage": usage,
        "final_report": final_report,
        "last_message_preview": last_message[:2000],
        "verdict": score_verdict(returncode, last_message, final_report),
    }


def main() -> int:
    args = parse_args()
    prompt_path = Path(args.prompt_file).resolve()
    out_dir = Path(args.out).resolve()
    cwd = Path(args.cwd).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if not prompt_path.exists():
        print(f"prompt file not found: {prompt_path}", file=sys.stderr)
        return 2
    if not cwd.exists():
        print(f"cwd not found: {cwd}", file=sys.stderr)
        return 2

    prompt_copy = out_dir / "prompt.md"
    prompt_copy.write_text(prompt_path.read_text(encoding="utf-8"), encoding="utf-8")
    events_path = out_dir / "events.jsonl"
    stderr_path = out_dir / "stderr.log"
    last_message_path = out_dir / "last-message.txt"
    score_path = out_dir / "score.json"

    cmd = ["codex", "-a", "never", "exec", "--json", "--output-last-message", str(last_message_path), "-C", str(cwd)]
    if not args.persist_session:
        cmd.insert(4, "--ephemeral")
    if args.model:
        cmd.extend(["--model", args.model])
    if args.schema_file:
        cmd.extend(["--output-schema", str(Path(args.schema_file).resolve())])
    cmd.append("-")

    with prompt_path.open("r", encoding="utf-8") as stdin_handle:
        with events_path.open("w", encoding="utf-8") as stdout_handle:
            with stderr_path.open("w", encoding="utf-8") as stderr_handle:
                proc = subprocess.run(
                    cmd,
                    stdin=stdin_handle,
                    stdout=stdout_handle,
                    stderr=stderr_handle,
                    cwd=str(cwd),
                    check=False,
                )

    score = summarize(read_events(events_path), last_message_path, proc.returncode)
    score["artifact_dir"] = str(out_dir)
    score_path.write_text(json.dumps(score, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(score, indent=2))
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
