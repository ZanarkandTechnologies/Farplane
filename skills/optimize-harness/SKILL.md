---
name: optimize-harness
description: "Turn observed Farplane behavior gaps into placement decisions, proof or eval, accepted changes, and review."
tier: 3
group: harness
source: local
template_uses:
  skill-template: "0.2.0"
  skill-eval-task: "0.1.0"
eval: eval_task.json
allowed-tools: Read, Glob, Grep, Bash

---

# Optimize Harness

## Context

Use this when the operator says Farplane should behave differently and wants
the harness changed, not just explained. This is the high-level entrypoint for
"fix this behavior" requests: diagnose the gap, choose the owning surface,
create proof, route the change, and review the result.

Weekly Interval may route selected self-evolution bets here when the bet is not
just a single skill edit or coding ticket, but an observed-versus-expected
harness behavior gap that needs diagnosis, placement, proof, change, and
review.

This skill orchestrates existing surfaces. It should not absorb their jobs:
`gap-analysis` diagnoses, `horizon-advisor` owns strategy deltas,
`leverage-advisor` scores compounding plays, `harness-advisor` places the fix,
`proof-advisor` chooses the proof surface and proof cases, `eval` executes
runnable eval proof after eval is selected, `skill-creator` packages new
reusable workflows, `skill-maintenance` backpropagates into existing skills,
`impl-plan` plans material coding tickets, `goal-advisor` compiles execution,
`self-improve` runs metric-driven experiments, and `review` judges readiness.

## Skill Signature

```text
optimize_harness(observed_behavior, expected_behavior?, metric?, evidence?) -> accepted_change | experiment_plan | blocked_report
state: reads(gap reports, farplane/goals.md?, interval reports?, harness algebra,
             harness doctrine, feature registry, skill registry, evals,
             tickets, target surfaces);
       writes(ticket?, eval_case?, experiment_artifact?, applied_change?,
              goals_delta_candidate?, review_receipt?)
gates: gap_named; loss_term_named; metric_or_reward_signal_named;
       owner_surface_named; proof_route_named; accept_hold_or_rollback_named;
       review_passes_or_blocked
routes: gap-analysis | horizon-advisor | leverage-advisor | harness-advisor |
  proof-advisor | eval | skill-creator | skill-maintenance | impl-plan |
  goal-advisor | self-improve | review
fails: changes without proof; optimizes vague taste; creates new skill before checking registry; hides blocked state
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Normalize the request into observed behavior, expected behavior,
  candidate metric when present, and evidence already available.
- [ ] 2. Bind the optimization target.
  - [ ] Read `farplane/goals.md` and
        `docs/fundamentals/harness-algebra.md` when the task is Farplane's own
        self-evolution or a material harness-optimization pass.
  - [ ] Name the loss term: human intervention, false completion, agent churn,
        coordination cost, ungrounded claims, brittle state loss, context bleed,
        source gaps, quality, proof, or auditability.
  - [ ] Name the reward signal or proof provider. Prefer reasoning over honest
        qualitative evidence early; use numbers only when the metric source is
        real enough to compare across intervals.
- [ ] 3. Diagnose the gap with [gap-analysis](../gap-analysis/SKILL.md).
  - [ ] If the gap is already obvious and well grounded, state it explicitly
    and keep moving.
  - [ ] If expected behavior is underspecified, mark the uncertainty instead of
    inventing a target.
- [ ] 4. Choose whether this is a full harness optimization or a smaller route.
  - [ ] Route strategy/value/KPI/frontier changes to
        [horizon-advisor](../horizon-advisor/SKILL.md).
  - [ ] Route pure leverage scoring to
        [leverage-advisor](../leverage-advisor/SKILL.md).
  - [ ] Continue here only when the improvement needs coordinated gap,
        placement, proof, change, and review.
- [ ] 5. Place the fix with [harness-advisor](../harness-advisor/SKILL.md).
  - [ ] Name one primary owner surface.
  - [ ] Name rejected surfaces and why they should not own this change now.
- [ ] 6. Design proof with [proof-advisor](../proof-advisor/SKILL.md).
  - [ ] Choose deterministic test, validator, eval, QA, visual QA, agent QA,
        review, or source-gap proof before creating proof artifacts.
  - [ ] Create or update an eval case only when eval is the selected proof
        surface and the expected behavior is durable.
  - [ ] Use e2e workflow evals when the failure is compositional across skills,
        tools, tickets, reports, or subagents.
  - [ ] Mark the case as `hardcase` only when it is unusually difficult,
    reusable, benchmark-worthy, or saleable after sanitization.
- [ ] 7. Choose direct change, experiment, or execution handoff.
  - [ ] 1. Use direct implementation when the owner and proof are clear.
  - [ ] 2. Use [self-improve](../self-improve/SKILL.md) when a target skill or
    harness surface needs metric-driven candidate search.
  - [ ] 3. Use [skill-maintenance](../skill-maintenance/SKILL.md) for
    existing skill hardening, eval-to-QA sync, registry, bulk rollout, or
    skill-contract migrations.
  - [ ] 4. Use [skill-creator](../skill-creator/SKILL.md) only when the stable
    reusable workflow has no existing owner.
  - [ ] 5. Use [impl-plan](../impl-plan/SKILL.md) when the accepted route is a
    material coding ticket needing a plan/proof contract.
  - [ ] 6. Use [goal-advisor](../goal-advisor/SKILL.md) when the selected
    frontier is ready for a ticket-backed Goal Packet, heartbeat, or rollout.
- [ ] 8. Apply the accepted change through the owning implementation workflow
  and keep evidence in the active ticket or proof artifact.
- [ ] 9. Decide accept, hold, or rollback.
  - [ ] `accept` only when the named loss is reduced, proof supports the claim,
        required review gates pass, no safety/test regression appears, and cost
        is within budget.
  - [ ] `hold` when local proof passes but workflow or composition proof is
        missing.
  - [ ] `rollback` when evidence is weak, regression appears, composition
        fails, or the owner surface was wrong.
- [ ] 10. Use the native execution phase for final proof, writeback, and
  review routing before claiming the harness behavior is improved.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Workflow spine:

```text
observe -> expected -> loss_term -> gap_report -> leverage_or_placement
        -> proof_route -> change_or_experiment -> accept_hold_rollback
        -> review -> writeback
```

Minimal handoff:

```text
Observed:
Expected:
Gap:
Loss term:
Reward signal:
Primary owner:
Proof:
Route:
Review gate:
```

Self-evolution routing:

```text
strategy gap -> horizon-advisor
unclear compounding value -> leverage-advisor
unclear owner surface -> harness-advisor
proof or e2e behavior gap -> eval
new reusable workflow -> skill-creator
existing skill backpropagation -> skill-maintenance
material coding ticket -> impl-plan
selected executable frontier -> goal-advisor
measured variant search -> self-improve
material harness behavior gap -> optimize-harness
```

## Gotchas

- Do not skip diagnosis just because the operator used a confident phrase like
  "obviously." Name the concrete gap before changing the harness.
- Do not optimize raw agent hours. Optimize accepted evidence-backed output and
  validated improvement cycles per human intervention hour, with quality,
  proof, auditability, and operator control as constraints.
- Do not invent a numeric score when the honest signal is qualitative. Use
  scores as guided reasoning only when the evidence and proof surface are named.
- Do not use `self-improve` for ordinary implementation. Use it only when there
  is a metric, target surface, search space, baseline, and candidate comparison.
- Do not keep hard cases in a separate capture backlog. Hardcase is eval
  metadata for a runnable proof case.
- Do not add a new skill before checking the generated skill registry for an
  existing owner or consolidation target.
- Do not turn context isolation into vibes. Treat context bleed, missing source
  refs, self-approval, and cross-thread state loss as observable incidents to
  close through reports, evals, tickets, or skill backpropagation.
- Do not let this skill become a hidden autonomous loop. Visible artifacts,
  tickets, evals, and review receipts carry state.

## Reference Map

- [gap-analysis](../gap-analysis/SKILL.md) - diagnose current versus expected
  behavior and name the next owner.
- [horizon-advisor](../horizon-advisor/SKILL.md) - rewrite value function,
  KPI tree, project goals, or current frontier when the strategy is wrong.
- [leverage-advisor](../leverage-advisor/SKILL.md) - score compounding value
  for an existing feature, workflow, capability, or artifact.
- [harness-advisor](../harness-advisor/SKILL.md) - choose the primary harness
  placement surface.
- [eval](../eval/SKILL.md) - create, tag, and run proof cases including
  hardcase mode.
- [skill-creator](../skill-creator/SKILL.md) - create or reshape a reusable
  skill only when a stable workflow lacks an owner.
- [impl-plan](../impl-plan/SKILL.md) - plan material coding tickets and proof
  contracts before execution.
- [goal-advisor](../goal-advisor/SKILL.md) - compile selected frontiers into
  Goal Packets, native Goal prompts, heartbeats, or rollouts.
- [self-improve](../self-improve/SKILL.md) - run metric-driven experiments for
  skill or harness-surface optimization.
- [skill-maintenance](../skill-maintenance/SKILL.md) - apply skill-system
  template, registry, contract, and bulk maintenance changes.
- [review](../review/SKILL.md) - judge plans, skill changes, evals, proof, and
  completion claims.
- the native execution phase - final proof, writeback, and review routing
  for applied changes.
- [docs/fundamentals/harness-engineering-doctrine.md](../../docs/fundamentals/harness-engineering-doctrine.md) -
  Farplane placement doctrine.
- [docs/specs/self-improvement-contracts.md](../../docs/specs/self-improvement-contracts.md) -
  compact signatures and target self-improvement workflow.

## Output

Return or write:

- `Observed`
- `Expected`
- `Loss term`
- `Metric or reward signal`
- `Gap report`
- `Placement decision`
- `Proof or eval case`
- `Direct change or experiment route`
- `Accept / hold / rollback decision`
- `Review result`
- `Next concrete action`
