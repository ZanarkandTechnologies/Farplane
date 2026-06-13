---
kind: goal-portfolio-example
title: AGI Toy Shop Goal Portfolio
owner: goal-advisor
status: draft
created_at: 2026-06-12
---

# AGI Toy Shop Goal Portfolio

This is an example Markdown planning view for one large project. It is meant to
be readable by a human, editable by an agent, and syncable to Notion as a view.
The repo file remains the source of truth.

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

Bad goal:

```text
Improve content.
```

Better goal:

```text
Produce 10 short-form hooks for the first AGI Toy Shop offer by W1, collect
Kenji's keep/reject labels, and extract at least 3 reusable content patterns
before updating the content skill.
```

## Portfolio Rule

Only expand the first evidence-producing branch deeply. Future branches stay as
trajectory placeholders until the current timeframe review produces evidence.

```text
portfolio.md = long-range map
ticket.md = current task contract
program.md = loop config
progress.md = observed turn log
child tickets = execution units
Notion = synced visual view
```

## Portfolio Map

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
│   │   │   │   │   │   ├── parallel: TASK-0003, TASK-0004
│   │   │   │   │   │   ├── amplifies: TASK-0002, TASK-0004, TASK-0005
│   │   │   │   │   │   └── state: planned
│   │   │   │   │   ├── TASK-0002 Publish first landing page draft/
│   │   │   │   │   │   ├── trigger: native_goal
│   │   │   │   │   │   ├── metric: review + artifact_presence
│   │   │   │   │   │   ├── depends_on: TASK-0001
│   │   │   │   │   │   └── state: planned
│   │   │   │   │   ├── TASK-0003 Install funnel tracking baseline/
│   │   │   │   │   │   ├── trigger: native_goal
│   │   │   │   │   │   ├── metric: mechanical
│   │   │   │   │   │   ├── parallel: TASK-0001, TASK-0004
│   │   │   │   │   │   └── state: planned
│   │   │   │   │   ├── TASK-0004 Generate 10 short-form content hooks/
│   │   │   │   │   │   ├── trigger: native_goal
│   │   │   │   │   │   ├── metric: human_feedback
│   │   │   │   │   │   ├── depends_on: TASK-0001 partial
│   │   │   │   │   │   ├── parallel: TASK-0002, TASK-0003
│   │   │   │   │   │   ├── amplifies: TASK-0005
│   │   │   │   │   │   └── state: planned
│   │   │   │   │   └── TASK-0005 Ask Kenji for content feedback/
│   │   │   │   │       ├── trigger: feedback_loop
│   │   │   │   │       ├── metric: human_feedback
│   │   │   │   │       ├── depends_on: TASK-0004
│   │   │   │   │       ├── amplifies: TASK-0004, W2
│   │   │   │   │       └── state: planned
│   │   │   │   └── W2 Iterate offer from W1 evidence/  <-- hold
│   │   │   │       └── hold: until W1 review
│   │   │   ├── M2 Improve content and conversion loop/  <-- hold
│   │   │   │   └── hold: until M1 review
│   │   │   └── M3 Add support and fulfillment reliability/  <-- hold
│   │   │       └── hold: until M1 review
│   │   ├── Q2 Scale winning channel/  <-- hold
│   │   │   └── hold: until Q1 review
│   │   ├── Q3 Add second product line/  <-- hold
│   │   └── Q4 Systematize operations/  <-- hold
│   ├── Y2 Expand product portfolio/  <-- hold
│   ├── Y3 Build durable brand and retention/  <-- hold
│   ├── Y4 Compound automation and partnerships/  <-- hold
│   └── Y5 Durable autonomous business/  <-- hold
```

## Metric Discovery

| Goal | Horizon | Metric Provider | Signal | Direction | Collection Plan |
| --- | --- | --- | --- | --- | --- |
| Define first toy offer | W1 | review | offer doc passes clarity and usefulness review | pass-fail | reviewer checks offer artifact |
| Landing page draft | W1 | review + artifact_presence | page draft exists and matches offer | pass-fail | inspect page artifact |
| Tracking baseline | W1 | mechanical | local event fires or tracking plan exists | pass-fail | run smoke or review tracking doc |
| Content hooks | W1 | human_feedback | Kenji labels 10 hooks keep/reject | learn | request Telegram feedback |
| First offer review | W1 end | hybrid | review verdict + collected evidence | accept-revise | CEO heartbeat summarizes W1 |

## Current Frontier

Expand only:

- `5Y > Y1 > Q1 > M1 > W1`

Hold:

- `W2+` until W1 has evidence
- `M2+` until M1 review
- `Q2+` until Q1 review
- `Y2+` until Y1 review

## Overflow Edges

Use this only when the map gets too dense. The AGI Toy Shop W1 slice is small
enough to keep edges inline in the Portfolio Map.

| Source | Edge | Target | Reason |
| --- | --- | --- | --- |
| W1 | hold | W2 | W2 should be planned only after W1 review |

## Replan Cadence

- Daily: update child-ticket progress and blockers.
- Weekly: run CEO heartbeat, close W1, expand W2.
- Monthly: review M1 evidence and decide M2.
- Quarterly: review Q1 and expand Q2.
- Yearly: revise Y2 from actual revenue, customer, and capability evidence.

## Continuation Policy

- `child_goal_complete:` update the task node in this map, append child
  completion progress, run review/proof, then start the next eligible W1 task
- `frontier_complete:` run the weekly CEO heartbeat before expanding W2
- `manual_replan:` allowed
- `heartbeat_replan:` weekly CEO heartbeat
- `no_op_policy:` append a heartbeat no-op when feedback or market evidence has
  not arrived yet

## Parent Heartbeat Prompt

```text
Inspect the AGI Toy Shop portfolio as a parent heartbeat.

Task: Read this portfolio, the parent program.md, and parent progress.md. Choose
exactly one next action: start_child_goal, resume_child_goal, request_feedback,
replan, or no_op. The current frontier is 5Y > Y1 > Q1 > M1 > W1.

Logging: Before ending, append a heartbeat entry to parent progress.md with the
chosen action, reason, evidence checked, and next child Goal Packet if any.

Metric: Preserve W1 evidence quality. Do not expand W2, M2, Q2, or Y2 until the
W1 review heartbeat runs.

After each turn: If an executable leaf is selected, create or update that child
Goal Packet and output its leaf native /goal prompt. Do not run the whole
portfolio as a native Goal and do not create hidden automation.
```

## First Leaf Native Goal Prompt

```text
/goal Run the child Goal Packet for TASK-0001 Define first toy offer.

Task: Define the first toy offer for the AGI Toy Shop W1 frontier. Use the
parent portfolio only as context; execute this leaf task to artifact, blocker,
or review-ready completion.

Logging: Before ending each turn, append a compact entry to the child
TASK-0001 progress.md with actions, artifacts, metric sample, drift verdict,
next action, and blockers.

Metric: Use review + artifact evidence for offer clarity and usefulness. Do not
claim market validation before tracking or launch evidence exists.

After each turn: Continue only this leaf task until complete, blocked, or
review-ready. On completion, append a completion entry that tells the parent
heartbeat to update TASK-0001 and choose the next eligible sibling.
```
