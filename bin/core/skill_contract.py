"""Shared parsing and typed contract for Farplane skill packages."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Annotated, Any, Literal, Union

import yaml
from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, ValidationError, model_validator

from bin.core.lint.source import (
    DuplicateKeyError,
    MarkdownFrontmatterError,
    UniqueYamlLoader,
    parse_markdown_frontmatter as _parse_shared_frontmatter,
    parse_markdown_frontmatter_document as _parse_shared_frontmatter_document,
)


METHOD_CLASSES = {"artifact", "integration", "internal"}
CAPABILITY_ID_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")
CapabilityId = Annotated[str, Field(pattern=CAPABILITY_ID_RE.pattern, min_length=1)]
NonEmptyText = Annotated[str, Field(min_length=1)]


class FrontmatterError(ValueError):
    """Raised when a Markdown YAML-frontmatter block is malformed."""


def parse_markdown_frontmatter_document(
    text: str,
    path: Path,
    *,
    required: bool = False,
) -> tuple[dict[str, Any] | None, str, str]:
    """Parse one Markdown document's YAML frontmatter without a second YAML parser."""

    try:
        return _parse_shared_frontmatter_document(text, path, required=required)
    except MarkdownFrontmatterError as exc:
        raise FrontmatterError(str(exc)) from exc


def parse_markdown_frontmatter(path: Path, *, required: bool = False) -> dict[str, Any] | None:
    """Parse one leading YAML frontmatter mapping, or return ``None`` when absent."""

    try:
        return _parse_shared_frontmatter(path, required=required)
    except MarkdownFrontmatterError as exc:
        raise FrontmatterError(str(exc)) from exc


def _parse_yaml_mapping(source: str, path: Path, *, label: str) -> dict[str, Any]:
    """Parse one YAML mapping with duplicate-key protection."""

    try:
        metadata = yaml.load(source, Loader=UniqueYamlLoader)
    except DuplicateKeyError as exc:
        raise FrontmatterError(f"{path}: duplicate {label} keys: {exc}") from exc
    except yaml.YAMLError as exc:
        raise FrontmatterError(f"{path}: invalid YAML {label}: {exc}") from exc

    if metadata is None:
        return {}
    if not isinstance(metadata, dict):
        raise FrontmatterError(f"{path}: {label} must be a mapping")
    if not all(isinstance(key, str) for key in metadata):
        raise FrontmatterError(f"{path}: {label} keys must be strings")
    return metadata


class StrictContract(BaseModel):
    """Reject fields which are not part of the active machine contract."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class EnsemblePersona(StrictContract):
    """One complete independent perspective for a skill-owned ensemble."""

    id: CapabilityId
    name: NonEmptyText
    prompt: NonEmptyText
    focus: Annotated[list[NonEmptyText], Field(min_length=1)]
    avoid: list[NonEmptyText] = Field(default_factory=list)
    output_shape: NonEmptyText | None = None


class SkillEnsemble(StrictContract):
    """Optional package-local personas for `ensemble: auto | max` calls."""

    version: Literal[1]
    personas: Annotated[list[EnsemblePersona], Field(min_length=3)]

    @model_validator(mode="after")
    def validate_personas(self) -> "SkillEnsemble":
        ids = [persona.id for persona in self.personas]
        if len(ids) != len(set(ids)):
            raise ValueError("persona ids must not contain duplicates")
        return self


class _CapabilityBase(StrictContract):
    pass


class ArtifactCapability(_CapabilityBase):
    """One skill-owned, durable artifact family."""

    kind: Literal["artifact"]
    produces: Annotated[list[CapabilityId], Field(min_length=1, max_length=1)]
    consumes: list[CapabilityId] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_artifact_flow(self) -> "ArtifactCapability":
        if len(self.consumes) != len(set(self.consumes)):
            raise ValueError("consumes must not contain duplicates")
        if self.produces[0] in self.consumes:
            raise ValueError("an artifact must not consume the artifact it produces")
        return self


class IntegrationCapability(_CapabilityBase):
    """A facility that consumes declared artifact families at a system boundary."""

    kind: Literal["integration"]
    consumes: list[CapabilityId] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_integration_inputs(self) -> "IntegrationCapability":
        if len(self.consumes) != len(set(self.consumes)):
            raise ValueError("consumes must not contain duplicates")
        return self


class ShortcutCapability(_CapabilityBase):
    """A non-projected direct command with no Capability Map projection."""

    kind: Literal["shortcut"]


CapabilityContract = Annotated[
    Union[ArtifactCapability, IntegrationCapability, ShortcutCapability],
    Field(discriminator="kind"),
]
CAPABILITY_CONTRACT_ADAPTER = TypeAdapter(CapabilityContract)


class SkillMethod(StrictContract):
    """One named technical method owned by a skill package."""

    id: NonEmptyText
    class_: Literal["artifact", "integration", "internal"] = Field(alias="class")
    output: NonEmptyText


class CommonChains(StrictContract):
    """Optional directional composition hints, never graph dependencies."""

    after: list[NonEmptyText]


class SurfaceSpec(StrictContract):
    path: NonEmptyText | None = None
    status: NonEmptyText | None = None


class PlannerContract(StrictContract):
    required_arguments: list[NonEmptyText]

    @model_validator(mode="after")
    def validate_required_arguments(self) -> "PlannerContract":
        if not self.required_arguments:
            raise ValueError("required_arguments must not be empty")
        if len(self.required_arguments) != len(set(self.required_arguments)):
            raise ValueError("required_arguments must not contain duplicates")
        return self


class SkillFrontmatter(StrictContract):
    """The complete supported frontmatter surface for a local skill package."""

    name: CapabilityId
    description: NonEmptyText
    tier: Literal[1, 2, 3]
    source: Literal["local", "external"]
    group: CapabilityId | None = None
    capability: CapabilityContract | None = None
    methods: list[SkillMethod] | None = None
    common_chains: CommonChains | None = None
    template_uses: dict[NonEmptyText, NonEmptyText] | None = None
    skill_template_version: NonEmptyText | None = None
    version: NonEmptyText | None = None
    eval: NonEmptyText | SurfaceSpec | None = None
    qa_checklist: NonEmptyText | SurfaceSpec | None = None
    skill_ui: NonEmptyText | SurfaceSpec | None = None
    allowed_tools: NonEmptyText | list[NonEmptyText] | None = Field(default=None, alias="allowed-tools")
    upstream_url: NonEmptyText | None = None
    argument_hint: NonEmptyText | None = Field(default=None, alias="argument-hint")
    planner_contract: PlannerContract | None = None
    # Kept only long enough for the existing registry validator to issue its
    # targeted retirement message instead of a generic unknown-field error.
    feature_refs: list[NonEmptyText] | NonEmptyText | None = None
    workflow: Any | None = None


def parse_skill_frontmatter(path: Path) -> dict[str, Any]:
    """Load the required YAML frontmatter block from one skill package."""

    metadata = parse_markdown_frontmatter(path, required=True)
    assert metadata is not None
    return metadata


def parse_skill_ensemble(path: Path) -> dict[str, Any]:
    """Load an optional package-local persona contract only when requested."""

    return _parse_yaml_mapping(path.read_text(encoding="utf-8"), path, label="ensemble")


def normalize_skill_frontmatter(metadata: dict[str, Any], path: Path) -> dict[str, Any]:
    """Return the strict, normalized contract for one skill frontmatter block."""

    try:
        normalized = SkillFrontmatter.model_validate(metadata).model_dump(
            by_alias=True,
            exclude_none=True,
        )
    except ValidationError as exc:
        message = "; ".join(
            f"{'.'.join(str(part) for part in error['loc'])}: {error['msg']}"
            for error in exc.errors()
        )
        raise FrontmatterError(f"{path}: invalid skill frontmatter: {message}") from exc
    return normalized


def normalize_skill_ensemble(metadata: dict[str, Any], path: Path) -> dict[str, Any]:
    """Return the strict, normalized optional ensemble contract for one package."""

    try:
        return SkillEnsemble.model_validate(metadata).model_dump(exclude_none=True)
    except ValidationError as exc:
        message = "; ".join(
            f"{'.'.join(str(part) for part in error['loc'])}: {error['msg']}"
            for error in exc.errors()
        )
        raise FrontmatterError(f"{path}: invalid skill ensemble: {message}") from exc


def normalize_method_contracts(value: Any, skill_name: str, path: Path) -> list[dict[str, str]]:
    if value in (None, ""):
        return []
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise FrontmatterError(
            f"{path}: methods must be a list of mappings with id, class, and output"
        )

    contracts: list[dict[str, str]] = []
    seen_ids: set[str] = set()
    for item in value:
        unknown = set(item) - {"id", "class", "output"}
        if unknown:
            names = ", ".join(sorted(unknown))
            raise FrontmatterError(f"{path}: methods entry has unsupported field(s): {names}")
        method_id = item.get("id")
        method_class = item.get("class")
        output = item.get("output")
        if not isinstance(method_id, str) or not method_id.startswith(f"{skill_name}:"):
            raise FrontmatterError(f"{path}: method id must start with {skill_name}:")
        if method_id in seen_ids:
            raise FrontmatterError(f"{path}: duplicate method id {method_id}")
        if method_class not in METHOD_CLASSES:
            allowed = ", ".join(sorted(METHOD_CLASSES))
            raise FrontmatterError(
                f"{path}: method {method_id} class must be one of: {allowed}"
            )
        if not isinstance(output, str) or not output.strip():
            raise FrontmatterError(f"{path}: method {method_id} output must be a non-empty string")
        seen_ids.add(method_id)
        contracts.append({"id": method_id, "class": method_class, "output": output})
    return contracts


def normalize_capability_contract(value: Any, path: Path) -> dict[str, Any] | None:
    """Validate an optional artifact, integration, or shortcut capability contract."""

    if value in (None, ""):
        return None
    if not isinstance(value, dict):
        raise FrontmatterError(f"{path}: capability must be a mapping")
    try:
        contract = CAPABILITY_CONTRACT_ADAPTER.validate_python(value)
    except ValidationError as exc:
        message = "; ".join(
            f"{'.'.join(str(part) for part in error['loc'])}: {error['msg']}"
            for error in exc.errors()
        )
        raise FrontmatterError(f"{path}: invalid capability contract: {message}") from exc
    return contract.model_dump(mode="json")
