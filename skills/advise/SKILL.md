---
name: advise
description: "Turn an under-specified decision into three options, tradeoffs, and one recommendation when the user asks for advice."
tier: 1
source: local
capability:
  kind: shortcut
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

## Skill Signature

```text
advise(decision, context?, ensemble?: auto | max) -> recommendation + dissent?

state: reads(decision, supplied context, and relevant evidence); writes(advice
  response or decision note); never mutates external state
owns: option comparison, recommendation, accepted tradeoff, and next owner
gates: real_decision; evidence_gap_visible; recommendation_explicit;
  dissent_preserved_when_ensemble
fails: neutral_menu; fake_options; automatic_ensemble; hidden_evidence_gap
```

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
  - [ ] When `ensemble` is `auto` or `max`, load `ensemble.yaml`, collect
    independent first passes, and preserve the strongest dissent in synthesis.
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

## Ensemble Mode

The direct path remains the default. When the operator asks for ensemble
coverage, accept only `ensemble: auto | max`:

- `auto`: select exactly three relevant, diverse personas from
  [ensemble.yaml](ensemble.yaml), state why they fit, then synthesize.
- `max`: use every persona in that file, then synthesize.

Each lane receives the same decision and evidence, completes its first pass
before critique, and returns a recommendation. Synthesis preserves the best
argument, meaningful dissent, tradeoff, confidence, and next owner; it is not
a majority vote.

When a recommendation changes existing behavior, place a concise **Change
preview** before the recommendation:

- **Before:** quote or cite the current behavior and exact gap; otherwise state
  the current assumption and evidence gap.
- **After:** state the smallest proposed change and how it closes that gap.
- **Example:** show one representative current input or workflow -> intended
  outcome.

## Guardrails

- Do not use this for direct execution requests with no meaningful choice.
- Do not invent fake options.
- Do not dump a full first-principles essay by default; use the basis to choose
  options that match the decision criteria and explain the recommendation
  compactly.
- Do not end with "if you want I can ..."
- Evidence gate: inspect supplied or local sources when the recommendation
  depends on facts; otherwise state the evidence gap before choosing.
- When known sources need broader extraction or scoring, return a visible
  synthesis-needed handoff rather than silently expanding this shortcut.
- Do not run an ensemble unless the operator explicitly requests `auto` or
  `max`; normal advice stays fast and single-agent.
- Hand UI/UX-facing choices to `functional-ui`.
- Embed this inside `impl-plan` for coding implementation plans.

## Gotchas

- Do not use `advise` to delay an obvious reversible action.
- Do not list neutral options without naming the recommendation.
- Do not invent a third option just to satisfy the three-option shape.
- Do not perform source-set feature synthesis in this primitive; the caller
  should provide synthesized choices when the task is broader than advice.

## Reference Map

- Inspect supplied and local evidence directly when enough; otherwise name the
  exact grounding or synthesis handoff the operator must request.
- [ensemble.yaml](ensemble.yaml) — load only for `ensemble: auto | max`.
