---
title: "Typed entity view projections"
status: implemented
owner: farplane-framework
created_at: 2026-07-31
updated_at: 2026-08-19
tags:
  - farplane
  - feature
  - sys-0014
  - projections
refs:
  - docs/systems/wiki.md
  - docs/farplane-framework/entity-view-projection-standard.md
  - docs/farplane-framework/entity-markdown-authoring.md
feature_id: FEAT-0076
system_id: SYS-0014
category: projections
public: true
surfaces:
  - bin/core/farplane_entities.py
  - bin/core/farplane_wiki.py
  - docs/farplane-framework/entity-view-projection-standard.md
  - docs/farplane-framework/entity-markdown-authoring.md
  - skills/init-advisor/scripts/bootstrap.sh
source_refs:
  - tickets/archive/TASK-0402/ticket.md
  - docs/farplane-framework/entities.md
external_refs: []
evidence_refs:
  - bin/tests/test_farplane_wiki.py
  - bin/tests/test_farplane_entities.py
  - docs/HISTORY.md
known_limits: "Typed views use explicit local membership and a bounded vocabulary for events, metrics, resources, weights, and transfers; arbitrary domain aggregations or UI products may still need a view-specific adapter."
metrics: []
last_verified: 2026-08-02
experimental: false
superseded_by: false
track: false
---

# Typed entity view projections

Typed entity views interpret selected canonical entities with a project-local
domain vocabulary while preserving the generic Wiki graph. They let one entity
set power market, infrastructure, relationship, or other specialized views
without copying entity truth.

```text
typed_view(private_entity_registry, graph, views_yaml)
  -> views/<view-id>.json
```

## At A Glance

- Feature ID: `FEAT-0076`
- System: [Wiki](../systems/wiki.md)
- Status: `implemented`
- Category: `projections`
- Primary user: project maintainer and specialized graph consumer
- Job: interpret canonical entities and evidence through an explicit local
  schema

## Problem

The generic Wiki graph can preserve who is connected and what sourced prose
says, but it cannot know whether a project's tags represent capital, power,
capacity, status, confidence, or a real directed transfer. Adding every domain
field to generic entity frontmatter would make the core schema unstable.

## What It Does

- Reads named view membership from `.farplane/views.yaml`.
- Validates view IDs, names, ordered canonical entity IDs, and duplicate keys.
- Lets each view declare relations, resources, units, resource tags, metric
  tags, problems, and status/confidence weights.
- Reads `## View`, `Latest Status`, `Timeline`, and inline `[key:value]` tags
  from canonical entity Markdown.
- Produces typed events, observations, resource summaries, undirected
  relationship bundles, and explicitly directed resource flows.
- Emits schema-v4 selected entity nodes without raw frontmatter or generic metadata.
- Deletes stale generated view JSON after a view is removed from configuration.

## User Stories

- As a project maintainer, I can define a domain vocabulary without changing
  the generic entity schema.
- As a specialized consumer, I can distinguish observations and dependencies
  from transfers that really moved between entities.
- As a reviewer, I can trace every event and flow to dated source prose.

## Operating Contract

`.farplane/views.yaml` owns membership and vocabulary. Entity Markdown owns
identity, prose, latest status, timelines, links, and source URLs.
`.farplane/views/<view-id>.json` is disposable output.

Relationships remain one undirected bundle per entity pair. A view may overlay
directed `resource_flows`, but only an explicit `transfer` mapping with one
linked counterparty emits a flow. Supply, demand, partnership, or a resource
mention alone never proves a transfer.

## Feature Flow

```mermaid
flowchart LR
  entities["entity Markdown<br/>view sections + timeline tags"] --> compiler["Wiki typed-view compiler"]
  schema["views.yaml<br/>membership + vocabulary"] --> compiler
  graph["generic graph.json"] --> compiler
  compiler --> view["views/<id>.json<br/>events + observations<br/>relationships + flows"]
```

## Surfaces

- Owner surfaces:
  - `bin/core/farplane_entities.py`
  - `docs/farplane-framework/entity-view-projection-standard.md`
- Supporting surfaces:
  - `docs/farplane-framework/entity-markdown-authoring.md`
  - `skills/init-advisor/scripts/bootstrap.sh`
- Generated surfaces:
- `.farplane/views/<view-id>.json`
  - bounded normalized view membership in the Wiki graph plus typed interpretation

## Proof And Quality

- `python3 -m unittest bin/tests/test_farplane_entities.py`
- `farplane wiki rebuild --project-root <project> --no-write`
- Tests cover membership and fingerprints, malformed schemas, status and
  confidence, metrics, unit normalization, observations, transfer directions,
  evidence timelines, and stale projection deletion.

## Rollout And Maintenance

- Extend `.farplane/views.yaml` vocabulary before adding project-specific core
  frontmatter.
- Keep generic `graph.json` semantics stable when typed view behavior changes.
- Version typed output when consumers require an incompatible schema change.
- Remove a view from YAML and rebuild to remove its generated JSON.

## Limits And Non-Goals

- Membership is explicit rather than query-defined.
- The generic compiler supports its declared event/resource model; it does not
  promise every domain aggregation or UI behavior.
- No view owns or duplicates canonical entity data.
- Delete or merge this feature only if typed domain interpretation stops being
  independently maintainable from generic Wiki graph.

## Alternatives Considered

- Option: add project-specific fields to generic entity frontmatter.
  Decision: reject.
  Reason: it couples every project vocabulary to one unstable global schema.
- Option: create separate domain entity stores.
  Decision: reject.
  Reason: copied identity and evidence would drift from canonical Markdown.

## Change History

- 2026-08-19: Moved typed entity views from Graph Systems to Wiki ownership
  and adopted Wiki rebuild/sync lifecycle commands.
- 2026-08-02: Replaced typed-view schema v3 with schema v4 lean entity nodes
  while preserving event, observation, relationship, flow, and summary semantics.
- 2026-07-31: Added the registry-backed feature owner for existing typed view
  behavior.
