---
kind: farplane-framework-entity-memory-standard
status: active
created_at: 2026-07-12
updated_at: 2026-07-22
framework_template_version: "2.0.9"
---

# Farplane Entity Memory

Entity Markdown is the single source of truth for the people, companies,
organizations, sources, datasets, topics, indicators, and other durable things
a project tracks. World and CRM are generated views; neither owns entity data.

```text
entities_compile(.farplane/entities/*.md)
  -> .farplane/entities/index.json
   + .farplane/entities/world.json
   + .farplane/entities/crm.json
   + validation_issues
```

Optional local view membership lives separately at `.farplane/views.yaml` and
is compiled into all three projections. Views select canonical entities; they
never copy or own entity data.

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

Core preserves declared entity order, sorts views by ID, embeds the normalized
`views` list into `index.json`, `world.json`, and `crm.json`, and includes it in
their shared `source_fingerprint`. Consumers apply membership as a read-time
filter. Feed Scout `entity_group_id` remains a source-owner bucket and does not
own view membership.

## Compilation

Run:

```text
farplane entities compile --project-root <project>
```

Core scans only flat entity Markdown, preserves frontmatter and body in the
compiled index, builds `by_id` and `views_by_id`, and deterministically reports malformed files,
nested paths, missing required fields, invalid or duplicate IDs, unresolved
references, malformed view config or membership, malformed funnel state,
coordinates, entity links, and question provenance. The command returns
non-zero when issues exist. All three JSON
files are atomically replaced generated views and must not be hand-edited.

Supported entity reference fields are `company_ref`, `organization_ref`,
`entity_refs`, `person_refs`, `opportunity_refs`, and `relationship_refs`.

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

Schema v3 emits `questions` and paragraph-backed `claims`. Nodes aggregate
`question_refs`; explicit associations carry references from their containing
claim block; question records link related entity, claim, and edge keys for FAQ
and question-filtered graph views. Questions do not become default graph nodes.
Question/session markers, storage paths, and entity-link URI spelling are not
part of semantic claim or edge key material, so provenance enrichment and file
moves do not replace an otherwise unchanged relationship.

`world.json` includes all valid entities as project-qualified nodes plus
explicit associations, claims, and questions. `crm.json` includes only
funnel-bearing entities. All projections carry the same deterministic
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
