---
name: dogfood-review
description: "Review the weekly self-improvement portfolio, carry experiment outcomes forward, and create a bounded non-interfering wave of experiment Goal Packets."
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
Dogfood is a portfolio learner and ticket supplier, not another heartbeat or
executor. It snapshots experiment state through a cutoff, carries prior
outcomes into a dated report, then may create a capacity-limited next wave.

The weekly cutoff is not an experiment deadline. Pulse and the original ticket
worker own execution and check-ins at the times declared by each Goal Packet.
Dogfood only observes ticket state that already exists.

Human-taste improvement is not a separate controller. When human judgment is
the honest reward, Dogfood may create a normal feedback experiment Goal Packet
that routes through `optimize-with-human`; Work Pulse executes it, and the
ticket-owned Review block waits for the reply without holding a worker.

## Skill Signature

```text
weekly_self_improvement(project_root, window, cutoff,
                        active_experiment_refs?, recent_archive_refs?,
                        previous_dogfood_report?, registry_refs?, reports?, metrics?,
                        experiment_wave_size = 2,
                        experiment_wip_limit = 3,
                        max_concurrent_live_delayed = 1,
                        one_active_per_attributable_surface = true,
                        write_policy?)
  -> dogfood_report
   + outcome_ledger
   + active_and_pending_portfolio
   + due_but_unscored_gaps
   + transfer_candidates
   + rejected_patterns
   + capacity_receipt
   + ranked_improvement_candidates
   + experiment_goal_packets[0..experiment_wave_size]
   + source_gaps
   + no_op_reason?

state:
  reads(farplane/harness.md, farplane/goals.yaml?, farplane/metrics.yaml?,
        tickets/TASK-*/{ticket,program,progress}.md,
        tickets/archive/TASK-*/{ticket,program,progress}.md,
        ticket-owned artifacts, previous Dogfood report, current Pulse/Interval/
        Feed Scout reports, feature/system registries, operator/reviewer evidence)
  writes(.farplane/reports/dogfood-review/<timestamp>.md,
         optional tickets/TASK-XXXX/{ticket,program,progress}.md[0..wave_size])

gates:
  qa_preflight_loaded; cutoff_bound; active_and_recent_archive_read;
  prior_report_used_as_cursor_not_canonical_state; existing_results_reviewed_first;
  report_written_before_selection; outcome_and_source_gaps_recorded;
  capacity_and_non_interference_proved; one_active_per_surface;
  delayed_live_cap_respected; packet_wave_cap_respected;
  canonical_ticket_and_goal_templates_reused; no_execution_or_checkin

routes:
  optimize-harness | self-improve | skill-maintenance | consolidate |
  doc-advisor | eval | optimize-with-human | review | pulse-update

fails:
  treating cutoff as an experiment deadline; scoring a matured Reward row;
  hiding due-but-unscored work; losing archived outcomes; duplicating a prior
  rejected pattern without new evidence; blocking unrelated immediate proof
  merely because delayed work is monitoring; creating conflicting experiments;
  creating a bare ticket or delayed packet without executable Check-In Program;
  executing, promoting, rolling back, or spawning an experiment
```

## Phase Boundary

Dogfood derives cross-ticket learning and chooses the next bounded experiment
wave. Ticket Reward rows, `program.md`, `progress.md`, and artifacts remain
canonical experiment state. The previous Dogfood report is only a cursor for
carryover, dedupe, and transfer status. Work Pulse later admits and dispatches
the packets; the worker executes the original `program.md`.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind and preflight the portfolio.
  - [ ] Read `qa_checklist.md`, cutoff/window, harness objectives/metrics,
        active Goal Packets, recent archived Goal Packets, the previous Dogfood
        report when present, and current reports/registry evidence.
  - [ ] Identify experiments from complete Goal Packet, experiment intent, or
        Reward/program evidence without adding ticket metadata; record missing
        files, metrics, receipts, or proof as source gaps.
- [ ] 2. Derive the portfolio snapshot without checking anything in.
  - [ ] For each experiment, read Reward rows, Metric Provider, Check-In
        Program, wake/stop/rollout policy, progress tail, and cited evidence.
  - [ ] Classify state at `cutoff` as settled, pending, monitoring,
        due-but-unscored, inconclusive, accepted, killed, iterating, or source
        gap; results settled after cutoff belong to the next report.
  - [ ] Build the outcome ledger, active/pending view, transfer candidates, and
        rejected patterns. Do not infer a terminal result that the ticket has
        not recorded.
- [ ] 3. Write the dated report before proposing new work.
  - [ ] Use `templates/dogfood-report.md`; carry prior-report transfer/rejection
        status forward only when confirmed by canonical tickets and evidence.
  - [ ] Record due-but-unscored gaps, attribution/proof quality, feature/system
        findings, and a no-execution receipt; index the report when available.
- [ ] 4. Compute capacity and rank candidates.
  - [ ] Count every nonterminal experiment toward total WIP, including
        monitoring and due-but-unscored work. Compute
        `available_slots = min(wave_size, max(0, wip_limit - active_wip))`.
  - [ ] Compute `available_delayed_slots = max(0,
        max_live_delayed - active_live_delayed)`; enforce it across the selected
        wave plus one active experiment per attributable surface. A
        due-but-unscored experiment blocks dependent/conflicting supply only;
        delayed monitoring does not block unrelated immediate toy/replay/eval
        work while total capacity remains.
  - [ ] Rank attributable hardening, refinement, docs, feature, policy,
        automation, hook/validator, metric, and context-selection candidates by
        objective impact, proofability, compounding value, cost, risk, and
        operator/review load. Reject duplicates and interference explicitly.
  - [ ] Treat a recurring request to improve a skill or artifact with human
        taste as an ordinary feedback experiment candidate, not a Taste Loop
        automation or standing worker.
- [ ] 5. Write zero to `available_slots` complete Goal Packets.
  - [ ] Reuse canonical ticket and Goal Packet templates; create one folder per
        independent experiment with `ticket.md`, `program.md`, and `progress.md`.
  - [ ] Every ticket names surface, hypothesis, baseline, Reward expectation and
        guard, metric/provider, proof route, budget, and promotion/rollback rule.
  - [ ] Immediate toy/replay/eval packets use native Goal with an immediately
        available signal and no future `check_in_at`, event wake, or delayed
        Check-In Program debt.
  - [ ] Human-feedback packets name the artifact, one decision question,
        `optimize-with-human` provider, reply thread, and review-state policy;
        their waiting state consumes review WIP but no execution worker.
  - [ ] Delayed packets set Reward `check_in_at` or an event wake and completely
        fill the canonical `program.md` Check-In Program: `inputs`, ordered
        `procedure`, matured-row-only `writeback`, `decisions`, `idempotency`,
        and `source_gap`, backed by Metric Provider, Heartbeat Policy, Stop
        Conditions, and Rollout Policy.
  - [ ] Default packets to `status: awaiting_review` unless `write_policy`
        explicitly grants `status: todo` admission and no human/external gate
        remains. Link all
        created packets from the report and append initialization progress only.
- [ ] 6. Finish-check and hand off.
  - [ ] Reapply `qa_checklist.md`; return report/packet paths, outcome and
        capacity receipts, ranking, source gaps/no-op reason, and proof that no
        experiment, check-in, promotion, rollback, or external action ran.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

- [Weekly Dogfood report](templates/dogfood-report.md) - outcome ledger,
  portfolio/capacity snapshot, candidate ranking, and packet-wave receipts.
- [Canonical ticket template](../../tickets/templates/ticket.md) - selected
  experiment scope, Reward rows, and Done / Proof.
- [Canonical Goal program](../../tickets/templates/goal-loop/program.md) and
  [progress template](../../tickets/templates/goal-loop/progress.md) - load
  whenever creating a packet; delayed packets must fill Check-In Program.

## Gotchas

- `check_in_at <= cutoff` means Pulse can resume the original packet; it does
  not authorize Dogfood to score it.
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

One dated portfolio report; zero to the capacity-bounded wave of complete
experiment Goal Packets; and a no-execution/check-in receipt.
