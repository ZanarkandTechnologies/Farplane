"""Reader check: Claude Haiku reads the whole final answer the way the user will.

Jev scores template sections but cannot tell when a busy reader is lost. Haiku
returns six facts and fixed rules turn them into at most one gap. Missing
credentials, timeouts and bad replies return None, so the stop is never held up.
Haiku runs through `claude -p` on the Claude subscription, never a paid API key.

Haiku over-reports, so fixed rules check its claims: a bold opening line counts
as the status, and a name the user used, a number, path, link or a name the
answer explains is not unexplained. "Unanswered" also needs Jev's agreement
(`response_format.select_gaps`).
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Mapping

MODEL_ENV = "FARPLANE_READER_MODEL"
DEFAULT_MODEL = "haiku"
# A bare child: no tools, MCP, skills, settings or hooks (a child Stop hook would loop).
CLAUDE_ARGS = ("-p", "--output-format", "json", "--no-session-persistence", "--tools", "",
               "--strict-mcp-config", "--disable-slash-commands", "--setting-sources", "",
               "--settings", '{"disableAllHooks":true}')
# Removed so the child signs in with the subscription, not a paid key.
PAID_KEYS = ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "CLAUDE_CODE_USE_BEDROCK",
             "CLAUDE_CODE_USE_VERTEX")
TIMEOUT = 4.0
MAX_REQUEST = 3000
MAX_FINAL = 12000
MIN_NAMES = 2
MAX_NAMES_SHOWN = 8

PROMPT = """You check a coding agent's final answer for a busy founder who saw only their own messages, not the agent's work.
Return JSON only:
{"answers_latest": true|false,
 "status_first": true|false,
 "process_narration": true|false,
 "unexplained_names": ["name", ...],
 "name_drift": true|false,
 "blocker": "short description" | "",
 "agent_can_clear_now": true|false}
- answers_latest: does it directly answer or report on what the latest message asked? A progress line while work is still running counts only if it also answers what can be answered now.
- status_first: do the first two lines say plainly where the request stands?
- process_narration: is most of it the agent's process or latest fix rather than the result?
- unexplained_names: the internal names the answer's main point depends on that the user did not use and would not know, left unexplained: ticket or session codes, commit hashes, branch names, internal tool or model names, metric jargon. Leave out file paths and links, commands to run, names from the user's latest or earlier messages, names the answer explains in a few words, public product names and common tech terms (SSD, CI, API, FiveM), and everyday words, including a part of the work described in plain words (the parser, the upload route). Usually empty.
- name_drift: does the answer call one thing by two or more different names (the matcher, then the retriever, then the ranker for the same part), so a reader could take them for different things? Plain pronouns and a name plus its short explanation do not count. Usually false.
- blocker: the thing the answer says stops the work or is left to do, in a few words; "" when nothing is.
- agent_can_clear_now: true only if the agent could clear that blocker itself right now with its own tools (rerun or fix a failing command or test, start a server, install a package, read a file or log, retry another way, fix a small bug it found) and nothing else must happen first. False when it needs the user (password, login, account, approval, payment, spend, a decision, a plan to approve, hardware) or is waiting on another person, session or running job."""


_EXPLAINED_AFTER = re.compile(r"^[`*_\"”’)]*\s*(?:\(|:|—|–| - |, (?:a|an|the|our|which|where|i\.e\.)\b| is\b| means\b| \()")
_LINK_TEXT = re.compile(r"\[([^\]]+)\]\(")
_NOT_A_NAME = re.compile(r"^[\W\d_]+$|/|^[-`~.]|\.\w{1,5}$|#\d+|^https?:")


def known_name(name: str, final: str, known: str) -> bool:
    """True for a name a reader can follow: the user used it, it is a number,
    path, flag, link or issue number, or the answer explains it where it appears."""
    name = name.strip().strip("`*\"'“”")
    if not name or _NOT_A_NAME.search(name) or name.lower() in known.lower():
        return True
    if any(name.lower() in text.lower() for text in _LINK_TEXT.findall(final)):
        return True
    return any(_EXPLAINED_AFTER.match(final[match.end():match.end() + 16])
               for match in re.finditer(re.escape(name), final, re.IGNORECASE))


def clip_request(text: str) -> str:
    """Keep the opening and the end of a long message: a long brief asks at the end."""
    if len(text) <= MAX_REQUEST:
        return text
    return text[:MAX_REQUEST // 3] + "\n[…]\n" + text[-2 * MAX_REQUEST // 3:]


def opens_with_status(final: str) -> bool:
    """A bold first line (after any heading or Context line) states the status."""
    for line in final.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or re.match(r"^\W{0,6}context\W{0,4}:", line, re.I):
            continue
        return line.startswith("**")
    return False


def claude_binary(environ: Mapping[str, str]) -> str | None:
    found = shutil.which("claude", path=environ.get("PATH"))
    local = Path(environ.get("HOME", str(Path.home()))) / ".local/bin/claude"
    return found or (str(local) if local.exists() else None)


def judge(latest_user_request: str, final: str, *, environ: Mapping[str, str],
          timeout: float = TIMEOUT, known: str = "") -> dict | None:
    binary = claude_binary(environ)
    if not binary:
        return None
    message = ((f"EARLIER USER MESSAGES (their names are known):\n{known[-MAX_REQUEST:]}\n\n"
                if known.strip() else "")
               + f"LATEST USER MESSAGE:\n{clip_request(latest_user_request)}"
               f"\n\nFINAL ANSWER:\n{final[:MAX_FINAL]}")
    env = {key: value for key, value in environ.items() if key not in PAID_KEYS}
    env["CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC"] = "1"
    try:
        done = subprocess.run(
            [binary, *CLAUDE_ARGS, "--model", environ.get(MODEL_ENV) or DEFAULT_MODEL,
             "--system-prompt", PROMPT],
            input=message, capture_output=True, text=True, timeout=timeout, env=env,
            cwd=env.get("HOME") or None)
        reply = json.loads(done.stdout)
        if reply.get("is_error"):
            return None
        facts = json.loads(re.search(r"\{.*\}", reply["result"], re.S).group(0))
    except Exception:
        return None
    fields = ("answers_latest", "status_first", "process_narration")
    names, blocker = facts.get("unexplained_names"), facts.get("blocker", "")
    clear = facts.get("agent_can_clear_now", False)
    if (not all(isinstance(facts.get(name), bool) for name in fields)
            or not isinstance(names, list) or not isinstance(blocker, str)
            or not isinstance(clear, bool)):
        return None
    names = [str(name) for name in names
             if not known_name(str(name), final, f"{latest_user_request}\n{known}")]
    # Haiku over-reports single names; two or more means the reader is lost.
    return {**{name: facts[name] for name in fields},
            "status_first": facts["status_first"] or opens_with_status(final),
            "unexplained_names": len(names) >= MIN_NAMES,
            # Quoted back in the nudge so the agent knows which names; never logged.
            "names": [str(name)[:40] for name in names][:MAX_NAMES_SHOWN],
            "fixable_blocker": bool(blocker.strip()) and clear,
            "name_drift": facts.get("name_drift") is True}


def gaps(facts: Mapping[str, bool] | None) -> list[str]:
    """An unanswered message outranks a buried status, then jargon, then name drift."""
    if not facts:
        return []
    if not facts["answers_latest"]:
        return ["unanswered"]
    # A buried status and unexplained names are separate fixes: naming the
    # names tells the agent exactly what to explain, "lead with the state" does not.
    found = []
    if facts["process_narration"] and not facts["status_first"]:
        found.append("cold_read")
    if facts["unexplained_names"]:
        found.append("plain_names")
    if found:
        return found
    if facts.get("name_drift"):
        return ["one_name"]
    return []
