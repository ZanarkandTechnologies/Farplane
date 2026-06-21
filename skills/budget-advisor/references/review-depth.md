# Review Depth Template

Use this template when `review_depth` is set.

`review_depth` spends budget on the caller skill's review phase. It does not
change the skill's core task or output contract.

## Inputs

```text
review_depth: 0 | 1 | 2 | 3
caller_skill:
base_result:
review_rubric_or_checklist:
stop_condition?: "fixed-count" | "no-material-findings" | "budget-spent"
```

## Program

```text
result = run caller skill base program

for pass in 1..review_depth:
  review_result = run review phase on result
  if review_result has no material findings:
    stop when stop_condition is "no-material-findings"
  result = revise result using accepted findings

return result in caller skill output contract
```

## Routing

- Use inline self-check when the review is tiny and the skill already owns a
  checklist.
- Use `review` when the result is a material artifact, evidence bundle, skill
  contract, prompt, plan, implementation, or completion claim.
- Use a reviewer subagent only when independent judgment is worth the
  coordination cost and the runtime supports it.

## Guardrails

- Cap ordinary `review_depth` at `3`.
- Stop early when findings repeat, become cosmetic, or require new execution
  evidence.
- Pass subskill review calls with `max_budget_depth: 0` unless the caller
  explicitly asks for nested budget expansion.
- Do not turn review depth into a same-scope `plan -> review -> plan -> review`
  loop.

## Output Fragment

```text
review_depth_program:
  template_ref: skills/budget-advisor/references/review-depth.md
  review_depth:
  review_route:
  stop_condition:
  final_output_contract:
```
