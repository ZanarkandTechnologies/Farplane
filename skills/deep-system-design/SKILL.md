---
name: deep-system-design
description: "Turn underspecified architecture intent into an implementation-ready System Design Brief."
tier: 2
source: local
argument-hint: "[--quick|--standard|--deep] [--customer-first|--data-first] <system, feature, service, or architecture idea>"
allowed-tools: Read, Glob, Grep
---

# Deep System Design

## Context

Use this before implementation planning when product intent is clear but the
architecture, entities, ownership, execution boundaries, or contracts are not.
Do not use it for a file-local implementation, settled architecture, primarily
UI work, or visual taste.

Read [workflow.md](references/workflow.md) before running this skill. It owns
the depth profiles, interview stages, scoring, challenge modes, writeback
details, and complete System Design Brief schema.

## Skill Signature

```text
deep_system_design(intent, local_evidence, profile?, entry_mode?)
  -> SystemDesignBrief + durable_owner + handoff
state: ticket/spec context + optional resumable interview state
gates: non_goals + decision_boundaries + contracts + execution + reliability
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] Read the active ticket, relevant specs, nearby architecture, and
  `docs/MEMORY.md` only when it answers a named architecture question.
- [ ] Load the full workflow reference; choose `quick`, `standard`, or `deep`,
  then state the `customer-first` or `data-first` entry path.
- [ ] For brownfield work, inspect current entities, schemas, handlers, jobs,
  queues, and infrastructure before asking the operator about internals.
- [ ] Use [reference-grounding](../reference-grounding/SKILL.md) to separate
  observed architecture from assumptions before recommending a system shape.
- [ ] Ask one highest-leverage question per round; recursively decompose until
  major leaves have ownership, contracts, storage, and execution choices.
- [ ] Make non-goals, decision boundaries, autonomy readiness, sync/async,
  reliability, UX-speed, and DevX tradeoffs explicit.
- [ ] Run one pressure pass that challenges a prior assumption, dependency,
  failure mode, or unnecessary abstraction.
- [ ] Do not crystallize while a required gate is unresolved, even if the
  ambiguity threshold is met; an explicit user warning is the only early exit.
- [ ] Write the System Design Brief to its active ticket or canonical spec, then
  hand off to `agent-testability-plan`, `impl-plan`, `spec-to-ticket`, or
  `runtime-debugging`.
- [ ] Use the [review protocol](../review/SKILL.md) before treating a material
  brief as ready for downstream implementation planning.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Operating Contract

```text
intent + local evidence
  -> interview(profile, entry_mode)
  -> System Design Brief
  -> ticket | spec
  -> next owner
```

- `customer-first` starts at the operator request path; `data-first` starts at
  records of truth. The chosen path must change the questioning order.
- A ready brief names scope/non-goals, decisions, decomposition, entities and
  storage, interfaces/signatures, execution/queues, reliability, runtime,
  UX-speed and DevX rationale, autonomy constraints, and evidence/inferences.
- Keep the durable brief on a visible ticket or spec. Do not create hidden
  sidecar design artifacts.

## Output

Return or write a concise readiness summary with the selected path, unresolved
gates or final ambiguity, durable artifact location, and named handoff.
