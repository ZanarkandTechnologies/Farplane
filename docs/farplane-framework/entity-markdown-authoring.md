---
title: "Entity Markdown Authoring"
status: active
owner: farplane-framework
created_at: 2026-07-31
updated_at: 2026-08-02
tags:
  - farplane
  - entities
  - markdown
  - authoring
refs:
  - docs/farplane-framework/entities.md
  - docs/farplane-framework/entity-view-projection-standard.md
  - skills/ingest-world-data/SKILL.md
  - bin/core/farplane_entities.py
---

# Entity Markdown Authoring

Use Entity Markdown to record durable people, organizations, sources, topics,
datasets, indicators, opportunities, and other project entities in
human-readable files. The Markdown is canonical; generated JSON projections are
disposable compiler output.

```text
author_entity(.farplane/entities/<id>.md, .farplane/views.yaml?)
  -> farplane entities compile
  -> index.json + world.json + crm.json + views/<view-id>.json + command diagnostics
```

For projection semantics and ownership boundaries, see
[Entity Memory](entities.md). For typed resource observations and transfers,
see [Entity View Projection Standard](entity-view-projection-standard.md).

## Complete Example

```markdown
---
id: nebius
kind: company
name: Nebius
aliases:
  - Nebius Group
location: Amsterdam, Netherlands
links:
  - https://nebius.com
funnel:
  pipeline: partnerships
  stage: researched
  status: active
  next_action: Verify infrastructure partnership fit
---

# Nebius

## Durable context

Cloud infrastructure company tracked for AI compute and power relationships.

## Relationships

Nebius received an investment from [NVIDIA](entity:nvidia). [^q-20260731-01]
Source: [company announcement](https://example.com/announcement).

## View: AI Infrastructure

### Latest Status

_As of 2026-07-31_

[role:compute-provider] Expanding AI infrastructure capacity while depending on
accelerator and power availability.

### Timeline

- 2026-03-11 [relation:investment] [status:announced] [confidence:primary]
  [capital-demand:2 USD-billion] Nebius announced an investment relationship
  with [NVIDIA](entity:nvidia).
  Source: [filing](https://example.com/filing).

## Question index

[^q-20260731-01]: Which companies connect AI capital, compute, and power supply?
```

The example can contribute:

- one canonical entity record;
- one paragraph-backed World association;
- one question-backed claim;
- one view-specific latest status;
- one dated typed-view event;
- one resource observation when `capital-demand` is declared in the view;
- one CRM entry because `funnel` is a non-empty mapping.

## File And Identity Rules

Store each entity directly under `.farplane/entities/`:

```text
.farplane/entities/
  nebius.md
  nvidia.md
```

Required frontmatter:

| Field | Contract |
| --- | --- |
| `id` | Lowercase letters, digits, hyphens, or underscores; must match the filename stem |
| `kind` | Project-owned classification such as `person`, `company`, `source`, or `topic` |
| `name` | Human-readable canonical name |

Common optional frontmatter:

| Field | Meaning |
| --- | --- |
| `aliases` | Alternate names used during lookup |
| `company_ref`, `organization_ref` | One canonical entity reference |
| `entity_refs`, `person_refs`, `opportunity_refs`, `relationship_refs` | Canonical entity reference lists |
| `location` | Freeform display and filter label |
| `latitude`, `longitude` | Optional paired numeric coordinates; compilation never geocodes |
| `links` | External source or profile URLs |
| `funnel` | Non-empty mapping that includes the entity in `crm.json` |

Keep view-specific roles, metrics, statuses, and relation vocabulary out of
generic frontmatter. Put them in named view sections and `.farplane/views.yaml`.

## Entity Links And Associations

Use a Markdown link with the `entity:` scheme:

```markdown
Acme buys castings from [Penang Castings](entity:penang-castings).
```

The compiler creates an undirected World association from the exact containing
sentence. It preserves the source entity, path, nearest section, display
context, source URLs, and question references.

Rules:

- the target ID must resolve to another canonical entity;
- self-links are invalid;
- links inside inline or fenced code are ignored;
- ordinary HTTP links remain evidence URLs rather than entity edges;
- prose may state direction, but the generic association identity stays
  undirected;
- do not duplicate the sentence in the target entity merely to create a reverse
  edge.

## Questions And Claims

Attach a stable `q-*` footnote to a factual paragraph or relationship:

```markdown
Nebius received an investment from [NVIDIA](entity:nvidia). [^q-20260731-01]

[^q-20260731-01]: Which companies connect AI capital, compute, and power supply?
```

The footnote definition must exist in the same entity file and contain the exact
question. An optional local session marker may follow it:

```markdown
[^q-20260731-01]: Which companies connect AI capital, compute, and power supply? | session=<id>
```

The question ID—not the session—is identity. Reuse the ID only for claims
serving the same exact inquiry. Question definitions do not become default
World nodes; generated question records point to related entity, claim, and
association keys.

## Named View Sections

Use one view heading with `Latest Status` and `Timeline` children:

```markdown
## View: AI Infrastructure

### Latest Status

_As of 2026-07-31_

[role:compute-provider] Current sourced interpretation.

### Timeline

- 2026-03-11 [relation:investment] [status:announced]
  [confidence:primary] Dated sourced evidence.
```

`Latest Status` is current freeform context for that entity in the named view.
Only dated bullets under a `Timeline` heading become compiled events. Event keys
are deterministic; authors do not maintain IDs.

Inline tags use:

```text
[tag-name:value]
```

Common compiler-recognized tags:

| Tag | Meaning |
| --- | --- |
| `[view:<id-or-name>]` | Explicitly routes a timeline event to a view when the enclosing heading is insufficient |
| `[relation:<type>]` or `[type:<type>]` | Event or relationship type |
| `[status:<value>]` | View-defined lifecycle state |
| `[confidence:<value>]` | View-defined evidence confidence |
| `[signal:<value>]` | Freeform typed signal |
| `[resource-tag:<number> <unit> by <horizon>]` | View-defined resource observation |
| `[metric-tag:<number> <unit>]` | View-defined numeric metric |

The view schema in `.farplane/views.yaml` decides what project-specific resource
and metric tag names mean. Unknown configured statuses, confidence values,
resources, units, transfers, or entity selectors become compile issues.

## View Configuration

Membership and domain vocabulary live in one ignored local file:

```yaml
views:
  ai-infrastructure:
    name: AI Infrastructure
    entity_ids:
      - nebius
      - nvidia
    relations:
      investment:
        patterns:
          - invested in
    resources:
      capital:
        name: Capital
        measure: flow
        base_unit: USD-billion
        units:
          USD-billion: 1
          USD-million: 0.001
    resource_tags:
      capital-demand:
        resource: capital
        direction: demand
        entity: source
    status_weights:
      announced: 0.5
    confidence_weights:
      primary: 1
```

A resource observation does not assert that anything moved between entities.
Add `transfer: source-to-linked` or `transfer: linked-to-source` only when the
tag describes a real exchange and exactly one counterparty is linked.

## CRM Promotion

CRM does not use separate Markdown. Add a non-empty `funnel` mapping to the
canonical entity:

```yaml
funnel:
  pipeline: agency-sales
  stage: researched
  status: active
  next_action: Prepare a concrete demonstration
```

The compiler includes that entity in `crm.json`. Removing `funnel` removes it
from the CRM projection while preserving it in the index and World.

## Compile And Repair

Run:

```bash
farplane entities compile --project-root <project>
```

Use `--no-write` to validate without replacing projections and `--json` to
inspect the complete result. The command returns non-zero when entity or typed
view issues exist.

Do not edit:

```text
.farplane/entities/index.json
.farplane/entities/world.json
.farplane/entities/crm.json
.farplane/views/<view-id>.json
```

`index.json` schema v5 is deliberately lookup-only: it stores bounded identity,
alias, location, reference, question, and source-path fields. It does not copy
the Markdown body, raw frontmatter, compile diagnostics, or derived counts.
Resolve an entity in the index, then read its `path` for full context. World
schema v4 omits raw frontmatter and generic metadata; CRM schema v4 contains
only project identity plus entity identity/path/funnel records. Recompile older
projections directly; no compatibility fields or dual-read path are emitted.

With `--json`, read validation issues and source counts from the command's
top-level `diagnostics` object rather than from generated projection files.

Repair the entity Markdown or `.farplane/views.yaml`, then compile again. A
fenced code block whose info string is `farplane` is retired and becomes a
compile issue; use inline tags under a named view section.
