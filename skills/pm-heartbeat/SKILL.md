---
name: pm-heartbeat
description: "Compatibility alias for pulse-update: turn the fast pulse lane into one bounded action decision and ledger update."
tier: 3
group: harness
source: local
template_uses:
  skill-template: "0.2.0"
  skill-eval-task: "0.1.0"
eval: eval_task.json
allowed-tools: Read, Glob, Grep, Bash

---

# PM Heartbeat

## Context

Compatibility alias: new automation contracts should call
[pulse-update](../pulse-update/SKILL.md). Keep this package so existing
automation prompts, evals, and report paths that still name `pm-heartbeat` do
not break during the migration.

Use this skill for the short-cadence PM idle loop. It does not own horizon
strategy or rhythm planning. It consumes those higher-level reports, reconciles
recent child-thread outcomes, chooses one bounded action, and records the
decision.

This skill should be easy to pilot by changing cadence and policy, without
rewriting the action logic. Frequency controls when the loop wakes; policy
controls what it may do.

## Automation Presets

`pm-heartbeat.bandit @30m -> reports.pm_heartbeat`

Canonical lane preset: `pulse-update.bandit @30m -> reports.pulse`.

The automation manifest supplies cadence, enabled flag, action authority,
allowed arms, child-thread budget, gates, reports, and project overrides. This
skill owns reward reconciliation, forced action checks, bandit scoring, child
handoff shape, and decision/outcome ledger writes.

## Skill Signature

```text
pm_heartbeat(project_root, policy, daily_plan, weekly_plan, bandit_state)
  -> reward_update
   + selected_action
   + child_thread_handoff?
   + decision_row
   + ledger_delta

state:
  reads(.farplane/reports/daily-pm-plan/latest.md,
        .farplane/reports/weekly-pm/latest.md,
        .farplane/automation/heartbeat-policy.json,
        .farplane/automation/action-arms.json,
        .farplane/automation/bandit-state.json,
        .farplane/automation/spawned-threads.jsonl,
        .farplane/automation/action-outcomes.jsonl)
  writes(.farplane/reports/pm-heartbeat/latest.md,
         .farplane/automation/decisions.jsonl,
         .farplane/automation/spawned-threads.jsonl,
         .farplane/automation/rewards.jsonl,
         .farplane/automation/reflections/latest.md)

gates:
  daily_plan_loaded_or_blocked; rewards_reconciled; forced_actions_checked;
  one_action_selected; child_budget_respected; side_effect_gates_respected;
  decision_recorded

routes:
  ticket-drainer | goal-advisor | feed-scout | skill-maintenance |
  eval | qa | review | daily-pm-plan | weekly-pm-plan

fails:
  rediscovering weekly strategy every beat; spawning multiple child threads
  without policy; executing broad work in the parent heartbeat; treating
  frequency as authority; skipping reward/outcome writeback
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind policy and context.
  - [ ] Read heartbeat policy, action arms, daily plan, weekly plan, bandit
        state, spawned thread rows, and recent outcomes.
  - [ ] If daily plan is missing or stale, write a blocked heartbeat report
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

- selected action and decision mode.
- reward update summary.
- child thread id or no-child maintenance result.
- expected outputs and reward horizon.
- report and state paths.
