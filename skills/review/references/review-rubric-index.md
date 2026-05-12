# Review Rubric Index

This is the primary rubric map for the `review` skill.

Use it to:

- read the ticket `Proof Contract` for declared rubric gates and metric claims
- choose the right rubric families for the ticket
- load the anti-slop search playbook when the review needs repo-grounded skepticism
- locate the correct family reference files
- score each family consistently
- write one structured review result and link it from the ticket `Evidence` section

## Shared Score Contract

Score each family and dimension from `1.0` to `5.0`.

- `1.0`: failing, unsafe, contradictory, or largely absent
- `2.0`: partially relevant, but still weak enough that key claims depend on
  reviewer inference, thin proof, or unresolved defects
- `3.0`: acceptable and directionally correct, but ordinary, caveated, or still
  missing some confidence-building detail
- `4.0`: strong, trustworthy, and pass-worthy with only minor caveats
- `5.0`: exemplary, persuasive, and hard to improve materially within scope

Calibration rules:

- start at `3.0` only if the work is genuinely workable and directionally right
- move down to `2.0` when the work has some substance but the reviewer still
  would not trust it without a focused follow-up pass
- move up to `4.0` only when the reviewer would defend a pass to a skeptical
  human without needing major caveats
- reserve `5.0` for clearly above-bar work with visible positive evidence, not
  merely absence of defects

Each family has its own reference file. Read the selected family files before scoring.

Also load `desloppify.md` whenever code, cleanup, integration, or evidence
trust is in scope. It is a cross-cutting search playbook, not a scored family.

## Calibration Examples

Use examples like these to separate adjacent bands:

- `2.0` vs `3.0`:
  `2.0` = the work has substance, but a skeptical reviewer still cannot trust
  it without a focused repair pass.
  Example: the main feature works in one happy-path screenshot, but edge-state
  claims remain unproven and the write-up overstates confidence.
  `3.0` = the work is believable and directionally correct, but still thin or
  ordinary enough that another pass is warranted.
  Example: the main path is covered and the delta is coherent, but evidence for
  failure states or neighboring integrations remains incomplete.
- `3.0` vs `4.0`:
  `3.0` = the reviewer still needs to attach visible caveats to justify trust.
  `4.0` = the reviewer would defend a pass to a skeptical human with only minor
  caveats.
  Example: every important claim maps to an artifact, the touched surfaces are
  coherent, and the remaining issues are polish-level rather than trust-level.
- `4.0` vs `5.0`:
  `4.0` = strong and ready.
  `5.0` = unusually strong, with visible positive evidence that the work is not
  just acceptable but difficult to improve materially within scope.
  Example: the implementation or evidence packet not only satisfies the ticket,
  but also improves surrounding clarity, removes dead weight, or makes skeptical
  review unusually easy.

## Family Template

Every family reference should provide:

- what the family is judging
- a family-level `1/2/3/4/5` score guide
- dimensions
- skeptic questions for each dimension
- evidence cues
- finding cues

For each rubric family, return:

- `score`
- `threshold`
- `pass`
- `dimension_scores`
- `findings`
- `next_action`

Default thresholds:

- `spec-contract`: `4.0`
- `implementation-plan`: `4.0`
- `code-quality`: `4.0`
- `debloatability`: `4.0`
- `ui-quality`: `4.0`
- `user-intent-satisfaction`: `4.0`
- `evidence-quality`: `4.0`
- `demo-quality`: `3.5`
- `video-quality`: `3.5`
- `integration-readiness`: `4.0`

Hard gates:

- `evidence-quality` below threshold cannot pass overall review
- `integration-readiness` below threshold cannot pass overall review
- `ui-quality` cannot pass if `functionality` is failing

## Rubric Selection

Choose rubric families from the ticket context:

- ticket `Proof Contract`:
  - start with declared rubric families, thresholds, and hard gates
  - add any missing families required by the actual changed surface
  - check declared metrics separately as traceability/evidence, not as a
    replacement for rubric judgment

- planning / contract review:
  - `spec-contract`
  - `implementation-plan`
- backend / api / internal code:
  - `code-quality`
  - `integration-readiness`
  - `evidence-quality`
- cleanup / runtime / docs / simplification work:
  - `debloatability`
  - `integration-readiness`
  - `evidence-quality` when claims depend on proof
- UI work:
  - `ui-quality`
  - `user-intent-satisfaction` when the ticket clearly expresses the user-facing ask or success feel
  - `code-quality`
  - `evidence-quality`
  - `demo-quality` when a demo is present
  - `video-quality` when a video is present
- final completion review:
  - `user-intent-satisfaction` when the ticket is user-facing
  - `integration-readiness`
  - `evidence-quality`
  - optional `demo-quality`
  - optional `video-quality`

If the reviewer wants to make stronger "worth it", willingness-to-pay, or competitive-market claims, the ticket/spec must already carry explicit user, alternative, and price-point evidence. Otherwise keep the judgment at the `user-intent-satisfaction` level and call the stronger market question underspecified.

When unsure, prefer adding `evidence-quality` and `integration-readiness`.

## Cross-Cutting Search Playbook

- File: `desloppify.md`
- Use when:
  - code or docs may have neighboring-surface drift
  - integration or invariant risk could hide outside the changed file
  - AI-generated or rapid patches need an anti-slop consistency sweep
  - evidence claims sound stronger than the attached proof
- Focus:
  - changed-file plus neighboring-surface search discipline
  - severity/confidence-ranked findings
  - invariant, naming, contract, and evidence drift

## Rubric Families

### 1. Spec Contract
- File: `spec-contract.md`
- Focus:
  - does the user story make sense
  - does the proposed parallelization make sense
  - does the selected ticket stay whole unless a real boundary exists
  - are success conditions testable
  - are boundaries explicit enough to prevent drift

### 2. Implementation Plan
- File: `implementation-plan.md`
- Focus:
  - readability for a human reviewer
  - bloatability
  - modularity
  - proof clarity
  - execution order
  - risk clarity
  - decision tone

### 3. Code Quality
- File: `code-quality.md`
- Focus:
  - modularity / reusability
  - bloatability and legacy cleanup
  - readability
  - boundaries
  - error handling
  - maintainability
- Extra lenses:
  - API
  - backend
  - types

### 4. UI Quality
- File: `ui-quality.md`
- Focus:
  - originality against strong existing examples
  - design quality
  - craft
  - functionality against strong examples
  - fidelity to intent

### 5. Debloatability
- File: `debloatability.md`
- Focus:
  - what dead surface was removed
  - what legacy/compatibility baggage was cleaned up
  - what duplication was reduced
  - whether clarity improved
  - whether deletion was safe

### 6. Evidence Quality
- File: `evidence-quality.md`
- Focus:
  - sufficiency
  - reproducibility
  - traceability
  - consistency
  - inspectability

### 7. Demo Quality
- File: `demo-quality.md`
- Focus:
  - fidelity
  - realism
  - workflow coverage
  - trustworthiness
  - communication clarity

### 8. Video Quality
- File: `video-quality.md`
- Focus:
  - legibility
  - coverage
  - pacing
  - faithfulness
  - verification value

### 9. Integration Readiness
- File: `integration-readiness.md`
- Focus:
  - integration safety
  - contract correctness
  - dependency readiness
  - coupling risk
  - merge readiness

### 10. User Intent Satisfaction
- File: `user-intent-satisfaction.md`
- Focus:
  - fidelity to the saved user ask
  - completeness of the promised outcome
  - leverage or worth-it feel for the intended user
  - whether the result would actually satisfy or impress the user
  - evidence confidence for any stronger value claims

## Review Result

Write the final review as a linked artifact and surface it from the ticket `Evidence` section.

Required fields:

- `work_type`
- `search_scope`
- `reviewed_at`
- `rubrics_used`
- `overall_score`
- `overall_threshold`
- `overall_verdict`
- `rerun_required`
- `evidence_quality`
- `integration_readiness`
- `traceability`
- `freshness`
- `hard_gate_failures`
- `finding_log`
- `blocking_findings`
- `next_action`

Then include one block per rubric family used:

- `score`
- `threshold`
- `pass`
- `dimension_scores`
- `findings`
- `next_action`

## Reviewer Heuristics

Always ask:

- What would make a skeptical human reviewer reject this?
- What claim is not actually proven?
- Which dimension is keeping this score out of the next higher band?
- What specific weakness makes this a `2` instead of a `3`, or a `4` instead of a `5`?
- What hard gate is failing?
- What is the lowest-scoring family and why?
- What concrete next pass would raise the score above threshold?
- Which neighboring surface did I check to rule out or confirm drift?
- Is this finding severe enough and proven enough to deserve a blocking slot?
