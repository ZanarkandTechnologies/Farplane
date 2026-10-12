#!/usr/bin/env python3
"""Run the commit skill against throwaway git repos and grade the resulting git state.

Each scenario builds a repo where this thread changed a few files and another thread
left unrelated work (modified, untracked, or already staged). Codex runs one natural
"commit it" request with the given skill staged under `.agents/skills/commit` and an
isolated CODEX_HOME, so no globally installed copy of the skill leaks in. The grade is
deterministic: the new commit must hold exactly this thread's paths, and the other
thread's work must still be uncommitted.

    python3 skills/commit/scripts/git_state_eval.py --skill-dir skills/commit --label candidate
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Scenario:
    id: str
    prompt: str
    mine: dict[str, str]                                  # path -> new content (this thread)
    other_modified: dict[str, str] = field(default_factory=dict)
    other_untracked: dict[str, str] = field(default_factory=dict)
    other_staged_deletes: list[str] = field(default_factory=list)


def bulk(prefix: str, count: int) -> dict[str, str]:
    return {f"{prefix}/item-{index:03d}/SKILL.md": f"# item {index}\n" for index in range(count)}


SCENARIOS = [
    Scenario(
        id="named_files",
        prompt="I fixed the parser bug in parser.py and added a regression case to test_parser.py. Commit the parser fix.",
        mine={"parser.py": "def parse(text):\n    return text.strip().split(',')\n",
              "test_parser.py": "from parser import parse\n\ndef test_trailing_space():\n    assert parse('a,b ') == ['a', 'b']\n"},
        other_modified={"notes.md": "# Notes\n\nDraft from another thread, still in progress.\n"},
    ),
    Scenario(
        id="staged_deletes_from_other_thread",
        prompt="I changed hooks/stop_gate.py so the stop gate skips nudges when blocked. Commit it.",
        mine={"hooks/stop_gate.py": "def gate(blocked):\n    return None if blocked else 'nudge'\n"},
        other_staged_deletes=["skills/x-account/SKILL.md", "skills/x-account/README.md"],
    ),
    Scenario(
        id="bulk_other_thread",
        prompt="I fixed the hook in hooks/gate.py and its test in tests/test_gate.py. Commit it.",
        mine={"hooks/gate.py": "def allow(event):\n    return event != 'blocked'\n",
              "tests/test_gate.py": "from hooks.gate import allow\n\ndef test_blocked():\n    assert not allow('blocked')\n"},
        other_modified={f"docs/page-{index:02d}.md": f"# Page {index}\n\nRewritten by another thread.\n" for index in range(40)},
        other_untracked=bulk("skills/merged", 160),
    ),
]

BASE_FILES = {
    "parser.py": "def parse(text):\n    return text.split(',')\n",
    "test_parser.py": "",
    "notes.md": "# Notes\n",
    "hooks/stop_gate.py": "def gate(blocked):\n    return 'nudge'\n",
    "hooks/gate.py": "def allow(event):\n    return True\n",
    "tests/test_gate.py": "",
    "skills/x-account/SKILL.md": "# x-account\n",
    "skills/x-account/README.md": "x-account\n",
    **{f"docs/page-{index:02d}.md": f"# Page {index}\n" for index in range(40)},
}


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout


def write(repo: Path, files: dict[str, str]) -> None:
    for relative, text in files.items():
        path = repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def build_repo(root: Path, scenario: Scenario, skill_dir: Path) -> tuple[Path, str]:
    repo = root / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "eval@example.com")
    git(repo, "config", "user.name", "Eval")
    write(repo, BASE_FILES)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "chore: base")
    base = git(repo, "rev-parse", "HEAD").strip()
    write(repo, scenario.mine)
    write(repo, scenario.other_modified)
    write(repo, scenario.other_untracked)
    if scenario.other_staged_deletes:
        git(repo, "rm", "-q", "--", *scenario.other_staged_deletes)
    shutil.copytree(skill_dir, repo / ".agents" / "skills" / "commit")
    with (repo / ".git" / "info" / "exclude").open("a", encoding="utf-8") as handle:
        handle.write(".agents/\n")
    return repo, base


def isolated_codex_home(root: Path, model: str) -> Path:
    home = root / "codex-home"
    home.mkdir()
    real = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")
    (home / "auth.json").symlink_to(real / "auth.json")  # credentials stay in place; nothing is copied
    (home / "config.toml").write_text(f'model = "{model}"\nmodel_reasoning_effort = "low"\n', encoding="utf-8")
    return home


def grade(repo: Path, base: str, scenario: Scenario, final: str) -> dict[str, object]:
    head = git(repo, "rev-parse", "HEAD").strip()
    commits = int(git(repo, "rev-list", "--count", f"{base}..HEAD").strip() or 0)
    committed = set(git(repo, "diff", "--name-only", base, head).split()) if commits else set()
    status = git(repo, "status", "--porcelain", "--untracked-files=all")
    pending = {line[3:] for line in status.splitlines()}
    others = set(scenario.other_modified) | set(scenario.other_untracked) | set(scenario.other_staged_deletes)
    checks = {
        "one_commit": commits == 1,
        "commit_holds_exactly_mine": committed == set(scenario.mine),
        "other_work_left_uncommitted": others <= pending and not (others & committed),
    }
    return {
        "scenario": scenario.id,
        "pass": all(checks.values()),
        "checks": checks,
        "commits": commits,
        "committed": sorted(committed),
        "other_paths_committed": len(others & committed),
        "final_mentions_other_work": any(word in final.lower() for word in ("other thread", "unstaged", "left", "untouched")),
    }


def run_scenario(scenario: Scenario, skill_dir: Path, model: str, keep: Path | None) -> dict[str, object]:
    root = Path(tempfile.mkdtemp(prefix=f"commit-eval-{scenario.id}-"))
    try:
        repo, base = build_repo(root, scenario, skill_dir)
        env = {**os.environ, "CODEX_HOME": str(isolated_codex_home(root, model))}
        final_file = root / "final.txt"
        completed = subprocess.run(
            ["codex", "exec", "--skip-git-repo-check", "--ephemeral", "-C", str(repo), "-s", "workspace-write",
             # workspace-write keeps .git read-only; the throwaway repo's .git must be writable to commit.
             "-c", f'sandbox_workspace_write.writable_roots=["{repo / ".git"}"]',
             "-o", str(final_file), scenario.prompt],
            env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=600, check=False,
        )
        final = final_file.read_text(encoding="utf-8") if final_file.exists() else ""
        result = grade(repo, base, scenario, final)
        result.update(
            returncode=completed.returncode,
            skill_read="skills/commit/SKILL.md" in completed.stdout + completed.stderr,
            final=final[:1200],
        )
        if keep:
            shutil.copytree(root, keep / scenario.id, symlinks=True, dirs_exist_ok=True)
        return result
    finally:
        shutil.rmtree(root, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--skill-dir", type=Path, required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--model", default="gpt-5.6-luna")
    parser.add_argument("--scenario", action="append", help="run only these scenario ids")
    parser.add_argument("--out", type=Path, help="write results JSON here and keep each scenario's workspace beside it")
    args = parser.parse_args()
    keep = args.out.parent / f"{args.out.stem}-workspaces" if args.out else None
    selected = [s for s in SCENARIOS if not args.scenario or s.id in args.scenario]
    results = [run_scenario(s, args.skill_dir.resolve(), args.model, keep) for s in selected]
    summary = {"label": args.label, "passed": sum(r["pass"] for r in results), "total": len(results), "results": results}
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    for r in results:
        line = {k: r[k] for k in ("scenario", "pass", "checks", "other_paths_committed", "skill_read", "returncode")}
        line["committed"] = r["committed"][:6] + ([f"... +{len(r['committed']) - 6} more"] if len(r["committed"]) > 6 else [])
        print(json.dumps(line))
    print(json.dumps({"label": args.label, "passed": summary["passed"], "total": summary["total"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
