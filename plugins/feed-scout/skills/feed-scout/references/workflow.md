# Feed Scout Workflow

## Configure

1. Accept a list of profile URLs or handles.
2. Infer `platform` and default `fetch_method`.
3. Apply defaults for cadence, tags, and signal threshold.
4. Validate the resulting tracked-profile rows.
5. Return setup steps and human gates for credentials, Notion, or automation.

## Run

1. Load enabled tracked profiles.
2. Discover new content from each profile.
3. Normalize raw output into `ContentItem` rows.
4. Compute canonical URL keys.
5. Skip seen items; queue new or changed items.
6. Extract content with `summarize` or existing thread text.
7. Run `harness-scout` on eligible content items.
8. Update the ingestion ledger with scout/proposal links.

## Review

1. Load pending proposals.
2. Group by tags, profile, or repeated decision pattern.
3. Use `best-of-worlds` for related proposals when several sources converge.
4. Recommend accept, reject, defer, or ticket.
5. Route accepted implementation work to `impl-plan`.

## Status

Report:

- tracked profile count
- enabled/disabled count
- last run time
- unseen content count
- pending proposal count
- credential or Notion blockers
- latest local evidence path

