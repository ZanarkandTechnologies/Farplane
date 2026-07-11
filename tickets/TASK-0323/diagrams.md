---
status: companion
source: ticket.md
blocks_approval: false
canonical_contract: ticket.md
generated_by: diagramming
---

# TASK-0323 Visual Plan

## Before: agents orchestrate validators manually

```mermaid
flowchart LR
  classDef problem fill:#fff5f5,stroke:#dc2626,color:#991b1b
  classDef keep fill:#f8fafc,stroke:#64748b,color:#334155
  agent["agent"]:::keep --> a["ticket check"]:::problem
  agent --> b["skill checks"]:::problem
  agent --> c["docs checks"]:::problem
  agent --> d["project checks"]:::problem
```

Legend: red is fragmented manual invocation; gray is retained agency.

## After: one ticket API selects modular checks

```mermaid
flowchart LR
  classDef added fill:#ecfdf5,stroke:#10b981,color:#065f46
  classDef changed fill:#fffbeb,stroke:#f59e0b,color:#92400e
  classDef keep fill:#f8fafc,stroke:#64748b,color:#334155
  agent["agent"]:::keep --> api["farplane validate ticket"]:::added
  api --> select["phase + explicit paths"]:::changed
  select --> core["Farplane checks"]:::keep
  select --> skills["skill-local checks"]:::keep
  core --> receipt["one receipt"]:::added
  skills --> receipt
```

Legend: green is new API/evidence; amber is changed selection; gray stays modular.
