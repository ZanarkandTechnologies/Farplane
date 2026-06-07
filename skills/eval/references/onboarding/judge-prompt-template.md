You are judging an agent answer for an eval.

Return only valid JSON with this shape:

{
  "verdict": "A",
  "pass": true,
  "rubric": {
    "groundedness": "A",
    "completeness": "A",
    "usefulness": "A",
    "repeatability": "A",
    "length_balance": "A"
  },
  "reference_point_results": [
    {"reference_point": "text", "met": true, "reason": "short reason"}
  ],
  "reason": "short reason"
}

Allowed verdicts and rubric values are `A`, `B`, `C`, or `D`. Do not use
0-100 scores. Set `pass` to true only for `A`; `B` is a near miss, not success.

Main grading rule: use the task reference points as the target. Penalize
missing reference points, unsupported claims, private leakage, vague advice,
non-repeatable artifacts, and answers that are too short or too long for the
task. Do not average tiers mechanically; let the most severe issue constrain
the overall verdict.

Repeatability: for reusable skills, prompts, workflows, or harness behavior,
judge whether another agent can run the artifact again from files alone without
hidden chat context, duplicated instructions, or rediscovered decisions.

Task:
{task_json}

Assistant answer:
{answer}
