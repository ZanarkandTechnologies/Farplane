---
status: companion
source: ticket.md
blocks_approval: false
canonical_contract: ticket.md
generated_by: diagramming
generation_lane: inline fallback; ticket scope was already operator-approved
---

# Visual Plan

## Reading Order

- `Before` shows the reference-memory gap.
- `After` shows the checkpointed edit loop.
- `What Changed` compresses the ownership delta.

## Before: Visual reasoning disappears into prose

The agent repeatedly inspects an unchanged image and must remember linguistic
references without a durable spatial scratchpad.

```mermaid
flowchart LR
  classDef keep fill:#f8fafc,stroke:#cbd5e1,color:#334155
  classDef problem fill:#fff5f5,stroke:#dc2626,color:#991b1b

  image["source image"]:::keep --> inspect["one-shot inspection"]:::problem
  inspect --> prose["the third item near the left..."]:::problem
  prose --> answer["answer with reference drift"]:::problem
```

Legend: gray is retained input; red is the current fragile path.

## After: Latest image advances while checkpoints stay recoverable

The agent edits the latest deterministic view, reobserves it, and can revise
without destroying any earlier state.

```mermaid
flowchart LR
  classDef keep fill:#f8fafc,stroke:#cbd5e1,color:#334155
  classDef added fill:#ecfdf5,stroke:#10b981,color:#065f46
  classDef changed fill:#fffbeb,stroke:#f59e0b,color:#92400e

  source["source.png"]:::keep --> latest["latest.png"]:::changed
  latest --> mark["normalized marks"]:::added
  mark --> checkpoint["checkpoint N + receipt"]:::added
  checkpoint --> latest
  latest --> verify["reobserve + verify"]:::changed
  verify --> answer["answer with checkpoint evidence"]:::added
```

Legend: gray is immutable input; amber is updated current state; green is new
capability or evidence.

## What Changed

```mermaid
flowchart LR
  classDef before fill:#fff5f5,stroke:#dc2626,color:#991b1b
  classDef after fill:#ecfdf5,stroke:#10b981,color:#065f46

  old["prose-only visual references"]:::before --> new["rendered, replayable spatial references"]:::after
  overwrite["edit risks losing prior state"]:::before --> checkpoints["latest pointer + immutable checkpoints"]:::after
```

## Feedback Guide

- Is the immutable-checkpoint/latest-pointer split clear?
- Does any proposed operation exceed the simple first version?
- Should a heavy CV adapter remain deferred until a real failure case demands it?
