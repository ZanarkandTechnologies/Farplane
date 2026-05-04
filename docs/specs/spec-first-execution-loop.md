# Spec-First Execution Loop

Date: 2026-04-07

## Goal

Define the current canonical execution model for Codexter:

- user-guided discovery up front
- spec-first planning
- post-system-design agent testability planning when the system will be hard for agents to reach, inspect, or coordinate
- autonomy-readiness capture before long-running or board-draining execution
- feature-sized work packages
- per-work-package `impl-plan`
- per-work-package `$impl` orchestration
- optional serial `$ralph` dispatch over ready filesystem tickets
- worker lanes launched by `$impl` where appropriate
- separate QA and review roles
- Stop hook as the final continuation/completion gate

This spec replaces older ambiguity about whether the system is ticket-first,
runtime-first, or fully black-box.

## Terminology

Use these terms precisely:

- **Spec**: the human-approved product/feature direction
- **Work package**: one meaningful feature-sized execution unit
- **Board state**: ticket `status` / `phase`
- **Execution lane**: one active runtime slot such as a tmux pane, worktree, or
  prompt worker
- **Claim**: which execution lane currently owns a work package
- **Progress surface**: the visible file/state that says what is active, what is
  done, and what is next
- **Autonomy Readiness**: the explicit inputs, permissions, compute, tools, QA
  risks, and human gates an agent needs before running unattended

Avoid using bare `lane` when you mean board state.

## Staged Flow

### 1. Discovery / Spec

Use:

- `brainstorm`
- `deep-interview`
- `prd`

Purpose:

- reduce ambiguity
- align on the design direction
- make success legible before implementation starts

The output of this stage is one coherent spec.

### 2. Agent Testability Planning

When the designed system will be hard for an agent to operate directly, run
`agent-testability-plan` before ticketization or per-ticket planning.

Purpose:

- decide which control accelerators the agent should have
- decide which hidden-state probes the agent should have
- decide whether multi-part execution needs one coordination view
- define the proof surfaces later tickets should preserve

The output of this stage is one visible `Agent Testability Brief`.

### 3. Work Packaging

After the spec is coherent, and after any needed testability planning, convert
it into work packages.

Default rule:

- one work package = one feature / meaningful capability

Do **not** split one feature into:

- tiny MVP first
- “real” version later

unless there is a real:

- dependency boundary
- brownfield integration boundary
- execution-risk boundary

Each work package that may be run unattended or drained by `$ralph` should carry
`Autonomy Readiness`: required user inputs/assets, credentials, external
services, compute, tooling gaps, QA risks, human gates, and agent decision
boundaries.

### 4. Planning

`impl-plan` plans one selected work package.

It should:

- inspect linked specs
- inspect any linked `Agent Testability Brief`
- inspect the relevant code
- write the execution plan into the ticket/progress surface
- define how the work will be proved

It should **not** decompose the whole spec into many micro-tasks.

### 5. Build Loop

`$impl` orchestrates one selected work package.

It should:

- read the selected ticket plus linked docs/specs
- prefer an explicit ticket selector over ambient runtime state
- launch the needed worker lanes for builder/reviewer/QA/evidence-check
- write progress and next action back to the ticket/progress surface
- exit after the round instead of becoming a permanent orchestrator pane

Inside `status: building`, runtime may progress through internal execution
subphases:

- `impl`
- `qa`
- `demo`

`$qa` and `$demo` may also be used as explicit recovery surfaces for those
subphases, but `$impl` remains the default public execution entrypoint.

Worker lanes may vary by ticket, but the public build-phase entrypoint is
`$impl`.

### 5b. Optional Serial Board Drain

`$ralph` may run after tickets are prepared.

It should:

- read active filesystem tickets
- select one ready, unblocked, dependency-safe, unclaimed, approval-free ticket
- hand planning tickets to `impl-plan`
- hand building tickets to `$impl`
- hand documenting tickets to `close-ticket`
- reread the board after each phase
- stop on no ready work, human gates, blockers, failed handoff, or loop limit

`$ralph` does not replace `$impl` and does not own parallel dispatch in the
current system.

### 6. QA + Review

These are separate roles and should stay separate.

#### QA

QA collects evidence:

- logs
- screenshots for UI-bearing work
- repro steps
- observed behavior

QA does not decide code quality.

#### Review

Review judges implementation quality:

- correctness
- regressions
- maintainability
- architecture/code quality
- whether the evidence is persuasive enough

Review does not own screenshot gathering.

### 7. Stop Hook

The Stop hook is the final gate.

It should decide:

- continue same work package
- block for human review
- mark complete

When it continues the same work package, it should re-enter the same `$impl`
contract using the existing verdict fields and follow-up/orchestrator message,
not a parallel hidden control plane.

It should not become:

- the main planner
- the main reviewer
- the main QA collector

## Ticket / Work Package Contract

For now, Markdown tickets remain the visible work-package files.

Each active work package should include:

- summary
- scope
- implementation plan
- acceptance criteria
- QA evidence expectations
- review rubric
- next action
- last verification

Future direction:

- keep `owner`
- add `claimed_by` and maybe `claimed_at` if ticket-native parallel dispatch is
  needed

## Review Gates

Every work package must define how it will be judged.

Minimum rubric dimensions:

- functionality correctness
- regression / integration safety
- code quality
- evidence adequacy

Optional dimensions:

- UI fidelity
- API contract correctness
- backend/data correctness
- security
- performance
- autonomy readiness for unattended or `$ralph` work

The review output should be explicit enough that the Stop hook can sanity-check
it without guessing.

## Evidence Policy

Phase 1 evidence should be:

- logs plus screenshots

Why:

- screenshots are required for UI trust
- logs are still useful supporting evidence
- video generation is deferred for now

For `$ralph` board drains, use three QA rings:

1. cheap per-ticket checks every time
2. targeted heavy QA only for risky tickets
3. batch or release QA after a declared milestone when multiple related tickets
   were drained

## Queue / Archive Policy

Active work stays in `tickets/`.

Completed or outdated work moves to `tickets/archive/`.

Archive is for:

- fully processed tickets
- temporary runtime smoke tickets
- superseded design tickets

Archive is a visibility/history surface, not a hot runtime surface.

## Current Implementation Bet

The current product bet is:

- keep Codexter’s planning/spec/review surfaces
- keep the queue readable
- improve longer runs and stronger review before adding more runtime machinery

This means:

- stronger review loop first
- clearer progress surface first
- cleaner continuation behavior first
- serial dispatcher over filesystem tickets now
- parallel dispatcher/worktrees later if still needed
