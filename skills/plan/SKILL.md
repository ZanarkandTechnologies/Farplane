---
name: plan
version: 0.1.0
description: Tier 2 generic planning interface. Use when a workflow needs to turn intent into executable shape, proof, and handoff rules without importing a domain-specific planning skill as the universal pattern.
tier: 2
source: local
allowed-tools: Read, Glob, Grep
---

# Plan

<!-- BEGIN CODEXTER_IMPORTANT_CHECKLIST -->
## Important Checklist

Source: `SKILL.md`

- [ ] State the intent, expected artifact, and domain pipeline.
- [ ] Use [reference-grounding](../reference-grounding/SKILL.md) when scope
  depends on local baseline, examples, official behavior, peer norms, or
  implementation patterns.
- [ ] If compact grounding is not enough, name the needed research method such
  as `research:gap` or `research:parity` for the caller before finalizing.
- [ ] Use [advise](../advise/SKILL.md) when there are real options to compare.
- [ ] Use [prototyping](../prototyping/SKILL.md) when scope risks premature
  scale, broad automation, large data, wide file edits, or overbuilt
  architecture.
- [ ] Choose one recommended path and accepted tradeoff.
- [ ] Write ordered executable steps, not only a strategy summary.
- [ ] Define proof before execution starts.
- [ ] Hand off to the domain execution skill with only the context it needs.
- [ ] Use [review](../review/SKILL.md) before claiming a material plan is ready.
<!-- END CODEXTER_IMPORTANT_CHECKLIST -->

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
4. Use a prototype gate when scale is the main risk.
5. Choose one recommended path and accepted tradeoff.
6. Convert intent into ordered executable steps.
7. Define proof before execution starts.
8. Hand off to the domain execution skill with only the context it needs.

## Tier Dependencies

- Use [reference-grounding](../reference-grounding/SKILL.md) for compact
  evidence checks.
- Use [research](../research/SKILL.md) when grounding needs a full brief.
- Use [advise](../advise/SKILL.md) for real option choice.
- Use [prototyping](../prototyping/SKILL.md) for `1 -> 10 -> 100` proof
  before scaling scope, automation, data, or architecture.
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
- `Prototype Note` when scale risk exists
- `Executable steps`
- `Proof`
- `Domain handoff`

## Guardrails

- Do not treat `impl-plan` as the generic Tier 2 planner. It is the coding
  implementation of this interface.
- Do not create a plan that leaves execution proof to be invented later.
- Do not invent a new domain pipeline when an existing domain skill owns it.
