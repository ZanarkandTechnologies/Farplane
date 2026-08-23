"""CLI adapter for the authoritative pure static-lint registry."""

from __future__ import annotations

import argparse

from farplane_cli_base import CORE_ROOT, CliError
from bin.core.lint import build_registry, lint, lint_ticket, render_payload
from bin.core.lint.models import LintContext, LintResult
from bin.core.lint.runner import payload
from bin.core.lint.source import DuplicateKeyError as _DuplicateKeyError
from bin.core.lint.source import LintSourceError, changed_paths, parse_source_file


def _print_failure(*, scope: str, changed: bool, output: str, as_json: bool) -> int:
    render_payload(
        payload(scope=scope, changed=changed, checks=[LintResult("lint_selection", False, output)]),
        as_json=as_json,
    )
    return 1


def run_lint(args: argparse.Namespace) -> int:
    """Run owner validators selected by a scope and optional changed-path boundary."""

    root = CORE_ROOT
    try:
        paths = changed_paths(root, base=args.base) if args.changed else ()
    except LintSourceError as exc:
        return _print_failure(scope=args.scope, changed=args.changed, output=str(exc), as_json=args.json)
    context = LintContext(root=root, changed=args.changed, base=args.base, paths=paths)
    try:
        checks = lint(build_registry(), context, args.scope)
    except (LintSourceError, ValueError) as exc:
        return _print_failure(scope=args.scope, changed=args.changed, output=str(exc), as_json=args.json)
    result = payload(scope=args.scope, changed=args.changed, checks=checks)
    render_payload(result, as_json=args.json)
    return 0 if result["ok"] else 1


def run_lint_ticket(args: argparse.Namespace) -> int:
    """Run static ticket checks only; phase-aware proof stays under validate ticket."""

    check = lint_ticket(CORE_ROOT, args.ticket)
    result = payload(scope="ticket", changed=False, checks=[check])
    render_payload(result, as_json=args.json)
    return 0 if result["ok"] else 1


def run_lint_cli(args: argparse.Namespace) -> int:
    """Dispatch the one public lint command without a validate-era alias."""

    if args.scope == "ticket":
        if args.ticket is None:
            raise CliError("lint ticket requires a ticket path", code=2)
        if args.changed or args.base:
            raise CliError("lint ticket is a direct static check and does not accept --changed or --base", code=2)
        return run_lint_ticket(args)
    if args.ticket is not None:
        raise CliError(f"lint {args.scope} does not accept a ticket path", code=2)
    return run_lint(args)
