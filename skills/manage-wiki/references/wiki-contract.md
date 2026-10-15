# Wiki Storage Contract

Read on every invocation for canonical storage, commands, search state and
projection behavior. Authoring notation lives in [notation.md](notation.md).

```text
wiki_sync(.farplane/entities/*.md, changed_paths?)
  -> .farplane/wiki/wiki.sqlite
   + .farplane/entities/{index,graph,crm}.json
   + .farplane/views/<view-id>.json
   + diagnostics
```

Markdown pages are the only source of truth. SQLite, the index, graph, CRM and
typed views are disposable projections; never hand-edit SQL rows or JSON to
repair drift.

## Commands

```bash
farplane wiki doctor --project-root <project>
farplane wiki search "Jane Smith" --project-root <project> --kind person
farplane wiki sync --project-root <project> --path .farplane/entities/jane-smith.md
farplane wiki rebuild --project-root <project>
```

- `doctor` checks the running Python's SQLite, FTS5, trigram tokenizer,
  database path and presence, schema version and staleness, and writes
  nothing. Use it, not the system `sqlite3` binary.
- `rebuild`/`sync` take `--no-write` and `--json`; `doctor`/`search` take
  `--json`. Any invalid source, unresolved link, bad view config or projection
  failure exits non-zero before generated state changes; SQLite and all JSON
  are promoted as one bundle and restored on failure. Read issues from the
  result's top-level `diagnostics`, never from projection files.

## Search

`search` takes optional `--kind`, `--role creator|client` and `--limit`, and
returns candidate `id`, `name`, `kind`, `path`, optional `location`,
`matched_label`, `match_types` and `similarity`. Exact id/name/alias matches
rank first after NFKD + casefold keeping only alphanumerics (`Open AI` =
`OpenAI`). FTS5/trigram hits are candidates only. Item text (problems,
resources) is searched through its owner's page. Search refuses a missing,
incompatible or stale database and names `rebuild` or `sync`.

## Sync And Rebuild

`sync` without `--path` applies every change; with `--path` only those pages,
and search stays stale until the rest sync. Sync replaces cached pages, labels,
FTS rows and claims by originating page; it never deletes every edge touching
an edited entity, because other pages own those inbound claims. A missing or
incompatible database makes sync rebuild. Deleting the database and running
`rebuild` must reproduce the same JSON as incremental sync.

## Projections

- `index.json` v5 = `{schema_version, source_fingerprint, entities[]}`; each
  entry holds only `id`, `kind`, `name`, `aliases`, `location`, `*_ref`
  fields, `question_refs` and `path`. No bodies, raw frontmatter or funnel.
  Resolve through search, then read `path`.
- `graph.json` v4 holds project-qualified nodes, paragraph-backed associations,
  claims and questions. Each problem/resource is a node with
  `owner_entity_id`, an `owns` edge from its owner and a directed `helps` edge
  carrying `impact` and `status`.
- `crm.json` v4 holds only identity, path and funnel records.
- All projections share `source_fingerprint`, so mixed fingerprints mean stale.
  Old projections: run `rebuild`; there are no compatibility fields.

## Named Views

`.farplane/views.yaml` (ignored, local) selects canonical entities into named
views; it never copies entity data and is not in `index.json`. Feed Scout
`entity_group_id` is a source-owner bucket, not view membership.

## Typed Views

`graph.json` stays the generic paragraph-backed graph and never interprets view
vocabulary. `.farplane/views/<view-id>.json` is a disposable typed projection;
sync deletes it when its view id leaves `views.yaml`.

Typed view v4 holds per-entity `view_status`, typed events, observations, and
`resource_flows` at top level, per relationship and per evidence row.
Relationships are one undirected bundle per pair (`directed: false`,
newest-first evidence); flow direction never changes relationship identity. A
flow keeps event key, date, resource, from/to, stated and normalized quantity,
state, confidence, sources and path.

- Keep stated and normalized quantities; weights feed scenarios but never
  rewrite a recorded amount.
- Do not sum repeated snapshots unless sources describe distinct transfers.
- Never infer a transfer from prose, supply/demand or partnership.
- Invalid units, directions, ambiguous counterparties and unresolved entities
  are compile issues, not guesses.

## Project Identity

Node ids are project-qualified: `project_id` (or `project.id`) from
`farplane/manifest.json`, else the normalized name plus a 10-char hash of the
root path. Set an explicit id before any cross-device sync.

## Report Boundary

Dated research, call and offer reports stay with their skill under
`.farplane/<skill>/reports/` and link pages through `entity_refs`. A page keeps
durable identity, context, claims, questions and funnel state, never a full
report or guessed private facts.
