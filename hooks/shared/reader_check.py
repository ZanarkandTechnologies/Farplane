"""Reader check: Claude Haiku reads the whole final answer the way the user will.

Jev scores template sections but cannot tell when a busy reader is lost. Haiku
returns three facts and fixed rules turn them into at most one gap. Missing
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

PROMPT = """You check a coding agent's final answer for a busy founder who saw only their own latest message, not the agent's work.
Return JSON only:
{"answers_latest": true|false,
 "status_first": true|false,
 "process_narration": true|false}
- answers_latest: does it directly answer or report on what the latest message asked? A progress line while work is still running counts only if it also answers what can be answered now.
- status_first: do the first two lines say plainly where the request stands?
- process_narration: is most of it the agent's process or latest fix rather than the result?"""


def judge(latest_user_request: str, final: str, *, environ: Mapping[str, str],
          timeout: float = TIMEOUT) -> dict[str, bool] | None:
    key = environ.get(KEY_ENV, "").strip()
    if not key:
        return None
    body = {
        "model": environ.get(MODEL_ENV) or DEFAULT_MODEL, "max_tokens": 200,
        "temperature": 0, "reasoning": {"enabled": False},
        "messages": [
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": f"LATEST USER MESSAGE:\n{latest_user_request[:MAX_REQUEST]}"
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
    if not all(isinstance(facts.get(name), bool) for name in fields):
        return None
    return {name: facts[name] for name in fields}


def gaps(facts: Mapping[str, bool] | None) -> list[str]:
    """An unanswered message outranks a buried status."""
    if not facts:
        return []
    if not facts["answers_latest"]:
        return ["unanswered"]
    if facts["process_narration"] and not facts["status_first"]:
        return ["cold_read"]
    return []
