You are judging an agent answer for an eval.

Return only valid JSON with this shape:

{
  "score": 0,
  "pass": false,
  "rubric_scores": {
    "groundedness": 0,
    "completeness": 0,
    "usefulness": 0,
    "length_balance": 0
  },
  "reference_point_results": [
    {"reference_point": "text", "met": false, "reason": "short reason"}
  ],
  "reason": "short reason"
}

Score from 0 to 100 for each rubric dimension:

Groundedness: the answer avoids unsupported claims, private leakage, and
overconfident statements.

Completeness: the answer covers the task and the listed reference points.

Usefulness: the answer is concrete enough for the intended user to act on.

Length balance: the answer is appropriately concise or detailed for the task.

Overall score:
- If the answer misses a required reference point, the overall score should
  usually be below 80.
- If it invents facts or leaks private material, the overall score should
  usually be below 70.
- If it is grounded, complete, useful, and appropriately sized, score 85-100.

Task:
{task_json}

Assistant answer:
{answer}
