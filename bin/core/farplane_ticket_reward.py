"""Validate the scheduling contract in ticket Reward rows."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


UNSCHEDULED_CHECK_IN = "unscheduled"


def markdown_heading_section(markdown: str, heading: str) -> str:
    lines = markdown.splitlines()
    target = f"## {heading}"
    for start, line in enumerate(lines):
        if line.strip() != target:
            continue
        end = next(
            (index for index in range(start + 1, len(lines)) if lines[index].startswith("## ")),
            len(lines),
        )
        return "\n".join(lines[start + 1 : end]).strip()
    return ""


def parse_fenced_yaml(section: str) -> tuple[dict[str, Any] | None, str | None]:
    fence_start = section.find("```yaml")
    if fence_start == -1:
        return None, "Reward must contain a fenced YAML block"
    yaml_start = section.find("\n", fence_start)
    fence_end = section.find("```", yaml_start + 1) if yaml_start != -1 else -1
    if yaml_start == -1 or fence_end == -1:
        return None, "Reward must contain a closed fenced YAML block"
    try:
        payload = yaml.safe_load(section[yaml_start + 1 : fence_end]) or {}
    except yaml.YAMLError as exc:
        return None, f"Reward fenced YAML is invalid: {exc}"
    if not isinstance(payload, dict):
        return None, "Reward fenced YAML must be a mapping"
    return payload, None


def is_timezone_bearing_iso_datetime(value: object) -> bool:
    if isinstance(value, datetime):
        return value.tzinfo is not None and value.utcoffset() is not None
    if not isinstance(value, str):
        return False
    raw = value.strip()
    if not raw or raw == UNSCHEDULED_CHECK_IN:
        return False
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


def validate_reward_markdown(markdown: str) -> list[str]:
    section = markdown_heading_section(markdown, "Reward")
    if not section:
        return []
    payload, parse_error = parse_fenced_yaml(section)
    if parse_error:
        return [parse_error]
    assert payload is not None
    raw_rewards = payload.get("kpi_rewards")
    if raw_rewards is None:
        return []
    if not isinstance(raw_rewards, list):
        return ["Reward.kpi_rewards must be a list"]

    errors: list[str] = []
    for index, raw_reward in enumerate(raw_rewards):
        if not isinstance(raw_reward, dict):
            errors.append(f"Reward.kpi_rewards[{index}] must be a mapping")
            continue
        check_in_at = raw_reward.get("check_in_at")
        if check_in_at == UNSCHEDULED_CHECK_IN or is_timezone_bearing_iso_datetime(check_in_at):
            continue
        reward_id = str(raw_reward.get("reward_id") or f"row-{index}").strip()
        errors.append(
            f"Reward.kpi_rewards[{index}] ({reward_id}) check_in_at must be a "
            "timezone-bearing ISO-8601 timestamp or the literal 'unscheduled'"
        )
    return errors


def validate_reward_file(path: Path) -> list[str]:
    return validate_reward_markdown(path.read_text(encoding="utf-8"))
