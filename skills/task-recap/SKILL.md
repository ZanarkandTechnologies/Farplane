---
name: task-recap
description: "Turn a paused Codex task, durable artifacts, and available thread context into a grouped quick recap with source-linked context, deltas, problems, gaps, and a safe next action."
tier: 3
group: operations
source: local
capability:
  kind: shortcut
template_uses:
  skill-template: "0.4.0"
  skill-surface-budget: "0.1.0"
allowed-tools: Read, Glob, Grep, Bash
---

# Task Recap

## Context

Use this when an operator returns to a paused Codex task and needs enough
grounded context to reply, decide, or hand off safely. It is a read-only
recovery workflow: it reconstructs context but never edits the task, sends a
message, or resumes execution.

Treat durable task state as primary: `ticket.md`, then `program.md`, the latest
80 lines of `progress.md`, linked evidence, and task-scoped source changes.
Use the accessible thread only as supplementary context. If a source is absent,
stale, or conflicts with another source, name that condition instead of filling
the gap from memory.

## Skill Signature

```text
task_recap(task_ref?, focus?) -> quick_recap + full_context? + source_ledger + next_action
state: reads(ticket, program, progress, artifacts, scoped diff/status, available thread context); writes(none)
owns: one source-linked, layered resumption brief
gates: task_boundary_bound_or_source_gap; grouped_quick_card_first; conflicts_labeled; claims_trace_to_sources; no_execution
routes: direct-answer | goal-advisor | review
fails: transcript-only certainty; fabricated task history; completion claim from stale state; unrelated worktree noise as task evidence
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind one task boundary and source ledger.
  - [ ] Use an explicit ticket, task/thread reference, or supplied paths; otherwise bind the current task only when it is unambiguous.
  - [ ] If no durable task source is accessible, return a bounded source-gap recap that names the exact missing ticket, artifact, or thread reference.
- [ ] 2. Recover the most authoritative task state.
  - [ ] Read `ticket.md`, `program.md` when present, the latest 80 `progress.md` lines, declared artifacts, and only relevant diff/status evidence.
  - [ ] When the caller or eval fixture supplies a readable path, open it before
    calling it a source gap; a known path is not missing context merely because
    its contents have not yet been read.
  - [ ] For a worktree capture, name the task-owned changed path or paths and
    any explicitly excluded unrelated paths plus its exact capture timestamp;
    do not use “scoped” as a substitute for the boundary.
  - [ ] Read available thread context only to recover the latest user ask, decisions, and unresolved discussion that the durable sources do not cover.
- [ ] 3. Reconcile history before narrating it.
  - [ ] Separate observed facts, source-backed decisions, and clearly marked inferences.
  - [ ] Surface conflicts between ticket state, progress, evidence, and scoped worktree state; do not promote a checkbox or a transcript claim into proof.
- [ ] 4. Build the layered recovery brief.
  - [ ] Put the grouped quick card immediately after any governing response
    ledger, before all recap prose or detail: `Now`, `Delta`, and `Risks &
    action`. Keep `Before`, `After`, and an indented `Example` together in
    `Delta`.
  - [ ] For a full recap, or when a conflict or source gap makes the card
    insufficient, follow it with a dated chronological timeline; each material
    entry includes its source label, such as `[progress.md]` or
    `[artifact: QA receipt]`.
  - [ ] A material proof conflict—implemented or unit-tested work paired with
    missing runtime proof—always requires the full detail layer, even for a
    status-only request.
  - [ ] In full mode, name the latest user question or decision explicitly and
    preserve each dated material event as its own sourced timeline entry. Use a
    full `YYYY-MM-DD HH:MM` date when available; never collapse several
    attempts or decisions into one summary bullet or abbreviate later events to
    time-only entries. Repeat a dated latest-question event in the timeline as
    well as naming it in `Latest user context`.
  - [ ] In a full detail ledger, copy literal supplied or task-relative source
    paths (for example, `tickets/TASK-0434/ticket.md`), not bare labels such as
    `ticket.md`, `ticket`, or `progress`. Put every path on its own bullet; do
    not use brace expansion, comma grouping, or “supplied” shorthand.
  - [ ] Trace every material delta as `Before`, `After`, and `Example`; never
    omit them from the quick card when the records support a material change.
  - [ ] In full mode, include a distinct `Problems and attempts` section. For
    each material problem, record the complete `symptom -> attempt -> observed
    result -> disposition -> remaining impact` chain, including why an attempt
    was rejected; do not leave this only implicit in the timeline or “do not
    repeat” line.
  - [ ] Preserve accepted and rejected decisions, the latest user ask, open questions, and response-ready context.
- [ ] 5. Finish with bounded evidence and routing.
  - [ ] Apply the first-load Todo List guardrails and list sources used, conflicts, and coverage gaps.
  - [ ] Return one safest next action or reply posture as the final line after
    a full recap's detail ledger; state an operator-visible Goal-compilation
    handoff only when the task is an active Goal and execution is requested.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

After any governing response ledger, begin with this grouped quick card,
collapsing only genuinely empty lines and never hiding gaps:

```md
## <TASK-ID or task label> — <state / confidence>

### Now
- **Reply now:** <safe reply posture>
- **Goal:** <operator's immediate reply or decision objective; task success condition>
- **Since you left:** <most decision-relevant update>

### Delta
- **Before:** <prior behavior or state> [source]
- **After:** <current behavior or state> [source]
  - **Example:** <representative input -> observed outcome> [source]

### Risks & action
- **Problems:** <important symptom, attempted path, and disposition> [source]
- **Open:** <smallest unresolved loop or conflict> [source]
  - **Need from you:** <decision, source, or `None`>
  - **Evidence limit:** <for example: “2026-08-08 worktree capture; historical,
    not live state.”>

<sub>Sources: <compact source list; for every worktree capture name the
task-owned path(s), excluded unrelated path(s), exact capture timestamp, and
that it is historical—not live state; include any other freshness limit or
gap></sub>
```

When the operator asks for a full recap, or the card contains a material
conflict or source gap, append this detail layer:

```text
### Details
Latest user context: <latest question, decision, or exact reply need> [source]
Timeline and decisions:
  - <YYYY-MM-DD HH:MM> <one fact or decision> [source]
Problems and attempts:
  - symptom -> attempt -> observed result -> disposition -> remaining impact [source]
Evidence and conflicts:
Open loops and safe next action:
Source ledger and gaps:
  - `<exact supplied or task-relative path>` — <what it supports / freshness>
  - `<next exact path>` — <what it supports / freshness>
Safe next: <one reply posture, decision, or source request>
```

Positive example: “The implementation exists, but the latest runtime receipt
failed. Put the customer-safe reply in `Now`, the implementation delta in
`Delta`, the rejected workaround and missing receipt in `Risks & action`, then
append the full source-labeled timeline when the operator asks what happened.”

## Gotchas

- A full recap is not a transcript dump: cite the smallest source set that
  supports each material claim.
- In full mode, do not summarize away the reason for reopening: name the latest
  question or decision, keep one dated sourced bullet per material event, and
  list literal task-relative or supplied paths in the detail-layer ledger,
  rather than only basenames such as `ticket` or `progress`.
- A material proof conflict always earns the full detail layer. Do not group
  path entries with brace syntax, commas, or “supplied source” shorthand.
- A timeline records order; `Problems and attempts` records causal outcome.
  Full mode needs both whenever a workaround, fix, or verification attempt is
  material.
- “Goal” begins with the operator's immediate reply or decision need, then
  states the underlying task success condition when it helps the next action.
- A quick card is not a status-only summary: keep the source-backed
  `Before` / `After` / indented `Example` visibly grouped in `Delta`.
- A supplied readable file path is evidence to inspect, not a source gap. Mark
  a gap only after the expected source is unavailable, unreadable, or too stale
  to support the claim.
- “Scoped worktree” is not enough: identify the relevant file path and every
  known excluded path, state its exact capture timestamp, then say it is
  historical rather than live.
- A timeline is a chronological reconstruction, not a topical problem list;
  include dates when records provide them and label each material event's source.
- A task can be partially implemented and still blocked; distinguish code,
  check, review, and user-acceptance state.
- A captured `git status` is historical, not live state: name its timestamp and
  this limit explicitly. Do not treat unrelated changes as task work or a past
  snapshot as current state.

## Reference Map

- [Ticket and Goal Packet resume contract](../../tickets/README.md) — read when
  a ticket or Goal Packet is available.
- the first-load Todo List guardrails — read before returning the recap and reapply
  when the recap will support a material decision.
- [Behavior eval cases](evals/evals.json) — use to test source coverage,
  conflicts, problem history, gaps, and worktree scope.

## Output

- `quick_recap`: a grouped, response-ready card with `Now`, `Delta`, and
  `Risks & action`.
- `full_context`: the appended, source-labeled detail layer when requested or
  needed to make a safe response.
- `source_ledger`: sources used, conflicts, freshness limits, and gaps.
- `next_action`: one safe reply posture, decision, or explicit source request.
