"""Cross-skill composition rules for the generated skill registry."""

from __future__ import annotations

from pathlib import Path
from typing import Any


class SkillCompositionError(ValueError):
    """Raised when skill composition violates the capability contract."""


def skill_ref_name(ref: str) -> str:
    """Return the skill portion of a skill, anchor, or method reference."""

    return ref.split("#", 1)[0].split(":", 1)[0]


def _composition_refs(row: dict[str, Any]) -> dict[str, list[str]]:
    return {
        "todo_skill_refs": [
            skill_ref_name(ref) for ref in row.get("todo_skill_refs", [])
        ],
        "skill_links": [skill_ref_name(ref) for ref in row.get("skill_links", [])],
        "common_chains": [
            skill_ref_name(ref)
            for ref in row.get("common_chains", {}).get("after", [])
        ],
    }


def _format_refs(refs_by_field: dict[str, list[str]]) -> str:
    return "; ".join(
        f"{field}={','.join(refs)}" for field, refs in refs_by_field.items()
    )


def validate_shortcut_composition_leaves(
    repo_root: Path,
    rows: list[dict[str, Any]],
) -> None:
    """Keep explicit-only shortcuts out of composition edges in both directions."""

    shortcut_names = {
        row["name"]
        for row in rows
        if isinstance(row.get("capability"), dict)
        and row["capability"].get("kind") == "shortcut"
    }
    if not shortcut_names:
        return

    for row in rows:
        targeted = {
            field: sorted(set(refs) & shortcut_names)
            for field, refs in _composition_refs(row).items()
            if set(refs) & shortcut_names
        }
        if targeted:
            source_path = repo_root / row["path"]
            raise SkillCompositionError(
                f"{source_path}: composition must not target explicit-only shortcut "
                f"skill(s) ({_format_refs(targeted)})"
            )

    for row in rows:
        capability = row.get("capability")
        if not isinstance(capability, dict) or capability.get("kind") != "shortcut":
            continue
        populated = {
            field: sorted(set(refs))
            for field, refs in _composition_refs(row).items()
            if refs
        }
        if populated:
            source_path = repo_root / row["path"]
            raise SkillCompositionError(
                f"{source_path}: explicit-only shortcut must be a composition leaf; "
                f"remove outbound composition refs ({_format_refs(populated)})"
            )
