#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fcntl
import json
import os
import re
import shutil
import stat as stat_module
import subprocess
import time
from contextlib import contextmanager
from dataclasses import asdict, dataclass, replace
from datetime import datetime, timezone
from pathlib import Path
from string import Template
from typing import Sequence


CHECKOUT_MODES = ("shared", "worktree")
RUN_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
PLACEHOLDER_HANDOFF_MARKERS = (
    "pending live external cli run",
    "- none reported yet",
    "status: pending",
    "observed output: pending",
)
HANDOFF_COMPLETION_SECTION_PATTERNS = {
    "changed_files": re.compile(
        r"^(?:Changed Files|Changed\s*/\s*Produced Files|Produced Files)$",
        re.I,
    ),
    "verification": re.compile(
        r"^(?:Verification(?:\s+Commands\s*&\s*Results)?|Self-Review Findings|Output Contract Compliance)$",
        re.I,
    ),
    "risks": re.compile(r"^(?:Risks(?:\s*/\s*Followups)?|Findings\s*/\s*Risks)$", re.I),
}
DEFAULT_FRONTEND_REQUIRED_SKILLS = (
    "frontend-craft",
    "functional-ui",
    "visual-design",
    "landing-page",
    "frontend-design",
    "image-generation",
    "video-generation",
    "video-ad-specs",
    "ai-marketing-videos",
    "explainer-video-guide",
    "storyboard-creation",
    "talking-head-production",
    "product-photography",
    "remotion",
    "remotion-render",
    "data-viz",
    "react-flow",
    "vercel-react-best-practices",
    "visual-qa",
    "review",
    "web-design-guidelines",
)
DEFAULT_FRONTEND_OPTIONAL_SKILLS: tuple[str, ...] = ()
DEFAULT_FRONTEND_SKILLS = DEFAULT_FRONTEND_REQUIRED_SKILLS


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
    optional_skill_names: tuple[str, ...]
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
    session_dir: Path
    durable_artifact_dir: Path | None
    prompt_path: Path
    handoff_path: Path
    dry_run: bool
    attachments: tuple[Path, ...]
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
    session_dir: str
    session_files: list[str]
    attachments: list[str]
    durable_artifact_dir: str | None
    status: str
    first_write_path: str | None


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


def read_prompt_arg(prompt: str, prompt_file: str, root: Path | None = None) -> str:
    if not prompt_file:
        return prompt
    resolved_root = root or project_root()
    path = Path(prompt_file).expanduser()
    if not path.is_absolute():
        path = resolved_root / path
    if not path.exists():
        raise SystemExit(f"prompt file not found: {prompt_file}")
    return path.read_text(encoding="utf-8")


def is_relative_to_path(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def resolve_expected_outputs(raw_paths: Sequence[str], checkout_path: Path) -> list[Path]:
    resolved_checkout = checkout_path.resolve(strict=False)
    outputs: list[Path] = []
    for raw_path in raw_paths:
        value = raw_path.strip()
        if not value:
            raise SystemExit("empty --expect-output path")
        path = Path(value).expanduser()
        if not path.is_absolute():
            path = resolved_checkout / path
        resolved = path.resolve(strict=False)
        if not is_relative_to_path(resolved, resolved_checkout):
            raise SystemExit(
                f"expected output must stay inside checkout {resolved_checkout}: {raw_path}"
            )
        outputs.append(resolved)
    return outputs


def ensure_expected_output_parents(expected_outputs: Sequence[Path]) -> None:
    for output in expected_outputs:
        output.parent.mkdir(parents=True, exist_ok=True)


def output_snapshot(paths: Sequence[Path]) -> dict[str, dict[str, object]]:
    snapshot: dict[str, dict[str, object]] = {}
    for path in paths:
        try:
            path_stat = path.lstat()
        except OSError:
            snapshot[str(path)] = {
                "exists": False,
                "mtime_ns": None,
                "size": None,
                "kind": "missing",
                "is_regular_file": False,
            }
            continue
        mode = path_stat.st_mode
        if stat_module.S_ISREG(mode):
            kind = "regular_file"
        elif stat_module.S_ISDIR(mode):
            kind = "directory"
        elif stat_module.S_ISLNK(mode):
            kind = "symlink"
        else:
            kind = "other"
        snapshot[str(path)] = {
            "exists": True,
            "mtime_ns": path_stat.st_mtime_ns,
            "size": path_stat.st_size,
            "kind": kind,
            "is_regular_file": kind == "regular_file",
        }
    return snapshot


def changed_expected_output(
    paths: Sequence[Path],
    before: dict[str, dict[str, object]],
) -> Path | None:
    for path in paths:
        current = output_snapshot([path]).get(str(path), {})
        if not current.get("exists") or not current.get("is_regular_file"):
            continue
        previous = before.get(str(path), {})
        if (
            not previous.get("exists")
            or previous.get("kind") != current.get("kind")
            or previous.get("mtime_ns") != current.get("mtime_ns")
            or previous.get("size") != current.get("size")
        ):
            return path
    return None


def markdown_sections(text: str) -> dict[str, str]:
    matched: dict[str, list[str]] = {}
    current_name = ""
    for line in text.splitlines():
        heading = re.match(r"^#+\s+(.+?)\s*$", line.strip())
        if heading:
            current_name = ""
            title = heading.group(1).strip()
            for name, pattern in HANDOFF_COMPLETION_SECTION_PATTERNS.items():
                if pattern.fullmatch(title):
                    current_name = name
                    matched.setdefault(name, [])
                    break
            continue
        if current_name:
            matched[current_name].append(line)
    return {name: "\n".join(lines).strip() for name, lines in matched.items()}


def handoff_body_mentions_expected_output(body: str, expected_outputs: Sequence[Path]) -> bool:
    if not expected_outputs:
        return True
    body_text = body.replace("\\", "/")
    for output in expected_outputs:
        output_text = str(output).replace("\\", "/")
        candidates = {output.name, output_text}
        try:
            candidates.add(output.as_posix())
        except ValueError:
            pass
        if any(candidate and candidate in body_text for candidate in candidates):
            return True
    return False


def handoff_has_completion_signal(
    path: Path,
    expected_outputs: Sequence[Path] = (),
) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    if not text.strip():
        return False
    lowered = text.lower()
    if any(marker in lowered for marker in PLACEHOLDER_HANDOFF_MARKERS):
        return False
    sections = markdown_sections(text)
    if not all(sections.get(name, "").strip() for name in HANDOFF_COMPLETION_SECTION_PATTERNS):
        return False
    return handoff_body_mentions_expected_output(
        sections.get("changed_files", ""),
        expected_outputs,
    )


def append_wrapper_first_write_evidence(
    *,
    handoff_path: Path,
    first_write_path: Path,
    first_write: dict[str, object],
) -> None:
    try:
        text = handoff_path.read_text(encoding="utf-8")
    except OSError:
        return
    if re.search(r"(?im)^##+\s+Wrapper First-Write Evidence\s*$", text):
        return
    lines = [
        "",
        "## Wrapper First-Write Evidence",
        "",
        f"- `first_write.json`: `{first_write_path}`",
        f"- status: `{first_write.get('status', 'missing')}`",
    ]
    observed_output = str(first_write.get("observed_output") or "").strip()
    if observed_output:
        lines.append(f"- observed output: `{observed_output}`")
    failure_reason = str(first_write.get("failure_reason") or "").strip()
    if failure_reason:
        lines.append(f"- failure reason: `{failure_reason}`")
    handoff_path.write_text(text.rstrip() + "\n" + "\n".join(lines) + "\n", encoding="utf-8")


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def timeout_completed_process(
    command: Sequence[str],
    exc: subprocess.TimeoutExpired,
    timeout_seconds: int | None,
) -> subprocess.CompletedProcess[str]:
    stdout = (
        exc.stdout.decode("utf-8", errors="replace")
        if isinstance(exc.stdout, bytes)
        else (exc.stdout or "")
    )
    stderr = (
        exc.stderr.decode("utf-8", errors="replace")
        if isinstance(exc.stderr, bytes)
        else (exc.stderr or "")
    )
    stderr = stderr + f"\nexternal CLI run timed out after {timeout_seconds} seconds\n"
    return subprocess.CompletedProcess(list(command), 124, stdout, stderr)


def run_command_capture(
    *,
    command: Sequence[str],
    cwd: Path,
    env: dict[str, str],
    timeout_seconds: int | None,
) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            list(command),
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
            env=env,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        return timeout_completed_process(command, exc, timeout_seconds)


def first_write_record(
    *,
    started_at: str,
    timeout_seconds: int,
    expected_outputs: Sequence[Path],
    before: dict[str, dict[str, object]],
) -> dict[str, object]:
    return {
        "status": "waiting",
        "started_at": started_at,
        "ended_at": "",
        "timeout_seconds": timeout_seconds,
        "expected_outputs": [str(path) for path in expected_outputs],
        "observed_output": "",
        "before": before,
    }


def finalize_first_write_record(
    *,
    first_write: dict[str, object],
    expected_outputs: Sequence[Path],
    before: dict[str, dict[str, object]],
    completed: subprocess.CompletedProcess[str],
) -> subprocess.CompletedProcess[str]:
    return_code = completed.returncode
    stderr = completed.stderr
    if first_write["status"] == "waiting":
        observed = changed_expected_output(expected_outputs, before)
        if observed is None:
            first_write["status"] = "failed"
            first_write["failure_reason"] = "process_exited_without_first_write"
            stderr += (
                "\nexternal CLI run exited without creating or modifying any "
                "expected regular output file\n"
            )
            if return_code == 0:
                return_code = 125
        else:
            first_write["status"] = "pass"
            first_write["observed_output"] = str(observed)
            first_write["observed_at"] = iso_now()
    first_write["ended_at"] = iso_now()
    first_write["after"] = output_snapshot(expected_outputs)
    return subprocess.CompletedProcess(list(completed.args), return_code, completed.stdout, stderr)


def run_with_expected_output_check(
    *,
    command: Sequence[str],
    cwd: Path,
    env: dict[str, str],
    timeout_seconds: int | None,
    expected_outputs: Sequence[Path],
) -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
    before = output_snapshot(expected_outputs)
    first_write = first_write_record(
        started_at=iso_now(),
        timeout_seconds=0,
        expected_outputs=expected_outputs,
        before=before,
    )
    completed = run_command_capture(
        command=command,
        cwd=cwd,
        env=env,
        timeout_seconds=timeout_seconds,
    )
    completed = finalize_first_write_record(
        first_write=first_write,
        expected_outputs=expected_outputs,
        before=before,
        completed=completed,
    )
    return completed, first_write


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


def dedupe_skill_names(names: Sequence[str], *, label: str) -> tuple[str, ...]:
    seen: set[str] = set()
    result: list[str] = []
    for raw_name in names:
        if not isinstance(raw_name, str):
            raise SystemExit(f"{label} contains a non-string skill name")
        name = raw_name.strip()
        if not name:
            raise SystemExit(f"{label} contains an empty skill name")
        if "/" in name or "\\" in name or name.startswith("."):
            raise SystemExit(f"{label} contains an invalid skill name: {name}")
        if name not in seen:
            seen.add(name)
            result.append(name)
    return tuple(result)


def load_skill_bundle(
    profile: str,
    root: Path | None = None,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    resolved_root = root or project_root()
    manifest_path = (
        resolved_root
        / "templates"
        / "external-cli"
        / "profiles"
        / profile
        / "skill-bundle.json"
    )
    if not manifest_path.exists():
        return DEFAULT_FRONTEND_REQUIRED_SKILLS, DEFAULT_FRONTEND_OPTIONAL_SKILLS
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid skill bundle manifest {manifest_path}: {exc}") from exc
    if not isinstance(manifest, dict):
        raise SystemExit(f"invalid skill bundle manifest {manifest_path}: expected object")
    required = dedupe_skill_names(
        manifest.get("required_skills", DEFAULT_FRONTEND_REQUIRED_SKILLS),
        label=f"{manifest_path} required_skills",
    )
    optional = dedupe_skill_names(
        manifest.get("optional_skills", ()),
        label=f"{manifest_path} optional_skills",
    )
    overlap = set(required).intersection(optional)
    if overlap:
        raise SystemExit(
            f"invalid skill bundle manifest {manifest_path}: duplicate required/optional skills: "
            + ", ".join(sorted(overlap))
        )
    return required, optional


def pi_auth_providers(home: Path | None = None) -> set[str]:
    auth_path = (home or Path.home()) / ".pi" / "agent" / "auth.json"
    try:
        auth = json.loads(auth_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    if not isinstance(auth, dict):
        return set()
    return {key for key, value in auth.items() if isinstance(key, str) and value}


def model_provider(profile: DelegateProfile) -> str:
    return profile.model.split("/", 1)[0] if "/" in profile.model else ""


def missing_live_env(
    profile: DelegateProfile,
    env: dict[str, str] | None = None,
    auth_providers: set[str] | None = None,
) -> list[str]:
    adapter = adapter_specs()[profile.adapter]
    source = os.environ if env is None else env
    providers = pi_auth_providers() if env is None and auth_providers is None else (auth_providers or set())
    provider = model_provider(profile)
    if adapter.name == "pi" and provider and provider in providers:
        return []
    return [name for name in adapter.env_requirements if not source.get(name)]


def load_profile(profile: str, root: Path | None = None) -> DelegateProfile:
    resolved_root = root or project_root()
    if profile != "frontend-pi-kimi":
        raise SystemExit(f"unknown delegate profile: {profile}")
    required_skills, optional_skills = load_skill_bundle(profile, resolved_root)
    return DelegateProfile(
        name="frontend-pi-kimi",
        adapter="pi",
        model="openrouter/moonshotai/kimi-k2.6",
        thinking="high",
        skill_names=required_skills,
        optional_skill_names=optional_skills,
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


@contextmanager
def profile_write_lock(profile: DelegateProfile, root: Path | None = None):
    target_root = profile_root(profile.name, root)
    target_root.mkdir(parents=True, exist_ok=True)
    lock_path = target_root / ".profile.lock"
    with lock_path.open("w", encoding="utf-8") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def available_skill_names(profile: DelegateProfile, root: Path | None = None) -> tuple[str, ...]:
    resolved_root = root or project_root()
    names = list(profile.skill_names)
    for skill_name in profile.optional_skill_names:
        if skill_source_path(skill_name, resolved_root).exists():
            names.append(skill_name)
    return tuple(names)


def copied_skill_path(profile: DelegateProfile, skill_name: str, root: Path | None = None) -> Path:
    return profile_root(profile.name, root) / "skills" / skill_name


def _copy_skill_bundle_unlocked(profile: DelegateProfile, root: Path | None = None) -> list[str]:
    resolved_root = root or project_root()
    copied: list[str] = []
    destination_root = profile_root(profile.name, resolved_root) / "skills"
    destination_root.mkdir(parents=True, exist_ok=True)
    for skill_name in available_skill_names(profile, resolved_root):
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


def copy_skill_bundle(profile: DelegateProfile, root: Path | None = None) -> list[str]:
    resolved_root = root or project_root()
    with profile_write_lock(profile, resolved_root):
        return _copy_skill_bundle_unlocked(profile, resolved_root)


def settings_skill_paths(profile: DelegateProfile, root: Path | None = None) -> str:
    paths = [copied_skill_path(profile, name, root) for name in available_skill_names(profile, root)]
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


def sync_profile_skills(
    profile: DelegateProfile,
    root: Path | None = None,
) -> tuple[list[str], Path, dict[str, object]]:
    resolved_root = root or project_root()
    with profile_write_lock(profile, resolved_root):
        copied = _copy_skill_bundle_unlocked(profile, resolved_root)
        settings = write_profile_settings(profile, resolved_root)
        doctor = doctor_profile(profile, resolved_root)
    return copied, settings, doctor


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
    optional_skill_checks = {
        name: skill_source_path(name, resolved_root).exists() for name in profile.optional_skill_names
    }
    env_checks = {
        name: bool(os.environ.get(name)) for name in adapter.env_requirements
    }
    auth_providers = pi_auth_providers()
    provider = model_provider(profile)
    provider_auth_ready = adapter.name == "pi" and provider in auth_providers
    env_ready = all(env_checks.values()) or provider_auth_ready
    ok = bool(executable_path) and all(template_checks.values()) and all(skill_checks.values())
    return {
        "profile": profile.name,
        "adapter": asdict(adapter),
        "ok": ok,
        "executable": executable_path,
        "install_hint": adapter.install_hint if not executable_path else "",
        "templates": template_checks,
        "skills": skill_checks,
        "optional_skills": optional_skill_checks,
        "skill_bundle": {
            "required": list(profile.skill_names),
            "optional": list(profile.optional_skill_names),
            "available": list(available_skill_names(profile, resolved_root)),
        },
        "env": env_checks,
        "env_required_for_live_run": list(adapter.env_requirements),
        "pi_auth": {
            "provider": provider,
            "provider_auth_ready": provider_auth_ready,
        },
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
    attachments: Sequence[str] = (),
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
    session_dir = runtime_dir / "sessions"
    session_dir.mkdir(parents=True, exist_ok=True)
    durable_dir = None
    if ticket_id:
        durable_dir = resolved_root / "tickets" / ticket_id / "artifacts" / "external-cli" / validated_run_id
        durable_dir.mkdir(parents=True, exist_ok=True)
    handoff_path = runtime_dir / "handoff.md"
    resolved_attachments: list[Path] = []
    for raw_attachment in attachments:
        attachment = Path(raw_attachment).expanduser()
        if not attachment.is_absolute():
            attachment = resolved_root / attachment
        if not attachment.exists():
            raise SystemExit(f"attachment not found: {raw_attachment}")
        resolved_attachments.append(attachment.resolve())
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
        session_dir=session_dir,
        durable_artifact_dir=durable_dir,
        prompt_path=runtime_dir / "prompt.md",
        handoff_path=handoff_path,
        dry_run=dry_run,
        attachments=tuple(resolved_attachments),
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
        f"- {name}: {copied_skill_path(profile, name, root)}"
        for name in available_skill_names(profile, root)
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
        "attachment_list": "\n".join(f"- {path}" for path in run.attachments) or "- none",
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
        "--session-dir",
        str(run.session_dir),
        "--model",
        profile.model,
        "--thinking",
        profile.thinking,
    ]
    for skill_name in available_skill_names(profile, root):
        command.extend(["--skill", str(copied_skill_path(profile, skill_name, root))])
    command.extend(["-p", f"@{run.prompt_path}"])
    for attachment in run.attachments:
        command.append(f"@{attachment}")
    return command


def terminate_process(process: subprocess.Popen[object]) -> None:
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def run_with_first_write_gate(
    *,
    command: Sequence[str],
    cwd: Path,
    env: dict[str, str],
    timeout_seconds: int | None,
    first_write_timeout_seconds: int,
    expected_outputs: Sequence[Path],
    runtime_dir: Path,
    handoff_path: Path | None = None,
    complete_when_output_and_handoff: bool = False,
    completion_grace_seconds: float = 0,
) -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
    started_at = iso_now()
    before = output_snapshot(expected_outputs)
    first_write = first_write_record(
        started_at=started_at,
        timeout_seconds=first_write_timeout_seconds,
        expected_outputs=expected_outputs,
        before=before,
    )
    stdout_live = runtime_dir / "stdout.live.log"
    stderr_live = runtime_dir / "stderr.live.log"
    global_deadline = time.monotonic() + timeout_seconds if timeout_seconds else None
    first_write_deadline = time.monotonic() + first_write_timeout_seconds
    forced_exit_code: int | None = None
    forced_stderr = ""
    completion_detected_at: float | None = None

    with stdout_live.open("w", encoding="utf-8") as stdout_file, stderr_live.open(
        "w", encoding="utf-8"
    ) as stderr_file:
        process = subprocess.Popen(
            list(command),
            cwd=cwd,
            stdout=stdout_file,
            stderr=stderr_file,
            text=True,
            env=env,
        )
        while True:
            observed = changed_expected_output(expected_outputs, before)
            if observed is not None and first_write["status"] == "waiting":
                first_write["status"] = "pass"
                first_write["observed_output"] = str(observed)
                first_write["observed_at"] = iso_now()

            if process.poll() is not None:
                break

            now = time.monotonic()
            if (
                complete_when_output_and_handoff
                and first_write["status"] == "pass"
                and handoff_path is not None
                and handoff_has_completion_signal(handoff_path, expected_outputs)
            ):
                if completion_detected_at is None:
                    completion_detected_at = now
                    first_write["completion_observed_at"] = iso_now()
                    first_write["completion_reason"] = "expected_output_and_handoff"
                if now - completion_detected_at >= completion_grace_seconds:
                    terminate_process(process)
                    forced_exit_code = 0
                    forced_stderr = (
                        "\nexternal CLI run stopped after expected output and "
                        "completed handoff were observed\n"
                    )
                    break
            if first_write["status"] == "waiting" and now >= first_write_deadline:
                terminate_process(process)
                forced_exit_code = 125
                forced_stderr = (
                    f"\nexternal CLI run failed first-write gate after "
                    f"{first_write_timeout_seconds} seconds; expected a regular file at one of: "
                    + ", ".join(str(path) for path in expected_outputs)
                    + "\n"
                )
                first_write["status"] = "failed"
                first_write["failure_reason"] = "first_write_timeout"
                break
            if global_deadline is not None and now >= global_deadline:
                terminate_process(process)
                forced_exit_code = 124
                forced_stderr = f"\nexternal CLI run timed out after {timeout_seconds} seconds\n"
                if first_write["status"] == "waiting":
                    first_write["status"] = "failed"
                    first_write["failure_reason"] = "run_timeout_before_first_write"
                break
            time.sleep(0.2)

        return_code = process.returncode if forced_exit_code is None else forced_exit_code

    stdout = stdout_live.read_text(encoding="utf-8", errors="replace") if stdout_live.exists() else ""
    stderr = stderr_live.read_text(encoding="utf-8", errors="replace") if stderr_live.exists() else ""
    completed = subprocess.CompletedProcess(list(command), return_code, stdout, stderr + forced_stderr)
    completed = finalize_first_write_record(
        first_write=first_write,
        expected_outputs=expected_outputs,
        before=before,
        completed=completed,
    )
    return completed, first_write


def copy_durable_artifacts(run: DelegateRun, command: Sequence[str]) -> None:
    if run.durable_artifact_dir is None:
        return
    for name in (
        "prompt.md",
        "handoff.md",
        "stdout.log",
        "stderr.log",
        "exit_code.txt",
        "command.json",
        "session_files.json",
        "attachments.json",
        "first_write.json",
    ):
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
    first_write: dict[str, object] | None = None,
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
    session_files = sorted(str(path) for path in run.session_dir.rglob("*.jsonl"))
    attachments = [str(path) for path in run.attachments]
    (run.runtime_dir / "session_files.json").write_text(
        json.dumps({"session_dir": str(run.session_dir), "session_files": session_files}, indent=2) + "\n",
        encoding="utf-8",
    )
    (run.runtime_dir / "attachments.json").write_text(
        json.dumps({"attachments": attachments}, indent=2) + "\n",
        encoding="utf-8",
    )
    first_write_path = None
    if first_write is not None:
        first_write_path = run.runtime_dir / "first_write.json"
        first_write_path.write_text(json.dumps(first_write, indent=2) + "\n", encoding="utf-8")
        append_wrapper_first_write_evidence(
            handoff_path=run.handoff_path,
            first_write_path=first_write_path,
            first_write=first_write,
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
        session_dir=str(run.session_dir),
        session_files=session_files,
        attachments=attachments,
        durable_artifact_dir=str(run.durable_artifact_dir) if run.durable_artifact_dir else None,
        status="dry_run" if run.dry_run else ("success" if exit_code == 0 else "failed"),
        first_write_path=str(first_write_path) if first_write_path else None,
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
    copied, settings, doctor = sync_profile_skills(profile)
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
    completed = None
    first_write = None
    with profile_write_lock(profile):
        _copy_skill_bundle_unlocked(profile)
        write_profile_settings(profile)
        run = build_run(
            profile=profile,
            ticket=args.ticket,
            checkout_mode=args.checkout,
            prompt=read_prompt_arg(args.prompt, args.prompt_file),
            run_id=args.run_id or now_run_id(profile.name),
            dry_run=args.dry_run,
            artifact_dir=args.artifact_dir,
            attachments=args.attach,
        )
        render_prompt(profile, run)
        command = build_pi_command(profile, run)
        expected_outputs = resolve_expected_outputs(args.expect_output, run.checkout_path)
        first_write_timeout = args.first_write_timeout_seconds
        if first_write_timeout < 0:
            raise SystemExit("--first-write-timeout-seconds must be 0 or greater")
        if args.completion_grace_seconds < 0:
            raise SystemExit("--completion-grace-seconds must be 0 or greater")
        if args.complete_when_output_and_handoff and not expected_outputs:
            raise SystemExit("--complete-when-output-and-handoff requires --expect-output")
        if args.complete_when_output_and_handoff and first_write_timeout == 0:
            raise SystemExit(
                "--complete-when-output-and-handoff requires a positive first-write timeout"
            )
        if run.dry_run and expected_outputs:
            first_write = {
                "status": "dry_run",
                "timeout_seconds": first_write_timeout,
                "expected_outputs": [str(path) for path in expected_outputs],
            }
        if not args.dry_run:
            ensure_expected_output_parents(expected_outputs)
            missing_env = missing_live_env(profile)
            if missing_env:
                raise SystemExit(
                    "missing environment for live run: "
                    + ", ".join(missing_env)
                    + "; use --dry-run until credentials/spend are approved"
                )
            env = os.environ.copy()
            env.setdefault("PI_TELEMETRY", "0")
            timeout = args.timeout_seconds if args.timeout_seconds > 0 else None
            if expected_outputs and first_write_timeout > 0:
                completed, first_write = run_with_first_write_gate(
                    command=command,
                    cwd=run.checkout_path,
                    env=env,
                    timeout_seconds=timeout,
                    first_write_timeout_seconds=first_write_timeout,
                    expected_outputs=expected_outputs,
                    runtime_dir=run.runtime_dir,
                    handoff_path=run.handoff_path,
                    complete_when_output_and_handoff=args.complete_when_output_and_handoff,
                    completion_grace_seconds=args.completion_grace_seconds,
                )
            elif expected_outputs:
                completed, first_write = run_with_expected_output_check(
                    command=command,
                    cwd=run.checkout_path,
                    env=env,
                    timeout_seconds=timeout,
                    expected_outputs=expected_outputs,
                )
            else:
                completed = run_command_capture(
                    command=command,
                    cwd=run.checkout_path,
                    env=env,
                    timeout_seconds=timeout,
                )
    result = collect_run_artifacts(run, command, completed, first_write)
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
    run.add_argument("--prompt-file", default="")
    run.add_argument("--run-id", default="")
    run.add_argument("--artifact-dir", default="")
    run.add_argument("--attach", action="append", default=[])
    run.add_argument(
        "--expect-output",
        action="append",
        default=[],
        help="Relative path, inside the checkout, that the external agent must create or modify early.",
    )
    run.add_argument(
        "--first-write-timeout-seconds",
        type=int,
        default=120,
        help=(
            "When --expect-output is supplied, fail the run if no expected regular "
            "output file changes within this many seconds. Use 0 to wait until "
            "process exit, then validate and record first_write.json."
        ),
    )
    run.add_argument(
        "--complete-when-output-and-handoff",
        action="store_true",
        help=(
            "With --expect-output and a positive first-write timeout, stop the "
            "external process successfully after an expected output changes and "
            "the managed handoff no longer looks like the placeholder."
        ),
    )
    run.add_argument(
        "--completion-grace-seconds",
        type=float,
        default=2.0,
        help="Seconds to wait after detecting expected output plus completed handoff before stopping the process.",
    )
    run.add_argument("--timeout-seconds", type=int, default=0)
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
