# Research: Run Artifacts Foundation Risk Analysis

Date: 2026-04-02

## Scope

Stress-test the highest-leverage planned feature:

- `TASK-0002` run artifacts foundation

The goal is to predict what will likely go wrong if Codexter adds `.codexter/runs/<RUN_ID>/` naively, then define the smallest design choices that de-risk the feature before implementation begins.

This memo is intentionally biased toward prevention:
- failure modes first
- then design constraints
- then the practical countermeasures

## Feature Under Test

The proposed feature is a minimal runtime artifact substrate:

```text
.codexter/
  runs/<RUN_ID>/
    prompt.md
    spec.md
    run-state.json
    summary.md
    rounds/
      01/
        contract.md
        builder-report.md
        evaluator-report.md
        metrics.json
        handoff.md
```

Its intended value is:
- resumability after context loss
- explicit round/phase state
- a machine-friendly control plane for future orchestration
- without replacing `tickets/` or `docs/`

## Main Risk

The biggest risk is not technical complexity by itself.
It is this:

> Codexter could accidentally create a second planning/execution system that competes with tickets instead of supporting them.

If that happens, the feature becomes overhead, not leverage.

## Predicted Failure Modes

## 1. Dual source of truth

### What goes wrong

If `tickets/` say one thing and `.codexter/runs/` says another, the harness becomes less trustworthy than it is today.

Typical failure shape:
- ticket says task is in `review`
- run state says it is in `executing`
- summary says the round passed
- acceptance criteria are still unchecked in the ticket

This is the fastest way to make the feature feel fake.

### Why it is likely

Codexter already has strong existing artifact surfaces:
- `tickets/`
- `docs/`
- memory/history/troubles

Adding runs introduces a third major artifact surface.

### Derisk

- Make `tickets/` the execution and approval source of truth.
- Make `.codexter/runs/` the per-run coordination and resume source of truth.
- Make `docs/` the durable human-readable memory source of truth.
- Document this split explicitly in the first contract.

### Circumvention rule

`run-state.json` must never replace ticket lane/approval state.
It can mirror linked ticket state, but the board remains canonical for board movement.

## 2. Schema over-design

### What goes wrong

The first version of `run-state.json` becomes too smart:
- too many fields
- speculative lifecycle states
- premature metrics
- fields that imply automation not yet implemented

Then every later slice has to either honor bad fields or migrate them.

### Why it is likely

This feature invites architecture enthusiasm because it looks foundational.

### Derisk

Start with the smallest schema that answers only:
- what run is this
- what phase is it in
- what ticket is it linked to
- what artifacts exist
- when was it updated
- what is the next visible handoff point

### Circumvention rule

If a field does not help resume, inspect, or hand off a run in v1, it should not exist.

## 3. Resumability illusion

### What goes wrong

The repo gains a run folder and state file, but a fresh agent still cannot realistically resume from it because the artifacts do not contain enough context.

Typical failure shape:
- `run-state.json` exists
- but there is no clear current contract
- no concise handoff
- no notion of what changed this round
- no explicit next action

This creates "paper resumability" instead of real resumability.

### Why it is likely

It is easy to store state.
It is harder to store enough context to actually continue work.

### Derisk

Require a minimal handoff surface in the contract:
- current prompt or problem statement
- current contract
- current phase
- linked ticket
- latest summary of what remains
- explicit next action

### Circumvention rule

No run is considered resumable unless a human can read its files and know what to do next without reading chat.

## 4. Hook coupling too early

### What goes wrong

The design assumes hooks or telemetry updates before the artifact contract is stable, forcing the hook layer to guess schema and file semantics.

That produces brittle behavior and rework.

### Why it is likely

`TASK-0005` depends on `TASK-0002`, but the temptation will be to think about the hook while designing the schema.

### Derisk

- Keep `TASK-0002` fully docs-first.
- No runtime writes in this slice.
- Design a schema that a passive hook could update later, but do not make the schema depend on hook behavior.

### Circumvention rule

The run artifact contract must be valid and useful even if no hook ever writes to it.

## 5. Artifact sprawl

### What goes wrong

Every run creates too many files too early, so people stop using the system or fake the artifacts.

Typical failure shape:
- prompt
- spec
- summary
- state
- contract
- builder report
- evaluator report
- metrics
- handoff
- plus ticket

For small work, this is too much.

### Why it is likely

The proposed tree already contains several artifacts, and future tickets add more.

### Derisk

Define:
- required files for v1
- optional files for later phases
- when a round folder is needed
- when a run can stay minimal

### Circumvention rule

In v1, only require what is necessary to resume and inspect.
Everything else should be optional until the orchestration loop is real.

## 6. Naming churn and path instability

### What goes wrong

The repo starts using one path, then later changes:
- `.codexter/runs/`
- `.codexter/state/`
- `.codexter/runtime/`
- `.omx/`-style variations

That creates migration pain immediately.

### Why it is likely

This is a foundational path decision and has not been exercised yet.

### Derisk

- Decide once that `.codexter/runs/` is the canonical run root.
- Treat path changes as migration-grade changes.
- Keep other runtime surfaces out of v1.

### Circumvention rule

Do not introduce multiple runtime roots in the first pass.

## 7. Hidden automation pressure

### What goes wrong

The schema quietly bakes in assumptions that later justify hidden behavior:
- `next_action` becomes auto-executed
- `status` becomes watcher-driven
- `resume` starts implying automatic continuation

This is how you slowly recreate the OMX auto-nudge problem.

### Why it is likely

Foundational runtime features often drift toward control-plane behavior.

### Derisk

- Make all run artifacts human-visible.
- Any "next action" field must be descriptive only.
- No field should imply permission to inject behavior.

### Circumvention rule

`run-state.json` is descriptive state, not executable authority.

## 8. Weak phase vocabulary

### What goes wrong

Phases are too vague or too numerous:
- `thinking`
- `working`
- `processing`
- `executing`
- `reviewing`
- `awaiting`
- `handoff_pending`

Different agents will interpret them differently.

### Why it is likely

Phase naming feels harmless until multiple tools/people rely on it.

### Derisk

Use a tiny phase vocabulary aligned to Codexter's actual workflow:
- `discovery`
- `planning`
- `building`
- `evaluating`
- `handoff`
- `complete`
- `failed`

### Circumvention rule

If a phase does not correspond to a real board/workflow state boundary, do not include it.

## 9. Ticket/run linkage ambiguity

### What goes wrong

One run links to many tickets loosely, or many runs link to one ticket with no primary relationship.

Then nobody knows which artifact set is the active one.

### Why it is likely

Codexter is ticket-first; runs are new.

### Derisk

For v1:
- one run has one primary linked ticket
- one ticket may have zero or one active run
- multiple runs per ticket should be an explicit later extension

### Circumvention rule

Do not support many-to-many ticket/run relationships in v1.

## 10. Sensitive or noisy artifact capture

### What goes wrong

Run artifacts accidentally become a dumping ground for:
- long logs
- secrets
- raw shell output
- huge diffs

That makes the repo noisy and risky.

### Why it is likely

Resumability systems often attract "just dump everything" behavior.

### Derisk

- Keep artifacts concise and structured.
- Store summaries, not raw logs, in v1.
- Reuse existing docs/memory rules about secrets and runtime state boundaries.

### Circumvention rule

If an artifact is too big or too sensitive to review comfortably in Git, it does not belong in v1.

## Design Constraints For V1

These should be treated as hard constraints.

## 1. Docs-first only

No hook logic.
No watcher logic.
No automation implied by the state file.

## 2. One source of truth per concern

- board state: `tickets/`
- durable memory: `docs/`
- per-run coordination: `.codexter/runs/`

## 3. Minimal schema

Recommended v1 `run-state.json` fields:

```json
{
  "schema_version": 1,
  "run_id": "RUN-0001",
  "title": "short human label",
  "phase": "planning",
  "status": "active",
  "linked_ticket": "TASK-0002",
  "created_at": "ISO8601",
  "updated_at": "ISO8601",
  "current_round": 0,
  "artifacts": {
    "prompt": "prompt.md",
    "spec": "spec.md",
    "summary": "summary.md"
  },
  "next_handoff": "one-line visible next action"
}
```

Nothing more should be required in v1.

## 4. Optional round directory

Do not require `rounds/01/` for every run immediately.
Make rounds optional until the orchestration loop exists.

## 5. Human-readable first

Every required machine-friendly artifact must still be understandable to a human reviewer.

## Derisking Moves To Apply Before Build

## Move 1: Freeze the ownership model

Add one short contract line:

- `tickets/` decide board movement and approval state
- `.codexter/runs/` decide per-run coordination state
- `docs/` decide durable knowledge

## Move 2: Freeze the minimal schema

Do not let later tickets expand the v1 schema during `TASK-0002`.
Any new field after the minimal set should require a concrete downstream use.

## Move 3: Require one example run

The docs should include one example run tree so reviewers can spot missing context immediately.

## Move 4: Keep rounds optional

Round artifacts should be introduced as part of orchestration work, not forced into the foundation prematurely.

## Move 5: Add anti-goals explicitly

The v1 contract should explicitly say it does not include:
- hooks
- auto-resume
- auto-continue
- watchers
- evaluator automation
- team runtime

This prevents drift.

## Move 6: Tie success to resume realism

Review question:

> Can a fresh agent read the run folder and know what to do next?

If the answer is no, the contract is incomplete.

## Circumvention Strategies For Specific Risks

If the feature starts drifting in implementation, these are the escape hatches:

### If it starts duplicating ticket state

Circumvent by removing duplicated board fields from `run-state.json`.

### If the schema starts expanding too fast

Circumvent by freezing `schema_version: 1` and rejecting new fields until a downstream ticket proves the need.

### If artifacts become too noisy

Circumvent by moving back to a required-minimum set:
- `prompt.md`
- `run-state.json`
- `summary.md`

and make everything else optional.

### If resume still feels weak

Circumvent by strengthening `summary.md` and `next_handoff`, not by immediately adding automation.

### If later work tries to smuggle in auto-control behavior

Circumvent by enforcing:

> run artifacts are descriptive, not imperative

## What To Watch During Implementation Review

When reviewing `TASK-0002`, the main red flags are:

- too many state fields
- duplicated ticket lane/approval state
- required round artifacts too early
- hook assumptions in the docs
- any implied runtime authority in `run-state.json`
- unclear linked-ticket semantics
- lack of a readable example run

## Bottom Line

The run-artifacts foundation is still the right first feature.
But its failure mode is easy to predict:

> if it becomes a second system instead of a thin coordination substrate, it will make Codexter worse.

The safe path is:

- keep it docs-first
- keep it minimal
- make ownership boundaries explicit
- require real resumability, not symbolic resumability
- delay hooks, automation, and rounds until later tickets

## Suggested Next Step

Before implementing `TASK-0002`, use this memo to tighten the ticket with three explicit additions:

1. anti-goals for v1
2. frozen minimal `run-state.json` field set
3. explicit ownership split between `tickets/`, `docs/`, and `.codexter/runs/`
