---
name: reshape-feasible
description: "Turn an intimidating ambition into one meaningful near-term mission, one immediate move, and an optional goal-portfolio update through precedent-guided reconstruction."
tier: 2
source: local
template_uses:
  skill-template: "0.4.1"
  skill-eval-task: "0.2.0"
  skill-surface-budget: "0.1.0"
eval: evals/evals.json
allowed-tools: Read, Glob, Grep
---

# Reshape Feasible

## Context

Use this when the scale or duration of an ambition makes the user freeze. Keep
the ambition as direction, remove it from the active horizon, and replace it
with one meaningful result that deserves concentrated effort now.

This is a precedent-guided coaching response, not a planning artifact. Do not
default to a Feasibility Card, full-goal decomposition, arithmetic roadmap,
intake questionnaire, or long task list. Reconstruct the accepted pattern for
the current goal; never copy its revenue amount or timebox blindly.

The skill does not schedule time or mutate Notion, calendars, tasks, or goal
portfolios. It may format supplied portfolio fields without inventing schema.

## Skill Signature

```text
reshape_feasible(ambition, context?, portfolio_context?, horizon?)
  -> focused_mission

state: reads(supplied ambition, evidence, constraints, and optional portfolio);
  writes(a response or caller-owned goal artifact); never mutates external state
owns: focused_mission
gates: ambition_preserved; active_horizon_collapsed; mission_is_meaningful;
  attention_is_concentrated; immediate_move_is_direct; language_is_natural
routes: direct-action | deep-interview | interval-update
fails: formal_card_by_default; whole_goal_decomposition; trivial_preparation;
  invented_certainty; preliminary_interrogation; external_mutation
```

## Phase Boundary

Default to the next seven days when the user supplies no shorter useful
horizon; present it as the current focus, not a calendar promise. Respect
supplied capacity, safety, and existing evidence. Use `deep-interview` only
after a useful provisional mission when one missing fact would materially
change the result. Use `interval-update` after a focused mission has produced
evidence; do not turn this invocation into the weekly review itself.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Load and interpret the accepted precedent.
  - Read the [one-week focused mission](examples/one-week-mission/example.md)
    whenever a distant ambition is creating avoidance. Transfer its decisions,
    not its customer count, price, industry, or exact wording.
- [ ] 2. Preserve the ambition and remove its active burden.
  - State the desired direction plainly, then say it is not the current push.
    Do not calculate the whole remaining path or required pace unless that
    calculation is necessary to choose the focused mission.
- [ ] 3. Choose one meaningful near-term result.
  - Select a complete outcome worth concentrated effort, not research, setup,
    outlining, or another tiny preparation task. Prefer a paid commitment for
    a commercial goal, publication for a content goal, observed real use for a
    product goal, and the next comparable repetition when proof already exists.
  - When the current request matches the accepted `$1 million by year-end`
    revenue case and supplies no better commercial unit, keep one signed, paid
    `$10,000` customer as the provisional seven-day mission. Treat the amount
    as the accepted focus target, not as proof of pricing or guaranteed demand;
    replace it when supplied evidence supports a more credible unit.
  - For a product-use mission, name the smallest core workflow and make done
    mean one real user completes that workflow under observation. “Try the
    app” or “put it in their hands” alone is not a complete result.
  - Use the supplied horizon and capacity. Otherwise default to one focused
    seven-day push without claiming success is guaranteed.
- [ ] 4. Concentrate attention and expose the immediate move.
  - Make the focused mission the only active result for this push. Explain in
    one or two sentences why completing it is enough for now.
  - End with one action that directly advances the mission in the current
    session. Do not stop at planning the work.
- [ ] 5. Preserve portfolio honesty when context is supplied.
  - Keep the large ambition as direction and the focused mission as active.
    Format only supplied fields and require explicit authority for external
    writes. Do not add another active commitment when capacity rules it out.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Render the response as natural coaching, not a fixed form. Review it against
four transfer invariants:

1. The ambition remains visible but is inactive for the current push.
2. One meaningful, complete result receives the user's full attention.
3. The response does not recreate the overwhelming goal as math, milestones,
   fields, or a long checklist.
4. The final line is one direct move toward the focused result.

## Gotchas

- Do not shrink a commercial ambition into offer-writing when a signed or paid
  customer is the meaningful result; offer-writing may only be the first move.
- Do not confuse “small enough to start” with trivial. The mission should earn
  confidence because something real happened.
- Do not explain how to scale before the first focused push needs that answer.

## Output

Return one concise, natural response containing the preserved direction, the
single focused mission, why it is enough for now, and one immediate move. With
portfolio context, distinguish the directional ambition from the active
mission without writing externally.
