# Feature Registry

Farplane's feature registry is generated compatibility output for structured
harness feature records. The authored source lives in active specs through
`feature_records_json` front matter blocks.

Use the generated registry when a source, video, blog, repo, or ticket proposes
a feature and the agent needs to answer:

- does Farplane already have this?
- where does it live?
- what source or ticket introduced it?
- what evidence proves it works?
- what limits or metrics should future work consider?

Use `skills/harness-advisor/` when the operator is asking where a proposed
Farplane improvement should live. That skill checks generated feature records
for existing features before recommending a primary surface.

`docs/specs/harness-techniques.md` remains the skimmable human inventory.
`docs/specs/feature-catalog.md` is the transitional spec-owned metadata source
for cross-cutting or historical records. Prefer moving records into the
smallest owning spec over adding new catalog-only entries.
`docs/features/registry.jsonl` is the queryable generated feature record for
technique dedupe, provenance, and benchmark history. `docs/sources/registry.jsonl`
is the source provenance registry; use `SRC-*` there to dedupe blogs, specs,
videos, docs, and repos before deciding whether they introduce or update
`FEAT-*` records.

## Record Shape

Each generated line in `registry.jsonl` is one JSON object:

```json
{
  "id": "FEAT-0063",
  "name": "Metric advisor cards",
  "status": "implemented",
  "category": "skills",
  "surfaces": ["skills/metric-advisor", "docs/specs/self-improvement-contracts.md"],
  "source_refs": ["tickets/TASK-0228/ticket.md"],
  "external_refs": [],
  "evidence_refs": ["skills/metric-advisor/SKILL.md"],
  "known_limits": "Advisory metric-card contract only; callers still own execution.",
  "metrics": ["metric_card_traceability_pass"],
  "last_verified": "2026-06-26"
}
```

## Field Contract

- `id`: stable `FEAT-####` identifier; never reuse an ID for a different
  technique.
- `name`: short, unique technique name.
- `status`: `implemented`, `partial`, `proposed`, `designed`, `deferred`, or
  `retired`.
- `category`: broad grouping such as `planning`, `proof`, `memory`,
  `source-ingestion`, `skills`, or `improvement-loop`.
- `surfaces`: repo paths that own the live behavior.
- `source_refs`: `SRC-*` records, local docs, tickets, memories, or specs that
  explain why the feature exists.
- `external_refs`: outside URLs, repos, videos, or standards that influenced the
  feature.
- `evidence_refs`: tickets, artifacts, commands, or experiment outputs that
  support the current status.
- `known_limits`: one concise caveat agents should preserve when comparing
  source ideas.
- `metrics`: metric names or scorecards associated with the feature. Leave empty
  when the feature is not benchmarked yet.
- `last_verified`: date when the record was last checked against live surfaces.

## Update Rules

1. Add or update `feature_records_json` in the smallest owning spec when a
   shipped or planned harness technique needs dedupe, provenance, or benchmark
   tracking.
2. Keep raw transcripts, bulky summaries, and one-off logs in `experiments/`,
   not in feature records.
3. Link to ticket evidence instead of copying proof into the record.
4. Keep `harness-techniques.md` synchronized at the category/status level, but
   do not duplicate every registry field there.
5. When a source proposes a feature, use `harness-scout` to search
   `docs/sources/registry.jsonl` first for source dedupe, then generated feature
   records for feature dedupe before creating a new ticket.
6. Run `python3 docs/features/validate_features.py --write` after metadata
   edits. Do not hand-edit `registry.jsonl`.

## Skill-Applicable Features

Use the same generated registry for features that apply to Farplane skill
packages. Set `category` to `skills` and keep the operational details in the
feature row's `surfaces`, `evidence_refs`, `known_limits`, and `metrics`.

Do not create a second hand-authored skill feature registry. The skill package
inventory already lives in generated form at `docs/skills/registry.jsonl`, and
future per-skill adoption fields should reference `FEAT-####` handles from this
registry rather than loose feature names.

Use [docs/specs/harness-techniques.md](../specs/harness-techniques.md#self-growing-harness-map)
for the full self-growing harness map.

## ID Allocation

1. Read generated `id` values before adding a record.
2. Pick the next unused numeric ID in `FEAT-####` form.
3. Do not fill gaps without checking archived branches or tickets that may
   already reference the missing ID.
4. Do not rename or reuse an ID after another doc, ticket, scorecard, or source
   run references it.

## Verification Rules

- Refresh `last_verified` when the record's status, surfaces, evidence, known
  limits, or metrics are checked against live repo files.
- Do not refresh `last_verified` for pure wording edits that do not inspect the
  live surfaces.
- If a feature moves from `proposed` to `implemented`, link the ticket or
  artifact that proves the change in `evidence_refs`.
- If a feature is retired, set `status` to `retired`, keep the record, and add
  the removal evidence instead of deleting the row.
- Prefer specific ticket or artifact paths over broad refs such as
  `docs/HISTORY.md` when proof exists.

## Validation

Run this before claiming feature metadata edits are safe:

```bash
python3 docs/features/validate_features.py --write
python3 docs/features/validate_features.py
```

The validator scans active specs for `feature_records_json`, writes or checks
the generated JSONL, and validates shape, ID uniqueness, allowed enum values,
local surface/evidence existence, `SRC-*` source references, date formats, and
generated-output freshness.
