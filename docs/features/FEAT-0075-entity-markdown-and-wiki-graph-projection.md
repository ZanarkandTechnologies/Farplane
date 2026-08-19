---
title: "Entity Markdown and Wiki graph projection"
status: implemented
owner: farplane-framework
created_at: 2026-07-31
updated_at: 2026-08-19
tags:
  - farplane
  - feature
  - sys-0014
  - knowledge-graph
refs:
  - docs/systems/wiki.md
  - docs/farplane-framework/entities.md
  - docs/farplane-framework/entity-markdown-authoring.md
  - docs/features/FEAT-0079-wiki-resolution-and-incremental-projections.md
feature_id: FEAT-0075
system_id: SYS-0014
category: memory
public: true
surfaces:
  - bin/core/farplane_entities.py
  - bin/core/farplane_wiki.py
  - bin/farplane.py
  - docs/farplane-framework/entities.md
  - docs/farplane-framework/entity-markdown-authoring.md
  - skills/manage-wiki/SKILL.md
source_refs:
  - tickets/TASK-0438/ticket.md
  - tickets/TASK-0441/ticket.md
  - tickets/archive/TASK-0395/ticket.md
  - tickets/archive/TASK-0399/ticket.md
external_refs: []
evidence_refs:
  - bin/tests/test_farplane_wiki.py
  - bin/tests/test_farplane_entities.py
  - tickets/archive/TASK-0399/ticket.md
known_limits: "The Wiki graph projection and identity resolver are project-local and paragraph-backed; cross-project identity, cloud sync, graph-database queries, inferred predicates, and automatic ambiguous merges remain separate concerns."
metrics: []
last_verified: 2026-08-19
experimental: false
superseded_by: false
track: false
---

# Entity Markdown and Wiki graph projection

Farplane stores durable project entities as human-readable Markdown and
compiles them into a deterministic search index and generic Wiki graph. This
feature gives projects one canonical place for identity, useful context,
question-backed claims, sourced timelines, and explicit relationships.

```text
wiki_graph(.farplane/entities/*.md)
  -> index.json + graph.json + validation_issues
```

## At A Glance

- Feature ID: `FEAT-0075`
- System: [Wiki](../systems/wiki.md)
- Status: `implemented`
- Category: `memory`
- Primary user: project maintainer and agent
- Job: preserve durable entity facts in readable files and produce a generic
  graph without introducing a second source of truth

## Problem

Research reports and transcripts contain useful facts, but they are dated,
owner-specific artifacts rather than stable entity memory. Storing canonical
entities directly in generated JSON would make edits opaque and mix authored
truth with disposable indexes.

## What It Does

- Reads flat `.farplane/entities/<id>.md` files with required `id`, `kind`, and
  `name` frontmatter.
- Emits a schema-v5 lookup index containing bounded identity, alias, location,
  reference, question, and canonical-path fields.
- Compiles `[label](entity:<id>)` links into sourced, paragraph-backed,
  undirected Wiki graph associations.
- Compiles question footnotes into claims and question indexes without turning
  questions into default graph nodes.
- Compiles dated timeline evidence, aliases, locations, and optional
  coordinates.
- Emits project-qualified node and edge keys plus a deterministic source
  fingerprint.
- Exports the same Wiki graph projection after either a clean Wiki rebuild or a
  validated page-scoped sync.
- Emits schema-v4 graph nodes without raw frontmatter, generic metadata,
  repeated diagnostics, or derived counts.
- Reports malformed files, IDs, references, links, coordinates, questions, and
  other authoring issues instead of guessing.

## User Stories

- As a project maintainer, I can edit durable facts in Markdown and regenerate
  machine views deterministically.
- As an agent, I can resolve identities through the index and follow `path` to
  inspect the canonical prose behind a graph association.
- As a graph consumer, I can detect stale mixed projections through the shared
  source fingerprint.

## Operating Contract

Entity Markdown is canonical. `index.json` and `graph.json` are generated and
must not be hand-edited. The filename stem equals the entity ID, nested entity
folders are invalid, and explicit body links are the only authored Wiki graph
associations.

`.farplane/wiki/wiki.sqlite` is also generated. It caches parsed pages and
originating-page edge claims so a Wiki sync can replace only claims authored by
changed or deleted articles. Undirected graph identity does not remove claim
ownership: editing entity B never deletes an inbound claim authored by entity
A. A clean rebuild must export the same JSON as incremental sync.

`index.json` is a lookup catalogue, not a document snapshot. It omits Markdown
bodies, raw frontmatter, claims, timelines, funnel state, view definitions, and
duplicate `by_id` records. Its envelope contains only schema version, source
fingerprint, and entity rows. The graph projection likewise omits raw frontmatter and generic
metadata. Consumers needing full context read the canonical file referenced by
`path`; compiler diagnostics come from the command result.

The generic Wiki graph does not infer predicates, inverse relationships,
transfers, or private facts. Project-specific interpretation belongs in
[Typed entity view projections](FEAT-0076-typed-entity-view-projections.md).
Funnel selection belongs in [CRM entity projection](FEAT-0077-crm-entity-projection.md).

See [Entity Markdown Authoring](../farplane-framework/entity-markdown-authoring.md)
for the complete write contract.

## Feature Flow

```mermaid
flowchart LR
  markdown["entity Markdown<br/>identity + prose + evidence"] --> wiki["Wiki Core<br/>validate + cache + fingerprint"]
  wiki --> sqlite["wiki.sqlite<br/>pages + labels + edge claims"]
  wiki --> index["index.json<br/>bounded lookup + source path"]
  wiki --> graph["graph.json<br/>nodes + associations<br/>claims + questions + timeline"]
  wiki --> issues["validation issues"]
```

## Surfaces

- Owner surfaces:
  - `bin/core/farplane_entities.py`
  - `bin/core/farplane_wiki.py`
  - `docs/farplane-framework/entities.md`
  - `docs/farplane-framework/entity-markdown-authoring.md`
- Supporting surfaces:
  - `skills/manage-wiki/SKILL.md`
  - `bin/farplane.py`
- Generated surfaces:
  - `.farplane/wiki/wiki.sqlite`
  - `.farplane/entities/index.json`
  - `.farplane/entities/graph.json`

## Proof And Quality

- `python3 -m unittest bin/tests/test_farplane_entities.py`
- `python3 -m unittest bin/tests/test_farplane_wiki.py`
- `farplane wiki rebuild --project-root <project> --no-write`
- Tests cover the bounded index schema, absence of duplicated prose,
  lean graph nodes, deterministic compilation, entity validation, associations, questions,
  claims, timelines, coordinates, code masking, and project identity.

## Rollout And Maintenance

- Update the authoring and framework contracts when parser-visible Markdown
  changes.
- Update tests before changing schema or semantic key material.
- Sync affected article paths after bounded authoring changes; run a clean
  rebuild after parser or generated-schema changes.
- Roll back by reverting source Markdown or compiler behavior and rebuilding;
  generated projections are disposable.

## Limits And Non-Goals

- No graph database, inferred ontology, automatic geocoding, or cross-project
  entity merge.
- No duplicate authored edge records.
- Full dated research remains in skill-owned reports and links into canonical
  entities when durable.
- Merge this feature only if canonical entity authoring and the generic Wiki graph
  projection move together to a clearer owner.

## Alternatives Considered

- Option: store canonical entities directly in JSON.
  Decision: reject.
  Reason: generated data is harder for humans to review and would mix source
  truth with projections.
- Option: use Harness GraphIR for entity data.
  Decision: reject.
  Reason: GraphIR models repository declarations and references; entity graph
  needs claims, questions, timelines, locations, and durable domain identity.

## Change History

- 2026-08-19: Moved the feature to Wiki, added generated SQLite/page-owned edge
  state, and replaced whole-repository compilation with sync plus rebuild
  recovery.
- 2026-08-02: Reduced the index envelope to schema/fingerprint/entities and
  replaced Graph schema v3 with schema v4 lean nodes plus compiler-owned diagnostics.
- 2026-08-02: Replaced the schema-v3 full-record index with a schema-v4 bounded
  lookup catalogue; canonical Markdown now remains the only full-text owner.
- 2026-07-31: Added the registry-backed feature owner for existing entity
  Markdown and graph behavior.
