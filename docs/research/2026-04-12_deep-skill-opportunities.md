# Deep Skill Opportunities

## Decision

Do not create `deep-*` variants for most skills.

Create exactly two new public deep skills:

- `deep-system-design`
- `deep-ui-design`

Then reuse the same multi-turn pressure-loop structure as an internal mode
inside a small set of existing planning and review skills.

That keeps the public workflow legible:

`brainstorm -> deep-interview -> deep-system-design -> functional-ui -> deep-ui-design -> frontend-design -> prd/spec -> spec-to-ticket -> impl-plan -> $impl -> review`

## Why

`deep-interview` works because it does four things the rest of the system often
does only once:

1. it keeps the mode active until readiness is explicit
2. it attacks ambiguity with one high-leverage question at a time
3. it pressure-tests prior answers instead of just collecting them
4. it crystallizes a reusable handoff artifact at the end

That same structure is useful when the unresolved problem is not user intent
but design decomposition, boundary quality, proof quality, or realism quality.

It is not useful for reference/index skills, one-shot transforms, or execution
plumbing.

## Recommendation

### Option 1: Make many public `deep-*` skills

Examples: `deep-prd`, `deep-spec`, `deep-review`, `deep-demo-realism`,
`deep-functional-ui`, `deep-impl-plan`.

Pros:

- explicit and easy to invoke
- each skill can optimize for its domain

Cons:

- public surface area explodes fast
- users have to learn which deep skill comes before which normal skill
- drift risk rises because every deep variant needs its own state machine

### Option 2: Keep only `deep-interview`, embed everything else invisibly

Pros:

- minimal public complexity
- fewer skills to maintain

Cons:

- system design remains underpowered as a first-class phase
- too much design pressure gets stuffed into `impl-plan`
- users lose a clear place to do architecture/decomposition before ticket-level planning

### Option 3: Add a small public deep family and embed deep modes elsewhere

Pros:

- solves the real gaps: architecture/decomposition quality and taste extraction
- keeps the public flow understandable
- lets existing skills borrow the same loop without multiplying names

Cons:

- requires a shared reusable deep-loop contract
- some skills need refactoring to support resumable multi-turn operation

## Best Path

Option 3.

The missing public phases are system design and UI taste extraction, not a
dozen different deep wrappers.
Your current harness already has:

- fuzzy intake: `brainstorm`
- intent clarification: `deep-interview`
- workflow recommendation: `functional-ui`
- visual execution/reference lookup: `frontend-design`
- requirements writing: `prd`
- ticket decomposition: `spec-to-ticket`
- ticket planning: `impl-plan`

What is thin is the space between clarified intent and executable planning:

- service decomposition
- responsibility boundaries
- interface contracts
- data ownership
- failure modes
- rollout shape
- what stays coupled vs extracted

That deserves one first-class skill.

Separately, there is also a gap between:

- "the workflow is right"
- "the visual taste is distinctive and user-aligned"

That deserves a second first-class skill.

## Proposed New Skill: `deep-system-design`

### Role

Use after `deep-interview` when the user intent is clear but the architecture is
not.

This skill should behave more like a Palantir-style decomposition interview than
a normal plan:

- ask one design-pressure question per round
- show and update an ambiguity score each round
- keep the session active until design readiness is explicit
- revisit earlier answers and attack weak seams
- force decomposition before implementation detail
- end with a reusable system-design artifact

### Shape parity with `deep-interview`

This should not just be "a good architecture prompt." It should reuse the same
control-loop shape as `deep-interview`:

1. preflight context intake
2. one-question-per-round interrogation
3. explicit ambiguity scoring after every answer
4. pressure-pass revisits of earlier claims
5. readiness gates that block handoff until critical design details exist
6. final crystallization into a reusable artifact

In other words, the difference is the target of the questioning, not the shape
of the mode.

### Entry modes

The skill should support two decomposition starts:

- **Customer-first**
  - start from the operator, workflow, and external contract
  - work backward into services, data, and execution boundaries
- **Data-first**
  - start from entities, events, and records of truth
  - work outward into APIs, jobs, ownership, and workflows

The system can pick one based on the problem, but it should make the chosen
mode explicit in the artifact.

### Core design dimensions

Score these explicitly each round:

- boundary clarity
- component responsibility clarity
- interface clarity
- data ownership clarity
- storage model clarity
- endpoint contract clarity
- execution model clarity
- parallelism strategy clarity
- queue/background-job clarity
- reliability-policy clarity
- failure-mode clarity
- operational clarity
- rollout/migration clarity
- non-goal clarity

### Stage order

1. System intent
2. decomposition tree
3. boundaries and ownership
4. entities, storage, and data contracts
5. interfaces, endpoints, and function signatures
6. runtime flows, parallelism, queues, and failure modes
7. rollout, migration, and proof

### Pressure modes

- **Decomposer**: split vague subsystems into responsibilities
- **Contrarian**: challenge unnecessary services, abstractions, or coupling
- **Load/Failure**: ask what breaks first and how it degrades
- **Operator**: force day-2 operational reality, not just happy-path diagrams
- **Simplifier**: ask what can stay monolithic for now

### Required output minimums

This skill should not exit with only a diagram and some prose. The minimum
artifact should be detailed enough that implementation agents can follow it as a
strict intermediate spec.

Required sections:

- `System Design Brief`
- `Architecture delta diagram`
- `Decomposition tree`
- `Entity model`
- `Database/storage choices`
- `Endpoint map`
- `Function signatures`
- `Background jobs and queues`
- `Parallelism model`
- `Reliability policy`
- `Runtime/deployment topology`
- `Configuration contracts`
- `Coding pattern decisions`
- `Open decisions`

### Required output details

The artifact should make these concrete:

- what entities/tables/documents exist
- what data each entity stores and which fields are canonical
- which database or storage system owns each category of data
- which endpoints, actions, or public interfaces exist
- the signatures for the important functions and handlers
- which work runs synchronously versus asynchronously
- what runs in-process, in background workers, in queues, or in orchestrators
- where parallelism is allowed and what the join boundaries are
- where rate limits apply
- where retries happen and what the idempotency strategy is
- which workflows might justify Temporal, Dagster, or similar orchestration
- how configuration is passed through the system
- what coding pattern decisions are fixed up front: functional style, class
  boundaries, module seams, handler/service split, and similar repo-shaping rules

### Readiness gates

Do not hand off while any of these are still vague:

- core entity model
- main function or endpoint signatures
- storage ownership
- sync vs async execution boundary
- background-job / queue model
- retry / idempotency / rate-limit policy
- deployment/runtime location of major components
- coding-pattern constraints that downstream agents are expected to follow

If those are missing, the ambiguity score should remain above threshold even if
the high-level diagram looks coherent.

### Required output artifact

Produce one `System Design Brief` containing:

- context and scope
- top-level architecture delta diagram
- decomposition tree
- explicit decomposition mode: customer-first or data-first
- component responsibility table
- entity and storage model
- endpoint map
- interface/function signature pack
- runtime execution topology
- parallelism and join-boundary notes
- queue/background-worker plan
- rate-limit, retry, and idempotency notes
- orchestration choice notes
- configuration contract summary
- coding-pattern decisions
- invariants and non-goals
- main failure modes
- rollout/migration shape
- proof plan
- open decision ledger
- handoff target: `prd`, `spec-to-ticket`, or `impl-plan`

## Where The Deep Pattern Should Be Reused

### First-class public deep skill

- `deep-interview`
  - keep as the intent/requirements clarifier
- `deep-system-design`
  - add as the architecture/decomposition clarifier
- `deep-ui-design`
  - add as the taste/style clarifier between workflow and visual build

### Existing skills that should gain an embedded deep mode or internal loop

- `prd`
  - good fit for a deeper multi-turn write/review loop
  - use when JTBD, slice boundary, or constraints are still soft after interview
  - likely shape: `prd --deep`
- `spec-to-ticket`
  - good fit as an internal decomposition review loop before ticket writeback
  - ask: is this really one slice, are dependencies in the right order, is agent testability explicit, what follow-up ticket is missing
  - likely shape: internal ticket-set challenge pass, not a new public skill
- `impl-plan`
  - strong fit for a design-review loop when a ticket still hides architecture choices
  - existing `--consensus` already points in this direction
  - likely shape: fold deep challenge into `--consensus` or add `--deep`
- `functional-ui`
  - should stay mostly static and recommendation-driven
  - it should infer the best workflow from comparable apps instead of interviewing the user at length
- `demo-realism`
  - useful when realism is still weak after one pass
  - likely shape: realism-pressure loop on operating model, records, timelines, and edge states
- `runtime-debugging`
  - useful as a persistent hypothesis loop
  - likely shape: stay active until one hypothesis is proven and the fix is verified, rather than acting like a one-pass checklist
- `review`
  - useful as a rerun-until-verdict loop for the reviewer lane
  - likely shape: keep challenging weak evidence or integration seams until the packet is either passable or clearly blocked

### Existing skills that should borrow only a small internal self-review, not a full deep mode

- `visual-qa`
  - already has a strong structured judgment contract
  - improve rerun discipline, not a separate `deep-visual-qa`
- `docs-closeout`
  - use a closeout checklist and archive-readiness review, but not a long interview loop
- `brainstorm`
  - keep divergent and lighter-weight; hand off to `deep-interview` or `deep-system-design`
- `repent`
  - recovery should stay immediate and short, not reflective and multi-turn

### Skills that should not become deep

- `commit-message`
- `bash-efficiency`
- `testing`
- `documentation`
- `codebase-analysis`
- `frontend-design`
- `diagramming`
- `convex`
- `data-viz`
- `three-js`
- `react-flow`
- `external-patterns`
- `find-skills`
- `init-project`

These are index, reference, transform, or execution-assist skills. Making them
multi-turn would mostly add ceremony.

## Proposed New Skill: `deep-ui-design`

### Role

Use after `functional-ui` when the workflow is clear but the user's visual
taste is still unclear.

This skill should exist to extract a distinctive aesthetic direction from the
human before `frontend-design` starts building.

### Shape parity with `deep-interview`

This should follow the same control-loop shape as `deep-interview`:

1. preflight context intake
2. one-question-per-round taste interview
3. explicit ambiguity scoring after every answer
4. pressure-pass revisits when taste claims are vague or contradictory
5. readiness gates before handoff
6. final crystallization into a reusable `Taste Brief`

### Why it should exist separately

`functional-ui` and `frontend-design` do different jobs:

- `functional-ui` decides how the product should work
- `frontend-design` builds and references implementation patterns

Neither is the right owner for a long multi-turn taste-extraction loop.

If the goal is to avoid samey AI-generated websites, you need a skill that
explicitly pulls out:

- emotional tone
- references
- anti-references
- typography appetite
- density preference
- motion comfort
- texture/depth preference
- boldness tolerance
- component-shape preference

### Core taste dimensions

Score these explicitly each round:

- originality clarity
- emotional-tone clarity
- typography-direction clarity
- color-system clarity
- density/spacing clarity
- motion-language clarity
- texture/material clarity
- reference quality
- anti-reference clarity
- component doctrine clarity

### Stage order

1. emotional and brand intent
2. references and anti-references
3. typography, color, and density
4. motion, texture, and composition
5. reusable component/system taste
6. anti-slop rules and final taste brief

### Pressure modes

- **Reference Interrogator**: ask what exactly is liked from a reference
- **Anti-Slop**: ask what should never appear
- **Extremes**: force a choice between safer and bolder directions
- **Consistency Check**: catch contradictions between references and desired tone
- **Systemizer**: convert vague mood language into reusable UI rules

### Required output artifact

Produce one `Taste Brief` containing:

- experience goal and emotional tone
- reference set
- anti-reference set
- typography doctrine
- color/material doctrine
- spacing and density doctrine
- motion doctrine
- component-shape doctrine
- imagery/illustration policy
- anti-slop rules
- canonical hero moments
- page/system notes for `frontend-design`

### Readiness gates

Do not hand off while any of these remain vague:

- at least 2 strong references and 1 anti-reference
- typography direction
- density preference
- color/material direction
- motion comfort level
- explicit anti-slop rules
- reusable component taste rules

If these are missing, `frontend-design` will regress to average-looking output.

## Practical Design Principle

Use the deep structure when all three are true:

1. the problem has unresolved judgment, not just missing information
2. the artifact benefits from pressure-testing and revisiting earlier answers
3. there is a meaningful readiness threshold before handoff

If one of those is missing, prefer a normal skill with a short built-in review
pass.

For `deep-system-design`, the minimum acceptable spec is not just "the idea is
clear." It is "the signatures, entities, execution boundaries, and operating
rules are explicit enough that an implementation agent can fill gaps without
inventing the system shape."

## Concrete Next Changes

1. Create `deep-system-design` as a new public skill between `deep-interview`
   and `prd` / `impl-plan`.
2. Create `deep-ui-design` as a new public skill between `functional-ui` and
   `frontend-design`.
3. Extract a shared deep-loop contract from `deep-interview`:
   - one-question rounds
   - explicit scoring dimensions
   - readiness gates
   - challenge modes
   - crystallization artifact
   - resumable state
4. Refactor these skills to adopt that contract internally:
   - `prd`
   - `impl-plan`
   - `spec-to-ticket`
   - `review`
   - `runtime-debugging`
5. Keep `functional-ui` static and recommendation-driven.
6. Keep `frontend-design` static and execution-oriented; it should consume the
   `Taste Brief` rather than own the interview.
7. Keep all other skills on lighter review loops unless real pain emerges.

## Suggested Public Workflow

For product/system work:

`brainstorm -> deep-interview -> deep-system-design -> prd -> spec-to-ticket -> impl-plan -> $impl -> review`

For UI-heavy product work:

`brainstorm -> deep-interview -> functional-ui -> deep-ui-design -> frontend-design -> impl-plan`

For brownfield ticket work:

`deep-interview --quick` only if intent is unclear -> `deep-system-design` only if architecture is still under-specified -> `impl-plan` -> `$impl` -> `review`

## Main Tradeoff Accepted

This chooses a clearer phase model over maximal surface reuse.

You will maintain two more public skills, but in exchange you stop overloading
`impl-plan` with upstream architecture work, you stop overloading
`frontend-design` with taste extraction, and you still avoid a noisy family of
`deep-*` variants that users have to memorize.
