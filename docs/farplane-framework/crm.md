---
kind: farplane-framework-crm-standard
status: active
created_at: 2026-07-12
updated_at: 2026-07-20
framework_template_version: "2.0.7"
---

# Farplane CRM

Farplane CRM is local relationship memory, not a sales-pipeline runtime.
Markdown entity files are canonical because people and organizations need both
structured identity and useful narrative context. Core compiles those files for
machine consumers.

```text
crm_compile(.farplane/crm/entities/**/*.md)
  -> .farplane/crm/entities.json + .farplane/crm/world.json
   + validation_issues
```

## Layout

```text
.farplane/crm/
  README.md
  entities/
    people/
    companies/
    opportunities/
  entities.json
  world.json
```

The type folders are organizational, not a closed taxonomy. Every entity file
requires `id`, `kind`, and `name`. IDs use lowercase letters, digits, hyphens,
or underscores. Structured relationship references live in frontmatter; durable
notes and personalized context live in the body.

```markdown
---
id: jane-smith
kind: person
name: Jane Smith
aliases:
  - Jane A. Smith
company_ref: acme
status: researching
location: Kuala Lumpur, Malaysia
latitude: 3.139
longitude: 101.6869
links:
  - https://example.com/jane
---

# Jane Smith

## Relationship context

Prospective design partner. Prefers concrete demonstrations.

## Open questions

- Does commissioning evidence belong to her team?
```

## Compilation

Run:

```text
farplane crm compile --project-root <project>
```

Core recursively scans entity Markdown, preserves frontmatter and body in each
compiled record, builds `by_id`, and deterministically reports malformed files, missing required
fields, invalid IDs, duplicate IDs, and unresolved CRM references. The command
returns non-zero when issues exist. Both `entities.json` and `world.json` are
generated from the same source records and replaced atomically; neither file
may be hand-edited.

Supported reference fields are `company_ref`, `organization_ref`,
`entity_refs`, `person_refs`, `opportunity_refs`, and `relationship_refs`.
Source/report references are not treated as CRM entity references.

## World Metadata

Use one optional flat location label for filtering and display:

```yaml
location: Penang, Malaysia
latitude: 5.4141
longitude: 100.3288
```

`latitude` and `longitude` are optional, but when used they must be numeric,
must appear together, and must fall within `-90..90` and `-180..180`.
Compilation never geocodes a location. An entity with `location` but no
coordinates remains in the searchable world projection and is simply not
plotted. Optional `aliases` is a list of known names used during entity lookup.

## Explicit Associations

Write an association as a stable CRM link inside the factual Markdown sentence:

```markdown
## Relationships

- Supplies aluminum housings to [Acme Motors](crm:acme-motors) from its Penang facility.
```

Only explicit `[label](crm:<entity-id>)` body links become world associations.
The target ID must resolve, and self-links are invalid. Core preserves the
normalized containing sentence text, original Markdown context, entity path,
and nearest section. It ignores link-like text inside inline or fenced code.
It emits an undirected `association`; it does not infer a predicate,
inverse relationship, or separate canonical edge record.

## Question Provenance

Use a stable `q-*` footnote when a durable claim should remain grouped by the
question that produced it. Put the reference on the factual paragraph or
relationship bullet and define the exact question under `## Question index` at
the bottom of every entity file that uses it:

```markdown
## Relationships

- Supplies aluminum housings to [Acme Motors](crm:acme-motors). [^q-20260720-01]

## Question index

[^q-20260720-01]: Which suppliers could support Acme's Malaysian expansion? | session=019f7e88-6864-7f23-8dbb-5e058009e911
```

The question text is required. `session=<id>` is optional local provenance and
never identifies the question; do not store turn IDs. Reuse one question ID
for follow-ups serving the same inquiry, and create a new ID when the underlying
question changes. Repeated definitions of one ID must use exactly the same
question text across entity files. Session provenance may be absent or differ;
the compiler aggregates it into `session_ids` without changing identity.

The compiler emits schema-version-2 `questions` and `claims` collections. Nodes
aggregate `question_refs`; explicit associations carry the references from
their containing claim block; question records list related entity, claim, and
edge keys for FAQ and question-filtered graph views. Questions do not become
default graph nodes. Unresolved references, empty definitions, and conflicting
definitions are validation errors. Question markers and optional session
metadata are stripped before semantic claim and edge keys are computed, so
provenance enrichment does not replace an otherwise unchanged relationship.

`world.json` contains all included entities as nodes, including unlocated
nodes, plus validated explicit associations. Every node and edge has a stable
project-qualified key. Project identity comes from `project_id` or
`project.id` in `farplane/manifest.json` when present. Local projects without
one receive a normalized name plus local-root hash so same-named folders do not
collide on one machine. Set an explicit manifest ID before cross-device/cloud
sync because the fallback intentionally changes across clones. Both generated
files carry the same deterministic `source_fingerprint`; consumers can flag a
stale mixed projection when those fingerprints diverge. Cross-project entity
resolution and cloud sync are separate concerns.

## Report Boundary

Dated research, evidence, candidate packets, calls, and offer reports stay with
their producing skill under `.farplane/<skill>/reports/`. They link CRM entities
through `entity_refs`. Entity Markdown stores durable relationship context,
personalization cues, known preferences, current status, open questions, and
follow-up state; it should not duplicate full reports or guessed private facts.
