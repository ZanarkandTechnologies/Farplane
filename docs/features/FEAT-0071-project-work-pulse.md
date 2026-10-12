---
title: Retired Project Work Pulse
status: retired
owner: feature-registry
created_at: 2026-07-10
updated_at: 2026-10-12
tags:
  - farplane
  - feature
  - sys-0003
  - retired
refs:
  - docs/farplane-framework/pulse-and-interval-loop.md
  - docs/prd.md
  - tickets/README.md
  - docs/features/FEAT-0072-scout-brief.md
feature_id: FEAT-0071
system_id: SYS-0003
category: planning
public: true
surfaces:
  - docs/features/FEAT-0071-project-work-pulse.md
source_refs:
  - docs/prd.md
external_refs: []
evidence_refs: []
known_limits: "Retired in #41 when the `pulse-update` executor and `plan-next-wave` refill planner skills were deleted. GitHub Issues hold work state; no Pulse executor skill or heartbeat automation remains."
metrics:
  - work_pulse_dispatch_correctness
  - empty_board_refill_quality
  - review_worker_release
last_verified: 2026-10-12
experimental: false
superseded_by: false
track: false
---

# Retired Project Work Pulse

Project Work Pulse is retired. It was retired in #41 when its `pulse-update`
executor and `plan-next-wave` refill planner skills were deleted. Work state
now lives in GitHub Issues (see [tickets/README.md](../../tickets/README.md));
there is no Pulse executor skill or heartbeat automation.

## Historical Behavior

The retired feature:

- ran one heartbeat per project that reconciled board state, serviced review
  and check-ins, and dispatched executable tickets by priority, then `due_at`;
- called a pure low-supply refill planner when ready supply fell below a
  watermark, ranking configured skill calls from stable problems, planning
  areas, metric movement, Scout Brief facts, and ticket history;
- materialized at most `wave_size` admitted calls as tickets; and
- released workers at human review while review reminders stayed
  ticket-owned.

## Change History

- 2026-07-10: Added as the Workstream 1 successor to FEAT-0066.
- 2026-07-11: Added derived experiment check-ins and shared execution for
  tickets informed by Feed Scout, Interval, and Dogfood.
- 2026-07-12: Made human-active work worker-free, replaced product descriptions
  with planning areas, added adaptive global-first history retrieval, and made
  scheduled sources context-only.
- 2026-07-14: Added FEAT-0072 ICP/world-memory retrieval and ticket context.
- 2026-07-16: Made Dogfood a report-only portfolio checkpoint.
- 2026-07-17: Replaced free-form work generation with configured skill
  calls and generic Pulse materialization.
- 2026-07-25: Narrowed refill to low supply, removed retired
  project-goal/product-bet planner inputs, and documented priority then
  due_at ordering.
- 2026-10-12: Retired in #41 when `pulse-update` and `plan-next-wave` were
  deleted; GitHub Issues hold work state.
