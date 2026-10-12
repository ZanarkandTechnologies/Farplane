"""Response-format check: Jev picks the answer's shape, then scores that shape's gaps.

Shapes mirror the Output Formatting templates in runtimes/AGENTS.md.
Every shape is also asked whether a cold reader gets the overall state.
Proof is deterministic: a completed change that changed files and cites
nothing gets one proof nudge; any citation means the agent did not forget,
except that a new feature a person would watch needs a video or `Unverified:`.
Proof keeps its own nudge after the one format nudge per turn is spent.
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
# Asked of every shape: an answer can follow its template and still lose the reader.
UNIVERSAL_GAPS = ["cold_read"]
VIDEO_SHAPES = {"completed_change", "progress"}
GAPS: dict[str, dict[str, str]] = {
    "cold_read": {
        "fix": "Lead with the overall state in plain words: what works, what does not, and the one thing the user must do. Drop internal terms and fix history.",
        "question": (
            "Would someone who saw only the user's latest message be lost reading this "
            "answer: unable to tell where their request now stands, what works and what "
            "does not, or what they must do? Score high when the answer narrates the "
            "latest fix, bug, or step instead of the overall state of what the user asked "
            "for, or leans on terms coined during the work (ticket or track names, "
            "nicknames for bugs, fixes, or internal parts) that the user never used. "
            "Score low when the answer states the result of what the user asked, even "
            "tersely; names of the user's own code, files, and commands are not internal "
            "terms, and an answer with nothing for the user to do need not say so."
        ),
    },
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
    "paths, link artifacts, and add `Verified:` with the check and result. If a "
    "check you can run is missing, run it now; use `Unverified:` only for proof "
    "that needs the user, hardware, or spend over the cap, and say which."
)

VIDEO_FIX = (
    "Record the new feature working and embed or link the video (.mp4, .mov or "
    ".webm) by absolute path. If you cannot record it, add `Unverified:` saying "
    "why there is no video."
)
FEATURE_QUESTION = (
    "Did the agent in this turn add a new feature or multi-step workflow, or change "
    "how a product behaves for the person using it, so that they would want to watch "
    "it working: a new screen, UI flow, interactive page, or game; an app's agents, "
    "characters, or workers acting differently; or robot or simulation behaviour? "
    "Judge what the user would see, not which files changed: launch code that changes "
    "how an app's workers behave counts. Score low for bug fixes and layout or styling "
    "tweaks that tests or screenshots prove, and for changes with nothing running to "
    "watch: config values, refactors, docs, tests, build scripts, internal libraries."
)

_VIDEO = re.compile(r"\.(?:mp4|mov|webm)\b", re.IGNORECASE)
_UNVERIFIED = re.compile(r"\bunverified[*_]{0,2}\s*:", re.IGNORECASE)
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


def names_proof(feedback_text: str) -> bool:
    """True when earlier gate feedback already asked for proof or a video."""
    return PROOF_FIX in feedback_text or VIDEO_FIX in feedback_text


def has_video_proof(final: str) -> bool:
    return bool(_VIDEO.search(final) or _UNVERIFIED.search(final))


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
    asked["visible_feature"] = {"type": "noul", "instructions": FEATURE_QUESTION}
    return asked


def select_gaps(answers: Mapping[str, object], *, files_changed: bool,
                final: str, proof_only: bool = False) -> tuple[str, list[str]]:
    """Return the chosen shape and at most MAX_GAPS gaps for that shape plus the universal ones.

    proof_only keeps just a proof gap: proof has its own once-per-turn nudge, so an
    earlier format nudge cannot use up the request for a video.
    """
    shape = str(_value(answers.get("shape"), "choice"))
    if shape not in SHAPES:
        raise ValueError(f"unknown shape: {shape}")
    scored = []
    for name in [*SHAPES[shape]["gaps"], *UNIVERSAL_GAPS]:  # type: ignore[misc]
        score = _score(answers.get(f"gap::{name}"))
        if score >= GAP_THRESHOLD:
            scored.append((score, name))
    gaps = [name for _, name in sorted(scored, reverse=True)]
    # A run's last progress update can report a new feature too. The video fix
    # also covers citing proof, so it replaces the generic proof nudge.
    if (files_changed and shape in VIDEO_SHAPES and not has_video_proof(final)
            and _score(answers.get("visible_feature")) >= GAP_THRESHOLD):
        gaps.insert(0, "video_proof")
    elif shape == "completed_change" and files_changed and not has_citation(final):
        gaps.insert(0, "proof")
    if proof_only:
        gaps = [name for name in gaps if name in ("proof", "video_proof")]
    return shape, gaps[:MAX_GAPS]


def feedback(gaps: list[str]) -> str:
    fixes = {"proof": PROOF_FIX, "video_proof": VIDEO_FIX}
    lines = "\n".join(
        f"- **Add:** {fixes.get(name) or GAPS[name]['fix']}" for name in gaps
    )
    return (
        f"#### Response format\n\n{TAG}\n\n{lines}\n"
        "- **Keep:** The answer's facts and proof; fill only what the dialogue "
        "already supports and add no empty headings.\n"
        "- **Return:** The revised final answer only; do not mention this gate."
    )


def _score(answer: object) -> float:
    score = _value(answer, "noul")
    if isinstance(score, (int, float)) and not isinstance(score, bool):
        return float(score)
    return 0.0


def _value(answer: object, field: str) -> object:
    if isinstance(answer, Mapping):
        return answer.get(field)
    return getattr(answer, field, None)
