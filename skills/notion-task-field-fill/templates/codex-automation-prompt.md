# Notion Task Field Fill Automation Prompt

Run `notion-task-field-fill` for the configured cadence.

Inputs:

- Mode: `notify` unless the automation is explicitly approved for
  `live-high-confidence`.
- Window: the last `N` hours in Asia/Kuala_Lumpur time.
- Target fields: `Act Time`, `Project`, `Areas`, `Attention Required`, `Tags`.

Steps:

1. Load `/Users/kenjipcx/.codex/private/TOOLS.md` and the focused private
   Notion doc it references, including the private compact property-id map.
2. Resolve named handles such as `notion.tasks.source`; do not print or persist
   resolved private IDs in tracked artifacts.
3. If a local helper script needs Notion credentials, use
   `scripts/notion_config.py` to load `NOTION_TOKEN` from the runtime env
   supplied by `farplane run -- <command>` or Doppler. Local TOML is not a
   credential source; do not read `NOTION_API_KEY` or Codex MCP config. When invoking `ntn`, bridge
   `NOTION_TOKEN` to `NOTION_API_TOKEN` only for that subprocess.
4. Enforce compact-query mode before any `ntn` Notion call:
   - At most 1 Tasks candidate query, `page_size <= 25`.
   - Always pass `filter_properties==<property-id>` query parameters; never
     query Tasks, Projects, or Goals broadly in this automation.
   - Do not use a separate Notion wrapper skill or search for initial Task
     candidates in this scheduled mode; wrappers may hide broad queries.
   - Do not repeat an equivalent data-source query. If compact querying fails,
     record `context_gap: compact_query_failed` and stop instead of retrying
     broadly.
5. Fetch recent candidate Tasks through `ntn api /v1/data_sources/{id}/query`
   with incomplete-status,
   missing-target-field, and narrow time-window filters. Normalize immediately,
   dedupe by page ID, then discard raw rows.
6. Before reading row contents, inspect the first returned row's property names.
   If the response includes unexpected keys such as `Display`, `Days Left`,
   `Blocked by`, `Skills Practiced`, `Location`, `Unblocked`, or formula/rollup
   fields, the query was wrong. Write `context_gap:
   unexpected_task_properties`, stop, and do not make more Notion calls.
7. If no normalized candidates remain, write empty artifacts and skip Plan Week,
   pinned pages, Projects, and Goals.
8. Fetch context only as needed:
   - Plan Week/pinned pages: at most 1 compact query when candidates need
     planning context.
   - Projects: at most 1 compact query only when a candidate needs Project or
     Areas inference.
   - Goals: at most 1 compact query only when goal relations are relevant.
9. Normalize rows and drop raw formulas, private IDs, formula URLs, and noisy
   fields before reasoning.
10. Produce per-field proposals with confidence and reasons.
11. Write `proposal.json`, `proposal.md`, `low-confidence-telegram.md`, and
   `run-summary.md` under the run artifact directory.
12. Send Telegram review requests for low-confidence or conflicted fields when
   Telegram is configured; otherwise record the fallback message path.
13. In `live-high-confidence` mode only, apply high-confidence typed patches and
   verify readback.
14. End with a concise summary of patches, suggestions, review requests,
    source gaps, and write receipts.

Hard gates:

- Do not mutate Notion in `dry-run`, `notify`, `weekly-preflight`, fixture, or
  connector-fallback mode.
- Do not write medium/low-confidence fields.
- Do not mutate task `Status`.
- Do not use raw public Notion API scripts, Notion MCP, or `NOTION_API_KEY`
  credential fallbacks.
- Do not create another recurring runner from inside this run.
- Do not paginate automatically or fetch full Notion page objects in scheduled
  mode.
- Do not continue after repeated equivalent `ntn` data-source query calls or unexpected
  Tasks properties; write a blocked summary instead.
