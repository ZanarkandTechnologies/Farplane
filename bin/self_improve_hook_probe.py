#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
BIN = ROOT / "bin"
if str(BIN) not in sys.path:
    sys.path.insert(0, str(BIN))

import stop_hook  # noqa: E402
from user_turn import (  # noqa: E402
    append_conversation_assistant_response,
    append_conversation_user_turn,
    conversation_window_path,
    load_conversation_window,
    normalize_user_turn,
    should_review_skill_opportunities,
    skill_opportunity_application_dir,
)


def emit(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def project_root_arg(raw: str) -> Path:
    return Path(raw).expanduser().resolve()


def set_dry_run_env(enabled: bool) -> None:
    if enabled:
        os.environ["CODEXTER_SKILL_OPPORTUNITY_APPLY_DRY_RUN"] = "1"
    else:
        os.environ.pop("CODEXTER_SKILL_OPPORTUNITY_APPLY_DRY_RUN", None)


def set_interval_env(interval: int) -> None:
    os.environ["CODEXTER_SKILL_OPPORTUNITY_APPLY_INTERVAL"] = str(max(interval, 1))


def expand_probe_template(template: str, index: int) -> str:
    return template.replace("{index}", str(index))


def recent_application_runs(project_root: Path, limit: int) -> list[dict[str, str]]:
    root = skill_opportunity_application_dir(project_root)
    if not root.exists():
        return []
    runs = sorted((path for path in root.iterdir() if path.is_dir()), key=lambda path: path.stat().st_mtime, reverse=True)
    result: list[dict[str, str]] = []
    for run_dir in runs[: max(limit, 1)]:
        result.append(
            {
                "run_path": str(run_dir.relative_to(project_root)),
                "input_path": str((run_dir / "input.json").relative_to(project_root)),
                "report_path": str((run_dir / "report.json").relative_to(project_root)),
                "stdout_path": str((run_dir / "stdout.log").relative_to(project_root)),
                "stderr_path": str((run_dir / "stderr.log").relative_to(project_root)),
            }
        )
    return result


def force_review(args: argparse.Namespace) -> int:
    project_root = project_root_arg(args.project_root)
    set_dry_run_env(args.dry_run)
    set_interval_env(args.interval)
    window = load_conversation_window(project_root, args.session_id)
    if args.force_due:
        window["last_review_turn_count"] = 0
        window["turn_count"] = max(int(window.get("turn_count") or 0), args.interval)
    trigger = should_review_skill_opportunities(window, cadence=args.interval)
    result = stop_hook.maybe_launch_skill_opportunity_review(
        base=ROOT,
        project_root=project_root,
        session_id=args.session_id,
        window=window,
        payload={"hook_event_name": "Stop", "cwd": str(project_root), "probe": "force-review"},
    )
    emit(
        {
            "command": "force-review",
            "project_root": str(project_root),
            "session_id": args.session_id,
            "dry_run": args.dry_run,
            "trigger": trigger,
            "launch_result": result,
            "hooklet_result": result,
            "recent_application_runs": recent_application_runs(project_root, args.recent),
        }
    )
    return 0


def simulate(args: argparse.Namespace) -> int:
    project_root = project_root_arg(args.project_root)
    set_dry_run_env(args.dry_run)
    set_interval_env(args.interval)
    prompt_template = args.prompt or "please $impl-plan TASK-0174 self-learning probe turn {index}"
    response_template = args.response or "probe assistant response {index}"

    for index in range(1, args.turns + 1):
        captured = normalize_user_turn(
            expand_probe_template(prompt_template, index),
            turn_id=f"{args.session_id}-probe-user-{index}",
            source="self_improve_hook_probe",
        )
        append_conversation_user_turn(project_root, args.session_id, captured)
        append_conversation_assistant_response(
            project_root,
            args.session_id,
            expand_probe_template(response_template, index),
            source="self_improve_hook_probe",
        )

    window = load_conversation_window(project_root, args.session_id)
    trigger = should_review_skill_opportunities(window, cadence=args.interval)
    result = stop_hook.maybe_launch_skill_opportunity_review(
        base=ROOT,
        project_root=project_root,
        session_id=args.session_id,
        window=window,
        payload={"hook_event_name": "Stop", "cwd": str(project_root), "probe": "simulate"},
    )
    emit(
        {
            "command": "simulate",
            "project_root": str(project_root),
            "session_id": args.session_id,
            "dry_run": args.dry_run,
            "turns_requested": args.turns,
            "window_path": str(conversation_window_path(project_root, args.session_id).relative_to(project_root)),
            "window_turn_count": window.get("turn_count"),
            "rolling_exchange_count": len(window.get("rolling_exchanges", [])),
            "trigger": trigger,
            "launch_result": result,
            "hooklet_result": result,
            "recent_application_runs": recent_application_runs(project_root, args.recent),
        }
    )
    return 0


def status(args: argparse.Namespace) -> int:
    project_root = project_root_arg(args.project_root)
    window = load_conversation_window(project_root, args.session_id)
    emit(
        {
            "command": "status",
            "project_root": str(project_root),
            "session_id": args.session_id,
            "window_path": str(conversation_window_path(project_root, args.session_id).relative_to(project_root)),
            "turn_count": window.get("turn_count"),
            "last_review_turn_count": window.get("last_review_turn_count"),
            "rolling_exchange_count": len(window.get("rolling_exchanges", [])),
            "pending_user_turn_present": bool(window.get("pending_user_turn")),
            "trigger": should_review_skill_opportunities(window, cadence=args.interval),
            "recent_application_runs": recent_application_runs(project_root, args.recent),
        }
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Probe Codexter's hook-backed self-learning skill opportunity sidecar."
    )

    def add_common_flags(target: argparse.ArgumentParser, *, after_subcommand: bool = False) -> None:
        default = argparse.SUPPRESS if after_subcommand else None
        target.add_argument(
            "--project-root",
            default=default or str(ROOT),
            help="Project root containing .harness and tickets",
        )
        target.add_argument(
            "--session-id",
            default=default or "self-improve-probe",
            help="Synthetic or live Codex session id",
        )
        target.add_argument(
            "--interval",
            type=int,
            default=default or 10,
            help="Review cadence in captured user turns",
        )
        target.add_argument(
            "--recent",
            type=int,
            default=default or 3,
            help="Recent application runs to print",
        )

    add_common_flags(parser)

    subparsers = parser.add_subparsers(dest="command", required=True)

    simulate_parser = subparsers.add_parser("simulate", help="Seed a rolling window and run the launcher")
    add_common_flags(simulate_parser, after_subcommand=True)
    simulate_parser.add_argument("--turns", type=int, default=10, help="Synthetic user/assistant exchanges to seed")
    simulate_parser.set_defaults(dry_run=True)
    simulate_parser.add_argument("--dry-run", dest="dry_run", action="store_true", help="Write a dry-run report instead of spawning Codex")
    simulate_parser.add_argument("--live", dest="dry_run", action="store_false", help="Spawn the real Codex sidecar")
    simulate_parser.add_argument("--prompt", default="", help="Prompt template; may use {index}")
    simulate_parser.add_argument("--response", default="", help="Assistant response template; may use {index}")
    simulate_parser.set_defaults(func=simulate)

    force_parser = subparsers.add_parser("force-review", help="Run the launcher against an existing window")
    add_common_flags(force_parser, after_subcommand=True)
    force_parser.set_defaults(dry_run=True)
    force_parser.add_argument("--dry-run", dest="dry_run", action="store_true", help="Write a dry-run report instead of spawning Codex")
    force_parser.add_argument("--live", dest="dry_run", action="store_false", help="Spawn the real Codex sidecar")
    force_parser.add_argument("--force-due", action="store_true", help="Make the loaded window due before launching")
    force_parser.set_defaults(func=force_review)

    status_parser = subparsers.add_parser("status", help="Print current rolling window and recent sidecar runs")
    add_common_flags(status_parser, after_subcommand=True)
    status_parser.set_defaults(func=status)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
