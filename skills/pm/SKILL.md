---
name: pm
description: "Use for \"plan my day\", \"plan my week\", \"ingest this meeting\" or \"tidy my Notion tasks\": a plan grounded in Plan Week, verified task updates, or safe field fills."
department: leadership
source: local
capability:
  kind: shortcut
template_uses:
  skill-template: "0.6.5"
  skill-surface-budget: "0.1.0"
allowed-tools: Read, Write, Glob, Grep, Bash
---

# PM

## Context

Use `pm` to plan a day or week, process meetings, sort projects and ideas,
review priorities and progress, or tidy incomplete Notion Tasks (`hygiene`).
Each week one Task named `Plan Week` stores the accumulated plan, decisions,
progress, and context. Load it first; query other Tasks, Projects, Goals, and
meeting notes only when the request needs them or the cache has a gap. Use the
existing Notion setup; do not add another planning system.

## Skill Signature

```text
pm(request, mode?: plan | ingest | review | hygiene, source_link?)
  -> grounded advice | verified PKMS updates | hygiene proposal + receipts
reads: private bindings, Plan Week first, then other relevant records as needed
does: reconciles current evidence with weekly intentions and requested action
writes: request-authorized Notion changes and private processing receipts only
returns: recommendation, source links, changed records, unresolved gaps
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Reconstruct the current week from canonical records.**
  `request + private bindings -> compact context | source gap`

  Rule: Read `~/.codex/private/TOOLS.md` and `~/.codex/private/docs/notion.md` for
  handles, property mappings, and current `ntn` recipes. Reuse `run_ntn` in
  `scripts/ntn_task_field_fill.py` to fetch data.
  - Launch credentialed commands through `farplane run` or Doppler. Bridge
    `NOTION_TOKEN` to `NOTION_API_TOKEN` only for the `ntn` subprocess.
  - Find the newest pinned page whose title begins with `Plan Week`, ordered by
    `Act Time`, then the title date. Never use the example ID from private docs.
  - When more records are needed, include recent activity and older open
    commitments linked from Plan Week or Projects; exclude Done, Dropped, or
    Migrated projects and deduplicate.
  - Planned dates and deadlines are different facts. Use Asia/Kuala_Lumpur:
    this week is Monday to Sunday (ending now for retrospectives), past week
    the previous seven days, next week from the next Monday.
  - Use compact `filter_properties` queries, normalize before reasoning, and
    paginate the requested scope or say it is incomplete. Fetch the bodies of
    relevant meeting tasks, including Done ones; titles are not enough.

  Assert:
  - Context identifies window, selected Plan Week, coverage, and source gaps.
  - On invalid cached property metadata, read only that source's schema,
    repair the private mapping or omit a removed optional property, and retry
    compactly. Missing auth/required mappings block dependent calls; no broad
    page dump or MCP fallback.

- [ ] **N2 — Reconcile projects, rewards, and commitments.**
  `context -> evidence-backed priorities + missing decisions`

  Rule: Task status decides completion; Plan Week holds reasoning and intentions.
  Recent execution can make an `Info Dumped` project active; an old focus
  flag cannot.
  - Keep separate: the operator's commitments, other people's actions, ideas,
    and actions with uncertain ownership. Preserve raw meeting notes; add a
    source-linked interpretation without inventing speech or identity.
  - Group projects serving one outcome. Separate building from income work and
    protect accepted build time. Judge cashflow work by credible payment and
    the full cost of selling, preparing, delivering, and supporting it.
  - Count access, equipment, collaborators, buyers, and permissions only when
    sources support them; leave unknown capacity and income targets unknown.

  Example: `Done teleoperation + stale project status -> execution exists ->
  next bounded folding test, not another teleoperation setup task`.
  Assert:
  - Recommendations distinguish facts, interpretations, and proposed goals.
  - Each new priority names its outcome and displacement; no invented deadline.

- [ ] **N3 — Turn the request into the smallest useful decision.**
  `priorities + request -> day plan | meeting deltas | weekly review`

  Rule: Day plan: one main outcome plus realistic supporting work; plan or
  negotiate interactively with [plan-day](references/plan-day.md) or
  [plan-week](references/plan-week.md).
  - Meeting ingestion derives concrete commitments and project context.
  - Weekly review compares intended with actual results, expected with actual
    rewards when known, and selected with parked work. Reuse existing Plan Week
    sections, including cashflow; impose no new template.
  - Advice and audit requests return proposals without changing Notion.
    Requests to edit, ingest, or save a plan authorize those bounded writes.
  - Keep new goals, changed obligations, and unclear ownership as proposals
    until the operator accepts them. Never send messages, publish, or spend.

  Assert:
  - The result answers the actual request and names missing decisive facts.
  - User-authored content, original expectations, and uncertainty survive edits.

- [ ] **N4 — Apply deltas once and verify their effects.**
  `authorized deltas + prior receipts -> verified updates | partial recovery`

  Rule: Before creating a task, compare source, action, owner, and project with
  existing rows and reuse a match. Resolve Project and Area from current
  relations; never infer a project from a title or overwrite a conflict.
  - Re-read affected content before editing, merge around concurrent changes,
    and read back every write, including Plan Week, before claiming success.
  - Meeting ingestion records `~/.codex/private/pm/processed/<source-id>.json`
    with a SHA-256 fingerprint of the ordered original note text and blocks
    (excluding PM interpretations), intended changes, and per-action
    target/readback receipts, written before and during the update.
  - An unchanged fingerprint skips only identical verified actions; reconcile
    newly accepted or authorized changes and changed notes instead of
    recreating actions. Resume only missing changes after a partial write.
  - Mark a source version complete only after every intended, authorized action
    is verified. Reading is not processing.

  Assert:
  - No processed stamp for advice, failed readback, or unapplied intended action.
  - Private IDs, source bodies, and receipts never enter tracked repo artifacts.

- [ ] **N5 — hygiene: fill missing Task fields only where evidence agrees.**
  `task window + Plan Week/Projects/Goals -> per-field proposal + typed patches | abstain`

  Rule: Default `dry-run`. Run one compact `ntn` Tasks query (bounded page
  size, `filter_properties`, no repeated equivalent query), normalize rows,
  then decide `Act Time`, `Project`, `Areas`, `Attention Required`, and `Tags`
  independently. Write only high-confidence typed patches in
  `live-high-confidence`, and read each back; abstain on conflicting evidence
  and queue it for Telegram or local review. Never mutate `Status`. Load
  [hygiene](references/hygiene.md) for modes, budgets, and artifacts, and
  [model](references/hygiene-model.md) plus
  [confidence](references/hygiene-confidence.md) when deciding fields.

  Example: `task names a project but its Area relation points elsewhere ->
  propose Project (high), abstain on Areas, ask for review`.

  Assert:
  - Unexpected Task properties or a failed compact query stop the run with a
    named `context_gap`; no broad page dump or MCP fallback.
  - Artifacts under `.farplane/state/pm/hygiene/runs/<run-id>/` name counts,
    per-field confidence, review requests, and readback receipts.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Common Examples

- `pm plan my day`: refresh the week, recognize completed work, choose today's
  outcome; edit Plan Week when asked to save the plan there.
- `pm ingest this meeting <link>`: interpret the source, reconcile/create
  commitments, update affected context and Plan Week, verify, record the version.
- `pm evaluate my week and plan next week`: compare outcomes with intentions,
  recommend next week's work/cashflow priorities, and save when requested.
- `pm tidy the tasks I added this week`: hygiene dry-run over this week's
  incomplete Tasks with a proposal and review requests.

The synthetic [golden trace](examples/golden.md) is calibration when changing
this skill or evaluating its behavior; it is not live user context.

## Gotchas

- A Done meeting can contain an unfinished commitment. Meeting completion is
  not action completion, and a guessed speaker is not an action owner.
- A date-heavy backlog is not a day plan. A potentially easy course can still
  consume a week in preparation; compare complete effort before displacing work.
- A connection to a data-center operator is not confirmed customer access or
  demand for a cabling robot. Keep the opportunity a hypothesis.
- A medium-confidence field written "because it is probably right" is a silent
  wrong fact in the planner; propose it instead.

## Output

Return the decision or recommendation, source links, this week's concrete
target when relevant, what should change, and material unknowns. For updates,
list records changed and verified plus any partial recovery; for advice, state
that no pages changed. Hygiene returns artifact paths, candidate and proposal
counts, per-field confidence, review requests, readback receipts, and
`provider_effects: none` outside `live-high-confidence`. Never claim complete
coverage when pagination or source-body fetching failed.
