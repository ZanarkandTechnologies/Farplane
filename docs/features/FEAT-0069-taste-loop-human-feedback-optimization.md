---
title: Retired Taste Loop human-feedback optimization
status: retired
owner: feature-registry
created_at: 2026-07-07
updated_at: 2026-07-11
tags:
  - farplane
  - feature
  - sys-0007
refs:
  - skills/dogfood-review/SKILL.md
  - skills/optimize-with-human/SKILL.md
  - skills/pulse-update/SKILL.md
  - skills/worker-artifact-review-request/SKILL.md
  - docs/features/FEAT-0070-experimental-feature-evaluation-reports.md
  - docs/features/FEAT-0071-project-work-pulse.md
feature_id: FEAT-0069
system_id: SYS-0007
category: improvement-loop
public: true
surfaces:
  - skills/dogfood-review/SKILL.md
  - skills/optimize-with-human/SKILL.md
  - skills/pulse-update/SKILL.md
  - skills/worker-artifact-review-request/SKILL.md
source_refs:
  - docs/systems/self-improvement-learning.md
  - docs/farplane-framework/v1.md
external_refs: []
evidence_refs:
  - tickets/archive/TASK-0326/artifacts/metadata-field-audit.md
known_limits: "Retired as a standalone controller; human-feedback experiments now use normal ticket Goal Packets and the shared Work Pulse."
metrics: []
last_verified: 2026-07-11
experimental: false
superseded_by:
  - FEAT-0070
  - FEAT-0071
track: false
---

# Retired Taste Loop human-feedback optimization

Taste Loop is retired as a standalone skill and scheduled controller. Its
useful primitives were smaller than the controller:

```text
Dogfood/self-improvement -> feedback experiment Goal Packet
Work Pulse               -> execute ticket and due check-ins
optimize-with-human       -> human feedback as the metric when appropriate
worker review request     -> initial or due Telegram request
progress.md Review block  -> mutable wait/reminder/reply state
```

Human review waits release the execution worker. The bound persistent thread
may wake on a direct reply, but an inactive thread is not worker occupancy.
Review WIP limits new supply; it does not itself trigger reminders. Pulse may
reconcile at most one review whose ticket-owned `next_reminder_at` is due.

This decomposition also prevents human-taste work from becoming a second
project heartbeat. The only heartbeat is Work Pulse; weekly Dogfood creates a
bounded improvement wave and all execution stays on the shared board.

## CRM Boundary

Prospects and customers are durable CRM records, not long-lived BAU tickets.
A CRM record may create a bounded action or experiment ticket that references
the record; the ticket returns the result and closes. Waiting CRM relationships
do not consume Work Pulse worker or review WIP capacity.

## Change History

- 2026-07-07: Created as an experimental Taste Loop handle.
- 2026-07-11: Retired by TASK-0326; behavior decomposed into self-improvement
  ticket supply, Work Pulse execution/check-ins, and ticket-owned review state.
