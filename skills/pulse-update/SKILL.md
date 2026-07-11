---
name: pulse-update
description: "Run one project Work Pulse: reconcile ordinary and due-check-in work, dispatch executable tickets, refill an empty board, request review, and write receipts."
tier: 3
group: harness
source: local
template_uses:
  skill-template: "0.2.0"
  skill-eval-task: "0.2.0"
eval: evals/evals.json
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Pulse Update

## Context

`pulse-update` is the one fast Work Pulse for a Farplane project. It manages
one board and one shared worker pool. It does not route through product-local
controllers.

Work Pulse owns five state-changing responsibilities:

1. Reconcile completed, failed, blocked, active, and review-ready work.
2. Derive matured delayed-reward check-ins and hand their original Goal
   Packets to a worker that executes the ticket-owned Check-In Program.
3. Select and dispatch executable tickets within worker capacity.
4. Request human review once, mark the ticket awaiting review, release the
   worker, and reconcile at most one due reminder without worker assignment.
5. When no executable ticket or due check-in exists, call the pure
   [ticket opportunity generator](../ticket-opportunity-generator/SKILL.md),
   materialize its accepted specs, and dispatch within remaining capacity.

Daily and Weekly Interval reports may supply current evidence and non-mutating
suggestions. They do not materialize planner specs or dispatch work in this
loop. Goal Advisor remains the execution compiler for material ticket work;
Pulse is the board manager, not the worker.

## Skill Signature

```text
work_pulse(project_root, wave_size = 1, worker_limit = 1,
           review_wip = 3, extensions?)
  -> reconciliation
   + execution_mode
   + ticket_deltas?
   + worker_handoffs?
   + human_review_requests?
   + report_ref
   + next_wake?

state:
  reads(farplane/harness.md?, farplane/goals.yaml?, farplane/metrics.yaml?,
        farplane/bindings.yaml?,
        farplane/automations.toml?, tickets/TASK-*/ticket.md,
        tickets/TASK-*/program.md?, tickets/TASK-*/progress.md?,
        ticket Reward.kpi_rewards[]?, Goal Packet Check-In Program?,
        tickets/archive/**, latest dated interval/feed reports?,
        .farplane/automation/spawned-threads.jsonl?,
        .farplane/automation/action-outcomes.jsonl?, farplane/pm.json?)
  writes(tickets/TASK-*/ticket.md when accepted planner specs are materialized,
         .farplane/reports/pulse/<timestamp>.md,
         .farplane/automation/decisions.jsonl?,
         .farplane/automation/spawned-threads.jsonl?,
         .farplane/automation/action-outcomes.jsonl?,
         farplane/pm.json when a persistent project worker thread is created)

gates:
  board_reconciled; terminal_state_recorded; ticket_eligibility_checked;
  due_reward_rows_derived; original_checkin_ticket_resumed;
  delayed_checkin_program_handed_off_without_reimplementation;
  matured_rows_handed_off_together; future_reward_rows_unchanged;
  review_status_excluded_from_execution;
  due_review_reminder_derived_from_progress; one_due_reminder_per_pulse;
  reminder_does_not_consume_worker; queue_size_does_not_trigger_chase;
  worker_limit_respected; review_wip_respected; empty_board_before_refill;
  wave_size_respected; planner_output_qa_passed; pulse_owns_materialization;
  no_inline_ticket_implementation; ticket_program_progress_proof_handoff;
  human_review_worker_released; side_effect_gates_respected;
  decision_and_report_written

routes:
  ticket-opportunity-generator | goal-advisor |
  worker-artifact-review-request | telegram-message | qa | review

fails:
  requires_or_invokes_product_controller; filters_tickets_by_product_origin;
  asks_interval_to_create_or_dispatch_work; plans_with_ready_work_available;
  creates_checkin_ticket; delegates_future_reward_row; asks_interval_to_score_reward;
  duplicates_or_invents_checkin_decision_policy;
  conflates_wave_size_with_worker_limit; exceeds_review_wip;
  implements_ticket_in_parent_pulse; keeps_worker_alive_only_for_human_review;
  assigns_worker_to_review_reminder; chases_based_on_review_queue_size;
  writes_planner_side_effects_before_candidate_qa; returns_silent_no_op
```

## Automation Preset

```text
pulse-update @30m
  project_root = <project>
  wave_size = 3
  worker_limit = 1
  review_wip = 3
```

Cadence only controls wake timing. It does not expand authority, worker
capacity, ticket scope, or external side-effect permission.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind project policy and reconcile state.
  - [ ] Resolve `project_root`, `wave_size`, `worker_limit`, `review_wip`,
        `farplane/harness.md`, `farplane/goals.yaml`, `farplane/metrics.yaml`,
        ticket paths, worker ledger, latest outcomes, current dated context,
        and project side-effect gates. Read bindings only when provider or
        authority mechanics affect the current decision.
  - [ ] Run or emulate
        `python3 skills/pulse-update/scripts/list_pulse_board.py --project-root <root> --worker-limit <n> --now <iso-datetime>`.
  - [ ] Archive terminal active tickets when safe or record the exact archive
        action still required.
  - [ ] Record active workers, released blocked workers, awaiting-review
        tickets, missing outputs, and stale ledger rows. Count a `status:
        active` ticket with `claimed_by` as occupied even when its worker-ledger
        row is missing; dedupe it against any matching active ledger row.
- [ ] 2. Handle completed, waiting, or matured work.
  - [ ] Reconcile ticket/program/progress/proof and outcome state before
        selecting new work.
  - [ ] Treat every `Reward.kpi_rewards[]` row with `check_in_at <= now` and
        missing `actual_result` or `reward_score` as due. Resume the original
        `status: waiting_signal` ticket; do not create a check-in
        ticket or findings row.
  - [ ] When one ticket has several matured rows, hand all of them to the same
        worker. Leave future and already-complete rows unchanged.
  - [ ] Hand the worker the original `ticket.md`, `program.md`, `progress.md`,
        exact matured row indexes, current timestamp, and evidence refs. Tell
        it to read `program.md` first and execute its `Check-In Program`, then
        return `accept`, `kill`, `iterate`, or `monitor`; do not restate the
        scoring or decision algorithm in Pulse.
  - [ ] If the original program is missing, stale, not in `delayed_reward`
        mode, or lacks executable evidence/decision rules, record the source
        gap and route Goal Advisor repair. Do not improvise a check-in policy.
  - [ ] When an artifact needs Kenji, route one request through
        [worker artifact review request](../worker-artifact-review-request/SKILL.md),
        record the receipt or blocker, set the ticket to awaiting review, and
        release the worker slot.
  - [ ] Read `progress.md` Review blocks for awaiting-review tickets. If one or
        more `next_reminder_at` values are due and undecided, select at most the
        oldest one and call the review-request wrapper in reminder mode without
        assigning a worker. Review WIP limits refill; it does not trigger chase.
  - [ ] Keep publish, post, spend, deploy, external contact, account mutation,
        and destructive actions gated even when local preparation is complete.
- [ ] 3. Admit executable tickets.
  - [ ] Ordinary work is executable when `status: todo`, `claimed_by` is
        absent, and dependencies are satisfied.
  - [ ] A `status: waiting_signal` ticket with a due Reward row is temporarily
        executable for its Check-In Program. Claims, dependencies, review
        state, and terminal-state exclusions still win.
  - [ ] Do not require product, product-lane, product-progress, or Reward
        metadata for ordinary or improvement tickets.
  - [ ] Treat `human_gate` as a final-action boundary: dispatch safe local work
        when it can stop before the gated action.
- [ ] 4. Choose one mode.
  - [ ] `dispatch_ready`: choose ordinary executable tickets and original
        tickets with due check-ins, then create handoffs up to available worker
        slots.
  - [ ] `plan_next_wave`: only when no ordinary executable ticket or due
        check-in exists, review WIP is below its limit, and current
        program/objective context is sufficient.
  - [ ] `request_human`: when value direction, authority, credentials, or a
        material source gap blocks both execution and safe planning.
  - [ ] `no_op`: only when reconciliation produced no due action and the exact
        reason is recorded.
- [ ] 5. Plan or dispatch without mixing ownership.
  - [ ] For refill, call
        `plan_next_wave(program, objective_contract, ticket_history,
        current_context, wave_size)` and accept only QA-passing executable
        specs. Bind `program` from `harness.md` and the objective contract from
        `goals.yaml` plus `metrics.yaml`; reports remain optional current
        context rather than a second planning owner.
  - [ ] Pulse alone materializes accepted specs as ticket files, then reruns
        admission before dispatch.
  - [ ] For each handoff, list `ticket.md`, optional `program.md`, optional
        `progress.md`, expected proof, authority gates, stop condition, and
        review route. Use Goal Advisor when the ticket requires Goal-backed
        continuation.
  - [ ] For a check-in handoff, require `program.md` and `progress.md`; list the
        exact matured Reward row indexes, timestamp, and evidence refs, and set
        the instruction to execute `program.md` `Check-In Program` first.
  - [ ] Never implement the ticket body in the parent Pulse beat.
- [ ] 6. Write visible state.
  - [ ] Write a date-stamped Pulse report with Core report frontmatter:
        `ref`, `kind: pulse`, `created_at`, and `ui_summary`.
  - [ ] Record the mode, admitted/excluded tickets, planner result, worker
        handoffs, review receipts, side-effect boundary, and next wake.
  - [ ] Append only the decision/outcome/worker ledger rows that actually
        changed; run `farplane reports index --project-root <root>` when
        available.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Worker Handoff Contract

```yaml
worker_handoff:
  ticket: tickets/TASK-XXXX/ticket.md
  program: tickets/TASK-XXXX/program.md | none
  progress: tickets/TASK-XXXX/progress.md | none
  expected_output:
  proof:
  authority_gates: []
  stop_condition:
  review_notify: worker-artifact-review-request | none_with_reason
  due_reward_rows: [] # indexes on the original ticket; empty for ordinary work
  checkin_evidence_refs: [] # delayed check-in sources; empty for ordinary work
  instruction: execute_ticket | execute_program_checkin
```

Default review transition:

```text
worker produces output + proof
-> sends one review request or records blocker
-> ticket becomes awaiting_review
-> progress.md records requested_at + next_reminder_at + thread_ref
-> worker exits
-> Pulse may dispatch other eligible work
```

## Execution Modes

- `dispatch_ready`: hand off up to `idle_worker_slots` ordinary or due-check-in
  tickets. A due handoff resumes the existing Goal Packet and never creates a
  check-in ticket.
- `plan_next_wave`: obtain `0..wave_size` specs, materialize accepted specs,
  then dispatch only up to remaining worker capacity.
- `request_human`: write one precise request with attempted safe alternatives.
- `no_op`: write the reconciled reason and next wake; no silent completion.

Every mode ends with this compact receipt, including explicit `none` values:

```yaml
pulse_receipt:
  mode:
  admitted: []
  excluded: []
  planner_call: none | {program, objective_contract, ticket_history, current_context, wave_size}
  planner_writes_or_dispatches: false
  product_controller: none
  worker_handoffs: [] # each uses the full Worker Handoff Contract above
  review_reminder: none | {ticket, progress_ref, send_receipt}
  report_ref:
  decision_or_outcome_rows: []
  next_wake:
```

The receipt is the minimum visible proof that Pulse made a bounded decision;
it is not an extra workflow or registry.

## Gotchas

- `wave_size` controls backlog creation; `worker_limit` controls concurrency.
- Review WIP is human-attention backpressure, not a reason to keep workers
  alive and not a chase trigger.
- A product or capability may appear inside a ticket without becoming a Pulse
  controller.
- Improvement and ordinary tickets use the same admission and handoff path.
- Due Reward rows are a generated eligibility projection. Ticket Reward and
  Goal Packet files remain canonical state; Pulse does not add check-in
  metadata.
- Pulse owns due-row derivation and dispatch, not experiment scoring policy.
  A delayed experiment without an executable Check-In Program is a repairable
  source gap, not permission for Pulse to infer one.

## Reference Map

- [ticket opportunity generator](../ticket-opportunity-generator/SKILL.md) -
  pure next-wave planning when no executable ticket exists.
- [worker artifact review request](../worker-artifact-review-request/SKILL.md) -
  phone-readable review request and receipt when a worker reaches human review.
- [goal-advisor](../goal-advisor/SKILL.md) - material ticket execution
  compilation from ticket/program/progress files.
- [Work Pulse feature](../../docs/features/FEAT-0071-project-work-pulse.md) -
  durable capability and proof contract.
