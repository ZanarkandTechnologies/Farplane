---
title: "CRM entity projection"
status: implemented
owner: farplane-framework
created_at: 2026-07-31
updated_at: 2026-08-19
tags:
  - farplane
  - feature
  - sys-0014
  - crm
refs:
  - docs/systems/wiki.md
  - docs/farplane-framework/entities.md
  - docs/farplane-framework/entity-markdown-authoring.md
feature_id: FEAT-0077
system_id: SYS-0014
category: projections
public: true
surfaces:
  - bin/core/farplane_entities.py
  - bin/core/farplane_wiki.py
  - docs/farplane-framework/entities.md
  - docs/farplane-framework/entity-markdown-authoring.md
source_refs:
  - tickets/archive/TASK-0399/ticket.md
  - docs/features/FEAT-0069-taste-loop-human-feedback-optimization.md
external_refs: []
evidence_refs:
  - bin/tests/test_farplane_wiki.py
  - bin/tests/test_farplane_entities.py
  - tickets/archive/TASK-0399/ticket.md
known_limits: "CRM is a generated funnel-bearing entity projection, not a campaign queue, outreach runtime, activity database, or authority to write customer data."
metrics: []
last_verified: 2026-08-02
experimental: false
superseded_by: false
track: false
---

# CRM entity projection

Farplane CRM is a generated view of canonical entities carrying non-empty
funnel state. It lets people, companies, opportunities, and relationships
participate in a pipeline without creating parallel CRM records.

```text
crm_projection(private_entity_registry)
  -> lean_funnel_bearing_entities
```

## At A Glance

- Feature ID: `FEAT-0077`
- System: [Wiki](../systems/wiki.md)
- Status: `implemented`
- Category: `projections`
- Primary user: operator, sales workflow, and relationship workflow
- Job: expose durable entity identity and explicit funnel state as a CRM view

## Problem

A separate CRM store would duplicate people and companies already represented
in Entity Markdown. Using campaign or ticket stages as CRM truth would also
confuse short-lived execution state with durable relationship context.

## What It Does

- Selects only canonical entities whose frontmatter contains a non-empty
  `funnel` mapping.
- Preserves only the project-qualified entity key, entity ID, kind, name,
  canonical source path, and funnel state.
- Produces project identity and the shared source fingerprint without copying
  raw frontmatter, `by_id`, named views, compiler diagnostics, or derived counts.
- Removes an entity from CRM when its funnel mapping is removed while
  preserving the canonical entity and graph node.

## User Stories

- As an operator, I can promote an existing person or company into a pipeline
  without making a duplicate record.
- As an agent, I can distinguish durable funnel truth from campaign queues,
  ticket state, and inferred opportunities.
- As a consumer, I can detect whether CRM and the Wiki graph were compiled from the same
  source state.

## Operating Contract

Entity Markdown remains canonical. `crm.json` is never hand-edited. The
`funnel` mapping is project-owned and must be an object; the compiler does not
invent stages, opportunities, next actions, or consent.

Operational campaign stages remain in their campaign artifact. Tickets may
reference CRM entities and write validated results back through an approved
workflow, but waiting relationships do not become long-lived work tickets.

## Feature Flow

```mermaid
flowchart LR
  entities["canonical entity Markdown"] --> filter{"non-empty funnel?"}
  filter -->|yes| crm["crm.json<br/>entity + funnel"]
  filter -->|no| graph["Wiki graph/index only"]
  crm --> consumer["CRM consumer"]
```

## Surfaces

- Owner surfaces:
  - `bin/core/farplane_entities.py`
  - `docs/farplane-framework/entities.md`
- Supporting surfaces:
  - `docs/farplane-framework/entity-markdown-authoring.md`
- Generated surfaces:
  - `.farplane/entities/crm.json`

## Proof And Quality

- `python3 -m unittest bin/tests/test_farplane_entities.py`
- `farplane wiki rebuild --project-root <project> --no-write`
- Tests prove the exact lean schema, funnel filtering, malformed funnel
  rejection, schema version, fingerprint consistency, and empty CRM behavior.

## Rollout And Maintenance

- Add or update funnel state only through the canonical entity file.
- Sync the changed entity path after CRM-relevant authoring changes; rebuild
  when recovering or changing generated schemas.
- Keep campaign, outreach, and ticket runtime fields outside the funnel
  contract.
- Roll back by removing or restoring the source funnel mapping and rebuilding.

## Limits And Non-Goals

- No independent CRM database or mutable campaign queue.
- No automatic enrichment, outreach, sending, opportunity creation, or consent.
- No inference that a researched person is a qualified opportunity.
- Merge this feature only if funnel projection stops having an independently
  useful consumer contract.

## Alternatives Considered

- Option: maintain `.farplane/crm/` as a second entity store.
  Decision: reject.
  Reason: identity, context, and references would drift.
- Option: use tickets as CRM records.
  Decision: reject.
  Reason: tickets own bounded work; relationships may remain relevant without
  active work.

## Change History

- 2026-08-19: Moved CRM entity projection to Wiki ownership and adopted Wiki
  sync/rebuild lifecycle commands.
- 2026-08-02: Replaced CRM schema v3 with schema v4 lean identity/path/funnel
  records and removed raw frontmatter, duplicate lookup, views, diagnostics, and counts.
- 2026-07-31: Added the registry-backed feature owner for existing CRM
  projection behavior.
