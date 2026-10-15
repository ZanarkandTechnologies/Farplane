# Feed Scout Instructions

This folder owns the feed-scout recipe for tracked-profile monitoring.

## Local Rules

- Keep `feed-scout` as an explicit-run recipe, not a daemon or hidden runner.
- Write the dated report before handing off candidates. Feed Scout creates no
  tickets, issues, or tasks; recovery and opportunity items stay candidates.
- Model user configuration as tracked profiles first, then discovered content
  items, then URL-keyed ledger rows.
- Use helper scripts for deterministic validation, URL keys, and fixture
  normalization.
- Do not store raw transcripts, bulky article text, secrets, or customer data
  in tracked docs.
- Promote only useful/scouted items into `farplane/sources/registry.jsonl`.
- The repo is public: private or operator-provided sources get
  `user-provided:<slug>` keys and compact summaries only; redact customer or
  internal sources before they are tracked; raw transcripts and full article
  copies never enter the registry.
- Keep Notion as an optional proposal review view, not the only durable source of
  truth.
- Do not invoke Goal, Pulse, workers, implementation, publication, outreach, or
  live Tasks writeback from candidate or recovery generation.
- Never commit private Notion database IDs, page IDs, or workspace handles to
  reusable skill files, templates, fixtures, or docs.
