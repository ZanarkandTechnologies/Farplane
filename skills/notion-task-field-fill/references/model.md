# Notion Task Field Fill Model

This reference defines the field-fill proposal model. The owning workflow and
hard gates live in `SKILL.md`.

## Pipeline

```text
RunEnvelope
  -> TimeWindow
  -> CandidateTasks
  -> FillContext
  -> PerFieldEvidence
  -> TaskFieldProposal
  -> NotificationPlan
  -> OptionalTypedWrite
  -> ReadbackReceipt
```

## Normalized Task

```json
{
  "name": "string",
  "status": "Not started | In progress | Review | Failed | Done | other",
  "created_time": "ISO-8601 or null",
  "act_time": "YYYY-MM-DD or null",
  "task_due_date": "YYYY-MM-DD or null",
  "project": ["human-readable project names"],
  "project_relations": ["named handles or relation refs"],
  "areas": ["human-readable area names"],
  "description": "string",
  "attention_required": "Foreground | Background | Delegateable | null",
  "tags": ["string"],
  "pinned": true,
  "url": "notion page url or private placeholder",
  "context_gap": ["string"]
}
```

Do not keep formula URLs, counters, relation internals, or raw page dumps in the
proposal artifact.

## Fill Context

```json
{
  "window": {
    "start": "ISO-8601",
    "end": "ISO-8601",
    "timezone": "Asia/Kuala_Lumpur"
  },
  "plan_week": {
    "title": "string",
    "summary": "short excerpt or summary",
    "source_ref": "private page handle or local artifact"
  },
  "pinned_pages": [
    {
      "title": "string",
      "summary": "short excerpt or summary",
      "source_ref": "private page handle or local artifact"
    }
  ],
  "projects": [
    {
      "name": "string",
      "status": "string",
      "focus_this_week": "string",
      "context": "string",
      "tags": ["string"],
      "active_period": "string",
      "area": "string or null",
      "source_ref": "private handle"
    }
  ],
  "active_goals": [
    {
      "name": "string",
      "context": "string",
      "source_ref": "private handle"
    }
  ],
  "context_gaps": ["string"]
}
```

## Candidate Filter

Include a task when all are true:

- `Status` is not `Done`, unless the user explicitly asks to audit completed
  tasks.
- `created_time` or `Act Time` falls inside the run window, or the user asks
  for "this week".
- At least one target field is empty or obviously incomplete.
- The task is not a pure formula/link artifact row with no human-readable name.

For scheduled runs, use created time when available. If created time is missing,
fall back to `Act Time` and record `context_gap: "created_time_missing"`.

## Efficient Fetch Plan

The automation must not discover candidates by repeatedly querying broad Tasks
views. Use this order:

1. Resolve source handles and compact property IDs from private local context.
2. Run exactly one Tasks candidate query with:
   - `page_size <= 25`
   - `filter_properties` limited to `Name`, `Status`, `Act Time`,
     `Task Due Date`, `Project`, `Areas`, `Attention Required`, `Tags`,
     `Description`, `Pinned`, and `Goals`
   - filters for incomplete status, missing target field, and the narrowest
     available time signal
3. Normalize immediately, dedupe by page ID, and post-filter to the requested
   `created_time` window when the MCP filter cannot express created time.
4. If the normalized candidate list is empty, write empty run artifacts and stop
   without fetching Plan Week, Projects, Goals, or page bodies.
5. Fetch Projects only when at least one candidate has missing `Project` or
   `Areas`.
6. Fetch Goals only when candidate task or project relations make goals relevant.

Never paginate automatically in scheduled runs. Hitting the first page limit is
a source gap to record, not a reason to fetch a second full page.

### Wrong-Query Detection

After the Tasks query returns, check the first row's property names before doing
any reasoning. Allowed property names are exactly:

```text
Name, Status, Act Time, Task Due Date, Project, Areas,
Attention Required, Tags, Description, Pinned, Goals
```

If the response includes unrelated properties such as `Display`, `Days Left`,
`Blocked by`, `Skills Practiced`, `Location`, `Unblocked`, or formula/rollup
fields, the query did not honor compact mode. Stop the run, write
`context_gap: "unexpected_task_properties"`, and do not make more Notion calls.

Repeated `API_query_data_source` calls against Tasks before normalization are
also a wrong-query signal. Stop after the first compact candidate query unless
the run mode is an explicit weekly audit, not the scheduled six-hour automation.

## Proposal Shape

```json
{
  "task": {
    "name": "string",
    "url": "private-url-or-placeholder",
    "status": "string"
  },
  "field_proposals": {
    "Act Time": {
      "status": "proposed | suggested | needs_kenji | abstain | already_set",
      "value": "YYYY-MM-DD or null",
      "confidence": "high | medium | low | none",
      "reasons": ["string"],
      "source_refs": ["string"]
    }
  },
  "patch": {
    "Act Time": "YYYY-MM-DD"
  },
  "telegram_required": true,
  "abstentions": [
    {
      "field": "Areas",
      "reason": "project_area_conflict",
      "details": "Task has project A but title/body points to area B."
    }
  ]
}
```

Only `status: "proposed"` plus `confidence: "high"` enters `patch`.

## Field-Specific Rules

### Act Time

Default to today's Asia/Kuala_Lumpur date when:

- the field is empty
- the task content does not mention a different date, day, week, deadline, or
  scheduled event
- the task is inside the current run window

Use medium or low confidence when the task mentions fuzzy timing such as "this
week", "soon", "after call", or "when X replies".

### Project

High confidence requires at least one of:

- the task already has a project relation and only needs normalization
- the task title/body names a project exactly or via a known alias from private
  Notion context
- Plan Week or pinned context mentions the task artifact under one active
  project, and no competing project matches

Medium confidence is enough for a suggestion, not a write. Low confidence sends
Telegram.

### Areas

Prefer project inheritance. High confidence requires:

- one high-confidence project, and
- that project has one current area mapping, and
- the task content does not contradict it

If a task already has a project but the area evidence conflicts, abstain and
ask Kenji.

### Attention Required

Use:

- `Foreground`: Kenji judgment, credentials, accounts, relationship work,
  calls, meetings, manual review, personal decisions, or tasks whose blocker is
  human access.
- `Delegateable`: bounded coding, writing, Notion cleanup, content production,
  research synthesis, or artifact work that an agent can complete.
- `Background`: passive watch items, broad reading, low-urgency exploration, or
  context collection.

This field can be high confidence even when Project/Areas are low confidence.

### Tags

Add conservative tags only:

- `Technical`: code, agents, automation, infra, models, repos
- `Research`: model/company/product/source investigation
- `Content`: reels, posts, scripts, landing copy, visuals
- `Reel`: explicit reel/short-form video task
- `Admin`: account setup, credentials, operations, scheduling

Do not invent new tags during automation unless the user explicitly approves a
new tag.

## Dry-Run Lessons Captured

- `Vibecoding glasses`: project and area were high-confidence because active
  project context matched the task title.
- `Look into Nvidia's new vision model`: project remained low/medium because
  the title was generic research; this should become a Telegram review request
  unless Plan Week ties it to one project.
- `correction capture task`: project evidence was strong, but area evidence
  conflicted; infer fields independently and abstain on the conflicting field.
- `[Reel] Zap myself`: attention and tags were high-confidence even if project
  routing needed review.
- `Redo landing page`: attention and technical/content tags were inferable from
  the work shape.
- `Setup long running claw with account`: account setup pushed attention to
  `Foreground` because credentials and human account access may be needed.
