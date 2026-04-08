# Review Rubric Index

This is the primary rubric map for the `review` skill.

Use it to:

- choose the right rubric families for the ticket
- locate the correct family reference files
- score each family consistently
- write one `Review Packet` back into the ticket

## Scoring Model

Score each family and dimension from `1.0` to `5.0`.

- `1`: failing, unsafe, contradictory, or largely absent
- `3`: acceptable and directionally correct, but still ordinary or caveated
- `5`: exemplary, persuasive, and hard to improve materially within scope

Interpolate `2` and `4` between the written anchors.

Each family has its own reference file. Read the selected family files before scoring.

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
  - `code-quality`
  - `evidence-quality`
  - `demo-quality` when a demo is present
  - `video-quality` when a video is present
- final completion review:
  - `integration-readiness`
  - `evidence-quality`
  - optional `demo-quality`
  - optional `video-quality`

When unsure, prefer adding `evidence-quality` and `integration-readiness`.

## Rubric Families

### 1. Spec Contract
- File: `spec-contract.md`
- Focus:
  - does the user story make sense
  - does the proposed parallelization make sense
  - is the slice sized correctly
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

## Review Packet

Write the final review back into the ticket under `Review Packet`.

Required fields:

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
- What hard gate is failing?
- What is the lowest-scoring family and why?
- What concrete next pass would raise the score above threshold?
