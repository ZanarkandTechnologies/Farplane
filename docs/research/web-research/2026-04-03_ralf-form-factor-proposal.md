# Research: Ideal RALF Form Factor

Date: 2026-04-03

## Scope

Define the ideal product form factor for `RALF` as a practical autonomous coding system:
- shaped for agent usability, not imitation
- capable of accepting heterogeneous inputs
- optimized to reduce unnecessary pauses
- opinionated about the minimum runtime substrate needed for trustable autonomy

This memo synthesizes:
- Geoffrey Huntley's "cursed" Ralph/Wiggum loop ideas
- `snarktank/ralph` as a lightweight implementation pattern
- `oh-my-codex` (OMX) as a heavier runtime reference
- current Codexter/Brute discussions and local research

## Executive Summary

The ideal `RALF` is **not** just:
- a bash loop
- a prompt pack
- a ticket board
- a tmux runtime

It is best understood as:

> an autonomy runtime that converts arbitrary operator input into one or more executable internal work items, then drives those work items through a bounded plan -> execute -> prove -> review loop with durable state, low-friction resume, and explicit proof of progress.

The core product decision is:

> keep human planning/project management flexible, but make agent execution strict.

That implies:
- external surfaces like Notion remain optional control-plane views
- internal work items become the canonical execution contract
- runtime state stays local and machine-friendly
- assisted continuation is visible and explicit, not hidden or injected by default

## What Ralph Means Across References

### Geoffrey Huntley Ralph / Wiggum pattern

What is strong:
- fresh context each loop
- one thing at a time
- externalized specs/files as durable memory
- simple operator-tunable shell surface
- especially good for greenfield generation

What is weak:
- less suitable as-is for brownfield repo work with many dependencies
- weak runtime observability
- weak structured handoff between planning and execution
- easy to drift into repeated loops without a richer progress model

Takeaway:
- steal the **fresh-context, externalized-memory, one-work-item** philosophy
- do not stop at a raw loop

### snarktank/ralph pattern

What is strong:
- PRD-first normalization
- structured JSON handoff
- one-story execution lane
- explicit progress file
- simple operator surface

What is weak:
- still narrow compared to a general heterogeneous-input autonomy system
- assumes a cleaner intake path than many brownfield workflows actually have

Takeaway:
- steal the idea that input should be normalized into a structured contract before execution

### OMX Ralph pattern

What is strong:
- real runtime substrate
- state validation
- hooks and per-turn updates
- persistent mode semantics
- planning gate (`ralplan`) before execution

What is weak:
- prompt-surface sprawl
- runtime complexity can outrun clarity
- hidden continuation pressure reduces operator trust
- tmux/watcher behavior is heavier than many workflows need

Takeaway:
- steal the runtime primitives
- reject hidden continuation and overgrown mode complexity

## Product Thesis

`RALF` should be a **general autonomy shell** with one canonical execution model:

1. accept any input shape
2. normalize it into one or more internal work items
3. pick a ready work item
4. run a bounded execution loop
5. collect proof
6. either close, branch, or block

That means the ideal product is:
- **input-flexible**
- **work-item strict**
- **runtime-light but real**
- **proof-driven**
- **resume-friendly**

## Canonical Entities

The product should have only a small number of first-class entities.

### 1. Intake

Raw user/operator input:
- freeform request
- spec doc
- bug report
- Notion card
- imported ticket
- existing local work item

### 2. Run

One top-level autonomous session:
- input source
- working directory
- autonomy level
- selected ready items
- timestamps
- logs
- resume metadata

### 3. Work Item

The canonical execution contract.

Every run should operate on one or more internal work items with:
- `id`
- `title`
- `source`
- `status`
- `phase`
- `dependencies`
- `acceptance criteria`
- `proof target`
- `resume packet`
- `runtime counters`
- `artifacts`

This is the load-bearing abstraction.
Whether the item originated from a Notion card, a pasted spec, or a single-line bug is irrelevant after normalization.

### 4. Projection Surfaces

Optional human-facing views:
- Notion board
- local board view
- CLI status
- markdown summaries

These should be projections of internal state, not the runtime substrate itself.

## Ideal Workflow

### Phase 1: Intake

Goal:
- accept heterogeneous input without making the operator pre-translate it

Behavior:
- identify the input class
- determine whether it is already executable
- if not executable, send it through spec/normalization

Examples:
- single bug with file path -> directly executable
- broad feature request -> needs normalization/spec
- PRD/spec doc -> split into executable work items
- Notion card -> import metadata, then normalize locally

### Phase 2: Normalize

Goal:
- produce a machine-friendly contract regardless of input shape

Outputs:
- one internal work item for linear tasks
- multiple dependency-linked work items for larger specs

Key rule:
- no direct execution against vague input if the system cannot define success

### Phase 3: Select

Goal:
- choose the next ready work item automatically

Selection inputs:
- dependency graph
- priority
- explicit operator pinning
- active run policy

Key rule:
- execution should happen against exactly one active work item per execution lane

### Phase 4: Execute

Goal:
- perform implementation work with minimal unnecessary pausing

The execution loop should be:
- bounded
- stateful
- observable

Default subphases:
- `build`
- `prove`
- `review`
- `fix`

This can stay close to the current Brute loop.

### Phase 5: Decide

After each loop, the system must choose one:
- continue same work item
- move to proof
- move to review
- block
- split follow-up work item
- mark done

### Phase 6: Sync

Goal:
- update optional external surfaces without making them the hot path

Sync targets:
- Notion
- board summaries
- docs/progress views

## The Core UX Decision

The biggest product decision is:

> should RALF be ticket-first, board-first, or prompt-first?

Recommended answer:

> input-flexible, work-item-first.

That means:
- operators can start from prompt/spec/board/ticket
- the system always executes against internal work items
- the board is a view, not the contract

Why this is better:
- works for both small and large inputs
- keeps execution logic uniform
- makes brownfield and greenfield share one substrate
- keeps external integrations optional

## The Missing Capabilities For Real Autonomy

These are the highest-value missing pieces between "useful runner" and "I trust this daily."

### 1. Planning gate

Problem:
- the system pauses because it does not know whether the input is executable yet

Needed capability:
- detect when input is underspecified
- automatically normalize/spec before execution

Why it matters:
- prevents wasted loops
- reduces pause frequency more than any other single feature

### 2. Validated runtime state

Problem:
- shell logic and prompt discipline alone are brittle

Needed capability:
- canonical run/work-item state
- validation on write/read
- explicit terminal semantics

Why it matters:
- trustable resume
- fewer nonsense states
- easier debugging

### 3. Per-turn progress telemetry

Problem:
- outer-loop progress is not the same as real progress

Needed capability:
- heartbeat on each agent turn
- `last_turn_at`
- progress summary
- stall candidate detection

Why it matters:
- distinguishes active thinking from dead air
- enables safer assistive autonomy

### 4. Resume packet

Problem:
- operators returning to a run should not need to reconstruct context from long transcripts

Needed capability:
- a compact operator resume surface per work item/run

Why it matters:
- large reduction in re-orientation cost

### 5. Proof-driven completion

Problem:
- autonomous systems over-claim completion

Needed capability:
- explicit proof targets
- proof sections/artifacts
- review reconciliation before done

Why it matters:
- raises trust
- lowers manual re-check burden

## What RALF Should Not Build First

These are seductive but lower ROI for v1.

### 1. Hidden continuation injection

Do not default to:
- automatic "yes, proceed"
- hidden tmux pane injection
- watcher-based continuation without operator visibility

Reason:
- reduces trust
- hides the autonomy boundary
- makes errors feel spooky rather than inspectable

### 2. Heavy team runtime

Do not start with:
- full mailbox/lease/worktree runtime
- tmux-first orchestration
- many execution modes

Reason:
- too much complexity before the single-lane execution model is right

### 3. Overgrown board semantics

Do not make the external board the runtime substrate.

Reason:
- high-churn machine state belongs in local machine-friendly state
- boards are for human control and visibility

## Assumptions And Tradeoffs

### Assumption: internal work items are canonical

Pros:
- uniform execution model
- easy dependency handling
- good resume/debug behavior

Cons:
- introduces another layer beyond Notion/external boards
- requires import/sync policy

Decision:
- worth it

### Assumption: external boards are projections, not hot-path runtime state

Pros:
- faster and more reliable execution loop
- less API fragility

Cons:
- requires sync discipline
- board may lag slightly behind runtime state

Decision:
- worth it

### Assumption: planning gate is mandatory for vague input

Pros:
- fewer dead-end execution loops
- less ambiguity-induced pausing

Cons:
- adds one front-loaded step for broad inputs

Decision:
- worth it

### Assumption: assisted continuation should be explicit, not hidden

Pros:
- operator trust
- easier mental model
- easier debugging

Cons:
- may be slightly less "hands-off" than aggressive auto-nudge systems

Decision:
- worth it

## Recommended Product Form Factor

The ideal form factor is:

### `ralf` as the umbrella product

Use `RALF` as the system/protocol name.

Suggested CLI shape:
- `ralf intake <input>`
- `ralf spec <input-or-run>`
- `ralf split <spec-or-item>`
- `ralf run [item]`
- `ralf status [run-or-item]`
- `ralf resume [run-or-item]`
- `ralf sync`

Or a more compact operator-friendly variant:
- `ralf start <input>`
- `ralf run`
- `ralf status`
- `ralf resume`
- `ralf sync`

Recommended product behavior:
- `ralf start` accepts anything
- the system decides whether to create one or many internal work items
- the system automatically selects a ready item unless the operator pins one
- the system runs a bounded build/prove/review/fix loop
- external surfaces are updated as projections

## Strongest Recommendation For V1

Build:

1. **Input normalization + planning gate**
2. **Canonical internal work-item schema**
3. **Single-lane bounded execution loop**
4. **Validated run/work-item state**
5. **Compact resume packet**
6. **Passive per-turn telemetry**

Do not build yet:

1. hidden continue injection
2. heavy team runtime
3. multiple autonomy modes
4. rich external board semantics as hot-path runtime

## Why This Will Increase Usage

The user's core complaint is not lack of raw capability.
It is:

> the system pauses too often when it does not know what to do.

The way to solve that is not "make it more aggressive."
It is:

> make the ambiguity resolution path and execution path explicit enough that the system rarely reaches a confused pause in the first place.

This design increases usage because it reduces the three biggest autonomy taxes:
- bad starts
- opaque stalls
- expensive resume/re-orientation

## Final Position

The ideal `RALF` is:

> a work-item-first autonomy shell with a mandatory normalization gate for ambiguous input, a bounded execution loop for active work, and a light but real runtime substrate for progress, proof, and resume.

That is the right middle ground between:
- Huntley's elegant simplicity
- OMX's runtime power
- Brute's ticket-first execution discipline

It is more usable than a raw Ralph loop, lighter than OMX, and more generally autonomous than Brute as it exists today.
