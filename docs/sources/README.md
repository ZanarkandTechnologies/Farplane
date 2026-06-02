# Source Registry

Farplane's source registry is the structured system of record for external and
operator-provided materials that inspire harness changes.

Use it when a blog, spec, video, repo, paper, official doc, or private
operator-provided source needs a durable answer to:

- have we already seen this source?
- what is its canonical identity?
- where are the local scout or research artifacts?
- which `FEAT-*` records or tickets came from it?
- did we adopt, adapt, reject, defer, or treat it as a duplicate?

`docs/sources/registry.jsonl` tracks source provenance. `docs/features/registry.jsonl`
tracks durable harness techniques. A single source can inform many features, and
a single feature can synthesize many sources.

## Record Shape

Each line in `registry.jsonl` is one JSON object:

```json
{
  "id": "SRC-0001",
  "title": "Symphony Service Specification",
  "source_type": "spec",
  "origin": "operator-provided draft specification",
  "canonical_url": "user-provided:symphony-service-spec-draft-v1",
  "canonical_key": "openai-symphony-service-spec-draft-v1",
  "visibility": "private",
  "captured_at": "2026-05-05",
  "local_artifacts": [
    "experiments/harness-scout/runs/2026-05-05-symphony-compatible-farplane/source-summary.md"
  ],
  "feature_refs": ["FEAT-0014"],
  "decision": "adapt",
  "duplicate_of": null,
  "status": "active",
  "last_verified": "2026-05-05",
  "notes": "Use as scheduler/runtime inspiration; Farplane stays normal Codex plus skills."
}
```

## Field Contract

- `id`: stable `SRC-####` identifier; never reuse an ID for a different source.
- `title`: short human-readable source title.
- `source_type`: `spec`, `blog`, `video`, `docs`, `repo`, `paper`,
  `user-provided`, or `research`.
- `origin`: where the source came from, such as a URL host, local repo, or
  operator-provided chat context.
- `canonical_url`: canonical URL when public, or a stable non-URL key such as
  `user-provided:<slug>` or `local-research:<slug>` when no public URL exists.
- `canonical_key`: normalized dedupe key. Use lowercase words joined by `-`.
- `visibility`: `public`, `private`, `internal`, `customer`, or `unknown`.
- `captured_at`: date the source was first captured in `YYYY-MM-DD` form.
- `local_artifacts`: local research memos, scout runs, summaries, scorecards,
  or handoffs that preserve the source decision.
- `feature_refs`: `FEAT-*` IDs influenced by this source.
- `decision`: `adopt`, `adapt`, `reject`, `defer`, `duplicate`, or
  `reference-only`.
- `duplicate_of`: `null` for canonical records or a `SRC-*` ID for duplicates.
- `status`: `active`, `archived`, `superseded`, or `sensitive-redacted`.
- `last_verified`: date the record was checked against live repo artifacts.
- `notes`: one concise operator-facing note about how to use the source.

## Update Rules

1. Search `canonical_url`, `canonical_key`, title, and known local artifacts
   before adding a new record.
2. Add a new `SRC-*` record only when the source identity is genuinely new.
3. If the source is a duplicate, add or update a record with `decision:
   duplicate` and `duplicate_of` instead of opening new feature tickets.
4. Keep raw transcripts, bulky source extracts, customer details, and secrets
   out of this registry. Link to redacted scout artifacts instead.
5. Link source records to `FEAT-*` records when durable techniques exist; link
   to tickets or research artifacts when a source is still only inspiration.
6. Keep `docs/features/registry.jsonl` focused on harness techniques. Do not
   copy source identity fields into feature records.

## ID Allocation

1. Read every existing `id` value in `registry.jsonl`.
2. Pick the next unused numeric ID in `SRC-####` form.
3. Do not fill gaps without checking tickets and archived branches that may
   already reference the missing ID.
4. Do not rename or reuse an ID after another doc, ticket, or feature record
   references it.

## Retention Rules

- Public sources may link to public URLs and compact local scout artifacts.
- Private or operator-provided sources should use stable `user-provided:<slug>`
  keys and compact summaries only.
- Customer/internal/sensitive sources must be redacted before tracked storage.
- Raw transcripts and full article copies stay out of canonical docs unless a
  later ticket explicitly defines a safe retention policy.

## Validation

Run this before claiming registry edits are safe:

```bash
python3 docs/sources/validate_sources.py
```

The validator checks JSONL shape, ID uniqueness, canonical-key uniqueness,
allowed enum values, local artifact existence, `FEAT-*` references, duplicate
links, and date formats.
