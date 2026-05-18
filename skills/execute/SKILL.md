---
name: execute
version: 0.1.0
description: Tier 2 generic execution interface. Use when a workflow needs the common do-the-work, prove-it, write-back, and review loop without treating one application pipeline as universal.
tier: 2
allowed-tools: Read, Glob, Grep
---

# Execute

Use this as the Tier 2 execution interface. It defines the common build/prove
shape every application pipeline can bind to.

This is an interface skill, not the Codexter coding executor. For code work,
`$impl` and `close-ticket` are Tier 3 coding-pipeline skills that implement
this interface.

## Job

1. Read the plan, scope, acceptance criteria, and proof contract.
2. Confirm the work is ready to execute rather than still needing planning.
3. Do the scoped work using the owning domain skill or tool.
4. Run the proof that was planned, or update the plan/ticket if proof is wrong.
5. Write results, blockers, evidence, and handoff state back to the durable
   artifact.
6. Run review before completion claims when the work is material.
7. Stop, revise, or close based on proof and review.

## Tier Dependencies

- Use [reference-grounding](../reference-grounding/SKILL.md) when execution
  depends on official behavior, local invariants, or examples.
- Use [review](../review/SKILL.md) before material completion claims.
- Use [plan](../plan/SKILL.md) when the work is not ready to execute.

## Domain Bindings

- Coding: `$impl`, `close-ticket`
- Frontend: implementation plus visual QA
- Presentations: build deck, render, review
- Documents: draft, revise, render, review
- Video/image/data: produce asset/output, inspect, verify

## Output

Produce an execution result with:

- `Scope executed`
- `Evidence`
- `Checks`
- `Review status`
- `Writeback`
- `Next state`

## Guardrails

- Do not execute vague intent. Route back to `plan` or the domain planning
  skill when scope or proof is unclear.
- Do not claim completion without durable evidence.
- Do not treat `$impl` as the generic Tier 2 executor. It is the coding
  implementation of this interface.
