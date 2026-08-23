"""Strict, path-owned YAML-frontmatter contracts for Farplane documentation."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError


FEATURE_ID_RE = re.compile(r"^FEAT-\d{4}$")
SYSTEM_ID_RE = re.compile(r"^SYS-\d{4}$")
NonEmptyText = Annotated[str, Field(min_length=1)]
FeatureId = Annotated[str, Field(pattern=FEATURE_ID_RE.pattern)]
SystemId = Annotated[str, Field(pattern=SYSTEM_ID_RE.pattern)]


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


class FeatureDocumentFrontmatter(NarrativeDocumentFrontmatter):
    """Typed source header for one authored FEAT page."""

    feature_id: FeatureId
    system_id: SystemId
    category: NonEmptyText
    public: bool
    surfaces: list[NonEmptyText]
    source_refs: list[NonEmptyText]
    external_refs: list[NonEmptyText]
    evidence_refs: list[NonEmptyText]
    known_limits: NonEmptyText
    metrics: list[NonEmptyText]
    last_verified: date
    experimental: bool
    superseded_by: bool | FeatureId | list[FeatureId]
    track: bool | NonEmptyText = False


class SystemDocumentFrontmatter(NarrativeDocumentFrontmatter):
    """Typed source header for one authored system page."""

    system_record_json: NonEmptyText


class FeatureTemplateFrontmatter(StrictDocumentModel):
    """Typed literal template for authored FEAT pages, including placeholders."""

    title: NonEmptyText
    status: NonEmptyText
    owner: NonEmptyText
    created_at: Literal["YYYY-MM-DD"]
    updated_at: Literal["YYYY-MM-DD"]
    tags: list[NonEmptyText]
    refs: list[NonEmptyText]
    feature_id: Literal["FEAT-####"]
    system_id: Literal["SYS-####"]
    category: NonEmptyText
    public: bool
    surfaces: list[NonEmptyText]
    source_refs: list[NonEmptyText]
    external_refs: list[NonEmptyText]
    evidence_refs: list[NonEmptyText]
    known_limits: NonEmptyText
    metrics: list[NonEmptyText]
    last_verified: Literal["YYYY-MM-DD"]
    experimental: bool
    superseded_by: bool | FeatureId | list[FeatureId]
    track: bool | NonEmptyText = False


class TemplateDocumentFrontmatter(StrictDocumentModel):
    """Typed metadata shared by the registered Markdown template surfaces."""

    template_id: NonEmptyText
    template_version: NonEmptyText
    feature_refs: list[FeatureId]
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
    if relative == "docs/features/TEMPLATE.md":
        return "feature_template"
    if re.fullmatch(r"docs/features/FEAT-\d{4}-.+\.md", relative):
        return "feature"
    if relative.startswith("docs/systems/") and path.name not in {"README.md", "registry.md"}:
        return "system"
    if relative.startswith("docs/skills/templates/") or relative == "docs/templates/HUMAN_REPORT_TEMPLATE.md":
        return "template"
    return "generated" if "generated" in relative.split("/") or path.name == "registry.md" else "narrative"


def validate_document_frontmatter(metadata: dict[str, Any], path: Path, root: Path) -> str:
    """Validate one parsed document frontmatter mapping and return its family."""

    contract_name = document_contract_name(path, root)
    contract = {
        "feature_template": FeatureTemplateFrontmatter,
        "feature": FeatureDocumentFrontmatter,
        "system": SystemDocumentFrontmatter,
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
