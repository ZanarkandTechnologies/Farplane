"""Canonical department taxonomy shared by skill validation and graph projection."""

from __future__ import annotations

import tomllib
from pathlib import Path


class DepartmentTaxonomyError(ValueError):
    """Raised when the checked-in department taxonomy is malformed."""


class CapabilityAdmissionConfigError(ValueError):
    """Raised when the Capability Map's classified admission config is malformed."""


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


def load_skill_capability_admission(
    repo_root: Path, departments: dict[str, str] | None = None
) -> dict[str, tuple[str, ...]]:
    """Load the complete department-keyed classified capability admission list."""
    department_labels = departments or load_skill_departments(repo_root)
    path = repo_root / "rules" / "skill-workflows.toml"
    try:
        payload = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise CapabilityAdmissionConfigError(f"unable to load {path}: {exc}") from exc

    raw_admission = payload.get("capability_admission")
    if not isinstance(raw_admission, dict):
        raise CapabilityAdmissionConfigError(f"{path}: [capability_admission] must be a table")

    configured_departments = set(raw_admission)
    expected_departments = set(department_labels)
    unknown_departments = sorted(configured_departments.difference(expected_departments))
    missing_departments = sorted(expected_departments.difference(configured_departments))
    if unknown_departments or missing_departments:
        details: list[str] = []
        if unknown_departments:
            details.append(f"unknown departments: {', '.join(unknown_departments)}")
        if missing_departments:
            details.append(f"missing departments: {', '.join(missing_departments)}")
        raise CapabilityAdmissionConfigError(f"{path}: " + "; ".join(details))

    normalized: dict[str, tuple[str, ...]] = {}
    all_capabilities: set[str] = set()
    for department_id in department_labels:
        values = raw_admission.get(department_id)
        if not isinstance(values, list):
            raise CapabilityAdmissionConfigError(
                f"{path}: capability_admission.{department_id} must be a list"
            )
        capabilities: list[str] = []
        seen_in_department: set[str] = set()
        for raw_capability in values:
            if not isinstance(raw_capability, str) or not raw_capability.strip():
                raise CapabilityAdmissionConfigError(
                    f"{path}: capability_admission.{department_id} values must be non-empty strings"
                )
            capability = raw_capability.strip()
            if capability in seen_in_department:
                raise CapabilityAdmissionConfigError(
                    f"{path}: duplicate capability {capability!r} in {department_id}"
                )
            if capability in all_capabilities:
                raise CapabilityAdmissionConfigError(
                    f"{path}: capability {capability!r} cannot belong to multiple departments"
                )
            capabilities.append(capability)
            seen_in_department.add(capability)
            all_capabilities.add(capability)
        normalized[department_id] = tuple(capabilities)
    return normalized


def load_skill_capability_labels(
    repo_root: Path, capability_admission: dict[str, tuple[str, ...]]
) -> dict[str, str]:
    """Load business-facing labels for classified capabilities admitted to the map."""
    path = repo_root / "rules" / "skill-workflows.toml"
    try:
        payload = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise CapabilityAdmissionConfigError(f"unable to load {path}: {exc}") from exc

    raw_labels = payload.get("capability_labels")
    if not isinstance(raw_labels, dict):
        raise CapabilityAdmissionConfigError(f"{path}: [capability_labels] must be a table")
    expected_capabilities = {
        capability
        for capabilities in capability_admission.values()
        for capability in capabilities
    }
    configured_roots = set(raw_labels)
    unknown_capabilities = sorted(configured_roots.difference(expected_capabilities))
    missing_capabilities = sorted(expected_capabilities.difference(configured_roots))
    if unknown_capabilities or missing_capabilities:
        details: list[str] = []
        if unknown_capabilities:
            details.append(
                f"labels for unadmitted capabilities: {', '.join(unknown_capabilities)}"
            )
        if missing_capabilities:
            details.append(f"missing labels: {', '.join(missing_capabilities)}")
        raise CapabilityAdmissionConfigError(f"{path}: " + "; ".join(details))

    normalized: dict[str, str] = {}
    for capability in sorted(expected_capabilities):
        label = raw_labels[capability]
        if not isinstance(label, str) or not label.strip():
            raise CapabilityAdmissionConfigError(
                f"{path}: capability label for {capability!r} must be a string"
            )
        normalized[capability] = label.strip()
    return normalized
