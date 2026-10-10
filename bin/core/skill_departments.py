"""Canonical department taxonomy shared by skill validation and graph projection."""

from __future__ import annotations

import tomllib
from pathlib import Path


class DepartmentTaxonomyError(ValueError):
    """Raised when the checked-in department taxonomy is malformed."""


class CapabilityAdmissionConfigError(ValueError):
    """Raised when the Capability Map's classified admission config is malformed."""


def load_skill_departments(repo_root: Path) -> dict[str, str]:
    path = repo_root / "config" / "skill-departments.toml"
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


def load_skill_specialists(
    repo_root: Path, departments: dict[str, str] | None = None
) -> dict[str, dict[str, object]]:
    """Load specialist desks: id -> label, department, deliverable, primary, and skills.

    Each desk lists its member skills; a skill may sit at only one desk.
    """
    department_labels = departments or load_skill_departments(repo_root)
    path = repo_root / "config" / "skill-workflows.toml"
    try:
        payload = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise CapabilityAdmissionConfigError(f"unable to load {path}: {exc}") from exc

    raw = payload.get("specialists")
    if not isinstance(raw, dict) or not raw:
        raise CapabilityAdmissionConfigError(f"{path}: [specialists] must be a non-empty table")
    specialists: dict[str, dict[str, object]] = {}
    seat: dict[str, str] = {}
    for specialist_id, entry in raw.items():
        where = f"{path}: specialists.{specialist_id}"
        if not isinstance(entry, dict):
            raise CapabilityAdmissionConfigError(f"{where} must be a table")
        unknown = sorted(set(entry).difference({"label", "department", "deliverable", "primary", "skills"}))
        if unknown:
            raise CapabilityAdmissionConfigError(f"{where} has unknown keys: {', '.join(unknown)}")
        values: dict[str, object] = {}
        for key in ("label", "department", "deliverable", "primary"):
            value = entry.get(key)
            if not isinstance(value, str) or not value.strip():
                raise CapabilityAdmissionConfigError(f"{where}.{key} must be a non-empty string")
            values[key] = value.strip()
        if values["department"] not in department_labels:
            raise CapabilityAdmissionConfigError(f"{where}.department {values['department']!r} is not a department")
        skills = entry.get("skills")
        if not isinstance(skills, list) or not skills or not all(isinstance(item, str) and item for item in skills):
            raise CapabilityAdmissionConfigError(f"{where}.skills must be a non-empty list of skill names")
        if len(skills) != len(set(skills)):
            raise CapabilityAdmissionConfigError(f"{where}.skills must not repeat a skill")
        for skill in skills:
            if skill in seat:
                raise CapabilityAdmissionConfigError(
                    f"{where}: skill {skill!r} already sits at specialist {seat[skill]!r}"
                )
            seat[skill] = specialist_id
        if values["primary"] not in skills:
            raise CapabilityAdmissionConfigError(f"{where}.primary {values['primary']!r} must be one of its skills")
        values["skills"] = tuple(skills)
        specialists[specialist_id] = values
    return specialists


def specialist_by_skill(specialists: dict[str, dict[str, object]]) -> dict[str, str]:
    return {skill: specialist_id for specialist_id, entry in specialists.items() for skill in entry["skills"]}


def desk_primary_skills(repo_root: Path) -> set[str]:
    """Each Capability Map desk's primary skill (its default verb); none for a project without desks."""
    try:
        return {str(desk["primary"]) for desk in load_skill_specialists(repo_root).values()}
    except (CapabilityAdmissionConfigError, DepartmentTaxonomyError):
        return set()


def validate_specialist_membership(
    rows: list[dict[str, object]], specialists: dict[str, dict[str, object]]
) -> list[str]:
    """Return errors for desk members that are missing or in another department."""
    rows_by_name = {str(row.get("name")): row for row in rows}
    errors: list[str] = []
    for specialist_id, entry in specialists.items():
        for skill in entry["skills"]:
            row = rows_by_name.get(skill)
            if row is None:
                errors.append(f"specialist {specialist_id!r} lists unknown skill {skill!r}")
            elif row.get("department") != entry["department"]:
                errors.append(
                    f"{skill}: department {row.get('department')!r} differs from specialist "
                    f"{specialist_id!r} department {entry['department']!r}"
                )
    return errors
