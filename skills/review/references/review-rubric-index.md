# Review Rubric Index

This is the primary rubric map for the `review` skill.

Use it to:

- choose the right rubric families for the ticket
- ask the right questions for each family
- score each family consistently
- write one `Review Packet` back into the ticket

## Scoring Model

Score each dimension from `1` to `5`.

- `1` = fail
- `2` = weak
- `3` = acceptable
- `4` = strong
- `5` = excellent

For each rubric family, return:

- `score`
- `threshold`
- `pass`
- `top_questions`
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

- weak `evidence-quality` cannot pass overall review
- weak `integration-readiness` cannot pass overall review
- `ui-quality` cannot pass if functionality is failing

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

Dimensions:
- story coherence
- slice sizing
- parallelization fit
- acceptance testability
- scope clarity

Questions:
- Does the user story make sense as one coherent unit of work?
- Is the ticket sized correctly for one execution slice?
- Does the proposed parallelization make sense, or is it fake concurrency?
- Are success conditions testable?
- Are dependencies and non-goals explicit enough to prevent drift?

### 2. Implementation Plan

Dimensions:
- human readability
- bloat resistance
- modularity
- proof clarity
- execution order
- risk clarity

Questions:
- Can a human read the plan quickly and know what will happen?
- Is the plan bloated with unnecessary abstraction or ceremony?
- Is modularity preserved?
- Does the plan explain how success will be proved?
- Is the execution order sensible?
- Are the main risks and weak assumptions explicit?

### 3. Code Quality

Dimensions:
- modularity and reuse
- bloat resistance
- readability
- boundary clarity
- error handling
- maintainability

Questions:
- Is the code modular and reusable where it should be?
- Did the implementation remove dead code and unnecessary legacy?
- Is the code readable and easy to reason about?
- Are boundaries and responsibilities clear?
- Is error handling sufficient?
- Is this easy for the next engineer to modify safely?

### 4. UI Quality

Dimensions:
- originality
- design quality
- craft
- functionality
- fidelity to intent

Questions:
- Does the UI feel deliberate rather than template-like?
- Are there original decisions instead of default component-library patterns?
- Is the visual craft solid: hierarchy, spacing, typography, color, contrast?
- Can users understand and use it without guessing?
- Does it match the intended product feel and the best examples in its category?

### 5. Debloatability

Dimensions:
- dead-surface removal
- compatibility cleanup
- duplication reduction
- clarity improvement
- deletion safety

Questions:
- What can be deleted now without losing real capability?
- What compatibility layer is still hanging around without earning its keep?
- What is duplicated across docs, skills, helpers, or schemas?
- What part of the system became clearer after the cleanup?
- Was the deletion/simplification safe and well-bounded?

### 6. Evidence Quality

Dimensions:
- sufficiency
- reproducibility
- traceability
- consistency
- inspectability

Questions:
- Do the artifacts actually prove the claims?
- Are there enough screenshots, logs, commands, and verification results?
- Can a human reproduce or inspect the proof quickly?
- Is each acceptance criterion traceable to evidence?
- Are any claims contradicted by the recorded artifacts?

### 7. Demo Quality

Dimensions:
- fidelity
- realism
- workflow coverage
- trustworthiness
- communication clarity

Questions:
- Does the demo honestly represent the product?
- Is it realistic rather than staged or fake-feeling?
- Does it cover the important workflow?
- Would a skeptical reviewer trust what they are seeing?
- Does it communicate the product clearly?

### 8. Video Quality

Dimensions:
- legibility
- coverage
- pacing
- faithfulness
- verification value

Questions:
- Is the video easy to read and follow?
- Does it show the key interactions and states?
- Is the pacing reasonable?
- Is it faithful to the actual product state?
- Does it help verification rather than just marketing?

### 9. Integration Readiness

Dimensions:
- integration safety
- contract correctness
- dependency readiness
- coupling risk
- merge readiness

Questions:
- Does this integrate cleanly with the rest of the system?
- Are interfaces and contracts preserved?
- Are dependencies resolved and ready?
- Is there hidden coupling or regression risk?
- Is this actually safe to advance or merge?

## Review Packet

Write the final review back into the ticket under `Review Packet`.

Required fields:

- `reviewed_at`
- `rubrics_used`
- `overall_score`
- `overall_verdict`
- `rerun_required`
- `blocking_findings`
- `next_action`

Then include one block per rubric family used:

- `score`
- `threshold`
- `pass`
- `top_questions`
- `findings`
- `next_action`

## Reviewer Heuristics

Always ask:

- What would make a skeptical human reviewer reject this?
- What part is bloated?
- What can be deleted safely right now?
- What part is least legible to the next engineer?
- What claim is not actually proven?
- What feels generic or template-like?
- What dependency or integration risk is hidden?
- Does the ticket contract still match what was actually built?
