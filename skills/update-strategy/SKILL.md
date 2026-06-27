---
name: update-strategy
description: "Turn project goals, tickets, progress, and feedback into strategy deltas, system gaps, experiments, and ticket updates."
tier: 3
group: project-ops
source: local
template_uses:
  skill-template: "0.2.0"
allowed-tools: Read, Glob, Grep, Bash

---

# Update Strategy

## Context

Use this as the generic project strategy refresh primitive. It is the interface
that project PM heartbeats call before choosing next tickets or Goal Advisor
handoffs.

Project-specific automations can call this skill or `interval-update` extensions
with caller-supplied sources, taste, private context, report shape, and cadence.
Keep those source-specific extensions at the automation or project-doc layer,
not in the generic strategy skill.

## Automation Presets

`update-strategy.weekly_pm @7d -> reports.update_strategy`

Use when a weekly PM heartbeat needs to refresh project strategy after required
context reports are fresh. The automation manifest supplies dependencies,
freshness, reports, gates, and cadence. This skill owns goal/ticket/progress
evidence review, system-gap detection, ticket deltas, Goal Advisor handoffs,
and the operator report.

Eval surface: missing-feedback handling, evidence-tied strategy deltas,
metric-honesty checks, and "strategy does not execute leaf tickets" guardrails.

## Skill Signature

```text
update_strategy(project_harness?, project_goals?, tickets?, progress?, metrics_or_feedback?, constraints?)
  -> strategy_delta
   + system_gaps
   + experiments
   + ticket_deltas
   + project_goals_delta
   + operator_report
state: reads(project harness, project goals, tickets, progress, metrics, feedback, recent PM reports); writes(strategy artifact or ticket deltas only when an owning project path is explicit)
gates: goals_read; tickets_read; feedback_loop_status_named; metric_honesty_preserved; ticket_deltas_actionable; side_effect_gates_respected
routes: goal-advisor | interval-update | review | ticket/spec owner
fails: updates strategy without evidence; invents metrics; skips proceedable tickets; turns PM strategy into hidden execution
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the project state.
  - [ ] Resolve project root and read the project harness, project goals, and
    current tickets when present.
  - [ ] Read progress, PM reports, metrics, feedback, or label exports supplied
    by the caller.
  - [ ] Name missing sources rather than fabricating them.
- [ ] 2. Check the feedback loop before strategy claims.
  - [ ] State whether the project has a working feedback loop, proxy feedback,
    human review metric, or missing instrumentation.
  - [ ] If feedback is missing, produce a concrete feedback-skill or unblock
    ticket delta instead of optimizing from vibes.
- [ ] 3. Compare current strategy against evidence.
  - [ ] Identify goals that advanced, stalled, became stale, or need a new
    proof point.
  - [ ] Identify system gaps blocking reach, activation, retention, revenue,
    quality, efficiency, learning, or trust.
  - [ ] Keep claims tied to ticket/progress/metric evidence.
- [ ] 4. Produce the strategy delta.
  - [ ] Name bets to keep, change, pause, kill, or test.
  - [ ] Convert each actionable strategy change into a ticket delta,
    experiment, or Goal Advisor handoff.
  - [ ] Keep human approvals, spend, publishing, customer contact, account
    changes, and private data behind explicit gates.
- [ ] 5. Finish with an operator report.
  - [ ] Include what changed, why, next tickets, blocked systems, missing
    feedback, and the next PM heartbeat or Goal Advisor route.
  - [ ] Use [review](../review/SKILL.md) when the strategy update is material,
    external-facing, or likely to create expensive work.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

```text
Strategy Update
- project:
- evidence window:
- feedback loop status:
- kept bets:
- changed bets:
- paused/killed bets:
- system gaps:
- experiments:
- ticket deltas:
- project goals delta:
- side-effect gates:
- next route:
```

## Gotchas

- Do not treat strategy as a status digest; it must change, preserve, or kill
  bets based on evidence.
- Do not invent KPIs or market feedback. Missing metrics become feedback-skill
  or instrumentation tickets.
- Do not let strategy updates bypass the ticket board; concrete work should
  become ticket deltas or Goal Advisor handoffs.
- Do not use caller-specific Notion, life, CRM, or private-tool assumptions
  unless the caller supplied those inputs.

## Reference Map

- [../goal-advisor/SKILL.md](../goal-advisor/SKILL.md) - compile selected
  strategy deltas into native Goal, heartbeat, rollout, feedback, or direct
  routes.
- [../review/SKILL.md](../review/SKILL.md) - use for material readiness or
  evidence-quality judgment.
- [../../docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md](../../docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md)
  - shared project harness and PM heartbeat vocabulary.

## Output

- `strategy_delta`
- `system_gaps`
- `experiments`
- `ticket_deltas`
- `project_goals_delta`
- `operator_report`
