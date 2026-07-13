---
status: companion
source: ticket.md
blocks_approval: false
canonical_contract: ticket.md
generated_by: diagramming
generation_lane: inline fallback
---

# Visual Plan

## Before: duplicated QA contracts drift

```mermaid
flowchart LR
  classDef keep fill:#f8fafc,stroke:#cbd5e1,color:#334155
  classDef problem fill:#fff5f5,stroke:#dc2626,color:#991b1b
  ticket["Done + QA Strategy"]:::keep --> guide["browser-first guide"]:::problem
  ticket --> skill["current qa contract"]:::problem
  guide --> tester["stale oversized tester"]:::problem --> receipt["weak receipt"]:::problem
  skill --> receipt
```

Legend: red = drift; gray = retained canonical context.

## After: one contract drives the complete journey

```mermaid
flowchart LR
  classDef keep fill:#f8fafc,stroke:#cbd5e1,color:#334155
  classDef added fill:#ecfdf5,stroke:#10b981,color:#065f46
  classDef changed fill:#fffbeb,stroke:#f59e0b,color:#92400e
  ticket["Done + QA Strategy"]:::keep --> qa["qa<br/>canonical contract"]:::changed
  qa --> tester["qa-tester<br/>operate + capture"]:::changed
  tester --> judge["independent judgment"]:::keep
  judge --> result["validated receipt + Links"]:::added
  result --> learn["ticket | cookbook | follow-up"]:::added
```

Legend: amber = changed owner; green = added capability; gray = retained boundary.

## What Changed

```mermaid
flowchart TD
  classDef before fill:#fff5f5,stroke:#dc2626,color:#991b1b
  classDef after fill:#ecfdf5,stroke:#10b981,color:#065f46
  stale["retired ticket fields"]:::before --> current["Done + QA Strategy + Links"]:::after
  images["images for every run"]:::before --> conditional["proof-type evidence"]:::after
  lost["learning stays in report"]:::before --> durable["explicit learning decision"]:::after
```

## Feedback Guide

- Is `qa` the single contract owner?
- Does the tester retain hard gates without duplicating recipes?
- Is shared learning selective and durable?
