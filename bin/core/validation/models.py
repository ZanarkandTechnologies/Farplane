"""Typed values for ticket validation."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable, Literal

ValidationPhase = Literal["planning", "complete"]
CheckMode = Literal["block", "warn"]


@dataclass(frozen=True)
class PathBoundary:
    source: str
    paths: tuple[str, ...] = ()
    base: str | None = None


@dataclass(frozen=True)
class ValidationContext:
    root: Path
    ticket: Path
    phase: ValidationPhase
    boundary: PathBoundary


@dataclass(frozen=True)
class CheckResult:
    check_id: str
    mode: CheckMode
    status: Literal["pass", "fail", "skip"]
    output: str = ""
    duration_ms: int = 0


CheckCallable = Callable[[ValidationContext, CheckMode], CheckResult]


@dataclass(frozen=True)
class CheckSpec:
    check_id: str
    run: CheckCallable
    mode: CheckMode = "block"


@dataclass
class ValidationReceipt:
    schema_version: int
    ticket: str
    phase: ValidationPhase
    path_source: str
    base: str | None
    changed_paths: list[str]
    selected_checks: list[str]
    results: list[CheckResult] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not any(result.status == "fail" and result.mode == "block" for result in self.results)

    def as_dict(self) -> dict[str, object]:
        payload = asdict(self)
        for result in payload["results"]:
            result.pop("duration_ms", None)
        payload["ok"] = self.ok
        return payload
