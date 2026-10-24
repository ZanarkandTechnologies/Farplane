"""Reader check: Claude Haiku reads the whole final answer the way the user will.

Jev scores template sections but cannot tell when a busy reader is lost. Haiku
returns six facts and fixed rules turn them into at most one gap. Missing
credentials, timeouts and bad replies return None, so the stop is never held up.
"""
from __future__ import annotations

import json
import re
from typing import Mapping
from urllib.request import Request, urlopen

MODEL_ENV = "FARPLANE_READER_MODEL"
DEFAULT_MODEL = "anthropic/claude-haiku-5.5"
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
KEY_ENV = "OPENROUTER_API_KEY"
TIMEOUT = 2.5
MAX_REQUEST = 3000
MAX_FINAL = 12000
MIN_NAMES = 2

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
- unexplained_names: the internal names the answer's main point depends on that the user did not use and would not know, left unexplained: ticket or session codes, commit hashes, branch names, internal tool or model names, metric jargon. Leave out file paths and links, commands to run, names from the user's latest or earlier messages, names the answer explains in a few words, public product names and common tech terms (SSD, CI, API, FiveM), and everyday words. Usually empty.
- name_drift: does the answer call one thing by two or more different names (the matcher, then the retriever, then the ranker for the same part), so a reader could take them for different things? Plain pronouns and a name plus its short explanation do not count. Usually false.
- blocker: the thing the answer says stops the work or is left to do, in a few words; "" when nothing is.
- agent_can_clear_now: true only if the agent could clear that blocker itself right now with its own tools (rerun or fix a failing command or test, start a server, install a package, read a file or log, retry another way, fix a small bug it found) and nothing else must happen first. False when it needs the user (password, login, account, approval, payment, spend, a decision, a plan to approve, hardware) or is waiting on another person, session or running job."""


def judge(latest_user_request: str, final: str, *, environ: Mapping[str, str],
          timeout: float = TIMEOUT, known: str = "") -> dict | None:
    key = environ.get(KEY_ENV, "").strip()
    if not key:
        return None
    body = {
        "model": environ.get(MODEL_ENV) or DEFAULT_MODEL, "max_tokens": 300,
        "temperature": 0, "reasoning": {"enabled": False},
        "messages": [
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": (f"EARLIER USER MESSAGES (their names are known):\n{known[-MAX_REQUEST:]}\n\n"
                                         if known.strip() else "")
                                        + f"LATEST USER MESSAGE:\n{latest_user_request[:MAX_REQUEST]}"
                                        f"\n\nFINAL ANSWER:\n{final[:MAX_FINAL]}"},
        ],
    }
    request = Request(ENDPOINT, data=json.dumps(body).encode("utf-8"),
                      headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urlopen(request, timeout=timeout) as response:
            content = json.load(response)["choices"][0]["message"]["content"]
        facts = json.loads(re.search(r"\{.*\}", content, re.S).group(0))
    except Exception:
        return None
    fields = ("answers_latest", "status_first", "process_narration")
    names, blocker = facts.get("unexplained_names"), facts.get("blocker", "")
    clear = facts.get("agent_can_clear_now", False)
    if (not all(isinstance(facts.get(name), bool) for name in fields)
            or not isinstance(names, list) or not isinstance(blocker, str)
            or not isinstance(clear, bool)):
        return None
    # Haiku over-reports single names; two or more means the reader is lost.
    return {**{name: facts[name] for name in fields},
            "unexplained_names": len(names) >= MIN_NAMES,
            "fixable_blocker": bool(blocker.strip()) and clear,
            "name_drift": facts.get("name_drift") is True}


def gaps(facts: Mapping[str, bool] | None) -> list[str]:
    """An unanswered message outranks a buried status, then jargon, then name drift."""
    if not facts:
        return []
    if not facts["answers_latest"]:
        return ["unanswered"]
    lost = facts["process_narration"] or facts["unexplained_names"]
    if lost and not facts["status_first"]:
        return ["cold_read"]
    if facts["unexplained_names"]:
        return ["plain_names"]
    if facts.get("name_drift"):
        return ["one_name"]
    return []
