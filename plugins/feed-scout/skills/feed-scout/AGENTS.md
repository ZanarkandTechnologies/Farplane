# Feed Scout Instructions

This folder owns the feed-scout recipe for tracked-profile monitoring.

## Local Rules

- Keep `feed-scout` as an explicit-run recipe, not a daemon or hidden runner.
- Model user configuration as tracked profiles first, then discovered content
  items, then URL-keyed ledger rows.
- Use helper scripts for deterministic validation, URL keys, and fixture
  normalization.
- Do not store raw transcripts, bulky article text, secrets, or customer data
  in tracked docs.
- Promote only useful/scouted items into `docs/sources/registry.jsonl`.
- Keep Notion as proposal review/writeback, not the only durable source of
  truth.
- For live Notion Tasks writeback, resolve required `Project` and `Areas`
  relations from explicit context or private Notion handles before writing, and
  verify them by readback after writing. If either relation is missing, mark the
  projection `routing_missing` or use local-only output instead of claiming
  success. See `MEM-0123`.
- Never commit private Notion database IDs, page IDs, or workspace handles to
  reusable skill files, templates, fixtures, or docs.
