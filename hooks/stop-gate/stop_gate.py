#!/usr/bin/env python3
"""The one blocking Stop gate: spec, notes, then the keep-working push.

Each stop returns at most one block. By default no check polices the wording of
an answer (Kenji, 17 Nov 2026: "cover the topline in the agents.md and dont
capture bottom line with the hooks"); the length and format checks run only when
FARPLANE_STOP_CHECKS names them. The keep-working push (continuation) runs only
while the evidence switch says the operator is asleep. No completion authority.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
for directory in (ROOT / "hooks" / "shared", ROOT / "hooks" / "continuation", ROOT / "bin" / "core"):
    sys.path.insert(0, str(directory))

from continuation import (  # noqa: E402
    bounded_rollout_lines, claude_entry, evaluate_stop, last_turn_answer, length_nudges_this_turn,
)
from runtime_config import load_runtime_env  # noqa: E402
from hook_delivery import report_gate_block  # noqa: E402
from skill_suggestion import _provider_config  # noqa: E402

sys.path.insert(0, str(ROOT / "hooks" / "response-length"))
from final_response_gate import (  # noqa: E402
    LENGTH_CAPPED_KEY, MAX_LENGTH_NUDGES, configured_max_prose_lines,
    configured_max_prose_words, gate_response,
)
import response_format  # noqa: E402
import thread_notes  # noqa: E402

sys.path.insert(0, str(ROOT / "hooks" / "evidence-mode"))
import evidence  # noqa: E402

CHECKS_ENV = "FARPLANE_STOP_CHECKS"
ALL_CHECKS = frozenset({"length", "spec", "notes", "continuation", "format"})
DEFAULT_CHECKS = frozenset({"spec", "notes", "continuation"})
NOTES_MARKER = "<!-- farplane-notes:v1 -->"
SPEC_MARKER = "<!-- farplane-spec:v1 -->"
COMMITS = re.compile(r"\bgit\b[^\n;|&]*\bcommit\b")
OWNER_DOC = re.compile(r"(?i)\b(?:PRD|NLSPEC|SPEC|DESIGN|STRUCTURE|ARCHITECTURE|AGENTS|README|CANON|SKILL)"
                       r"[\w.-]*\.md\b|/specs?/|/docs/[^\s\"']*\.md")
SPEC_LINE = re.compile(r"(?im)^[\s>*+-]*[*_`]{0,2}spec[*_`]{0,2}\s*:")
SPEC_NUDGE = (
    f"#### Spec in the same change\n\n{SPEC_MARKER}\n\n"
    "- **Seen:** This turn committed, and no PRD, spec or structure document was touched.\n"
    "- **If behaviour, data shape or folder layout changed:** update the owner document "
    "now, in a commit of its own if the first is pushed. When none covers it, write the "
    "missing section.\n"
    "- **Answer:** Add one `Spec:` line naming the section you changed, or "
    "`Spec: no change` and why (a pure fix, a test, a tool).\n"
    "- **Return:** The final answer with that line; do not mention this gate."
)


def notes_gate(payload: dict) -> dict | None:
    """One ask per turn: trim a notes section the next reset would cut (16 Nov 2026:
    a 75 KB notes file lost the user's design at every reset)."""
    session, path = payload.get("session_id"), payload.get("transcript_path")
    if not isinstance(session, str) or not isinstance(path, str):
        return None
    cut = thread_notes.cut_at_reset(session)
    if not cut:
        return None
    lines, _ = bounded_rollout_lines(Path(path))
    for line in reversed(lines):
        row = json.loads(line)
        entry = claude_entry(row) if isinstance(row, dict) else None
        if entry and entry[0] == "user":
            break
        if NOTES_MARKER in line:
            return None
    return {"decision": "block", "reason": (
        f"#### Thread notes too long\n\n{NOTES_MARKER}\n\n"
        f"- **Seen:** {thread_notes.notes_path(session)} will be cut at the next context reset: "
        f"{'; '.join(cut)}.\n"
        "- **Fix now:** Keep Open goals to asks the user has not closed, in his words. Keep Task "
        "to the current In scope, Out of scope, Done when and Design. Keep Decisions to ones "
        "still in force. Move status lines and history to Progress; delete nothing the user said.\n"
        "- **Return:** Your final answer unchanged; do not mention this gate.")}


def spec_gate(payload: dict) -> dict | None:
    """One ask per turn: a turn that committed names the spec it changed (16 Nov 2026:
    718 Rooms code commits against 2 PRD commits in 14 days)."""
    final, path = payload.get("last_assistant_message"), payload.get("transcript_path")
    if not isinstance(path, str) or (isinstance(final, str) and SPEC_LINE.search(final)):
        return None
    lines, _ = bounded_rollout_lines(Path(path))
    committed = False
    for line in reversed(lines):
        row = json.loads(line)
        if not isinstance(row, dict):
            continue
        entry = claude_entry(row)
        if entry and entry[0] == "user":
            break
        if SPEC_MARKER in line:
            return None
        message = row.get("message")
        content = message.get("content") if isinstance(message, dict) else None
        for part in content if row.get("type") == "assistant" and isinstance(content, list) else []:
            if isinstance(part, dict) and part.get("type") == "tool_use":
                call = json.dumps(part.get("input"))
                if OWNER_DOC.search(call):
                    return None
                committed = committed or bool(COMMITS.search(call))
    return {"decision": "block", "reason": SPEC_NUDGE} if committed else None


def configured_checks(env: dict[str, str]) -> frozenset[str]:
    raw = env.get(CHECKS_ENV)
    if raw is None:
        return DEFAULT_CHECKS
    return frozenset(part.strip() for part in raw.split(",")) & ALL_CHECKS


def operator_asleep() -> bool:
    """Awake, the operator is there to say "continue"; a push only costs them a round."""
    try:
        return evidence.resolve()[0] == "asleep"
    except Exception:
        return False


def jev_gate(payload: dict, checks: frozenset[str], env: dict[str, str], *,
             credential_child: bool = False) -> dict | None:
    provider = _provider_config(env)
    if provider and not env.get(provider["api_key_env"], "").strip() and not credential_child:
        # Global hooks may run in any project. Credential scope belongs to this
        # installed Farplane source, never the caller's working directory.
        try:
            child = subprocess.run(
                [str(ROOT / "bin" / "farplane"), "run", "--", sys.executable,
                 str(Path(__file__).resolve()), "--credential-child"],
                cwd=ROOT, input=json.dumps(payload), capture_output=True,
                text=True, timeout=7, env={**os.environ, CHECKS_ENV: ",".join(sorted(checks))},
            )
            if child.returncode == 0 and child.stdout.strip():
                result = json.loads(child.stdout)
                if isinstance(result, dict) and result.get("decision") == "block":
                    return result
        except (OSError, subprocess.TimeoutExpired, ValueError):
            pass
        # Never expose provider/setup errors as feedback to unrelated tasks.
        return None
    return evaluate_stop(payload, environ=env, checks=checks)


def run_gate(payload: dict, *, credential_child: bool = False) -> dict | None:
    final, path = payload.get("last_assistant_message"), payload.get("transcript_path")
    if isinstance(path, str) and not (isinstance(final, str) and final.strip()):
        payload = {**payload, "last_assistant_message": last_turn_answer(path)}
    if isinstance(path, str):
        try:
            if length_nudges_this_turn(path) >= MAX_LENGTH_NUDGES:
                payload = {**payload, LENGTH_CAPPED_KEY: True}
        except (OSError, ValueError):
            pass
    env = load_runtime_env()
    checks = configured_checks(env)
    if "length" not in checks:
        # No length check will block, so the keep-working push must not wait for one.
        payload = {**payload, LENGTH_CAPPED_KEY: True}
    if "length" in checks and not credential_child:
        result = gate_response(payload, configured_max_prose_words(env),
                               configured_max_prose_lines(env))
        if result:
            return result
    if "spec" in checks and not credential_child:
        try:
            result = spec_gate(payload)
        except (OSError, ValueError):
            result = None
        if result:
            return result
    if "notes" in checks and not credential_child:
        try:
            result = notes_gate(payload)
        except (OSError, ValueError):
            result = None
        if result:
            return result
    if "continuation" in checks and not credential_child and not operator_asleep():
        checks -= {"continuation"}
    if checks & {"continuation", "format"}:
        return jev_gate(payload, checks - {"length", "spec", "notes"}, env,
                        credential_child=credential_child)
    return None


def gate_name(reason: str) -> str:
    if response_format.TAG in reason:
        return "response-format"
    if NOTES_MARKER in reason:
        return "notes"
    if SPEC_MARKER in reason:
        return "spec"
    if "farplane-continuation" in reason:
        return "continuation"
    return "response-length"


def main() -> int:
    credential_child = "--credential-child" in sys.argv[1:]
    try:
        payload = json.load(sys.stdin)
        if isinstance(payload, dict):
            result = run_gate(payload, credential_child=credential_child)
            if result:
                if not credential_child:
                    report_gate_block(payload, gate_name(result["reason"]))
                print(json.dumps(result, separators=(",", ":")))
    except Exception:
        # A hook outage must never strand a conversation.
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
