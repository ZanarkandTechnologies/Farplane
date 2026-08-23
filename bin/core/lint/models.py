"""Typed, side-effect-free contracts for static lint selection."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Literal


LintScope = Literal["skills", "docs", "evals", "project", "tickets"]


@dataclass(frozen=True)
class LintContext:
    """One static lint invocation and its explicitly selected repository paths."""

    root: Path
    changed: bool = False
    base: str | None = None
    paths: tuple[str, ...] = ()


@dataclass(frozen=True)
class LintResult:
    """A deterministic result suitable for CLI and Git-gate receipts."""

    check_id: str
    ok: bool
    output: str = ""


CommandBuilder = Callable[[LintContext], tuple[str, ...]]
LintCallable = Callable[[LintContext], LintResult]


@dataclass(frozen=True)
class LintSpec:
    """One read-only repository contract and the paths that can affect it."""

    check_id: str
    scopes: frozenset[LintScope]
    path_globs: tuple[str, ...]
    command: CommandBuilder | None = None
    run: LintCallable | None = None
    always_on_changed: bool = False

    def __post_init__(self) -> None:
        if not self.check_id:
            raise ValueError("lint check_id must be non-empty")
        if not self.scopes:
            raise ValueError(f"{self.check_id}: lint scopes must be non-empty")
        if not self.path_globs:
            raise ValueError(f"{self.check_id}: lint path selectors must be non-empty")
        if (self.command is None) == (self.run is None):
            raise ValueError(f"{self.check_id}: specify exactly one command or runner")
