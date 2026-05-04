#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from dataclasses import asdict, dataclass, replace
from datetime import datetime, timezone
from pathlib import Path
from string import Template
from typing import Sequence


CHECKOUT_MODES = ("shared", "worktree")
RUN_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
DEFAULT_FRONTEND_SKILLS = (
    "frontend-craft",
    "functional-ui",
    "visual-design",
    "landing-page",
    "frontend-design",
)


@dataclass(frozen=True)
class AdapterSpec:
    name: str
    executable: str
    install_hint: str
    command_mode: str
    supports_json: bool
    supports_skills: bool
    env_requirements: tuple[str, ...]


@dataclass(frozen=True)
class DelegateProfile:
    name: str
    adapter: str
    model: str
    thinking: str
    skill_names: tuple[str, ...]
    template_dir: Path
    allowed_tools: tuple[str, ...]
    default_checkout: str


@dataclass(frozen=True)
class DelegateRun:
    run_id: str
    ticket_id: str
    profile: DelegateProfile
    checkout_mode: str
    checkout_path: Path
    runtime_dir: Path
    durable_artifact_dir: Path | None
    prompt_path: Path
    handoff_path: Path
    dry_run: bool
    prompt: str
    ticket_context: str


@dataclass(frozen=True)
class DelegateRunResult:
    run_id: str
    command: list[str]
    exit_code: int
    checkout_mode: str
    checkout_path: str
    stdout_log: str
    stderr_log: str
    prompt_path: str
    handoff_path: str
    runtime_dir: str
    durable_artifact_dir: str | None
    status: str


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def now_run_id(profile: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{stamp}-{profile}"


def validate_run_id(run_id: str) -> str:
    if not RUN_ID_PATTERN.fullmatch(run_id):
        raise SystemExit(
            "invalid run id: use only letters, numbers, dot, underscore, and dash; "
            "path separators are not allowed"
        )
    return run_id


def normalize_ticket_id(raw: str) -> str:
    value = raw.strip()
    if not value:
        return ""
    if value.endswith("ticket.md"):
        return Path(value).parent.name.upper()
    if "/" in value:
        return Path(value).name.upper()
    return value.upper()


def ticket_path(ticket: str, root: Path) -> Path | None:
    if not ticket:
        return None
    candidate = Path(ticket)
    if candidate.exists():
        return candidate.resolve()
    ticket_id = normalize_ticket_id(ticket)
    path = root / "tickets" / ticket_id / "ticket.md"
    return path if path.exists() else None


def read_text(path: Path | None, fallback: str = "No ticket supplied.") -> str:
    if path is None:
        return fallback
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return fallback


def render_template(path: Path, values: dict[str, str]) -> str:
    content = path.read_text(encoding="utf-8")
    for key, value in values.items():
        content = content.replace("{{" + key + "}}", value)
    return Template(content).safe_substitute(values)


def adapter_specs() -> dict[str, AdapterSpec]:
    return {
        "pi": AdapterSpec(
            name="pi",
            executable="pi",
            install_hint="npm install -g @mariozechner/pi-coding-agent",
            command_mode="print",
            supports_json=True,
            supports_skills=True,
            env_requirements=("OPENROUTER_API_KEY",),
        )
    }


def missing_live_env(profile: DelegateProfile, env: dict[str, str] | None = None) -> list[str]:
    adapter = adapter_specs()[profile.adapter]
    source = os.environ if env is None else env
    return [name for name in adapter.env_requirements if not source.get(name)]


def load_profile(profile: str, root: Path | None = None) -> DelegateProfile:
    resolved_root = root or project_root()
    if profile != "frontend-pi-kimi":
        raise SystemExit(f"unknown delegate profile: {profile}")
    return DelegateProfile(
        name="frontend-pi-kimi",
        adapter="pi",
        model="openrouter/moonshotai/kimi-k2.6",
        thinking="high",
        skill_names=DEFAULT_FRONTEND_SKILLS,
        template_dir=resolved_root / "templates" / "external-cli" / "profiles" / profile,
        allowed_tools=("read", "bash", "edit", "write", "grep", "find", "ls"),
        default_checkout="worktree",
    )


def profile_root(profile: str, root: Path | None = None) -> Path:
    return (root or project_root()) / ".harness" / "external-cli" / "profiles" / profile


def runs_root(root: Path | None = None) -> Path:
    return (root or project_root()) / ".harness" / "external-cli" / "runs"


def skill_source_path(name: str, root: Path | None = None) -> Path:
    return (root or project_root()) / "skills" / name


def copied_skill_path(profile: DelegateProfile, skill_name: str, root: Path | None = None) -> Path:
    return profile_root(profile.name, root) / "skills" / skill_name


def copy_skill_bundle(profile: DelegateProfile, root: Path | None = None) -> list[str]:
    resolved_root = root or project_root()
    copied: list[str] = []
    destination_root = profile_root(profile.name, resolved_root) / "skills"
    destination_root.mkdir(parents=True, exist_ok=True)
    for skill_name in profile.skill_names:
        source = skill_source_path(skill_name, resolved_root)
        destination = destination_root / skill_name
        if not source.exists():
            raise SystemExit(f"missing skill source for profile {profile.name}: {source}")
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(
            source,
            destination,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
        )
        copied.append(str(destination))
    return copied


def settings_skill_paths(profile: DelegateProfile, root: Path | None = None) -> str:
    paths = [copied_skill_path(profile, name, root) for name in profile.skill_names]
    return ",\n".join(f"    {json.dumps(str(path))}" for path in paths)


def write_profile_settings(profile: DelegateProfile, root: Path | None = None) -> Path:
    resolved_root = root or project_root()
    target = profile_root(profile.name, resolved_root) / "settings.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    rendered = render_template(
        profile.template_dir / "settings.json.tpl",
        {"settings_skill_paths": settings_skill_paths(profile, resolved_root)},
    )
    target.write_text(rendered, encoding="utf-8")
    return target


def doctor_profile(profile: DelegateProfile, root: Path | None = None) -> dict[str, object]:
    resolved_root = root or project_root()
    adapter = adapter_specs()[profile.adapter]
    executable_path = shutil.which(adapter.executable)
    template_checks = {
        name: (profile.template_dir / name).exists()
        for name in ("APPEND_SYSTEM.md", "prompt.md.tpl", "handoff.md.tpl", "settings.json.tpl")
    }
    skill_checks = {
        name: skill_source_path(name, resolved_root).exists() for name in profile.skill_names
    }
    env_checks = {
        name: bool(os.environ.get(name)) for name in adapter.env_requirements
    }
    env_ready = all(env_checks.values())
    ok = bool(executable_path) and all(template_checks.values()) and all(skill_checks.values())
    return {
        "profile": profile.name,
        "adapter": asdict(adapter),
        "ok": ok,
        "executable": executable_path,
        "install_hint": adapter.install_hint if not executable_path else "",
        "templates": template_checks,
        "skills": skill_checks,
        "env": env_checks,
        "env_required_for_live_run": list(adapter.env_requirements),
        "live_ready": ok and env_ready,
    }


def build_run(
    *,
    profile: DelegateProfile,
    ticket: str,
    checkout_mode: str,
    prompt: str,
    run_id: str,
    dry_run: bool,
    artifact_dir: str,
    root: Path | None = None,
) -> DelegateRun:
    resolved_root = root or project_root()
    validated_run_id = validate_run_id(run_id)
    if checkout_mode not in CHECKOUT_MODES:
        raise SystemExit(f"invalid checkout mode: {checkout_mode}")
    resolved_ticket_path = ticket_path(ticket, resolved_root)
    if ticket and resolved_ticket_path is None:
        raise SystemExit(f"ticket not found: {ticket}")
    ticket_id = normalize_ticket_id(str(resolved_ticket_path)) if resolved_ticket_path else ""
    runtime_dir = Path(artifact_dir).expanduser() if artifact_dir else runs_root(resolved_root) / validated_run_id
    if not runtime_dir.is_absolute():
        runtime_dir = resolved_root / runtime_dir
    runtime_dir.mkdir(parents=True, exist_ok=True)
    durable_dir = None
    if ticket_id:
        durable_dir = resolved_root / "tickets" / ticket_id / "artifacts" / "external-cli" / validated_run_id
        durable_dir.mkdir(parents=True, exist_ok=True)
    handoff_path = runtime_dir / "handoff.md"
    checkout_path = prepare_checkout_path(
        checkout_mode=checkout_mode,
        runtime_dir=runtime_dir,
        root=resolved_root,
        dry_run=dry_run,
    )
    return DelegateRun(
        run_id=validated_run_id,
        ticket_id=ticket_id,
        profile=profile,
        checkout_mode=checkout_mode,
        checkout_path=checkout_path,
        runtime_dir=runtime_dir,
        durable_artifact_dir=durable_dir,
        prompt_path=runtime_dir / "prompt.md",
        handoff_path=handoff_path,
        dry_run=dry_run,
        prompt=prompt,
        ticket_context=read_text(resolved_ticket_path),
    )


def prepare_checkout_path(*, checkout_mode: str, runtime_dir: Path, root: Path, dry_run: bool) -> Path:
    if checkout_mode == "shared":
        return root

    checkout_path = runtime_dir / "checkout"
    if dry_run:
        return checkout_path

    if checkout_path.exists():
        return checkout_path

    completed = subprocess.run(
        ["git", "worktree", "add", "--detach", str(checkout_path), "HEAD"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise SystemExit(f"failed to create delegate worktree at {checkout_path}: {detail}")
    return checkout_path


def render_prompt(profile: DelegateProfile, run: DelegateRun, root: Path | None = None) -> Path:
    skill_lines = "\n".join(
        f"- {name}: {copied_skill_path(profile, name, root)}" for name in profile.skill_names
    )
    values = {
        "append_system": read_text(profile.template_dir / "APPEND_SYSTEM.md", ""),
        "profile_name": profile.name,
        "adapter": profile.adapter,
        "model": profile.model,
        "run_id": run.run_id,
        "ticket_ref": run.ticket_id or "none",
        "prompt": run.prompt,
        "ticket_context": run.ticket_context,
        "skill_list": skill_lines,
        "handoff_path": str(run.handoff_path),
    }
    rendered = render_template(profile.template_dir / "prompt.md.tpl", values)
    run.prompt_path.write_text(rendered, encoding="utf-8")
    handoff = render_template(profile.template_dir / "handoff.md.tpl", values)
    run.handoff_path.write_text(handoff, encoding="utf-8")
    return run.prompt_path


def build_pi_command(profile: DelegateProfile, run: DelegateRun, root: Path | None = None) -> list[str]:
    command = [
        "pi",
        "--model",
        profile.model,
        "--thinking",
        profile.thinking,
    ]
    for skill_name in profile.skill_names:
        command.extend(["--skill", str(copied_skill_path(profile, skill_name, root))])
    command.extend(["-p", f"@{run.prompt_path}"])
    return command


def copy_durable_artifacts(run: DelegateRun, command: Sequence[str]) -> None:
    if run.durable_artifact_dir is None:
        return
    for name in ("prompt.md", "handoff.md", "stdout.log", "stderr.log", "exit_code.txt", "command.json"):
        source = run.runtime_dir / name
        if source.exists():
            shutil.copy2(source, run.durable_artifact_dir / name)
    (run.durable_artifact_dir / "command.json").write_text(
        json.dumps({"command": list(command)}, indent=2) + "\n",
        encoding="utf-8",
    )


def collect_run_artifacts(
    run: DelegateRun,
    command: Sequence[str],
    completed: subprocess.CompletedProcess[str] | None,
) -> DelegateRunResult:
    stdout = "" if completed is None else completed.stdout
    stderr = "" if completed is None else completed.stderr
    exit_code = 0 if completed is None else completed.returncode
    if completed is None:
        stdout = "dry-run: command was rendered but not executed\n"
    (run.runtime_dir / "stdout.log").write_text(stdout, encoding="utf-8")
    (run.runtime_dir / "stderr.log").write_text(stderr, encoding="utf-8")
    (run.runtime_dir / "exit_code.txt").write_text(f"{exit_code}\n", encoding="utf-8")
    (run.runtime_dir / "command.json").write_text(
        json.dumps({"command": list(command)}, indent=2) + "\n",
        encoding="utf-8",
    )
    copy_durable_artifacts(run, command)
    return DelegateRunResult(
        run_id=run.run_id,
        command=list(command),
        exit_code=exit_code,
        checkout_mode=run.checkout_mode,
        checkout_path=str(run.checkout_path),
        stdout_log=str(run.runtime_dir / "stdout.log"),
        stderr_log=str(run.runtime_dir / "stderr.log"),
        prompt_path=str(run.prompt_path),
        handoff_path=str(run.handoff_path),
        runtime_dir=str(run.runtime_dir),
        durable_artifact_dir=str(run.durable_artifact_dir) if run.durable_artifact_dir else None,
        status="dry_run" if run.dry_run else ("success" if exit_code == 0 else "failed"),
    )


def emit(payload: dict[str, object], as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(payload.get("summary") or json.dumps(payload, sort_keys=True))


def command_doctor(args: argparse.Namespace) -> dict[str, object]:
    profile = load_profile(args.profile)
    result = doctor_profile(profile)
    if result["live_ready"]:
        summary = f"doctor {profile.name}: live ready"
    elif result["ok"]:
        summary = f"doctor {profile.name}: dry-run ready; live environment missing"
    else:
        summary = f"doctor {profile.name}: attention required"
    result["summary"] = summary
    return result


def command_setup(args: argparse.Namespace) -> dict[str, object]:
    profile = load_profile(args.profile)
    copied = copy_skill_bundle(profile)
    settings = write_profile_settings(profile)
    doctor = doctor_profile(profile)
    return {
        "summary": f"setup {profile.name}: copied {len(copied)} skills",
        "profile": profile.name,
        "copied_skills": copied,
        "settings": str(settings),
        "doctor": doctor,
    }


def command_run(args: argparse.Namespace) -> dict[str, object]:
    profile = load_profile(args.profile)
    if args.model:
        profile = replace(profile, model=args.model)
    if args.thinking:
        profile = replace(profile, thinking=args.thinking)
    copy_skill_bundle(profile)
    write_profile_settings(profile)
    run = build_run(
        profile=profile,
        ticket=args.ticket,
        checkout_mode=args.checkout,
        prompt=args.prompt,
        run_id=args.run_id or now_run_id(profile.name),
        dry_run=args.dry_run,
        artifact_dir=args.artifact_dir,
    )
    render_prompt(profile, run)
    command = build_pi_command(profile, run)
    completed = None
    if not args.dry_run:
        missing_env = missing_live_env(profile)
        if missing_env:
            raise SystemExit(
                "missing environment for live run: "
                + ", ".join(missing_env)
                + "; use --dry-run until credentials/spend are approved"
            )
        env = os.environ.copy()
        env.setdefault("PI_TELEMETRY", "0")
        completed = subprocess.run(
            command,
            cwd=run.checkout_path,
            text=True,
            capture_output=True,
            check=False,
            env=env,
        )
    result = collect_run_artifacts(run, command, completed)
    payload = asdict(result)
    payload["summary"] = f"run {profile.name}: {result.status}"
    return payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Delegate work to configured external CLI profiles.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ("doctor", "setup"):
        sub = subparsers.add_parser(name)
        sub.add_argument("--profile", default="frontend-pi-kimi")
        sub.add_argument("--json", action="store_true")

    run = subparsers.add_parser("run")
    run.add_argument("--profile", default="frontend-pi-kimi")
    run.add_argument("--ticket", default="")
    run.add_argument("--checkout", choices=CHECKOUT_MODES, default="shared")
    run.add_argument("--model", default="")
    run.add_argument("--thinking", default="")
    run.add_argument("--prompt", default="Implement the delegated task and write the requested handoff.")
    run.add_argument("--run-id", default="")
    run.add_argument("--artifact-dir", default="")
    run.add_argument("--dry-run", action="store_true")
    run.add_argument("--json", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "doctor":
        payload = command_doctor(args)
    elif args.command == "setup":
        payload = command_setup(args)
    elif args.command == "run":
        payload = command_run(args)
    else:
        parser.error(f"unknown command: {args.command}")
    emit(payload, args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
