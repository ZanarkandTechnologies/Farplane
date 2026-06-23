---
name: pulse-update
description: "Turn the fast pulse lane into drift reconciliation, one bounded action decision, child-thread handoff, and outcome ledger updates."
tier: 3
group: harness
source: local
skill_template_version: "0.2.0"
eval: eval_task.json
allowed-tools: Read, Glob, Grep, Bash
---

# Pulse Update

## Context

Use this skill for the fast pulse lane: immediate attention, triage, reward
reconciliation, and one bounded action. It does not own horizon strategy or
rhythm planning. It consumes those higher-level reports, checks for drift
against the active task and rhythm plan, chooses one bounded action, and records
the decision.

This skill should be easy to pilot by changing cadence and policy, without
rewriting the action logic. Interval controls when the lane wakes; policy
controls what it may do. `pm-heartbeat` is the legacy compatibility alias.

## Automation Presets

`pulse-update.bandit @30m -> reports.pulse`

The automation manifest supplies lane interval, enabled flag, action authority,
allowed arms, child-thread budget, gates, reports, and project overrides. This
skill owns reward reconciliation, forced action checks, bandit scoring, child
handoff shape, and decision/outcome ledger writes.

## Skill Signature

```text
pulse_update(project_root, lane_policy, rhythm_plan, horizon_plan, action_state)
  -> drift_check
   + reward_update
   + selected_action
   + child_thread_handoff?
   + decision_row
   + ledger_delta

state:
  reads(.farplane/reports/rhythm/latest.md,
        .farplane/reports/horizon/latest.md,
        .farplane/automation/heartbeat-policy.json,
        .farplane/automation/action-arms.json,
        .farplane/automation/bandit-state.json,
        .farplane/automation/spawned-threads.jsonl,
        .farplane/automation/action-outcomes.jsonl)
  writes(.farplane/reports/pulse/latest.md,
         .farplane/automation/decisions.jsonl,
         .farplane/automation/spawned-threads.jsonl,
         .farplane/automation/rewards.jsonl,
         .farplane/automation/reflections/latest.md)

gates:
  rhythm_plan_loaded_or_blocked; horizon_plan_loaded_or_blocked;
  drift_against_active_task_checked; rewards_reconciled;
  forced_actions_checked; one_action_selected; child_budget_respected;
  side_effect_gates_respected; decision_recorded

routes:
  ticket-drainer | goal-advisor | feed-scout | skill-maintenance |
  eval | qa | review | rhythm-update | horizon-update

fails:
  rediscovering horizon strategy every beat; spawning multiple child threads
  without policy; executing broad work in the parent heartbeat; treating
  interval as authority; skipping drift or reward/outcome writeback
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind policy and context.
  - [ ] Read lane policy, action arms, rhythm plan, horizon plan, bandit
        state, spawned thread rows, and recent outcomes.
  - [ ] If rhythm plan is missing or stale, write a blocked pulse report
        instead of inventing strategy.
- [ ] 2. Reconcile previous outcomes.
  - [ ] Inspect prior spawned thread rows and expected outputs.
  - [ ] Apply immediate rewards for completed, partial, blocked, noisy, or
        missing-output child work.
  - [ ] Avoid double-counting already rewarded outcomes.
- [ ] 3. Check forced actions.
  - [ ] Prefer `reward_update`, `metric_snapshot`, or `weekly_reflection` when
        policy thresholds require maintenance.
  - [ ] Otherwise score allowed action arms with the configured deterministic
        bandit policy.
- [ ] 4. Select one bounded action.
  - [ ] Record mode as `forced`, `explore`, or `exploit`.
  - [ ] Respect `maxChildThreadsPerBeat`, open child-thread limits, gates, and
        action authority.
- [ ] 5. Spawn or record.
  - [ ] If the action needs a child, create a named child-thread handoff with
        objective, context refs, gates, expected outputs, reward horizon, and
        stop condition.
  - [ ] If no child is needed, write the maintenance result directly.
- [ ] 6. Write decision state.
  - [ ] Append decision, spawned-thread, reward, and report rows.
  - [ ] Update reflection only from observed outcomes and current plan context.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

- drift check, selected action, and decision mode.
- reward update summary.
- child thread id or no-child maintenance result.
- expected outputs and reward horizon.
- report and state paths.
