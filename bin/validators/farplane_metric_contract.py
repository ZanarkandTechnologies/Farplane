"""Strict validation for project metric definitions."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, StrictBool, ValidationError, field_validator


class MetricDefinitionModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    type: Literal["flow", "stock", "markdown"]
    unit: str | None = None
    direction: Literal["maximize", "minimize"] | None = None
    label: str | None = None
    description: str | None = None
    display: Literal["bar_plus_cumulative", "line", "reading"] | None = None
    pinned: StrictBool | None = None
    max_age_days: int | None = None
    guard: dict[str, Any] | None = None
    leverage: Literal["distribution", "edge"] | None = None

    @field_validator("unit")
    @classmethod
    def non_empty_string(cls, value: str | None) -> str | None:
        if value is not None and (not isinstance(value, str) or not value.strip()):
            raise ValueError("must be a non-empty string")
        return value.strip() if value is not None else None

    @field_validator("label", "description")
    @classmethod
    def optional_non_empty_string(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("must be a non-empty string when present")
        return value.strip() if value is not None else None


def validate_metric_definition_schema(metrics: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    allowed_types = {"flow", "stock", "markdown"}
    allowed_displays = {"bar_plus_cumulative", "reading", "line"}
    edge_metric_ids: list[str] = []
    for metric_id, definition in sorted(metrics.items()):
        prefix = f"farplane/metrics.yaml metrics.{metric_id}"
        metric_type = str(definition.get("type") or "")
        is_markdown = metric_type == "markdown"
        is_numeric = metric_type in {"flow", "stock"}
        refresh_ref = definition.get("refresh_ref")
        inline_refresh = definition.get("refresh")
        if bool(refresh_ref) == bool(inline_refresh):
            errors.append(f"{prefix} must declare exactly one of refresh_ref or refresh.")
        if "product" in definition:
            errors.append(f"{prefix}.product is retired; metrics are project-level definitions.")
        derived_or_projection_fields = sorted(
            field
            for field in (
                "aggregation",
                "alignment",
                "cadence",
                "compare",
                "cumulative",
                "formula",
                "kind",
                "timezone",
                "window",
                "windows",
            )
            if field in definition
        )
        if derived_or_projection_fields:
            errors.append(
                f"{prefix} uses unsupported derived/projection config: "
                f"{', '.join(derived_or_projection_fields)}; declare only type: "
                "flow|stock|markdown and let refreshers emit facts while Core derives window views."
            )
        leverage = definition.get("leverage")
        if leverage not in {None, "distribution", "edge"}:
            errors.append(f"{prefix}.leverage must be distribution or edge when present.")
        if leverage == "distribution" and not is_numeric:
            errors.append(f"{prefix}.leverage distribution requires type: flow or stock.")
        if leverage == "edge":
            edge_metric_ids.append(metric_id)
            if not is_markdown:
                errors.append(f"{prefix}.leverage edge requires type: markdown.")
        if is_markdown:
            disallowed_markdown_fields = sorted(
                field
                for field in ("direction", "display", "guard", "target", "target_direction", "unit")
                if field in definition
            )
            if disallowed_markdown_fields:
                errors.append(
                    f"{prefix} type markdown cannot declare: {', '.join(disallowed_markdown_fields)}."
                )
        elif is_numeric:
            if not str(definition.get("unit") or "").strip():
                errors.append(f"{prefix}.unit must be a non-empty string.")
            if not str(definition.get("direction") or "").strip():
                errors.append(f"{prefix}.direction must be a non-empty string.")
            elif definition.get("direction") not in {"maximize", "minimize"}:
                errors.append(f"{prefix}.direction must be maximize or minimize.")
        if "max_age_days" in definition and (
            not isinstance(definition.get("max_age_days"), int) or definition.get("max_age_days", 0) < 1
        ):
            errors.append(f"{prefix}.max_age_days must be a positive integer.")
        guard = definition.get("guard")
        if guard is not None:
            if not isinstance(guard, dict):
                errors.append(f"{prefix}.guard must be an object.")
            else:
                if guard.get("operator") not in {"greater_than_or_equal", "less_than_or_equal"}:
                    errors.append(
                        f"{prefix}.guard.operator must be greater_than_or_equal or less_than_or_equal."
                    )
                if not isinstance(guard.get("threshold"), (int, float)):
                    errors.append(f"{prefix}.guard.threshold must be numeric.")
        try:
            MetricDefinitionModel.model_validate(definition)
        except ValidationError as exc:
            for error in exc.errors():
                field = ".".join(str(part) for part in error.get("loc", ()))
                error_type = str(error.get("type") or "")
                if field == "type" and error_type in {"missing", "value_error", "string_type"}:
                    errors.append(f"{prefix}.{field} must be a non-empty string.")
                elif field == "type" and error_type == "literal_error":
                    errors.append(f"{prefix}.type must be one of: {', '.join(sorted(allowed_types))}.")
                elif field == "direction" and error_type == "literal_error":
                    errors.append(f"{prefix}.direction must be maximize or minimize.")
                elif field in {"label", "description"}:
                    errors.append(f"{prefix}.{field} must be a non-empty string when present.")
                elif field == "display" and error_type == "literal_error":
                    errors.append(f"{prefix}.display must be one of: {', '.join(sorted(allowed_displays))}.")
                elif field == "pinned":
                    errors.append(f"{prefix}.pinned must be boolean when present.")
                else:
                    errors.append(f"{prefix}.{field}: {error.get('msg')}.")
    if len(edge_metric_ids) > 1:
        errors.append(
            "farplane/metrics.yaml may declare exactly one leverage edge metric: "
            f"{', '.join(edge_metric_ids)}."
        )
    return errors
