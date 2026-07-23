---
name: pulse-update
description: "Run one bounded multi-phase Work Pulse: maintain state, service due reviews, dispatch executable tickets, refill low ready supply, and write one receipt."
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

Each wake runs five bounded phases in order; an earlier phase never suppresses
a later eligible phase:

1. Reconcile completed, failed, blocked, active, and review-ready work without
   treating human-active tickets as Pulse workers.
2. Derive matured delayed-reward check-ins and hand their original Goal
   Packets to a worker that executes the ticket-owned Check-In Program.
3. Select and dispatch executable tickets within worker capacity.
4. Request human review once per completed artifact, mark the ticket awaiting
   review, release the worker, repair malformed review ledgers, and execute
   policy-derived Telegram or Phone Chaser actions up to `review_chase_limit`
   without worker assignment. Keep the tickets distinct while projecting one
   bounded review pool per area for operator presentation.
5. When unclaimed ready supply after dispatch is below its configured low
   watermark, call the pure
   [plan next wave](../plan-next-wave/SKILL.md),
   materialize its admitted configured-skill calls, and dispatch within remaining capacity.

Hard output invariant: the canonical Pulse receipt is exactly one valid JSON
object with no YAML, Markdown fence, or prose around it. Whenever refill runs,
the response must render `pulse_receipt.planner_call` rather than only
narrating the decision.
That receipt carries the actual planning-input envelope, configured planning
skill refs, global-first history, goals, review-pool and operator-availability
state, optional World Memory, canonical proposed skill calls, and admitted call
IDs. A receipt that omits `planner_call`, configured skills, global history, or
the admitted call references is invalid.

Ticket dispatch is context-isolated:
`create_thread(complete_handoff) -> verify clean first turn -> set canonical
title -> claim/register`. Never fork the Pulse manager to create a worker.

Daily and Weekly Interval reports may supply current evidence and non-mutating
suggestions. They do not materialize planner calls or dispatch work in this
loop. Goal Advisor remains the execution compiler for material ticket work;
Pulse is the board manager, not the worker.

`dogfood-review` supplies a dated checkpoint only. Normal refill may read that
report as `current_context`; Dogfood cannot call a planner, allocation, or
materialization path.

## Skill Signature

```text
work_pulse(project_root, wave_size = 1, worker_limit = 1,
           review_wip = 3, review_chase_limit = 1,
           ready_low_watermark = 1, extensions?)
  -> reconciliation
   + maintenance_actions[]
   + review_service_actions[]
   + review_area_pools[]
   + worker_handoffs[]
   + refill_result?
   + blockers[]
   + report_ref
   + next_wake?

state:
  reads(farplane/harness.yaml?, farplane/metrics.yaml?, .farplane/metrics/**?,
        farplane/bindings.yaml?,
        farplane/automations.toml?, tickets/TASK-*/ticket.md,
        tickets/TASK-*/program.md?, tickets/TASK-*/progress.md?,
        ticket Reward.kpi_rewards[]?, Goal Packet Check-In Program?,
        tickets/archive/**, configured Feed Scout World Memory?,
        terminal AI-planned Reward preference rows?,
        latest dated interval/feed reports?,
        .farplane/state/ticket-thread-associations.jsonl?,
        .farplane/state/dispatch-circuit.json?, farplane/pm.json?)
  writes(tickets/TASK-*/ticket.md when admitted planner skill calls are materialized,
         .farplane/reports/pulse/<timestamp>.md,
         .farplane/automation/decisions.jsonl?,
         .farplane/state/ticket-thread-associations.jsonl?,
         .farplane/state/dispatch-circuit.json?,
         farplane/pm.json when a persistent project worker thread is created)

gates:
  board_reconciled; terminal_state_recorded; ticket_eligibility_checked;
  stale_guard_preflight_resolved_before_planning;
  due_reward_rows_derived; original_checkin_ticket_resumed;
  delayed_checkin_program_handed_off_without_reimplementation;
  matured_rows_handed_off_together; future_reward_rows_unchanged;
  review_status_excluded_from_execution; malformed_review_state_repaired;
  due_review_action_derived_from_progress_and_binding; review_chase_limit_respected;
  notification_credentials_owned_by_automation; phone_chaser_policy_respected;
  reminder_does_not_consume_worker; queue_size_does_not_trigger_chase;
  worker_limit_respected; human_active_ticket_does_not_consume_worker;
  review_pool_limit_respected; review_saturation_changes_selection_strategy;
  ready_low_watermark_checked_after_dispatch;
  maintenance_does_not_suppress_later_phases; review_service_does_not_consume_worker;
  wave_size_respected; configured_planning_skills_passed;
  passive_area_icps_passed; world_memory_loaded_once_for_fact_selection;
  preference_memory_normalized_from_terminal_rewards;
  skill_workflows_not_reconstructed; planner_output_qa_passed;
  pulse_owns_materialization;
  no_inline_ticket_implementation; ticket_program_progress_proof_handoff;
  clean_worker_task_created_without_manager_history;
  human_review_worker_released; side_effect_gates_respected;
  decision_and_report_written

routes:
  plan-next-wave | goal-advisor |
  worker-artifact-review-request | telegram-message | qa | review

fails:
  requires_or_invokes_product_controller; filters_tickets_by_product_origin;
  asks_interval_to_create_or_dispatch_work;
  creates_checkin_ticket; delegates_future_reward_row; asks_interval_to_evaluate_reward;
  duplicates_or_invents_checkin_decision_policy;
  conflates_wave_size_with_worker_limit; exceeds_review_area_pool_limit;
  globally_blocks_safe_dispatch_due_to_review_saturation;
  implements_ticket_in_parent_pulse; keeps_worker_alive_only_for_human_review;
  assigns_worker_to_review_action; chases_based_on_review_queue_size;
  lets_ticket_credential_scope_block_internal_notification;
  counts_human_ticket_claim_as_pulse_worker; spawns_area_planner;
  forks_manager_thread_for_ticket_worker; claims_worker_before_clean_lineage_verified;
  writes_planner_side_effects_before_call_validation; materializes_unconfigured_skill;
  returns_silent_no_op
```

## Automation Preset

```text
pulse-update @30m
  project_root = <project>
  wave_size = 1
  worker_limit = 1
  review_wip = 3
  review_chase_limit = 1
  ready_low_watermark = 1
```

Cadence only controls wake timing. It does not expand authority, worker
capacity, ticket scope, or external side-effect permission.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind project policy and reconcile state.
  - [ ] Resolve `project_root`, `wave_size`, `worker_limit`, `review_wip`,
        `farplane/harness.yaml` including optional goals, `farplane/metrics.yaml`, current metric readings,
        ticket paths, ticket-thread association index, latest ticket/progress
        outcomes, current dated context,
        and project side-effect gates. Read bindings only when provider or
        authority mechanics affect the current decision.
  - [ ] Before planner input is fingerprinted, resolve every configured hard
        guard at point of use. Run
        `scripts/guard_preflight.py begin --project-root <root> --date <date>`;
        dispatch each returned `refresh_ref` (or inline refresh) exactly once,
        even when it provides multiple stale guards, then reload through
        `guard_preflight.py finish`. This preflight is Pulse maintenance and
        consumes zero wave slots.
    - [ ] A refreshed current healthy guard continues into ordinary planning in
          the same Pulse.
    - [ ] A refreshed current failing guard blocks ordinary admission on the
          named real gap, not on observation age. Apply a safe bounded
          mechanical repair in Pulse maintenance when one exists; otherwise
          report or route the material underlying incident. Neither repair path
          enters the value portfolio or consumes wave capacity.
    - [ ] A failed, unavailable, or still-stale refresh returns an explicit
          source gap and no planner calls. Never ask Plan Next Wave to create a
          metric-refresh or observation-restoration ticket.
    - [ ] Start planning through `guard_preflight.py plan` (or the equivalent
          `begin_planning_if_ready` call) so `plan_wave_guard.py` cannot create
          the planning fingerprint until the reloaded receipt is current and
          healthy.
  - [ ] Run or emulate
        `python3 skills/pulse-update/scripts/list_pulse_board.py --project-root <root> --worker-limit <n> --review-wip <n> --now <iso-datetime>`.
  - [ ] Archive terminal active tickets when safe or record the exact archive
        action still required.
  - [ ] Record Pulse-owned active workers from the ticket-thread association index,
        human-active tickets, released blocked workers, awaiting-review
        tickets, missing outputs, and stale association rows. A `status: active`
        ticket without a live ticket-thread association row is unavailable for
        dispatch but does not consume `worker_limit`.
  - [ ] Project awaiting-review tickets into one pool per canonical area.
        `review_wip` limits those operator-facing pools, not the number of
        distinct ticket artifacts and not worker concurrency.
- [ ] 2. Handle completed, waiting, or matured work.
  - [ ] Reconcile ticket/program/progress/proof and outcome state before
        selecting new work.
  - [ ] Treat every `Reward.kpi_rewards[]` row with `check_in_at <= now` and a
        blank or `monitor` decision as due. Resume the original
        `status: waiting_signal` ticket; do not create a check-in
        ticket or findings row.
  - [ ] When one ticket has several matured rows, hand all of them to the same
        worker. Leave future and already-complete rows unchanged.
  - [ ] Hand the worker the original `ticket.md`, `program.md`, `progress.md`,
        exact matured Reward IDs, current timestamp, and evidence refs. Tell
        it to read `program.md` first and execute its `Check-In Program`, then
        return `accept`, `kill`, or `monitor`; do not restate the
        scoring or decision algorithm in Pulse.
  - [ ] If the original program is missing, stale, not in `delayed_reward`
        mode, or lacks executable evidence/decision rules, record the source
        gap and route Goal Advisor repair. Do not improvise a check-in policy.
  - [ ] When an artifact needs Kenji, route one request through
        [worker artifact review request](../worker-artifact-review-request/SKILL.md),
        record the receipt or blocker, set the ticket to awaiting review, and
        release the worker slot.
  - [ ] Read `progress.md` Review blocks for awaiting-review tickets and the
        structured `bindings.yaml#operator.review_chase_policy`. An
        awaiting-review ticket with no parseable Review block is a mechanical
        repair action, never a silent wait.
  - [ ] Select the oldest due actions up to `review_chase_limit`: retry a
        missing/blocked initial Telegram, send a configured Telegram reminder,
        or dispatch a configured Phone Chaser call. Execute them through
        `worker-artifact-review-request` without assigning workers.
  - [ ] Treat internal review notifications as automation-owned credential use;
        ticket-local no-credential/publication/account boundaries do not block
        notification delivery and notification grants no broader authority.
        Review WIP does not trigger chase or suppress planning.
  - [ ] Keep each ticket's Review block and decision canonical. Area pooling is
        a presentation and prioritization projection; it never merges tickets,
        Rewards, decisions, or proof obligations.
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
- [ ] 4. Run every bounded manager phase.
  - [ ] `maintenance`: archive all mechanically safe terminal work, reconcile
        stale worker association rows and ticket/progress outcomes, and derive due check-ins. This phase consumes
        no worker slot and never ends the beat by itself.
  - [ ] `review_service`: repair invalid ticket-owned review state and execute
        up to `review_chase_limit` policy-derived Telegram/phone actions without
        workers. Queue size alone never triggers chase.
  - [ ] `dispatch_ready`: choose ordinary executable tickets and original
        tickets with due check-ins, then create handoffs up to available worker
        slots. Saturated review pools do not globally block dispatch; prefer
        unattended-safe tickets with machine or delayed feedback and low
        immediate review load.
    - [ ] For a new ticket worker, use the app's clean `create_thread(prompt,
          project target)` path with the complete handoff as its initial prompt.
          Never use `fork_thread` for a ticket worker: a fork copies the Pulse
          manager's heartbeat history and is reserved for work whose source
          conversation is itself required context. Resume an existing task only
          when the durable ticket-thread association index already binds that task ID.
    - [ ] Before claiming the ticket or registering the worker, verify the
          returned task is the requested project task and begins from the
          delegation packet rather than inherited manager turns. Treat
          `forked_from_id`, pre-delegation heartbeat history, or unverifiable
          lineage as a failed launch: archive or release the bad task when safe,
          record the circuit failure, and leave the ticket unclaimed.
    - [ ] Treat worker create/lookup as a shared dispatch mechanism. After two
          consecutive non-returning or unverifiable attempts, open a circuit,
          stop repeating that launch on every wake, and record the health-check
          condition required to close it. Continue maintenance, review service,
          and safe refill while the circuit is open.
    - [ ] Before worker launch, run `scripts/dispatch_circuit.py probe`. Record
          each failed create/lookup with `failure --reason <reason>` and each
          verified success with `success`. An open circuit blocks ordinary
          launches for thirty minutes, then permits exactly one half-open probe;
          probe failure reopens it and verified success closes it.
    - [ ] Bound each worker create/lookup attempt to 30 seconds. If it has not
          returned with a verifiable thread ID, stop waiting, record `failure`,
          leave the ticket unclaimed, and continue later phases. Never hold the
          whole heartbeat open for coordination recovery.
  - [ ] `plan_next_wave`: after dispatch, call the planner when remaining
        unclaimed ready supply is below `ready_low_watermark`, even when
        maintenance, review service, dispatch, human-active tickets, or
        awaiting-review tickets also exist. Do not wait for spawned workers.
    - [ ] Build one canonical planning-input object containing
          `harness.planning.skill_refs` plus the complete passive
          `harness.areas` ICP/metric context. Add objectives/guards, optional
          goals, metric readings, global-first history, bounded terminal Reward preference memory,
          review-area-pool state, operator availability, optional
          Tasty Pack evidence for relevant content candidates, report refs,
          board state, and wave size. Include a derived `semantic_time_state`
          for metric freshness, goal urgency/deadline buckets, matured Reward
          IDs, and operator-availability validity; serialization time alone is
          not planning novelty. Call
          `scripts/plan_wave_guard.py begin` before planning. An identical
          completed fingerprint is `no_op_unchanged_input`; an active claim is
          `blocked_overlap`.
    - [ ] Build and fingerprint this object only after guard preflight. Include
          the refreshed guard reading, freshness, source ref, and refresh receipt
          in `metric_state` / `semantic_time_state`; do not pass stale guard
          state downstream and expect the planner to repair it.
    - [ ] Resolve `farplane/bindings.yaml#feed_scout.world_memory` once per
          planning call. When present, include its `updated_at`, complete
          relevant source-backed facts, confidence/freshness, source refs, and
          source gaps as `world_memory`. Do not replay all dated reports or
          treat World Memory as authority.
    - [ ] Derive `preference_memory` from terminal AI-planned Reward rows in the
          same global/progressive history: map `accept -> accept` and
          `kill -> reject`; omit `monitor`, blank, and pending. Preserve
          `actual_result`, `evaluated_at`, ticket plus `reward_id` provenance,
          applicability, reconsideration boundary, and evidence refs. Never
          infer preference from chat, World Memory, or Tasty Pack evidence.
  - [ ] `request_human`: record a precise blocker when value direction, authority, credentials, or a
        material source gap blocks both execution and safe planning.
  - [ ] `no_op`: only when reconciliation produced no due action and the exact
        reason is recorded.
- [ ] 5. Plan or dispatch without mixing ownership.
  - [ ] For refill, call
        `plan_next_wave(planning_skill_refs = harness.planning.skill_refs,
        areas = harness.areas, objective_contract, metric_goals = harness.goals,
        metric_state, ticket_history_query, current_context, world_memory,
        preference_memory, wave_size)` and accept only validated configured-skill
        calls. Resolve metric direction, freshness, and guards from
        `metrics.yaml`; reports remain optional current context.
  - [ ] Resolve each configured skill, read its `planner_contract`, and reject
        any call with an unconfigured skill, missing required argument, copied
        workflow or extra argument not declared in `required_arguments`.
  - [ ] Require the planner to read the latest global ticket history sample
        first through `farplane tickets history --json`; allow progressive
        origin/skill/area/KPI/status/Reward filters only when needed.
  - [ ] Pulse alone materializes each admitted call into the generic ticket
        template. The ticket records the selected skill and bound arguments,
        objective contribution, evidence, proof, authority, and stop boundary;
        it never copies the skill's todo/workflow.
  - [ ] Before materializing a batch, allocate collision-free IDs with
        `python3 skills/pulse-update/scripts/next_ticket_id.py --project-root <root>
        --count <n> --reserve`. The allocator atomically reserves a batch after
        scanning active and archived durable ticket paths plus frontmatter
        identities. Never infer the next ID from the active board alone.
  - [ ] Before materialization, serialize the exact planner response and run
        `plan-next-wave/scripts/validate_wave_response.py`; reject an invalid
        call rather than filling missing arguments or evidence in Pulse.
  - [ ] Materialize the validated admitted IDs through
        `scripts/materialize_skill_call.py --response <response.json>
        --ticket-id <allocated-id>...`; this deterministic seam writes only the
        generic call receipt, objective contribution, and proof placeholders.
  - [ ] Finish the atomic planning claim with admitted ticket IDs plus each
        selected `skill_ref` and optional passive `area_id`. The guard rejects duplicate IDs and admissions
        above `wave_size`; record `completed`, `no_op`, `source_gap`, or
        `human_request` in the existing decisions ledger and release the lock.
  - [ ] For each handoff, list `ticket.md`, optional `program.md`, optional
        `progress.md`, expected proof, authority gates, stop condition, and
        review route. Use Goal Advisor when the ticket requires Goal-backed
        continuation.
  - [ ] For a check-in handoff, require `program.md` and `progress.md`; list the
        exact matured Reward IDs, timestamp, and evidence refs, and set
        the instruction to execute `program.md` `Check-In Program` first.
  - [ ] Never implement the ticket body in the parent Pulse beat.
- [ ] 6. Write visible state.
  - [ ] Write a date-stamped Pulse report with Core report frontmatter:
        `ref`, `kind: pulse`, `created_at`, and `ui_summary`.
  - [ ] Record the mode, admitted/excluded tickets, planner result, worker
        handoffs, review receipts, side-effect boundary, and next wake.
  - [ ] Append only decision rows and ticket-thread association rows that
        actually changed; put outcome receipts in the Pulse report and
        ticket/progress state. Run `farplane reports index --project-root <root>` when
        available.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Worker Handoff Contract

```text
create_ticket_worker(complete_handoff, project_target, canonical_title)
  -> create_thread(initial_prompt = complete_handoff, target = project_target)
  -> verify(project_target + first_turn_is_delegation + no_inherited_history)
  -> set_title("[TASK-XXXX] <ticket title>")
  -> claim_ticket + register_worker

reject: fork_thread | claim_before_verification | title_as_ticket_identity
```

```yaml
worker_handoff:
  creation_mode: clean_thread # create_thread; never fork_thread for ticket workers
  ticket: tickets/TASK-XXXX/ticket.md
  program: tickets/TASK-XXXX/program.md | none
  progress: tickets/TASK-XXXX/progress.md | none
  expected_output:
  proof:
  authority_gates: []
  stop_condition:
  review_notify: worker-artifact-review-request | none_with_reason
  due_reward_ids: [] # stable reward_id values on the original ticket; empty for ordinary work
  checkin_evidence_refs: [] # delayed check-in sources; empty for ordinary work
  instruction: execute_ticket | execute_program_checkin
```

Default review transition:

```text
worker produces output + proof
-> sends one review request or records blocker
-> ticket becomes awaiting_review
-> progress.md records requested_at + Telegram/phone receipts + thread_ref
-> worker exits
-> Pulse may dispatch other eligible work
```

## Phase Outcomes

- `maintenance`: reconcile every safe mechanical action in the current board snapshot.
- `review_service`: repair malformed waits and execute at most
  `review_chase_limit` due Telegram/phone actions.
- `dispatch_ready`: hand off up to `idle_worker_slots` ordinary or due-check-in
  tickets. A due handoff resumes the existing Goal Packet and never creates a
  check-in ticket. Create or resume exactly one persistent task per ticket,
  titled `[TASK-XXXX] <ticket title>`; lifecycle state never changes the title.
  New tasks use clean creation with the handoff as their initial prompt. They
  never fork the Pulse manager or inherit its heartbeat transcript, and Pulse
  verifies that clean first turn before setting the canonical title, claiming
  the ticket, or writing the ticket-thread association. Ticket identity comes from the
  durable ticket ID and task ID, never parsed title text.
- `plan_next_wave`: obtain `0..wave_size` configured-skill calls when ready
  supply is below the low watermark, materialize the admitted calls, then
  dispatch only up to remaining capacity.
- `request_human`: write one precise request with attempted safe alternatives.
- `no_op`: write the reconciled reason and next wake; no silent completion.

Every mode ends with this compact receipt, including explicit `none` values:

```yaml
pulse_receipt:
  phases:
    maintenance: {archived: [], repaired: []}
    review_service: {actions: []}
    execution: {dispatched: [], idle_slots_after: 0}
    refill: {called: false, admitted: [], reason: none}
  guard_preflight:
    selected_guards: []
    refreshed: []
    current_healthy: []
    current_failing: []
    source_gaps: []
    wave_slots_consumed: 0
  admitted: []
  excluded: []
  planner_call:
    value: none | planned
    input_ref:
    planning_skill_refs: []
    passive_areas: []
    objective_contract: {}
    metric_goals: []
    metric_state: {}
    semantic_time_state: {}
    ticket_history_queries: []
    world_memory: none # or {updated_at, relevant_facts, source_gaps}
    preference_memory: [] # terminal Reward accept/kill rows only
    skill_receipts: []
    proposed_skill_calls: []
    admitted_call_ids: []
    review_pool_state: {limit: 0, active: [], queued: [], saturated: false}
    taste_evidence: none
    current_context: {}
    wave_size: 0
    admitted_skill_provenance: [] # ticket_id + skill_ref + optional passive area_id
  planner_writes_or_dispatches: false
  product_controller: none
  worker_handoffs: [] # each uses the full Worker Handoff Contract above
  review_action: none | {ticket, progress_ref, action, send_or_dispatch_receipt}
  report_ref:
  decision_or_outcome_rows: []
  next_wake:
```

The receipt is the minimum visible proof that Pulse made a bounded decision;
it is not an extra workflow or registry.

When `phases.refill.called` is `true`, `planner_call.value` must be `planned`
and the receipt must populate the canonical inputs shown above, including
configured skills, goals, global-first history, review-pool state, operator
availability, World Memory, preference memory, canonical proposed calls, and
admitted call IDs. Omission of the configured-skill or call receipt makes the
Pulse decision incomplete.

## Gotchas

- `wave_size` controls backlog creation; `worker_limit` controls concurrency.
- `ready_low_watermark` controls when planning compares the next portfolio; it
  does not force admission and may trigger after a dispatch in the same wake.
- A dispatch circuit breaker prevents repeated task-create/lookup outages from
  consuming every wake. It does not authorize inline ticket execution.
- Human-active tickets are board commitments, not Pulse workers. Only live
  ticket-thread association rows consume `worker_limit`.
- Review WIP caps operator-facing area pools. Saturation changes selection
  toward unattended-safe, machine-verifiable work; it is not a global dispatch
  block, planner suppression rule, reason to keep workers alive, or chase
  trigger.
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

- [plan next wave](../plan-next-wave/SKILL.md) -
  pure next-wave planning when ready supply is below its configured watermark.
- [worker artifact review request](../worker-artifact-review-request/SKILL.md) -
  phone-readable review request and receipt when a worker reaches human review.
- [goal-advisor](../goal-advisor/SKILL.md) - material ticket execution
  compilation from ticket/program/progress files.
- [Work Pulse feature](../../docs/features/FEAT-0071-project-work-pulse.md) -
  durable capability and proof contract.
