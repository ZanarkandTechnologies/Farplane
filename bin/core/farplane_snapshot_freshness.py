"""Local freshness of the generated project UI snapshot, reported by farplane doctor.

The snapshot is ignored machine state, so a stale one is a local hygiene issue,
never a repository contract error.
"""
from __future__ import annotations

import json
from pathlib import Path

from farplane_project_snapshot import PROJECT_SNAPSHOT_PATH, sha256_file


def snapshot_freshness_issues(project_root: Path) -> list[str]:
    """Doctor issues for a UI snapshot whose sources changed since it was written."""
    snapshot_path = project_root / PROJECT_SNAPSHOT_PATH
    if not snapshot_path.exists():
        return []
    try:
        sources = json.loads(snapshot_path.read_text(encoding="utf-8")).get("sources")
    except (OSError, ValueError, AttributeError):
        return [f"project_snapshot_unreadable:{PROJECT_SNAPSHOT_PATH}"]
    issues = []
    for source in sources if isinstance(sources, list) else []:
        if not isinstance(source, dict) or not source.get("path") or not source.get("hash"):
            continue
        current = sha256_file(project_root / str(source["path"]))
        if current and current != source["hash"]:
            issues.append(f"project_snapshot_stale:{source['path']}")
    return issues
