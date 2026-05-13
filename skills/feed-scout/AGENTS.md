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

