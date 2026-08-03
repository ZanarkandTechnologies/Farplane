# Tickets

Active work lives in `tickets/TASK-*/ticket.md`.

One source of truth per concern:

- frontmatter = queue state and execution state
- body = plan, references, evidence, and blockers
- `.farplane/state/` = live runtime state
- `docs/` = durable knowledge after the ticket is done
- `tickets/archive-index.jsonl` = compact locator for new GitHub-issue closes
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
  archive-index.jsonl  # compact locator for new GitHub-issue closes
  archive/
    TASK-0000/         # legacy local archive; remains readable
      ticket.md
      artifacts/
  templates/
    ticket.md
```

No lane folders. No hand-maintained board file. The ticket itself is the board card.

## Lifecycle

1. create the ticket as `status: awaiting_review` when approval is still needed,
   or `status: todo` when it is admitted
2. the executing session sets `status: active` and adds `claimed_by`
3. on human review or delayed signal, clear `claimed_by` and use
   `awaiting_review` or `waiting_signal`
4. on a non-ticket blocker, clear the claim, set `blocked`, and record details
   in `progress.md`
5. after implementation, proof, review, and durable docs, use `$close-ticket`
   to create or resume one issue in the project's configured GitHub repository
6. keep the issue glanceable with `Before`, `After`, `Example`, `Key decisions`,
   and compact `Proof`; for material feature work, require the passing reviewed
   `$demo` MP4 as the first marked comment, followed by any explicitly selected
   supporting screenshots through the authenticated GitHub browser composer
7. verify the issue body and every expected media marker, then close the issue
   as completed
8. run `farplane ticket close TASK-XXXX` with that issue and selected media;
   Core re-verifies the closed issue, writes terminal metadata, mines the
   still-local packet, writes its compact locator, emits completion, and only
   then deletes the exact packet

## Terminal Archive Contract

For newly closed tickets, the closed issue is the durable terminal record.
Its body preserves the concise before/after/example, key decisions, and proof
summary. Explicitly selected final screenshots and videos are preserved as
marked issue comments so each upload can be verified and retried independently.
The compact `tickets/archive-index.jsonl` row is a local identity, status, and
URL projection; it is not a second ticket archive.

Every terminal gate is retain-local. A repository that does not match
`integrations.github.repo`, missing authentication, unsupported media, missing
or duplicate marker, failed upload, unclosed issue, mining failure, or locator
conflict leaves the full active packet in place. The configured repository may
be public, private, or internal. Retries resume the exact marked issue and
comments rather than creating duplicates. Agents must not manually move or
delete the packet.

Existing `tickets/archive/TASK-*` directories remain readable legacy records.
This workflow does not migrate or delete them. GitHub Releases, release assets,
tags, downloadable bundles, manifests, remote restore, and reconstruction of a
deleted ticket packet are future work and outside the current contract.

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
- deliberate reset/resume starts from `ticket.md`, `program.md`, and the latest
  80 lines of `progress.md`; load older receipts only to resolve a named
  evidence gap
- one ticket owns one persistent Codex task titled exactly
  `[TASK-XXXX] <ticket title>`; execution, review, feedback, waiting, and
  check-in resume it. Do not create `Plan ...` or `Execute ...` copies, and do
  not parse the display title as identity.

## Goal Packets

Use a Goal Packet when native Goal mode is used for material, long-running,
feedback-heavy, rollout, heartbeat, business-loop, or skill-improvement work.

```text
goal_loop(ticket.md, program.md, progress.md, trigger)
  -> next_turn + evidence + drift_verdict + state_delta
```

Every active Goal uses one decision backbone:

```text
observe -> choose_next(execute | diagnose | report_now | request_feedback | stop)
        -> act -> verify -> write_back
```

Goal Advisor compiles the packet, Metric Advisor establishes or repairs the
measurement contract, Leverage Advisor compares moves only when several
plausible options need judgment, and the domain skill executes. Plan Next Wave
is an upstream empty-board refiller and never participates inside an active
Goal.

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

A ticket is a work card, not a trigger. Creating a ticket, moving `status`, or
adding `compute_target` does not start an agent by itself.

Farplane work starts from an explicit invocation:

- local operator request, such as asking Codex to run `TASK-0123`
- operator-invoked Goal/heartbeat board drain, which selects one eligible
  ticket and emits a native Goal prompt
- a recognized board comment or shared-board action after an external runner
  converts it into a `FarplaneRunEnvelope`
- a future Codex Cloud, Symphony, or other runner payload

`status: todo` means the ticket is eligible once invoked and its dependencies
are satisfied. It does not mean Farplane should watch the board and begin work
without an explicit Pulse, Goal, operator, or external-runner invocation.

## Canonical Frontmatter

```yaml
---
ticket_id: TASK-0002
title: short title
status: todo
created_at: 2026-04-03T00:00:00Z
updated_at: 2026-04-03T00:00:00Z
---
```

Sparse routing overrides are added only when they differ from defaults:

```yaml
priority: high
due_at: 2026-04-10T17:00:00+08:00
claimed_by: codex-019ef784
depends_on: [TASK-0001]
human_gate: [post, "Public X post needs Kenji approval."]
compute_target: local_worktree
```

## Field Meanings

- `status`: the sole lifecycle state: `todo`, `active`, `awaiting_review`,
  `waiting_signal`, `blocked`, `done`, `failed`, or `rejected`.
- `priority`: optional `urgent`, `high`, `medium`, or `low`; omission means
  `medium`. Priority expresses strategic importance.
- `due_at`: optional delivery deadline as a timezone-bearing ISO-8601
  timestamp, for example `2026-04-10T17:00:00+08:00` or
  `2026-04-10T09:00:00Z`. It expresses when the ticket artifact or outcome is
  needed; it is distinct from priority and from Reward `check_in_at`, which
  schedules outcome evaluation. Executable tickets sort by priority, then
  earliest `due_at` with missing deadlines last, then ticket ID.
- `claimed_by`: optional human-facing alias for the current active execution
  turn. It is present only with `status: active` and cleared when execution
  parks, waits, completes, or releases the worker.
- `depends_on`: optional structural ticket prerequisites. Non-ticket blocker
  detail belongs in `progress.md`, not a second blocker list.
- `compute_target`: optional ticket-level compute override. Supported values
  are `local_shared`, `local_worktree`, `symphony`, and `codex_cloud`; future
  targets may be recorded but remain blocked unless the active workflow and
  adapter support them.
  - `local_shared` runs in the current checkout.
  - `local_worktree` requires a ticket runtime record under
    `.farplane/state/tickets/TASK-XXXX.runtime.json`.
  - `symphony` and `codex_cloud` are future external-adapter targets and must
    stay blocked in local Farplane until those adapters exist.
- `human_gate`: optional final-action gate. Omit it when the worker may finish
  without human approval. Use `[tag, "reason"]` when the
  worker may prepare artifacts and proof but must stop before that final
  action, such as `[post, "Public X post needs Kenji approval before it goes live."]`.
  Allowed tags live in `farplane/bindings.yaml` `human_gates`.
- `rejection_reason`: optional compact rejection summary; a durable rejection
  entry in `progress.md` is also valid.

`phase`, `owner`, `blocked_by`, `ready`, `approval_required`, `requires_qa`,
`requires_demo`, `next_action`, and `last_verification` are not ticket metadata.
Their former information is owned by `status`, `claimed_by`, `depends_on`, the
ticket `Program`/`Change Plan`, `QA Strategy`, `Done`, and `progress.md`.

For Goal Advisor, Pulse, heartbeat, and board-drain, the explicit invocation is
the operator or automation running the selector. After that, a ticket is
selectable only when `status: todo`, `claimed_by` is absent, and every
dependency is active-board complete, present in the compact closed-ticket
locator, or present in a legacy local archive. A `waiting_signal` ticket is
temporarily selectable only when a ticket Reward row matures. These are hard
gates, not ranking preferences.

`human_gate` is not a second ticket-start approval gate. It marks a final
outside-world action that the worker must not take without Kenji. Pulse records
the review wait, releases the worker, reminds only when due, and continues safe
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
- no `phase`, `owner`, `blocked_by`, `ready`, `approval_required`,
  `requires_qa`, `requires_demo`, `next_action`, or `last_verification` fields
- no `## Status` body block
- the H1 matches `ticket_id` and `title`
- do not store raw transport-level runtime ids such as `session_id` in ticket frontmatter
- `status: active` requires a session-specific `claimed_by`; every other
  status clears it
- review/check-in mutable state lives in `progress.md`
- QA, demo, and reviewer gates live in `QA Strategy`
- do not invent a second machine-readable state block in the body

## Sizing Doctrine

- first-load Goal state is the full `ticket.md`, full `program.md` when
  present, and at most the latest 80 lines of `progress.md`
- target at most 300 first-load lines; block planning or completion above 400
  lines until duplicated policy is consolidated or bulky evidence moves to
  `artifacts/`
- line count is a context constraint, not a quality score: required proof,
  safety, ownership, and reconstruction behavior must remain intact
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
farplane validate ticket tickets/TASK-XXXX/ticket.md --phase planning
```

The ticket validation route includes `ticket.context-budget`. It reports
pressure above the 300-line target and blocks above the 400-line hard limit.

The validator treats `tickets/TASK-*/ticket.md` as canonical and still tolerates
flat `tickets/TASK-*.md` files only as archived pre-directory ticket history.

Reward scheduling is an explicit tagged union:

- `check_in_at: <timezone-bearing ISO-8601 timestamp>` schedules delayed work.
- `check_in_at: unscheduled` declares that no check-in should be delegated.
- Missing, blank, null, timezone-naive, or other values are malformed and the
  owning ticket must repair them; validators and Work Pulse do not invent a
  date or silently treat them as unscheduled.

## Body Contract

Keep the body short by default. The main job of a ticket body is to let a
developer or subagent understand the task contract, variable files, operations,
and proof without opening every file first.

Default sections:

- `Summary`
- `Scope`
- `Delta`
- `Change Plan`
- `Map`
- `Done`
- `QA Strategy`
- `State`
- `Docs Strategy`
- `Links`
- `Notes`

Optional sections only when they add signal:

- `Reward`
- `Planned Skill Call`
- `Objective Contribution`
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

Keep `Delta` brief after ticket creation. `Change Plan` owns executable units;
`Map` is only their compact visual or signature projection and must not repeat
the prose.

Use `Reward` for Pulse-created tactical tickets, interval-planned tickets,
experiments, and other work whose planning value should be obvious before
execution. Keep it small:

```yaml
kpi_rewards:
  - reward_id: accepted-harness-improvements-7d
    kpi_id: accepted_harness_improvements
    expected_reward: "one proof-backed harness improvement"
    check_in_at: "2026-04-10T00:00:00Z"
    actual_result:
    decision:
    evaluated_at:
    evaluation_key:
    supersedes_evaluation_key:
    evidence_refs: []
guard: "do not count planned intent as KPI movement; count only completed tickets with proof"
```

`Reward` is not a metrics registry. Manual/operator tickets may omit it; every
AI-planned or experimental Reward row uses the canonical fields below.
`reward_id` is unique and stable inside the ticket and remains the identity when
rows are reordered. `check_in_at` is when Work Pulse may resume the original
ticket to compare the expectation with evidence. The check-in worker writes the
latest `actual_result`, `decision`, `evaluated_at`, `evaluation_key`, and
`evidence_refs`; score-only rows are not realized value.

Canonical state is derived without another lifecycle field:

```text
pending          = decision empty  AND check_in_at > now
due              = decision empty  AND check_in_at <= now
monitor_pending  = decision monitor AND check_in_at > now
monitor_due      = decision monitor AND check_in_at <= now
terminal_accept  = decision accept
terminal_kill    = decision kill
```

`monitor` updates the same row's `check_in_at` to a later instant after storing
the completed evaluation. `accept` and `kill` are terminal. Re-applying the
same `evaluation_key` is a no-op. A correction replaces the latest row fields,
sets `supersedes_evaluation_key`, and appends a progress entry naming the
replaced evaluation.

```text
evaluation_key
  = sha256(ticket_id, reward_id, check_in_at, evidence_digest, program_digest)

accepted_reward(ticket, reward)
  iff reward.decision == accept
      AND reward.actual_result is non-empty
      AND reward.evaluated_at is valid
      AND reward.evidence_refs is non-empty
      AND ticket-scoped review evidence is pass/TAS-A
```

There are exactly two learning horizons. Work Pulse derives matured rows and
resumes the original ticket for ticket-local evaluation. Weekly Dogfood reads
the recorded terminal outcomes for portfolio learning without rescoring them.
Pulse admission receipts may be joined to eventual Reward decisions for plan
outcome analysis, but Farplane has no independent plan score or plan-wave loop.
If the provider, guard, anti-metric, or proof route needs more detail, put the
metric card in `program.md` or route through `metric-advisor`.

### Reward versus experiment prediction

These are different learning horizons:

```text
Experiment prediction:
  immediate expected observation if a causal hypothesis is right
  owner: Metric Card plus experiment plan/program
  miss route: agent-qa-test:experiment for first-principles validity/inference review

Reward.expected_reward:
  delayed realized value expected from the completed ticket
  owner: Objective Contribution projection plus Reward row
  miss route: gap-analysis, then accept | kill | monitor at check-in
```

Do not duplicate either value. An experiment-like ticket may use both because
they answer different questions: “did the mechanism produce the expected
observation now?” and “did the shipped work create the expected value later?”
A deterministic implementation ticket can omit the experiment prediction.
When a Reward miss is also downstream of a causal experiment surprise, preserve
both receipts and run the scientific surprise route before making a method-level
claim.

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
After the checkpoint passes, use `farplane ticket close TASK-XXXX` for the
terminal state, verified archive writeback, mining, locator write, and cleanup;
do not hand-edit, manually move, or manually delete the packet. Farplane Stop
hooks are telemetry-only and do not own proof repair or terminal closeout.

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
