---
status: companion
source: ticket.md
blocks_approval: false
canonical_contract: ticket.md
generated_by: diagramming
generation_lane: delegated subagent
---

# Visual Plan

## Reading Order

- Start with `Before` to see why one feedback loop currently has several
  competing strategy owners.
- Check `After` to see the proposed metric-to-ticket control loop and the
  refill-only boundary.
- Use `What Changed` for the compact contract replacements.
- Give scope feedback against `Feedback Guide`; `ticket.md` remains canonical.

## Before: One feedback loop is split across several strategy surfaces

Metrics expose values and raw differences, while Interval is intentionally
report-first and maintenance-limited. Mutable direction is then repeated across
goals, product bets, an uncalled strategy skill, planner inputs, and tickets.

```mermaid
flowchart TD
  classDef keep fill:#f8fafc,stroke:#cbd5e1,color:#334155
  classDef problem fill:#fff5f5,stroke:#dc2626,color:#991b1b

  observations["metric observations<br/>value + raw daily_diff"]:::problem
  interval["Daily / Weekly Interval<br/>report + capped known fixes"]:::problem
  goals["harness goals<br/>target + date"]:::problem
  bets["identity.product_bets<br/>solution portfolio"]:::problem
  strategy["update-strategy<br/>no live caller"]:::problem
  refill["Plan Next Wave<br/>also receives goals + bets"]:::problem
  tickets["ticket board<br/>priority, dependencies, proof"]:::keep
  pulse["Pulse<br/>priority → ticket ID"]:::problem
  execution["worker / native Goal Packet"]:::keep

  observations --> interval
  interval -. "ungrounded or new direction waits" .-> refill
  goals --> refill
  bets --> refill
  strategy -. "similar reasoning, separate owner" .-> tickets
  refill --> tickets
  tickets --> pulse --> execution
```

Legend:

- red = current problem, duplicated state, or behavior being replaced
- gray = canonical execution context that stays
- dashed edge = indirect, delayed, or unclear ownership

## After: Metric movement flows directly through Interval into proofable work

Stable intent constrains review and refill, but mutable strategy lives only on
the ticket board. Daily and Weekly use the same first-principles reasoning over
different evidence windows; Plan Next Wave remains a side-effect-free fallback
when the board needs refill and Interval lacks grounded work.

```mermaid
flowchart TD
  classDef keep fill:#f8fafc,stroke:#cbd5e1,color:#334155
  classDef added fill:#ecfdf5,stroke:#10b981,color:#065f46
  classDef changed fill:#fffbeb,stroke:#f59e0b,color:#92400e

  intent["stable intent<br/>problems + areas + objective metrics"]:::keep
  observations["metric observations<br/>previous + current"]:::keep
  movement["derive_metric_movement(...)<br/>delta + velocity + momentum"]:::added
  interval["Daily / Weekly Interval<br/>same review, different window"]:::changed
  report["dated report<br/>written before board mutation"]:::added
  decision{"intervention grounded?"}:::changed
  direct["known intervention<br/>create / update ticket"]:::added
  investigate["uncertain cause<br/>decision-changing evidence ticket"]:::added
  noTicket["insufficient evidence<br/>no ticket mutation"]:::keep
  refill["Plan Next Wave<br/>low-supply refill only"]:::changed
  board["only mutable strategy state<br/>priority + due_at + deps + proof"]:::changed
  pulse["Pulse ordering<br/>priority → due_at → ticket ID"]:::changed
  execution["worker / native Goal Packet"]:::keep

  observations --> movement --> interval --> report --> decision
  intent --> interval
  decision -->|"known"| direct --> board
  decision -->|"uncertain but testable"| investigate --> board
  decision -->|"not grounded"| noTicket
  noTicket -. "later, if ready supply is low" .-> refill
  intent --> refill
  refill -->|"validated skill call"| board
  board --> pulse --> execution
```

Legend:

- green = added derived capability, artifact, or direct admission path
- amber = changed owner, behavior, routing, or ordering
- gray = stable context or existing execution mechanism retained
- dashed edge = conditional later fallback, not a required hop

## What Changed

Diagram intent: compress the six implementation units into direct old-to-new
contract replacements.

```mermaid
flowchart LR
  classDef before fill:#fff5f5,stroke:#dc2626,color:#991b1b
  classDef after fill:#ecfdf5,stroke:#10b981,color:#065f46
  classDef changed fill:#fffbeb,stroke:#f59e0b,color:#92400e

  metricOld["before: raw metric diff"]:::before --> metricNew["after: direction-normalized movement"]:::after
  intervalOld["before: capped report recovery"]:::before --> intervalNew["after: first-principles ticket admission"]:::after
  stateOld["before: goals + bets + strategy skill"]:::before --> stateNew["after: ticket board is mutable strategy"]:::after
  refillOld["before: planner gates known work"]:::before --> refillNew["after: planner refills weak supply"]:::changed
  deadlineOld["before: priority → ticket ID"]:::before --> deadlineNew["after: priority → due_at → ticket ID"]:::after
  docsOld["before: competing owner docs"]:::before --> docsNew["after: one control-loop contract"]:::after
```

Legend:

- red = retired or replaced contract
- green = new contract or capability
- amber = retained component with a narrower responsibility

## Short Notes

- Positive progress velocity always means favorable movement; `minimize`
  metrics invert the raw direction.
- Ticket admission requires materiality, executability, concrete proof, and no
  active duplicate; there is no numeric ticket cap.
- An investigation ticket is an outcome ticket only when it must reproduce the
  cause, rule out alternatives, select a correction, and emit proof.
- `due_at` is delivery timing, `priority` is importance, and
  `Reward.check_in_at` remains outcome-evaluation timing.
- Native Goal mode and ticket Goal Packets stay intact; only the project-level
  `goals` array is retired.

## Feedback Guide

- Does `Before` honestly show the latency and duplicate ownership being removed?
- Does `After` make it clear that Interval writes its report before ticket
  mutation?
- Is the boundary between same-run Interval admission and later low-supply
  refill unambiguous?
- Are metric direction, investigation outcomes, deadline ordering, and native
  Goal preservation represented correctly?
- Is any replacement in `What Changed` missing, unnecessary, or scoped
  incorrectly?
- Does any requested scope correction need to go back into canonical
  `ticket.md`?
