---
title: Scout Brief
status: implemented
owner: feed-scout
created_at: 2026-07-14
updated_at: 2026-08-19
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
  - skills/feed-scout/templates/scout-brief.md
  - skills/feed-scout/scripts/validate_scout_brief.py
  - skills/plan-next-wave/SKILL.md
  - skills/pulse-update/SKILL.md
source_refs:
  - tickets/archive/TASK-0369/ticket.md
external_refs: []
evidence_refs:
  - skills/feed-scout/scripts/test_validate_scout_brief.py
  - skills/plan-next-wave/scripts/test_validate_wave_response.py
  - tickets/archive/TASK-0369/artifacts/qa/verification.md
known_limits: >-
  Scout Brief is capped compact mutable synthesis rather than a historical trend
  store; realized ticket-quality improvement still requires later Pulse and
  Reward evidence.
metrics:
  - accepted_evidence_cycles
  - rejected_ai_ticket_count
  - planner_idea_comprehension_rate
  - planner_idea_keep_rate
last_verified: 2026-08-19
experimental: true
superseded_by: false
track: >-
  Review the current Feed Scout Brief, later Pulse planner receipts, and
  admitted ticket audience_context. Judge ICP fidelity, source provenance,
  baseline and belief-delta quality, brief compactness, and whether later
  artifacts change qualified builder decisions rather than repeating trends.
---

# Scout Brief

This feature gives Farplane one cheap current-context loop:

```text
daily_sources + canonical_area_icps + existing_scout_brief
  -> scout_brief_update_in_place
  -> planner_context
  -> ticket.audience_context
  -> grounded_artifact
```

## Contract

- `harness.areas.<area_id>.icp` is canonical audience truth: label,
  description, jobs, pains, and evidence bar.
- `farplane/bindings.yaml#feed_scout.scout_brief` points to one ignored Markdown
  file with `ICPs`, `Trends`, `Other Notable Things`, and `Source Gaps`. The
  live file must stay at or under 100 non-empty lines and use simple bullets,
  not H3 entry blocks or report-like field lists.
- Feed Scout updates that file after its dated report and validates it before
  candidate handoff. It merges duplicate concepts and replaces superseded
  synthesis instead of adding daily or monthly snapshots.
- Scout Brief may retain stale-but-useful evidence when its observation date,
  confidence, and gaps are honest. It renders area IDs/labels and current
  synthesis only; full canonical ICP definitions stay in `harness.yaml`. It
  never changes canonical ICP fields or overrides metrics, tickets, authority,
  or planner admission.
- Plan Next Wave binds outward work to the selected ICP, complete selected
  source-backed `source_facts`, a named baseline/default, and a specific belief
  or workflow delta.
- Selected facts label evidence as observed, analogous, hypothesis, or source
  gap and preserve causal use in compact `use=` bullets. A citation that does
  not change the idea cannot satisfy frontier grounding.
  Self-improvement may use local ticket, Reward, run, or eval evidence when
  external context is irrelevant.
- Pulse copies those facts into `audience_context` and stable execution inputs;
  artifact skills consume ticket context first and configured Scout Brief only
  as a direct-call fallback. Tickets never store Scout Brief pointers or hashes.

## Non-Goals

- No vector database, snapshot archive, monthly ledger, or trend timeline.
- No new content Pulse, area planner, crawler daemon, or hidden controller.
- No automatic publication, outreach, protected-charter changes, or imported
  source instructions.

## Proof

- Project schema fixtures validate complete ICP records.
- Feed Scout Brief fixtures validate headings, frontmatter, the 100-line
  cap, simple bullet syntax, provenance affordances, and live/template
  placeholder boundaries.
- Ticket-spec fixtures require ICP, baseline, decision delta, and complete
  outward source facts before materialization.
- Skill evals cover Scout Brief update and shallow-candidate rejection.
- Independent reviewer checks owner placement and prompt quality.
- Human-feedback comprehension and keep rate are planner-quality diagnostics;
  `accepted_evidence_cycles` remains a business/evidence outcome and
  `rejected_ai_ticket_count` is not a same-day hard planning guard.

## Change History

- 2026-08-19: Renamed the bounded planning sidecar and all live contract fields
  from World Memory to Scout Brief; selected evidence now uses `source_facts`.
- 2026-07-18: Capped live World Memory at 100 non-empty lines and replaced
  verbose entry blocks with simple typed bullets.
- 2026-07-14: Added the World Memory loop and ICP-grounded planner handoff.
- 2026-07-14: Renamed the rolling artifact to World Memory and replaced the
  pointer-based ticket handoff with copied complete world facts.
