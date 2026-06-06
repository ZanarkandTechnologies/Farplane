---
name: advise
description: Use when the user wants advice, tradeoff framing, or a recommendation and has not already supplied a clear take. Produces 3 viable options with pros/cons and names the best recommendation directly.
tier: 1
source: local
skill_template_version: "0.1.0"
---

# Advise

Use when the user needs judgment, not a neutral menu.

## Job

Turn an unclear choice into a compact recommendation:

1. Name the real decision.
2. Start from first principles: objective, user/system need, root cause,
   constraints, assumptions, proof/falsification, tradeoffs, and non-goals.
3. Name the criteria that matter here.
4. Compare exactly 3 viable options.
5. Recommend one.
6. State the accepted tradeoff and direct next step.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] State the real decision in one sentence.
- [ ] Start from first principles before comparing options: objective,
  user/system need, root cause, constraints, assumptions, proof/falsification,
  tradeoffs, and non-goals.
- [ ] Name the evaluation criteria that matter for this user, repo, or ticket.
- [ ] Require supplied evidence when the recommendation depends on current
  facts, official behavior, peer norms, local baseline, or implementation
  examples.
- [ ] Surface an evidence gap instead of launching a higher-tier research pass
  from this Tier 1 primitive.
- [ ] Compare exactly 3 viable options with concrete pros and cons.
- [ ] Recommend one option clearly and name the tradeoff being accepted.
- [ ] Keep source-set feature synthesis out of this primitive; the caller
  should provide the synthesized choices when the task is broader than advice.
- [ ] State the direct next step or owning next skill.
- [ ] For changes to this skill, require a separate review pass before claiming
  the update is ready.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->
## Output

Use this shape when a visible decision note is useful:

- `Decision`
- `Options`
- `Recommendation`
- `Tradeoff accepted`
- `Next step`

## Guardrails

- Do not use this for direct execution requests with no meaningful choice.
- Do not invent fake options.
- Do not dump a full first-principles essay by default; use the basis to choose
  better options and explain the recommendation compactly.
- Do not end with "if you want I can ..."
- Evidence gate: if the recommended option depends on facts not already in
  context, use `reference-grounding` or state the evidence gap before choosing.
- Use `reference-grounding` when the recommendation depends on evidence.
- Use `best-of-worlds` when known sources must be extracted, scored, and
  adapted before advice.
- Hand UI/UX-facing choices to `functional-ui`.
- Embed this inside `impl-plan` for coding implementation plans.
