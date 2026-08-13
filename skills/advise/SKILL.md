---
name: advise
description: "Turn an under-specified decision into three options, tradeoffs, and one recommendation when the user asks for advice."
tier: 1
source: local
template_uses:
  skill-template: "0.1.0"
  skill-qa-checklist: "0.1.0"
  skill-surface-budget: "0.1.0"
qa_checklist: qa_checklist.md

---

# Advise

## Context

`advise` is a Tier 1 primitive. Use it only when the active workflow needs a
judgment call among real options; direct execution requests should stay with
the owning skill or caller.

Use when the user needs judgment, not a neutral menu.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Read `qa_checklist.md` as preflight guardrails when using this skill
  for material advice.
- [ ] 2. State the real decision and the criteria that matter.
- [ ] 3. Check evidence needs; use supplied/local grounding when needed, or name
  the evidence gap instead of doing higher-tier research inside this skill.
- [ ] 4. Compare exactly 3 viable options with concrete pros and cons when three
  realistic options exist.
- [ ] 5. Recommend one option clearly, name the accepted tradeoff, and state the
  direct next step or owning next skill.
- [ ] 6. Finish-check the advice.
  - [ ] No neutral menu, fake third option, hidden evidence gap, or vague
    "if you want" ending.
  - [ ] For high-stakes, expensive, or durable decisions, route to
    `deliberative-advice` or an independent review pass.
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
  options that match the decision criteria and explain the recommendation
  compactly.
- Do not end with "if you want I can ..."
- Evidence gate: if the recommended option depends on facts not already in
  context, use `reference-grounding` or state the evidence gap before choosing.
- Use `reference-grounding` when the recommendation depends on evidence.
- Use `best-of-worlds` when known sources must be extracted, scored, and
  adapted before advice.
- Escalate to `deliberative-advice` / `deliberative-advice:complex` when the decision is
  high-stakes, expensive, ambiguous across several credible perspectives, or
  likely to benefit from independent critique before synthesis.
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
- [../deliberative-advice/SKILL.md](../deliberative-advice/SKILL.md) - use for
  high-stakes or complex recommendations that need independent perspectives,
  critique, synthesis, and visible dissent.
