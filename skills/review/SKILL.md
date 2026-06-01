---
name: review
description: Run an anchored 1-to-5 rubric review against the active ticket, scoring the right review families and using an anti-slop search playbook for code, UI, evidence, demos, and videos.
tier: 1
source: local
---

# Review

Use for skeptical, ticket-aware review before a plan, implementation, evidence
claim, or completion claim is treated as ready.

## Job

Read the active ticket and proof contract, choose the relevant rubric families,
inspect the changed surface plus nearby consistency risks, and return an
anchored verdict: `pass`, `revise`, or `block`.

<!-- BEGIN CODEXTER_IMPORTANT_CHECKLIST -->
## Important Checklist

Source: `SKILL.md`

- [ ] Read the active ticket and the linked proof before judging anything.
- [ ] Read the ticket `Proof Contract` and carry declared metrics, rubric gates, hard gates, and evidence obligations into the review.
- [ ] Read the [review rubric index](./references/review-rubric-index.md) and choose the families that actually fit this ticket.
- [ ] If code, cleanup, integration, or evidence trust is in scope, read the [desloppify guide](./references/desloppify.md) before scoring.
- [ ] Inspect the changed surface and the minimum neighboring code, docs, invariants, or interfaces needed to test consistency.
- [ ] If the work scaled a repetitive pattern across many files, records,
  skills, sources, users, or tickets, look for a representative
  `prototyping` note or sample proof before trusting the scale claim.
- [ ] If UI judgment is needed, require a visual QA artifact from the caller
  rather than faking visual review inside this primitive.
- [ ] If the ticket claims screenshots, traces, logs, or QA artifacts, qualify that evidence before passing review.
- [ ] If the ticket declares metrics, verify the metric result is traceable to a command, artifact, or autoresearch log before using it as evidence.
- [ ] Rank substantive findings by severity and confidence instead of returning generic questions.
- [ ] Write the review result with scores, verdict, hard-gate failures if any, and the concrete next action, then make sure the ticket links it from `Evidence`.
<!-- END CODEXTER_IMPORTANT_CHECKLIST -->
## Core Flow

1. Read the active ticket first.
2. Read its `Proof Contract`.
3. Select rubric families from ticket gates plus actual changed surface.
4. Open `references/review-rubric-index.md` only when family choice is not
   obvious from this file.
5. Open selected family references only when their detailed skeptic questions
   are needed for scoring.
6. Inspect changed files, evidence, and the smallest neighboring surfaces that
   could falsify the claim.
7. Score each family on the anchored `1.0`-to-`5.0` scale.
8. Return severity-ranked findings and a concrete next action.
9. Write or link the review artifact from the ticket `Evidence` section when
   the workflow requires durable proof.

## Rubric Routing

- Planning: `spec-contract` + `implementation-plan`
- Code/backend/api: `code-quality` + `integration-readiness` +
  `evidence-quality`
- UI or user-facing workflow: `user-intent-satisfaction` plus relevant
  quality/evidence families
- UI source review: add `ui-quality` + `frontend-guidelines`; require
  `web-design-guidelines` when source is available
- Cleanup/refactor/runtime/doc simplification: add `debloatability`
- Code, cleanup, integration, or evidence-heavy work: use
  `references/desloppify.md`

## Scoring

- `1.0`: failing, unsafe, contradictory, or largely absent
- `2.0`: partial work exists, but trust is low
- `3.0`: acceptable direction, but ordinary or incomplete
- `4.0`: strong, trustworthy, and defensible with minor caveats
- `5.0`: exemplary and hard to improve within scope

Overall `pass` requires all required rubric thresholds and hard gates to pass.
Weak `evidence-quality` or `integration-readiness` forces `revise` or `block`.

## Hard Gates

- Evidence is missing, stale, untraceable, or weaker than the claim: `revise` or
  `block`.
- Integration readiness is weak or neighboring contracts were not checked:
  `revise` or `block`.
- A declared metric is not tied to a command, artifact, or log: `revise` or
  `block`.
- A broad scale claim has no representative sample proof when one was needed:
  `revise` or `block`.
- UI judgment is requested without visual QA evidence: `revise` or `block`.
- The work contradicts the ticket, spec, memory, or user request: `block`.

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
- `overall_score`
- `overall_threshold`
- `verdict`
- `rerun_required`
- `hard_gate_failures`
- `finding_log`
- `rubric_sections`
- `blocking_findings`
- `next_action`

## Guardrails

- Do not review before reading the active ticket and proof contract.
- Do not emit a score without inspected evidence.
- Do not approve weak evidence or weak integration readiness.
- Do not stop at the changed file when neighboring contracts could invalidate
  the claim.
- Do not substitute review for QA or visual QA.
- Do not output only questions; return scores, findings, verdict, and next
  action.
