---
name: plan
version: 0.1.0
description: Tier 2 generic planning interface. Use when a workflow needs to turn intent into executable shape, proof, and handoff rules without importing a domain-specific planning skill as the universal pattern.
tier: 2
source: local
allowed-tools: Read, Glob, Grep
---

# Plan

Use this as the Tier 2 planning interface. It defines the common shape every
application pipeline can bind to: coding, frontend, presentations, documents,
video, image, data, or future domains.

This is an interface skill, not the Codexter coding planner. For code work,
`spec-to-ticket` and `impl-plan` are Tier 3 coding-pipeline skills that
implement this interface.

## Job

1. Clarify the intent and expected artifact.
2. Ground expectations before scoping when the target depends on examples,
   official behavior, peer norms, or local baseline.
3. Compare real options when the path is materially ambiguous.
4. Choose one recommended path and accepted tradeoff.
5. Convert intent into ordered executable steps.
6. Define proof before execution starts.
7. Hand off to the domain execution skill with only the context it needs.

## Tier Dependencies

- Use [reference-grounding](../reference-grounding/SKILL.md) for compact
  evidence checks.
- Use [research](../research/SKILL.md) when grounding needs a full brief.
- Use [advise](../advise/SKILL.md) for real option choice.
- Use [review](../review/SKILL.md) before claiming a material plan is ready.

## Domain Bindings

- Coding: `spec-to-ticket`, `impl-plan`
- Frontend: UX spec, visual spec, implementation plan, visual QA plan
- Presentations: brief/spec, slide plan, build plan, render/review plan
- Documents: outline/spec, draft plan, revision plan, render/review plan
- Video/image/data: asset/spec plan, build plan, proof plan

## Output

Produce a compact plan interface note with:

- `Intent`
- `Grounding`
- `Options / recommendation`
- `Executable steps`
- `Proof`
- `Domain handoff`

## Guardrails

- Do not treat `impl-plan` as the generic Tier 2 planner. It is the coding
  implementation of this interface.
- Do not create a plan that leaves execution proof to be invented later.
- Do not invent a new domain pipeline when an existing domain skill owns it.
