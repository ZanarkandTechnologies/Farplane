#!/usr/bin/env python3
"""Validate Farplane project framework file conventions."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TEXT_SUFFIXES = {
    ".json",
    ".jsonl",
    ".md",
    ".py",
    ".sh",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
SKIP_PREFIXES = (
    ".git/",
    ".farplane/",
    "docs/archive/",
    "node_modules/",
    "tickets/archive/",
)
SECRET_VALUE_RE = re.compile(
    r"(?i)\b(api[_-]?key|access[_-]?token|secret|password)\b\s*[:=]\s*[\"']?[A-Za-z0-9_./+=-]{8,}"
)
RETIRED_INTEGRATIONS_REF = "farplane/" + "integrations.md"


def tracked_files(root: Path) -> list[Path]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=root,
            check=True,
            capture_output=True,
            text=False,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return sorted(
            path.relative_to(root)
            for path in root.rglob("*")
            if path.is_file() and ".git" not in path.parts
        )

    return [Path(raw.decode("utf-8")) for raw in result.stdout.split(b"\0") if raw]


def should_scan(path: Path) -> bool:
    path_string = path.as_posix()
    if any(path_string.startswith(prefix) for prefix in SKIP_PREFIXES):
        return False
    return path.suffix in TEXT_SUFFIXES


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    framework_dir = root / "farplane"
    automations = framework_dir / "automations.md"
    bindings = framework_dir / "bindings.md"
    retired_integrations = framework_dir / "integrations.md"

    if not framework_dir.exists():
        return errors

    if retired_integrations.exists():
        errors.append(f"{RETIRED_INTEGRATIONS_REF} is retired; use farplane/bindings.md.")

    if automations.exists() and not bindings.exists():
        errors.append("farplane/automations.md requires farplane/bindings.md.")

    if bindings.exists():
        text = bindings.read_text(encoding="utf-8")
        if "kind: project-bindings" not in text[:500]:
            errors.append("farplane/bindings.md must use front matter kind: project-bindings.")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if SECRET_VALUE_RE.search(line):
                errors.append(
                    f"farplane/bindings.md:{line_number} looks like it stores a secret value; "
                    "bindings are non-secret coordinates only."
                )

    for path in sorted(framework_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if "framework_template_version:" not in text[:700]:
            errors.append(
                f"{path.relative_to(root)} must declare framework_template_version in front matter."
            )

    for rel_path in tracked_files(root):
        if not should_scan(rel_path):
            continue
        full_path = root / rel_path
        try:
            text = full_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if RETIRED_INTEGRATIONS_REF in text:
            errors.append(
                f"{rel_path}: references retired {RETIRED_INTEGRATIONS_REF}; use farplane/bindings.md."
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()

    errors = validate(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Farplane project file conventions OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
