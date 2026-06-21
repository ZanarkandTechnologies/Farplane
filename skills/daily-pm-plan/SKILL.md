---
name: daily-pm-plan
description: "Turn weekly PM strategy, recent outcomes, tickets, and fresh signals into today's ranked operating plan for PM heartbeats."
tier: 3
group: harness
source: local
skill_template_version: "0.2.0"
eval: eval_task.json
allowed-tools: Read, Glob, Grep, Bash
---

# Daily PM Plan

## Context

Use this skill for daily planning. It translates weekly direction into today's
priority lanes, blockers, action constraints, and optional execution handoffs.
It should guide the shorter `pm-heartbeat` loop rather than execute broad work
itself.

`ticket-drainer` remains a separate skill. Daily planning may invoke or schedule
it when policy says ticket execution belongs at the daily cadence.

## Automation Presets

`daily-pm-plan.operating_plan @1d -> reports.daily_pm_plan`

The automation manifest supplies cadence, gates, reports, freshness, and local
overrides. This skill owns daily synthesis, ticket/blocked-work triage,
priority lane ranking, and the daily plan report.

## Skill Signature

```text
daily_pm_plan(project_root, weekly_plan, heartbeat_outcomes, tickets, policy)
  -> daily_plan
   + ranked_action_lanes
   + ticket_drainer_handoff?
   + blockers
   + ledger_delta

state:
  reads(.farplane/reports/weekly-pm/latest.md,
        .farplane/reports/pm-heartbeat/latest.md,
        .farplane/automation/action-outcomes.jsonl,
        .farplane/state/run-ledger.json,
        tickets/TASK-*/ticket.md,
        farplane/goals.md)
  writes(.farplane/reports/daily-pm-plan/latest.md,
         .farplane/reports/daily-pm-plan/runs/<timestamp>.md,
         .farplane/state/run-ledger.json,
         ticket deltas only when safe and explicit)

gates:
  weekly_plan_loaded_or_blocked; ticket_board_checked; outcomes_checked;
  daily_priorities_ranked; action_lanes_bounded; side_effect_gates_respected

routes:
  ticket-drainer | pm-heartbeat | feed-scout | update-memory |
  update-strategy | goal-advisor | review

fails:
  executing broad leaf work in the daily planner; ignoring weekly direction;
  producing a status digest without priorities; running full feed scout without
  freshness need; bypassing ticket gates
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Load the daily planning basis.
  - [ ] Read weekly PM report, current goals, ticket board, recent heartbeat
        decisions/outcomes, run ledger, and policy.
  - [ ] If weekly PM report is missing or stale, write a blocked daily report
        and request `weekly-pm-plan`.
- [ ] 2. Refresh only needed signals.
  - [ ] Reuse fresh external context when available.
  - [ ] Run or request lightweight feed scouting only when stale or required by
        today's planning decision.
- [ ] 3. Rank today's lanes.
  - [ ] Produce ranked action lanes for `pm-heartbeat`, including reason,
        expected outputs, constraints, and no-go zones.
  - [ ] Name blocked, unclear, human-gated, and stale tickets separately.
- [ ] 4. Decide ticket execution placement.
  - [ ] If policy says daily cadence owns ticket execution, invoke or hand off
        `ticket-drainer`.
  - [ ] If policy says the short heartbeat owns execution, write ticket
        execution as an allowed action lane instead.
- [ ] 5. Write the daily plan.
  - [ ] Write latest and timestamped daily plan reports.
  - [ ] Update ledger freshness and next expected heartbeat behavior.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

- daily priority lanes.
- blockers and stale context.
- ticket execution placement.
- allowed action constraints for `pm-heartbeat`.
- report and ledger paths.
