---
name: review
description: Reusable TAS review rubric contract for judging whether provided task context, artifacts, and evidence are pass-ready, need revision, blocked, or invalid to review.
tier: 1
source: local
---

# Review

Use as the canonical review rubric contract before a plan, implementation,
evidence bundle, skill, prompt, eval, doc, or completion claim is treated as
ready.

This skill is not an actor prompt. It does not decide whether to spawn a
reviewer, how to route subagents, or how to write back to a ticket. The caller
or reviewer actor supplies the task context and owns artifact writeback.

## Contract

Apply the selected review families to provided task context, changed artifacts,
and evidence. Return a TAS verdict with findings, hard-gate failures, and one
concrete next action.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Important Checklist

- [ ] Confirm the task context, changed artifacts, and evidence being reviewed
  are available.
- [ ] Start from caller-declared rubric families and TAS gates; add only an
  obvious missing hard-gate family with explanation.
- [ ] Inspect the artifact and the minimum neighboring context needed to judge
  consistency, proof strength, and integration risk.
- [ ] Apply TAS verdicts and hard gates; do not use numeric scores.
- [ ] Return findings, blocking issues, and one concrete next action.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->
## Core Flow

1. Confirm supplied task context and evidence are sufficient to review.
2. Start from caller-declared rubric families and TAS gates. If none are
   declared, return `TAS-D` for material review and ask the caller for a review
   handoff.
3. Validate the declared families against the actual changed surface and add an
   obvious missing hard-gate family only when needed.
4. Open `references/review-rubric-index.md` only when family choice is not
   obvious from the handoff and this file.
5. Open selected family references only when their detailed skeptic questions
   are needed for a TAS decision.
6. Inspect changed files, evidence, and the smallest neighboring surfaces that
   could falsify the claim.
7. Assign TAS per selected family and overall.
8. Return severity-ranked findings and one concrete next action.

## Rubric Family Catalog

The calling skill, workflow, or ticket `Proof Contract` owns rubric routing.
This review contract owns the available families, TAS meanings, and hard gates.
Use `references/reviewer-handoff.md` when creating a durable reviewer handoff.

Common families:

- `spec-contract`
- `implementation-plan`
- `code-quality`
- `ui-quality`
- `frontend-guidelines`
- `user-intent-satisfaction`
- `debloatability`
- `evidence-quality`
- `demo-quality`
- `video-quality`
- `integration-readiness`
- `skill-contract`
- `prompt-quality`
- `eval-quality`

Reviewer sanity check:

- Start with the caller-declared families and `required_tas` gates.
- Add a missing family only when the changed surface makes the omission
  obvious, such as `evidence-quality` for proof claims or
  `integration-readiness` for cross-surface changes.
- Report any added family in `rubrics_used` and explain why.
- Do not silently replace the caller's routing with a generic default.
- For code, cleanup, integration, or evidence-heavy work, use
  `references/desloppify.md` as the cross-cutting search playbook.

## TAS Verdicts

- `TAS-A`: pass. Requirements and required evidence are satisfied with only
  minor or no caveats.
- `TAS-B`: revise. Directionally correct, but one or more meaningful issues,
  missing evidence points, or caveats remain before pass.
- `TAS-C`: block. Wrong scope, unsafe, contradictory, materially unreliable, or
  missing core proof.
- `TAS-D`: invalid review. The provided context or evidence is insufficient to
  judge honestly.

Overall `pass` requires `TAS-A` on required hard-gate families. `TAS-B` is a
near miss, not a pass. `TAS-D` means review cannot proceed without more context.

## Hard Gates

- Evidence is missing, stale, untraceable, or weaker than the claim: `TAS-B` or
  `TAS-C`.
- Integration readiness is weak or neighboring contracts were not checked:
  `TAS-B` or `TAS-C`.
- A declared metric is not tied to a command, artifact, or log: `TAS-B` or
  `TAS-C`.
- A broad scale claim has no representative sample proof when one was needed:
  `TAS-B` or `TAS-C`.
- UI judgment is requested without visual QA evidence: `TAS-B` or `TAS-C`.
- The work contradicts the task, spec, memory, or user request: `TAS-C`.
- The review lacks enough task context or evidence to judge: `TAS-D`.

## Completion Receipt

When the Stop hook requests visible completion review with a nonce, write a
ticket-scoped completion receipt under
`tickets/TASK-XXXX/artifacts/review/<timestamp>-completion-receipt.json`, link
it from ticket `Evidence`, and tell the calling lane to echo the same nonce as:

```text
COMPLETION_PASSWORD: <nonce>
```

## Output

Return or write:

- `work_type`
- `search_scope`
- `rubrics_used`
- `overall_tas`
- `verdict`: `pass`, `revise`, `block`, or `invalid`
- `rerun_required`
- `hard_gate_failures`
- `finding_log`
- `rubric_sections`
- `blocking_findings`
- `next_action`

## Guardrails

- Do not apply TAS before inspecting the supplied task context and evidence.
- Do not emit numeric scores.
- Do not approve weak evidence or weak integration readiness.
- Do not stop at the changed file when neighboring contracts could invalidate
  the claim.
- Do not substitute review for QA or visual QA.
- Do not output only questions; return TAS, findings, verdict, and next action.
