---
kind: interval-report
ref: reports/interval/<interval_id>/<timestamp>
project: <project>
automation_id: <automation_id>
interval_id: <interval_id>
report_workflows: <enabled workflow list>
status: draft
created_at: <timestamp>
review_window: <start>..<end>
planning_window: <start>..<end>
context_bundle: <path>
ui_summary: "<one concise report-card summary under 100 words>"
---

# Interval Update Report

## Summary

- `decision:`
- `why_now:`
- `accepted_tradeoff:`

## Evidence Reviewed

| Source | Status | Key signal | Evidence |
| --- | --- | --- | --- |

## Drift Check

- `drift_against:` parent plan, original goals, mission, current milestone
- `verdict:` aligned | drifting | blocked | source_gap
- `evidence:`
- `correction:`

## KPI / Feedback Status

| Axis / KPI / feedback surface | State | Trend | Confidence | Gap |
| --- | --- | --- | --- | --- |

Daily metric readings: `.farplane/metrics/daily/YYYY-MM-DD.json`.
Project/UI projection: `.farplane/project/ui/latest.json`.

## Report Workflows

Run only workflows enabled by the automation config. For disabled workflows,
write `not_configured`; for source-dependent workflows with no source, write
`not_applicable` plus the source gap.

| Workflow | Verdict | Evidence | Next planning implication |
| --- | --- | --- | --- |
| Plan progress |  |  |  |
| Codex attention drift |  |  |  |
| Ticket / board drift |  |  |  |
| Relationship / feedback obligations |  |  |  |
| Opportunity signals |  |  |  |
| Goal drift |  |  |  |
| Metric snapshot |  |  |  |
| Compounding leverage review |  |  |  |
| Tracked feature review |  |  |  |
| Priority planning |  |  |  |

## Reward Closure

Use this section when prior interval reports selected leverage bets or reward
signals. Close the loop before selecting new bets or writing the next-window
plan.

| Previous bet | Expected reward | Observed result | Evidence | Decision |
| --- | --- | --- | --- | --- |

Decisions: `accept`, `continue`, `kill`, `resize`, `source_gap`.

## Budget / Runway Review

Use this section to decide whether active projects deserve another planning
window. Start rough: cite ticket `Reward` blocks, metric snapshots, reports,
source gaps, and visible operator feedback before adding cost accounting.

| Active project | Contribution mode | Spend / attention used | Expected reward | Observed evidence | Decision | Next constraint |
| --- | --- | --- | --- | --- | --- | --- |

Decisions: `continue`, `narrow`, `pause`, `instrument`, `stop`,
`escalate_to_revenue`.

Rules:

- `Reward.kpi_rewards[]` plus `Reward.guard` are the ticket-level budget
  justification and KPI attribution shape. Do not invent a second ticket budget
  field.
- Missing exact spend is not a blocker for the first review; record rough
  attention used and add an instrumentation gap only if the decision needs
  precision.
- Work with no weekly evidence should be paused, narrowed, or converted into an
  instrumentation ticket.

## Self-Update / Leverage Review

Use this section only when `compounding_leverage_review` is enabled. It is the
state store for leverage decisions; do not create a separate leverage backlog
unless a ticketed migration proves one is needed.

### Self-Evolution Signals

Summarize signals as evidence, not as a blind aggregate score. If a signal is
not measured yet, write `source_gap` and route the missing proof surface.

| Signal | Direction | Evidence | Confidence | Planning implication |
| --- | --- | --- | --- | --- |
| Accepted output / autonomous worker elapsed minutes |  |  |  |  |
| Human attention minutes / auto-time ratio |  |  |  |  |
| Ticket intervention turns / auto-completion rate |  |  |  |  |
| Proof closure rate |  |  |  |  |
| False completion / self-approval incidents |  |  |  |  |
| Context isolation failures |  |  |  |  |
| Source gaps |  |  |  |  |
| Skill backpropagation events |  |  |  |  |

| Lever | Surface | Loss term | Evidence | Score | Bet | Reward signal | Route |
| --- | --- | --- | --- | --- | --- | --- | --- |

Score format:
`compound=<1-5>; proof_speed=<1-5>; reuse=<1-5>; operator_effort=<1-5>; friction=<1-5>; risk=<1-5>`.

Decision states:

- `selected`: one of the 1-3 bets for the next planning window.
- `rejected`: evidence says the lever should not be pursued now.
- `deferred`: plausible but not worth displacing the selected bets.
- `expired`: old candidate with no fresh evidence.
- `escalated`: high-confidence urgent signal routed before the next interval.

## Strategy Decisions

| Decision | Kind | Evidence | Consequence | Owner / next surface |
| --- | --- | --- | --- | --- |

Kinds: `keep`, `change`, `pause`, `kill`, `test`.

## Ops Memory Challenge

Use this section to challenge the current Pulse operating belief in
`farplane/ops-memory.md`. Do not create a separate idea ledger; summarize what
the last window proved, disproved, or left unmeasured, then route a compact
ops-memory delta or Pulse constraint.

```text
pulse_belief_reviewed:
what_worked:
what_failed:
belief_to_keep:
belief_to_revise:
belief_to_drop:
double_down_guard:
source_gap:
```

## Strategy Input For Pulse

Use this compact block as the strategy input consumed by Pulse. Weekly reports
usually set the broader bets; Daily reports usually recalibrate focus,
blockers, prefer/avoid rules, and temporary lane-weight overrides. Pulse may
slice tactical tickets from this block plus `farplane/ops-memory.md` only when
the board has no safe proceedable work.

```text
focus:
bets:
prefer:
avoid:
blocked:
reward:
lane_weight_overrides:
```

## Ops Memory Delta

Use this block when the interval should refresh `farplane/ops-memory.md`.
Ops memory is active working context, not a replacement for `goals.yaml`,
`products.md`, tickets, or dated interval reports. Keep the delta compact and
edit existing sections rather than appending a second roadmap.

```text
current_focus:
active_projects:
budget_runway:
next_frontier:
constraints:
parking_lot:
recent_decisions:
```

## Next Window Plan

## Lane Distribution

| Lane | Planned weight | Ticket budget | Why now | Expected reward | Guardrail check |
| --- | ---: | ---: | --- | --- | --- |

Use `farplane/products.md` for plannable lanes and `farplane/harness.md`
allocation guardrails for static safety rails. Planned weights are next-window
decisions, not permanent product strategy. Each selected lane must name the
goal, bottleneck, or reward signal it is expected to move. Product lane weights
are allocation priors, not hard quotas; record the evidence for any temporary
override.

| Priority | Why now | Expected output | Proof or reward signal | Owner / next surface |
| --- | --- | --- | --- | --- |

## Goals Delta

Use this block as the only bridge from interval evidence into `farplane/goals.yaml`.
Do not edit the goals portfolio before this block exists.

| Delta | Target | Decision | Evidence | Risk | Next action |
| --- | --- | --- | --- | --- | --- |

Decisions:

- `auto_apply`: source refs, current-signal notes, stale labels, or minor
  milestone wording backed by clear evidence.
- `approval_required`: north star, KPI, strategy axis, project priority, hold,
  stop condition, quarterly goal, yearly goal, or durable milestone changes.
- `rejected_source_gap`: insufficient evidence; create an instrumentation,
  access, feedback, or research ticket instead.

## Ticket Delta

| Ticket / candidate | Delta | Reason | Evidence |
| --- | --- | --- | --- |

## Downstream Guidance

- `top_lanes:`
- `strategy_input_for_pulse:`
- `ops_memory_delta:`
- `constraints:`
- `blocked_or_human_gated:`
- `allowed_pulse_actions:`
- `do_not_do:`

## Scheduled Actions

| Action | Due? | Result | Evidence | Next due |
| --- | --- | --- | --- | --- |
| quarterly_plan |  |  |  |  |
| annual_review |  |  |  |  |

Default: keep quarterly/yearly and other intervals greater than one week as
scheduled actions inside the weekly interval until repeated evidence shows a
separate persistent lane adds value.

## Source Gaps And Blockers

-

## Outputs

- `context_bundle:`
- `interval_report:`
- `goals_delta_applied:`
- `goals_delta_requires_approval:`
- `ticket_deltas:`
- `ops_memory_delta:`
- `ledger_update:`
