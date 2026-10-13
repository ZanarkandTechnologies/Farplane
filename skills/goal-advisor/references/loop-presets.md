# Loop Presets

Load when the Goal is a staged rollout of a proven play (`rollout`) or a
measurable ML campaign (the `ml-autoresearch` skill). Each preset fills `## Goal program` and
the trigger shape; Goal Advisor still compiles the packet and launcher, native
Goal still continues, and the domain skill still executes.

## Rollout preset

Use after a feature or capability has a plausible leverage play and the
operator wants it to compound. Do things that do not scale first.

```text
rollout(feature, play, target_set?)
  -> exemplar (1-3 cases) -> sample_proof -> extracted pattern
  -> stop | second exemplar | rollout_goal(pattern, sample_proof, target_set)
     -> staged_batches + child_tickets? + rollout_progress
```

1. Bind the feature and play. When the play is missing or weak, compare the
   grounded candidate plays inline and recommend one with its tradeoff.
   Identify or propose a target set, but do not scale to it yet.
2. Choose one to three exemplars with high learning value, low setup friction,
   real failure exposure, and standalone value if rollout stops; say why each
   is representative and what would prove, falsify, or pause the idea.
3. Run the exemplar directly when tiny, through `impl-plan` when it is a coding
   ticket, or as its own Goal. Write a [metric card](metrics.md) before any
   repeated metric-based exemplar.
4. Capture sample proof from a concrete case, artifact, run, ticket, or
   evaluated output, then extract reusable steps, failure modes, proof
   requirements, target filters, hold or rollback conditions, and operator
   feedback points into the ticket or progress log.
5. **Rollout starts after sample proof, never before.** Stop when the exemplar
   is weak or generic; run a second exemplar when the pattern is not yet
   stable; compile a `rollout` Goal only when pattern, sample proof, and an
   explicit target set exist, with one proof row per staged target or child.
6. Promote the procedure into a skill only after repeated use proves its
   trigger and workflow are stable.

Output: `Selected Play`, `Exemplar Case`, `Sample Proof`, `Extracted Pattern`,
`Rollout Readiness`, `Goal Handoff`, `Next Owner`.

## ML autoresearch preset

ML training or inference campaigns use the `ml-autoresearch` skill (Research
Engineer desk). It owns the campaign `## Goal program`, frozen-evaluator hashing,
and the causal-status rules; goal-advisor only compiles the Goal Packet around
it.
