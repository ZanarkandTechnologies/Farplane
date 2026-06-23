---
name: rhythm-update
description: "Turn horizon strategy, recent pulse outcomes, tickets, and fresh signals into a day-scale ranked operating plan."
tier: 3
group: harness
source: local
template_uses:
  skill-template: "0.2.0"
  skill-eval-task: "0.1.0"
eval: eval_task.json
allowed-tools: Read, Glob, Grep, Bash

---

# Rhythm Update

## Context

Use this skill for the rhythm lane: day-scale planning, priority lanes,
blockers, action constraints, and optional execution handoffs. It translates
horizon direction into the next few days of operating rhythm. It should guide
the faster `pulse-update` loop rather than execute broad work
itself.

`ticket-drainer` remains a separate skill. Rhythm planning may invoke or
schedule it when policy says ticket execution belongs at the rhythm lane.
`daily-pm-plan` is the legacy compatibility alias.

## Automation Presets

`rhythm-update.operating_plan @1d -> reports.rhythm`

The automation manifest supplies lane interval, gates, reports, freshness, and
local overrides. This skill owns rhythm synthesis, ticket/blocked-work triage,
priority lane ranking, and the rhythm report.

## Skill Signature

```text
rhythm_update(project_root, lane_policy, horizon_plan, recent_pulse_reports, tickets, ledger)
  -> drift_check
   + day_range_plan
   + ranked_action_lanes
   + ticket_drainer_handoff?
   + blockers
   + ledger_delta

state:
  reads(.farplane/reports/horizon/latest.md,
        .farplane/reports/pulse/latest.md,
        .farplane/automation/action-outcomes.jsonl,
        .farplane/state/run-ledger.json,
        tickets/TASK-*/ticket.md,
        farplane/goals.md)
  writes(.farplane/reports/rhythm/latest.md,
         .farplane/reports/rhythm/runs/<timestamp>.md,
         .farplane/state/run-ledger.json,
         ticket deltas only when safe and explicit)

gates:
  horizon_plan_loaded_or_blocked; drift_against_horizon_checked;
  ticket_board_checked; pulse_outcomes_checked; rhythm_priorities_ranked;
  action_lanes_bounded; side_effect_gates_respected

routes:
  ticket-drainer | pulse-update | feed-scout | update-memory |
  update-strategy | goal-advisor | review

fails:
  executing broad leaf work in the rhythm planner; ignoring horizon direction;
  producing a status digest without priorities; running full feed scout without
  freshness need; bypassing ticket gates
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Load the rhythm planning basis.
  - [ ] Read horizon report, current goals, ticket board, recent pulse
        decisions/outcomes, run ledger, and policy.
  - [ ] If horizon report is missing or stale, write a blocked rhythm report
        and request `horizon-update`.
- [ ] 2. Refresh only needed signals.
  - [ ] Reuse fresh external context when available.
  - [ ] Run or request lightweight feed scouting only when stale or required by
        today's planning decision.
- [ ] 3. Rank the next day-range lanes.
  - [ ] Produce ranked action lanes for `pulse-update`, including reason,
        expected outputs, constraints, and no-go zones.
  - [ ] Name blocked, unclear, human-gated, and stale tickets separately.
- [ ] 4. Decide ticket execution placement.
  - [ ] If policy says daily cadence owns ticket execution, invoke or hand off
        `ticket-drainer`.
  - [ ] If policy says the short heartbeat owns execution, write ticket
        execution as an allowed action lane instead.
- [ ] 5. Write the rhythm plan.
  - [ ] Write latest and timestamped rhythm reports.
  - [ ] Update ledger freshness and next expected pulse behavior.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

- drift check and day-range priority lanes.
- blockers and stale context.
- ticket execution placement.
- allowed action constraints for `pulse-update`.
- report and ledger paths.
