# Proposal: Ideal Product Form Factor For RALF

Date: 2026-04-03

## Goal

Define the best product shape for `RALF` as an autonomous coding CLI that can take different input types, convert them into executable work, and keep moving with minimal operator interruption while preserving trust.

This proposal optimizes for:
- high operator trust
- minimal unnecessary pauses
- resumability after context loss
- support for both small and large inputs
- visible artifacts instead of hidden runtime magic

## Primary Inputs RALF Must Accept

RALF should accept four canonical input classes:

1. **Spec input**
   - Example: PRD, feature brief, long-form requirements doc
   - Needed behavior: discovery, decomposition, ticket creation, dependency graphing

2. **Task input**
   - Example: "fix this bug", "implement issue #42", one linear ticket
   - Needed behavior: direct normalization into one internal work item, then execute

3. **Board input**
   - Example: Notion card, kanban lane item, imported issue
   - Needed behavior: map external metadata into the internal execution contract

4. **Resume input**
   - Example: existing run id, existing internal ticket, interrupted session
   - Needed behavior: recover run state and continue from the next visible action

## The Core Design Decision

RALF should not treat "ticketing", "specs", and "runtime state" as competing systems.

Instead:
- the **external board** is a human-facing planning and prioritization surface
- the **internal work item** is the canonical execution contract
- the **run artifact** is the canonical execution-state surface for long-running autonomy

This gives one coherent model:
- large input -> many internal work items + dependencies
- small input -> one internal work item
- resumable long run -> one run artifact linked to the active internal work item

## Recommended Product Shape

RALF should be one product with distinct phases, not a single endless loop and not many unrelated workflow names.

Recommended surfaces:

### 1. `ralf intake`

Purpose:
- normalize any input into a standard request envelope

Output:
- input kind
- scope hypothesis
- ambiguity level
- likely touchpoints
- recommended next phase

### 2. `ralf spec`

Purpose:
- clarify ambiguous inputs
- create or refine a bounded spec

Use when:
- the input is broad, vague, or greenfield
- the request has no clear success criteria

Output:
- one compact execution-ready spec

### 3. `ralf ticketize`

Purpose:
- turn a spec or complex task into one or more internal work items
- attach dependencies and readiness signals

Output:
- one or more internal tickets
- dependency graph
- sequencing hints

### 4. `ralf run`

Purpose:
- select the next ready work item and execute it through the autonomy loop

Core loop:
- contract
- build
- prove
- review
- fix if needed
- close or block

Output:
- updated ticket
- updated run artifact
- visible next action

### 5. `ralf verify`

Purpose:
- normalize proof, QA, review, and acceptance coverage into one report shape

Output:
- pass/fail
- missing proof
- next required action

### 6. `ralf resume`

Purpose:
- recover a paused or interrupted run without rebuilding context from chat

Output:
- current phase
- current work item
- last verification state
- next visible action

## Canonical Entities

RALF should standardize around four entities:

### A. Request

The raw incoming thing:
- prompt
- spec
- issue
- board card
- existing ticket

### B. Work Item

The canonical execution contract:
- id
- title
- acceptance criteria
- dependencies
- phase
- status
- owner/runtime lane
- proof requirements
- operator resume packet

This can be stored as a local Markdown ticket with frontmatter plus constrained body sections.

### C. Run

The canonical execution-state container for a long-running autonomous attempt:
- run id
- autonomy mode
- active work item
- phase
- round
- last turn
- last verification
- next visible action

This should exist only when work is long-running, resumable, or phaseful.

### D. External Board Projection

The human-facing view:
- Notion board
- GitHub issue state
- simple kanban projection

This should not be the hot execution surface.

## Recommended Storage Ownership

### Local is canonical for execution

Local files should be authoritative for:
- internal work items
- run state
- proof artifacts
- operator resume
- per-round handoffs

Why:
- cheap repeated reads/writes
- easy diffing
- low latency
- less API fragility
- easier for agents to reason about

### External board is canonical for planning and prioritization

External tools such as Notion should be authoritative for:
- backlog visibility
- human prioritization
- approval state
- non-execution collaboration

Why:
- this matches how operators actually work
- preserves a clean planning UX

### Sync boundary

RALF should sync compact summaries back outward:
- status
- current phase
- blocker
- next action
- artifact links

It should not push every micro-update outward.

## Workflow For Different Input Sizes

### Small input

Example:
- one bug
- one issue
- one precise implementation request

Flow:
- `intake` -> create one work item -> `run`

No spec phase unless ambiguity is high.

### Medium input

Example:
- one feature with a few coherent steps

Flow:
- `intake` -> `spec` if needed -> one or more work items -> `run`

### Large input

Example:
- fresh product spec
- greenfield application
- major refactor

Flow:
- `intake` -> `spec` -> `ticketize` -> dependency graph -> repeated `run` over ready items

This is where Ralph-style decomposition matters most.

## What RALF Should Steal From Ralph/OMX

### From Geoffrey Huntley Ralph

Steal:
- fresh context between iterations
- strong bias toward one bounded task at a time
- externalized memory
- operator tuning via visible artifacts and prompt improvement

Do not steal blindly:
- pure while-loop minimalism as the whole product

Reason:
- it is excellent as a technique
- insufficient as the sole product form factor for mixed-input, resumable, multi-phase work

### From snarktank/ralph

Steal:
- explicit PRD -> task-list conversion
- single-story execution per iteration
- append-only learnings
- hard stop condition

Do not steal blindly:
- forcing JSON task lists as the only work-item format

Reason:
- local Markdown tickets are more operator-readable and already align with the existing harness direction

### From OMX

Steal:
- mode/state validation
- phase-aware runtime state
- per-turn lifecycle bookkeeping
- explicit verification as runtime data
- clear launch surfaces

Do not steal blindly:
- default auto-nudge / hidden continuation
- watcher-heavy control-plane complexity
- mode sprawl
- invasive tmux/runtime machinery for v1

## Assumptions And Tradeoffs

### Assumption 1: Internal work items are necessary

Pros:
- one execution contract for any input size
- support dependencies and readiness
- support resume and review
- easier for agents to reason about than raw board cards

Cons:
- adds a translation step from external sources
- can feel like duplicated state if synced poorly

Decision:
- accept this assumption
- keep internal work items canonical for execution

### Assumption 2: Run artifacts are needed for long-running work

Pros:
- resumability
- phase visibility
- easier stall diagnosis
- less dependence on chat history

Cons:
- second state surface if overused
- too much ceremony for tiny tasks

Decision:
- use run artifacts only for long-running, resumable, or multi-round work
- do not force them for every tiny task

### Assumption 3: Notion alone should not be the runtime surface

Pros:
- avoids API-heavy hot loops
- improves agent throughput and reliability
- keeps execution local and inspectable

Cons:
- requires sync discipline
- humans may prefer one tool

Decision:
- Notion stays a board projection, not the execution engine

### Assumption 4: Full autonomy needs explicit modes

Pros:
- clearer trust boundary
- easier adoption
- fewer surprises

Cons:
- adds one more concept to the product

Decision:
- keep only three modes:
  - `interactive`
  - `assisted-autonomous`
  - `full-autonomous`

## What Is Missing For Real Autonomy

These are the real blockers to "I stop using the tool because it pauses too much":

### 1. A planning gate

RALF needs to detect when input is too vague for direct execution and route it through `spec` first.

Without this:
- autonomy wastes loops on scope discovery
- operators have to re-steer constantly

### 2. Validated runtime state

RALF needs a small validated run-state object with:
- phase
- status
- round
- current work item
- last verification
- next visible action

Without this:
- resume remains fragile
- pauses become opaque

### 3. Passive per-turn telemetry

RALF needs cheap lifecycle bookkeeping:
- last agent turn
- current phase
- last proof result
- likely stall state

Without this:
- long runs are hard to trust
- operators discover stalls too late

### 4. A normalized verifier output

Proof needs one shape:
- what was checked
- what passed
- what failed
- what remains

Without this:
- review results stay too scattered
- automation cannot reliably decide next action

### 5. A strong operator resume packet

Every active work item or run needs:
- what happened
- what remains
- what blocked
- what to do next

Without this:
- every pause turns into a context rebuild

## What Not To Build In V1

Do not build these first:
- tmux/watcher-heavy continuation systems
- mailbox/lease/lock runtimes
- default auto-continue injection
- invisible board mutations
- multiple overlapping state systems
- many thin command aliases

These look advanced but will slow adoption unless the core execution contract is already trusted.

## Strongest V1 Recommendation

The best v1 product form factor is:

> **RALF as a phaseful CLI with internal work items as the execution contract and optional run artifacts for long-running autonomy.**

Concretely:
- Notion or another board can remain the human planning surface
- every input becomes one or more local internal work items
- `ralf run` executes exactly one ready work item through contract/build/prove/review
- `ralf spec` and `ralf ticketize` are invoked only when needed
- long-running work gets a run artifact with validated state and next action
- telemetry is passive and visible
- no hidden continuation by default

## Product Pitch

RALF should feel like this:

- give it anything: a spec, an issue, a board card, or a direct task
- it normalizes the input into executable work
- it decides whether the work needs clarification, decomposition, or direct execution
- it executes the next ready slice with clear proof requirements
- it leaves behind enough state that neither the user nor the model has to guess what happened

That is the real autonomy unlock.

The goal is not "a loop that keeps running."
The goal is:

> **a system that knows what it is doing, knows when it is blocked, knows what happens next, and can continue without wasting operator attention.**

## Bottom Line

If the product is designed well:
- small tasks feel fast because they become one work item and run directly
- large tasks feel tractable because they decompose into a visible dependency graph
- pauses become acceptable because resume is cheap
- trust rises because state and proof are visible

The ideal RALF is not just a better loop.

It is:
- a better intake model
- a better execution contract
- a better resume model
- a better autonomy boundary

## Sources

- Geoffrey Huntley, "Ralph Wiggum as a 'software engineer'" - https://ghuntley.com/ralph/
- Geoffrey Huntley, "i ran Claude in a loop for three months..." - https://ghuntley.com/cursed/
- snarktank/ralph - https://github.com/snarktank/ralph
