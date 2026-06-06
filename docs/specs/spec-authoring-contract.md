# Spec Authoring Contract

Status: Draft v1

Purpose: Define when Farplane should use a PRD, a system spec, or a ticket plan,
and provide a reusable Symphony-style section template plus conformance matrix
for complex runtime/service work.

## 1. Layer Split

| Artifact | Owns | Does not own |
| --- | --- | --- |
| PRD | user stories, product motivation, success feel, constraints, non-goals | detailed state machines, config schema, full test matrix |
| System spec | domain model, ownership, interfaces, execution modes, config, state, failures, observability, conformance | ticket-local execution proof or final QA artifacts |
| Ticket | one build/review loop, concrete file plan, acceptance criteria, evidence, blockers, closeout state | whole-system theory or raw source research |

Default rule: keep PRDs readable, make serious specs testable, and make tickets
executable.

## 2. Spec Depth Decision

```ts
type SpecDepth = "light" | "system" | "service-runtime";
```

### `light`

Use when the work is a small local behavior, a narrow doc/rule update, or a
single-surface workflow note.

Required:

- problem / decision,
- scope and non-goals,
- owner surface,
- verification or review hook.

### `system`

Use when multiple modules, skills, adapters, or tickets need one reusable
contract.

Required:

- goals and non-goals,
- ownership model,
- domain model,
- core interfaces or signatures,
- state or lifecycle,
- failure handling,
- follow-up ticket map,
- verification checklist.

### `service-runtime`

Use when the design includes scheduling, queues, external runners, retries,
workspace/process lifecycle, long-running coordination, credentials, or
operator observability.

Required:

- all `system` sections,
- config schema,
- explicit state machines,
- failure/recovery model,
- observability/status surfaces,
- safety and trust boundaries,
- conformance matrix,
- implementation checklist.

## 3. Template For System / Service Specs

Use this outline when a spec depth is `system` or `service-runtime`:

1. `Status` and `Purpose`
2. `Core Decision`
3. `Goals`
4. `Non-Goals`
5. `Ownership Model`
6. `Mode Map` or `Top-Level Flow`
7. `Domain Model`
8. `Configuration` or `Policy`
9. `State Machines` or lifecycle
10. `Failure Model`
11. `Observability And Proof`
12. `Safety Rules`
13. `Conformance Matrix`
14. `Follow-Up Ticket Map`
15. `Implementation Checklist`
16. `References`

Do not force every heading into small specs. The template is a tool for
runtime-grade clarity, not a tax on every ticket.

## 4. Domain Model Guidance

Define named entities before describing flows. A good spec makes it easy to
answer:

- what is the record of truth?
- which component creates, reads, updates, and deletes it?
- which fields are stable identifiers versus display labels?
- which fields are implementation-defined?
- what is normalized before downstream code sees it?

Use compact TypeScript-like sketches even for non-TypeScript systems when they
make the data contract easier to review.

## 5. State And Failure Guidance

For runtime-like systems, state and failure sections are required because they
prevent hidden orchestration drift.

Minimum state detail:

- entry trigger,
- in-progress states,
- terminal states,
- retry/reentry path,
- cancellation or human-gate path.

Minimum failure detail:

- config/read failure,
- adapter/input failure,
- execution failure,
- proof/write failure,
- external service failure,
- operator-visible recovery action.

## 6. Conformance Matrix Template

Use a table like this:

| Area | Requirement | Profile | Proof | Ticket |
| --- | --- | --- | --- | --- |
| workflow loading | config parses and required defaults apply | core | unit test / validator | `TASK-XXXX` |
| adapter normalization | raw board item maps to `WorkItem` | core | fixture test | `TASK-XXXX` |
| failure handling | unsupported compute blocks without fallback | core | JSON fixture | `TASK-XXXX` |
| observability | proof packet links commands and review artifacts | core | artifact review | `TASK-XXXX` |
| optional extension | external runner shim works in dry-run | extension | smoke artifact | `TASK-XXXX` |

Profiles:

- `core`: required for the shipped capability.
- `extension`: required only when the optional adapter/runtime is implemented.
- `real-integration`: environment-dependent smoke or credential-backed proof.

## 7. Example: Board And Compute Orchestration

`docs/specs/invocation-and-adapters.md` is a `service-runtime`-depth spec
because it defines:

- board adapters,
- compute targets,
- local and future external execution modes,
- state machines,
- failure handling,
- observability/proof,
- safety boundaries,
- conformance matrix,
- follow-up ticket map.

The PRD remains user-story level. The tickets carry the build proof. The spec
is the reusable contract between them.

## 8. Skill Handoffs

- `deep-system-design` should choose the spec depth when the design is reusable
  or runtime-like.
- `spec-to-ticket` should inspect the conformance matrix and slice tickets
  around proofable requirements.
- `impl-plan` should use the spec as the source of truth for entities,
  signatures, boundaries, and proof expectations, not re-litigate the system
  architecture.
- `review` should score complex specs with `spec-contract`,
  `implementation-plan`, `integration-readiness`, `evidence-quality`, and
  `debloatability` when bloat risk is material.

## 9. Anti-Bloat Rules

- Do not put service-runtime sections in PRDs.
- Do not copy full specs into tickets.
- Do not add config/state/failure sections when the work is a small local rule
  or one-file fix.
- Do not make a conformance matrix without proof columns.
- Do not invent a new template when this one already covers the needed depth.
