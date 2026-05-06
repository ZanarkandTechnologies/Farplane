#!/usr/bin/env python3
"""Deterministic binary assertions for prompt-like skill evals."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class AssertionResult:
    name: str
    passed: bool
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def evaluate_case(case: dict[str, Any], output: dict[str, Any]) -> list[AssertionResult]:
    text = str(output.get("output", ""))
    files = set(_as_list(output.get("files")))
    results: list[AssertionResult] = []

    for expected in _as_list(case.get("must_contain")):
        results.append(
            AssertionResult(
                name=f"must_contain:{expected}",
                passed=expected in text,
                message="found required text" if expected in text else "missing required text",
            )
        )

    for forbidden in _as_list(case.get("must_not_contain")):
        results.append(
            AssertionResult(
                name=f"must_not_contain:{forbidden}",
                passed=forbidden not in text,
                message="forbidden text absent" if forbidden not in text else "forbidden text present",
            )
        )

    for path in _as_list(case.get("expected_files")):
        results.append(
            AssertionResult(
                name=f"expected_file:{path}",
                passed=path in files,
                message="expected file reported" if path in files else "expected file missing",
            )
        )

    if not results:
        results.append(
            AssertionResult(
                name="has_output",
                passed=bool(text.strip()),
                message="output exists" if text.strip() else "output is empty",
            )
        )

    return results
