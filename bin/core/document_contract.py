"""Strict, path-owned YAML-frontmatter contracts for Farplane documentation."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError


NonEmptyText = Annotated[str, Field(min_length=1)]


class DocumentContractError(ValueError):
    """Raised when a document does not match its path-owned frontmatter contract."""


class StrictDocumentModel(BaseModel):
    """Reject unowned fields instead of letting YAML become an extension bag."""

    model_config = ConfigDict(extra="forbid", strict=True, str_strip_whitespace=True)


class NarrativeDocumentFrontmatter(StrictDocumentModel):
    """Frontmatter for durable, authored documentation."""

    title: NonEmptyText
    status: NonEmptyText
    owner: NonEmptyText
    created_at: date
    updated_at: date
    tags: list[NonEmptyText] = Field(default_factory=list)
    refs: list[NonEmptyText] = Field(default_factory=list)
    framework_template_version: NonEmptyText | None = None
    source_of_truth: list[NonEmptyText] = Field(default_factory=list)
    version: NonEmptyText | None = None


class GeneratedDocumentFrontmatter(StrictDocumentModel):
    """Frontmatter for generated documentation projections."""

    title: NonEmptyText
    status: Literal["generated"]
    owner: NonEmptyText
    updated_at: date
    created_at: date | None = None
    tags: list[NonEmptyText] = Field(default_factory=list)
    refs: list[NonEmptyText] = Field(default_factory=list)


class TemplateDocumentFrontmatter(StrictDocumentModel):
    """Typed metadata shared by the registered Markdown template surfaces."""

    template_id: NonEmptyText
    template_version: NonEmptyText
    consumer_scope: NonEmptyText
    applies_to: list[NonEmptyText] = Field(default_factory=list)
    status: NonEmptyText | None = None
    kind: NonEmptyText | None = None
    surface_fields: dict[NonEmptyText, NonEmptyText] = Field(default_factory=dict)


def _format_validation_error(error: ValidationError) -> str:
    return "; ".join(
        f"{'.'.join(str(part) for part in item['loc'])}: {item['msg']}"
        for item in error.errors()
    )


def document_contract_name(path: Path, root: Path) -> str:
    """Return the explicit frontmatter family selected by a document path."""

    relative = path.resolve().relative_to(root.resolve()).as_posix()
    if (
        (relative.startswith("skills/harness/templates/") and path.name != "README.md")
        or relative.startswith("skills/manage-wiki/templates/")
        or relative == "skills/report-gen/templates/human-report.md"
    ):
        return "template"
    return "generated" if "generated" in relative.split("/") or path.name == "registry.md" else "narrative"


def validate_document_frontmatter(metadata: dict[str, Any], path: Path, root: Path) -> str:
    """Validate one parsed document frontmatter mapping and return its family."""

    contract_name = document_contract_name(path, root)
    contract = {
        "template": TemplateDocumentFrontmatter,
        "generated": GeneratedDocumentFrontmatter,
        "narrative": NarrativeDocumentFrontmatter,
    }[contract_name]
    try:
        contract.model_validate(metadata)
    except ValidationError as exc:
        raise DocumentContractError(
            f"{path}: invalid {contract_name} frontmatter: {_format_validation_error(exc)}"
        ) from exc
    return contract_name
