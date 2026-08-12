from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml


TEST_DIR = Path(__file__).resolve().parent
if str(TEST_DIR) not in sys.path:
    sys.path.insert(0, str(TEST_DIR))

from test_check_farplane_project_files import write_framework_manifest, write_required_project_files
from bin.validators.check_farplane_project_files import validate


def test_markdown_edge_metric_is_valid_only_as_one_unselected_text_field(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    metrics_path = farplane / "metrics.yaml"
    metrics = yaml.safe_load(metrics_path.read_text(encoding="utf-8"))
    metrics["metrics"]["edge"] = {
        "refresh": "Summarize verified project edge.",
        "label": "Edge",
        "description": "Current demonstrable advantage.",
        "type": "markdown",
        "leverage": "edge",
        "pinned": True,
        "max_age_days": 1,
    }
    metrics_path.write_text(yaml.safe_dump(metrics, sort_keys=False), encoding="utf-8")

    assert validate(tmp_path) == []


def test_markdown_leverage_contract_rejects_invalid_combinations_and_duplicate_edge(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    metrics_path = farplane / "metrics.yaml"
    metrics = yaml.safe_load(metrics_path.read_text(encoding="utf-8"))
    metrics["metrics"]["edge"] = {
        "refresh": "Summarize verified project edge.",
        "label": "Edge",
        "description": "Current demonstrable advantage.",
        "type": "markdown",
        "leverage": "distribution",
        "unit": "claims",
        "direction": "maximize",
    }
    metrics["metrics"]["edge_two"] = {
        "refresh": "Summarize another edge.",
        "label": "Another edge",
        "description": "Invalid second edge.",
        "type": "markdown",
        "leverage": "edge",
    }
    metrics["metrics"]["edge_three"] = {
        "refresh": "Summarize another edge again.",
        "label": "Third edge.",
        "description": "Invalid third edge.",
        "type": "markdown",
        "leverage": "edge",
    }
    metrics_path.write_text(yaml.safe_dump(metrics, sort_keys=False), encoding="utf-8")

    errors = validate(tmp_path)

    assert "farplane/metrics.yaml metrics.edge.leverage distribution requires type: flow or stock." in errors
    assert "farplane/metrics.yaml metrics.edge type markdown cannot declare: direction, unit." in errors
    assert "farplane/metrics.yaml may declare exactly one leverage edge metric: edge_three, edge_two." in errors


def test_markdown_observation_requires_text_value(tmp_path: Path) -> None:
    farplane = tmp_path / "farplane"
    farplane.mkdir()
    write_framework_manifest(farplane)
    write_required_project_files(tmp_path)
    metrics_path = farplane / "metrics.yaml"
    metrics = yaml.safe_load(metrics_path.read_text(encoding="utf-8"))
    metrics["metrics"]["edge"] = {
        "refresh": "Summarize verified project edge.",
        "label": "Edge",
        "description": "Current demonstrable advantage.",
        "type": "markdown",
        "leverage": "edge",
        "pinned": True,
    }
    metrics_path.write_text(yaml.safe_dump(metrics, sort_keys=False), encoding="utf-8")
    observation_path = tmp_path / ".farplane" / "metrics" / "observations" / "metric:edge" / "2026-08-12.json"
    observation_path.parent.mkdir(parents=True)
    observation_path.write_text(json.dumps({"schema_version": 1, "date": "2026-08-12", "source_id": "metric:edge", "status": "available", "observations": [{"metric_id": "edge", "date": "2026-08-12", "value": 4, "status": "available"}], "gaps": []}), encoding="utf-8")

    errors = validate(tmp_path)

    assert ".farplane/metrics/observations/metric:edge/2026-08-12.json edge@2026-08-12 must have a non-empty Markdown value." in errors
