---
name: execute
version: 0.1.0
description: "Deprecated compatibility wrapper for native execution phase guidance when no domain execution skill owns the artifact."
tier: 2
source: local
allowed-tools: Read, Glob, Grep
---

# Execute

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] Treat this as a compatibility wrapper; prefer the native Tier 0 execution
  phase and domain-specific execution skills.
- [ ] Read the plan, scope, acceptance criteria, and proof contract.
- [ ] Confirm execution is ready; if scope or proof is still unclear, stop and
  return the gap to the caller, native planning phase, or domain planning skill.
- [ ] Use [reference-grounding](../reference-grounding/SKILL.md) when execution
  depends on official behavior, local invariants, or examples.
- [ ] Use [prototyping](../prototyping/SKILL.md) before broad batch edits,
  large data operations, many-file rewrites, or new automation when the pattern
  has not been proven on a representative slice.
- [ ] Do the scoped work using the owning domain skill or tool.
- [ ] Run the planned proof or update the durable artifact if the proof is
  wrong.
- [ ] Write results, blockers, evidence, and handoff state back to the durable
  artifact.
- [ ] Use the [review protocol](../review/SKILL.md) before material completion claims;
  delegate to the native `reviewer` lane with a reviewer handoff from the
  durable task pointer or proof contract when available.
- [ ] End with a clear next state: done, revise, blocked, or closeout.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Deprecated: use the Tier 0 execution phase from `templates/global/AGENTS.md` for
ordinary execution. Keep this skill only as a temporary compatibility wrapper
for older callers that explicitly invoke `$execute`.

This is not the Farplane coding executor. For code work,
`$impl` and `close-ticket` are Tier 3 coding-pipeline skills that implement
the concrete execution and closeout workflow.

## Job

1. Read the plan, scope, acceptance criteria, and proof contract.
2. Confirm the work is ready to execute rather than still needing planning.
3. Prototype first when execution would otherwise touch broad scale before the
   pattern is known.
4. Do the scoped work using the owning domain skill or tool.
5. Run the proof that was planned, or update the plan/ticket if proof is wrong.
6. Write results, blockers, evidence, and handoff state back to the durable
   artifact.
7. Run review before completion claims when the work is material, preferably by
   delegating to the native `reviewer` lane with the durable task pointer,
   changed files, evidence artifacts, review focus, caller-declared rubric
   families, required TAS gates, hard gates, and expected output path.
8. Stop, revise, or close based on proof and review.

## Phase Dependencies

- Use [reference-grounding](../reference-grounding/SKILL.md) when execution
  depends on official behavior, local invariants, or examples.
- Use [prototyping](../prototyping/SKILL.md) before scaling an unproven
  pattern across files, records, users, or automation.
- Use the [review protocol](../review/SKILL.md) before material completion claims; for
  material work, route review through the native `reviewer` lane when available
  instead of relying on coordinator self-review. The calling workflow owns the
  rubric routing and passes it through the reviewer handoff.
- Use the native planning phase or a domain planning skill when the work is not
  ready to execute.

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
- `Prototype Note` when broad execution was gated by a sample
- `Checks`
- `Review status`
- `Writeback`
- `Next state`

## Guardrails

- Do not execute vague intent. Route back to native planning or the domain
  planning skill when scope or proof is unclear.
- Do not claim completion without durable evidence.
- Do not treat `$impl` as the generic Tier 2 executor. It is the coding
  implementation of this interface.
