---
name: advise
description: Use when the user wants advice, tradeoff framing, or a recommendation and has not already supplied a clear take. Produces 3 viable options with pros/cons and names the best recommendation directly.
---

# Advise

Use this when the user is looking for judgment, not just a menu of possibilities.

## Job

1. Assume a guidance gap when the user has not supplied a take.
2. Frame the real decision in one sentence.
3. Compare 3 viable options.
4. Recommend one option clearly.
5. State the next step directly instead of ending with an upsell.

## Use When

- the user asks what they should do
- the user asks for options, alternatives, tradeoffs, or a recommendation
- the user has described a problem but not a preferred direction
- a plan, architecture, or product choice has multiple legitimate paths

## Do Not Use When

- the task is a direct execution request with no meaningful decision to make
- the user has already chosen the direction and only wants implementation
- the answer must stay source-bound and recommendation-free, such as strict documentation synthesis

## Workflow

1. Restate the decision briefly.
2. Name the evaluation criteria that matter most for this case.
3. Use `reference-grounding` first when the best recommendation depends on
   current facts, official behavior, peer norms, local baseline, or
   implementation examples. Escalate to `research:*` when a full brief is
   needed.
4. Present exactly 3 viable options.
5. For each option, give concrete pros and cons.
6. Recommend one option and explain why it wins under the current constraints.
7. Name the main tradeoff being accepted.
8. Move straight into the recommended next step when execution is obvious.

## Output

Produce a compact decision note with:

- `Decision`
- `Options`
- `Recommendation`
- `Tradeoff accepted`
- `Next step`

## Guardrails

- do not mirror uncertainty back to the user when you can make a grounded call
- do not present fake alternatives that are obviously invalid
- do not exceed 3 options unless the user explicitly asks for more
- do not end with "if you want I can ..."
- do not turn source-set synthesis into advice; use `best-of-worlds` when the
  job is to extract, score, and adapt ideas from known sources
- if the choice is UI/UX-facing, hand off to `functional-ui`
- if the choice is an implementation plan, embed this workflow inside `impl-plan`
