---
name: dogfood-review
description: "Reduce all self-improvement ticket evidence for an interval into one dated portfolio checkpoint and bounded planner context."
tier: 3
group: operations
source: local
template_uses:
  skill-template: "0.3.9"
eval: evals/evals.json
qa_checklist: qa_checklist.md
allowed-tools: Read, Glob, Grep, Bash
---

# Dogfood Review

## Context

Use this weekly or manually to learn from the complete `self_improvement`
portfolio. Dogfood is the cadence-triggered reducer for SYS-0007: it joins
ticket-owned observations into a dated checkpoint and makes that report
available to normal Plan Next Wave as `current_context`.

Dogfood is not a planner, ticket materializer, executor, check-in worker, or
skill mutator. Plan Next Wave keeps configured-skill binding, cross-horizon
ranking, and `0..wave_size` admission. Pulse alone materializes, dispatches,
checks in, and records Reward decisions.

## Skill Signature

```text
weekly_self_improvement(project_root, window, cutoff,
                        previous_report?, ticket_history_query?,
                        reports?, metrics?, registry_refs?)
  -> dogfood_report
   + outcome_ledger
   + live_portfolio
   + due_checkin_gaps
   + portfolio_selection_lessons[]
   + opportunity_signals[]
   + planner_context_ref
   + source_gaps[]

state:
  reads(farplane/harness.yaml areas.self_improvement,
        cutoff-bound paginated exact admission receipts,
        every still-live earlier self_improvement ticket,
        tickets/**/{ticket,program,progress}.md, Reward rows and artifacts,
        previous Dogfood checkpoint, owning self-improvement ticket packets,
        metrics, feature/system/skill health and operator/reviewer evidence)
  writes(.farplane/reports/dogfood-review/<timestamp>.md)

gates:
  qa_and_golden_loaded; cutoff_bound; exact_area_receipts_or_source_gap;
  all_matching_pages_read; all_live_earlier_packets_read;
  ticket_truth_not_rewritten; report_written; stable_pattern_ids;
  no_execution; no_materialization; no_checkin; no_reward_decision;
  no_skill_mutation; planner_context_only

routes: plan-next-wave current_context | self-improve | skill-maintenance |
        eval | optimize-with-human | review | pulse-update

fails:
  declared_experiments_only; target_ticket_quota; planner_or_allocation_api;
  duplicate_target_skill_lessons; ambiguous_area_treated_as_canonical;
  missing_outcomes_as_zero; direct_ticket_write; execution_or_checkin
```

## Phase Boundary

Ticket Goal Packets own observations, causal evidence, check-ins, and Reward
decisions. For skill optimization, the owning ticket's instantiated
`program.md` owns the harden/refine policy; target-local self-improve files are
legacy notes, not active state. Dogfood owns interval joins and
portfolio-selection lessons only. The previous report is a cursor/checkpoint,
never canonical ticket state.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Read `qa_checklist.md`, the relevant owner-local golden example,
  cutoff/window, complete `harness.areas.self_improvement`, metrics, previous
  checkpoint, and current registry/report evidence.
- [ ] 2. Reconstruct the complete portfolio.
  - [ ] Run `farplane tickets history --area self_improvement --all --json` and
        require `receipt.exhausted: true`; then apply the cutoff and include
        every still-live earlier ticket. A numeric limit is not a complete
        portfolio receipt.
  - [ ] Treat missing receipt or ambiguous `area_derivation` as a source gap;
        do not infer membership from a convenient KPI.
  - [ ] Read each packet's Reward rows, program/check-in policy, progress tail,
        artifacts, reviewer/QA receipts, and cited target-memory version.
- [ ] 3. Join outcomes without mutating them.
  - [ ] Preserve pending, monitoring, due, accepted, killed, iterating, and
        source-gap state; missing or immature signals never become zero.
  - [ ] Keep ticket evidence canonical. Dogfood may record stable portfolio
        pattern IDs and refs but never copy target-skill rules.
  - [ ] Compare ultimate-outcome forecasts with external evidence only;
        enabler/guard completion is not realized revenue, reach, or subscriptions.
- [ ] 4. Write one dated report using `templates/dogfood-report.md`.
  - [ ] Include every matched ticket, live conflict, due-check-in gap, forecast
        error, accepted/rejected portfolio pattern, qualified and deprioritized
        opportunity signal, history-query receipt, source gap, and exact cursor.
  - [ ] Emit `planner_context_ref` to the report. Do not generate executable
        skill calls or invoke a planner/allocation API.
- [ ] 5. Finish-check and hand off.
  - [ ] Reapply `qa_checklist.md` and record no-execution,
        no-materialization, no-check-in, no-Reward-decision, and no-mutation
        receipts.
  - [ ] Normal Plan Next Wave may later read the report as bounded
        `current_context`; it derives capacity-based `wave_size` and competes
        self-improvement with all areas.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

For a prompt-heavy or judgment-dependent portfolio checkpoint, first read
[the golden portfolio checkpoint](examples/golden/portfolio-checkpoint.md) with
`qa_checklist.md`. Transfer invariants, never fixture facts or wording; an
independent reviewer receives the candidate, golden invariants, QA, and
held-out context, but not planner scratch reasoning.

- [Weekly Dogfood report](templates/dogfood-report.md) — complete interval
  checkpoint and planner-context receipt.
- [Golden portfolio checkpoint](examples/golden/portfolio-checkpoint.md) — load
  during planning and independent review; transfer invariants, not fixture facts.

## Guardrails

- Read scope is complete and cutoff-bound; output admission remains elsewhere.
- `query.limit: all` plus `receipt.exhausted: true` is the mechanical no-cap
  proof; a large fixed limit is not pagination or exhaustion evidence.
- `accept` and `kill` are terminal only when the owning ticket recorded them.
- A direct known fix remains a normal planner signal or existing projected
  ticket; Dogfood does not create it.
- Accepted toy evidence suggests a transfer test, not doctrine-wide rollout.
- Every pattern/lesson reference has a stable ID, scope, source ticket/Reward/
  evidence refs, status, and target-memory ref when promoted.

## Output

One dated portfolio checkpoint, complete reconstruction/query receipts,
portfolio-selection lessons, source-bound opportunity signals, a
`planner_context_ref`, and explicit proof that Dogfood performed no planning,
materialization, execution, check-in, Reward decision, or skill mutation.

## Gotchas

- A missing result is pending or a source gap, never zero.
- KPI fallback is ambiguous membership unless an exact admission receipt exists.
- Portfolio lessons do not authorize a ticket, Reward decision, or skill edit.

## Reference Map

- [QA checklist](qa_checklist.md) — reconstruction and no-action gates.
- [Report template](templates/dogfood-report.md) — dated checkpoint shape.
- [Golden checkpoint](examples/golden/portfolio-checkpoint.md) — transferable
  quality invariants for planning and held-out review.
