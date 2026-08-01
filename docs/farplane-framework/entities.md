---
kind: farplane-framework-entity-memory-standard
status: active
created_at: 2026-07-12
updated_at: 2026-08-02
framework_template_version: "2.0.14"
---

# Farplane Entity Memory

Entity Markdown is the single source of truth for the people, companies,
organizations, sources, datasets, topics, indicators, and other durable things
a project tracks. The lookup index, World, CRM, and typed views are generated;
none owns full entity data.

```text
entities_compile(.farplane/entities/*.md)
  -> .farplane/entities/index.json
   + .farplane/entities/world.json
   + .farplane/entities/crm.json
   + validation_issues
```

For a write-ready grammar and complete example, see
[Entity Markdown Authoring](entity-markdown-authoring.md).

Optional local view membership lives separately at `.farplane/views.yaml` and
is compiled into World and typed-view projections. Views select canonical
entities; they never copy or own entity data, and they are not duplicated into
the lookup index.

## Flat Layout

```text
.farplane/entities/
  jane-smith.md
  acme.md
  nasdaq-composite.md
  index.json  # generated entity/search index
  world.json  # generated graph projection
  crm.json    # generated funnel projection
```

Entity Markdown must be directly inside `.farplane/entities/`; nested type
folders are invalid. The filename stem must equal `id`, so an entity is always
found at `.farplane/entities/<id>.md`. The `kind` frontmatter field owns
classification. Every entity requires `id`, `kind`, and `name`. IDs use
lowercase letters, digits, hyphens, or underscores.

```markdown
---
id: jane-smith
kind: person
name: Jane Smith
aliases:
  - Jane A. Smith
company_ref: acme
location: Kuala Lumpur, Malaysia
latitude: 3.139
longitude: 101.6869
links:
  - https://example.com/jane
funnel:
  pipeline: agency-sales
  stage: researching
  status: active
  next_action: Prepare a concrete demonstration
---

# Jane Smith

## Relationship context

Prospective design partner. Prefers concrete demonstrations.
```

`funnel` is optional. Adding a non-empty funnel mapping promotes the existing
entity into the generated CRM view; it never creates a second CRM record.
Entities without funnel state remain in the entity index and World view but do
not appear in `crm.json`.

## Named Views

Keep multiple private project-local slices in one ignored config:

```yaml
views:
  ai-bubble:
    name: AI Bubble
    entity_ids:
      - nvidia
      - openai
      - coreweave
```

Each view ID and entity ID uses the canonical entity ID syntax. Names are
required, membership must be non-empty and unique, and every member must
resolve to a flat entity Markdown file. Duplicate YAML keys are invalid rather
than silently using the last value. Config absence means no named views; an
empty scaffold uses `views: {}`.

Core preserves declared entity order, sorts views by ID, and embeds bounded
membership into `world.json` while writing each typed view under
`.farplane/views/`. Feed Scout `entity_group_id` remains a source-owner
bucket and does not own view membership.

## Compilation

Run:

```text
farplane entities compile --project-root <project>
```

Core scans only flat entity Markdown and keeps full frontmatter and body in a
private in-memory registry while it builds every projection. It deterministically
reports malformed files, nested paths, missing required fields, invalid or
duplicate IDs, unresolved references, malformed view config or membership,
malformed funnel state, coordinates, entity links, and question provenance.
The command returns non-zero when issues exist. `--json` returns compiler-owned
`diagnostics` containing issues, source counts, and the typed-view issue count;
those diagnostics are not copied into every projection. Generated JSON files
are atomically replaced and must not be hand-edited.

Supported entity reference fields are `company_ref`, `organization_ref`,
`entity_refs`, `person_refs`, `opportunity_refs`, and `relationship_refs`.

## Lookup Index Contract

`index.json` schema v5 is a bounded lookup catalogue. Its envelope contains
only `schema_version`, `source_fingerprint`, and `entities`. Each entity entry
contains only fields needed to resolve, filter, or route to a canonical entity:

```json
{
  "id": "jane-smith",
  "kind": "person",
  "name": "Jane Smith",
  "aliases": ["Jane A. Smith"],
  "location": "Kuala Lumpur, Malaysia",
  "company_ref": "acme",
  "question_refs": ["q-20260802-01"],
  "path": ".farplane/entities/jane-smith.md"
}
```

The index does not serialize Markdown bodies, raw frontmatter, funnel state,
view definitions, claims, timelines, diagnostics, counts, or a duplicate
`by_id` copy. Search the
bounded fields, then read `path` when full prose or unindexed frontmatter is
needed. World owns graph associations and evidence projections; CRM owns funnel
selection; `.farplane/views.yaml` and typed-view JSON own specialized view
membership and interpretation.

## World Metadata

Use an optional flat location label for filtering and display:

```yaml
location: Penang, Malaysia
latitude: 5.4141
longitude: 100.3288
```

Coordinates are optional, but when used they must be numeric, paired, and
within `-90..90` latitude and `-180..180` longitude. Compilation never
geocodes. Unlocated entities remain searchable and appear as unlocated World
nodes. Optional `aliases` lists names used during entity lookup.

## Paragraph-Backed Entity Links

Link another entity inside the factual Markdown sentence or paragraph:

```markdown
## Relationships

- Supplies aluminum housings to [Acme Motors](entity:acme) from its Penang facility.
```

Only resolved `[label](entity:<entity-id>)` body links become World
associations. Self-links are invalid. Core preserves the normalized containing
sentence, display context, source entity path, nearest section, and question
references from the containing paragraph. Inline and fenced code are ignored.
Associations are undirected; the compiler does not infer predicates, inverse
relationships, or separate canonical edge records.

## View Status, Timelines, And Observations

Keep view-specific language in a named section of the entity body rather than
expanding generic frontmatter. `Latest Status` is freeform node context. Dated
bullets under its sibling `Timeline` section are evidence records:

```markdown
## View: AI Bubble

### Latest Status

_As of 2026-07-22_

[role:accelerator-supplier] NVIDIA is the central accelerator supplier in the
tracked network, but its announced projects still depend on delivered power.

### Timeline

- 2026-03-11 [relation:investment] [status:announced] [confidence:primary]
  [capital-supply:2 USD-billion] NVIDIA reported a stake in
  [Nebius](entity:nebius).
  Source: [SEC filing](https://example.com).
```

Core keeps these bullets in its in-memory compilation registry and emits them
to `world.json` plus matching typed views. A timeline row belongs to its source
entity and every linked entity, so consumers can derive both companies'
histories without copying the paragraph. Bullets outside a `Timeline` heading
remain ordinary prose. Event keys are deterministic compiler fingerprints of
the date, entities, sources, prose, and tags; authors do not maintain event IDs.

View schemas live in ignored project-local `.farplane/views.yaml`. A view owns
its relation vocabulary, resource and metric tag mappings, units and
conversions, tracked problems, and status or confidence weights. For example,
`capital-supply` can map to resource `capital`, direction `supply`, and the
source entity. This keeps entity Markdown readable while allowing different
views to interpret different tag languages.

A resource observation is not automatically a transfer. Add `transfer` only
when the tag itself asserts a resource moved between the timeline source and
its single linked counterparty:

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

Valid transfer directions are `source-to-linked` and `linked-to-source`.
Transfer tags require exactly one linked entity. Untagged observations remain
requirements, capacity claims, or dependencies and must not be rendered as
money, energy, compute, or material changing hands.

`farplane entities compile` writes `.farplane/views/<view-id>.json` with:

- view status attached to each selected entity;
- typed events and resource observations;
- explicit directed `resource_flows` at projection, relationship, and evidence
  levels without changing the relationship's undirected identity;
- one undirected relationship bundle per entity pair;
- latest evidence plus a date-sorted evidence timeline on every relationship.

Generic `world.json` keeps all paragraph-backed associations and inline tags
without interpreting the view vocabulary. A fenced code block whose info string
is `farplane` is a compile issue; migrate it to inline tags under the relevant
view section.

The typed view projection is schema version 4. It inherits bounded identity,
location, routing, and provenance fields from World nodes rather than copying
raw frontmatter or generic metadata. See
[Entity View Projection Standard](entity-view-projection-standard.md) for the
authored vocabulary, compiler output, consumer behavior, and migration rules.

## Question and Source Provenance

Use a stable `q-*` footnote when a durable claim should remain grouped by the
question that produced it. Put the reference on its factual paragraph or
relationship bullet and define the exact question in the same entity file:

```markdown
## Relationships

- Supplies aluminum housings to [Acme Motors](entity:acme). [^q-20260720-01]
  Source: [Research call](../customer-research/reports/2026-07-13-call.md).

## Question index

[^q-20260720-01]: Which suppliers could support Acme's Malaysian expansion? | session=019f7e88-6864-7f23-8dbb-5e058009e911
```

The question text is required. `session=<id>` is optional local provenance and
never identifies the question; do not store turn IDs. Reuse an ID only for
follow-ups serving the same exact inquiry. Repeated definitions must use the
same question text across entity files; session provenance may differ and is
aggregated into `session_ids`.

World schema v4 emits `questions` and paragraph-backed `claims`. Nodes contain
only project-qualified identity, routing, location, aliases, coordinates, and
question references; arbitrary frontmatter remains in canonical Markdown.
Nodes aggregate
`question_refs`; explicit associations carry references from their containing
claim block; question records link related entity, claim, and edge keys for FAQ
and question-filtered graph views. Questions do not become default graph nodes.
Question/session markers, storage paths, and entity-link URI spelling are not
part of semantic claim or edge key material, so provenance enrichment and file
moves do not replace an otherwise unchanged relationship.

`index.json` schema v5 includes bounded lookup records. `world.json` schema v4
includes all valid entities as project-qualified nodes plus explicit
associations, claims, and questions. `crm.json` schema v4 includes only lean
identity/path/funnel records and does not copy raw frontmatter, `by_id`, view
definitions, diagnostics, or derived counts. All projections carry the same deterministic
`source_fingerprint`; consumers can detect mixed stale projections when the
fingerprints diverge.

Project identity comes from `project_id` or `project.id` in
`farplane/manifest.json`. Projects without one receive a normalized name plus
local-root hash. Set an explicit manifest ID before cross-device sync.
Cross-project entity resolution and cloud sync remain separate concerns.

## Report Boundary

Dated research, evidence, calls, and offer reports remain with their producing
skill under `.farplane/<skill>/reports/`. They link canonical entities through
`entity_refs`. Entity Markdown stores durable identity, useful context, claims,
questions, and optional funnel state; it should not duplicate full reports or
guessed private facts.
