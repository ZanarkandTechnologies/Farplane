---
title: Farplane Program Language Audit Decision Note
status: draft
owner: codex
created_at: 2026-06-22
context_ref: experiments/decisions/2026-06-22-farplane-program-language-audit/context.md
skill: deliberative-advice
---

# Farplane Program Language Audit Decision Note

## Decision

Farplane should standardize on one semantic kernel with multiple thin
projections, not one syntax everywhere.

The canonical kernel should be owned by `docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md` and
should remain close to:

```text
ProgramNotation := Params + Steps + Bindings + State + Gates + Metrics
                 + Evidence + Automation + Review + Next
```

The projection rule should be:

```text
canonical_program(surface_artifact)
  -> ProgramNotation + validation_result + evidence_refs
```

## Stakes

The operator reports that Farplane has too many standards and languages to
learn. The decision affects skill authoring, tickets, Goal Packets, invocation
adapters, proof packets, review/QA surfaces, future integrations, and agent
prompt burden.

A good result reduces cognitive load and increases reuse without flattening
Farplane's useful ownership boundaries.

## Grounding

Current repo evidence shows real dialect diversity:

- `docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md` already names the problem and defines a
  common intermediate notation.
- `docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md` preserves separate ownership for
  `ticket.md`, `program.md`, and `progress.md`.
- `docs/features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md` uses TypeScript-like contracts for
  `FarplaneRunEnvelope`, `BoardAdapter`, `WorkItem`, `ComputeDecision`, and
  `ProofPacket`.
- `docs/fundamentals/harness-algebra.md` uses compact function notation such as
  `H(task, state) -> output + evidence + state_delta`.
- `docs/skills/system.md` owns `Skill Signature` and `Todo List` conventions.
- `tickets/README.md` owns frontmatter and the compact `Program` body shape.
- `skills/goal-advisor/SKILL.md` explicitly warns that `program.md` is loop
  configuration, not a second ticket.
- `skills/farplane-invocation/SKILL.md` keeps invocation as validation,
  routing, and proof writing, not a runner.

The evidence supports the operator's intuition that there are many languages,
but it also shows that most dialects have legitimate local affordances.

## Perspectives

### Operator Value

Recommendation: choose one semantic kernel with multiple projections.

Strongest reason: the operator learns one conceptual spine, then each artifact
becomes a familiar projection instead of a new language.

Risk: "multiple projections" can become a nicer label for continued sprawl
unless field names, examples, and ordering are standardized aggressively.

### Engineering Risk

Recommendation: standardize fields and validation contracts, not one universal
surface syntax.

Strongest reason: this gets the maintainability win with the least migration
churn. Existing Markdown, Goal Packet files, TypeScript-like contracts, and
Python validators can keep their local strengths.

Risk: a semantic kernel becomes documentation theater unless there are
validators, round-trip examples, and clear projection ownership.

### Evidence Skeptic

Recommendation: adopt the semantic kernel as a draft standard only after a
small round-trip prototype.

Strongest reason: repo evidence already points this way, but does not yet prove
that dialect mismatch is the main source of failures.

Risk: the council may overfit to clean conceptual docs while real mistakes may
come from stale docs, weak tickets, or missing validators.

### Systems Fit

Recommendation: `docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md` owns the shared semantic
vocabulary; each existing surface owns its projection.

Strongest reason: a single syntax everywhere would blur boundaries Farplane
depends on: tickets own task contracts, Goal `program.md` owns loop config,
skills own reusable workflow steps, and invocation owns runtime boundaries.

Risk: a new kernel without projection conformance checks adds abstraction
without reducing complexity.

### Language Design

Recommendation: use three projection families:

- Markdown/YAML for human-authored artifacts.
- Compact function notation for agent-facing contracts.
- TypeScript/Python schemas for public runtime contracts and validators.

Strongest reason: this matches what agents and tools already handle well.
Agents read Markdown instructions well, parse signatures quickly, and can
validate structured data through Python/TypeScript tooling.

Risk: loose projection rules would keep ad hoc pseudocode alive under a new
name.

## Critique / Ranking

### Option 1: Semantic Kernel With Thin Projections

This is the best fit.

It reduces cognitive load while preserving why each surface exists. It also
matches the existing `program-notation` spec, so the migration is refinement
rather than reinvention.

Accepted cost: validators and examples become mandatory. Without them, this
option fails.

### Option 2: Keep Current Multi-Dialect System

This is safest short-term.

It avoids churn and respects that the system already works. However, it does
not solve the operator's core pain, and it leaves every future agent to infer
projection rules from scattered docs.

Accepted cost if chosen: Farplane stays powerful but hard to onboard.

### Option 3: One Syntax Everywhere

This is appealing for teaching and validation.

It would make the system easier to explain at first glance. But it would likely
make skills and tickets less readable, over-code human task memory, and blur
Goal/ticket/invocation ownership boundaries.

Accepted cost if chosen: high migration churn and loss of local affordances.

## Recommendation

Adopt Option 1.

Do not rewrite Farplane into Python, TypeScript, Elixir, YAML, or a custom DSL.
Instead:

```text
FarplaneProgram =
  semantic_kernel
+ human_projection(Markdown + YAML frontmatter)
+ agent_projection(function signatures + compact steps)
+ machine_projection(TypeScript interfaces + Python/Pydantic or JSON Schema)
```

Use this rule:

```text
surface_artifact
  -> normalize_to_program_notation()
  -> validate_projection()
  -> round_trip_or_report_drift()
```

## Dissent

The strongest dissent favors one syntax everywhere, likely YAML or
TypeScript-like schemas.

That path would be easier to lint, diff, document, and teach in a vacuum. It
may be right if a prototype shows that agents and the operator author and
debug artifacts faster in one schema without losing readability.

The current evidence does not justify that migration yet.

## Tradeoff Accepted

Farplane accepts a small amount of syntax diversity in exchange for preserving
surface fit:

- Skills stay checklist-first.
- Tickets stay compact Markdown task memory.
- Goal `program.md` stays loop configuration.
- Invocation/adapters stay typed runtime boundaries.
- Proof packets stay structured evidence.
- Function notation stays an agent-facing contract shorthand.

The standardization target is semantic sameness, not visual sameness.

## Confidence

Medium-high.

Confidence is high that one syntax everywhere is the wrong default. Confidence
is medium that the current `ProgramNotation` fields are exactly complete,
because that should be tested with representative artifacts.

## Next Owner

Create a ticket owned by `harness-advisor` with support from
`skill-maintenance` and `goal-advisor`.

Suggested ticket title:

```text
TASK-XXXX Standardize ProgramNotation projections across core Farplane surfaces
```

## Proof / Evidence Gap

Before broad edits, run a small prototype:

1. Pick 1 skill, 1 ticket, 1 Goal Packet, and 1 invocation/proof envelope.
2. Normalize each into `ProgramNotation`.
3. Render each back into its original projection.
4. Validate that meaning is preserved.
5. Record drift: missing fields, ambiguous ownership, invalid evidence refs,
   unbound gates, or duplicated state.

Prototype signature:

```text
program_projection_prototype(skill, ticket, goal_packet, invocation)
  -> normalized_programs[]
   + round_trip_drift[]
   + validator_requirements
   + migration_ticket
```

Pass condition:

- the prototype reduces ambiguity without making human artifacts harder to
  read;
- validators catch real projection drift;
- the resulting standard can be explained in one page plus examples.

## Draft Standard

### Canonical Fields

Use these names everywhere when the concept appears:

- `params`
- `steps`
- `bindings`
- `state`
- `gates`
- `metrics`
- `evidence`
- `automation`
- `review`
- `next`

No surface has to expose every field. Every material surface should map to the
fields it does expose.

### Projection Ownership

- `docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md`: canonical semantic vocabulary and
  projection conformance rules.
- `docs/skills/system.md`: skill signatures, Todo Lists, and skill projection.
- `tickets/README.md`: ticket frontmatter/body projection.
- `docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md`: Goal Packet boundaries and projection.
- `docs/features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md`: envelope, adapter, compute, and
  proof schemas.
- Python/Pydantic or JSON Schema validators: normalized validation and drift
  detection.

### Syntax Policy

- Markdown is the default human surface.
- YAML frontmatter is metadata and routing, not the full program language.
- Function notation is for compact contracts only:

  ```text
  thing(input, state?) -> output + evidence + state_delta
  ```

- TypeScript-style interfaces are for public runtime contracts and adapter
  boundaries.
- Python/Pydantic or JSON Schema is for validators and migration tooling.
- Pipeline notation is explanatory only, not canonical syntax.
- Mermaid and prose diagrams are explanation surfaces, not executable language.

## Review Notes

The council used independent lanes with a durable context packet. All five
lanes converged on the same recommendation. The main unresolved evidence gap
is prototype proof that the semantic kernel reduces mistakes and does not add
another layer of abstraction.
