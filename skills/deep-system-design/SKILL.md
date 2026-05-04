---
name: deep-system-design
description: Socratic deep system-design interview with ambiguity gating before implementation planning. Use when user intent is clear but entities, signatures, storage, execution boundaries, queues, retries, and architecture choices are still under-specified.
argument-hint: "[--quick|--standard|--deep] [--customer-first|--data-first] <system, feature, service, or architecture idea>"
allowed-tools: Read, Glob, Grep
---

<Purpose>
Deep System Design is an architecture-first Socratic clarification loop before implementation planning. It turns vague statements like "build an ingestion pipeline" or "design the backend for this app" into a reusable `System Design Brief` with explicit entities, storage choices, endpoint maps, function signatures, background jobs, parallelism, reliability policy, UX-speed decisions, devx tradeoffs, and coding-pattern constraints.
</Purpose>

<Use_When>
- The request is clear at the product level but still vague at the system-design level
- The user wants architecture and decomposition before code
- The user says "deep system design", "do the system design first", "figure out the signatures", "what are the tables", or "work backward from the data/customer"
- `deep-interview` or normal discussion has clarified intent, but `agent-testability-plan`, `impl-plan`, or `spec-to-ticket` would still have to invent major system shape
- You need a strict intermediate spec between the idea and implementation
</Use_When>

<Do_Not_Use_When>
- The request already has clear file/symbol targets and little architectural ambiguity
- The task is primarily about product workflow or UI behavior; use `functional-ui`
- The task is primarily about visual taste; use `deep-ui-design`
- The architecture is already specified well enough that implementation planning should begin
</Do_Not_Use_When>

<Why_This_Exists>
Agents often produce weak system design because they jump from high-level intent to code without making the architecture explicit. A single design pass usually misses ownership boundaries, entity models, execution modes, queue boundaries, fan-out/fan-in strategy, retries, rate limits, deployment choices, UX-speed decisions, devx costs, and the repo-shaping coding rules that downstream agents should follow. This workflow applies Socratic pressure plus ambiguity scoring so implementation starts from an explicit, reusable, opinionated system brief instead of from guesses.
</Why_This_Exists>

<Depth_Profiles>
- **Quick (`--quick`)**: fast architecture pass; target threshold `<= 0.30`; max rounds 5
- **Standard (`--standard`, default)**: full system-design interview; target threshold `<= 0.20`; max rounds 12
- **Deep (`--deep`)**: high-rigor architecture/decomposition interview; target threshold `<= 0.15`; max rounds 20

If no flag is provided, use **Standard**.

<Mode_Flags>
- **`--customer-first`**: start from the operator, workflow, external contract, and request path, then work backward into services, data, and execution boundaries
- **`--data-first`**: start from the entities, events, records of truth, and storage model, then work outward into endpoints, jobs, and workflows
</Mode_Flags>
</Depth_Profiles>

<Execution_Policy>
- Ask ONE question per round (never batch)
- Ask about decomposition, ownership, and data/contract boundaries before implementation details
- Force explicit UX-speed and devx tradeoff reasoning for sync/async boundaries, queues, and orchestration choices
- Target the weakest system-design dimension each round after applying the stage-priority rules below
- Treat every answer as a claim to pressure-test before moving on: the next question should usually force an explicit signature, entity, boundary, execution tradeoff, reliability rule, or UX/devx rationale
- Do not rotate to a new design dimension just for coverage when the current answer is still vague; stay on the same thread until the system shape is reusable
- Before crystallizing, complete at least one explicit pressure pass that revisits an earlier answer with a sharper dependency, failure, or simplification challenge
- Gather codebase facts via repo inspection before asking the user about internals
- For brownfield work, prefer evidence-backed confirmation questions such as "I found X queue and Y storage pattern in the current codebase. Should this design preserve that or deliberately replace it?"
- Always run a preflight context intake before the first interview question
- Reduce user effort: ask only the highest-leverage unresolved question
- In Codex CLI, prefer `request_user_input` when available; otherwise use concise plain-text one-question turns
- Re-score ambiguity after each answer and show progress transparently
- Do not hand off to implementation while ambiguity remains above threshold unless the user explicitly opts to proceed with warning
- Do not crystallize or hand off while `Non-goals`, `Decision Boundaries`,
  `Autonomy Readiness`, or the required readiness gates remain unresolved, even
  if the weighted ambiguity threshold is met
- Treat early exit as a safety valve, not the default success path
- Persist mode state for resume safety (`state_write` / `state_read`)
</Execution_Policy>

<Steps>

## Phase 0: Preflight Context Intake

1. Parse `{{ARGUMENTS}}` and derive a short task slug.
2. Attempt to load the latest relevant context from the active ticket, linked specs/docs, and any persisted `state_read(mode="deep-system-design")` snapshot.
3. Inspect the current technical surface when the task is brownfield:
   - relevant tickets/specs
   - nearby schemas, handlers, workers, queues, and infrastructure config
   - existing API or data contracts
4. If no snapshot exists, create a minimum context snapshot with:
   - Task statement
   - Product/workflow context
   - Stated system ask
   - Probable architecture hypothesis
   - Known facts/evidence
   - Constraints
   - Unknowns/open questions
   - Decision-boundary unknowns
   - Likely modules/services/tables/jobs
5. Persist the snapshot in mode state and, when a ticket already exists, mirror the key points into the ticket `Working Notes` instead of creating sidecar runtime artifacts.

## Phase 1: Initialize

1. Parse `{{ARGUMENTS}}`, the depth profile (`--quick|--standard|--deep`), and the entry mode (`--customer-first|--data-first`).
   - If neither mode flag is provided, infer one explicitly before the first question:
     - prefer `--customer-first` when the problem is framed around user flow, request path, operator workflow, latency, or product behavior
     - prefer `--data-first` when the problem is framed around ingestion, pipelines, entities, records of truth, warehousing, indexing, or event processing
2. Detect project context:
   - classify **brownfield** (existing codebase target) vs **greenfield**
   - for brownfield, collect relevant codebase context before questioning
3. Initialize state via `state_write(mode="deep-system-design")`:

```json
{
  "active": true,
  "current_phase": "deep-system-design",
  "state": {
    "interview_id": "<uuid>",
    "profile": "quick|standard|deep",
    "entry_mode": "customer-first|data-first",
    "type": "greenfield|brownfield",
    "initial_idea": "<user input>",
    "rounds": [],
    "current_ambiguity": 1.0,
    "threshold": 0.3,
    "max_rounds": 5,
    "challenge_modes_used": [],
    "system_context": null,
    "current_stage": "operator-request-path | record-of-truth",
    "current_focus": "decomposition-root",
    "context_surface": "ticket:<path>#Working Notes | state:deep-system-design.context_snapshot"
  }
}
```

4. Announce kickoff with profile, entry mode, threshold, and current ambiguity.
5. State explicitly that the chosen entry mode changes the order of questioning and decomposition.

## Phase 2: Socratic System-Design Loop

Repeat until ambiguity `<= threshold`, the pressure pass is complete, the readiness gates are explicit, the user exits with warning, or max rounds are reached.

### 2a0) Apply the entry-mode branch

`entry_mode` is not metadata only. It must change the questioning path:

- **Customer-first path**
  - start from the user/operator request path
  - identify the visible interaction or trigger
  - decompose the request path into collaborating subsystems
  - derive the data written/read by each subsystem
  - then define jobs, queues, retries, rate limits, and runtime placement
- **Data-first path**
  - start from records of truth, entities, event streams, and storage boundaries
  - identify how data enters, changes, and is materialized
  - decompose the ownership graph around those data boundaries
  - then derive endpoints, jobs, request paths, and runtime triggers from the data model

If a question does not reflect the chosen path, rewrite it before asking.

### 2a1) Recursive decomposition rule

This skill must decompose recursively, not just list architecture topics once.

Use this working loop:

1. choose the current system, request path, or data root
2. split it into 2-5 child responsibilities
3. assign ownership and runtime boundary to each child
4. define each child's inputs, outputs, and stored data
5. recurse on any child that is still too vague to yield signatures and execution rules
6. stop recursion only when the leaf is explicit enough to answer the per-component interrogation contract

Do not leave decomposition as a flat component list when one or more nodes are still too vague to define signatures, storage, triggers, or execution choices.

### 2a) Generate next question

Use:
- Original idea
- Prior Q&A rounds
- Current dimension scores
- Brownfield technical context (if any)
- Activated challenge mode injection (Phase 3)

Target the lowest-scoring dimension, but respect the stage order for the chosen entry mode:

- **Customer-first**
  - **Stage 1 — Request path:** Operator Flow, Scope, Non-goals, Decision Boundaries
  - **Stage 2 — Runtime decomposition:** Components, Ownership, Runtime Boundaries
  - **Stage 3 — Contracts from the path:** Endpoints, Signatures, Entities, Storage, Configuration
  - **Stage 4 — Execution and reliability:** Sync/Async, Jobs, Queues, Parallelism, Retries, Rate Limits, Idempotency
  - **Stage 5 — Brownfield grounding:** Context Clarity (brownfield only)

- **Data-first**
  - **Stage 1 — Records of truth:** Entities, Storage, Ownership, Non-goals, Decision Boundaries
  - **Stage 2 — Dataflow decomposition:** Event sources, state changes, materializations, readers/writers
  - **Stage 3 — Contracts from the data model:** Endpoints, Signatures, Runtime Boundaries, Configuration
  - **Stage 4 — Execution and reliability:** Sync/Async, Jobs, Queues, Parallelism, Retries, Rate Limits, Idempotency
  - **Stage 5 — Brownfield grounding:** Context Clarity (brownfield only)

Question-generation rule by mode:

- **Customer-first questions** should sound like:
  - what is the first user/operator action or trigger?
  - what component receives it?
  - what child responsibilities does that request path split into?
  - which data does each step read/write?
  - which parts must stay inline for latency and which can move behind a job or queue?

- **Data-first questions** should sound like:
  - what are the records of truth and who owns them?
  - what events or writes create or mutate those records?
  - what derived views or materializations exist?
  - what endpoints/jobs consume or expose that data?
  - where should background processing, retries, or rate limiting wrap the dataflow?

Follow-up pressure ladder after each answer:
1. Ask for the concrete entity, endpoint, signature, or interface implied by the claim
2. Probe the hidden assumption, dependency, or coupling that makes the design work
3. Force a boundary or tradeoff: what stays synchronous, what moves to background, what stays monolithic, what is intentionally deferred, and why that improves UX or preserves devx
4. Ask what breaks first and how the system should degrade or recover
5. Ask whether fan-out/fan-in, queuing, retries, or rate limiting belong at this boundary and what operator/developer pain they introduce

Prefer staying on the same thread for multiple rounds when it has the highest leverage. Breadth without pressure is not progress.

At least one full recursive decomposition pass is required before crystallization:

- root -> child responsibilities
- child -> leaf responsibilities
- leaf -> signatures + execution choices

If the interview has not yet reached leaf-level contracts for the major branches, keep interviewing even if the top-level architecture sounds coherent.

Detailed dimensions:
- Scope Clarity — what the designed system actually covers
- Decomposition Clarity — component/service/module split
- Ownership Clarity — who owns each entity, flow, and runtime responsibility
- Entity Model Clarity — tables/documents/events/records of truth
- Storage Clarity — which database/storage system owns which data
- Endpoint Contract Clarity — external/public/internal interface map
- Signature Clarity — function/handler/job signature detail
- Execution Model Clarity — sync vs async, request path vs background path
- Queue/Background Clarity — jobs, workers, triggers, orchestration
- Parallelism Clarity — safe fan-out/join boundaries and concurrency model
- Reliability Policy Clarity — retries, idempotency, rate limiting, backoff, failure handling
- UX-Speed Rationale Clarity — why each execution choice makes the product feel faster or safer for the user
- DevX Rationale Clarity — why each execution choice is worth the operational and implementation complexity
- Runtime/Deployment Clarity — where things run and how they are triggered
- Coding Pattern Clarity — handler/service split, functional vs class boundaries, module seam rules
- Context Clarity — existing codebase understanding (brownfield only)

`Non-goals` and `Decision Boundaries` are mandatory readiness gates. Ask about them early and keep revisiting them until they are explicit.

### 2b) Ask the question

Use structured user-input tooling available in the runtime (`AskUserQuestion` / equivalent) and present:

```text
Round {n} | Target: {weakest_dimension} | Ambiguity: {score}%

{question}
```

### 2c) Score ambiguity

Score each weighted dimension in `[0.0, 1.0]` with justification + gap.

Greenfield:

`ambiguity = 1 - (scope × 0.10 + decomposition × 0.12 + ownership × 0.10 + entities × 0.12 + storage × 0.10 + endpoints × 0.08 + signatures × 0.10 + execution × 0.08 + queues × 0.06 + parallelism × 0.04 + reliability × 0.05 + runtime × 0.03 + coding_patterns × 0.02)`

Brownfield:

`ambiguity = 1 - (scope × 0.08 + decomposition × 0.11 + ownership × 0.09 + entities × 0.11 + storage × 0.09 + endpoints × 0.08 + signatures × 0.10 + execution × 0.08 + queues × 0.06 + parallelism × 0.04 + reliability × 0.05 + runtime × 0.03 + coding_patterns × 0.02 + context × 0.06)`

Readiness gate:
- `Non-goals` must be explicit
- `Decision Boundaries` must be explicit
- Core entity model must be explicit
- Main function or endpoint signatures must be explicit
- Storage ownership must be explicit
- Sync vs async boundaries must be explicit
- Fan-out / fan-in boundaries must be explicit where parallelism exists
- Background-job / queue model must be explicit when asynchronous work exists
- Retry / idempotency / rate-limit policy must be explicit where relevant
- UX-speed rationale must be explicit for major sync/async and queue decisions
- DevX rationale must be explicit for major queue/orchestrator/reliability decisions
- `Autonomy Readiness` must name required human inputs, permissions,
  credentials, compute, tools, QA risks, and human gates for unattended work
- A pressure pass must be complete: at least one earlier answer has been revisited with a dependency, failure, or simplification follow-up
- If any gate is unresolved, continue interviewing even when weighted ambiguity is below threshold

### 2d) Report progress

Show the weighted breakdown table, readiness-gate status (`Non-goals`, `Decision Boundaries`, `Entities`, `Signatures`, `Execution`, `Reliability`, `UX-Speed`, `DevX`), and the next focus dimension.

### 2e) Persist state

Append the round result and updated scores via `state_write`.

### 2f) Round controls

- Do not offer early exit before the first explicit signature/entity probe and one persistent follow-up have happened
- Round 4+: allow explicit early exit with risk warning
- Soft warning at profile midpoint (e.g. round 3/6/10 depending on profile)
- Hard cap at profile `max_rounds`

## Phase 3: Challenge Modes

Use each mode once when applicable. These are normal escalation tools, not rare rescue moves:

- **Decomposer** (round 2+): split vague subsystems into responsibilities
- **Contrarian** (round 2+): challenge unnecessary services, abstractions, or coupling
- **Load/Failure** (round 3+): ask what breaks first, what gets rate-limited, and how retries/backoff should work
- **Operator** (round 4+): force day-2 operational reality, deployment/runtime assumptions, and trigger paths
- **Speed/Ergonomics** (round 4+): force an explicit answer on whether queues, background jobs, or orchestration improve user-perceived speed enough to justify the developer/operator cost
- **Simplifier** (round 5+ or when the system sprawls too fast): ask what can stay monolithic, synchronous, or deliberately manual for now

Track used modes in state to prevent repetition.

## Phase 4: Crystallize Artifacts

When threshold is met (or the user exits with warning / hard cap):

1. Write the interview transcript summary to:
   - the active ticket `Working Notes` / `Handoff` when a ticket already exists
   - otherwise the current response as a compact `Deep-System-Design Summary`
2. Write the execution-ready system-design artifact to:
   - `docs/specs/<slug>.md` when the project has a specs surface and the design is spec-level
   - otherwise the active ticket when one already exists
   - otherwise the current response handoff plus the next canonical artifact owner, usually `agent-testability-plan`, `impl-plan`, or `spec-to-ticket`

### Canonical write-back rule

When the project has been bootstrapped with `deep-init-project`, durable system design should live on normal Codexter surfaces:

- spec-level reusable architecture doctrine -> `docs/specs/<slug>.md`
- ticket-local implementation-oriented design summary -> active ticket
- chat-only fallback -> current response when no durable project surface exists

Do not create hidden sidecar design artifacts. Keep the durable design brief on the visible specs/ticket surfaces that later planning and review can reuse.

The `System Design Brief` should include:
- Metadata (profile, entry mode, rounds, final ambiguity, threshold, context type)
- Context snapshot reference/path
- Clarity breakdown table
- System scope
- In-scope and non-goals
- Decision boundaries
- Decomposition tree
- Component responsibility table
- Entity model
- Database/storage choices
- Endpoint map
- Function/handler/job signature pack
- Component execution matrix
- Background jobs and queues
- Parallelism model
- Reliability policy
- UX-speed rationale
- DevX rationale
- Runtime/deployment topology
- Configuration contracts
- Autonomy Readiness: inputs/assets, permissions/credentials, external
  services, compute/runtime needs, tooling gaps, QA risks, human gates, and
  agent decision boundaries
- Coding pattern decisions
- Brownfield evidence vs inference notes for any repository-grounded confirmation questions
- Pressure-pass findings (which answer was revisited, and what changed)
- Full or condensed transcript

### Minimum acceptable `System Design Brief`

Do not exit with only architecture prose. The minimum brief must contain reusable build rules:

- explicit core entities/tables/documents/events
- explicit storage ownership
- explicit endpoint or interface map
- explicit important function/handler/job signatures
- explicit per-component execution matrix: trigger, runs where, sync/async, queue/orchestrator, fan-out/fan-in, join point
- explicit sync vs async boundaries
- explicit queue/background-worker/orchestrator plan when relevant
- explicit retry, idempotency, and rate-limit policy where relevant
- explicit UX-speed rationale for major execution choices
- explicit DevX rationale for major execution choices
- explicit runtime/deployment notes
- explicit autonomy-readiness notes for anything that can block a long-running
  agent mid-implementation or QA
- explicit coding-pattern constraints for downstream implementation agents

If those are missing, the brief is not implementation-ready.

### Required per-component interrogation

For each major component, subsystem, or job in the decomposition tree, force an
explicit mini-contract before moving on:

- `Responsibility`: what this unit owns
- `Trigger`: what starts it
- `Runs where`: request handler, worker, cron, orchestrator, client, edge, etc.
- `Sync or async`: and why
- `Queue/orchestrator`: none, queue, workflow engine, cron, webhook, etc.
- `Fan-out/fan-in`: where parallelism starts and where results rejoin
- `Rate limits`: where throttling applies
- `Retries/idempotency`: what can safely retry and how duplicates are prevented
- `User impact`: how this choice makes UX faster, safer, or more predictable
- `Developer/operator impact`: what complexity this adds or removes

If the skill cannot answer those questions for a major component, that component
is still under-designed and ambiguity should remain above threshold.

## Phase 5: Execution Bridge

Present execution options after artifact generation using explicit handoff contracts.

### 1. `agent-testability-plan` (Recommended when agent operability is the next question)
- **Input Artifact:** the current `System Design Brief`
- **Consumer Behavior:** treat the `System Design Brief` as the system source of truth, then derive the control accelerators, state probes, coordination views, and proof surfaces the agent will need later
- **Expected Output:** a reusable `Agent Testability Brief` on a visible spec/ticket surface
- **Best When:** the system shape is clear, but future tickets or plans would still have to guess what utilities, probes, or dashboards the agent should have

### 2. `impl-plan`
- **Input Artifact:** the current `System Design Brief` plus the active ticket when available
- **Consumer Behavior:** treat the `System Design Brief` as the system source of truth; do not reinvent entities, signatures, or runtime boundaries by default
- **Expected Output:** an implementation plan that preserves the designed system shape and proof requirements
- **Best When:** architecture is clarified and the next step is approval-ready execution planning

### 3. `spec-to-ticket`
- **Input Artifact:** the current `System Design Brief`
- **Consumer Behavior:** preserve the decomposition, contracts, and proof shape when splitting into tickets
- **Best When:** the architecture is clear but the work still needs dependency-ordered ticketization

### 4. `runtime-debugging`
- **Input Artifact:** the current `System Design Brief`
- **Consumer Behavior:** use the explicit runtime boundaries, queues, and reliability assumptions as the debugging baseline
- **Best When:** the design work is for a failing brownfield system that will likely need instrumentation or root-cause proof next

## Top Gotchas

1. Do not crystallize a design that lacks explicit signatures; downstream agents will invent them.
2. Do not skip entity/storage ownership; without it, the database shape and runtime responsibilities drift immediately.
3. Do not add queues, workers, retries, or orchestration by vibes alone; force the trigger path, failure mode, and idempotency story to be explicit.

## Outcome Contract

When this skill is used, the response or artifact must include:

1. Interview metadata and final ambiguity score
2. Clarity breakdown table
3. Explicit readiness-gate status
4. A reusable `System Design Brief`, written to visible specs/ticket surfaces
5. Entity/storage map
6. Endpoint/signature pack
7. Execution/reliability model
8. Autonomy-readiness blockers and human gates
9. Clear handoff target (`agent-testability-plan`, `impl-plan`, `spec-to-ticket`, or `runtime-debugging`)

</Steps>
