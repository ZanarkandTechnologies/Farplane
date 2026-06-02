# notion-context tasks_this_week fallback recipe

This mirror documents how `notion-context.tasks_this_week` should behave when
two different Notion MCP surfaces are available at different times.

## Goal

Return normalized task rows for the canonical weekly Tasks view when possible.
When exact enumeration is unavailable, report connector state and continue with
a safe local fallback for Farplane automation. Do not use semantic search to
approximate task rows.

## Canonical Inputs

- Weekly Tasks view:
  private handle `notion.tasks.this_week_view`
- Weekly Tasks data source recovered by fetching the canonical URL:
  private handle `notion.tasks.source`
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

2. `mcp_data_source_query`
   - Use when the app connector can fetch database/data-source metadata and
     query a data source, but cannot query a saved view.
   - Fetch the canonical weekly Tasks URL to recover the database/data-source
     identifier and schema.
   - In the current Tasks database, the recovered source is private handle
     `notion.tasks.source`.
   - Query the recovered data source with the closest available SQL/filter:
     keep `Status != Done` for active planning, include `Backlog`, `Not started`,
     `In Progress`, and `Review`, and prefer rows with `Act Time` in the current
     visible weekly window when the date property is queryable.
   - If exact view filters cannot be reproduced, mark
     `context_gap: "view_filter_approximated"` on normalized rows.
   - If a connector advertises a data-source query wrapper but returns
     `notion-query-data-sources not found`, stop Notion row enumeration and
     continue to `connector_unavailable`; do not treat that as a task-board
     failure.
   - Fetch or query the not-done Projects source when relation URLs need
     enrichment; otherwise keep project relation URLs and mark the missing
     project context.

3. `local_token_mcp_data_source_query`
   - Use when the remote OAuth Notion MCP cannot query rows, but the local
     token-backed Notion MCP server is configured in Codex as
     `@notionhq/notion-mcp-server`.
   - This is still an MCP path. It should expose `API-query-data-source`,
     `API-retrieve-a-page`, and related `API-*` tools.
   - Query the same Tasks data source with read-only filters:
     `Act Time` in the requested window and `Status != Done`.
   - Do not call Notion's public API directly from custom scripts for this
     wrapper; the API token belongs inside the local MCP server config.

4. `connector_unavailable`
   - Use when Notion tools are absent or authentication is expired.
   - Also use this when the exposed MCP surface can fetch metadata but cannot
     query rows.
   - Report the connector state explicitly.
   - Fall back to the local filesystem ticket board for Farplane automation.
   - Do not create, update, or complete Notion tasks.

## Subagent Probe Discipline

When testing this wrapper through a subagent, require staged progress writes:

1. Write an artifact header and exact visible Notion MCP tool names first.
2. Run a bounded local-token MCP Tasks proof with `API-query-data-source`,
   `page_size: 5`, `Act Time` in the requested window, and `Status != Done`.
3. Append normalized rows plus `has_more` and `next_cursor` before attempting
   full paging.
4. Page full Tasks rows in bounded chunks and append after each page.
5. Query pinned rows separately with `Pinned = true` and `Act Time` within the
   last 14 days, then fetch pinned page bodies one at a time and append a read
   marker after each page.
6. Fetch Goals and Projects as independent branches; record `filter_gap` if
   their exact local-token MCP filters are not encoded yet.

If a broad probe writes no artifact progress within one minute, interrupt it
and rerun only the bounded Tasks proof stage before continuing.

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
- Never use semantic search as a fallback for task-board enumeration.
- Never call the public Notion API directly from ad hoc scripts; token-backed
  Notion access must flow through the local MCP server.
- Never select a local work item just because Notion context is thin; select
  local work only when the filesystem ticket board itself has a safe ready
  ticket.
- Auth expiry and missing query tools are connector state, not task-board
  failure.
