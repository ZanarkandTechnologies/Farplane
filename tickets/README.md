# Tickets

Active work lives in `tickets/TASK-*/ticket.md`.

One source of truth per concern:

- frontmatter = queue state and execution state
- body = plan, references, evidence, and blockers
- `.harness/state/` = live runtime state
- `docs/` = durable knowledge after the ticket is done
- transcript = disposable context, not the canonical resume surface

## Canonical Layout

```text
tickets/
  TASK-0001/
    ticket.md
    artifacts/
  TASK-0002/
    ticket.md
  archive/
    TASK-0000/
      ticket.md
      artifacts/
  templates/
    ticket.md
```

No lane folders. No hand-maintained board file. The ticket itself is the board card.

## Lifecycle

1. create the ticket in `tickets/`
2. set `status: todo` or `status: review`
3. after approval, set `status: building`
4. when implementation and verification pass, set `phase: documenting`
5. write durable docs
6. move the ticket into `tickets/archive/` when it is no longer active, or set `status: done` briefly if you intentionally want a short-lived visible completion state before archiving

## Progress Surface Policy

- the ticket is the canonical durable progress surface
- `.harness/state/` is runtime-only and may track active claim/lane/session/verdict state
- transcripts are useful evidence but are not the canonical resume surface
- deliberate reset/resume requires the ticket to carry a clear `next_action`,
  `last_verification`, blockers, and evidence references

## Invocation Policy

A ticket is a work card, not a trigger. Creating a ticket, setting
`ready: true`, moving `status`, or adding `compute_target` does not start an
agent by itself.

Codexter work starts from an explicit invocation:

- local operator request, such as asking Codex to run `TASK-0123`
- operator-invoked `$ralph`, which serially selects one eligible ticket
- a recognized board comment or shared-board action after an external runner
  converts it into a `CodexterRunEnvelope`
- a future Codex Cloud, Symphony, or other runner payload

`ready` means the ticket is eligible once invoked. It does not mean Codexter
should watch the board and begin work automatically.

## Canonical Frontmatter

```yaml
---
ticket_id: TASK-0002
title: short title
phase: planning
status: review
owner: codex
claimed_by: agent-03  # optional active session claim alias
priority: medium
# optional compute override: local_shared, local_worktree, symphony, or codex_cloud
# compute_target: local_shared
depends_on: []
blocked_by: []
ready: false
approval_required: true
requires_qa: true
requires_demo: false
created_at: 2026-04-03T00:00:00Z
updated_at: 2026-04-03T00:00:00Z
next_action: await approval to set status: building
last_verification: none
---
```

## Field Meanings

- `phase`: `planning`, `building`, `documenting`, `complete`, `failed`
- `status`: `todo`, `review`, `building`, `blocked`, `done`, `failed`
- `owner`: broad work owner, not a live session id
- `claimed_by`: optional human-facing active claim alias for the current live session, such as `agent-03`
- `compute_target`: optional ticket-level compute override. Supported values
  are `local_shared`, `local_worktree`, `symphony`, and `codex_cloud`; future
  targets may be recorded but remain blocked unless the active workflow and
  adapter support them.
  - `local_shared` runs in the current checkout.
  - `local_worktree` requires a ticket runtime record under
    `.harness/state/tickets/TASK-XXXX.runtime.json`.
  - `symphony` and `codex_cloud` are future external-adapter targets and must
    stay blocked in local Codexter until those adapters exist.
- `depends_on`: structural prerequisites
- `blocked_by`: concrete ticket-ID blockers only
- `ready`: whether `next_action` can be executed now
- `approval_required`: explicit approval gate
- `requires_qa`: whether `$impl` must produce a passing QA phase before completion
- `requires_demo`: whether `$impl` must also produce a passing demo phase after QA
- `next_action`: the one authoritative next step
- `last_verification`: the one-line authoritative verification summary; keep
  detailed commands and artifacts in `Evidence`

For `$ralph`, the explicit invocation is the operator running `$ralph`. After
that, a ticket is selectable only when `ready: true`,
`approval_required: false`, `blocked_by: []`, `claimed_by:` is empty, and every
dependency is complete, archived, or explicitly waived in the ticket body.

For Codexter invocation, `bin/codexter_boards.py` is the canonical v1
BoardAdapter surface for reading filesystem tickets into normalized `WorkItem`
JSON. It is intentionally read-first: evidence links still belong in the
ticket `Evidence` section until a later ticket ships traceable writeback.
Future board adapters must satisfy
`docs/specs/board-adapter-conformance.md` before they become live ticket
sources.

## Invariants

- no `lane` field
- no `## Status` body block
- the H1 matches `ticket_id` and `title`
- do not store raw transport-level runtime ids such as `session_id` in ticket frontmatter
- do not set `status: building` while `approval_required: true`
- do not set `status: building` while `blocked_by` is non-empty
- `requires_demo: true` implies `requires_qa: true`
- do not invent a second machine-readable state block in the body

## Sizing Doctrine

- default ticket = the largest coherent capability an agent can build and prove in one strong pass
- CRUD workflows stay whole by default: schema, handlers, UI, validation, and proof belong together when they serve one operator workflow
- for complex systems, the first ticket should usually create one reusable proof surface plus one minimal end-to-end happy path
- split later work by shared proof surface, reusable foundation, risky migration, external blocker, or real service/runtime boundary
- do not split a pipeline into one ticket per internal step unless those steps are truly separate ownership or proof boundaries
- do not invent microservices during planning just to make the board look neat; split by service only when the runtime boundary is real

## Validator

Run:

```bash
python3 tickets/scripts/check_ticket_metadata.py
```

The validator treats `tickets/TASK-*/ticket.md` as canonical and still tolerates
legacy flat `tickets/TASK-*.md` files during migration.

## Body Contract

Keep the body short by default. The main job of a ticket body is to let a
developer or subagent understand the code shape without opening files first.

Default sections:

- `Summary`
- `Scope`
- `Plan`
- `Acceptance Criteria`
- `Verification`
- `Proof Contract`
- `Refs`
- `Evidence`
- `Blockers`

Optional sections only when they add signal:

- `Gap Analysis`
- `Diagram`
- `Agent Contract`
- `Autonomy Readiness`
- `Evidence Checklist`

The default `Plan` should answer four things:

1. what changes and why now
2. where the change lives: touched files, inspected files, signature deltas,
   and key type/data shapes when they matter
3. blast radius: callers, workflows, or systems that could break
4. how to verify: tests, checks, and strongest evidence to gather

For material, stateful, interface-heavy, or cross-boundary work, the `Plan`
should also show:

1. a compact `Type Sketch` naming the important structs, records, or payloads
2. one `Typed flow example` showing a representative object or payload evolving
   through the main path

Keep both compact. The point is to make typed data continuity legible in plain
text, not to dump full schemas into the ticket.

Use `Gap Analysis` when the work is about a missing, partial, parity-driven, or
otherwise under-specified feature and the main planning question is "what does
a production-grade version of this capability actually need?"

That section should answer:

1. what exists today and where it stops
2. what a credible production implementation usually includes
3. which gaps matter for this ticket now versus later
4. which comparable apps, repos, docs, or standards grounded that judgment

`Acceptance Criteria` should define what "done now" means in concrete,
measurable terms.

`Verification` should say how each criterion is measured: test passes, manual
checks, and required evidence.

`Proof Contract` should name the actual completion scoreboard for material
work:

1. metrics that can be measured mechanically, or `Metrics: none mechanical`
   when no honest metric exists
2. review rubric families, thresholds, and hard gates that the `review` skill
   must use
3. evidence artifacts required before completion can pass
4. optional autoresearch session path when repeated metric experiments are
   warranted

Keep full rubric bodies in `skills/review/references/` and full autoresearch
session files in the owning `autoresearch` artifacts. Tickets should carry the
handles, thresholds, and artifact obligations, not duplicate the specialist
contracts.

For UI-bearing, browser-driven, canvas/game, or otherwise agentically hard
tickets, add:

1. `Agent Contract`
2. `Evidence Checklist`

The `Agent Contract` should make QA fast and deterministic instead of leaving
browser navigation to improvisation. It should name:

1. `Open`
2. `Test hook`
3. `Stabilize`
4. `Inspect`
5. `Key screens/states`
6. `QA cookbook`
7. `Taste refs`
8. `Expected artifacts`
9. `Delegate with`

When the repo has `docs/bootstrap-brief.md` with `Agent Experience /
Testability` defaults, or a richer `Agent Testability Brief`, carry those
surfaces into the first relevant ticket instead of restating them from memory.
When the repo has `qa/cookbook/`, point the ticket at the matching workflow doc
or seed one during planning.

For tickets that may be drained by `$ralph` or run unattended, add `Autonomy
Readiness` and name:

1. human inputs/assets
2. credentials or external access
3. compute/runtime needs
4. tooling gaps
5. QA risks and which QA ring applies
6. human gates for plan review, QA review, deploy, spend, or destructive work
7. decisions the agent may make autonomously

If those answers are missing, keep the ticket gated instead of marking it ready
for the board-draining loop.

Do not duplicate the same idea across multiple headings. If a short summary and
the plan already explain the change, do not add more ceremony.

Use `Refs` for durable source URLs, specs, issues, websites, or comparable
examples instead of spreading links across extra note sections or duplicating
them in frontmatter.

## Evidence Artifacts

Store ticket artifacts under `tickets/TASK-XXXX/artifacts/`.

Examples:

- screenshots
- logs
- exported review JSON
- short clips
- seed or fixture notes that help reproduce the proof surface

Link those artifacts from the ticket `Evidence` section instead of preallocating
empty review-output fields in the template or repeating the artifact path under
`Verification`.

Canonical policy references:

- [context-and-handoff-policy.md](/Users/kenjipcx/coding-harness/Codexter/docs/specs/context-and-handoff-policy.md)
- [runtime-surface spec](/Users/kenjipcx/coding-harness/Codexter/docs/specs/runtime-surface.md)
