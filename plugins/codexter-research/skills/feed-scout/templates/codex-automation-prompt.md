# Feed Scout Codex Automation Prompt

Run `feed-scout:run` for the configured tracked profiles.

Steps:

1. Load the tracked profile DB or fixture named by the automation.
2. Validate profile rows with `skills/feed-scout/scripts/validate_profiles.py`.
3. Discover new content for enabled profiles using the configured fetch method.
4. Normalize discovered content with
   `skills/feed-scout/scripts/normalize_items.py`.
5. Compute canonical keys with `skills/feed-scout/scripts/dedupe_key.py`.
6. Skip seen URLs and queue new or changed content items.
7. Extract content with `summarize` or existing thread text.
8. Run `harness-scout` on eligible content items.
9. Use `best-of-worlds` when several scout runs point at the same pattern.
10. Write proposal rows to Notion or a local review inbox only when the
    destination is explicitly configured.
11. Record evidence paths and blockers in the run summary.

Do not poll forever, launch Codex, push code, spend API budget, or create live
Notion databases unless the automation configuration explicitly authorizes that
action.
