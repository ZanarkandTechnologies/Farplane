# notion-context tasks_this_week fallback recipe

This mirror documents how `notion-context.tasks_this_week` should behave when
two different Notion MCP surfaces are available at different times.

## Goal

Return normalized task rows for the canonical weekly Tasks view when possible.
When exact enumeration is unavailable, return a degraded-but-honest diagnostic
and continue with a safe local fallback for Codexter automation.

## Canonical Inputs

- Weekly Tasks view:
  `https://app.notion.com/p/638d85a858b04d038d8b97be1a879a1f?v=2de4d8d5-ed56-42b1-9665-957507d26d52`
- Weekly Tasks data source recovered by fetching the canonical URL:
  `collection://43a439fd-74c5-4b43-9afb-950f047e5d4f`
- Not-done Projects view:
  `view://35cd43a2-3942-81aa-95fd-000c1396f17d`

## Fallback Ladder

1. `exact_view_query`
   - Use when a strong Notion MCP exposes a saved-view/database-view query
     tool.
   - Query the canonical view directly.
   - Page through results until the operation has enough rows for the requested
     task, or until the view is exhausted.
   - Normalize rows immediately; drop formula fields.

2. `api_data_source_query`
   - Use when the MCP row-query tool is unavailable but a public Notion API
     token is available in `NOTION_API_KEY` or `NOTION_TOKEN`.
   - Run:
     `python3 bin/notion_tasks_this_week.py --start YYYY-MM-DD --end YYYY-MM-DD --json`
   - For "this week" automation, use `[today - 7 days, today]` unless the user
     explicitly asks for a different window.
   - The helper calls Notion's public Data Sources API:
     `POST /v1/data_sources/43a439fd-74c5-4b43-9afb-950f047e5d4f/query`.
   - It filters `Act Time` with `on_or_after` and `on_or_before`, filters
     `Status` with `does_not_equal: Done`, sorts by `Act Time` and `Status`,
     and emits normalized rows.

3. `mcp_data_source_query`
   - Use when the app connector can fetch database/data-source metadata and
     query a data source, but cannot query a saved view.
   - Fetch the canonical weekly Tasks URL to recover the database/data-source
     identifier and schema.
   - In the current Tasks database, the recovered source is
     `collection://43a439fd-74c5-4b43-9afb-950f047e5d4f`.
   - Query the recovered data source with the closest available SQL/filter:
     keep `Status != Done` for active planning, include `Backlog`, `Not started`,
     `In Progress`, and `Review`, and prefer rows with `Act Time` in the current
     visible weekly window when the date property is queryable.
   - If exact view filters cannot be reproduced, mark
     `context_gap: "view_filter_approximated"` on normalized rows.
   - If a connector advertises a data-source query wrapper but returns
     `notion-query-data-sources not found`, skip this tier and continue to
     `search_fetch_diagnostics`; do not treat that as a task-board failure.
   - Fetch or query the not-done Projects source when relation URLs need
     enrichment; otherwise keep project relation URLs and mark the missing
     project context.

4. `search_fetch_diagnostics`
   - Use when only weak Notion tools such as fetch/search are exposed.
   - Fetch the canonical weekly Tasks URL first. If fetch proves the page/view
     exists but does not enumerate rows, search for narrow candidate terms from
     the user's request or known foreground Codexter task names.
   - Search inside the recovered Tasks data source when supported:
     `collection://43a439fd-74c5-4b43-9afb-950f047e5d4f`.
   - Use small targeted searches such as `In progress Review`,
     `Foreground Codexter automation`, and known task terms from the user
     request. Avoid one huge broad query.
   - Fetch each candidate task page. Page fetches include a `<properties>` JSON
     block with `Status`, `Act Time`, `Project`, `Pinned`,
     `Attention Required`, `Tags`, and `url`.
   - Normalize fetched candidate pages, then locally filter to `Status != Done`
     and prefer `Status in {"In progress", "Review"}` plus foreground/pinned
     rows.
   - Return candidates as `candidate_rows` with
     `context_gap: "search_fetch_diagnostics_not_complete_view"`, not as
     complete board enumeration.
   - For unattended Codexter automation, fall back to the local filesystem
     ticket board unless candidate task pages provide enough permanent project
     context to select work safely.

5. `connector_unavailable`
   - Use when Notion tools are absent or authentication is expired.
   - Report the connector state explicitly.
   - Fall back to the local filesystem ticket board for Codexter automation.
   - Do not create, update, or complete Notion tasks.

## Normalized Task Shape

Keep:

- `Name`
- `Status`
- `Act Time`
- `Project`
- `Projects`
- `Related Entities`
- `Description`
- `Attention Required`
- `Pinned`
- `Tags`
- `execution_context`
- `context_gap`
- `url`

Drop formula fields such as `Display`, `Days Left`, `Progress`, `Hours Spent`,
and `formulaResult://...` pointers unless the caller asks for connector
diagnostics.

## Safety Rules

- Never mutate Notion status from an automation fallback.
- Never claim weak search/fetch diagnostics are complete task-board
  enumeration.
- Never select a local work item just because Notion context is thin; select
  local work only when the filesystem ticket board itself has a safe ready
  ticket.
- Auth expiry and missing query tools are connector state, not task-board
  failure.
