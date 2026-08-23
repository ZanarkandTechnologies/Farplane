#!/usr/bin/env python3
"""Lint Farplane's portable Agent-Skills eval manifests."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bin.core.eval_contract import (  # noqa: E402
    EvalContractError,
    lint_agent_skills_eval_suite,
    suite_json_schema,
)


def discover_eval_manifests(root: Path) -> list[Path]:
    """Return only canonical production skill suites; fixtures have unit coverage."""

    return sorted(path for path in (root / "skills").glob("*/evals/evals.json") if path.is_file())


def changed_paths(root: Path, *, base: str | None = None) -> set[Path]:
    commands = [
        ["git", "diff", "--name-only", "--cached"],
        ["git", "diff", "--name-only"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ]
    if base:
        commands.append(["git", "diff", "--name-only", f"{base}...HEAD"])
    changed: set[Path] = set()
    for command in commands:
        result = subprocess.run(command, cwd=root, text=True, capture_output=True, check=False)
        if result.returncode:
            raise EvalContractError(result.stderr.strip() or f"cannot read changed paths: {' '.join(command)}")
        changed.update(Path(line) for line in result.stdout.splitlines() if line.strip())
    return changed


def selected_eval_manifests(root: Path, *, changed: bool = False, base: str | None = None) -> list[Path]:
    manifests = discover_eval_manifests(root)
    if not changed:
        return manifests
    paths = changed_paths(root, base=base)
    if Path("bin/core/eval_contract.py") in paths or Path(__file__).relative_to(root) in paths:
        return manifests
    return [path for path in manifests if path.relative_to(root) in paths]


def lint_eval_manifests(root: Path, paths: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in paths:
        try:
            lint_agent_skills_eval_suite(path, root=root)
        except EvalContractError as exc:
            errors.append(f"{path.relative_to(root)}: {exc}")
    return errors


def check_generated_schema(root: Path) -> str | None:
    """Return a drift error when the checked-in tooling schema is stale."""

    schema_path = root / "docs" / "contracts" / "farplane-eval-suite-v1.schema.json"
    if not schema_path.is_file():
        return f"generated schema is missing: {schema_path.relative_to(root)}"
    try:
        checked_in = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return f"generated schema cannot be read: {exc}"
    if checked_in != suite_json_schema():
        return f"generated schema is stale: {schema_path.relative_to(root)}"
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Farplane repository root")
    parser.add_argument("--changed", action="store_true", help="lint only changed manifests")
    parser.add_argument("--base", help="also include paths changed from BASE...HEAD")
    parser.add_argument("--schema", action="store_true", help="print the generated JSON Schema and exit")
    parser.add_argument("--check-schema", action="store_true", help="fail when the checked-in JSON Schema has drifted")
    args = parser.parse_args()
    if args.schema:
        print(json.dumps(suite_json_schema(), indent=2, sort_keys=True))
        return 0
    root = args.root.resolve()
    if args.check_schema:
        schema_error = check_generated_schema(root)
        if schema_error:
            print(f"eval contract invalid: {schema_error}", file=sys.stderr)
            return 1
    try:
        manifests = selected_eval_manifests(root, changed=args.changed, base=args.base)
    except EvalContractError as exc:
        print(f"eval contract invalid: {exc}", file=sys.stderr)
        return 1
    errors = lint_eval_manifests(root, manifests)
    if errors:
        print("eval contract invalid:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    suffix = " changed" if args.changed else ""
    print(f"eval contract OK ({len(manifests)}{suffix} manifests checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
