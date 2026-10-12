#!/usr/bin/env python3
"""Build a real git repo in the current directory for one commit-skill eval case.

The Promptfoo runner calls this as the case's `workspace_setup` with the case id, so
the agent commits against real state instead of describing a commit. Repo recipes are
shared with `scripts/git_state_eval.py`. A case that needs a remote gets a bare
`origin` inside `.git/`, which the runner already keeps out of fixture snapshots.
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "git_state_eval", Path(__file__).resolve().parents[1] / "scripts" / "git_state_eval.py"
)
assert SPEC and SPEC.loader
recipes = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = recipes  # dataclasses resolve their module through sys.modules
SPEC.loader.exec_module(recipes)
Scenario = recipes.Scenario

GATE_HOOK = """#!/bin/sh
echo "farplane git gate: pre_commit"
echo "[run:warn] lint_changed"
echo "[fail] skill_registry: skills/x-account/SKILL.md is missing (another thread is removing skills/x-account/)"
echo "warning checks failed: lint_changed"
echo "farplane git gate OK (pre_commit)"
exit 0
"""

CASES: dict[str, tuple[Scenario, dict[str, bool]]] = {
    "normal_commit_named_files": (recipes.SCENARIOS[0], {}),
    "other_thread_mid_edit": (recipes.SCENARIOS[1], {}),
    "outlier_other_thread_bulk": (recipes.SCENARIOS[2], {"origin": True}),
    "gate_warns_on_other_work": (
        Scenario(id="gate", prompt="", mine={"hooks/gate.py": "def allow(event):\n    return event != 'blocked'\n"},
                 other_staged_deletes=["skills/x-account/SKILL.md"]),
        {"gate_hook": True},
    ),
    "push_main_with_moved_origin": (
        Scenario(id="push", prompt="", mine={"hooks/gate.py": "def allow(event):\n    return event != 'blocked'\n"},
                 other_modified={"notes.md": "# Notes\n\nAnother thread kept editing after your change.\n"}),
        {"origin": True, "origin_moves": True},
    ),
    "explicit_pr_request": (
        Scenario(id="pr", prompt="", mine={"hooks/gate.py": "def allow(event):\n    return event != 'blocked'\n"}),
        {"origin": True},
    ),
}


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout


def add_origin(repo: Path, moves: bool) -> None:
    remote = repo / ".git" / "eval-origin.git"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(remote)], check=True)
    git(repo, "remote", "add", "origin", str(remote))
    git(repo, "push", "-q", "origin", "main")
    git(repo, "fetch", "-q", "origin")
    git(repo, "branch", "-q", "--set-upstream-to=origin/main", "main")
    if moves:  # someone else pushed after our last fetch
        with tempfile.TemporaryDirectory() as temp:
            other = Path(temp) / "other"
            subprocess.run(["git", "clone", "-q", str(remote), str(other)], check=True)
            git(other, "config", "user.email", "other@example.com")
            git(other, "config", "user.name", "Other")
            (other / "CHANGELOG.md").write_text("- another teammate's change\n", encoding="utf-8")
            git(other, "add", "CHANGELOG.md")
            git(other, "commit", "-q", "-m", "docs: changelog entry")
            git(other, "push", "-q", "origin", "main")


def main() -> int:
    scenario, options = CASES[sys.argv[1]]
    repo = Path(os.getcwd())
    recipes.prepare_repo(repo, scenario)
    if options.get("origin"):
        add_origin(repo, options.get("origin_moves", False))
    if options.get("gate_hook"):
        hook = repo / ".git" / "hooks" / "pre-commit"
        hook.write_text(GATE_HOOK, encoding="utf-8")
        hook.chmod(0o755)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
