#!/usr/bin/env python3
"""Scaffold a human-in-the-loop autoresearch session."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


FILES = [
    "autoresearch.md",
    "autoresearch.sh",
    "autoresearch.jsonl",
    "autoresearch.ideas.md",
    "feedback-request.md",
]


def slugify(value: str) -> str:
    cleaned = []
    for char in value.lower():
        if char.isalnum():
            cleaned.append(char)
        elif cleaned and cleaned[-1] != "-":
            cleaned.append("-")
    return "".join(cleaned).strip("-") or "hitl-session"


def render_md(args: argparse.Namespace) -> str:
    return f"""# HITL Autoresearch Session

## Objective

{args.goal}

## Scope

- Session name: `{args.name}`
- Artifact family: `{args.artifact_family}`
- Editable/output scope: `{args.scope}`
- Metric: `{args.metric_name}`
- Direction: `{args.direction}`
- Verify: `./autoresearch.sh`
- Guard: none unless the active agent adds a local non-destructive check
- Max iterations: {args.max_iterations}

## Human Feedback Contract

Review question:

> {args.question}

Feedback source: `feedback.json`

Expected shape:

```json
{{
  "run": 1,
  "score": 8,
  "verdict": "keep",
  "feedback": "What worked and what did not?",
  "next_instruction": "What should the next run change?"
}}
```

## Loop

1. Create one logical variant under `outputs/run-N/`.
2. Summarize the artifact and paths in `feedback-request.md`.
3. Use the `telegram-message` skill to send `feedback-request.md` when
   Telegram env vars are configured.
4. Stop for human feedback when `feedback.json` is missing.
5. Run `./autoresearch.sh` after feedback exists.
6. Keep, revise, or discard based on score, verdict, and rationale.
7. Use `next_instruction` as the next hypothesis.

## Constraints

- Do not publish, send outreach, spend money, or make external promises.
- Do not hardcode Telegram credentials.
- Keep artifacts reviewable by Kenji without extra context.
- Prefer one strong iteration over many unreviewable variants.

## Blocked Stop Condition

Stop only when the session is waiting for human feedback, Telegram credentials
are missing and the local request file is written, or the artifact cannot be
created after recording attempted paths, evidence, safe options, recommended
next action, and the one missing input.
"""


def render_runner(metric_name: str) -> str:
    return f"""#!/usr/bin/env bash
set -euo pipefail

if [[ ! -f feedback.json ]]; then
  echo "METRIC {metric_name}=0"
  echo "No feedback.json found; waiting for human feedback." >&2
  exit 2
fi

python3 - <<'PY'
import json
from pathlib import Path

data = json.loads(Path("feedback.json").read_text())
score = float(data.get("score", 0))
print("METRIC {metric_name}=" + str(score))
PY
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--name", required=True)
    parser.add_argument("--goal", required=True)
    parser.add_argument("--artifact-family", default="demo")
    parser.add_argument("--scope", default="outputs/")
    parser.add_argument("--metric-name", default="human_score")
    parser.add_argument("--direction", choices=["higher", "lower"], default="higher")
    parser.add_argument("--question", required=True)
    parser.add_argument("--max-iterations", type=int, default=5)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    root = Path(args.root) / slugify(args.name)
    root.mkdir(parents=True, exist_ok=True)
    existing = [name for name in FILES if (root / name).exists()]
    if existing and not args.force:
        raise SystemExit(
            f"Session already has files: {', '.join(existing)}. Use --force to overwrite."
        )

    (root / "outputs").mkdir(exist_ok=True)
    (root / "autoresearch.md").write_text(render_md(args), encoding="utf-8")
    runner = root / "autoresearch.sh"
    runner.write_text(render_runner(args.metric_name), encoding="utf-8")
    runner.chmod(0o755)
    (root / "autoresearch.ideas.md").write_text(
        "# Autoresearch Ideas\n\n- Use Kenji's feedback as the next hypothesis.\n",
        encoding="utf-8",
    )
    request = (
        f"# Feedback Request\n\n"
        f"Session: {args.name}\n\n"
        f"Review question: {args.question}\n\n"
        f"Create `feedback.json` after reviewing the latest artifact.\n"
    )
    (root / "feedback-request.md").write_text(request, encoding="utf-8")
    header = {
        "type": "config",
        "goal": args.goal,
        "metric_name": args.metric_name,
        "direction": args.direction,
        "scope": [args.scope],
        "verify_command": "./autoresearch.sh",
        "guard_command": None,
        "max_iterations": args.max_iterations,
        "human_feedback": True,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    (root / "autoresearch.jsonl").write_text(json.dumps(header) + "\n", encoding="utf-8")
    print(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
