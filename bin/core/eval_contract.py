"""Typed, portable Agent-Skills eval-suite contract for Farplane."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, JsonValue, ValidationError, field_validator, model_validator


SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FEATURE_ID_RE = re.compile(r"^FEAT-\d{4}$")


class EvalContractError(ValueError):
    """Raised when an authored Agent-Skills eval suite is not portable or safe."""


class StrictEvalModel(BaseModel):
    """Keep the portable contract closed except for its named extension map."""

    model_config = ConfigDict(extra="forbid", strict=True, str_strip_whitespace=True)


class FarplaneEvalMetadata(StrictEvalModel):
    """Typed execution, identity, and linkage metadata for one eval case."""

    title: str | None = None
    context: str | None = None
    notes: str | None = None
    tags: list[str] = Field(default_factory=list)
    workspace_fixture: str | None = None
    feature_id: str | None = Field(default=None, pattern=FEATURE_ID_RE.pattern)
    extensions: dict[str, JsonValue] = Field(default_factory=dict)

    @field_validator("tags")
    @classmethod
    def validate_text_list(cls, values: list[str]) -> list[str]:
        if any(not value for value in values):
            raise ValueError("list values must be non-empty strings")
        if len(values) != len(set(values)):
            raise ValueError("list values must not contain duplicates")
        return values

    @field_validator("workspace_fixture")
    @classmethod
    def validate_workspace_fixture(cls, value: str | None) -> str | None:
        if value is None:
            return None
        candidate = Path(value)
        if candidate.is_absolute() or ".." in candidate.parts:
            raise ValueError("workspace_fixture must stay relative to the skill root")
        return candidate.as_posix()


class EvalMetadata(StrictEvalModel):
    """Reserve the metadata namespace rather than accepting arbitrary case keys."""

    farplane: FarplaneEvalMetadata | None = None


class AgentSkillsEvalCase(StrictEvalModel):
    """One portable Agent-Skills evaluation case."""

    id: str = Field(min_length=1)
    prompt: str = Field(min_length=1)
    expected_output: str = Field(min_length=1)
    files: list[str] = Field(default_factory=list)
    assertions: list[str] = Field(default_factory=list)
    metadata: EvalMetadata | None = None

    @field_validator("files")
    @classmethod
    def validate_files(cls, values: list[str]) -> list[str]:
        normalized: list[str] = []
        for value in values:
            if not value:
                raise ValueError("file paths must be non-empty strings")
            candidate = Path(value)
            if candidate.is_absolute() or ".." in candidate.parts:
                raise ValueError("file paths must stay relative to the skill root")
            normalized.append(candidate.as_posix())
        if len(normalized) != len(set(normalized)):
            raise ValueError("file paths must not contain duplicates")
        return normalized

    @field_validator("assertions")
    @classmethod
    def validate_assertions(cls, values: list[str]) -> list[str]:
        if any(not value for value in values):
            raise ValueError("assertions must be non-empty strings")
        if len(values) != len(set(values)):
            raise ValueError("assertions must not contain duplicates")
        return values


class AgentSkillsEvalSuite(StrictEvalModel):
    """The original Agent-Skills portable root, deliberately without a format key."""

    skill_name: str = Field(min_length=1, pattern=SKILL_NAME_RE.pattern)
    evals: list[AgentSkillsEvalCase] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_unique_case_ids(self) -> "AgentSkillsEvalSuite":
        ids = [case.id for case in self.evals]
        if len(ids) != len(set(ids)):
            raise ValueError("eval IDs must be unique")
        return self


def _format_validation_error(error: ValidationError) -> str:
    details = []
    for item in error.errors():
        location = ".".join(str(part) for part in item["loc"]) or "$"
        details.append(f"{location}: {item['msg']}")
    return "; ".join(details)


def load_agent_skills_eval_suite(path: Path) -> AgentSkillsEvalSuite:
    """Parse and type one suite without making filesystem assertions."""

    try:
        raw: Any = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise EvalContractError(f"cannot read eval manifest: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise EvalContractError(f"invalid JSON: {exc.msg} (line {exc.lineno}, column {exc.colno})") from exc
    try:
        return AgentSkillsEvalSuite.model_validate(raw)
    except ValidationError as exc:
        raise EvalContractError(_format_validation_error(exc)) from exc


def _feature_registry(root: Path) -> dict[str, dict[str, Any]]:
    registry_path = root / "docs" / "features" / "registry.jsonl"
    if not registry_path.is_file():
        raise EvalContractError("feature registry is missing: docs/features/registry.jsonl")
    features: dict[str, dict[str, Any]] = {}
    for line_number, line in enumerate(registry_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise EvalContractError(
                f"feature registry is invalid JSON at line {line_number}: {exc.msg}"
            ) from exc
        if isinstance(row, dict) and isinstance(row.get("id"), str):
            features[row["id"]] = row
    return features


def _validate_feature_binding(*, root: Path, feature_id: str, skill_root: Path, feature: dict[str, Any]) -> None:
    """Prove that an eval's feature link resolves to its docs and owning skill."""

    owner_spec = feature.get("owner_spec")
    if not isinstance(owner_spec, str) or not owner_spec.strip():
        raise EvalContractError(f"feature_id {feature_id} has no owner_spec in the feature registry")
    owner_path = Path(owner_spec)
    if owner_path.is_absolute() or ".." in owner_path.parts:
        raise EvalContractError(f"feature_id {feature_id} has an unsafe owner_spec: {owner_spec}")
    if not (root / owner_path).is_file():
        raise EvalContractError(f"feature_id {feature_id} owner_spec does not exist: {owner_spec}")

    try:
        skill_surface = skill_root.relative_to(root).as_posix()
    except ValueError as exc:
        raise EvalContractError("eval skill directory must be inside the Farplane repository") from exc
    surfaces = feature.get("surfaces")
    if not isinstance(surfaces, list) or skill_surface not in surfaces:
        raise EvalContractError(
            f"feature_id {feature_id} must list {skill_surface} in feature registry surfaces"
        )


def lint_agent_skills_eval_suite(path: Path, *, root: Path) -> AgentSkillsEvalSuite:
    """Validate one suite's typed shape and feature-document references."""

    suite = load_agent_skills_eval_suite(path)
    skill_root = path.parent.parent.resolve()
    if path.parent.name != "evals":
        raise EvalContractError("eval manifest must be named evals/evals.json")
    if suite.skill_name != skill_root.name:
        raise EvalContractError(
            f"skill_name {suite.skill_name!r} must match owning directory {skill_root.name!r}"
        )
    feature_registry: dict[str, dict[str, Any]] | None = None
    for case in suite.evals:
        farplane = case.metadata.farplane if case.metadata else None
        if farplane is None:
            continue
        if farplane.feature_id:
            if feature_registry is None:
                feature_registry = _feature_registry(root.resolve())
            feature = feature_registry.get(farplane.feature_id)
            if feature is None:
                raise EvalContractError(f"unknown feature_id: {farplane.feature_id}")
            _validate_feature_binding(
                root=root.resolve(),
                feature_id=farplane.feature_id,
                skill_root=skill_root,
                feature=feature,
            )
    return suite


def suite_json_schema() -> dict[str, Any]:
    """Return the generated source-of-truth JSON Schema for documentation/tooling."""

    return AgentSkillsEvalSuite.model_json_schema()
