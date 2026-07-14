#!/usr/bin/env python3
"""Compile bounded Phone Chaser review-call metadata from a Farplane ticket."""

from __future__ import annotations

import argparse
import json
import re
import secrets
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MAX_FIELD_CHARS = 700


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticket", required=True, help="Path to tickets/TASK-XXXX/ticket.md.")
    parser.add_argument("--artifact", action="append", default=[], help="Relevant artifact or evidence file.")
    parser.add_argument("--review-id", help="Opaque gateway review id from review-bind.")
    parser.add_argument("--webhook-url", help="Gateway review relay URL.")
    parser.add_argument("--capability", help="Gateway review capability for this one review.")
    parser.add_argument("--decision-question", help="Question the recipient should answer.")
    parser.add_argument("--approve-effect", help="What approve permits.")
    parser.add_argument("--revision-example", action="append", default=[], help="Concrete acceptable revision.")
    parser.add_argument("--limit", action="append", default=[], help="Boundary the call must not cross.")
    parser.add_argument("--message", help="Short spoken reminder override.")
    parser.add_argument("--dry-run", action="store_true", help="Allow placeholder callback values for local proof.")
    return parser.parse_args()


def read_text(path_value: str) -> str:
    path = Path(path_value)
    if not path.is_absolute():
        path = ROOT / path
    return path.read_text(encoding="utf-8")


def frontmatter_value(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", text, flags=re.MULTILINE)
    return strip_quotes(match.group(1).strip()) if match else ""


def section(text: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\s*\n(?P<body>.*?)(?=^## |\Z)"
    match = re.search(pattern, text, flags=re.MULTILINE | re.DOTALL)
    return clean(match.group("body")) if match else ""


def clean(value: str, limit: int = MAX_FIELD_CHARS) -> str:
    without_fences = re.sub(r"```.*?```", " ", value, flags=re.DOTALL)
    collapsed = " ".join(without_fences.replace("- [x]", "").replace("- [ ]", "").split())
    return collapsed[:limit].rstrip()


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] in {'"', "'"} and value[-1] == value[0]:
        return value[1:-1]
    return value


def summarize_artifacts(paths: list[str]) -> str:
    snippets = []
    for path_value in paths:
        text = read_text(path_value)
        title = frontmatter_value(text, "title") or first_heading(text) or Path(path_value).name
        snippets.append(f"{title}: {clean(text, 450)}")
    return clean(" ".join(snippets), 900)


def first_heading(text: str) -> str:
    match = re.search(r"^#\s+(.+?)\s*$", text, flags=re.MULTILINE)
    return clean(match.group(1), 120) if match else ""


def require_callback(args: argparse.Namespace) -> tuple[str, str, str]:
    if args.review_id and args.webhook_url and args.capability:
        return args.review_id.strip(), args.webhook_url.strip(), args.capability.strip()
    if args.dry_run:
        return "dry-run-review", "http://127.0.0.1:8789/phone-chaser/review", "dry-run-capability"
    raise SystemExit("review-id, webhook-url, and capability are required unless --dry-run is set")


def main() -> int:
    args = parse_args()
    ticket_text = read_text(args.ticket)
    review_id, webhook_url, capability = require_callback(args)
    title = frontmatter_value(ticket_text, "title") or first_heading(ticket_text)
    summary = section(ticket_text, "Summary")
    scope = section(ticket_text, "Scope")
    done = section(ticket_text, "Done / Proof") or section(ticket_text, "Done")
    state = section(ticket_text, "State")
    artifact_summary = summarize_artifacts(args.artifact)
    decision_question = args.decision_question or "Do you approve, want revisions, or reject this artifact?"
    approve_effect = args.approve_effect or "Approval returns the decision to the originating Codex task only; it does not publish or mutate accounts."
    revision_examples = args.revision_example or [
        "Ask for a clearer lead.",
        "Ask for a narrower claim.",
        "Ask to keep a limitation more visible.",
    ]
    limits = args.limit or [
        "No publication, outreach, spend, deployment, credential use, or account mutation.",
        "The call can only submit approve, revise, or reject for this review.",
    ]

    context = {
        "title": title,
        "objective": clean(summary or scope),
        "produced": clean(artifact_summary or done),
        "why_it_matters": clean(state or summary),
        "decision_question": clean(decision_question, 260),
        "approve_effect": clean(approve_effect, 300),
        "revision_examples": [clean(item, 180) for item in revision_examples],
        "limits": [clean(item, 220) for item in limits],
    }
    message = args.message or (
        f"Kenji. This is Farplane. {title} is waiting for review. "
        "Say approve, revise, or reject, plus a short reason."
    )
    metadata = {
        "message": clean(message, 420),
        "review_context": context,
        "review_callback": {
            "review_id": review_id,
            "webhook_url": webhook_url,
            "capability": capability,
        },
        "call_id": f"phone-review-{secrets.token_urlsafe(8)}",
    }
    print(json.dumps(metadata, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
