---
title: "Entity Markdown Authoring"
status: active
owner: farplane-framework
created_at: 2026-07-31
updated_at: 2026-08-19
tags:
  - farplane
  - entities
  - markdown
  - authoring
refs:
  - docs/systems/wiki.md
  - docs/features/FEAT-0079-wiki-resolution-and-incremental-projections.md
  - docs/farplane-framework/entities.md
  - docs/farplane-framework/entity-view-projection-standard.md
  - skills/manage-wiki/SKILL.md
  - bin/core/farplane_entities.py
  - bin/core/farplane_wiki.py
---

# Entity Markdown Authoring

Use Entity Markdown to record durable people, organizations, sources, topics,
datasets, indicators, opportunities, and other project entities as Wiki
articles. The Markdown is canonical; SQLite and JSON are disposable generated
projections.

```text
manage_wiki(source_ref, publication_intent = preview, page_deltas?, entity_scope?, project_root?)
  -> staged_pages + changed_pages + resolution_receipt + projection_refs
```

For projection semantics and ownership boundaries, see
[Wiki Storage And Projections](entities.md). For typed resource observations
and transfers, see
[Entity View Projection Standard](entity-view-projection-standard.md).

## Safe Authoring Workflow

Use `manage-wiki` for general Wiki mutation. Source-producing skills hand it a
source reference and proposed durable page deltas instead of independently
implementing entity creation, duplicate checks, or graph writes.

Bind `publication_intent` from the operator's words:

- `apply`: “save/add/update/write/publish this to Wiki” or “apply these Wiki
  changes.” This authorizes the complete valid Wiki changeset without a second
  page-by-page approval.
- `preview`: “preview/propose/draft/show the Wiki changes,” any explicit
  no-write instruction, or research/analysis with no Wiki-write direction.
- Conflicting instructions never silently write; return the conflict and the
  staged state needed to resolve it.

The operator supplies the source and intent, not filenames or entity IDs.
Manage Wiki chooses which existing articles to update, which sufficiently
sourced identities need new articles, and where entity links belong. This is a
normal authoring workflow, not an `impl-plan` software change.

1. Bind `project_root`, `source_ref`, `publication_intent`, and `entity_scope`,
   then run
   `farplane wiki doctor`; stop before canonical writes when required SQLite
   search support is unavailable.
2. Stage source-backed changes for the touched articles; do not publish a
   partially linked intermediate article.
3. Scan only staged articles for unlinked durable mentions in the active
   project `entity_scope`. Existing `entity:` links, code, citations, generic
   nouns, and incidental names are not unresolved entities.
4. Search exact IDs, names, and aliases first, then FTS5 lexical and trigram
   candidates. Read plausible candidate articles and compare kind, location,
   nearby entities, local prose, and source evidence.
5. Record one outcome per mention: `link`, `update_existing`, `create_new`,
   `ambiguity`, `skip_source_gap`, or `blocked`. Only one unique exact match may
   auto-link; multiple plausible candidates are always `ambiguity`.
6. Create sufficiently sourced missing articles inside the same changeset and
   insert `[label](entity:<id>)` links into the factual source prose.
7. Validate the complete Markdown and view-config changeset. In `preview`,
   return the staged diff and expected sync/projection receipt without writes.
8. In `apply`, commit only when references, links, notation, and resolution
   decisions are valid, then sync touched or deleted paths. Core replaces their
   cached page state and outgoing claims, then exports graph, CRM, the bounded
   index, and typed views.

Do not CRUD database rows or JSON edges. The authored sentence owns the claim;
the originating article is the unit of replacement.

## Notation Catalogue

This table is the complete compiler-significant Wiki article notation.
Ordinary Markdown remains ordinary prose unless listed here.

| Scope | Notation | Meaning and rules |
| --- | --- | --- |
| Frontmatter | `---` YAML `---` | Required at the start of every article; it must parse as a mapping |
| Identity | `id: acme` | Required; lowercase letters, digits, hyphens, or underscores; must equal the filename stem and cannot start with `.` or `-` |
| Classification | `kind: company` | Required project-owned entity type; it scopes search and consumers but does not create a folder |
| Display | `name: Acme` | Required canonical human-readable name |
| Lookup | `aliases: [Acme Corp]` | Optional alternate labels used by exact and hybrid resolution |
| Identity refs | `company_ref`, `organization_ref` | Optional single IDs; validated lookup relationships, not graph edges |
| Identity refs | `entity_refs`, `person_refs`, `opportunity_refs`, `relationship_refs` | Optional ID lists; validated lookup relationships, not graph edges |
| Place | `location: Penang, Malaysia` | Optional display/filter label; no geocoding |
| Coordinates | `latitude`, `longitude` | Optional paired finite numbers within latitude `-90..90` and longitude `-180..180` |
| External refs | `links: [https://…]` | Optional durable profile/source URLs; they do not create entity edges |
| CRM | `funnel: {…}` | Optional non-empty mapping; includes this same entity in generated `crm.json` |
| Title/sections | `# Name`, `## Context` | Human article structure and nearest-section provenance; headings do not create entities or edges |
| Entity relation | `[Acme](entity:acme)` | Resolved body link; creates a paragraph-backed outgoing claim and Wiki graph association from this article |
| Source evidence | `[filing](https://…)` | HTTP(S) link in the same claim/timeline context; captured as source evidence, not an entity edge |
| Question ref | `[^q-20260819-01]` | Attaches one or more stable question IDs to the containing factual block |
| Question definition | `[^q-…]: Exact question?` | Required same-file definition for a used question ID |
| Session provenance | `[^q-…]: Question? \| session=<id>` | Optional local session provenance; the `q-*` ID remains question identity |
| Named view | `## View: AI Infrastructure` | Starts view-specific article context; matches a configured view ID or name |
| Current view state | `### Latest Status` | Freeform current interpretation under a named view |
| Status date | `_As of 2026-08-19_` | Optional latest-status date; `As of:` is also accepted |
| Status tags | `[role:compute-provider]` | Any `[key:value]` tags inside Latest Status are preserved as typed current context |
| Timeline | `### Timeline` | Only dated list items below this heading become timeline evidence |
| Timeline row | `- 2026-08-19 …` | `-`, `*`, or `+` list item followed by an ISO date; event identity is generated from semantic content |
| View route | `[view:ai-infrastructure]` | Routes a timeline item when its heading is insufficient |
| Event type | `[relation:investment]` or `[type:investment]` | Explicit event/relationship type; otherwise configured patterns may classify it |
| State | `[status:announced]` | View-defined lifecycle value |
| Confidence | `[confidence:primary]` | View-defined evidence-confidence value |
| Signal | `[signal:capacity-risk]` | Freeform typed signal preserved on the event |
| Resource observation | `[<configured-resource-tag>:2 USD-billion by 2028]` | Numeric value, unit, and optional `by` or `@` horizon interpreted by `.farplane/views.yaml` |
| Metric | `[<configured-metric-tag>:300 MW]` | Numeric value and unit interpreted by `.farplane/views.yaml` |
| Literal examples | inline code or fenced code | Entity links, question refs, and timeline metadata inside code are ignored |
| Retired notation | triple-backtick fence whose info string is `farplane` | Invalid; use headings, entity links, question footnotes, and inline tags |

An entity link is the only authoring notation that creates a generic Wiki graph
edge. Frontmatter identity references are useful for lookup and validation but
do not silently create graph claims. Likewise, a resource observation becomes
a directed transfer only when its view configuration explicitly declares
`transfer` and the evidence links exactly one counterparty.

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
- one paragraph-backed Wiki graph association;
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

The compiler creates an undirected Wiki graph association from the exact containing
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
graph nodes; generated question records point to related entity, claim, and
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

Wiki includes that entity in `crm.json`. Removing `funnel` removes it
from the CRM projection while preserving it in the index and graph.

## Validate, Search, Publish, And Repair

Check runtime and initialize generated state:

```bash
farplane wiki doctor --project-root <project>
farplane wiki rebuild --project-root <project>
```

Search before creating or linking an entity:

```bash
farplane wiki search "Nebius Group" --project-root <project> --kind company
```

Sync validated changes by canonical path:

```bash
farplane wiki sync --project-root <project> \
  --path .farplane/entities/nebius.md \
  --path .farplane/entities/nvidia.md
```

`rebuild` and `sync` accept `--no-write` to validate without replacing
projections and `--json` for the complete result. `doctor` and `search` accept
`--json`. Commands return non-zero when runtime readiness, entity, view, or
projection issues exist; generated state is not partially replaced.

Omit `--path` to sync every detected source change. Supply one or more
`--path` flags for a bounded changeset; unrelated dirty articles then keep
search stale until they are synchronized. A missing or incompatible database
causes sync to perform a clean rebuild.

Do not edit:

```text
.farplane/wiki/wiki.sqlite
.farplane/entities/index.json
.farplane/entities/graph.json
.farplane/entities/crm.json
.farplane/views/<view-id>.json
```

`index.json` schema v5 is deliberately lookup-only: it stores bounded identity,
alias, location, reference, question, and source-path fields. It does not copy
the Markdown body, raw frontmatter, compile diagnostics, or derived counts.
Resolve candidates through `farplane wiki search`, then read `path` for full
context. Graph schema v4 omits raw frontmatter and generic metadata; CRM schema v4 contains
only project identity plus entity identity/path/funnel records. Recompile older
projections with `farplane wiki rebuild`; no compatibility fields or dual-read
path are emitted.

With `--json`, read validation issues and source counts from the command's
top-level `diagnostics` object rather than from generated projection files.

Repair the entity Markdown or `.farplane/views.yaml`, then sync or rebuild
again. A
fenced code block whose info string is `farplane` is retired and becomes a
compile issue; use inline tags under a named view section.
