"""Typed, portable Agent-Skills eval-suite contract for Farplane."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, JsonValue, ValidationError, field_validator, model_validator


SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


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
    workspace_setup: str | None = None
    extensions: dict[str, JsonValue] = Field(default_factory=dict)

    @field_validator("tags")
    @classmethod
    def validate_text_list(cls, values: list[str]) -> list[str]:
        if any(not value for value in values):
            raise ValueError("list values must be non-empty strings")
        if len(values) != len(set(values)):
            raise ValueError("list values must not contain duplicates")
        return values

    @field_validator("workspace_fixture", "workspace_setup")
    @classmethod
    def validate_workspace_fixture(cls, value: str | None) -> str | None:
        if value is None:
            return None
        candidate = Path(value)
        if candidate.is_absolute() or ".." in candidate.parts:
            raise ValueError("workspace paths must stay relative to the skill root")
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


def lint_agent_skills_eval_suite(path: Path, *, root: Path) -> AgentSkillsEvalSuite:
    """Validate one suite's typed shape and its owning-skill placement."""

    suite = load_agent_skills_eval_suite(path)
    skill_root = path.parent.parent.resolve()
    if path.parent.name != "evals":
        raise EvalContractError("eval manifest must be named evals/evals.json")
    if suite.skill_name != skill_root.name:
        raise EvalContractError(
            f"skill_name {suite.skill_name!r} must match owning directory {skill_root.name!r}"
        )
    return suite


def suite_json_schema() -> dict[str, Any]:
    """Return the generated source-of-truth JSON Schema for documentation/tooling."""

    return AgentSkillsEvalSuite.model_json_schema()
