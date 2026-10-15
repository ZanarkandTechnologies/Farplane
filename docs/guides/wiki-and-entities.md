---
title: "Wiki And Entities"
status: active
owner: harness
created_at: 2026-07-12
updated_at: 2026-10-15
framework_template_version: "3.0.0"
tags:
  - farplane
  - wiki
  - entities
  - notes
refs:
  - skills/manage-wiki/SKILL.md
  - skills/manage-wiki/references/wiki-contract.md
  - skills/manage-wiki/references/notation.md
  - bin/core/farplane_entities.py
  - bin/core/farplane_wiki.py
  - docs/guides/graphs.md
  - runtimes/AGENTS.md
  - install.sh
---

# Wiki And Entities

How a Farplane project remembers people, companies, and what it learned about
them, and where research one thread found waits for the next. The Wiki is a
folder of Markdown articles; everything else about it is generated.

```text
wiki_sync(.farplane/entities/*.md, changed_paths?)
  -> .farplane/wiki/wiki.sqlite
   + .farplane/entities/index.json
   + .farplane/entities/graph.json
   + .farplane/entities/crm.json
   + .farplane/views/<view-id>.json
   + diagnostics
```

The articles under `.farplane/entities/` are the single source of truth.
SQLite, the lookup index, graph, CRM, and typed views are disposable
projections; none owns entity data. Exact notation and command behavior live
with the skill that writes the Wiki: the
[storage contract](../../skills/manage-wiki/references/wiki-contract.md) and
the [authoring notation](../../skills/manage-wiki/references/notation.md).

## What Goes Where

| Knowledge | Owner |
| --- | --- |
| Research one thread found that another thread would reuse | [Thread notes](#thread-notes) in `~/.farplane/memory/` |
| Ingested data about people, companies, and other entities | the Wiki, through `manage-wiki` |
| Task state, decisions, and proof for one piece of work | the GitHub issue |
| Project invariants worth retrieving outside their owner | `docs/MEMORY.md` |
| Who the operator is and what they focus on | `~/.farplane/USER.md` |
| Dated research, call, prospect, and offer reports | the producing skill under `.farplane/<skill>/reports/`, linking pages through `entity_refs` |

The Wiki owns canonical articles, mention resolution, entity links,
originating-page edge claims, and the index, graph, CRM, and typed-view
projections. Harness graphs (skills, files, hooks) are a separate engine; see
[Graphs](graphs.md). A page keeps durable identity, useful context, claims,
questions, and funnel state, never a full report or guessed private facts.

## Pages

Each article sits directly at `.farplane/entities/<id>.md`; nested folders are
invalid and the filename stem must equal `id`. The folder may be a symlink
into the local-only memory repo, as in the operator workspace. Every page
needs `id`, `kind`, and `name`.

`kind` is a free, project-owned classification: the compiler scopes search and
consumers by it but does not restrict its values. By `manage-wiki` policy only
people and companies get pages. A creator or client is a person with that
entry in `roles`, with no separate creator or CRM record; problems, resources,
and goals are items on their owner's page (`<owner-id>#<item-id>`), never pages
of their own. A resource points at the problems it can solve with `helps`, and
the graph emits each item as a `problem` or `resource` node with an `owns` edge
from its owner and a directed `helps` edge. Generic frontmatter stays limited
to shared identity, reference, location, link, funnel, role, and item fields;
view-specific vocabulary goes in view sections and `.farplane/views.yaml`.

Only a resolved `[label](entity:<id>)` link in body prose creates a graph
association. It is kept with its containing sentence, nearest section, source
path, source URLs, and question references; it is undirected, never inferred,
and owned by the page whose sentence asserted it. Frontmatter `*_ref` fields
and `links` validate identity and support lookup but never create edges. A
stable `q-*` footnote groups a claim under the exact question that produced
it; questions are not graph nodes. Coordinates are optional and never
geocoded; unlocated entities stay searchable and appear as unlocated nodes.

Pages of one role share a shape, kept as templates and registered in
`config/template-registry.jsonl`. The
[creator page template](../../skills/manage-wiki/templates/creator-page.md) gives a creator a lede,
their top ideas under fixed `### ` themes in `## Claims` and `## Stories`
(capped at 100 claims and 50 stories, each line's citations counting how often
they repeat it); the YouTube bridge builds new creator pages from it.

## CRM

CRM has no separate Markdown. A non-empty `funnel` mapping, or `client` in
`roles`, puts the existing page in `crm.json`; removing it removes the CRM
entry while the page stays in the index and graph. The CRM projection only
selects: it never invents stages, opportunities, next actions, or consent, and
a researched person is not a qualified opportunity. Issues own bounded work
and may reference CRM entities; a relationship that is waiting stays on its
entity page, not as a long-lived issue.

## Views

`.farplane/views.yaml` is ignored, local, and authored. It holds named views:
each view's membership is an explicit entity-ID list, not a query, plus the
view's own relation, resource, metric, unit, status, and confidence
vocabulary. Views select canonical entities; they never copy entity data and
are not duplicated into the lookup index. Feed Scout's `entity_group_id` is a
source-owner bucket, not view membership.

```text
compile_view(entities, view_schema)
  -> typed_events + observations + resource_flows + relationship_bundles
```

- Entity pages own identity, prose, sources, a view's `Latest Status`, and the
  dated `Timeline` evidence under `## View: <name>`. A timeline row counts for
  its page and every linked entity, so it is never copied into the
  counterparty's page; event keys are generated, never authored.
- `graph.json` stays the generic paragraph-backed graph and never interprets
  view vocabulary.
- `.farplane/views/<view-id>.json` is a disposable typed projection for custom
  consumers; sync deletes it when its view leaves `views.yaml`.

The typed-view compiler covers its declared events, observations, resources,
weights, and transfers only. Other domain aggregations or UI behavior belong in
a view-specific adapter, not in core frontmatter.

A resource tag records an observation (supply, demand, capacity, a
requirement, or a claim), not an exchange. Only a tag whose view config
declares `transfer` (`source-to-linked` or `linked-to-source`), with exactly
one linked counterparty, emits a directed resource flow. So "NVIDIA invested
2 USD-billion in CoreWeave and needs 5 GW by 2030" means capital flowed from
NVIDIA to CoreWeave and the pair share a power dependency; no power transfer is
asserted. Aggregation keeps stated and normalized quantities, never sums
repeated snapshots as distinct transfers unless the sources say so, never
infers a transfer from prose, and lets status or confidence weights inform
scenarios without rewriting a recorded amount.

Consumers render a quiet bidirectional structural edge per entity pair and
layer each resource flow as a directional overlay. Requirements and
dependencies may appear in detail or filters but never animate as if they
moved. At low zoom, hide amount labels; reveal direction, amount, date, and
source on hover or selection.

## Storage, Search, And Sync

```bash
farplane wiki doctor --project-root <project>
farplane wiki search "Jane Smith" --project-root <project> --kind person
farplane wiki sync --project-root <project> --path .farplane/entities/jane-smith.md
farplane wiki rebuild --project-root <project>
```

- `doctor` checks the running Python's SQLite, FTS5, trigram tokenizer,
  database, schema version, and staleness, and writes nothing. Authoring stops
  before canonical writes when it fails.
- `search` returns ranked candidates: exact normalized ID, name, and alias
  matches first, then FTS5 lexical and trigram hits. Similar spelling is
  retrieval evidence, not identity; read the returned `path` before resolving a
  non-exact mention. Search refuses a missing, incompatible, or stale database.
- `sync` reparses changed articles and replaces their cached pages, labels,
  search rows, and claims by originating article. It never deletes every edge
  touching an edited entity, because other pages own those inbound claims.
- `rebuild` reparses everything and is the recovery and equivalence oracle:
  deleting the database and rebuilding must reproduce the same index, graph,
  CRM, and typed-view JSON as valid incremental sync.

Core stages SQLite and all JSON as one bundle and restores the prior bundle if
any promotion fails, so a failed run never leaves mixed state; every
projection carries the same `source_fingerprint`. The retired
`.farplane/entities/world.json` is removed on a successful run and never read.
Node IDs are project-qualified from `project_id` (or `project.id`) in
`farplane/manifest.json`, else the normalized name plus a root-path hash; set
an explicit ID before any cross-device sync. Cross-project entity resolution
and cloud sync are separate concerns.

`.farplane/` is otherwise generated state; entity Markdown and `views.yaml`
are its only two authored local owners, kept local because they may hold
personal research and relationship organization. Shared source coordinates
stay in tracked `farplane/bindings.yaml`; never add a generic
`.farplane/config.yaml`. Rebuild stale projections with `farplane wiki
rebuild`; never hand-edit SQL rows or generated JSON.

## Authoring Safely

`manage-wiki` owns every Wiki mutation. Source-producing skills hand it a
source reference and proposed page deltas instead of creating entities,
checking duplicates, or writing graph state themselves. The operator supplies
the source and intent, not filenames or IDs. Explicit save, add, update, or
publish to Wiki means `apply`; anything else, including research with no
Wiki-write direction, means `preview`, and conflicting directions never
silently write. Each retained mention gets one outcome: `link`,
`update_existing`, `create_new`, `ambiguity`, `skip_source_gap`, or `blocked`.
Only one unique exact match may auto-link; several plausible candidates are an
ambiguity. Normal Wiki authoring is not an `impl-plan` software change.

## Limits

- Search is project-local and lexical: Python's standard-library `sqlite3`
  with FTS5 and trigram. There is no vector retrieval, graph-database query
  language, or hosted store or sync.
- SQLite speeds retrieval and page-scoped updates; it is never a second
  writable entity store. The JSON index alone is not the search path, and
  `graph.json` is never edited directly.
- No inferred predicates, automatic ambiguous merges, or entities created
  without source evidence. Search quality never substitutes for missing source
  evidence.
- Before changing a projection schema or the semantic claim or edge key
  material, change the tests in `bin/tests/test_farplane_entities.py` and
  `bin/tests/test_farplane_wiki.py` first, then run `farplane wiki rebuild`.

## Thread Notes

Notes let one thread hand its research to another without redoing the work.
They are plain Markdown in the operator's one local-only memory repo, found
with `rg`, with no index, schema, database, or projection. The same repo holds
the operator's Wiki pages, so a processed call and the research it touches
share one history.

```text
~/.farplane/memory/                 local git repo, no remote, pre-push guard
  README.md
  2026-10-06-<slug>.md              note useful to any project
  projects/<project>/2026-10-06-<slug>.md
  entities/<id>.md                  Wiki pages (generated *.json ignored)
```

The workspace's `.farplane/entities` is a symlink to `entities/`, so
`manage-wiki` and `farplane wiki` keep using the workspace as project root.

- One file per finding, named `YYYY-MM-DD-<slug>.md`, with `title` and a
  one-line `summary` in front matter. Put the finding first, then sources.
- Project-scoped notes go under `projects/<project>/`, where `<project>` is the
  project folder name; everything else goes at the top level.
- Before researching, search the notes: `rg -il "<topic>" ~/.farplane/memory`.
- After writing or changing a note, commit it in the notes repo:
  `git -C ~/.farplane/memory add -A && git -C ~/.farplane/memory commit -m "note: <slug>"`.
  Wiki changes commit as `entity: <what>`; a processed call commits once as
  `call: <date> <title>`.
- Correct a wrong note in place; git keeps the old version.
- Never add a remote. Notes may hold client names, strategy, and private
  research, so they stay on this machine. The repo sits outside every pushable
  checkout, and its `pre-push` hook refuses any push.

`farplane install` creates the repo if it is missing and keeps the `pre-push`
guard in place on every install; it never touches existing notes. The folder
also opens as an Obsidian vault (`.obsidian/workspace*.json` is gitignored).
