---
kind: project-goals-example
title: AGI Toy Shop Project Goals
owner: horizon-advisor
status: draft
created_at: 2026-06-12
updated_at: 2026-06-23
---

# AGI Toy Shop Goals

This is an example `farplane/goals.yaml` planning view for one large project. It
is meant to be readable by a human, editable by an agent, and syncable to Notion
as a view. The repo file remains the source of truth.

## North Star

Build AGI Toy Shop into a profitable autonomous toy storefront whose offer,
content, funnel, product catalog, support, and agent skills improve from
evidence.

## Goal Writing Standard

Each goal should define an outcome, metric, timeframe, scope, and proof surface.

```text
good_goal(intent, horizon, evidence_state)
  -> outcome + metric + timeframe + constraints + proof_surface
```

## Goal Rule

Only expand the first evidence-producing branch deeply. Future branches stay as
trajectory placeholders until the current timeframe review produces evidence.

```text
farplane/goals.yaml = long-range map
ticket.md = current task contract
program.md = loop config
progress.md = observed turn log
child tickets = execution units
Notion = synced visual view
```

## Goal Map

```text
AGI Toy Shop/
├── 5Y Build a compounding autonomous toy store/
│   ├── metric: profitable repeatable revenue engine + durable capabilities
│   ├── Y1 Launch first profitable revenue engine/
│   │   ├── metric: first repeatable offer/funnel/content loop
│   │   ├── Q1 Prove offer, funnel, content, and tracking/
│   │   │   ├── metric: review + artifact + first feedback/market baseline
│   │   │   ├── M1 Create first evidence loop/
│   │   │   │   ├── type: project
│   │   │   │   ├── W1 Launch first offer test and baseline tracking/  <-- expanded
│   │   │   │   │   ├── type: project_slice
│   │   │   │   │   ├── TASK-0001 Define first toy offer/
│   │   │   │   │   │   ├── trigger: native_goal
│   │   │   │   │   │   ├── metric: review + artifact
│   │   │   │   │   │   └── state: planned
```

## Current Milestone

Y1 > Q1 > M1 > W1: launch the first offer test and tracking baseline.

## Goal Advisor Handoff

```text
goal_advisor(
  files=[farplane/goals.yaml, tickets/TASK-0001/ticket.md, tickets/TASK-0001/program.md, tickets/TASK-0001/progress.md],
  task="compile TASK-0001 into a native Goal prompt",
  metric_provider=review,
  trigger=active_goal
)
```

