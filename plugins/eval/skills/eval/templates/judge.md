You are judging an agent answer for a harness eval.

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

Allowed verdicts:
- `A`: strong pass. The answer is grounded, complete, useful, repeatable where relevant, and well-sized.
- `B`: near miss. The answer is usable but has a clear missing detail, caveat, or quality issue that should be fixed.
- `C`: revise. The answer is directionally relevant but misses a meaningful requirement or would not be reliable yet.
- `D`: fail or blocked. The answer is unsupported, incomplete, unusable, non-repeatable, or impossible to judge from the evidence.

Rubric values must be `A`, `B`, `C`, or `D`. Set `pass` to true only for `A`.

Groundedness: whether the answer is supported by the task and reference points
and avoids invented claims.
- `A`: fully grounded; avoids unsupported claims and states uncertainty when evidence is missing.
- `B`: mostly grounded; only minor unsupported wording, mild overclaim, or missing caveat.
- `C`: some correct facts, but includes material unsupported claims or overstates weak evidence.
- `D`: mostly unsupported or fabricated; invents important facts, names, metrics, features, dates, prices, or customer claims.

Completeness: whether the answer covers all required parts of the request and
reference points.
- `A`: covers all required points directly, including necessary caveats or constraints.
- `B`: covers most required points but misses one meaningful detail, caveat, or subpart.
- `C`: covers some required points but omits important parts of the task.
- `D`: misses most required points or answers the wrong question.

Usefulness: whether the answer helps the intended user take action in the real
scenario.
- `A`: clear, specific, scenario-appropriate, and actionable; includes the right format, examples, caveats, or next steps.
- `B`: useful at a basic level, but could use stronger structure, examples, phrasing, or decision support.
- `C`: somewhat relevant but too vague, incomplete, or generic to be practically useful.
- `D`: not actionable; generic, confusing, misleading, or unusable.

Repeatability: the answer or artifact can be reused by another agent without
rediscovering the same decisions, duplicating instructions, or depending on
chat-only context.
- `A`: another agent can rerun from files alone; commands, artifacts, branch paths, and proof are explicit.
- `B`: mostly repeatable, but one setup assumption, path, command, or decision should be clearer.
- `C`: partially repeatable but depends on chat context, duplicated guidance, or rediscovered decisions.
- `D`: not repeatable from files alone.

Length balance: the answer is appropriately concise or detailed for the task.
- `A`: well-sized for the request; concise when needed, detailed when needed, and easy to scan.
- `B`: reasonable length, but could be tighter or more developed.
- `C`: noticeably too terse or too verbose; length makes important content harder to use.
- `D`: far too short to answer the task, or excessively long and unfocused.

Reference point rule:
- Mark every reference point as met or not met.
- If any required reference point is not met, the overall verdict should usually be `B` at best, and often `C`.
- If groundedness is `C` because of a material unsupported claim, the overall verdict should usually be `C` or `D`.
- If the answer is accurate but not actionable, the overall verdict should usually be `B` or `C`.
- If the answer invents facts, leaks private material, or cannot be judged from available evidence, the overall verdict should be `D`.
- Only `A` is a pass. `B` is useful diagnostic signal, not success.
- Do not average rubric tiers mechanically. Let the most severe issue constrain the overall verdict.

Task:
{task_json}

Assistant answer:
{answer}
