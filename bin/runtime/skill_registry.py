from __future__ import annotations

import json
import re
from pathlib import Path
from typing import NamedTuple


SKILL_MENTION_PATTERN = re.compile(
    r"(?:"
    r"(?<!\S)\$(?P<plain_skill>[A-Za-z0-9][A-Za-z0-9_-]*)(?![A-Za-z0-9_-])"
    r"|"
    r"(?<=\[)\$(?P<linked_skill>[A-Za-z0-9][A-Za-z0-9_-]*)"
    r"(?=\]\([^\n)]*/SKILL\.md(?:#[^\n)]*)?\))"
    r")",
    re.IGNORECASE,
)
SKILL_REGISTRY_RELATIVE_PATH = Path("docs/skills/registry.jsonl")


class SkillRegistrySnapshot(NamedTuple):
    records: dict[str, dict[str, object]]
    status: str
    path: Path
    error: str


def load_skill_registry(project_root: Path) -> SkillRegistrySnapshot:
    path = project_root / SKILL_REGISTRY_RELATIVE_PATH
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return SkillRegistrySnapshot({}, "missing", path, "registry file not found")
    except OSError as exc:
        return SkillRegistrySnapshot({}, "invalid", path, f"registry read failed: {exc}")

    records: dict[str, dict[str, object]] = {}
    try:
        for line_number, raw_line in enumerate(lines, start=1):
            if not raw_line.strip():
                continue
            record = json.loads(raw_line)
            if not isinstance(record, dict):
                raise ValueError(f"line {line_number} is not an object")
            name = record.get("name")
            if not isinstance(name, str) or not name.strip():
                raise ValueError(f"line {line_number} has no skill name")
            canonical_name = name.strip()
            lookup_name = canonical_name.lower()
            if lookup_name in records:
                raise ValueError(f"line {line_number} duplicates skill {canonical_name}")
            records[lookup_name] = {**record, "name": canonical_name}
    except (json.JSONDecodeError, ValueError) as exc:
        return SkillRegistrySnapshot({}, "invalid", path, str(exc))
    return SkillRegistrySnapshot(records, "loaded", path, "")


def extract_skill_mentions(
    raw_text: str,
    *,
    project_root: Path | None = None,
    registry: SkillRegistrySnapshot | None = None,
) -> list[str]:
    snapshot = registry or load_skill_registry(
        project_root or Path(__file__).resolve().parents[2]
    )
    if snapshot.status != "loaded":
        return []

    mentions: list[str] = []
    seen: set[str] = set()
    for match in SKILL_MENTION_PATTERN.finditer(raw_text):
        lookup_name = str(
            match.group("plain_skill") or match.group("linked_skill") or ""
        ).strip().lower()
        record = snapshot.records.get(lookup_name)
        if record is None or lookup_name in seen:
            continue
        seen.add(lookup_name)
        mentions.append(str(record["name"]))
    return mentions
