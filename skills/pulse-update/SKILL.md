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
allowed-tools: Read, Write, Glob, Grep, Bash

---

# Pulse Update

## Context

Use this skill for the Farplane Pulse loop: immediate attention, worker
portfolio management, reward reconciliation, ready-ticket execution, tactical
next-wave planning, and worker handoff writeback. It does not own drift review,
scrum reflection, strategy, product-boundary decisions, or scheduled planning.
It may read Weekly and Daily strategy as constraints. Its job is to keep useful
worker throughput high inside policy: execute the board, manage open worker
threads, remind or record waiting human-review workers when useful, and when the
board is empty instantiate the next safe tactical wave from already-accepted
strategy.
Pulse should have founder-like ambition inside these gates: generate bold,
bounded tactical ideas from the current `farplane/ops-memory.md` belief state,
fresh strategy inputs, and board evidence, then let Daily and Weekly intervals
challenge that belief from observed outcomes. Do not add a separate idea ledger;
use Pulse reports, interval reports, tickets, rewards, metrics, and ops memory.
Planning stays in the parent Pulse beat. Worker tickets are for execution: every
ticket Pulse creates or admits must be immediately actionable by a worker and
must produce a concrete artifact, proof packet, local state change, QA result,
draft, rendered asset, dataset, or review receipt that advances a named
`farplane/products.md` product, lane, or artifact workflow. An artifact is not
enough by itself; it must contribute to the product portfolio instead of being
generic busywork. Do not create tickets whose main output is planning more
tickets, choosing a direction, refreshing strategy, or deciding what should be
done next.

This skill should be easy to pilot by changing cadence and extensions, without
rewriting the action logic. Interval controls when Pulse wakes; policy controls
what it may do.

## Automation Presets

`pulse-update.executor @30m -> reports.pulse`

Pulse resolves the standard Farplane project refs by default: the static
project charter, long-term goals, project bindings, active ops memory, local
tickets, recent interval guidance, project products, local product skill refs
under `.agents/skills/`, execution policy, spawned threads, outcomes, rewards,
reports, and
`farplane/pm.json`. The live Codex automation supplies cadence, concurrency cap,
and true project extensions only. Pulse owns reward reconciliation, proceedable
ticket admission, execution handoff shape, planning-request reporting, and
decision/outcome ledger writes.

Empty-board behavior is bounded. If no proceedable ticket exists and no
mechanical admission repair is available, Pulse first checks
`farplane/goals.yaml`, `farplane/bindings.yaml`, `farplane/ops-memory.md` when
present, the latest Weekly and Daily strategy inputs, and
`farplane/products.md` lane weights. Ops memory supplies the active focus,
active projects, managed open worker notes, critical paths, next frontier,
constraints, and parking lot. When those inputs are fresh and safe, Pulse may
create a small next wave of tactical tickets from the active frontier and
immediately admit them through the same hard gates. Each next-wave decision
should name the active belief, frontier, bottleneck, or reward signal being
tested so the next Daily or Weekly report can keep, revise, or drop that
belief. If a manager-level note, ops-memory correction, ticket closure receipt,
or prioritization judgment is required, Pulse should do that directly in the
parent beat or write `request_planning`; it should not delegate that thinking
as a worker ticket. When strategy or ops memory is missing, stale, unsafe, or
requires product/goal judgment, Pulse writes `request_planning` with the source
gap, idle reason, and board evidence.

Open human-review workers are not board-wide blockers. If a worker has finished
local artifacts, AI review, QA, or a prep packet and is waiting on Kenji for
review or a final human-gated action, Pulse should leave that thread open,
record the waiting reason in the report or ops memory, ask the worker thread to
send a phone-viewable Telegram reminder when the reminder is useful and not
noisy, then continue safe local work when capacity remains. Human review
backlog should bias Pulse away from spawning more human-review-heavy tickets
and toward local artifact, research, experiment, proof, QA, packaging, or draft
content work.

Proceedable ticket selection is a hard gate. Pulse must not select local ticket
implementation work unless the ticket is `ready: true`,
`approval_required: false`, `blocked_by: []`, `claimed_by:` empty, dependency
satisfied, not `phase: complete` or `status: done`, not parked, and not waiting
on external credentials or other non-computer-actionable input. A compact
`human_gate` frontmatter value is a final-action gate, not a ticket-start gate:
`human_gate: none` means the worker can finish normally; `human_gate: [tag,
"reason"]` means the worker may prepare local artifacts and proof but must stop
before the tagged final action. Gate tags are project policy from
`farplane/bindings.yaml` `human_gates`, such as `post`, `publish`, `spend`,
`deploy`, `external_contact`, `account_mutation`, or `destructive_cleanup`.

## Skill Signature

```text
pulse_update(project_root, extensions?, pulse_policy?)
  -> reward_update
   + execution_mode
   + child_thread_handoffs?
   + next_wave_ticket_deltas?
   + planning_request?
   + decision_row
   + ledger_delta

state:
  reads(farplane/harness.md?,
        farplane/goals.yaml?,
        farplane/bindings.yaml?,
        farplane/products.md?,
        farplane/ops-memory.md?,
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
         tickets/TASK-*/ticket.md when plan_next_wave_when_empty creates safe tactical tickets,
         farplane/pm.json when persistent PM-owned worker threads are spawned)

gates:
  default_refs_resolved; ops_memory_resolved_or_gap_labeled;
  strategy_inputs_resolved_or_gap_labeled;
  bindings_resolved_or_gap_labeled; open_worker_threads_reconciled;
  extensions_merged; board_loaded; rewards_reconciled;
  proceedable_ticket_admission_checked; lane_weight_bias_checked;
  next_wave_tickets_rewarded_when_created; execution_cap_respected;
  side_effect_gates_respected; decision_recorded;
  pm_thread_grouping_updated_when_persistent

routes:
  goal-advisor | impl-plan | feed-scout | skill-maintenance |
  eval | qa | review

fails:
  performing drift review or weekly scrum planning; rediscovering strategy
  every beat; creating strategy-shaped or unsafe refill tickets in Pulse;
  executing broad work in the parent heartbeat; treating goal-advisor as the
  default empty-board fallback; treating interval as authority;
  skipping reward/outcome writeback; using planner-level exploration before
  reward learning proves value; generating tickets without parseable
  Reward.kpi_rewards plus guard; planning every possible project instead of the active
  frontier; duplicating caps or cadence from heartbeat policy into ops memory;
  treating open human-review threads as board-wide blockers; bundling local
  artifact creation with post/publish/spend/deploy/external-contact final
  actions when a safe prep ticket would keep throughput moving; creating worker
  tickets whose main deliverable is to plan, prioritize, refresh strategy,
  choose future tickets, or otherwise hand planning back to Pulse
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind policy and context.
  - [ ] Resolve standard Farplane refs for ticket board, `farplane/ops-memory.md`
        when present, latest interval guidance, latest Weekly and Daily
        strategy inputs, `farplane/goals.yaml`, `farplane/bindings.yaml`, static
        project charter, project products and lane weights, execution policy,
        local product skill refs from admitted tickets, spawned thread rows,
        recent outcomes, report paths, and `farplane/pm.json`.
  - [ ] Read `farplane/bindings.yaml` for operator behavior inputs such as
        human gate tags, active-time or notification preferences when present,
        and worker-cap extensions supplied by the caller or policy.
  - [ ] Merge caller-supplied extensions for execution caps, budgets, gates, or
        extra context refs.
  - [ ] Treat Weekly/Daily strategy as constraints and tactical inputs only; do
        not perform drift review, KPI mutation, product-boundary decisions, or
        weekly scrum planning inside Pulse.
- [ ] 2. Reconcile previous outcomes.
  - [ ] Inspect prior spawned thread rows and expected outputs.
  - [ ] Inspect open worker/thread rows or app-visible worker state when
        available. Classify completed, active, waiting-human-review, waiting
        final-action, blocked, stale, and missing-output workers.
  - [ ] For waiting human-review or final-action workers, record the ticket,
        thread id, waiting reason, last notification when visible, and whether
        a worker-context Telegram reminder is useful or noisy. Do not let those
        workers block safe unrelated work.
  - [ ] Apply immediate rewards for completed, partial, blocked, noisy, or
        missing-output child work.
  - [ ] Avoid double-counting already rewarded outcomes.
- [ ] 3. Admit ready tickets.
  - [ ] Build the proceedable set from local ticket state. Treat `ready: false`,
        `approval_required: true`, nonempty `blocked_by`, nonempty
        `claimed_by`, incomplete dependencies, `phase: complete`,
        `status: done`, parked next actions, external credential blockers, and
        non-computer-actionable blockers as hard exclusions.
  - [ ] Interpret `human_gate: none | [tag, "reason"]` as a final-action gate.
        Do not execute the tagged final action without Kenji, but do not block
        local prep, artifacts, research, proof, QA, packaging, or draft work
        merely because the final action is gated.
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
  - [ ] If no executable work exists and fresh Weekly/Daily strategy can be
        converted into safe tactical work, choose
        `plan_next_wave_when_empty`.
  - [ ] If no executable work exists because the queue is empty, vague, stale,
        blocked by product/goal judgment, unsafe, or undersupplied, choose
        `request_planning` and record the exact planning request for Daily or
        Weekly Interval.
  - [ ] Choose `no_op_blocked` only when execution, mechanical repair, and
        planning request are all blocked or unsafe.
- [ ] 5. Plan, spawn, or record.
  - [ ] For `plan_next_wave_when_empty`, read the latest Weekly strategy, Daily
        strategy, `farplane/goals.yaml`, `farplane/bindings.yaml`,
        `farplane/ops-memory.md` when present, `farplane/products.md` lane
        weights, open worker state, and board state.
  - [ ] Check the active focus, active projects, critical paths, next frontier,
        constraints, and parking lot before creating tickets. If ops memory is
        missing, stale, or contradicted by fresh interval strategy, record the
        gap or override in the Pulse report.
  - [ ] Name the current ops-memory belief, frontier, bottleneck, or reward
        signal being tested. Avoid creating a new idea ledger; the Pulse report
        and generated ticket `Reward` block are the evidence trail.
  - [ ] Create only small tactical tickets that ladder to a current focus, bet,
        active project, frontier step, lane, bottleneck, or reward signal.
        Generated tickets must be pure execution tickets: immediately
        actionable, scoped to a concrete output, and able to finish with an
        artifact, proof packet, local state change, QA result, draft, rendered
        asset, dataset, or review receipt that advances a named product, lane,
        product reward, or artifact workflow from `farplane/products.md`.
        Require the ticket summary, scope, or reward block to name that
        products.md contribution. Do not create tickets whose main deliverable
        is a plan, candidate ticket list, prioritization decision, strategy
        refresh, or recommendation for what Pulse should do next.
  - [ ] Do manager work in the parent beat. If the next useful move is
        ops-memory refresh, ticket closure reconciliation, frontier selection,
        or queue prioritization, apply the bounded writeback directly in the
        Pulse report/state/ops-memory when policy allows, or write a
        `request_planning` for Daily/Weekly when it needs product or goal
        judgment.
  - [ ] Prefer safe local work when Kenji is asleep/unavailable, review backlog
        is high, or worker threads are waiting on human feedback: local
        artifacts, research, experiment design/run, proof, QA, packaging, draft
        video/content, ranking packets, and decision packets.
  - [ ] Avoid blocky tickets that combine reversible preparation with final
        human-gated actions. Prefer `make/rank/prepare drafts` separately from
        `post/publish/spend/deploy/contact`.
  - [ ] Use product lane weights as selection bias when several equally safe
        slices are available; Daily strategy, blockers, freshness, and proof
        urgency may override the bias when the reason is recorded.
  - [ ] Every generated ticket must include parseable
        `Reward.kpi_rewards[]` plus `guard`.
  - [ ] Prefer this priority ladder:
        execute ready unblocked work; continue the active ops-memory frontier;
        continue the main daily focus; unblock the main daily focus; improve
        proof, review, or instrumentation for the focus; prepare downstream
        work for the weekly bet; support
        product/marketing only when it ladders to the weekly bet; improve the
        harness only when it improves future throughput or proof; no-op only
        when safe support work would be fake progress.
  - [ ] If maintenance is selected, name the active frontier it unblocks.
  - [ ] For each admitted ticket, create a named child-thread handoff with
        objective, context refs, local product skill ref when present, gates,
        expected outputs, reward horizon, and stop condition.
  - [ ] For managed waiting workers, leave the worker thread open and let that
        worker own follow-up when Kenji replies. Pulse may ask the worker thread
        to send a reminder or summarize state, but should not create a duplicate
        approval queue.
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
- `manage_worker_portfolio`: reconcile open workers, reward finished workers,
  leave human-review/final-action workers open, send or request bounded
  worker-context reminders when useful, and keep selecting safe local work
  rather than no-oping behind human review.
- `repair_ticket_admission_state`: perform only mechanical repair that can make
  an existing ticket executable, such as stale ready/approval/phase metadata or
  missing proof-state links. Do not make product or strategy decisions here.
- `plan_next_wave_when_empty`: when the board has no proceedable ticket and
  current strategy inputs are fresh, create a small wave of tactical tickets
  from ops-memory active frontier, Weekly/Daily strategy, product lane weights,
  open worker state, bindings, and board evidence. Treat this as a bounded test
  of Pulse's current operating belief, not as long-horizon strategy or a
  separate idea ledger. Planning and prioritization happen inside this parent
  beat; worker tickets created by this mode must be pure execution tickets with
  a concrete deliverable, stop condition, and explicit `farplane/products.md`
  contribution, not planning tickets, generic artifact tickets, or ticket
  generators. The mode must not change goals, KPIs, product
  boundaries, external systems, cadence, caps, spend, publishing, or customer
  contact. Generated tickets require parseable `Reward.kpi_rewards[]` plus
  `guard` and must pass normal admission gates before execution. If the frontier
  points at a gated final action, create or select a safe local prep/research/
  proof/draft/ranking ticket instead of the final action.
- `request_planning`: write a planning request for Daily or Weekly Interval
  when the board lacks executable work or needs product/goal judgment. Include
  queue evidence, idle reason, and suggested planning scope.
- `no_op_blocked`: stop only when execution, repair, and planning request are
  all blocked, unsafe, or would create noisy work.
