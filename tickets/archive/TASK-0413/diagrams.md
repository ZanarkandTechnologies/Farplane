---
status: companion
source: ticket.md
blocks_approval: false
canonical_contract: ticket.md
generated_by: diagramming
generation_lane: inline
---

# Visual Plan

## Reading Order

- `Before` shows the ambiguous demo output and missing Goal handoff.
- `After` shows the single owner and completion sequence.

## Before: Demo format and invocation vary by ticket

```mermaid
flowchart LR
  classDef keep fill:#f8fafc,stroke:#cbd5e1,color:#334155
  classDef problem fill:#fff5f5,stroke:#dc2626,color:#991b1b

  qa["QA evidence"]:::keep --> choose["Choose screenshots, HTML, slides, clip, or video"]:::problem
  choose --> pack["Generic demo package"]:::problem
  goal["Goal completion"]:::problem -. optional .-> pack
  pack --> review["Completion review"]:::keep
```

Legend:

- Red = ambiguous or unreliable behavior.
- Gray = existing evidence/review flow that stays.

## After: Demo owns one evidence-grounded recap

```mermaid
flowchart LR
  classDef keep fill:#f8fafc,stroke:#cbd5e1,color:#334155
  classDef added fill:#ecfdf5,stroke:#10b981,color:#065f46
  classDef changed fill:#fffbeb,stroke:#f59e0b,color:#92400e

  goal["Material implementation Goal"]:::keep --> qa["QA pass"]:::keep
  qa --> demo["demo(ticket, passed_qa)"]:::changed
  demo --> plan["Ticket-scoped content plan"]:::added
  plan --> mp4["Narrated MP4 + evidence map"]:::added
  mp4 --> review["TAS-A completion review"]:::keep
  review --> close["Close ticket"]:::keep
```

Legend:

- Amber = changed owner or behavior.
- Green = new artifact or capability.
- Gray = canonical lifecycle steps retained.

## What Changed

```mermaid
flowchart LR
  classDef before fill:#fff5f5,stroke:#dc2626,color:#991b1b
  classDef after fill:#ecfdf5,stroke:#10b981,color:#065f46
  classDef changed fill:#fffbeb,stroke:#f59e0b,color:#92400e

  formats["Variable demo formats"]:::before --> recap["One narrated MP4"]:::after
  ticket["Ticket demo configuration"]:::before --> skill["Stable recipe in demo skill"]:::changed
  optional["Optional Goal handoff"]:::before --> program["Program invokes demo after QA"]:::after
```

## Feedback Guide

- Is `demo` clearly the sole recipe owner?
- Is the lifecycle visibly `QA → demo → review → close`?
- Are direct non-Goal changes correctly outside the new path?
