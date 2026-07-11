"""Allowlisted validation check registry."""

from __future__ import annotations

from .models import CheckSpec


class CheckRegistry:
    def __init__(self) -> None:
        self._checks: dict[str, CheckSpec] = {}

    def register(self, spec: CheckSpec) -> None:
        if spec.check_id in self._checks:
            raise ValueError(f"duplicate validation check id: {spec.check_id}")
        self._checks[spec.check_id] = spec

    def resolve(self, check_id: str) -> CheckSpec:
        try:
            return self._checks[check_id]
        except KeyError as exc:
            raise ValueError(f"unknown validation check id: {check_id}") from exc

    def ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._checks))
