#!/usr/bin/env python3
"""Scaffold a best-of-worlds synthesis workspace."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True, help="Workspace slug")
    parser.add_argument("--target", required=True, help="Synthesis target")
    parser.add_argument("--source", action="append", default=[], help="Source URL, repo, or project path")
    parser.add_argument("--directory", default="experiments/best-of-worlds")
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip()).strip("-").lower()
    return slug or "synthesis"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_new(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise SystemExit(f"Refusing to overwrite {path}. Use --force.")
    path.write_text(content, encoding="utf-8")


def render_feature_ledger(target: str) -> str:
    return f"""# Feature Ledger: {target}

| Feature | Source | Evidence | User job | Metric moved | Transferable principle | Risks |
| --- | --- | --- | --- | --- | --- | --- |
"""


def render_decision_matrix(target: str) -> str:
    return f"""# Decision Matrix: {target}

| Feature | Scores | Decision | Reason | Implementation note |
| --- | --- | --- | --- | --- |

Decision values: `adopt`, `adapt`, `reject`, `defer`.
"""


def render_metrics(target: str) -> str:
    return f"""# Metrics: {target}

## Metric Card

- Target user:
- Job-to-be-done:
- Artifact being improved:
- Primary behavior to improve:
- Primary metric:
- Direction:
- Guard metric:
- Anti-metric:
- Minimum meaningful delta:
- Measurement method:

## Judgement Questions

- Which metric best represents the user job?
- Which guard prevents gaming?
- What minimum delta is worth keeping?
"""


def render_handoff(target: str) -> str:
    return f"""# Handoff: {target}

## Recommendation

TBD

## Adopt

- TBD

## Adapt

- TBD

## Reject

- TBD

## Defer

- TBD

## Next Skill

- `impl-plan`, `autoresearch-plan`, `self-improve`, `gap-analysis`, or `functional-ui`
"""


def main() -> int:
    args = parse_args()
    root = Path(args.directory).resolve() / slugify(args.name)
    root.mkdir(parents=True, exist_ok=True)

    created_at = now_iso()
    sources = [
        {"type": "source", "source": source, "target": args.target, "created_at": created_at}
        for source in args.source
    ]
    sources_path = root / "sources.jsonl"
    if sources_path.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite {sources_path}. Use --force.")
    with sources_path.open("w", encoding="utf-8") as handle:
        for source in sources:
            handle.write(json.dumps(source, sort_keys=True) + "\n")

    write_new(root / "feature-ledger.md", render_feature_ledger(args.target), args.force)
    write_new(root / "decision-matrix.md", render_decision_matrix(args.target), args.force)
    write_new(root / "metrics.md", render_metrics(args.target), args.force)
    write_new(root / "handoff.md", render_handoff(args.target), args.force)

    print(f"Created best-of-worlds synthesis workspace in {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
