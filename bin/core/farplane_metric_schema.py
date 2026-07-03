from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator


MetricStatus = Literal["available", "source_gap", "not_applicable", "blocked"]
BatchStatus = Literal["available", "source_gap", "partial", "blocked"]

OBSERVATION_ROOT = Path(".farplane/metrics/observations")


class MetricObservation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    metric_id: str
    date: str
    value: float | None
    status: MetricStatus = "available"
    payload: dict[str, Any] = Field(default_factory=dict)

    @field_validator("metric_id", "date")
    @classmethod
    def non_empty_string(cls, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("must be a non-empty string")
        return value.strip()

    @model_validator(mode="after")
    def available_has_value(self) -> "MetricObservation":
        if self.status == "available" and self.value is None:
            raise ValueError("available observations must include a numeric value")
        return self


class MetricObservationBatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal[1] = 1
    date: str
    source_id: str
    status: BatchStatus
    observations: list[MetricObservation] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)
    payload: dict[str, Any] = Field(default_factory=dict)

    @field_validator("date", "source_id")
    @classmethod
    def non_empty_string(cls, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("must be a non-empty string")
        return value.strip()


def metric_observation(
    metric_id: str,
    date: str,
    value: float | int | None,
    status: MetricStatus = "available",
    payload: dict[str, Any] | None = None,
) -> MetricObservation:
    return MetricObservation(
        metric_id=metric_id,
        date=date,
        value=float(value) if isinstance(value, (int, float)) else None,
        status=status,
        payload=payload or {},
    )


def observation_from_reading(
    metric_id: str,
    date: str,
    reading: dict[str, Any],
    payload_extra: dict[str, Any] | None = None,
) -> MetricObservation:
    payload = reading.get("payload") if isinstance(reading.get("payload"), dict) else {}
    if payload_extra:
        payload = {**payload, **payload_extra}
    raw_status = str(reading.get("status") or "available")
    status: MetricStatus = raw_status if raw_status in {"available", "source_gap", "not_applicable", "blocked"} else "source_gap"  # type: ignore[assignment]
    return metric_observation(metric_id, date, reading.get("value"), status, payload)


def metric_batch(
    source_id: str,
    date: str,
    observations: list[MetricObservation | dict[str, Any]],
    gaps: list[str] | None = None,
    status: BatchStatus | None = None,
    payload: dict[str, Any] | None = None,
    **extra: Any,
) -> MetricObservationBatch:
    normalized = [
        item if isinstance(item, MetricObservation) else MetricObservation.model_validate(item)
        for item in observations
    ]
    inferred_status: BatchStatus
    if status is not None:
        inferred_status = status
    elif any(obs.status == "available" for obs in normalized):
        inferred_status = "partial" if gaps else "available"
    else:
        inferred_status = "source_gap"
    return MetricObservationBatch(
        schema_version=1,
        date=date,
        source_id=source_id,
        status=inferred_status,
        observations=normalized,
        gaps=gaps or [],
        payload={**(payload or {}), **extra},
    )


def batch_path(project_root: Path, source_id: str, date: str) -> Path:
    return project_root / OBSERVATION_ROOT / source_id / f"{date}.json"


def write_metric_batch(
    project_root: Path,
    source_id: str,
    date: str,
    observations: list[MetricObservation | dict[str, Any]],
    gaps: list[str] | None = None,
    status: BatchStatus | None = None,
    payload: dict[str, Any] | None = None,
    **extra: Any,
) -> Path:
    batch = metric_batch(source_id, date, observations, gaps, status, payload, **extra)
    path = batch_path(project_root, source_id, date)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(batch.model_dump(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)
    return path


def read_metric_batch(path: Path) -> MetricObservationBatch:
    return MetricObservationBatch.model_validate(json.loads(path.read_text(encoding="utf-8")))


def read_metric_batches(project_root: Path, through_date: str | None = None) -> list[MetricObservationBatch]:
    root = project_root / OBSERVATION_ROOT
    if not root.exists():
        return []
    batches: list[MetricObservationBatch] = []
    for path in sorted(root.glob("*/*.json")):
        if through_date and path.stem > through_date:
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("schema_version") != 1:
            continue
        batches.append(MetricObservationBatch.model_validate(payload))
    return batches


def validate_metric_batch_file(path: Path) -> list[str]:
    try:
        read_metric_batch(path)
    except (json.JSONDecodeError, ValidationError, ValueError) as exc:
        return [f"{path} must match MetricObservationBatch schema: {exc}"]
    return []
