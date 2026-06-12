# Spec-First Execution Loop

Date: 2026-04-07

## Goal

Define the current canonical execution model for Farplane:

- user-guided discovery up front
- spec-first planning
- post-system-design agent testability planning when the system will be hard for agents to reach, inspect, or coordinate
- autonomy-readiness capture before long-running or board-draining execution
- feature-sized work packages
- Work Admission before planning/building
- per-work-package `impl-plan`
- per-work-package `$impl` orchestration
- optional serial `$ralph` dispatch over ready filesystem tickets
- worker lanes launched by `$impl` where appropriate
- separate QA and review roles
- native Goal for semantic continuation and Stop hook for mechanical
  active-ticket gates

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
- **Run Hints**: compact execution hints for inputs, permissions, compute,
  tools, QA risks, human gates, and agent decision boundaries before
  unattended or delegated work
- **Work Admission**: `$work` classification of one request, ticket, batch,
  board-selected unit, epic, or metric loop into Goal, compute, planning,
  proof, testability, and downstream skill choices

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

Each work package should use the compact ticket-as-program body: `Summary`,
`Scope`, `Delta`, `Program`, `Map`, `Done / Proof`, `State`, `Links`, and
sparse `Notes`.

Material, delegated, unattended, or `$ralph`-drained packages should also carry
`Run Hints`: required user inputs/assets, credentials, external services,
compute, tooling gaps, QA risks, human gates, and agent decision boundaries.
Those hints help `$work` decide size, Goal policy, compute, planning, proof,
and batchability, but they do not start execution.

### 3b. Work Admission

`$work` runs before planning/building when the right execution mode is not
obvious.

It should classify the unit as:

- tiny direct work
- one normal ticket
- ticket batch
- board drain
- epic that needs reslicing
- metric loop

It should then choose:

- whether native Goal is unnecessary, recommended, or required
- whether to use current checkout, local worktree, Codex Cloud, or Symphony
- whether to bypass planning, use a light plan, run `impl-plan`, or reslice
- whether proof is smoke, tests, QA, visual QA, review, demo, or a batch ledger
- whether blockers should be handled by fallback, recorded, or returned to the
  operator

For ticket batches, `$work` requires one proof row per ticket plus one
batch-level regression row before completion.

### 4. Planning

`impl-plan` plans one selected work package after `$work` or the operator
decides material planning is warranted.

It should:

- inspect linked specs
- inspect any linked `Agent Testability Brief`
- inspect the relevant code
- write the execution plan into the ticket/progress surface
- define how the work will be proved

It should **not** decompose the whole spec into many micro-tasks.
It should not be forced onto tiny direct work, and it should not absorb vague
epic discovery that belongs in PRD, system design, or `spec-to-ticket`.

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

The main agent orchestrates a work package; it does not personally do every
step when separate lanes are available. The default lane split is:

1. builder implements inside the declared scope
2. reviewer scores the work against the ticket `Done / Proof` contract and selected
   review rubrics
3. QA gathers evidence such as logs, screenshots, repro steps, and observations
4. evidence-check verifies whether the QA evidence supports the claimed verdict
5. the main agent integrates outputs, writes next action, and owns the final
   completion claim

Ownership boundaries:

- builder does not own final review, final QA judgment, or merge/integration
  authority
- reviewer does not gather screenshots or act as QA
- QA does not decide code quality
- evidence-check catches weak, contradictory, or low-context QA artifacts
- integration remains singular with the coordinating lane

Native Codex subagents are the default worker implementation when available.
Tmux-backed lanes are only an optional visibility/runtime wrapper for long-lived
visible workers; they are not the core QA delegation rule and not a hidden
orchestrator.

### 5b. Optional Serial Board Drain

`$ralph` may run after tickets are prepared, ideally inside a native Goal that
states the board-drain stopping condition.

It should:

- read active filesystem tickets
- select one ready, unblocked, dependency-safe, unclaimed, approval-free ticket
  or a safe related tiny-ticket batch
- hand the selected work unit to `$work`
- preserve per-ticket proof rows plus a batch regression row for batches
- reread the board after each work unit
- stop on no ready work, human gates, blockers, failed handoff, or loop limit

`$ralph` does not replace `$work` or `$impl` and does not own parallel dispatch
in the current system.

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

### 7. Goal And Stop Hook

Native Goal is the semantic continuation gate for Goal-backed work. It should
carry the outcome, verification surface, iteration policy, and blocked stop
condition.

The Stop hook is the mechanical active-ticket gate.

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
- the fuzzy autonomy checker for Goal-backed work

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

For `$work` or `batch-work` ticket batches, use a batch ledger:

| Ticket | Change | Local proof | Result | Blocker |
| --- | --- | --- | --- | --- |
| TASK-0001 | short change | focused check | pass/block/fail | none or evidence |
| Batch | combined regression | batch check | pass/block/fail | none or evidence |

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

- keep Farplane’s planning/spec/review surfaces
- keep the queue readable
- improve longer runs and stronger review before adding more runtime machinery

This means:

- stronger review loop first
- clearer progress surface first
- cleaner continuation behavior first
- serial dispatcher over filesystem tickets now
- parallel dispatcher/worktrees later if still needed
