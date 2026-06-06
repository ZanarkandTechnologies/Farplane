---
name: advise
description: Use when the user wants advice, tradeoff framing, or a recommendation and has not already supplied a clear take. Produces 3 viable options with pros/cons and names the best recommendation directly.
tier: 1
source: local
skill_template_version: "0.1.0"
---

# Advise

## Context

`advise` is a Tier 1 primitive. Use it only when the active workflow needs a
judgment call among real options; direct execution requests should stay with
the owning skill or caller.

Use when the user needs judgment, not a neutral menu.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. State the real decision in one sentence.
- [ ] 2. Start from first principles before comparing options: objective,
  user/system need, root cause, constraints, assumptions, proof/falsification,
  tradeoffs, and non-goals.
- [ ] 3. Name the evaluation criteria that matter for this user, repo, or ticket.
- [ ] 4. Require supplied evidence when the recommendation depends on current
  facts, official behavior, peer norms, local baseline, or implementation
  examples.
- [ ] 5. Surface an evidence gap instead of launching a higher-tier research pass
  from this Tier 1 primitive.
- [ ] 6. Compare exactly 3 viable options with concrete pros and cons.
- [ ] 7. Recommend one option clearly and name the tradeoff being accepted.
- [ ] 8. State whether the recommendation is fully grounded or needs a
  higher-tier source synthesis step.
- [ ] 9. State the direct next step or owning next skill.
- [ ] 10. Review before completion.
  - [ ] For changes to this skill, require a separate review pass before claiming
  the update is ready.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Use the visible decision-note shape in `## Output` when the recommendation
needs to survive beyond chat.
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

## Gotchas

- Do not use `advise` to delay an obvious reversible action.
- Do not list neutral options without naming the recommendation.
- Do not invent a third option just to satisfy the three-option shape.
- Do not perform source-set feature synthesis in this primitive; the caller
  should provide synthesized choices when the task is broader than advice.

## Reference Map

- [../reference-grounding/SKILL.md](../reference-grounding/SKILL.md) - use
  when the recommendation depends on evidence.
- [../best-of-worlds/SKILL.md](../best-of-worlds/SKILL.md) - use when supplied
  sources must be synthesized before advice.
