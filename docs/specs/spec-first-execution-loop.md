# Spec-First Execution Loop

Date: 2026-04-07

## Goal

Define the current canonical execution model for Codexter:

- user-guided discovery up front
- spec-first planning
- feature-sized work packages
- per-work-package `impl-plan`
- per-work-package `$impl` orchestration
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

### 2. Work Packaging

After the spec is coherent, convert it into work packages.

Default rule:

- one work package = one feature / meaningful capability

Do **not** split one feature into:

- tiny MVP first
- “real” version later

unless there is a real:

- dependency boundary
- brownfield integration boundary
- execution-risk boundary

### 3. Planning

`impl-plan` plans one selected work package.

It should:

- inspect linked specs
- inspect the relevant code
- write the execution plan into the ticket/progress surface
- define how the work will be proved

It should **not** decompose the whole spec into many micro-tasks.

### 4. Build Loop

`$impl` orchestrates one selected work package.

It should:

- read the selected ticket plus linked docs/specs
- prefer an explicit ticket selector over ambient runtime state
- launch the needed worker lanes for builder/reviewer/QA/evidence-check
- write progress and next action back to the ticket/progress surface
- exit after the round instead of becoming a permanent orchestrator pane

Worker lanes may vary by ticket, but the public build-phase entrypoint is
`$impl`.

### 5. QA + Review

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

### 6. Stop Hook

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

The review output should be explicit enough that the Stop hook can sanity-check
it without guessing.

## Evidence Policy

Phase 1 evidence should be:

- logs plus screenshots

Why:

- screenshots are required for UI trust
- logs are still useful supporting evidence
- video generation is deferred for now

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
- dispatcher/worktrees later if still needed
