---
title: Goal Advisor Algebra
owner: goal-advisor
status: active
created_at: 2026-06-13
---

# Goal Algebra

Load this reference when several workflow skills are invoked together or when
retired execution-surface migration detail matters.

The job of `goal-advisor` is to choose the Goal Packet architecture and compile
the operator's intent into one native Goal contract, not to run each named skill
as a separate top-level workflow.

```text
GoalPacket := Files + Task + Program + Progress + Prompt + Drift

Task :=
  desired_end_state
+ boundaries
+ constraints
+ non_goals

Program :=
  metric_provider
+ budget_policy
+ after_each_turn
+ drift_policy
+ heartbeat_policy
+ stop_conditions

MetricProvider :=
  mechanical_evidence
| human_feedback
| review_verdict
| agent_qa
| market_signal
| hybrid_metric

Progress :=
  turn_log
+ evidence
+ metric_samples
+ drift_verdicts
+ next_action

GoalPortfolio :=
  north_star
+ portfolio_map
+ current_frontier
+ metric_discovery
+ child_goal_packets
+ parent_heartbeat_policy
+ sync_targets
```

## Composition Rules

- `agent-qa-test` fills the `agent_qa` metric provider and the fix-or-rerun
  policy.
- `optimize-with-human` fills `MetricProvider.human_feedback` through
  `feedback-request.md`, `feedback.json`, and `human_score` or `accepted`.
- `review` fills the `review_verdict` provider for serious completion,
  skill-contract, or proof-bundle judgments.
- `$impl` fills coding-ticket execution only after this skill has compiled the
  Goal files, mode, budget, metric, and stop policy.
- Retired public surfaces map into Goal standards:
  - `$work` -> admission/profile fields in `program.md`
  - `$ralph` -> heartbeat board-drain pattern
  - `batch-work` -> batch Goal file list plus per-ticket proof ledger

## Skill Improvement Composition

For skill-improvement work, native Goal mode is the durable loop runner. Draft
the Goal so it reads the target skill package plus any `self-improve/` context,
optimizes toward `program.md`, uses `self-improve` only for eval, memory, or
prompt scaffolding, and uses `skill-maintenance` for accepted writeback into
`SKILL.md`, references, or plugin/source copies.

## Question Policy

- Ask when the answer changes safety, scope, verification, spend, destructive
  boundaries, or irreversible external side effects.
- Do not ask for fields already present in the ticket body, `Done / Proof`,
  linked plan, or operator message.
- Do not ask broad interview questions just because the Goal could be richer.
- If more than 3 fields are missing, ask the 3 that affect execution safety
  most and mark the rest as assumptions.
