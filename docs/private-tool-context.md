# Private Tool Context

Farplane keeps reusable harness behavior in the repo and personal environment
facts outside the repo. This lets skills and templates stay shareable while
local agents can still find the handles they need to operate in Kenji's
workspace.

## Concept

Use this split:

- `skills/*`: how a workflow works.
- tracked docs and templates: what the reusable harness expects.
- `~/.codex/private/TOOLS.md`: local index of private tool context.
- `~/.codex/private/docs/*`: focused private notes for one tool or workspace.
- local env/MCP config: credentials and tokens.

Skills can point to private docs by path or named handle, but they should not
embed private database IDs, private URLs, device names, or account-specific
workspace notes.

## Recommended Layout

```text
~/.codex/private/
  TOOLS.md
  docs/
    notion.md
    local-paths.md
    telegram.md
```

`TOOLS.md` is the table of contents. Tool-specific files own the actual handles.

For example, Notion context belongs in `~/.codex/private/docs/notion.md`:

- Tasks, Projects, and Goals data source handles
- canonical saved view handles
- private schema notes needed for planning
- page creation defaults and project/area mappings

The reusable `notion-context` skill should say how to query, normalize, and
fall back safely. It should refer to private handles such as
`notion.tasks.source` instead of hard-coding the underlying collection URL.

## What Goes Where

Put in private docs:

- Notion database IDs, saved view URLs, page examples, and schema cache notes
- local service URLs, device names, SSH aliases, workspace-specific paths
- account-specific tool preferences and private project mappings
- non-secret handles that would still be awkward or leaky in a public repo

Put in local env or MCP config:

- API tokens
- bot tokens
- private ingest keys
- cookies, session secrets, and credentials

Put in tracked repo docs:

- the conceptual rule
- placeholder examples
- named handles
- safety policy and proof expectations
- tests that prove behavior without live private IDs

## Rules

- Do not copy private docs into tracked repos, shared skills, public docs,
  tickets, generated templates, or test fixtures.
- Use named handles or placeholders in shared artifacts.
- Keep credentials out of private Markdown docs when an env file or MCP config
  is the correct owner.
- If a private handle is required but missing, fail closed with a clear
  `private_context_missing` or `configured: false` state.
- For Notion planning automation, keep access MCP-only. Do not add public
  Notion API script fallbacks.

## Example Pattern

Shared skill text:

```md
Load `~/.codex/private/docs/notion.md` and resolve `notion.tasks.source`.
Query rows through the Notion MCP. If the private handle is missing, report
`private_context_missing`; do not guess with semantic search.
```

Private doc text:

```md
### `notion.tasks.source`

- Data source: `collection://...`
- Database URL: `https://www.notion.so/...`
```

Tracked test text:

```md
Weekly Tasks source: private handle `notion.tasks.source`
Expected fallback: connector unavailable or local filesystem board
Forbidden actions: mutate Notion status, public API fallback
```

## Verification

For refactors that move private handles out of tracked surfaces:

```bash
rg -n "LIVE_ID_OR_PRIVATE_URL_PATTERN" . ~/.codex/skills/<skill-name>
python3 tickets/scripts/check_ticket_metadata.py
python3 bin/check_skill_capabilities.py validate
```

The grep should return no tracked or reusable-skill matches for the live handle.
Private docs may still contain the real value.
