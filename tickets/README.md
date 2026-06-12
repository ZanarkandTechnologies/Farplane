# Tickets

Active work lives in `tickets/TASK-*/ticket.md`.

One source of truth per concern:

- frontmatter = queue state and execution state
- body = plan, references, evidence, and blockers
- `.farplane/state/` = live runtime state
- `docs/` = durable knowledge after the ticket is done
- transcript = disposable context, not the canonical resume surface

## Canonical Layout

```text
tickets/
  TASK-0001/
    ticket.md
    program.md      # optional Goal Packet loop configuration
    progress.md     # optional Goal Packet append-only loop log
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
- for material native Goal work, the ticket should carry or point to a Goal
  Packet: `ticket.md` for the task contract, `program.md` for loop
  configuration, and `progress.md` for append-only turn logs
- `.farplane/state/` is runtime-only and may track active claim/lane/session/verdict state
- transcripts are useful evidence but are not the canonical resume surface
- deliberate reset/resume requires the ticket to carry a clear `next_action`,
  `last_verification`, blockers, and evidence references

## Goal Packets

Use a Goal Packet when native Goal mode is used for material, long-running,
feedback-heavy, rollout, heartbeat, business-loop, or skill-improvement work.

```text
goal_loop(ticket.md, program.md, progress.md, trigger)
  -> next_turn + evidence + drift_verdict + state_delta
```

- `ticket.md` owns objective, scope, acceptance criteria, proof, blockers, and
  current next action.
- `program.md` owns trigger mode, metric or feedback provider, budget,
  after-each-turn routine, drift policy, heartbeat policy, and stop conditions.
- `progress.md` owns compact append-only turn logs, evidence pointers,
  feedback samples, drift verdicts, blockers, and next actions.

Use `tickets/templates/goal-loop/program.md` and
`tickets/templates/goal-loop/progress.md` when scaffolding these files. See
`docs/specs/goal-loop-contract.md` for the full contract.

## Invocation Policy

A ticket is a work card, not a trigger. Creating a ticket, setting
`ready: true`, moving `status`, or adding `compute_target` does not start an
agent by itself.

Farplane work starts from an explicit invocation:

- local operator request, such as asking Codex to run `TASK-0123`
- operator-invoked `$ralph`, which serially selects one eligible ticket
- a recognized board comment or shared-board action after an external runner
  converts it into a `FarplaneRunEnvelope`
- a future Codex Cloud, Symphony, or other runner payload

`ready` means the ticket is eligible once invoked. It does not mean Farplane
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
    `.farplane/state/tickets/TASK-XXXX.runtime.json`.
  - `symphony` and `codex_cloud` are future external-adapter targets and must
    stay blocked in local Farplane until those adapters exist.
- `depends_on`: structural prerequisites
- `blocked_by`: concrete ticket-ID blockers only
- `ready`: whether `next_action` can be executed now
- `approval_required`: explicit approval gate
- `requires_qa`: whether `$impl` must produce a passing QA phase before completion
- `requires_demo`: whether `$impl` must also produce a passing demo phase after QA
- `next_action`: the one authoritative next step
- `last_verification`: the one-line authoritative verification summary; keep
  detailed commands and artifacts in `Links`, `State`, `progress.md`, or
  ticket-scoped artifacts

For `$ralph`, the explicit invocation is the operator running `$ralph`. After
that, a ticket is selectable only when `ready: true`,
`approval_required: false`, `blocked_by: []`, `claimed_by:` is empty, and every
dependency is complete, archived, or explicitly waived in the ticket body.

For Farplane invocation, `bin/farplane_boards.py` is the canonical v1
BoardAdapter surface for reading filesystem tickets into normalized `WorkItem`
JSON. It is intentionally read-first: evidence links still belong in the
ticket `Links` or `State` section until a later ticket ships traceable writeback.
Future board adapters must satisfy
`docs/specs/invocation-and-adapters.md` before they become live ticket
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
flat `tickets/TASK-*.md` files only as archived pre-directory ticket history.

## Body Contract

Keep the body short by default. The main job of a ticket body is to let a
developer or subagent understand the task contract, variable files, operations,
and proof without opening every file first.

Default sections:

- `Summary`
- `Scope`
- `Delta`
- `Program`
- `Map`
- `Done / Proof`
- `State`
- `Links`
- `Notes`

Optional sections only when they add signal:

- `Gap Analysis`
- `Agent Contract`
- `Run Hints`
- `Goal Packet`

The ticket is a compact task program over files and skills:

```text
task_program(vars, operations, proof) -> artifact + evidence + state_delta
```

Use `Delta` to answer:

1. what changes
2. before versus after behavior
3. why now
4. first-principles basis: objective, need, assumptions, root cause,
   constraints, first viable slice, proof/falsification, tradeoff, and
   non-goals when material

Use `Program` for the execution sketch:

```text
vars:
  target =
  owner =

program:
  ground(vars) -> current_state
  change(current_state) -> artifact_delta
  verify(done_when, proof) -> evidence
```

This replaces long prose build plans for normal tickets. Create a separate
`plan.md` only when the build plan is long, deeply technical, likely to change
independently, or too large to keep the ticket readable.

Use `Map` for file grounding and examples:

1. `Touch` and `Inspect` lists
2. callable signature deltas when seams matter
3. a compact `Type Sketch` when payloads or state matter
4. one `Typed flow example` showing a representative object or payload moving
   through the main path
5. one Mermaid delta map when the flow, ownership, or typed data path is easier
   to skim visually

Keep map detail compact. The point is to make task shape legible in plain text,
not to dump full schemas into the ticket.

Use `Gap Analysis` when the work is about a missing, partial, parity-driven, or
otherwise under-specified feature and the main planning question is "what does
a production-grade version of this capability actually need?"

That section should answer:

1. what exists today and where it stops
2. what a credible production implementation usually includes
3. which gaps matter for this ticket now versus later
4. which comparable apps, repos, docs, or standards grounded that judgment

Use `Done / Proof` as the single completion scoreboard:

```text
done_when:
  - concrete done condition

proof:
  checks:
    - command or deterministic check
  manual:
    - direct inspection
  review:
    - rubric: skill-contract
      required_tas: TAS-A
  evidence:
    - artifact path or required artifact kind
```

For material work, `Done / Proof` is still the completion scoreboard. It should
name honest mechanical metrics when they exist, `none mechanical` when they do
not, reviewer rubric families, TAS gates, hard gates, and required artifacts.
Keep full rubric bodies in `docs/review/rubrics/` and full autoresearch session
files in the owning autoresearch artifacts. Tickets carry handles, thresholds,
and artifact obligations, not duplicate specialist contracts.

For UI-bearing, browser-driven, canvas/game, or otherwise agentically hard
tickets, add `Agent Contract`.

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

For tickets that may be drained by `$ralph`, run unattended, batched, or routed
through external compute, add `Run Hints` and name:

1. human inputs/assets
2. credentials or external access
3. compute/runtime needs
4. tooling gaps
5. QA risks and which QA ring applies
6. human gates for plan review, QA review, deploy, spend, or destructive work
7. decisions the agent may make autonomously
8. likely size, Goal recommendation, compute hint, proof weight, and
   batchability when those affect `$work`

If those answers are missing, keep the ticket gated instead of marking it ready
for the board-draining loop.

Do not duplicate the same idea across multiple headings. If `Delta`, `Program`,
`Map`, and `Done / Proof` already explain the task, do not add more ceremony.

Use `Links` for durable source URLs, specs, issues, websites, comparable
examples, sidecar files, artifacts, and reviews instead of spreading links
across extra note sections or duplicating them in frontmatter.

## Evidence Artifacts

Store ticket artifacts under `tickets/TASK-XXXX/artifacts/`.

Examples:

- screenshots
- logs
- exported review JSON
- short clips
- seed or fixture notes that help reproduce the proof surface

Link those artifacts from `Links` or `State` instead of preallocating empty
review-output fields in the template or repeating the artifact path under
`Done / Proof`.

Canonical policy references:

- [context-and-handoff-policy.md](/Users/kenjipcx/coding-harness/Farplane/docs/specs/context-and-handoff-policy.md)
- [invocation and adapters spec](/Users/kenjipcx/coding-harness/Farplane/docs/specs/invocation-and-adapters.md)
