---
title: Pulse and interval automation
status: retired
owner: feature-registry
created_at: 2026-07-07
updated_at: 2026-09-20
tags:
  - farplane
  - feature
  - retired
refs:
  - docs/features/FEAT-0067-daily-interval-review-reports.md
  - docs/features/FEAT-0071-project-work-pulse.md
feature_id: FEAT-0065
system_id: SYS-0003
category: planning
public: true
surfaces:
  - farplane/automations/
  - skills/pulse-update/SKILL.md
  - skills/automation-advisor/SKILL.md
source_refs:
  - docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md
external_refs: []
evidence_refs:
  - skills/pulse-update/evals/evals.json
  - skills/automation-advisor/audits/2026-09-20-company-os-adoption.md
known_limits: "Retired umbrella retained as migration history. Work Pulse and Company OS Daily/Weekly own the active behavior."
metrics:
  - pulse_action_relevance
  - interval_report_usefulness
  - ticket_supply_learning
last_verified: 2026-09-20
experimental: false
superseded_by:
  - FEAT-0067
  - FEAT-0071
track: false
---

# Pulse And Interval Automation

This umbrella feature is retired. It formerly grouped Work Pulse with the
`interval-update` skill and Daily/Weekly BAU reports.

Current ownership is split:

- [FEAT-0071](FEAT-0071-project-work-pulse.md) owns the sole execution heartbeat.
- [FEAT-0067](FEAT-0067-daily-interval-review-reports.md) owns Company OS Daily
  and Weekly through `pm-daily` and `pm-weekly`.
- `automation-advisor` owns desired and live scheduler configuration.
- Farplane Core owns metric refresh planning and deterministic reducers.

The former Interval skill, weekly draft, knowledge-promotion route, and recovery
ticket admission were deleted after all active consumers moved to these owners.
Historical audit and memory text may mention the retired name but grants no
runtime or configuration authority.
