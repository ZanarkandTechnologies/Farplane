---
title: Notion Task Field Fill Workflow Detail
status: active
owner: notion-task-field-fill
---

# Notion Task Field Fill Workflow Detail

Load this reference after candidates exist or when preparing a scheduled/live
run. The first-load skill owns gates and phase order; this file owns modes,
query budgets, field rules, artifacts, automation shape, and completion detail.

## Job

For a bounded task window:

1. Fetch recent Notion Tasks that are missing operational planning fields.
2. Fetch the latest user context needed to infer safe values.
3. Produce per-field proposals with confidence, reasons, source refs, and
   abstentions.
4. Send Kenji a Telegram review request for low-confidence fields.
5. Optionally apply high-confidence patches through a typed Notion action
   surface, then verify readback.

## Modes

- `dry-run`: default. Produce the proposal artifact and Telegram review message
  artifacts; do not mutate Notion.
- `notify`: dry-run plus best-effort Telegram messages for low-confidence or
  blocked fields.
- `live-high-confidence`: apply only typed high-confidence patches after the
  proposal artifact exists. Verify readback for every changed page.
- `weekly-preflight`: run dry-run against the weekly review window and add a
  `Task Hygiene` section for the caller's weekly strategy automation.
- `fixture`: use local tests and examples only; do not call Notion or Telegram.

## Inputs

Accept a compact run envelope:

```json
{
  "mode": "dry-run",
  "hours": 6,
  "timezone": "Asia/Kuala_Lumpur",
  "fields": ["Act Time", "Project", "Areas", "Attention Required", "Tags"],
  "candidate_statuses": ["Not started", "In progress", "Review"],
  "artifact_dir": ".farplane/state/notion-task-field-fill/runs/<run-id>"
}
```

When `hours` is omitted for a scheduled run, use the automation cadence. When
the user says "this week", use Monday 00:00 through now in
Asia/Kuala_Lumpur.

## Context Sources

Load private handles, schema notes, compact property IDs, project/area mappings,
and task-creation defaults from
`/Users/kenjipcx/.codex/private/docs/notion.md`. Query the live workspace
through `ntn` only. Scheduled `notify` mode has a strict order: candidate
Tasks must come from the explicit compact Tasks query in the next section, not
from a broad wrapper or search result.

- recent candidate Tasks from the private handle `notion.tasks.source`
- latest pinned `Plan Week` page body
- required recent pinned planning pages
- not-done Projects with context, focus, tags, status, active period, and area
  mapping
- active Goals
- active Areas or latest project/area mapping from private Notion context

If an active Areas view is missing, use the latest project/area mapping from
private Notion context and mark `context_gap: "areas_view_missing"`.

## Compact Query Contract

Scheduled automation runs must optimize for the smallest useful Notion payload.
The failure mode to avoid is fetching full Notion page objects repeatedly and
only normalizing after the model context has already absorbed formula, relation,
URL, and rollup payloads.

Before querying, read the private Notion doc for source handles and the
private-only compact property-id map. Keep those IDs out of tracked artifacts.

Default call budget for `notify` mode:

- Tasks: 1 compact candidate query.
- Plan Week or pinned planning pages: 0 calls when no candidate tasks exist; at
  most 1 compact pinned-page query when candidates need context.
- Projects: 0 calls when no candidate has missing `Project` or `Areas`; at most
  1 compact not-done project query.
- Goals: 0 calls unless candidate task or project relations mention goals; at
  most 1 compact active-goal query.
- Search: disabled for scheduled runs unless the candidate title contains an
  exact active-project alias already documented in private context.

For every `ntn api /v1/data_sources/{data_source_id}/query` call:

- Set `page_size` to the smallest honest limit: `25` for task candidates,
  `20` for projects, `10` for goals, and `5` for pinned planning pages.
- Pass `filter_properties==<property-id>` query parameters for only the fields
  needed by the run. Never query a Tasks, Projects, or Goals data source
  without `filter_properties`.
- Sort by the narrow date/status signal needed for the call. Do not paginate
  automatically in scheduled runs; record `context_gap: "candidate_page_limit"`
  if the page limit is hit.
- Deduplicate immediately by page ID and discard raw rows after creating
  normalized summaries.
- Do not call the same data source with an equivalent filter twice. If a compact
  query fails or returns unexpectedly huge raw rows, stop and record
  `context_gap: "compact_query_failed"` instead of retrying broadly.

After the Tasks candidate query, inspect only the property keys of the first
returned row before reading row contents. The only allowed Tasks keys are:
`Name`, `Status`, `Act Time`, `Task Due Date`, `Project`, `Areas`,
`Attention Required`, `Tags`, `Description`, `Pinned`, and `Goals`. If the
response includes unrelated keys such as `Display`, `Days Left`, `Blocked by`,
`Skills Practiced`, `Location`, `Unblocked`, `Related Entities`, or formula and
rollup fields, treat the query as wrong: record
`context_gap: "unexpected_task_properties"`, write a short blocked run summary,
and stop without further Notion calls.

Scheduled runs must produce a tiny `query-ledger` section in `run-summary.md`
with each Notion call's purpose, page size, sanitized property names, candidate
count, `has_more`, and whether raw rows were discarded. Do not include Notion
IDs or URLs in this ledger.

For the scheduled six-hour run, the Tasks query should filter to incomplete
rows with at least one missing target field and a current-window signal. Prefer
`created_time` when the `ntn`/API surface supports it. If only property filters are
available, use `Act Time` inside the local day/week window, then post-filter
top-level `created_time` during normalization. If no candidates remain after
post-filtering, write empty artifacts and skip all context calls.

## Proposal Rules

Use the detailed model in [references/model.md](references/model.md) and the
confidence rubric in [references/confidence.md](references/confidence.md).

Core rules that must be applied every run:

- Infer per field, not per task.
- A task with an existing project should inherit the project's area when the
  project area is single and current.
- A task with a project/area conflict should abstain for `Areas` and request
  Kenji review instead of overwriting the relation.
- A task title alone is never enough for a high-confidence project relation.
- Plan Week and pinned planning pages can raise confidence when they mention
  the same project, artifact, or current focus.
- Generic research titles stay medium or low confidence unless the project
  context makes the route obvious.
- `Attention Required` can often be inferred safely:
  - `Foreground` for tasks requiring Kenji judgment, credentials, account setup,
    relationship work, or manual review.
  - `Delegateable` for bounded agent/repo/content execution.
  - `Background` for passive research, watch items, or low-urgency probes.
- Tags should be conservative; add only obvious tags such as `Content`,
  `Technical`, `Research`, `Admin`, or `Reel` when the title/body/project
  plainly supports them.

## Low-Confidence Telegram Rule

When any target field is low confidence or blocked by contradictory evidence:

1. Add the field to the proposal with `status: "needs_kenji"`.
2. Write a short message file using
   [templates/telegram-low-confidence.md](templates/telegram-low-confidence.md).
3. Send the message with the installed `telegram-message` skill/script when
   Telegram is configured.
4. If Telegram is not configured, keep the message file in the run artifact and
   report the fallback path.

Do not send secrets, raw private IDs, full Notion page dumps, or long reports.
Ask Kenji to fill the field or choose among 2-3 human-readable options.

## Output Artifacts

Every run writes:

```text
<artifact_dir>/
  proposal.json
  proposal.md
  low-confidence-telegram.md
  run-summary.md
```

Use [templates/proposal.json](templates/proposal.json) for the machine-readable
shape. The Markdown report should include:

- run window and mode
- connector/tool status
- candidates considered
- high-confidence patches
- medium-confidence suggestions
- low-confidence Telegram review requests
- abstentions and source gaps
- live-write receipts or readback failures when applicable

## Hard Gates

- Never write Notion from `dry-run`, `notify`, `weekly-preflight`, fixture, or
  connector-fallback mode.
- Never mutate task `Status`, delete pages, archive pages, publish, spend money,
  or create a hidden recurring runner from this skill.
- Never use raw Notion public API scripts as a fallback. Notion access must flow
  through `ntn` or fail closed.
- Never copy private Notion IDs, saved view URLs, page IDs, Telegram tokens, or
  credentials into tracked artifacts.
- Never run broad Notion data-source queries in scheduled automation. Missing
  private compact-property metadata is a source gap, not permission to fetch
  full pages.
- Never apply a medium- or low-confidence field in live mode.
- Never let a successful Telegram send count as a Notion write.

## Automation Prompt

Use [templates/codex-automation-prompt.md](templates/codex-automation-prompt.md)
for recurring every-N-hours runs. The automation should wake Codex, invoke this
skill in `notify` or `dry-run` mode first, and only use
`live-high-confidence` after the proposal/readback path has been reviewed.

## Weekly Strategy Handoff

When a weekly strategy automation asks for task hygiene, execute this skill in
`weekly-preflight` mode before that automation finalizes its context bundle.
Add the result under `Task Hygiene` with proposals, abstentions, Telegram
requests, and source gaps. Weekly strategy should consume the hygiene result as
evidence; it should not independently mutate Notion.

## Outcome Contract

The skill is complete for a run when:

- candidate tasks were fetched or a connector gap was recorded
- context sources were fetched or specific source gaps were recorded
- every missing field has a high/medium/low/abstain decision
- low-confidence fields produced a Telegram request or fallback message path
- live mode changed only high-confidence fields and recorded readback receipts
- the run summary points to the proposal artifact and any blockers
