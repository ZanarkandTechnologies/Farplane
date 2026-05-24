# Todos

- [ ] Read the operator request, ticket, batch, or board context.
- [ ] Classify the work unit: direct request, single ticket, ticket batch,
  board drain, epic slice, or metric loop.
- [ ] Check scope readiness: executable now, needs `impl-plan`, needs
  reslicing, or needs a metric/research loop.
- [ ] Choose the execution profile: ambition, Goal policy, compute target,
  planning route, proof route, testability route, and blocker policy.
- [ ] Use [plan](../plan/SKILL.md) or `impl-plan` only when material planning
  is warranted.
- [ ] Use [execute](../execute/SKILL.md), `$impl`, direct local work, or
  `close-ticket` only after the work unit is executable.
- [ ] For ticket batches, require one proof row per ticket plus one batch-level
  regression row before completion.
- [ ] For board drains, hand board selection and grouping to `$ralph`; do not
  create hidden scheduler state here.
- [ ] Use `goal-crafter` or native `/goal` when the work is ambitious,
  long-running, batch-oriented, board-draining, metric-driven, or likely to
  need durable unblock behavior.
- [ ] Record blockers with evidence instead of asking the operator when the
  ticket policy already gives a safe fallback.

