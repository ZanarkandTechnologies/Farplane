"""Response-format check: Jev picks the answer's shape, then scores that shape's gaps.

Shapes mirror the Output Formatting templates in runtimes/AGENTS.md.
Every shape also gets the reader gaps (`reader_check.py`) and a deterministic
relative-path check. Proof is deterministic: a completed change that changed
files and cites nothing gets one proof nudge; any citation means the agent did
not forget, except that a new feature a person would watch needs a video or
`Unverified:`. Proof keeps its own nudge after a format nudge is spent.
"""
from __future__ import annotations

from pathlib import Path
import re
import sys
from typing import Mapping

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "bin" / "core"))
from farplane_response import measure_response  # noqa: E402

GAP_THRESHOLD = 0.6
MAX_GAPS = 2
# Answers, proposals, decisions and blockers stay short; reports of finished or
# running work keep the full length budget. Tables, fenced blocks and labelled
# lines (Before/After/Example/Verified...) don't count.
SHORT_ANSWER_WORDS = 180
SHORT_SHAPES = {"simple_answer", "proposed_change", "decision_needed", "blocked"}
TAG = "<!-- farplane-response-format:v1 -->"

# Each shape names the AGENTS.md template heading it mirrors; a test keeps them in step.
SHAPES: dict[str, dict[str, object]] = {
    "simple_answer": {
        "skeleton": '**<The answer in one plain sentence.>**\n\n<Supporting detail: bullets, a table, or a diagram, whichever fits.>',
        "template": "Default shape",
        "description": "Answers a question, explains something, reviews, or reports findings; a one-line suggested fix or a short list of next steps after the answer still belongs here.",
        "gaps": ["conclusion_first"],
    },
    "proposed_change": {
        "skeleton": '**<What will change, in one plain sentence.>**\n\n> **Before:** <how it behaves now>\n>\n> **After:** <how it will behave>\n>\n> **Example:** <one concrete case>\n\n- **Proof planned:** <how it will be checked>',
        "template": "Proposed change",
        "description": "Proposes a design, plan, or change for the user to approve; nothing has been changed yet (files_changed is false).",
        "gaps": ["before_after_example", "proof_planned"],
    },
    "completed_change": {
        "skeleton": '### <Change name>\n\n**<Worked | Partial | Did not work>: <what works now, in plain words>.**\n\n> **Before:** <old behaviour>\n>\n> **After:** <new behaviour>\n>\n> **Example:** <one concrete case>\n\n- **Verified:** <check and result> (or **Unverified:** <why>)\n- **Limit:** <what remains, or the one thing the user must do>',
        "template": "Completed change",
        "description": "Reports changes the agent made in this turn, however small (files_changed is true).",
        "gaps": ["before_after_example"],
    },
    "blocked": {
        "skeleton": '**Partial: <what works>, but <what is blocked>.**\n\n- **Blocker:** <what stops it>\n- **Evidence:** <what shows it>\n- **Recovery:** <the next step and who takes it>',
        "template": "Blocked work",
        "description": "Reports that requested work could not be finished because something blocks it.",
        "gaps": ["blocker_recovery"],
    },
    "decision_needed": {
        "skeleton": '**Recommendation: <option>, because <reason>.**\n\n- **Choice needed:** <the exact choice>\n- **Consequence:** <what each option changes>\n- **Default:** <what happens if the user does not answer>',
        "template": "Default shape",
        "description": "Asks the user to choose between options before work continues.",
        "gaps": ["decision_choice"],
    },
    "progress": {
        "skeleton": '**<Where it stands, in plain words.>**\n\n- **Goal:** <the outcome the user asked for>\n- **Progress:** <done so far; what is running now>\n- **Next:** <next step and when it lands>',
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
VIDEO_SHAPES = {"completed_change", "progress"}
# Gaps without a "question" are not scored by Jev: the reader check or a
# deterministic rule raises them.
GAPS: dict[str, dict[str, str]] = {
    "unanswered": {
        "fix": "Answer what the user's latest message asked in the first lines. If work is still running, answer what you can now, then say what you are waiting for and when it lands.",
    },
    "cold_read": {
        "fix": "Lead with the overall state in plain words: what works, what does not, and the one thing the user must do. Drop internal terms and fix history.",
    },
    "plain_names": {
        "fix": "Say in a few words what each name the user did not use is (ticket or session codes, commit hashes, branches, internal tools, files), or drop it.",
    },
    "one_name": {
        "fix": "Give each thing one name and keep it throughout; replace the synonyms that make one part read as several.",
    },
    "context_line": {
        "fix": "Open with one sentence, **Context:** You asked …; I …, reminding the user what they asked and what this thread did, because they may come back hours later.",
    },
    "absolute_paths": {
        "fix": "Name every file by its absolute path (for example /Users/…/file.md), in links and in text, so it opens from any folder or a phone. Write the path exactly as it is, spaces included, [a](/Users/me/My Docs/a.png); never %20 or angle brackets.",
    },
    "short_answer": {
        "fix": "Cut the prose to about 150 words in 80% ASD-STE100: the answer or decision in the first sentence, one fact per sentence, active voice, no restated question, no recap of earlier turns. Keep labelled lines and tables.",
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
    "proposal_gain": {
        "fix": "Title each proposed next step by its gain, not its work: what it unlocks, the metric it moves and by about how much, or the time or money it saves (\"Exports keep every valid row: 0 lost rows, was 12%\", not \"Add blank-record handling\"); then one line on the work.",
        "question": "Does the answer propose or offer next steps or options whose titles or lead words name only the work to do (\"add X\", \"build the Y feature\", \"refactor Z\") without saying what each unlocks, which metric it improves, or what it gains, so the reader cannot judge its value at a glance? Score low when there are no proposed next steps or each already leads with its gain." + _SCOPE,
    },
    "progress_ledger": {
        "fix": "Add Goal, Track, and Progress lines.",
        "question": "Does the progress update omit the goal, the current track, or what was completed and what is next?" + _SCOPE,
    },
}
PROOF_FIX = (
    "Cite the proof this turn produced: embed screenshots or video with absolute "
    "paths written as they are, spaces included (![shot](/Users/me/My Docs/a.png), "
    "never %20 or angle brackets), link artifacts, and add `Verified:` with the check and result. If a "
    "check you can run is missing, run it now; use `Unverified:` only for proof "
    "that needs the user, hardware, or spend over the cap, and say which."
)

VIDEO_FIX = (
    "Record the new feature working and embed or link the video (.mp4, .mov or "
    ".webm) by absolute path, spaces included, never %20. If you cannot record it, add `Unverified:` saying "
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

# A relative file link target, or a backticked relative path with an extension.
# `./run.sh` and `../x` read as commands to run, not files to open. An absolute
# target is written as it is, spaces included: the Claude app reads `%20` and
# angle brackets literally, so a local target with either doesn't open (unless it's
# quoted in a code span as an example).
_ENCODED_PATH = re.compile(r"\]\((?:<[/~]|[/~][^)]*%20)[^)]*\)")
_CODE_SPAN = re.compile(r"`[^`\n]*`")
_RELATIVE_PATH = re.compile(
    r"\]\((?!https?:|mailto:|file:|#|/|~|<[/~])[^)\s]+\)"
    r"|`(?![/~]|\.\.?/)[\w.-]+(?:/[\w.-]+)+\.\w{1,6}(?::\d+)?`"
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


_BEFORE = re.compile(r"(?i)\bbefore\b\**\s*[:|]")
_AFTER = re.compile(r"(?i)\b(?:after|now)\b\**\s*[:|]")
BEFORE_AFTER_MIN_WORDS = 40


def has_before_after(final: str) -> bool:
    return bool(_BEFORE.search(final) and _AFTER.search(final))


def needs_before_after(shape: str, *, files_changed: bool, final: str) -> bool:
    """Any answer reporting or proposing a change shows Before / After, unless tiny."""
    if not (files_changed or shape == "proposed_change"):
        return False
    return len(final.split()) >= BEFORE_AFTER_MIN_WORDS and not has_before_after(final)


_CONTEXT_LINE = re.compile(r"^\W{0,6}context\W{0,4}:", re.IGNORECASE)


def has_context_line(final: str) -> bool:
    """A Context: line among the first three non-blank lines, under any heading."""
    lines = [line for line in final.splitlines() if line.strip() and not line.lstrip().startswith("#")]
    return any(_CONTEXT_LINE.match(line.strip()) for line in lines[:3])


def has_citation(final: str) -> bool:
    return bool(_CITATION.search(final))


def has_relative_path(final: str) -> bool:
    return bool(_RELATIVE_PATH.search(final) or _ENCODED_PATH.search(_CODE_SPAN.sub("", final)))


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
        if "question" in spec:
            asked[f"gap::{name}"] = {"type": "noul", "instructions": spec["question"]}
    asked["visible_feature"] = {"type": "noul", "instructions": FEATURE_QUESTION}
    return asked


def select_gaps(answers: Mapping[str, object], *, files_changed: bool, final: str,
                reader_gaps: list[str] | None = None,
                proof_only: bool = False, long_turn: bool = False) -> tuple[str, list[str]]:
    """Return the chosen shape and at most MAX_GAPS gaps, most important first.

    Order: proof, then the reader's gaps, absolute paths, and the shape's scored gaps.
    proof_only keeps just a proof gap: proof has its own nudge, so an earlier
    format nudge cannot use up the request for a video.
    """
    shape = str(_value(answers.get("shape"), "choice"))
    if shape not in SHAPES:
        raise ValueError(f"unknown shape: {shape}")
    scored = []
    for name in SHAPES[shape]["gaps"]:  # type: ignore[union-attr]
        score = _score(answers.get(f"gap::{name}"))
        if score >= GAP_THRESHOLD:
            scored.append((score, name))
    ranked = [name for _, name in sorted(scored, reverse=True)]
    if needs_before_after(shape, files_changed=files_changed, final=final):
        # A fixed rule, not a score: a change always shows its Before / After,
        # and it outranks the progress ledger.
        ranked = ["before_after_example",
                  *(n for n in ranked if n not in ("before_after_example", "progress_ledger"))]
    # Next steps can close any shape, so their gain line is scored for every shape.
    if "proposal_gain" not in ranked and _score(answers.get("gap::proposal_gain")) >= GAP_THRESHOLD:
        ranked.append("proposal_gain")
    too_long = shape in SHORT_SHAPES and measure_response(final).prose_words > SHORT_ANSWER_WORDS
    gaps = [*(["context_line"] if long_turn and not has_context_line(final) else []),
            *(["short_answer"] if too_long else []),
            *(reader_gaps or []),
            *(["absolute_paths"] if has_relative_path(final) else []),
            *ranked]
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


CONTEXT_SKELETON = "**Context:** You asked <the request>; I <what this thread did>."


def skeleton(shape: str | None, *, long_turn: bool = False) -> str:
    """The fixed template for one reply shape, with the Context line on long turns."""
    if shape not in SHAPES:
        return ""
    lines = str(SHAPES[shape]["skeleton"]).split("\n")
    if long_turn:
        # Status stays first; the reminder sits right under it.
        heading = 2 if lines[0].startswith("#") else 0
        lines[heading + 1:heading + 1] = ["", CONTEXT_SKELETON]
    return "\n".join(lines)


# Gaps that mean the answer's structure is wrong; only these carry the shape
# template. Every other gap is an in-place edit, so the answer keeps its form.
STRUCTURAL_GAPS = {"before_after_example", "proof_planned", "blocker_recovery",
                   "decision_choice", "progress_ledger"}


def feedback(gaps: list[str], shape: str | None = None, *, long_turn: bool = False,
             names: list[str] | None = None) -> str:
    fixes = {"proof": PROOF_FIX, "video_proof": VIDEO_FIX}
    if names:
        fixes["plain_names"] = (GAPS["plain_names"]["fix"]
                                + " Here: " + ", ".join(f"“{name}”" for name in names) + ".")
    lines = "\n".join(
        f"- **Add:** {fixes.get(name) or GAPS[name]['fix']}" for name in gaps
    )
    structural = any(name in STRUCTURAL_GAPS for name in gaps)
    template = skeleton(shape, long_turn=long_turn) if structural else ""
    shown = (f"Use this order ({SHAPES[shape]['template']}); it sets the order, not "
             f"the form, and keeps only the parts the dialogue supports:\n\n````markdown\n{template}\n````\n\n"
             if template else "")
    return (
        f"#### Response format\n\n{TAG}\n\n{shown}{lines}\n"
        "- **Keep:** The answer's facts and proof, and its tables, diagrams, code "
        "blocks and images as they are; change only what the lines above ask, fill "
        "only what the dialogue already supports, and add no empty headings.\n"
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
