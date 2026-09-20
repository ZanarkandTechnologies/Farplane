#!/usr/bin/env python3
"""Run sanitized continuation decisions through the configured Jev provider."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "bin" / "runtime"))

from continuation import QUESTION  # noqa: E402
from skill_suggestion import (  # noqa: E402
    ENDPOINT_ENV, MODEL_ENV, HttpDecisionClient, _provider_config,
)

THRESHOLD = 0.5


def load_cases() -> list[dict[str, str]]:
    value = json.loads((Path(__file__).with_name("eval_cases.json")).read_text())
    if not isinstance(value, list):
        raise ValueError("continuation eval cases must be a list")
    required = {"id", "expected", "original_request", "latest_user_request",
                "proposed_final"}
    for case in value:
        if not isinstance(case, dict) or not required <= case.keys():
            raise ValueError("continuation eval case has an invalid shape")
        if case["expected"] not in {"allow", "nudge"}:
            raise ValueError(f"invalid expected decision for {case['id']}")
    return value


def state_for(case: dict[str, str]) -> dict[str, object]:
    return {
        "original_request": case["original_request"],
        "latest_user_request": case["latest_user_request"],
        "recent_dialogue": [
            {"role": "user", "text": case["latest_user_request"]},
            {"role": "assistant", "text": case["proposed_final"]},
        ],
        "proposed_final": case["proposed_final"],
        "own_nudges_this_user_turn": 0,
        "recognized_length_feedback_this_user_turn": False,
        "source_truncated": False,
    }


def main() -> int:
    environ = dict(os.environ)
    config = _provider_config(environ)
    if config is None or not environ.get(config["api_key_env"], "").strip():
        print("continuation sanity check requires the configured Jev credentials",
              file=sys.stderr)
        return 2

    def evaluate(case: dict[str, str]) -> dict[str, object]:
        client = HttpDecisionClient(
            api_key=environ[config["api_key_env"]],
            provider=config["provider"],
            endpoint=environ.get(ENDPOINT_ENV) or config["endpoint"],
            timeout=5,
        )
        result = client.system_one(
            state=state_for(case),
            questions={"nudge": {"type": "noul", "instructions": QUESTION}},
            model=environ.get(MODEL_ENV) or config["model"],
        )
        score = result["answers"]["nudge"]["noul"]
        observed = "nudge" if score >= THRESHOLD else "allow"
        return {
            "id": case["id"],
            "expected": case["expected"],
            "observed": observed,
            "score": score,
            "pass": observed == case["expected"],
        }

    cases = load_cases()
    with ThreadPoolExecutor(max_workers=min(5, len(cases))) as pool:
        rows = list(pool.map(evaluate, cases))
    for row in rows:
        print(json.dumps(row, sort_keys=True))
    passed = sum(bool(row["pass"]) for row in rows)
    print(json.dumps({"cases": len(rows), "passed": passed,
                      "status": "pass" if passed == len(rows) else "fail"},
                     sort_keys=True))
    return 0 if passed == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
