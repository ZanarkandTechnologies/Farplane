# CRM

Ignored local customer and relationship state for this project.

Use this directory for Markdown-owned relationship entities. Skill-produced reports live under
their producing skill, such as `.farplane/customer-research/reports/`, and link
back here with stable `entity_refs`.

## Layout

```text
.farplane/crm/
  README.md
  entities/
    people/
    companies/
    opportunities/
  entities.json  # generated
  world.json     # generated map/graph projection
```

Each file under `entities/**/*.md` is canonical relationship state. Use stable,
lowercase IDs and keep structured identity/linking fields in frontmatter while
putting personalized notes in the Markdown body:

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
```

Required frontmatter is `id`, `kind`, and `name`. Supported CRM reference fields
include `company_ref`, `organization_ref`, `entity_refs`, `person_refs`,
`opportunity_refs`, and `relationship_refs`; every referenced ID must resolve.

Use optional `aliases` for known names and one flat `location` for display and
filtering. Optional `latitude` and `longitude` must be supplied together,
numeric, and in range. The compiler does not geocode; entities without
coordinates remain searchable but are not plotted.

Encode an explicit association inside its factual sentence:

```markdown
## Relationships

- Supplies aluminum housings to [Acme Motors](crm:acme-motors) from its Penang facility.
```

Only resolved `[label](crm:<entity-id>)` body links generate associations.
Self-links are invalid. The generated edge is undirected and retains normalized
sentence text, original Markdown context, source path, and section; code
spans/fences are ignored and no predicate or inverse relationship is inferred.

When a claim answers a durable question, add a stable question footnote to the
claim block and define it at the bottom of every entity file that uses it:

```markdown
- Supplies aluminum housings to [Acme Motors](crm:acme-motors). [^q-20260720-01]

## Question index

[^q-20260720-01]: Which suppliers could support Acme's Malaysian expansion? | session=optional-local-session-id
```

Question text is required. The session suffix is optional provenance, never
question identity; do not store turn IDs. Matching `q-*` definitions must use
the same exact question text across files, while session provenance may be
absent or differ. Compilation aggregates sessions, rejects unresolved or
question-text-conflicting references, and emits question-aware claims, nodes,
and edges without adding question nodes to the default graph.

Run `farplane crm compile --project-root <project>` after edits. The generated
`entities.json` contains structured frontmatter, Markdown bodies, paths, a
`by_id` lookup, question-backed claims, and validation issues. `world.json`
contains project-qualified nodes, questions, claims, and explicit
sentence-backed associations for map and graph consumers.
Both are generated from the same source records and must not be hand-edited.
Set `project.id` in `farplane/manifest.json` before cross-device/cloud sync;
the collision-safe local fallback is path-derived and clone-local.

## Report Links

Keep frontmatter minimal:

```yaml
---
skill: "customer-research"
entity_refs:
  - "jane-smith"
  - "acme"
name: "Person Name"
links:
  - "https://example.com/profile"
industry: "Industry or field, when useful for search."
relevance: "Why this person is relevant to the call or project."
created_at: "YYYY-MM-DD"
---
```

`entity_refs` values must resolve to compiled entity IDs. Do not hand-maintain
report arrays on CRM entities; discover backlinks by scanning
`.farplane/*/reports/**/*.md`. CRM has no report index. Any future derived
cross-skill report index must live outside CRM and be introduced through a
ticketed reporting change.

Keep dated research evidence in skill-owned reports. Put durable relationship
context, personalization cues, known preferences, open questions, and current
follow-up state in the entity body without copying entire reports into CRM.
