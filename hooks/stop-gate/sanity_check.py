#!/usr/bin/env python3
"""Run sanitized final answers through the configured Jev response-format check.

Passes when no clean answer is nudged and most answers with a known gap are.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "hooks" / "shared"))

from response_format import questions, select_gaps  # noqa: E402
from skill_suggestion import (  # noqa: E402
    ENDPOINT_ENV, MODEL_ENV, HttpDecisionClient, _provider_config,
)

MIN_RECALL = 0.8


def load_cases() -> list[dict[str, object]]:
    value = json.loads(Path(__file__).with_name("eval_cases.json").read_text())
    required = {"id", "latest_user_request", "proposed_final", "files_changed",
                "expected_shape", "expected_fixes"}
    if not isinstance(value, list) or not all(
            isinstance(case, dict) and required <= case.keys() for case in value):
        raise ValueError("response-format eval cases have an invalid shape")
    return value


def main() -> int:
    environ = dict(os.environ)
    config = _provider_config(environ)
    if config is None or not environ.get(config["api_key_env"], "").strip():
        print("response-format sanity check requires the configured Jev credentials",
              file=sys.stderr)
        return 2

    def evaluate(case: dict[str, object]) -> dict[str, object]:
        client = HttpDecisionClient(
            api_key=environ[config["api_key_env"]], provider=config["provider"],
            endpoint=environ.get(ENDPOINT_ENV) or config["endpoint"], timeout=8,
        )
        final = str(case["proposed_final"])
        state = {"latest_user_request": case["latest_user_request"],
                 "proposed_final": final, "files_changed": case["files_changed"]}
        result = client.system_one(state=state, questions=questions(),
                                   model=environ.get(MODEL_ENV) or config["model"])
        shape, gaps = select_gaps(result["answers"], files_changed=bool(case["files_changed"]),
                                  final=final)
        expected = list(case["expected_fixes"])  # type: ignore[arg-type]
        scores = {key.removeprefix("gap::"): answer.get("noul")
                  for key, answer in result["answers"].items()
                  if key.startswith("gap::") or key == "visible_feature"}
        return {"id": case["id"], "shape": shape, "expected_shape": case["expected_shape"],
                "scores": scores,
                "gaps": gaps, "expected": expected,
                "false_nudge": bool(gaps) and not expected,
                "caught": bool(expected) and bool(set(gaps) & set(expected))}

    cases = load_cases()
    with ThreadPoolExecutor(max_workers=5) as pool:
        rows = list(pool.map(evaluate, cases))
    for row in rows:
        print(json.dumps(row, sort_keys=True))
    gap_cases = [row for row in rows if row["expected"]]
    false_nudges = sum(bool(row["false_nudge"]) for row in rows)
    recall = sum(bool(row["caught"]) for row in gap_cases) / max(1, len(gap_cases))
    shape_hits = sum(row["shape"] == row["expected_shape"] for row in rows)
    ok = false_nudges == 0 and recall >= MIN_RECALL
    print(json.dumps({"cases": len(rows), "false_nudges": false_nudges,
                      "recall": round(recall, 2), "shape_accuracy": f"{shape_hits}/{len(rows)}",
                      "status": "pass" if ok else "fail"}, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
