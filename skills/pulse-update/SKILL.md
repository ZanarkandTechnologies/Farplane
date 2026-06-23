---
name: pulse-update
description: "Run the Farplane fast idle loop: reconcile outcomes, use reasoning plus bandit state to select one action, spawn a worker when useful, and update decision ledgers."
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
reconciliation, reasoning plus bandit-based action selection, and one bounded
action. It does not own drift review, scrum reflection, strategy, or scheduled
planning. It may read Steer guidance as constraints, but its job is to choose
the next board/action-tree move and spawn or record the worker handoff.

This skill should be easy to pilot by changing cadence and policy, without
rewriting the action logic. Interval controls when Pulse wakes; policy controls
what it may do.

## Automation Presets

`pulse-update.bandit @30m -> reports.pulse`

The live Codex automation supplies cadence and prompt context. Project policy
may supply action arms, child-thread budget, gates, and local overrides. Pulse
owns reward reconciliation, forced action checks, bandit scoring, action-tree
selection, child handoff shape, and decision/outcome ledger writes. If no
proceedable ticket exists, Pulse chooses one narrow refill or maintenance arm;
`consult goal-advisor` is an arm, not the default.

## Skill Signature

```text
pulse_update(project_root, pulse_policy, board_state, action_tree, reward_state)
  -> reward_update
   + selected_action
   + child_thread_handoff?
   + decision_row
   + ledger_delta

state:
  reads(farplane/goals.md?,
        .farplane/reports/steer/**?,
        .farplane/automation/heartbeat-policy.json,
        .farplane/automation/action-arms.json,
        .farplane/automation/bandit-state.json,
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
  board_loaded; rewards_reconciled;
  forced_actions_checked; one_action_selected; child_budget_respected;
  side_effect_gates_respected; decision_recorded;
  pm_thread_grouping_updated_when_persistent

routes:
  goal-advisor | impl-plan | feed-scout | skill-maintenance |
  eval | qa | review | steer-update

fails:
  performing drift review or weekly scrum planning; rediscovering strategy
  every beat; spawning multiple child threads without policy; executing broad
  work in the parent heartbeat; treating goal-advisor as the default empty-board
  fallback; treating interval as authority; skipping reward/outcome writeback
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind policy and context.
  - [ ] Read Pulse policy, action tree/action arms, local ticket board, latest Steer
        guidance when present, bandit state, spawned thread rows, and recent
        outcomes.
  - [ ] Treat Steer guidance as constraints only; do not perform drift review
        or weekly scrum planning inside Pulse.
- [ ] 2. Reconcile previous outcomes.
  - [ ] Inspect prior spawned thread rows and expected outputs.
  - [ ] Apply immediate rewards for completed, partial, blocked, noisy, or
        missing-output child work.
  - [ ] Avoid double-counting already rewarded outcomes.
- [ ] 3. Check forced actions.
  - [ ] Prefer `reward_update`, `metric_snapshot`, or `steer_request` when
        policy thresholds require maintenance.
  - [ ] Otherwise score allowed action arms with the configured deterministic
        bandit policy.
- [ ] 4. Select one bounded action.
  - [ ] Record mode as `forced`, `explore`, or `exploit`.
  - [ ] Respect `maxChildThreadsPerBeat`, open child-thread limits, gates, and
        action authority.
  - [ ] When selecting ticket work, choose one proceedable ticket from local
        ticket state, prefer ready/unblocked work, and route substantial coding
        execution through `goal-advisor` when the ticket needs a Goal-backed
        worker program.
  - [ ] If no proceedable ticket exists, choose one narrow refill or
        maintenance arm from the action tree instead of inventing strategy in
        the Pulse context.
  - [ ] Treat `consult goal-advisor` as one action-tree arm only when the empty
        board is caused by unclear goals, an unclear milestone, or missing
        executable Goal Packets.
- [ ] 5. Spawn or record.
  - [ ] If the action needs a child, create a named child-thread handoff with
        objective, context refs, gates, expected outputs, reward horizon, and
        stop condition.
  - [ ] If the child is a persistent PM-owned worker chat that should appear
        under the project employee in the UI, append its thread ID to
        `farplane/pm.json` `threads.chats`.
  - [ ] If no child is needed, write the maintenance result directly.
- [ ] 6. Write decision state.
  - [ ] Append decision, spawned-thread, reward, and report rows.
  - [ ] Write a date-stamped Pulse report and keep newest-report pointers in
        state when needed.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

- selected action and decision mode.
- reward update summary.
- child thread id or no-child maintenance result.
- expected outputs and reward horizon.
- report and state paths.

## Default Action Arms

- `pick_ready_ticket`: choose one ready, unblocked ticket and spawn a bounded
  PM-owned worker when useful.
- `split_oversized_ticket`: turn one blocked or too-large ticket into a smaller
  executable ticket handoff.
- `clarify_blocker`: ask for or record the smallest blocker clarification.
- `create_prep_ticket`: add one small setup, research, QA, or cleanup ticket
  that unlocks obvious work.
- `run_qa_or_eval`: collect proof for a ticket or workflow whose next reward
  depends on evidence.
- `refresh_ticket_metadata`: repair stale ready/approval/phase metadata so the
  board becomes selectable again.
- `consult_goal_advisor`: ask for Goal Advisor help only when goals or the next
  milestone are too unclear to create executable work.
- `no_op_unsafe`: stop when all available actions violate gates, require human
  approval, or would create noisy work.
