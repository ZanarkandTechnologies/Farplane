---
name: pm
description: "Use the Notion Plan Week cache, tasks, projects, goals, and meeting notes to plan days, ingest commitments, and review priorities when asked for pm."
tier: 3
group: back-office
source: local
capability:
  kind: shortcut
template_uses:
  skill-template: "0.6.2"
  skill-surface-budget: "0.1.0"
allowed-tools: Read, Write, Glob, Grep, Bash
---

# PM

## Context

Use `pm` for:
- planning a day or week;
- processing meetings;
- sorting projects and ideas; and
- reviewing priorities and progress.

Each week, one Task named `Plan Week` stores the accumulated plan, decisions,
progress, and context for that week. Load this cache first. Query the other
Tasks, Projects, Goals, and meeting notes only when the request needs more
context or the cache has a gap that must be checked. Use the existing Notion
setup; do not add another planning system.

## Skill Signature
```text
pm(request, source_link?) -> grounded advice or verified PKMS updates
reads: private bindings, Plan Week first, then other relevant records as needed
does: reconciles current evidence with weekly intentions and requested action
writes: request-authorized Notion changes and private processing receipts only
returns: recommendation, source links, changed records, unresolved gaps
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Reconstruct the current week from canonical records.**
  `request + private bindings -> compact context | source gap`

  Rules:
  - Read `~/.codex/private/TOOLS.md` and
    `~/.codex/private/docs/notion.md` for source handles, property mappings, and
    current `ntn` recipes.
  - Reuse `run_ntn` in
    `../notion-task-field-fill/scripts/ntn_task_field_fill.py` when useful. Do
    not run its field-fill workflow merely to fetch data.
  - Launch credentialed commands through `farplane run` or Doppler. Bridge
    `NOTION_TOKEN` to `NOTION_API_TOKEN` only for the `ntn` subprocess.
  - Find the newest pinned page whose title begins with `Plan Week`. Order by
    `Act Time`, then by the date in the title. Fetch its full relevant body.
    Never use the example ID from the private docs.
  - Start with Plan Week. Fetch other Tasks, Goals, Projects, or meeting notes
    only when the request requires them or Plan Week lacks decisive context.
  - When additional records are needed, include relevant recent activity and
    older open commitments linked from Plan Week or Projects. Exclude terminal
    Done, Dropped, or Migrated projects, then deduplicate the result.
  - Treat planned dates and deadlines as different facts.
  - Use Asia/Kuala_Lumpur for time windows:
    - this week is Monday through Sunday, ending now for retrospective work;
    - past week is the previous seven days; and
    - next week begins the next Monday.
  - Use compact `filter_properties` queries and normalize records before
    reasoning. Paginate the requested scope or state that the result is
    incomplete.
  - Fetch the bodies of relevant meeting tasks, including Done meetings. Titles
    alone are not enough.

  Assert:
  - Context identifies window, selected Plan Week, coverage, and source gaps.
  - On invalid cached property metadata, read only that source's schema,
    repair the private mapping or omit a removed optional property, and retry
    compactly. Missing auth/required mappings block dependent calls; no broad
    page dump or MCP fallback.

- [ ] **N2 — Reconcile projects, rewards, and commitments.**
  `context -> evidence-backed priorities + missing decisions`

  Rules:
  - Task status determines whether work is complete. Plan Week holds reasoning
    and intentions.
  - Recent execution can make an `Info Dumped` project active. An old focus flag
    cannot do that by itself.
  - Keep these categories separate:
    - the operator's commitments;
    - other people's actions;
    - ideas; and
    - actions with uncertain ownership.
  - Preserve raw meeting notes. Add a source-linked interpretation without
    inventing missing speech or silently changing someone's identity.
  - Group projects that serve the same outcome.
  - Separate meaningful building from income work. Protect accepted build time
    without requiring every build project to make money immediately.
  - Judge cashflow work by credible payment and the full cost of selling,
    preparation, delivery, and support.
  - Count access, equipment, collaborators, buyers, and permissions only when
    the sources support them.
  - Leave unknown capacity and income targets unknown.

  Example: `Done teleoperation + stale project status -> execution exists ->
  next bounded folding test, not another teleoperation setup task`.
  Assert:
  - Recommendations distinguish facts, interpretations, and proposed goals.
  - Each new priority names its outcome and displacement; no invented deadline.

- [ ] **N3 — Turn the request into the smallest useful decision.**
  `priorities + request -> day plan | meeting deltas | weekly review`

  Rules:
  - For a day plan, choose one main outcome and a realistic amount of supporting
    work.
  - For meeting ingestion, derive concrete commitments and project context from
    the source.
  - For a weekly review, compare:
    - intended results with actual results;
    - expected rewards with actual rewards, when known; and
    - selected work with parked work.
  - Reuse the existing Plan Week sections, including cashflow. Do not impose a
    new template on every run.
  - Advice and audit requests return proposals without changing Notion.
  - Requests to edit, ingest, or save a plan in the weekly page authorize those
    bounded writes. Do not ask again.
  - Keep new goals, changed obligations, and unclear ownership as proposals
    until the operator accepts them.
  - Never send messages, publish, or spend.

  Assert:
  - The result answers the actual request and identifies missing decisive facts.
  - User-authored content, original expectations, and uncertainty survive edits.

- [ ] **N4 — Apply deltas once and verify their effects.**
  `authorized deltas + prior receipts -> verified updates | partial recovery`

  Rules:
  - Before creating a task, compare its source, action, owner, and project with
    existing rows. Reuse a matching row.
  - Resolve Project and Area from current relations and evidence. Do not infer a
    project from a title or overwrite a conflicting relation.
  - Re-read affected content before editing, then merge around concurrent
    changes.
  - Read back every write, including Plan Week, before claiming success.
  - For meeting ingestion, use
    `~/.codex/private/pm/processed/<source-id>.json`.
  - Record a SHA-256 fingerprint of a stable, ordered snapshot of the original
    note text and blocks. Exclude generated PM interpretations and receipts.
  - Store intended changes and per-action target/readback receipts privately
    before and during the update.
  - An unchanged fingerprint skips only identical actions that were already
    verified.
  - Reconcile newly accepted proposals and newly authorized changes against
    action receipts, even when the source is unchanged.
  - Reconcile changed notes instead of recreating actions blindly.
  - If a write is partial or uncertain, inspect its targets and resume only the
    missing changes.
  - Mark a source version complete only after every intended, authorized action
    is verified. Keep unresolved proposals explicit. Reading is not processing.

  Assert:
  - No processed stamp for advice, failed readback, or unapplied intended action.
  - Private IDs, source bodies, and receipts never enter tracked repo artifacts.
  - No new Notion schema/Processed checkbox is needed for this initial shortcut.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Common Examples

- `pm plan my day`: refresh the week, recognize completed work, choose today's
  outcome; edit Plan Week when asked to save the plan there.
- `pm ingest this meeting <link>`: interpret the source, reconcile/create
  commitments, update affected context and Plan Week, verify, record the version.
- `pm evaluate my week and plan next week`: compare outcomes with intentions,
  recommend next week's work/cashflow priorities, and save when requested.

The synthetic [golden trace](examples/golden.md) is calibration when changing
this skill or evaluating its behavior; it is not live user context.
## Gotchas

- A Done meeting can contain an unfinished commitment. Meeting completion is
  not action completion, and a guessed speaker is not an action owner.
- A date-heavy backlog is not a day plan. A potentially easy course can still
  consume a week in preparation; compare complete effort before displacing work.
- A connection to a data-center operator is not confirmed customer access or
  demand for a cabling robot. Keep the opportunity a hypothesis.

## Output

Return a compact answer containing:
- the decision or recommendation;
- source links;
- this week's concrete target, when relevant;
- what should change; and
- material unknowns.

For updates, list the records that were changed and verified, plus any partial
recovery. For advice, state that no pages changed. Do not claim complete
coverage when pagination or source-body fetching failed.
