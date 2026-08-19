---
title: Work Pulse Runbook
owner: pulse-update
status: active
kind: skill-reference
---

# Work Pulse Runbook

Load this for every operated Pulse wake. `SKILL.md` owns admission and output
gates; this file owns the conditional mechanics.

## 1. Reconcile And Refresh Guards

1. Read the ticket board, Goal Packets, ticket-task association index, review
   blocks, current metrics, configured stable problems/areas/planning skills,
   side-effect policy, and current report evidence.
2. Run `scripts/guard_preflight.py begin --project-root <root> --date <date>`.
   Dispatch each returned `refresh_ref` or inline refresh once, even if it
   serves several stale guards, then reload with `guard_preflight.py finish`.
3. Continue the same wake when the refreshed guard is current and healthy.
   When current and failing, block admission on its named real gap and perform
   only an available bounded mechanical repair. When refresh fails or remains
   stale, return a source gap and no planner calls.
4. Start planning through `guard_preflight.py plan` so the planning fingerprint
   cannot exist before the refreshed state is current and healthy.
5. Run or emulate `scripts/list_pulse_board.py --project-root <root>
   --worker-limit <n> --review-wip <n> --now <iso>` and archive mechanically
   safe terminal work. Record stale associations and missing outputs.

Only live Pulse-owned ticket-task associations consume `worker_limit`.
Human-active tickets do not. An active ticket with no live association is
unavailable for dispatch but consumes no slot.

## 2. Delayed Reward And Review Service

- A Reward row is due when `check_in_at <= now` and its decision is blank or
  `monitor`. Resume its original `waiting_signal` ticket. Group all matured
  rows from that ticket into one handoff and leave future/completed rows alone.
- The handoff includes the original `ticket.md`, `program.md`, `progress.md`,
  exact Reward IDs, current time, and evidence refs. The worker reads the
  program first and executes its Check-In Program to return `accept`, `kill`,
  or `monitor`.
- Missing, stale, non-`delayed_reward`, or non-executable program state is a
  Goal Advisor repair gap. Pulse never invents scoring or creates a check-in
  ticket.
- For review, require the Review `thread_ref` to match the durable ticket-task
  association. Emit `repair_thread_identity` on mismatch; never resume through
  the manager task or create a duplicate worker.
- An unparseable Review block is a mechanical repair, not a silent wait.
  Select the oldest due retry/reminder/phone actions up to
  `review_chase_limit` and execute through
  `worker-artifact-review-request` without assigning a worker.
- Internal review notifications use automation-owned credentials. This does
  not weaken publication, account, spend, deploy, contact, or destructive
  action gates. Review queue size alone never triggers chase or suppresses
  planning.
- Pool awaiting-review tickets by canonical area only for presentation and
  prioritization. Never merge ticket, Reward, decision, or proof state.

## 3. Dispatch

Ordinary work is eligible when `status: todo`, unclaimed, dependencies are
satisfied, and no review/terminal exclusion wins. A waiting-signal ticket is
temporarily eligible only for due Reward rows. `human_gate` blocks only the
gated final action; safe local work may stop before it.

For a new worker:

1. Run `scripts/dispatch_circuit.py probe`.
2. Call the app's clean `create_thread` with the complete handoff and project
   target. Never use `fork_thread` for ticket work.
3. Bound create/lookup to 30 seconds. Verify target, task ID, and that the first
   turn is the delegation packet with no inherited manager history.
4. On success, set `[TASK-XXXX] <ticket title>`, then claim and register. On
   failure, leave unclaimed and record `failure --reason <reason>`.
5. After two consecutive unverifiable/non-returning attempts, open the circuit.
   It blocks launches for 30 minutes, permits one half-open probe, reopens on
   failure, and closes only after a verified success. Maintenance, review, and
   safe refill continue while it is open.

The handoff names ticket/program/progress refs, expected output and proof,
authority gates, stop condition, review route, due Reward IDs, check-in
evidence, and `execute_ticket | execute_program_checkin`. Goal Advisor owns
material continuation. Pulse never implements ticket bodies.

## 4. Refill

After dispatch, refill when remaining unclaimed ready supply is below
`ready_low_watermark`; do not wait for workers. Build and fingerprint the
planning envelope only after guard preflight. It includes:

- configured `harness.planning.skill_refs`, stable identity problems, complete
  passive area ICPs, objectives/guards, current metric readings/movement, and
  refresh receipts;
- global-first ticket history from `farplane tickets history --json`, with
  progressive filters only when needed;
- semantic time for metric freshness, matured Rewards, and operator validity;
- review-area pools, operator availability, current reports, and relevant
  Tasty Pack evidence;
- the configured `feed_scout.scout_brief` loaded once, including `updated_at`,
  complete selected facts, confidence/freshness, refs, and gaps;
- terminal AI-planned Reward preferences only: `accept -> accept`,
  `kill -> reject`; omit blank, monitor, and pending while preserving ticket,
  Reward ID, result, evaluated time, applicability, reconsideration, and refs.

Run `scripts/plan_wave_guard.py begin`; identical completed input is
`no_op_unchanged_input`, and an active claim is `blocked_overlap`. Call Plan
Next Wave with the exact configured skills and envelope. For each returned
call, read the selected skill's `planner_contract`; reject unconfigured skills,
missing required arguments, undeclared extras, or copied workflows.

Before writing:

1. Validate the serialized response with
   `plan-next-wave/scripts/validate_wave_response.py`.
2. Reserve collision-free IDs with
   `scripts/next_ticket_id.py --project-root <root> --count <n> --reserve`.
3. Materialize through `scripts/materialize_skill_call.py --response
   <response.json> --ticket-id <id>...`. The seam writes only the generic call
   receipt, objective contribution, and proof placeholders.
4. Finish the planning claim with admitted IDs, selected `skill_ref`, optional
   `area_id`, and `completed | no_op | source_gap | human_request`. Enforce
   unique IDs and the `wave_size` cap.

## 5. Phase Outcomes

- `maintenance`: perform every safe mechanical reconciliation.
- `review_service`: repair invalid waits and run capped due review actions.
- `dispatch_ready`: hand off up to idle slots, including original due check-ins.
- `plan_next_wave`: return `0..wave_size` calls, materialize them, then dispatch
  only within remaining capacity.
- `request_human`: record one precise blocker plus safe alternatives attempted.
- `no_op`: record the reconciled reason and next wake; never return silently.

## 6. Canonical Receipt

Return exactly one JSON object with these fields; use explicit `null`, empty
arrays, or empty objects rather than omitting a branch:

```json
{
  "pulse_receipt": {
    "phases": {
      "maintenance": {"archived": [], "repaired": []},
      "review_service": {"actions": []},
      "execution": {"dispatched": [], "idle_slots_after": 0},
      "refill": {"called": false, "admitted": [], "reason": null}
    },
    "guard_preflight": {
      "selected_guards": [], "refreshed": [], "current_healthy": [],
      "current_failing": [], "source_gaps": [], "wave_slots_consumed": 0
    },
    "admitted": [],
    "excluded": [],
    "planner_call": {
      "value": null,
      "input_ref": null,
      "planning_skill_refs": [],
      "stable_problems": [],
      "passive_areas": [],
      "objective_contract": {},
      "metric_state": {},
      "semantic_time_state": {},
      "ticket_history_queries": [],
      "scout_brief": null,
      "preference_memory": [],
      "skill_receipts": [],
      "proposed_skill_calls": [],
      "admitted_call_ids": [],
      "review_pool_state": {},
      "taste_evidence": null,
      "current_context": {},
      "wave_size": 0,
      "admitted_skill_provenance": []
    },
    "planner_writes_or_dispatches": false,
    "product_controller": null,
    "worker_handoffs": [],
    "review_action": null,
    "report_ref": null,
    "decision_or_outcome_rows": [],
    "next_wake": null
  }
}
```

When refill ran, `planner_call.value` is `planned` and every observed planning
input, proposed call, admitted ID, and provenance row is populated. The dated
Pulse report carries Core frontmatter (`ref`, `kind: pulse`, `created_at`,
`ui_summary`) plus outcomes and blockers; index it when available.
