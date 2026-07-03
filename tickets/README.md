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
- durable proof defaults to ticket-local artifacts under
  `tickets/TASK-XXXX/artifacts/`; global `.farplane/results/` is runtime
  scratch or explicit adapter output, not the preferred durable evidence home
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
  feedback samples, reflection, compact decision entries, drift verdicts,
  blockers, and next actions.
- `artifacts/` owns durable proof, bulky evidence, QA, review, evals,
  screenshots, reports, and generated prompts.

Use `tickets/templates/goal-loop/program.md` and
`tickets/templates/goal-loop/progress.md` when scaffolding these files. See
`docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md`
for the full contract.

## Invocation Policy

A ticket is a work card, not a trigger. Creating a ticket, setting
`ready: true`, moving `status`, or adding `compute_target` does not start an
agent by itself.

Farplane work starts from an explicit invocation:

- local operator request, such as asking Codex to run `TASK-0123`
- operator-invoked Goal/heartbeat board drain, which selects one eligible
  ticket and emits a native Goal prompt
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
claimed_by: codex-019ef784  # optional active session claim alias; empty when unclaimed
priority: medium
# optional compute override: local_shared, local_worktree, symphony, or codex_cloud
# compute_target: local_shared
depends_on: []
blocked_by: []
ready: false
approval_required: true
requires_qa: true
requires_demo: false
human_gate: none
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
- `claimed_by`: optional human-facing active claim alias for the current live
  session. Codex agents must use a session-specific alias such as
  `codex-019ef784`, not plain `codex`; clear this field when the live session
  blocks, parks, completes, or archives the ticket.
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
- `requires_qa`: whether `$goal-advisor` must produce a passing QA phase before completion
- `requires_demo`: whether `$goal-advisor` must also produce a passing demo phase after QA
- `human_gate`: compact final-action gate. Use `none` when the worker may
  finish the ticket without human approval. Use `[tag, "reason"]` when the
  worker may prepare artifacts and proof but must stop before that final
  action, such as `[post, "Public X post needs Kenji approval before it goes live."]`.
  Allowed tags live in `farplane/bindings.yaml` `human_gates`.
- `next_action`: the one authoritative next step
- `last_verification`: the one-line authoritative verification summary; keep
  detailed commands and artifacts in `Links`, `progress.md`, or
  ticket-scoped artifacts
- `decision_refs`: optional references to `progress.md` entries or
  `decisions.md` headings; do not put decision bodies in frontmatter

For Goal Advisor, Pulse, heartbeat, and board-drain, the explicit invocation is
the operator or automation running the selector. After that, a ticket is
selectable only when
`ready: true`, `approval_required: false`, `blocked_by: []`, `claimed_by:` is
empty, `phase` is not `complete` or `failed`, `status` is not `done` or
`failed`, the ticket is not parked or waiting on external credentials/feedback,
and every dependency is complete, archived, or explicitly waived in the ticket
body. These are hard gates, not ranking preferences.

`human_gate` is not a second ticket-start approval gate. It marks a final
outside-world action that the worker must not take without Kenji. Pulse should
leave that worker thread open, record or remind when useful, and continue safe
local work such as artifacts, research, proof, QA, packaging, or draft content
instead of treating human review as board-wide blockage.

For Farplane invocation, `bin/farplane_boards.py` is the canonical v1
BoardAdapter surface for reading filesystem tickets into normalized `WorkItem`
JSON. It is intentionally read-first: evidence links still belong in the
ticket `Links` section until a later ticket ships traceable writeback.
Future board adapters must satisfy
`docs/features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md`
before they become live ticket sources.

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
- `Change Plan`
- `Done`
- `QA Strategy`
- `Docs Strategy`
- `Links`
- `Notes`

Optional sections only when they add signal:

- `Reward`
- `Gap Analysis`
- `Agent Contract`
- `Run Hints`

The ticket is a compact task program over files and skills:

```text
ticket_change_plan(delta, change_units, qa_strategy) -> artifact_delta + evidence + state_delta
```

Use `Delta` to answer:

1. what changes
2. before versus after behavior
3. why now
4. first-principles basis: objective, need, assumptions, root cause,
   constraints, first viable slice, proof/falsification, tradeoff, and
   non-goals when material

Keep `Delta` brief after ticket creation. When `impl-plan(ticket)` runs, it
expands the work into `Change Plan` units instead of making readers cross-map
separate Delta, Program, and Map sections.

Use `Reward` for Pulse-created tactical tickets, experiments, and other work
whose planning value should be obvious before execution. Keep it small:

```text
Reward:
  moves: the goal, KPI axis, bottleneck, lane, or reward signal this advances
  win_signal: the observable result that says this ticket mattered
  guard: what must not regress or be gamed while chasing the signal
```

`Reward` is not a metrics registry and is not mandatory for every legacy
ticket. If the provider, guard, anti-metric, or proof route needs more detail,
put the metric card in `program.md` or route through `metric-advisor`.

Use `Change Plan` for the executable task-local program and file map. Split it
into one heading and one fenced block per coherent change:

```md
### Change 1: short label
```

```text
fixes:
  - plain-language problem or delta this change resolves
before: local before state
after: local after state
read:
  - path: file or doc to inspect
    reason: why this file matters
write:
  - path: file or doc to change
    change: specific edit
operation:
  - ordered implementation action
signature_or_type_impact:
  - module / symbol(input): output, or compact type sketch
routes:
  docs: doc-advisor | no_docs
  qa: tests | qa-tester | visual-qa | agent-qa-test | none
  review: reviewer | inline | none
qa:
  - focused QA or evidence expectation for this unit
failure_modes:
  - real trap to avoid
```

Avoid synthetic labels unless a ticket truly needs stable anchors for
many-to-many traceability. In normal tickets, `fixes:` is enough.

This replaces both `Program` and `Map` for normal tickets. Create a separate
`plan.md` only when the change plan is long, deeply technical, likely to change
independently, or too large to keep the ticket readable.

For Goal-backed tickets, use `progress.md` as the default reflection and
decision log. Add `decisions.md` only when a ticket has material branching
decisions, council notes, architecture/API/data-model tradeoffs, or reusable
rationale that would become hard to recover from a chronological log. Do not
create empty `decisions.md` files.

Use an optional visual system map inside `Change Plan` only when it earns its
keep:

1. cross-module topology
2. ownership boundaries
3. data flow or state transitions
4. seams that are easier to see in a diagram than in `read` / `write`

Keep diagram detail compact. The point is to make task shape legible in plain
text, not to dump full schemas into the ticket.

Use `Gap Analysis` when the work is about a missing, partial, parity-driven, or
otherwise under-specified feature and the main planning question is "what does
a production-grade version of this capability actually need?"

That section should answer:

1. what exists today and where it stops
2. what a credible production implementation usually includes
3. which gaps matter for this ticket now versus later
4. which comparable apps, repos, docs, or standards grounded that judgment

Use `Done` as the completion scoreboard:

```text
done_when:
  - concrete done condition
```

Use `QA Strategy` as the proof and QA plan that `goal-advisor(ticket)` can lift
into the Goal Packet inputs:

```text
qa_strategy:
  proof_weight: smoke | tests | qa | visual_qa | review | agent_qa | demo
  checks:
    - command or deterministic check
  manual:
    - direct inspection
  delegated_lanes:
    - qa-tester | visual-qa | agent-qa-test | reviewer | none
  review:
    - rubric: skill-contract
      required_tas: TAS-A
  evidence:
    - artifact path or required artifact kind
  goal_advisor_inputs:
    proof_route: delegated lanes required before completion
    final_evidence: report, command output, review receipt, screenshot, demo artifact, or blocker report
    final_checkpoint: QA evidence review, completion review, reviewer TAS gate, or none
  residual_risk:
    - unrun final path, flaky surface, or explicit remaining risk
```

For material work, `QA Strategy` should name honest mechanical metrics when
they exist, `none mechanical` when they do not, reviewer rubric families, TAS
gates, hard gates, delegated lanes, final checkpoint, and required artifacts.
Keep full rubric bodies in `docs/review/rubrics/` and full experiment session
files in the owning experiment artifacts. Tickets carry handles, thresholds,
and artifact obligations, not duplicate specialist contracts.

For material feature work, include critical-path proof in `QA Strategy`.
Use compact prose or bullets to name the real workflow or lifecycle being
claimed, then break long end-to-end proof into smaller ordered sanity checks.
Each check should make clear what action ran, what observation would prove the
state moved correctly, where the evidence lives, and where the next review
point should inspect data, logs, artifacts, UI, or session state. If the full
path is too long, expensive, flaky, or blocked, record the substitute checks and
residual risk rather than claiming full end-to-end proof.

For material Goal-backed work, put the final checkpoint in `QA Strategy`. Name
the QA evidence review, completion review, reviewer TAS gate, or explicit
`none` decision that must exist before completion. Do not rely on a Stop hook
or transcript memory to discover missing QA after the agent claims done.

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

For tickets that may be drained by Goal Advisor/heartbeat, run unattended,
batched, or routed through external compute, add `Run Hints` and name:

1. human inputs/assets
2. credentials or external access
3. compute/runtime needs
4. tooling gaps
5. QA risks and which QA ring applies
6. human gates for plan review, QA review, deploy, spend, or destructive work
7. decisions the agent may make autonomously
8. likely size, Goal recommendation, compute hint, proof weight, and
   batchability when those affect `$work`
9. expected beats and parallel eligibility when Pulse or another heartbeat
   needs capacity-learning hints

If those answers are missing, keep the ticket gated instead of marking it ready
for the board-draining loop.

Do not duplicate the same idea across multiple headings. `Change Plan` owns the
implementation program and file map. `Done` owns the final scoreboard.
`QA Strategy` owns proof route, evidence, review gates, and final checkpoint.
`program.md` owns Goal loop configuration after `goal-advisor` runs.

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

Link those artifacts from `Links` instead of preallocating empty
review-output fields in the template or repeating the artifact path under
`Done` and `QA Strategy`.

Canonical policy references:

- [Lean global agent operating kernel](../docs/features/FEAT-0042-lean-global-agent-operating-kernel.md)
- [Symphony-compatible Farplane invocation contract](../docs/features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md)
