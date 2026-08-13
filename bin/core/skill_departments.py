"""Canonical department taxonomy shared by skill validation and graph projection."""

from __future__ import annotations

import tomllib
from pathlib import Path


class DepartmentTaxonomyError(ValueError):
    """Raised when the checked-in department taxonomy is malformed."""


class WorkflowRootConfigError(ValueError):
    """Raised when the Capability Map's curated workflow-root config is malformed."""


def load_skill_departments(repo_root: Path) -> dict[str, str]:
    path = repo_root / "rules" / "skill-departments.toml"
    try:
        payload = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise DepartmentTaxonomyError(f"unable to load {path}: {exc}") from exc

    departments = payload.get("departments")
    if not isinstance(departments, dict) or not departments:
        raise DepartmentTaxonomyError(f"{path}: [departments] must be a non-empty table")

    normalized: dict[str, str] = {}
    for department_id, label in departments.items():
        if not isinstance(department_id, str) or not isinstance(label, str):
            raise DepartmentTaxonomyError(f"{path}: departments must map string IDs to labels")
        clean_id = department_id.strip()
        clean_label = label.strip()
        if not clean_id or not clean_label:
            raise DepartmentTaxonomyError(f"{path}: department IDs and labels must be non-empty")
        normalized[clean_id] = clean_label
    return normalized


def load_skill_workflow_roots(
    repo_root: Path, departments: dict[str, str] | None = None
) -> dict[str, tuple[str, ...]]:
    """Load the complete department-keyed workflow-root selection for the map."""
    department_labels = departments or load_skill_departments(repo_root)
    path = repo_root / "rules" / "skill-workflows.toml"
    try:
        payload = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise WorkflowRootConfigError(f"unable to load {path}: {exc}") from exc

    raw_roots = payload.get("workflow_roots")
    if not isinstance(raw_roots, dict):
        raise WorkflowRootConfigError(f"{path}: [workflow_roots] must be a table")

    configured_departments = set(raw_roots)
    expected_departments = set(department_labels)
    unknown_departments = sorted(configured_departments.difference(expected_departments))
    missing_departments = sorted(expected_departments.difference(configured_departments))
    if unknown_departments or missing_departments:
        details: list[str] = []
        if unknown_departments:
            details.append(f"unknown departments: {', '.join(unknown_departments)}")
        if missing_departments:
            details.append(f"missing departments: {', '.join(missing_departments)}")
        raise WorkflowRootConfigError(f"{path}: " + "; ".join(details))

    normalized: dict[str, tuple[str, ...]] = {}
    all_roots: set[str] = set()
    for department_id in department_labels:
        values = raw_roots.get(department_id)
        if not isinstance(values, list) or not values:
            raise WorkflowRootConfigError(
                f"{path}: workflow_roots.{department_id} must be a non-empty list"
            )
        roots: list[str] = []
        seen_in_department: set[str] = set()
        for raw_root in values:
            if not isinstance(raw_root, str) or not raw_root.strip():
                raise WorkflowRootConfigError(
                    f"{path}: workflow_roots.{department_id} values must be non-empty strings"
                )
            root = raw_root.strip()
            if root in seen_in_department:
                raise WorkflowRootConfigError(
                    f"{path}: duplicate root {root!r} in {department_id}"
                )
            if root in all_roots:
                raise WorkflowRootConfigError(
                    f"{path}: root {root!r} cannot belong to multiple departments"
                )
            roots.append(root)
            seen_in_department.add(root)
            all_roots.add(root)
        normalized[department_id] = tuple(roots)
    return normalized


def load_skill_workflow_labels(
    repo_root: Path, workflow_roots: dict[str, tuple[str, ...]]
) -> dict[str, str]:
    """Load business-facing labels for the configured real workflow roots."""
    path = repo_root / "rules" / "skill-workflows.toml"
    try:
        payload = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise WorkflowRootConfigError(f"unable to load {path}: {exc}") from exc

    raw_labels = payload.get("workflow_labels")
    if not isinstance(raw_labels, dict):
        raise WorkflowRootConfigError(f"{path}: [workflow_labels] must be a table")
    expected_roots = {root for roots in workflow_roots.values() for root in roots}
    configured_roots = set(raw_labels)
    unknown_roots = sorted(configured_roots.difference(expected_roots))
    missing_roots = sorted(expected_roots.difference(configured_roots))
    if unknown_roots or missing_roots:
        details: list[str] = []
        if unknown_roots:
            details.append(f"labels for unconfigured roots: {', '.join(unknown_roots)}")
        if missing_roots:
            details.append(f"missing labels: {', '.join(missing_roots)}")
        raise WorkflowRootConfigError(f"{path}: " + "; ".join(details))

    normalized: dict[str, str] = {}
    for root in sorted(expected_roots):
        label = raw_labels[root]
        if not isinstance(label, str) or not label.strip():
            raise WorkflowRootConfigError(f"{path}: workflow label for {root!r} must be a string")
        normalized[root] = label.strip()
    return normalized
