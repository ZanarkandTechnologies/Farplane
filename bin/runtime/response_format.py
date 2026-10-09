"""Response-format check: Jev picks the answer's shape, then scores that shape's gaps.

Shapes mirror the Output Formatting templates in templates/global/AGENTS.md.
Proof is deterministic: a completed change that changed files and cites
nothing gets one proof nudge; any citation means the agent did not forget.
"""
from __future__ import annotations

import re
from typing import Mapping

GAP_THRESHOLD = 0.6
MAX_GAPS = 2
TAG = "<!-- farplane-response-format:v1 -->"

# Each shape names the AGENTS.md template heading it mirrors; a test keeps them in step.
SHAPES: dict[str, dict[str, object]] = {
    "simple_answer": {
        "template": "Default shape",
        "description": "Answers a question, explains something, reviews, or reports findings; a one-line suggested fix inside an explanation still belongs here.",
        "gaps": ["conclusion_first"],
    },
    "proposed_change": {
        "template": "Proposed change",
        "description": "Proposes a design, plan, or change for the user to approve; nothing has been changed yet (files_changed is false).",
        "gaps": ["before_after_example", "proof_planned"],
    },
    "completed_change": {
        "template": "Completed change",
        "description": "Reports changes the agent made in this turn, however small (files_changed is true).",
        "gaps": ["before_after_example"],
    },
    "blocked": {
        "template": "Blocked work",
        "description": "Reports that requested work could not be finished because something blocks it.",
        "gaps": ["blocker_recovery"],
    },
    "decision_needed": {
        "template": "Default shape",
        "description": "Asks the user to choose between options before work continues.",
        "gaps": ["decision_choice"],
    },
    "progress": {
        "template": "Long-horizon progress",
        "description": "A mid-run status update on long multi-step work that continues afterwards.",
        "gaps": ["progress_ledger"],
    },
}

_SCOPE = (
    " Score high only when the section is missing or buried, adding it would make "
    "the answer materially easier to use or more complete, and the dialogue already "
    "holds the content to fill it. Score low when it is present, unnecessary for an "
    "answer this small, or would need information the agent does not have."
)
GAPS: dict[str, dict[str, str]] = {
    "conclusion_first": {
        "fix": "Lead with the conclusion in the first sentence.",
        "question": "Does the final answer bury its conclusion behind context or process narration?" + _SCOPE,
    },
    "before_after_example": {
        "fix": "Add a compact Before / After / Example blockquote for the change.",
        "question": "Does the final answer describe a behavior or design change without a clear before, after, and concrete example?" + _SCOPE,
    },
    "proof_planned": {
        "fix": "Add one line naming how the proposed change will be proved.",
        "question": "Does the proposed change omit how it will be checked or proved?" + _SCOPE,
    },
    "blocker_recovery": {
        "fix": "Name the blocker, the evidence, and the recovery path.",
        "question": "Does the blocked-work answer omit the specific blocker, its evidence, or the recovery path?" + _SCOPE,
    },
    "decision_choice": {
        "fix": "State the recommendation, the exact choice needed, and the safe default.",
        "question": "Does the answer ask for a decision without a recommendation, the exact choice, or a safe default?" + _SCOPE,
    },
    "progress_ledger": {
        "fix": "Add Goal, Track, and Progress lines.",
        "question": "Does the progress update omit the goal, the current track, or what was completed and what is next?" + _SCOPE,
    },
}
PROOF_FIX = (
    "Cite the proof this turn produced: embed screenshots or video with absolute "
    "paths, link artifacts, and add `Verified:` with the check and result. If "
    "nothing was verified, add `Unverified:` and why."
)

_CITATION = re.compile(
    r"!\[[^\]]*\]\([^)]+\)"                 # media embed
    r"|\[[^\]]+\]\([^)]+\)"                  # markdown link
    r"|https?://\S+"                         # bare URL
    r"|^ {0,3}(?:`{3,}|~{3,})"                # fenced command output or code
    r"|\b(?:verified|unverified)[*_]{0,2}\s*:",
    re.IGNORECASE | re.MULTILINE,
)
_EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit", "apply_patch"}


def has_citation(final: str) -> bool:
    return bool(_CITATION.search(final))


def is_edit_tool(name: object) -> bool:
    return name in _EDIT_TOOLS


def questions() -> dict[str, object]:
    asked: dict[str, object] = {
        "shape": {
            "type": "choice",
            "instructions": (
                "Which shape best describes the proposed final answer to the "
                "latest user request? Judge what the answer does, not its formatting."
            ),
            "criteria": {name: str(spec["description"]) for name, spec in SHAPES.items()},
        }
    }
    for name, spec in GAPS.items():
        asked[f"gap::{name}"] = {"type": "noul", "instructions": spec["question"]}
    return asked


def select_gaps(answers: Mapping[str, object], *, files_changed: bool,
                cited: bool) -> tuple[str, list[str]]:
    """Return the chosen shape and at most MAX_GAPS gap names for that shape only."""
    shape = str(_value(answers.get("shape"), "choice"))
    if shape not in SHAPES:
        raise ValueError(f"unknown shape: {shape}")
    scored = []
    for name in SHAPES[shape]["gaps"]:  # type: ignore[union-attr]
        score = _value(answers.get(f"gap::{name}"), "noul")
        if isinstance(score, (int, float)) and not isinstance(score, bool) and score >= GAP_THRESHOLD:
            scored.append((float(score), name))
    gaps = [name for _, name in sorted(scored, reverse=True)]
    if shape == "completed_change" and files_changed and not cited:
        gaps.insert(0, "proof")
    return shape, gaps[:MAX_GAPS]


def feedback(gaps: list[str]) -> str:
    lines = "\n".join(
        f"- **Add:** {PROOF_FIX if name == 'proof' else GAPS[name]['fix']}" for name in gaps
    )
    return (
        f"#### Response format\n\n{TAG}\n\n{lines}\n"
        "- **Keep:** Everything else in the answer; fill only what the dialogue "
        "already supports and add no empty headings.\n"
        "- **Return:** The revised final answer only; do not mention this gate."
    )


def _value(answer: object, field: str) -> object:
    if isinstance(answer, Mapping):
        return answer.get(field)
    return getattr(answer, field, None)
