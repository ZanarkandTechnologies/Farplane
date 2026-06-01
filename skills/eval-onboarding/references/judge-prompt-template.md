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

Main grading rule: use the task reference points as the target. Penalize
missing reference points, unsupported claims, private leakage, vague advice, and
answers that are too short or too long for the task.

Task:
{task_json}

Assistant answer:
{answer}
