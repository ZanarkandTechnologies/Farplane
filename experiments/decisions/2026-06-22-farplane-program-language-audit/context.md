---
title: Farplane Program Language Audit Council Context
status: draft
owner: codex
created_at: 2026-06-22
decision_type: deliberative-advice
---

# Farplane Program Language Audit Council Context

## Decision

Should Farplane standardize the custom program language used across skills,
tickets, Goal Packets, invocation envelopes, adapters, proof packets, and
harness docs? If yes, what should the standard be and what should remain as
surface-specific projection?

## Why This Matters

The operator feels there are too many languages and standards to learn. The
desired outcome is higher reusability and clearer composition: each component
should connect with the others through the same conceptual language instead of
forcing agents and humans to translate between many local dialects.

This is a high-leverage design decision because it touches:

- skill authoring and first-load todo lists
- ticket planning and `Program` sections
- Goal Packet `ticket.md`, `program.md`, and `progress.md`
- invocation adapters and compute/proof contracts
- review, QA, and proof surfaces
- future integration with TypeScript, Python, and external runners
- prompt/context burden for future agents

## Prior Discussion Summary

The operator suspects Farplane has accumulated too many standards and asks for
max-council deliberative advice rather than immediate edits. The operator also
suggests optimizing for languages agents are trained on and already use well:
math/function notation, Elixir-style functional composition, Python, and
TypeScript.

## Current Behavior

Farplane currently uses multiple related dialects:

- Markdown frontmatter YAML for tickets, skills, and docs.
- Markdown body sections for human-readable contracts.
- `Skill Signature` blocks such as
  `skill(task, state) -> artifact + evidence + state_delta`.
- `## Todo List` checklists inside `SKILL.md` as executable first-load steps.
- Ticket `Program` blocks with `vars:` and pseudocode operations.
- Goal Packet files where `ticket.md` owns task contract, `program.md` owns
  loop config, and `progress.md` owns observed execution.
- TypeScript-like contracts for `BoardAdapter`, `WorkItem`,
  `FarplaneRunEnvelope`, `ComputeDecision`, and `ProofPacket`.
- Algebraic harness notation such as `H(task, state) -> output + evidence +
  state_delta`.
- Mermaid diagrams for human workflow maps.
- Python scripts and validators for live implementation.

`docs/specs/program-notation.md` already proposes a common intermediate
notation:

```text
ProgramNotation := Params + Steps + Bindings + State + Gates + Metrics
                 + Evidence + Automation + Review + Next
```

It explicitly says every surface does not need the same Markdown shape, but
should project into the common intermediate notation.

## Expected Behavior

A future standard should make Farplane easier to learn, compose, validate, and
extend without flattening all surfaces into an awkward single file syntax.

The standard should answer:

- What is the one semantic model?
- Which syntax should humans see by default?
- Which syntax should machines validate?
- Which syntax should agents use in prompts and skill signatures?
- How do skills, tickets, Goal Packets, invocation, and proof map into the same
  fields?
- What should be deprecated or renamed?
- What is the migration path with low churn?

## Options Under Consideration

### Option A: Keep Current Multi-Dialect System

Keep the current system mostly as-is. Clarify docs and add examples, but do not
attempt to standardize deeply.

### Option B: One Semantic Kernel, Multiple Projections

Standardize a small canonical semantic kernel and projection rules. Keep
Markdown where humans need readability, TypeScript/Python schemas where tools
need validation, and function signatures where agents need compact contracts.

### Option C: One Syntax Everywhere

Force skills, tickets, Goal Packets, invocation, and proof into a single syntax
family, likely YAML or TypeScript-like object schemas.

### Option D: Adopt an External Language

Make Python, TypeScript, Elixir-style pipelines, or a formal DSL the primary
program language across Farplane.

## Known Evidence

- `docs/specs/program-notation.md` already names dialect sprawl and proposes a
  common intermediate notation.
- `docs/specs/goal-loop-contract.md` defines `GoalPacket`, `ticket.md`,
  `program.md`, and `progress.md` ownership.
- `docs/specs/invocation-and-adapters.md` defines TypeScript-like runtime
  contracts for invocation, adapters, compute, and proof.
- `docs/fundamentals/harness-algebra.md` defines the core harness function
  `H(task, state) -> output + evidence + state_delta` and mini-harness
  composition.
- `docs/skills/system.md` defines skill signatures, Todo Lists, tier model,
  phase ownership, and source ownership.
- `tickets/README.md` defines ticket frontmatter, ticket body shape, and
  `task_program(vars, operations, proof) -> artifact + evidence + state_delta`.
- `skills/goal-advisor/SKILL.md` defines Goal Advisor as execution compiler
  and warns not to treat `program.md` as a second ticket.
- `skills/farplane-invocation/SKILL.md` defines invocation as validation,
  routing, and proof writing, not a hidden runner.

## Relevant Files

- `docs/specs/program-notation.md`
- `docs/specs/goal-loop-contract.md`
- `docs/specs/invocation-and-adapters.md`
- `docs/fundamentals/harness-algebra.md`
- `docs/skills/system.md`
- `tickets/README.md`
- `tickets/templates/ticket.md`
- `skills/goal-advisor/SKILL.md`
- `skills/farplane-invocation/SKILL.md`
- `templates/global/AGENTS.md`
- `AGENTS.md`

## Constraints And Non-Goals

- Do not silently implement a cross-repo migration in this council pass.
- Do not remove readable Markdown checklists from skills without proof that
  agents perform better with the replacement.
- Do not turn Farplane into a hidden runtime or daemon as part of language
  cleanup.
- Do not introduce a novel heavy DSL unless it clearly beats existing agent and
  tool affordances.
- Preserve current tickets, skills, and Goal Packet semantics unless the
  recommendation names a deliberate migration.
- Optimize for future agents and humans reconstructing state from files alone.

## Lane Briefs

### Operator Value

Judge by learnability, cognitive load, taste, speed of use, and whether the
standard makes the system feel like pieces snap together.

### Engineering Risk

Judge by implementation cost, migration churn, validator feasibility,
backwards compatibility, integration failure modes, and maintainability.

### Evidence Skeptic

Judge what is actually supported by current repo evidence versus intuition.
Name what evidence would change the recommendation.

### Systems Fit

Judge ownership boundaries: which surface should own the standard, which
surfaces should only project from it, and where standardization would create
hidden coupling.

### Language Design

Judge syntax choices against agent priors and tool ecosystems: mathematical
function notation, Python, TypeScript, YAML/Markdown, and Elixir-style
pipelines. Recommend the smallest coherent language family.

## Output Shape

Each lane should return:

- `Perspective`
- `Recommendation`
- `Strongest reason`
- `Biggest risk`
- `Strongest opposing point`
- `Evidence that would change my mind`
- `Concrete standardization constraints`

The chair synthesis should compare exactly three viable final options, choose
one, preserve dissent, name confidence, and specify the next owner/proof
surface.

## Critique And Ranking Plan

After first-pass lanes are collected, rank the options by:

1. Reduces cognitive load for agents and operator.
2. Improves reuse/composition across skills, tickets, Goals, invocation, and
   proof.
3. Preserves human-readable Markdown surfaces where they are working.
4. Enables validation without forcing every artifact into code.
5. Minimizes migration churn and avoids architecture drift.

## Proof Or Next Owner

Recommended next owner is likely a ticket or spec update owned by
`harness-advisor`, `skill-maintenance`, or `goal-advisor`, with proof through a
small prototype: translate 1 skill, 1 ticket, 1 Goal Packet, and 1 invocation
envelope into the proposed canonical model and validate that round-tripping
preserves meaning.
