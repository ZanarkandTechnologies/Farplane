# Feed Scout Codex Automation Prompt

Run `feed-scout:run` for the configured tracked profiles and harness resources.

Configured local surfaces:

- source config: `farplane/bindings.yaml#feed_scout`
- daily feed root: `.farplane/feed-scout/daily`
- ingestion ledger: `.farplane/feed-scout/ledger.jsonl`
- proposal ledger or local inbox: `.farplane/feed-scout/proposals.jsonl`
- report root: `.farplane/reports/feed-scout`

Steps:

1. Load the `feed_scout` config named by the automation.
2. Validate configured profile/resource rows before discovery.
3. Validate that every harness resource references existing tracked entities and
   that child resources reference an existing parent resource.
4. Discover new content for enabled profiles and enabled harness resources
   using the configured fetch method.
5. Normalize discovered content with
   `skills/feed-scout/scripts/normalize_items.py`.
6. Compute canonical keys with `skills/feed-scout/scripts/dedupe_key.py`.
7. Skip seen URLs and queue new or changed content items.
8. Extract content with `summarize`, repo inspection, or existing thread text.
9. Run `harness-scout` on eligible content items and cite `entity_ids` when
   several resources come from the same person or organization.
10. Use `best-of-worlds` when several scout runs point at the same pattern.
11. Write proposal rows to Notion or a local review inbox only when the
    destination is explicitly configured.
12. Write `.farplane/feed-scout/daily/feed-YYYY-MM-DD.json`,
    `.farplane/feed-scout/daily/latest.json`,
    `.farplane/reports/feed-scout/<timestamp>.md`, and
    `.farplane/reports/feed-scout/latest.json` when those paths are configured.
13. Record evidence paths and blockers in the run summary.

Do not poll forever, launch Codex, push code, spend API budget, or create live
Notion databases unless the automation configuration explicitly authorizes that
action.
