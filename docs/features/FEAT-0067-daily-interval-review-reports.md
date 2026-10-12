---
title: Company OS daily and weekly operating reviews
status: implemented
owner: feature-registry
created_at: 2026-07-07
updated_at: 2026-10-12
tags:
  - farplane
  - feature
  - sys-0003
  - company-os
refs:
  - skills/report-gen/SKILL.md
  - skills/automation-advisor/SKILL.md
  - docs/farplane-framework/pulse-and-interval-loop.md
feature_id: FEAT-0067
system_id: SYS-0003
category: planning
public: true
surfaces:
  - skills/report-gen/SKILL.md
  - skills/report-gen/templates/project-memory.md
  - skills/report-gen/templates/project-report.md
  - skills/report-gen/templates/company-report.md
  - farplane/automations/
source_refs:
  - docs/farplane-framework/pulse-and-interval-loop.md
  - docs/prd.md
external_refs: []
evidence_refs:
  - skills/report-gen/evals/evals.json
  - skills/automation-advisor/audits/2026-09-20-company-os-adoption.md
known_limits: "Daily and Weekly maintain operating memory and existing work. They do not choose strategy, admit tasks, start Multica execution, or perform external side effects."
metrics:
  - operating_review_usefulness
last_verified: 2026-10-12
experimental: true
superseded_by: false
track: >-
  Review Daily and Weekly source coverage, money-linked movement, constraints,
  commitments, stale-write protection, and whether the run avoided strategy
  invention, task admission, Multica execution, and unsafe side effects.
  Return continue, adjust, cap, pause, graduate, or source_gap.
---

# Company OS Daily And Weekly Operating Reviews

Farplane adopts Zanarkand AI's proven four-stage boundary:

```text
automation fetches and freezes sources
-> automation caches isolated local inputs
-> PM skill emits one JSON extraction
-> automation validates, renders, applies, and reads back
```

Daily runs `report-gen` in `daily` mode once per eligible Project. It reconstructs the
operator-defined commercial bet from project-local Farplane configuration,
judges movement from results, identifies the constraint closest to the next
monetization event, and selects one next commitment.

Weekly runs `report-gen` in `weekly` mode once over the complete frozen Project set. It
consolidates observed movement, results, constraints, decisions, and next-week
commitments. Missing Project coverage blocks weekly effects.

## Boundaries

- Multica is the task dashboard and evidence source; Codex executes work.
- Automations own provider reads/writes, pagination, source caches, rendering,
  stale-write checks, idempotency, and readback.
- PM skills read local files only and write exactly one JSON result.
- Actions may update authorized existing issues only. Both cadences forbid new
  task admission, autonomous strategy invention, broad knowledge promotion,
  external messages, and work execution.
- The former Interval skill and its weekly-draft/promotion machinery are
  deleted. Daily and Weekly have no compatibility path back to them.

## Proof

- Desired and live Daily prompts call `report-gen` in `daily` mode.
- Desired and live Weekly prompts call `report-gen` in `weekly` mode.
- No Work Pulse heartbeat remains; GitHub Issues hold work state.
- Eval contracts cover activity-versus-result judgment, incomplete coverage,
  money-adjacent unblocking, and the automation/skill boundary.

## Change History

- 2026-10-12: Daily moved from the deleted `progress-update` skill into
  `report-gen` `daily` mode (#41); its template and evals moved with it.
