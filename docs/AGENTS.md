# Docs Instructions

This tree owns durable human-readable context. Keep the document set as small
as possible while maximizing reader quality, source-of-truth clarity, and
machine-checkable outputs.

## Strategy

- Update an existing owner before creating a new doc.
- Put current behavior contracts in `docs/specs/`.
- Put reusable theory, doctrine, and background in `docs/fundamentals/`.
- Put public framework narrative in `docs/farplane-framework/`.
- Put generated or machine-readable inventories behind their owning source
  files; do not hand-author duplicate truth.
- Put task-local plans, proof, and bulky evidence in tickets or artifacts.
- Put temporary research outside tracked docs unless it has a current owner.

## Feature Records

Specs own feature metadata. Add or update `feature_records_json` in the
smallest owning spec, preferring an existing behavior spec over a new catalog
entry. Use `docs/specs/feature-catalog.md` only for transitional, cross-cutting,
or historical records without a clearer spec owner.

After editing feature metadata, run:

```bash
python3 docs/features/validate_features.py --write
```

`docs/features/registry.jsonl` is generated compatibility output. Do not
hand-edit it.

## Stale Docs

Delete stale docs instead of preserving archives by default. Before deleting,
move any current contract, lesson, or source decision into the smallest active
owner: a spec, fundamentals doc, skill, ticket, or generated registry source.
