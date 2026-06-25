---
name: pulse-update
description: "Run the Farplane fast executor loop: reconcile outcomes, execute ready tickets up to policy cap, request planning when blocked, and update ledgers."
tier: 3
group: harness
source: local
template_uses:
  skill-template: "0.2.0"
  skill-eval-task: "0.1.0"
eval: eval_task.json
allowed-tools: Read, Glob, Grep, Bash

---

# Pulse Update

## Context

Use this skill for the Farplane Pulse loop: immediate attention, reward
reconciliation, ready-ticket execution, planning requests, and worker handoff
writeback. It does not own drift review, scrum reflection, strategy, product
lane selection, or scheduled planning. It may read interval guidance as
constraints, but its job is to execute the board, not decide what the board
should contain.

This skill should be easy to pilot by changing cadence and extensions, without
rewriting the action logic. Interval controls when Pulse wakes; policy controls
what it may do.

## Automation Presets

`pulse-update.executor @30m -> reports.pulse`

Pulse resolves the standard Farplane project refs by default: the static
project charter, local tickets, recent interval guidance, project products,
local product skill refs under `.agents/skills/`, execution policy, spawned
threads, outcomes, rewards, reports, and
`farplane/pm.json`. The live Codex automation supplies cadence, concurrency cap,
and true project extensions only. Pulse owns reward reconciliation, proceedable
ticket admission, execution handoff shape, planning-request reporting, and
decision/outcome ledger writes.

Empty-board behavior is simple: if no proceedable ticket exists and no
mechanical admission repair is available, Pulse writes `request_planning` with
the source gap, idle reason, and board evidence. Daily or Weekly Interval owns
creating, splitting, or reprioritizing work from `farplane/products.md`.

Proceedable ticket selection is a hard gate. Pulse must not select local ticket
implementation work unless the ticket is `ready: true`,
`approval_required: false`, `blocked_by: []`, `claimed_by:` empty, dependency
satisfied, not `phase: complete` or `status: done`, not parked, and not waiting
on external credentials, human feedback, deploy, publish, spend, or other
non-computer-actionable input.

## Skill Signature

```text
pulse_update(project_root, extensions?, pulse_policy?)
  -> reward_update
   + execution_mode
   + child_thread_handoffs?
   + planning_request?
   + decision_row
   + ledger_delta

state:
  reads(farplane/harness.md?,
        farplane/goals.md?,
        farplane/products.md?,
        .agents/skills/**/SKILL.md?,
        .farplane/reports/interval/**?,
        .farplane/automation/heartbeat-policy.json,
        .farplane/automation/spawned-threads.jsonl,
        .farplane/automation/action-outcomes.jsonl,
        tickets/TASK-*/ticket.md,
        farplane/pm.json?)
  writes(.farplane/reports/pulse/<YYYY-MM-DDTHHMMSSZ>.md,
         .farplane/automation/decisions.jsonl,
         .farplane/automation/spawned-threads.jsonl,
         .farplane/automation/rewards.jsonl,
         farplane/pm.json when persistent PM-owned worker threads are spawned)

gates:
  default_refs_resolved; extensions_merged; board_loaded; rewards_reconciled;
  proceedable_ticket_admission_checked; execution_cap_respected;
  side_effect_gates_respected; decision_recorded;
  pm_thread_grouping_updated_when_persistent

routes:
  goal-advisor | impl-plan | feed-scout | skill-maintenance |
  eval | qa | review

fails:
  performing drift review or weekly scrum planning; rediscovering strategy
  every beat; creating product-shaped refill tickets in Pulse; executing broad
  work in the parent heartbeat; treating goal-advisor as the default empty-board
  fallback; treating interval as authority; skipping reward/outcome writeback;
  using planner-level exploration before reward learning proves value
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind policy and context.
  - [ ] Resolve standard Farplane refs for ticket board, latest interval
        guidance, static project charter, project products, execution policy,
        local product skill refs from admitted tickets, spawned thread rows,
        recent outcomes, report paths, and `farplane/pm.json`.
  - [ ] Merge caller-supplied extensions for execution caps, budgets, gates, or
        extra context refs.
  - [ ] Treat interval guidance as constraints only; do not perform drift review
        or weekly scrum planning inside Pulse.
- [ ] 2. Reconcile previous outcomes.
  - [ ] Inspect prior spawned thread rows and expected outputs.
  - [ ] Apply immediate rewards for completed, partial, blocked, noisy, or
        missing-output child work.
  - [ ] Avoid double-counting already rewarded outcomes.
- [ ] 3. Admit ready tickets.
  - [ ] Build the proceedable set from local ticket state. Treat `ready: false`,
        `approval_required: true`, nonempty `blocked_by`, nonempty
        `claimed_by`, incomplete dependencies, `phase: complete`,
        `status: done`, parked next actions, and external or human gates as hard
        exclusions.
  - [ ] Respect `maxChildThreadsPerBeat`, open child-thread limits,
        parallelizability notes, side-effect gates, and action authority.
  - [ ] Prefer tickets that match the latest interval guidance, but do not
        perform strategy ranking inside Pulse.
- [ ] 4. Choose execution mode.
  - [ ] If proceedable tickets exist, choose `execute_ready_tickets` and execute
        every admitted ticket up to policy cap.
  - [ ] If no ticket is proceedable but a purely mechanical ticket metadata or
        proof-state repair would make an existing ticket executable, choose
        `repair_ticket_admission_state`.
  - [ ] If no executable work exists because the queue is empty, vague, stale,
        blocked by product/goal judgment, or undersupplied, choose
        `request_planning` and record the exact planning request for Daily or
        Weekly Interval.
  - [ ] Choose `no_op_blocked` only when execution, mechanical repair, and
        planning request are all blocked or unsafe.
- [ ] 5. Spawn or record.
  - [ ] For each admitted ticket, create a named child-thread handoff with
        objective, context refs, local product skill ref when present, gates,
        expected outputs, reward horizon, and stop condition.
  - [ ] If the child is a persistent PM-owned worker chat that should appear
        under the project employee in the UI, append its thread ID to
        `farplane/pm.json` `threads.chats`.
  - [ ] If no child is needed, write the repair or planning request result
        directly.
- [ ] 6. Write decision state.
  - [ ] Append decision, spawned-thread, reward, and report rows.
  - [ ] Write a date-stamped Pulse report and keep newest-report pointers in
        state when needed.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

- execution mode.
- reward update summary.
- child thread ids, repair result, planning request, or blocked reason.
- expected outputs and reward horizon.
- report and state paths.

## Execution Modes

- `execute_ready_tickets`: execute all ready, unblocked, unclaimed,
  dependency-satisfied, approval-free, non-parked, non-complete,
  parallelizable tickets up to policy cap.
- `repair_ticket_admission_state`: perform only mechanical repair that can make
  an existing ticket executable, such as stale ready/approval/phase metadata or
  missing proof-state links. Do not make product or strategy decisions here.
- `request_planning`: write a planning request for Daily or Weekly Interval
  when the board lacks executable work or needs product/goal judgment. Include
  queue evidence, idle reason, and suggested planning scope.
- `no_op_blocked`: stop only when execution, repair, and planning request are
  all blocked, unsafe, or would create noisy work.
