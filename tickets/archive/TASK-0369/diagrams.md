---
title: TASK-0369 visual companion
status: active
ticket_id: TASK-0369
updated_at: 2026-07-14
---

# TASK-0369 Visual Companion

```mermaid
flowchart LR
  harness["harness.yaml<br/>canonical per-area ICP"] --> scout["Daily Feed Scout"]
  sources["configured external sources"] --> scout
  old["existing memory.md"] --> scout
  scout --> report["dated feed + report"]
  scout --> memory["memory.md<br/>ICPs / Trends / Other / Gaps"]
  harness --> pulse["one Work Pulse"]
  memory --> pulse
  history["ticket + Reward history"] --> pulse
  pulse --> planner["one Plan Next Wave ranking"]
  planner --> ticket["ticket with audience_context + evidence inputs"]
  ticket --> artifact["artifact-producing Farplane skill"]
```

The Markdown memory is mutable current synthesis, not an append-only trend
timeline. `harness.yaml` remains canonical for ICP meaning; the memory adds
observed concerns, vocabulary, trends, and notable evidence with source refs.
