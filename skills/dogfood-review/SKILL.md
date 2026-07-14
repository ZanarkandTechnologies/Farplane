---
name: dogfood-review
description: "Review the weekly self-improvement portfolio, plan a reserved five-ticket experiment wave, and hand admitted specs to Pulse for materialization."
tier: 3
group: harness
source: local
template_uses:
  skill-template: "0.3.7"
eval: evals/evals.json
qa_checklist: qa_checklist.md
allowed-tools: Read, Glob, Grep, Bash
---

# Dogfood Review

## Context

Use this skill from the weekly self-improvement automation or manually.
Dogfood is the retrospective and reserved allocator for the existing
`self_improvement` planning area, not another heartbeat or executor. It
snapshots experiment state through a cutoff, carries prior outcomes into a
dated report, then uses the same `plan-next-wave` history, Reward, dedupe,
guard, and executable-spec gates to target five new self-improvement tickets.
Pulse remains the only ticket materializer and worker/check-in manager.

The weekly cutoff is not an experiment deadline. Pulse and the original ticket
worker own execution and check-ins at the times declared by each Goal Packet.
Dogfood only observes ticket state that already exists.

The weekly wave may mix immediate experiments, delayed experiments, and
human-feedback experiments. Immediate work routes through native Goal and
`self-improve`; delayed work keeps its future signal and executable Check-In
Program in the original Goal Packet; human-feedback work routes through
`optimize-with-human`. Iterations stay inside the original ticket.

## Skill Signature

```text
weekly_self_improvement(project_root, window, cutoff,
                        active_experiment_refs?, recent_archive_refs?,
                        previous_dogfood_report?, registry_refs?, reports?, metrics?,
                        ticket_history_query = `farplane tickets history`,
                        area_instruction_ref = `harness.areas.self_improvement.planner_instruction`,
                        weekly_ticket_target = 5,
                        recovery_ticket_limit = 1,
                        max_concurrent_live_delayed = 5,
                        one_active_per_attributable_surface = true,
                        write_policy = pulse_materialization_only)
  -> dogfood_report
   + outcome_ledger
   + active_and_pending_portfolio
   + due_checkin_pending_gaps
   + transfer_candidates
   + rejected_patterns
   + weekly_allocation_receipt
   + ranked_improvement_candidates
   + admitted_self_improvement_specs[0..weekly_ticket_target]
   + pulse_materialization_receipt
   + materialized_ticket_paths[0..weekly_ticket_target]
   + source_gaps
   + no_op_reason?

state:
  reads(farplane/harness.yaml, farplane/metrics.yaml?, .farplane/metrics/**?,
        farplane/harness.yaml `areas.self_improvement` complete record,
        `farplane tickets history --json` global and self_improvement receipts,
        `farplane skills rollout scan --json`, skill/eval/QA/template health,
        tickets/TASK-*/{ticket,program,progress}.md,
        tickets/archive/TASK-*/{ticket,program,progress}.md,
        ticket-owned artifacts, previous Dogfood report, current Pulse/Interval/
        Feed Scout reports, completed core:ticket-completion-learning@1.1.0
        reports and their ticket_output receipts, feature/system registries,
        operator/reviewer evidence)
  writes(.farplane/reports/dogfood-review/<timestamp>.md)
  requests(pulse-update materialization of admitted specs)
  pulse_writes(tickets/TASK-*/{ticket,program,progress}.md, admission receipts)

gates:
  qa_preflight_loaded; cutoff_bound; active_and_recent_archive_read;
  prior_report_used_as_cursor_not_canonical_state; existing_results_reviewed_first;
  report_written_before_selection; outcome_and_source_gaps_recorded;
  reserved_area_is_self_improvement; global_history_before_area_filter;
  canonical_self_improvement_instruction_loaded_and_applied;
  five_ticket_target_or_explicit_shortfall; one_active_per_surface;
  delayed_live_cap_respected; executable_spec_gate_passed;
  pulse_only_materialization; no_execution_or_checkin

routes:
  optimize-harness | self-improve | skill-maintenance | consolidate |
  doc-advisor | eval | optimize-with-human | review | pulse-update

fails:
  treating cutoff as an experiment deadline; deciding a matured Reward row;
  hiding due-check-in-pending work; losing archived outcomes; duplicating a prior
  rejected pattern without new evidence; blocking unrelated immediate proof
  merely because delayed work is monitoring; creating conflicting experiments;
  using active WIP to erase the weekly allocation; creating filler to reach five;
  writing ticket files outside Pulse; executing, checking in, promoting, rolling
  back, or spawning an experiment during the review
```

## Phase Boundary

Dogfood derives cross-ticket learning, writes the report, and invokes the one
planner in `reserved_area:self_improvement` scope. Ticket Reward rows,
`program.md`, `progress.md`, and artifacts remain canonical experiment state.
The previous Dogfood report is only a cursor for carryover, dedupe, and transfer
status. Pulse materializes admitted specs; workers later execute ticket-owned
programs and Pulse resumes matured check-ins.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind and preflight the portfolio.
  - [ ] Read `qa_checklist.md`, cutoff/window, harness objectives/metrics,
        active Goal Packets, recent archived Goal Packets, the previous Dogfood
        report when present, and current reports/registry evidence.
  - [ ] Load the complete `harness.areas.self_improvement` record and treat
        `harness.areas.self_improvement.planner_instruction` as the canonical
        candidate-generation policy. Do not restate or narrow that policy in
        Dogfood; return an exact instruction-use receipt.
  - [ ] Run `farplane tickets history --limit 20 --json` without filters first,
        then progressively query `self_improvement`, Reward decisions, status,
        KPI, or a wider window. Preserve expected/actual Reward fields and
        `area_derivation` ambiguity.
  - [ ] Read current skill/template rollout, eval and QA coverage, configured
        harness metrics, and recurring correction evidence. Treat UI-only
        health projections as diagnostic evidence rather than canonical Reward.
  - [ ] Identify experiments from complete Goal Packet, experiment intent, or
        Reward/program evidence without adding ticket metadata; record missing
        files, metrics, receipts, or proof as source gaps.
- [ ] 2. Derive the portfolio snapshot without checking anything in.
  - [ ] For each experiment, read Reward rows, Metric Provider, Check-In
        Program, wake/stop/rollout policy, progress tail, and cited evidence.
  - [ ] Classify canonical Reward state at `cutoff`: blank decisions are
        pending or due, `monitor` decisions are monitoring or monitor-due, and
        only `accept` or `kill` are settled. Results settled after cutoff belong
        to the next report.
  - [ ] Treat `reward_id` as row identity. Aggregate terminal decisions and
        their recorded evidence without changing `actual_result`, `decision`,
        evaluation keys, or check-in time.
  - [ ] Build the outcome ledger, active/pending view, transfer candidates, and
        rejected patterns. Do not infer a terminal result that the ticket has
        not recorded.
  - [ ] Read new completed ticket-completion learning reports and their
        projected-ticket receipts since the prior Dogfood cursor. Treat their
        compact findings and created/existing/no-ticket decisions as portfolio
        evidence; do not recreate their tickets, edit a skill, or rewrite
        doctrine.
- [ ] 3. Write the dated report before proposing new work.
  - [ ] Use `templates/dogfood-report.md`; carry prior-report transfer/rejection
        status forward only when confirmed by canonical tickets and evidence.
  - [ ] Record due-check-in-pending gaps, attribution/proof quality, feature/system
        findings, history-query receipts, harness-health findings, and a
        no-execution receipt; index the report when available.
- [ ] 4. Generate and rank the reserved weekly portfolio.
  - [ ] Record every nonterminal experiment, including monitoring and
        due-check-in-pending work. Active WIP informs conflicts, delayed load,
        worker/review burden, and same-surface admission, but does not subtract
        from the five new weekly slots.
  - [ ] Compute `available_delayed_slots = max(0,
        max_live_delayed - active_live_delayed)`; enforce it across the selected
        wave plus one active experiment per attributable surface. A
        due-check-in-pending experiment blocks dependent/conflicting supply only;
        delayed monitoring does not block unrelated immediate toy/replay/eval
        work while weekly allocation remains.
  - [ ] Apply `harness.areas.self_improvement.planner_instruction` across four
        evidence lanes: prior ticket Reward outcomes and
        rejected patterns; harness-health gaps weighted by heat/composition;
        `leverage-advisor` plays over accepted capabilities; and observed
        failure/loss-term placements through `harness-advisor` plus harness
        algebra when needed.
  - [ ] Rank attributable hardening, refinement, docs, feature, policy,
        automation, hook/validator, metric, and context-selection candidates by
        objective impact, proofability, compounding value, cost, risk, and
        operator/review load. Reject duplicates and interference explicitly.
  - [ ] Treat a recurring request to improve a skill or artifact with human
        taste as an ordinary feedback experiment candidate, not a Taste Loop
        automation or standing worker.
- [ ] 5. Admit and materialize zero to five complete self-improvement specs.
  - [ ] Every candidate names area, surface, hypothesis, baseline, expected
        Reward and guard, metric/provider, proof route, horizon, cost/risk,
        budget, stop condition, and promotion/rollback rule.
  - [ ] Mark the proposed feedback shape as immediate toy/replay/eval,
        human-feedback, or delayed. Delayed candidates include the required
        future signal and check-in procedure outline so planner admission can
        materialize a complete Goal Packet without inventing the experiment.
  - [ ] Call `plan-next-wave` with `planning_scope =
        reserved_area:self_improvement` and `wave_size = weekly_ticket_target`.
        Pass the complete `harness.areas.self_improvement` record and require
        `harness.areas.self_improvement.planner_instruction` in the returned
        area-instruction receipt and every admitted spec's ranking trace.
        Require the same complete executable spec, direct-value/preventive
        mechanism, guard, dedupe, authority, proof, and artifact gates as Pulse.
  - [ ] Target five admitted specs. Return fewer only for named hard guards,
        same-surface conflicts, duplicates, source gaps, delayed-live limits, or
        candidates that cannot become complete executable experiment specs.
        Never admit filler merely to reach five.
  - [ ] Every admitted spec names `feedback_class` and a complete route:
        immediate Goal with no future check-in; delayed Goal Packet with stable
        Reward row and executable Check-In Program; or human-feedback Goal
        Packet routed through `optimize-with-human`.
  - [ ] Send the accepted spec batch to Pulse's bounded materialization route.
        Dogfood must not write ticket files itself, dispatch workers, or run any
        experiment body. Record returned ticket IDs and exact area attribution.
  - [ ] A settled known-fix recovery may occupy one of the five slots only when
        its spec names the recurring failure, preventive mechanism, existing
        KPI/guard, and next-run proof; it is not an extra sixth ticket.
  - [ ] Completion learning already projects at most one direct-fix or
        prove-or-reject ticket. Reconcile that ticket in history and dedupe and
        never create a second recovery or experiment ticket for the same
        report/semantic dedupe key.
- [ ] 6. Finish-check and hand off.
  - [ ] Reapply `qa_checklist.md`; return report, outcome/history/health views,
        ranking, admitted specs, Pulse materialization receipt, ticket paths,
        shortfall reasons, and proof that no experiment body, check-in,
        promotion, rollback, or external action ran.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

- [Weekly Dogfood report](templates/dogfood-report.md) - outcome ledger,
  portfolio/capacity snapshot, candidate ranking, and packet-wave receipts.

## Gotchas

- `check_in_at <= cutoff` means Pulse can resume the original packet; it does
  not authorize Dogfood to score it.
- `accept` and `kill` are the only settled Reward decisions. `monitor` remains
  live and consumes delayed/surface capacity until its updated check-in
  matures, but does not erase unrelated weekly allocation.
- Dogfood aggregates canonical terminal outcomes; it never converts legacy
  score fields, expected-reward declarations, or missing evidence into realized
  value and never rescales a worker's decision.
- Planner quality is derived by joining Pulse-admitted ticket IDs to eventual
  Reward decisions in this weekly portfolio view. Do not create an independent
  plan score, plan-wave registry, or real-time planner mutation loop.
- An accepted toy result is evidence for a bounded transfer/pilot candidate,
  not permission for doctrine-wide rollout.

## Reference Map

- [Feature registry guide](../../docs/features/README.md) - load when tracked
  or experimental features are in the review set.
- [System registry guide](../../docs/systems/README.md) - load when tracked
  systems are in the review set.
- [Self Improve](../self-improve/SKILL.md) - downstream measured search route,
  not weekly selection.
- [Pulse Update](../pulse-update/SKILL.md) - execution and due-check-in owner.

## Output

One dated retrospective portfolio report; a reserved five-spec
`self_improvement` wave or explicit shortfall; Pulse materialization paths; and
a no-experiment-execution/check-in receipt.
