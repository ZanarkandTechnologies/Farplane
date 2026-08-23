---
title: "Farplane Entity View Projection Standard"
status: active
owner: farplane-framework
created_at: 2026-07-23
updated_at: 2026-08-02
framework_template_version: "2.0.14"
---

# Entity View Projection Standard

This standard lets a project interpret canonical entity Markdown with a local
domain vocabulary while preserving one generic Wiki graph.

```text
compile_view(entities, view_schema)
  -> typed_events + observations + resource_flows + relationship_bundles
```

## Ownership Boundary

- `.farplane/entities/<id>.md` owns identity, prose, sources, latest status,
  and dated timeline evidence.
- `.farplane/views.yaml` owns local entity membership and the view's relation,
  metric, resource, unit, problem, status, and confidence vocabulary.
- `.farplane/entities/graph.json` remains the generic paragraph-backed graph.
- `.farplane/views/<view-id>.json` is a disposable typed projection for custom
  consumers. It never becomes a second source of truth; compilation removes
  generated view JSON whose view ID is no longer configured.

Generic entity frontmatter stays limited to shared identity fields. View tags
live inline in Markdown so each project can define its own vocabulary without
changing the entity schema.

## Authored Contract

```markdown
## View: AI Bubble

### Latest Status

_As of 2026-07-23_

[role:accelerator-supplier] NVIDIA supplies accelerators and finances demand.

### Timeline

- 2026-01-26 [relation:investment] [status:announced]
  [capital-supply:2 USD-billion] [power-demand:5 GW by 2030]
  NVIDIA invested in [CoreWeave](entity:coreweave).
  Source: [filing](https://example.com/filing).
```

Authors do not add event IDs or duplicate the paragraph in the counterparty's
file. Compilation fingerprints the evidence and associates it with every
linked entity.

## Observation And Transfer Semantics

Every valid resource tag emits an observation for the configured entity. An
observation can describe supply, demand, capacity, a requirement, or a claim;
it does not prove an exchange.

Only an explicit `transfer` mapping emits a directed resource flow:

```yaml
resource_tags:
  capital-supply:
    resource: capital
    direction: supply
    entity: source
    transfer: source-to-linked
  power-demand:
    resource: electrical-capacity
    direction: demand
    entity: source
```

`transfer` accepts `source-to-linked` or `linked-to-source` and requires one
linked counterparty. The resulting flow retains the event key, date, resource,
from/to entity IDs, stated and normalized quantities, state, confidence,
evidence, source URLs, and source path.

The example therefore means:

- capital flowed from NVIDIA to CoreWeave;
- NVIDIA/CoreWeave have a relationship involving a 5 GW power dependency;
- no power transfer is asserted.

## Projection Contract

Typed view schema v4 preserves the schema-v3 event, observation, relationship,
flow, and summary semantics while inheriting lean graph nodes. Selected
entities contain bounded graph identity/routing fields plus `view_status`; raw
frontmatter and generic metadata remain in canonical Markdown.

Typed view schema v4 exposes `resource_flows` at three levels:

1. top-level flow ledger for filtering and resource views;
2. relationship-level flows for pair inspection and graph rendering;
3. evidence-level flows tying each transfer to one dated source paragraph.

Relationships remain one unordered bundle per entity pair with `directed:
false`, newest-first evidence, source URLs, relation types, resource IDs, and
latest context. Flow direction never changes relationship identity.

Consumers should render a quiet bidirectional structural edge and layer each
resource flow as a colored directional overlay. Requirements and dependencies
may appear in detail or filters but must not animate as if they moved. At low
zoom, hide amount labels; reveal direction, amount, date, and source on hover or
selection.

## Aggregation Rules

- Keep stated quantities and normalized quantities; never discard source units.
- Status/confidence weights may support scenario summaries but do not rewrite
  the recorded transfer amount.
- Do not sum repeated timeline snapshots as independent flow unless the source
  paragraphs describe distinct transfers.
- Do not infer transfers from prose, `supply`, `demand`, partnership, or a
  resource-bearing relationship alone.
- Invalid units, directions, transfer values, ambiguous counterparties, and
  unresolved entities are compile issues rather than guessed data.

## 2.0.14 Migration

1. Recompile typed views with Farplane 2.0.14 to replace schema v3 with schema
   v4 lean entity nodes.
2. Read arbitrary entity frontmatter through the selected entity's `path`.
3. Preserve existing event, observation, relationship, flow, and summary consumers.

## 2.0.10 Migration

1. Keep canonical Markdown and local view config; remove authored event records
   or project-specific generic frontmatter introduced for custom rendering.
2. Mark only proven exchange tags with `transfer`.
3. Compile with Farplane 2.0.10.
4. Update typed view consumers to schema v3 and read
   `counts.resource_flows`.
5. Preserve generic graph consumers unchanged.
