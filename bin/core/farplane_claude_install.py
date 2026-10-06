#!/usr/bin/env python3
"""Render Farplane's Claude Code plugin; install.sh --runtime claude is the entrypoint.

Claude Code reads the same SKILL.md packages and a compatible hook payload
schema, so this helper only translates the Codex-shaped single sources into a
local plugin marketplace at <claude>/farplane/:

- hooks.json          -> plugin/hooks/hooks.json
- agents/*.toml       -> plugin/agents/<name>.md (invoked as farplane:<name>)
- runtimes/claude     -> plugin/.claude-plugin/plugin.json with a content version
- templates/global    -> <claude>/farplane/AGENTS.md, imported from CLAUDE.md
- ~/.farplane/USER.md -> imported from CLAUDE.md, so every session sees the operator profile
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tomllib
from datetime import datetime
from pathlib import Path
from typing import Any

MANAGED_DIR = "farplane"
PLUGIN_NAME = "farplane"
PLUGIN_ID = f"{PLUGIN_NAME}@{PLUGIN_NAME}"
LEGACY_AGENT_PREFIX = "farplane-"
AGENT_MARKER = "<!-- Managed by Farplane install.sh --runtime claude; edit agents/*.toml instead. -->"
CLAUDE_MD_BEGIN = "<!-- BEGIN FARPLANE -->"
CLAUDE_MD_END = "<!-- END FARPLANE -->"
CODEX_HOOK_PREFIX = '"$HOME/.codex/hooks/'
READ_ONLY_TOOLS = "Write, Edit, NotebookEdit"


def managed_root(claude_home: Path) -> Path:
    return claude_home / MANAGED_DIR


def is_managed_hook(entry: dict[str, Any], claude_home: Path) -> bool:
    marker = str(managed_root(claude_home) / "hooks") + "/"
    return any(marker in str(hook.get("command", "")) for hook in entry.get("hooks", []))


def claude_hooks(hooks_json: Path, claude_home: Path) -> dict[str, Any]:
    """Translate Codex hook commands to the Claude-managed hook links."""
    source = json.loads(hooks_json.read_text(encoding="utf-8"))
    prefix = f'"{managed_root(claude_home) / "hooks"}/'
    rendered: dict[str, list[dict[str, Any]]] = {}
    for event, entries in source.get("hooks", {}).items():
        for entry in entries:
            hooks = []
            for hook in entry.get("hooks", []):
                command = str(hook.get("command", ""))
                if CODEX_HOOK_PREFIX not in command:
                    continue
                # Telemetry tags the hook host from FARPLANE_AGENT_RUNTIME; gates ignore it.
                hooks.append({**hook, "command": "FARPLANE_AGENT_RUNTIME=claude " + command.replace(CODEX_HOOK_PREFIX, prefix)})
            if hooks:
                rendered.setdefault(event, []).append({**entry, "hooks": hooks})
    return {"description": source.get("description", ""), "hooks": rendered}


def strip_managed_settings_hooks(settings: dict[str, Any], claude_home: Path) -> dict[str, Any]:
    """Retire hook entries earlier installs merged into settings.json; keep operator entries."""
    hooks = {}
    for event, entries in (settings.get("hooks") or {}).items():
        kept = [entry for entry in entries if not is_managed_hook(entry, claude_home)]
        if kept:
            hooks[event] = kept
    merged = {key: value for key, value in settings.items() if key != "hooks"}
    if hooks:
        merged["hooks"] = hooks
    return merged


def render_agent(toml_path: Path) -> tuple[str, str]:
    data = tomllib.loads(toml_path.read_text(encoding="utf-8"))
    lines = ["---", f"name: {data['name']}", f"description: {json.dumps(data['description'])}"]
    # Codex model ids do not exist in Claude Code; subagents inherit the session model.
    if data.get("sandbox_mode") == "read-only" or "Write and Edit tools are blocked" in data.get("developer_instructions", ""):
        lines.append(f"disallowedTools: {READ_ONLY_TOOLS}")
    lines += ["---", AGENT_MARKER, "", data["developer_instructions"].strip(), ""]
    return data["name"], "\n".join(lines)


def plugin_files(repo: Path, claude_home: Path) -> dict[str, str]:
    files = {"hooks/hooks.json": json.dumps(claude_hooks(repo / "hooks.json", claude_home), indent=2) + "\n"}
    for path in sorted((repo / "agents").glob("*.toml")):
        name, text = render_agent(path)
        files[f"agents/{name}.md"] = text
    digest = hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()
    manifest = json.loads((repo / "runtimes/claude/.claude-plugin/plugin.json").read_text(encoding="utf-8"))
    # Claude caches installed plugins by version; a content version makes updates land.
    major, minor, _patch = manifest["version"].split(".")
    manifest["version"] = f"{major}.{minor}.{int(digest[:8], 16)}"
    files[".claude-plugin/plugin.json"] = json.dumps(manifest, indent=2) + "\n"
    return files


def marketplace_json() -> str:
    return json.dumps({
        "name": PLUGIN_NAME,
        "description": "Local Farplane harness plugin rendered by install.sh --runtime claude.",
        "owner": {"name": "Zanarkand Technologies"},
        "plugins": [{"name": PLUGIN_NAME, "source": "./plugin", "description": "Farplane hooks and subagents"}],
    }, indent=2) + "\n"


def backup(path: Path, backup_root: Path, claude_home: Path) -> None:
    if not (path.exists() or path.is_symlink()):
        return
    dest = backup_root / path.relative_to(claude_home)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(path), dest)


def write_if_changed(path: Path, text: str, backup_root: Path, claude_home: Path) -> bool:
    if path.is_file() and not path.is_symlink() and path.read_text(encoding="utf-8") == text:
        return False
    backup(path, backup_root, claude_home)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


def write_plugin(repo: Path, claude_home: Path, backup_root: Path) -> list[str]:
    root = managed_root(claude_home)
    plugin_root = root / "plugin"
    files = plugin_files(repo, claude_home)
    changed = [rel for rel, text in files.items() if write_if_changed(plugin_root / rel, text, backup_root, claude_home)]
    for stale in sorted(plugin_root.rglob("*")):
        rel = stale.relative_to(plugin_root).as_posix()
        if stale.is_file() and rel not in files:
            backup(stale, backup_root, claude_home)
            changed.append(f"retired {rel}")
    if write_if_changed(root / ".claude-plugin/marketplace.json", marketplace_json(), backup_root, claude_home):
        changed.append("marketplace.json")
    return changed


def retire_legacy_agents(claude_home: Path, backup_root: Path) -> list[str]:
    retired = []
    for path in sorted((claude_home / "agents").glob(f"{LEGACY_AGENT_PREFIX}*.md")):
        if AGENT_MARKER in path.read_text(encoding="utf-8"):
            backup(path, backup_root, claude_home)
            retired.append(path.stem)
    return retired


def claude_md_block(claude_home: Path) -> str:
    contract = managed_root(claude_home) / "AGENTS.md"
    return f"{CLAUDE_MD_BEGIN}\n# Farplane global contract\n@{contract}\n\n# Operator profile\n@~/.farplane/USER.md\n{CLAUDE_MD_END}\n"


def merge_claude_md(text: str, block: str) -> str:
    if CLAUDE_MD_BEGIN in text and CLAUDE_MD_END in text:
        head, rest = text.split(CLAUDE_MD_BEGIN, 1)
        tail = rest.split(CLAUDE_MD_END, 1)[1].lstrip("\n")
        return head + block + ("\n" + tail if tail else "")
    return (text.rstrip() + "\n\n" if text.strip() else "") + block


def claude_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["claude", "plugin", *args], capture_output=True, text=True, timeout=120)


def register_plugin(claude_home: Path, changed: bool) -> str:
    """Add the local marketplace once, then install or refresh the cached plugin."""
    if shutil.which("claude") is None:
        return "skipped: claude CLI not on PATH"
    if PLUGIN_NAME not in claude_cli("marketplace", "list").stdout:
        result = claude_cli("marketplace", "add", str(managed_root(claude_home)))
        if result.returncode:
            return f"failed marketplace add: {result.stderr.strip() or result.stdout.strip()}"
    else:
        claude_cli("marketplace", "update", PLUGIN_NAME)
    if PLUGIN_ID not in claude_cli("list").stdout:
        result = claude_cli("install", PLUGIN_ID)
        return "installed" if result.returncode == 0 else f"failed install: {result.stderr.strip() or result.stdout.strip()}"
    if not changed:
        return "current"
    result = claude_cli("update", PLUGIN_ID)
    return "updated" if result.returncode == 0 else f"failed update: {result.stderr.strip() or result.stdout.strip()}"


def install(repo: Path, claude_home: Path, *, register: bool = True) -> dict[str, Any]:
    backup_root = claude_home / ".install-backups" / f"farplane-{datetime.now():%Y%m%d-%H%M%S}"
    report: dict[str, Any] = {}

    claude_md = claude_home / "CLAUDE.md"
    current = claude_md.read_text(encoding="utf-8") if claude_md.exists() else ""
    report["claude_md"] = write_if_changed(claude_md, merge_claude_md(current, claude_md_block(claude_home)), backup_root, claude_home)

    report["plugin"] = write_plugin(repo, claude_home, backup_root)
    report["retired_agents"] = retire_legacy_agents(claude_home, backup_root)

    settings_path = claude_home / "settings.json"
    if settings_path.exists():
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
        stripped = strip_managed_settings_hooks(settings, claude_home)
        report["settings_hooks_retired"] = stripped != settings and write_if_changed(
            settings_path, json.dumps(stripped, indent=2) + "\n", backup_root, claude_home
        )
    if register:
        report["registration"] = register_plugin(claude_home, bool(report["plugin"]))
    report["backup_root"] = str(backup_root) if backup_root.exists() else None
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--target", type=Path, default=Path.home() / ".claude")
    parser.add_argument("--no-register", action="store_true", help="Render files without calling the claude CLI.")
    args = parser.parse_args(argv)
    report = install(args.repo.resolve(), args.target.expanduser().resolve(), register=not args.no_register)
    print(json.dumps(report, indent=2))
    failed = str(report.get("registration", "")).startswith("failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
