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
3. Enforce compact-query mode before any Notion MCP call:
   - At most 1 Tasks candidate query, `page_size <= 25`.
   - Always pass `filter_properties`; never query Tasks, Projects, or Goals
     broadly in this automation.
   - Do not use `notion-context` or search for initial Task candidates in this
     scheduled mode; wrappers may hide broad queries.
   - Do not repeat an equivalent data-source query. If compact querying fails,
     record `context_gap: compact_query_failed` and stop instead of retrying
     broadly.
4. Fetch recent candidate Tasks through Notion MCP with incomplete-status,
   missing-target-field, and narrow time-window filters. Normalize immediately,
   dedupe by page ID, then discard raw rows.
5. Before reading row contents, inspect the first returned row's property names.
   If the response includes unexpected keys such as `Display`, `Days Left`,
   `Blocked by`, `Skills Practiced`, `Location`, `Unblocked`, or formula/rollup
   fields, the query was wrong. Write `context_gap:
   unexpected_task_properties`, stop, and do not make more Notion calls.
6. If no normalized candidates remain, write empty artifacts and skip Plan Week,
   pinned pages, Projects, and Goals.
7. Fetch context only as needed:
   - Plan Week/pinned pages: at most 1 compact query when candidates need
     planning context.
   - Projects: at most 1 compact query only when a candidate needs Project or
     Areas inference.
   - Goals: at most 1 compact query only when goal relations are relevant.
8. Normalize rows and drop raw formulas, private IDs, formula URLs, and noisy
   fields before reasoning.
9. Produce per-field proposals with confidence and reasons.
10. Write `proposal.json`, `proposal.md`, `low-confidence-telegram.md`, and
   `run-summary.md` under the run artifact directory.
11. Send Telegram review requests for low-confidence or conflicted fields when
   Telegram is configured; otherwise record the fallback message path.
12. In `live-high-confidence` mode only, apply high-confidence typed patches and
   verify readback.
13. End with a concise summary of patches, suggestions, review requests,
    source gaps, and write receipts.

Hard gates:

- Do not mutate Notion in `dry-run`, `notify`, `weekly-preflight`, fixture, or
  connector-fallback mode.
- Do not write medium/low-confidence fields.
- Do not mutate task `Status`.
- Do not use raw public Notion API scripts.
- Do not create another recurring runner from inside this run.
- Do not paginate automatically or fetch full Notion page objects in scheduled
  mode.
- Do not continue after repeated `API_query_data_source` calls or unexpected
  Tasks properties; write a blocked summary instead.
