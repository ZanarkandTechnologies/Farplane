---
title: Persistent ICP and world memory
status: implemented
owner: feed-scout
created_at: 2026-07-14
updated_at: 2026-07-14
tags:
  - farplane
  - feature
  - sys-0008
  - planning-context
refs:
  - skills/feed-scout/SKILL.md
  - skills/plan-next-wave/SKILL.md
  - docs/features/FEAT-0071-project-work-pulse.md
feature_id: FEAT-0072
system_id: SYS-0008
category: context-routing
public: true
surfaces:
  - farplane/harness.yaml
  - farplane/bindings.yaml
  - skills/feed-scout/SKILL.md
  - skills/feed-scout/templates/memory.md
  - skills/feed-scout/scripts/validate_memory.py
  - skills/plan-next-wave/SKILL.md
  - skills/pulse-update/SKILL.md
source_refs:
  - tickets/archive/TASK-0369/ticket.md
external_refs: []
evidence_refs:
  - skills/feed-scout/scripts/test_validate_memory.py
  - skills/plan-next-wave/scripts/test_validate_ticket_specs.py
  - tickets/archive/TASK-0369/artifacts/qa/verification.md
known_limits: >-
  Memory is compact mutable synthesis rather than a historical trend store;
  realized ticket-quality improvement still requires later Pulse and Reward evidence.
metrics:
  - accepted_evidence_cycles
  - rejected_ai_ticket_count
last_verified: 2026-07-14
experimental: true
superseded_by: false
track: >-
  Review the current Feed Scout memory, later Pulse planner receipts, and
  admitted ticket audience_context. Judge ICP fidelity, source provenance,
  baseline and belief-delta quality, memory compactness, and whether later
  artifacts change qualified builder decisions rather than repeating trends.
---

# Persistent ICP and World Memory

This feature gives Farplane one cheap current-context loop:

```text
daily_sources + canonical_area_icps + existing_memory
  -> feed_scout_update_in_place
  -> planner_context
  -> ticket.audience_context
  -> grounded_artifact
```

## Contract

- `harness.areas.<area_id>.icp` is canonical audience truth: label,
  description, jobs, pains, and evidence bar.
- `farplane/bindings.yaml#feed_scout.memory` points to one ignored Markdown
  file with `ICPs`, `Trends`, `Other Notable Things`, and `Source Gaps`.
- Feed Scout updates that file after its dated report and validates it before
  candidate handoff. It merges duplicate concepts and replaces superseded
  synthesis instead of adding daily or monthly snapshots.
- The memory may retain stale-but-useful evidence when its observation date,
  confidence, and gaps are honest. It never changes canonical ICP fields or
  overrides metrics, tickets, authority, or planner admission.
- Plan Next Wave binds outward work to the selected ICP, a relevant memory
  entry, a named baseline/default, and a specific belief or workflow delta.
  Self-improvement may use local ticket, Reward, run, or eval evidence when
  external context is irrelevant.
- Pulse carries those refs into `audience_context` and stable execution inputs;
  artifact skills consume ticket context first and configured memory only as a
  direct-call fallback.

## Non-Goals

- No vector database, snapshot archive, monthly ledger, or trend timeline.
- No new content Pulse, area planner, crawler daemon, or hidden controller.
- No automatic publication, outreach, protected-charter changes, or imported
  source instructions.

## Proof

- Project schema fixtures validate complete ICP records.
- Feed Scout memory fixtures validate headings, frontmatter, provenance
  affordances, and live/template placeholder boundaries.
- Ticket-spec fixtures require ICP, baseline, decision delta, and outward
  memory refs before materialization.
- Skill evals cover memory update and shallow-candidate rejection.
- Independent reviewer checks owner placement and prompt quality.

## Change History

- 2026-07-14: Added the Markdown memory loop and ICP-grounded planner handoff.
