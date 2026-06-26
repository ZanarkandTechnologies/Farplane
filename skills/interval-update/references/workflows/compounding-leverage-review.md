---
title: "Compounding Leverage Review Workflow"
status: active
owner: interval-update
kind: workflow-reference
template_uses:
  skill-template: "0.3.2"
---

# Compounding Leverage Review Workflow

## Context

Use this workflow when a weekly or longer interval should ask: which
improvement bets would compound the project fastest next window? This is the
self-evolution planning lane. It belongs in interval planning because it needs
reports, goals, tickets, lessons, troubles, eval signals, and recent outcomes.

This workflow scores and routes. It does not implement the selected
experiments.

For Farplane self-evolution, optimize the harness-algebra objective:
increase validated meaningful improvement cycles per human intervention hour.
Accepted agent-hours count only when they produce reviewed artifacts or
accepted state deltas. Preserve quality, proof, auditability, operator control,
and context isolation as constraints.

## Workflow Signature

```text
compounding_leverage_review(context_bundle, review_window, planning_window,
                             harness_ref, goals_ref, workflow_findings?,
                             registries?)
  -> lever_inventory
   + leverage_scores
   + top_experiment_candidates
   + next_window_bets
   + reward_signals_to_check_next_window
   + goal_advisor_handoffs
   + source_gaps

state: reads(context_bundle, harness_ref, goals_ref, tickets, pulse_reports,
             interval_reports, docs/LESSONS.md?, docs/TROUBLES.md?,
             spec feature metadata?, docs/features/registry.jsonl?,
             docs/skills/registry.jsonl?);
       writes(parent_interval_update_report_section)
gates: loss_term_named; evidence_cited; 1_to_3_bets_only;
       owner_surface_named; proof_or_reward_signal_named;
       previous_reward_signals_closed_or_gap_labeled;
       urgent_escalation_high_confidence_only;
       leaf_work_routed_not_executed
routes: horizon-advisor | leverage-advisor | harness-advisor |
        proof-advisor | eval | skill-creator | skill-maintenance |
        impl-plan | goal-advisor | self-improve | optimize-harness
fails: giant wish list; vague self-improvement; hidden strategy rewrite;
       scoring without evidence; executing experiments inside the interval
```

## Source Contract

Default sources from the context bundle:

- `farplane/harness.md` for the static human thesis, durable leverage
  commitments, non-tradeoffs, agent authority, and charter change rule.
- `farplane/goals.md` for value function, goals, holds, and current milestone.
- review-window Pulse reports, interval reports, ticket outcomes, blockers, and
  worker evidence.
- `docs/LESSONS.md` and `docs/TROUBLES.md` for repeated misses and fixed
  lessons.
- recently created or changed skills, spec feature records, generated feature
  registry rows, eval results, review findings, tickets, reports, and explicitly
  supplied external source refs.

Optional sources:

- Spec feature metadata, `docs/features/registry.jsonl`, and
  `docs/skills/registry.jsonl` when present.
- Eval, review, QA, or telemetry refs when already loaded by the interval.
- Workflow findings from plan progress, goal drift, ticket board drift,
  attention drift, metrics, feedback, and opportunities.
- Prior interval reports that selected leverage bets or named reward signals.
- Recent skill, hook, validator, template, automation, feature, or docs changes
  inside `review_window`.
- Weekly self-evolution signals when available: accepted output, accepted
  agent-hours with proof, human intervention minutes, proof closure,
  false-completion/self-approval incidents, context isolation failures, source
  gaps, and skill-backpropagation events.

## Reward Closure Rule

Before selecting new leverage bets, inspect prior interval reports for selected
bets and reward signals whose review date or next interval has arrived.

Classify each previous bet:

- `accept`: the reward signal arrived and the lever should become normal
  practice, policy, documentation, or a follow-up rollout.
- `continue`: evidence is positive but incomplete; carry the same reward signal
  forward with a sharper proof check.
- `kill`: the bet failed, created drag, or no longer matches goals.
- `resize`: the bet was directionally right but too broad or too narrow.
- `source_gap`: the reward cannot be judged because the needed signal was not
  captured; route instrumentation, logging, reporting, or feedback collection.

Do not pick new bets until this closure pass is written into the interval
report's `Reward Closure` section.

## Advisor Boundaries

- `horizon-advisor`: use when the value function, KPI tree, north star,
  strategy axes, or current frontier itself should change.
- `harness-advisor`: use when a selected leverage bet challenges the static
  charter, durable leverage commitments, non-tradeoffs, or owner surface.
- `leverage-advisor`: use to score how an existing feature, workflow,
  capability, or artifact could compound value.
- Charter deltas: record in the interval report as human-approval-required
  proposals; do not patch `farplane/harness.md` inside this workflow.
- `proof-advisor`: use when the claim needs proof selection, proof-case design,
  or routing between deterministic tests, validators, eval, QA, visual QA,
  agent QA, review, and source-gap tickets.
- `eval`: use after eval is selected as the proof surface and runnable eval
  rows, judges, hardcases, or eval-run proof are needed.
- `skill-creator`: use only when a selected bet needs a new or meaningfully
  reshaped reusable skill with a stable trigger and repeatable workflow.
- `skill-maintenance`: use when existing skills need backpropagation from
  reports, lessons, troubles, eval findings, QA checklist gaps, or registry
  drift.
- `impl-plan`: use when a selected bet is a material coding ticket that needs a
  concrete implementation plan and proof contract before execution.
- `goal-advisor`: use only after a selected bet is concrete enough to become a
  ticket-backed Goal Packet or heartbeat execution loop.
- `self-improve`: use when the target surface needs measured variant search,
  baseline comparison, and promotion rules.
- `optimize-harness`: use when the whole observed-versus-expected harness
  behavior is the task and the workflow should diagnose, place, prove, change,
  and review the improvement end to end.

Advisor routing table:

```text
| Condition | Route | Output expected |
| --- | --- | --- |
| Value function, KPI tree, north star, strategy axis, or frontier changes | horizon-advisor | approval-required goals delta or strategy packet |
| Static thesis, durable leverage commitments, non-tradeoffs, or agent authority changes | harness-advisor | approval-required harness delta proposal |
| Candidate capability is valuable but compounding value is unclear | leverage-advisor | scored leverage play and proof step |
| Candidate is selected but owner surface is unclear | harness-advisor | primary owner surface and rejected alternatives |
| Behavior claim needs proof route, eval, hardcase, or e2e chain test | eval | proof surface, eval case, QA/review/validator route, or source-gap ticket |
| New reusable workflow is stable enough to package | skill-creator | skill package plan or skill package change |
| Existing skill needs lessons/troubles/eval findings backpropagated | skill-maintenance | hardening/refinement, eval-to-QA sync, registry/audit proof |
| Material coding change needs a plan before execution | impl-plan | ticket plan and proof contract |
| Selected bet is ready for execution | goal-advisor | ticket-backed Goal Packet or heartbeat-compatible handoff |
| Target needs measured candidate search | self-improve | baseline, candidates, metric, promotion recommendation |
| Whole harness behavior gap should be optimized end to end | optimize-harness | accepted change, experiment plan, or blocked report |
| Bet is small, obvious, and safe | ticket delta or Pulse guidance | bounded next action with reward signal |
| Signal cannot be judged | instrumentation, eval, feedback, or source ticket | source-gap closure path |
```

## Signal Policy

Leverage signals are not a new Farplane file type by default. They are source
claims extracted from existing artifacts: interval reports, Pulse reports,
tickets, lessons, troubles, skill/feature registry changes, eval/review
results, feedback refs, metric refs, opportunity refs, or supplied external
source refs.

If a project later proves that leverage signals need a separate state store,
add it with a ticket and migration proof. Until then, write selected, rejected,
expired, deferred, or escalated leverage decisions into the dated interval
report.

Urgent escalation may bypass weekly selection only when:

- confidence is high.
- loss term, evidence refs, review-by date, and owner route are explicit.
- The signal would lose meaningful value before the next weekly interval.
- The escalation creates a report, ticket, Goal Advisor handoff, or human
  approval request; it must not mutate strategy directly.

## Phase Boundary

Run inline when there are only a few obvious candidate levers. Use read-only
subagents for `leverage-advisor` or `harness-advisor` when the report has many
candidate surfaces or the owner-surface decision is material.

## Todo List

- [ ] 1. Bind the leverage objective.
  - [ ] Read the value function, goals, current milestone, holds, and recent
        interval evidence.
  - [ ] Read the static human thesis, durable leverage commitments,
        non-tradeoffs, agent authority, and change rule from
        `farplane/harness.md`.
  - [ ] Name the loss term being improved, such as human intervention, false
        completion, agent churn, coordination cost, ungrounded claims, brittle
        state loss, quality, or auditability.
  - [ ] For Farplane itself, review self-evolution signals as evidence:
        accepted output, accepted agent-hours with proof, intervention minutes,
        proof closure, false completion, context isolation failures, source
        gaps, and skill-backpropagation events.
  - [ ] Mark missing signals as source gaps instead of inventing precision.
- [ ] 2. Close previous reward signals.
  - [ ] Read prior interval reports for selected bets and reward signals whose
        check date is due.
  - [ ] Classify each previous bet as `accept`, `continue`, `kill`, `resize`,
        or `source_gap`.
  - [ ] Cite evidence from reports, tickets, Pulse outcomes, QA/eval results,
        feedback, metrics, or source gaps.
  - [ ] Write the closure result before selecting new bets.
- [ ] 3. Build a lever inventory.
  - [ ] Identify candidate levers from tickets, reports, lessons, troubles,
        evals, feature/skill registries, external source refs, and workflow
        findings.
  - [ ] Include recent skill, hook, validator, template, automation, feature,
        docs, or review-system changes inside `review_window`.
  - [ ] Dedupe candidates by lever, change type, and evidence refs.
  - [ ] Mark stale candidates as expired unless new evidence reopens them.
  - [ ] Group candidates by surface: skill, doc/spec, ticket contract, eval,
        validator, hook/script, automation prompt, subagent, UI, or project
        goal.
  - [ ] Treat repeated planning misses as likely backpropagation candidates for
        planning skills, interval workflows, evals, QA checklists, or report
        templates.
- [ ] 4. Score leverage.
  - [ ] Score candidates for compounding value, proof speed, reuse surface,
        operator-effort reduction, implementation friction, and rollout risk.
  - [ ] Treat scores as reasoning aids, not authoritative telemetry; cite why
        each score is plausible and which evidence would change it.
  - [ ] Use `leverage-advisor` when a candidate needs deeper scoring.
  - [ ] Use `harness-advisor` when the owner surface is unclear.
- [ ] 5. Choose next-window bets.
  - [ ] Pick 1-3 bets only.
  - [ ] For each bet, name the experiment, owner surface, expected output,
        reward signal, proof check, cost/risk, and next owner.
  - [ ] Prefer bets that reduce repeated planning misses, context bleed,
        source gaps, false completion, or skill-backpropagation delay.
- [ ] 6. Route execution.
  - [ ] Create proposed ticket deltas or Goal Advisor handoffs for selected
        bets.
  - [ ] Mark strategy/KPI/current-frontier changes as approval-required goals
        deltas and route them to `horizon-advisor`.
  - [ ] Mark static thesis, durable leverage commitment, non-tradeoff, or
        agent-authority changes as approval-required harness deltas and route
        them to `harness-advisor`.
  - [ ] Route proof gaps to `eval` before claiming the lever worked.
  - [ ] Route new reusable workflows to `skill-creator`; route existing skill
        backpropagation to `skill-maintenance`.
  - [ ] Route coding-ticket planning to `impl-plan` before `goal-advisor` when
        the implementation needs a plan/proof contract.
  - [ ] Route broad observed-versus-expected harness gaps to `optimize-harness`.
  - [ ] Record selected, rejected, deferred, expired, or escalated leverage
        decisions in the interval report.
  - [ ] Do not execute the selected bet inside this workflow.

## Templates

Reward closure table:

```text
| Previous bet | Expected reward | Observed result | Evidence | Decision |
```

Leverage table:

```text
| Lever | Surface | Loss term | Evidence | Compounding value | Cost/risk | Experiment | Reward signal | Next owner |
```

Scoring rubric:

```text
compounding_value:
  5 = improves many future runs or projects
  3 = improves one recurring workflow
  1 = one-off cleanup
proof_speed:
  5 = signal visible in next interval
  3 = signal visible in 2-3 intervals
  1 = slow or speculative
reuse_surface:
  5 = reusable skill/template/validator/hook/docs pattern
  3 = reusable inside this project
  1 = narrow local fix
operator_effort_reduction:
  5 = removes repeated human supervision or review burden
  3 = reduces a recurring decision or correction
  1 = little operator relief
implementation_friction:
  5 = hard, broad, or risky implementation
  3 = moderate implementation
  1 = easy patch or docs change
rollout_risk:
  5 = high chance of wrong autonomy, false confidence, or broad regression
  3 = contained behavior risk
  1 = reversible and low blast radius
```

Candidate score format:

```text
score = compound:<1-5>; proof_speed:<1-5>; reuse:<1-5>;
        operator_effort:<1-5>; friction:<1-5>; risk:<1-5>
```

Selection heuristic:

```text
Prefer high compound + high proof_speed + high reuse + high operator_effort
when friction and risk are low enough for the next planning window. Do not
select more than three bets even when many candidates score well.
```

Read-only subagent handoff:

```text
Read <context_bundle>. Run compounding_leverage_review for <review_window> and
<planning_window>. Return lever_inventory, leverage_scores, top 1-3 bets,
reward_signals_to_check_next_window, goal_advisor_handoffs, and source_gaps.
Do not mutate files or execute experiments.
```

## Gotchas

- This is not a prompt to improve everything. Pick a few bets with evidence.
- Leverage Advisor scores a capability; Harness Advisor places a harness
  change; Goal Advisor compiles selected execution.
- If the right move is to rewrite the value function or KPI tree, route to
  Horizon Advisor instead of hiding the strategy change in the weekly plan.
- If the right move is to rewrite the human thesis or static leverage
  commitments, route to Harness Advisor and human approval instead of hiding the
  charter change in products, goals, or the weekly plan.
- A new skill or feature is not automatically a lever. It becomes a lever only
  when there is evidence that using, hardening, or rolling it out changes a
  named loss term.
- A selected bet without a reward signal is not selected yet. Rewrite it until
  next interval can judge whether it worked.
- Skill updates are the backpropagation path. When daily or weekly reports show
  a repeated miss, decide whether it belongs in a new skill, existing skill
  hardening, eval, QA checklist, validator, or project-specific prompt.

## Reference Map

- Parent interval update loads this file only when
  `report_workflows.compounding_leverage_review` is enabled.
- `../../../leverage-advisor/SKILL.md` - score existing capabilities or workflows.
- `../../../harness-advisor/SKILL.md` - choose the owner surface for Farplane
  harness changes.
- `../../../goal-advisor/SKILL.md` - compile selected bets into Goal Packets.

## Output

```text
lever_inventory:
  - lever:
    surface:
    loss_term:
    evidence:
leverage_scores:
  - lever:
    compounding_value:
    proof_speed:
    reuse_surface:
    operator_effort_reduction:
    friction:
    rollout_risk:
top_experiment_candidates:
  - experiment:
    expected_output:
    proof_check:
    reward_signal:
next_window_bets:
  - bet:
    next_owner:
    route:
leverage_decisions:
  - decision:
    next_owner:
    reward_signal:
    evidence:
goal_advisor_handoffs:
source_gaps:
```
