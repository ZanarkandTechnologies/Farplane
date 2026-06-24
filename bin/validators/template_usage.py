"""Shared template usage metadata helpers.

The standard consumer shape is:

  template_uses:
    template-id: "x.y.z"

Legacy fields stay readable only so rollout reports can explain older files.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


LEGACY_TEMPLATE_FIELDS = {
    "skill_template_version": "skill-template",
    "framework_template_version": "farplane-framework",
}

TEMPLATE_TARGET_BASIS = {
    "skill-template": "local skills that declare skill-template usage",
    "skill-eval-task": "skills with an eval_task.json surface",
    "skill-qa-checklist": "skills with a qa_checklist.md surface",
    "skill-method-reference": "skill reference files that declare method-reference usage",
    "farplane-framework": "projects with a farplane/manifest.json surface",
    "farplane-steer-config": "projects in the rollout inventory",
}


class TemplateUsageError(ValueError):
    """Raised when template usage metadata is malformed."""


def normalize_template_uses(
    metadata: dict[str, Any], path: Path | str, *, include_legacy: bool = True
) -> dict[str, str]:
    """Return normalized template uses from front matter or JSON metadata."""

    path_label = str(path)
    raw = metadata.get("template_uses", {})
    uses: dict[str, str] = {}

    if raw in (None, ""):
        raw = {}
    if not isinstance(raw, dict):
        raise TemplateUsageError(f"{path_label}: template_uses must be a mapping")

    for template_id, version in raw.items():
        if not isinstance(template_id, str) or not template_id.strip():
            raise TemplateUsageError(f"{path_label}: template_uses keys must be non-empty strings")
        if not isinstance(version, str) or not version.strip():
            raise TemplateUsageError(
                f"{path_label}: template_uses.{template_id} must be a non-empty string"
            )
        uses[template_id.strip()] = version.strip()

    if include_legacy:
        for field, template_id in LEGACY_TEMPLATE_FIELDS.items():
            version = metadata.get(field)
            if version not in (None, "") and template_id not in uses:
                uses[template_id] = str(version).strip()

    return uses


def legacy_template_uses(metadata: dict[str, Any]) -> dict[str, str]:
    """Return only legacy-template-field usages for migration reporting."""

    uses: dict[str, str] = {}
    for field, template_id in LEGACY_TEMPLATE_FIELDS.items():
        version = metadata.get(field)
        if version not in (None, ""):
            uses[template_id] = str(version).strip()
    return uses


def template_target_basis(template_id: str) -> str:
    """Return the plain-English target rule for rollout reports."""

    return TEMPLATE_TARGET_BASIS.get(template_id, f"consumers declaring {template_id}")
