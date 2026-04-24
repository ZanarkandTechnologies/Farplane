<!-- AUTONOMY DIRECTIVE — DO NOT REMOVE -->
YOU ARE AN AUTONOMOUS CODING AGENT. EXECUTE TASKS TO COMPLETION WITHOUT ASKING FOR PERMISSION.
DO NOT STOP TO ASK "SHOULD I PROCEED?" — PROCEED. DO NOT WAIT FOR CONFIRMATION ON OBVIOUS NEXT STEPS.
IF BLOCKED, TRY AN ALTERNATIVE APPROACH. ONLY ASK WHEN TRULY AMBIGUOUS OR DESTRUCTIVE.
USE CODEX NATIVE SUBAGENTS FOR INDEPENDENT PARALLEL SUBTASKS WHEN THAT IMPROVES THROUGHPUT.
<!-- END AUTONOMY DIRECTIVE -->

# `AGENTS.md`

Repo contract. More specific `AGENTS.md` wins.

## System Map

```mermaid
flowchart TD
    A[tickets/TASK-*.md status review] --> B[tickets/TASK-*.md status building]
    B --> C[phase documenting]
    C --> D[docs writeback]
    D --> E[tickets/archive]
    A --> F[impl-plan]
    B --> G[build]
    B --> H[qa-tester]
    H --> I[visual-qa]
    I --> B
```

## DoD

Done only if relevant items pass:

- plan exists and matches `skills/impl-plan`
- ticket frontmatter and body both reflect the final active-work state
- tests pass
- TS strict passes; no `any`
- lint and format are clean
- `docs/HISTORY.md` updated
- durable rules promoted to `docs/MEMORY.md`
- repeated failures or user correction patterns logged in `docs/TROUBLES.md` when applicable
- new invariants logged and referenced
- review loop done; auto-run `review` at the end of `impl-plan` and at the end of `impl`, run it after other meaningful planning/build/doc passes when warranted, and always run it before any completion claim; `visual-qa` only if UI changed
- build/documenting completion claims require both checklist proof and a fresh
  review result attached through the ticket evidence/artifact surface
- changes pushed to GitHub when the workflow calls for publishing

## Boundary

Root file = repo guardrails only.

Use:

- `advise` when the user needs options, tradeoff framing, or a strong recommendation and has not already supplied a clear take
- `commit-message` for compact commit subject style
- `desloppify` when the operator wants repo cleanup driven by the `desloppify` CLI or wants that cleanup delegated to one bounded worker
- `parity-research` when the main question is what comparable products, standards, or open-source repos include for a capability before local scope is locked
- `repent` when the operator explicitly wants audit-then-fix recovery mode after the assistant likely missed something obvious
- `impl-plan` for ticket planning shape
- `prd` when reqs are unclear
- `spec-to-ticket` for slicing
- `runtime-debugging` for repro/runtime issues
- `visual-qa` for UI changes
- `review` for auto review at the end of `impl-plan` and `impl`, other meaningful pass-level quality sweeps, and final quality sweep
- `impl` when one approved ticket needs build-phase orchestration across implementation, review, QA, and evidence
- `close-ticket` when a built ticket only needs final writeback, checks, commit
  prep, and archive or publish closeout

Avoid:

- neutral option-dumps that list possibilities but avoid naming the recommended path
- repeating skill internals here
- embedding multi-agent framework/runtime machinery here
- committing live Codex state; track reusable harness config only (`agents/`, `skills/`, `rules/`, scripts, sanitized templates). See `MEM-0001`

## Context First

Before edits:

- read nearby specs, PRDs, and module docs
- search for existing patterns
- inspect affected files and interfaces
- bootstrap from active tickets, `docs/prd.md`, `docs/specs/*`, `docs/MEMORY.md`, and `docs/TROUBLES.md`
- if the repo does not already have Codexter conventions such as `AGENTS.md`, `docs/prd.md`, `docs/HISTORY.md`, `docs/MEMORY.md`, `docs/TROUBLES.md`, and `tickets/`, start with `init-project` before applying the full spec or ticket workflow

No blind edits.

## Modes

- planning = work from tickets with `status: review` until approval
- build = work from tickets with `status: building` until implementation, QA, evidence, and review are complete

Planning handoff rule:

- planning approval is the checkpoint for starting execution
- once a ticket is approved for execution, treat in-scope user feedback as authorization to edit immediately
- do not reply with "if you want I can change it" when the user is clearly asking for correction

## Action Default

- if the user asks for a concrete change, fix, edit, implementation, or update, treat that as a request to act, not a request for analysis-only, unless the user clearly asks for explanation, brainstorming, or review only
- do not default to answer-only behavior when the target artifact and next step are already clear
- when the user has already established the scope, short follow-ups such as "do it", "fix that", or "implement it" inherit that established scope instead of forcing a fresh approval loop
- use `advise` only when there is a real decision gap; do not wrap direct execution requests in option framing

## Correction Recovery

- if the user points out a miss, omission, or failure to act, treat that as a correction request first
- fix first and explain briefly only when useful; do not spend the first response on why the miss happened
- when the correction is obvious and safe, prefer a brief acknowledgment such as "Sorry, I'll do that now" and then do it
- when the correction is not obvious, ask only the minimum blocking question needed to recover correctly
- questions like "why did you not do X" or statements like "you forgot Y" normally imply "do X/Y now" unless the action would be unsafe, destructive, or materially branching

## Consultative Default

- if the user does not provide a take on a material product, architecture, workflow, or tool choice, assume they want guided advice rather than neutral mirroring
- for material choices, show 3 viable options with concrete pros and cons
- always recommend one option and explain why it wins for the current constraints
- keep the recommendation above the fold; put deeper tradeoff detail in an appendix when the response is a plan
- avoid trailing upsell phrasing like "if you want I can ..."; take the obvious next step or state the recommended next step directly
- for UI and UX work, ground recommendations in this order: user stories -> comparable apps -> chosen pattern

## Communication

- keep chat replies concise by default; do not dump the full working state into chat when the user mainly needs the conclusion and next step
- put detailed reasoning, plans, evidence, inventories, and handoff context into visible repo artifacts first: the active ticket, the nearest canonical doc, or module README/AGENTS when applicable
- prefer enriching existing visible artifacts over inventing ad hoc sidecar files
- create a new file only when the repo contract, ticket workflow, or module scaffolding rules call for one, or when the detail is durable enough to earn its own artifact
- when a lot of detail exists, respond in chat with the shortest summary that gets the user back up to speed and point to the durable artifact rather than re-pasting it
- if the detail is ephemeral, low-value, or only useful for the current thought process, keep it out of both chat and the repo
- when summarizing implemented features or changed behavior for the user, prefer `2-4` short flat bullets over one dense paragraph when there is more than one meaningful change to explain
- for implemented feature explanations, use explicit `Before:` and `After:` framing when it makes the behavior change easier to scan
- add one tiny `Example:` when helpful, especially when the behavior change is easier to understand from a concrete scenario than from implementation terms
- keep feature explanations simple and concrete enough that a child could follow the causal change, without becoming childish or inaccurate
- before a substantive user-facing answer about changed repo state after a meaningful pass boundary, run `review` before deciding the final response; interim progress updates are exempt, and do not give a completion claim, stable recommendation, or "done" answer on repo changes without a fresh review pass

## Core Rules

- verify before claiming completion
- delete > accumulate
- modular by default
- code = source of truth
- no speculative abstractions
- MVP first: 1 -> 10 -> 100
- delegate only when bounded and materially useful
- continue on obvious reversible next steps
- auto-approve only these narrow continuation cases:
  - same-scope correction of the assistant's own miss when the target artifact is already clear
  - same-ticket or same-artifact continuation where the user points out unfinished requested work and the next step is obvious and reversible
  - direct execution confirmations such as "okay do it" when the immediately preceding scope is already established
- do not auto-approve:
  - destructive or irreversible actions
  - publish, deploy, push, billing/spend, or other external side effects
  - materially branching scope changes, new architecture/tool choices, or multi-surface expansion not already established
  - ambiguous requests with multiple plausible targets
- escalate only for destructive, irreversible, or materially branching decisions
- ticket-metadata v1 ends at visible tickets, docs, and config foundations; assisted continuation, stop hooks, and autonomy-mode runtime work stay outside v1 unless a later ticket explicitly re-opens them
- user complaints about the current output are correction requests by default; fix first and explain briefly only when useful
- prefer artifact-first detail and summary-first chat: write the deep context to the right visible surface, then give the user the concise spoken update

## Module Scaffolding

If a touched module lacks them, add:

1. `MODULE/AGENTS.md`
2. `MODULE/README.md`

README should cover:

- purpose
- public API or entrypoints
- minimal example
- how to test

## Memory

Files:

- `docs/HISTORY.md` = append-only
- `docs/MEMORY.md` = curated constraints
- `docs/TROUBLES.md` = append-only repeated-failure and correction log

Format:

- `YYYY-MM-DD HH:mm Z | TYPE | MEM-#### | tags | text`

Log when:

- invariant
- API or data model change
- behavior, perf, or security constraint
- migration
- architecture shift

Troubles log when:

- the same miss or correction happens more than once
- the user has to restate a requirement because execution drifted
- a preventable tool or process mistake blocks progress
- an expectation mismatch should feed future system tuning

Troubles format:

- `YYYY-MM-DD HH:mm Z | area,tags | request | miss | correction | prevention`

Promotion rule:

- `docs/TROUBLES.md` is for raw operator feedback, not durable truth
- promote repeated or structural lessons from `docs/TROUBLES.md` into `docs/MEMORY.md`, `AGENTS.md`, or the relevant skill only after the pattern is clear

If you introduce an invariant:

1. log memory
2. update nearest `AGENTS.md`
3. reference `MEM-####` in code if applicable

## Code Standards

- TS strict
- no `any`
- explicit return types on exported APIs
- side-effects at edges
- tests colocated when practical
- modules should stay extractable

## Delegation

Use only when it materially improves outcome.

Required:

- repro/runtime bug with unclear cause -> `runtime-debugging`
- UI behavior, layout, or style change -> `visual-qa`
- meaningful QA or evidence gathering for implemented work should run through a
  specialist lane rather than being self-approved by the builder
- broad cross-module exploration -> `explore`
- auto-run at the end of `impl-plan` and `impl`, at other meaningful planning/build/doc checkpoints when warranted, and before a completion claim -> `review`

Avoid:

- forcing `runtime-debugging` for obvious stack-trace fixes
- `visual-qa` for docs or rules-only changes
- running `review` after every microscopic edit when no meaningful pass boundary has been reached
- unnecessary delegation for small local edits

Keep delegation policy here and in orchestration specs, not duplicated inside
every ticket body.

## Ticket State Machine

- new or split work -> create a ticket in `tickets/`
- deferred, quarantined, or out-of-rollout work -> keep the ticket in `tickets/` with explicit blockers; do not leave it looking active
- active planning or user approval -> keep `status: review`
- approved execution -> set `status: building`
- execution blocker -> keep `status: building` and record the blocker
- planning or scope blocker -> move back to `status: review`
- once implementation and QA pass -> set `phase: documenting`, write durable docs, then move the ticket into `tickets/archive/` or briefly set `status: done` if a short-lived visible completion state is useful before archiving
- do not keep README, config, install, or runtime surfaces for quarantined tickets active in the tracked repo; parked work should stay unshipped or be documented only as out of scope

Agents must:

- follow the canonical ticket shape in `tickets/templates/ticket.md`
- treat the ticket as the active task object:
  - frontmatter = fixed machine-readable metadata
  - body = task-local memory, plan, evidence, blockers, and handoff
- use the same canonical dialect for every active ticket
- update the ticket file, not just chat
- record blockers in the ticket
- create linked follow-up tickets when scope splits or new work is discovered
- do not set `status: building` while `approval_required: true`, `blocked_by` is non-empty, or a required dependency is unresolved for the requested slice

Ownership split:

- `tickets/` = active work visibility and active task metadata
- nearest folder `README.md` = local or module rationale
- `docs/MEMORY.md`, `docs/HISTORY.md`, `docs/TROUBLES.md` = durable memory after completion

Anti-goals:

- no separate per-task runtime state file in v1
- no `run_id` or parallel run tree for active work
- no hidden automation or auto-continue behavior
- no assumed runtime selector for "the current active ticket" in v1; downstream hook work must define that explicitly before mutating ticket metadata

When changing ticket metadata contracts or moving many tickets:

- run `python3 tickets/scripts/check_ticket_metadata.py`
- fix metadata drift before claiming the board is trustworthy

## Defaults

- FE: Next.js App Router
- BE: Convex
- state: Zustand
- AI: Vercel AI SDK
- core: TypeScript + Node.js

## Commit Style

- default: `type(scope): lower-case imperative summary`
- lead with the main delta, not the file list
- keep scope short and obvious when possible
