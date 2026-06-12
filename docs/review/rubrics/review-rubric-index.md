# Review Rubric Index

This is the primary rubric map for the Farplane review protocol. The `review`
skill is a thin callable wrapper over this docs-owned contract.

Use it to:

- read the ticket `Done / Proof` block for declared rubric gates and metric
  claims
- choose the right rubric families for the ticket
- load the anti-slop search playbook when the review needs repo-grounded skepticism
- locate the correct family reference files
- assign one TAS to each family from modular binary checks
- write one structured review result and link it from the ticket `Links`,
  `State`, or artifact references

## Shared TAS Contract

- `TAS-A`: pass. Required checks pass, blocker checks do not fail, and evidence
  supports the claim with only minor caveats.
- `TAS-B`: revise. Directionally correct, but one or more repairable required
  checks fail or evidence remains too thin for pass.
- `TAS-C`: block. A blocker check fails, wrong scope or unsafe behavior appears,
  contradictions are material, or core proof is missing.
- `TAS-D`: invalid review. The provided context or evidence is insufficient to
  judge honestly.

Calibration rules:

- `TAS-A` requires the reviewer to be able to defend pass to a skeptical human
  without major caveats.
- `TAS-B` is a near miss, not a pass.
- `TAS-C` is for material trust failures, wrong-scope work, unsafe work, or
  missing core proof.
- `TAS-D` is for invalid review state, not low-quality work.

Each family has its own reference file. Read the selected family files before
assigning TAS.

Also load `desloppify.md` whenever code, cleanup, integration, or evidence
trust is in scope. It is a cross-cutting search playbook, not a TAS family.

## Calibration Examples

Use examples like these to separate TAS outcomes:

- `TAS-B`:
  the work has substance, but a required check fails in a repairable way or a
  skeptical reviewer still cannot trust the evidence without a focused repair
  pass.
  Example: the main feature works in one happy-path screenshot, but the required
  edge-state evidence check fails and the write-up overstates confidence.
- `TAS-A`:
  required checks pass, every important claim maps to an artifact, the touched
  surfaces are coherent, and remaining issues are polish-level rather than
  trust-level.
  Example: the main path is covered and the delta is coherent, but evidence for
  failure states or neighboring integrations is complete enough for the claim.
- `TAS-C`:
  the work is materially off-scope, unsafe, contradictory, or missing core
  proof.
- `TAS-D`:
  the review cannot be run because the task context, changed artifacts, or
  evidence were not supplied.

## Family Template

Every family reference should provide:

- what the family is judging
- a family-level TAS guide
- modular checklist groups
- evidence cues
- finding cues

Checklist groups should use stable IDs and binary questions. Group related
checks under small modules such as `required_checks`, `blocker_checks`,
`evidence_checks`, and optional family-specific modules. Do not assign TAS per
dimension or average checklist results. Checklist groups guide inspection; the
family returns exactly one TAS.

For each rubric family, return:

- `tas`
- `pass`
- `checks`
- `failed_checks`
- `findings`
- `next_action`

Default required family verdicts:

- `spec-contract`: `TAS-A`
- `implementation-plan`: `TAS-A`
- `code-quality`: `TAS-A`
- `frontend-code-maintainability`: `TAS-A` when selected
- `debloatability`: `TAS-A`, or `TAS-B` when cleanup is advisory and no hard
  gate depends on it
- `ui-quality`: `TAS-A`
- `frontend-guidelines`: `TAS-A`
- `user-intent-satisfaction`: `TAS-A`
- `evidence-quality`: `TAS-A`
- `demo-quality`: `TAS-A` when demo is required, otherwise diagnostic
- `video-quality`: `TAS-A` when video proof is required, otherwise diagnostic
- `integration-readiness`: `TAS-A`
- `skill-contract`: `TAS-A` when skill files or skill-system behavior changed
- `prompt-quality`: `TAS-A` when subagent, delegated CLI, eval, structured
  output, or AI-app prompts changed
- `eval-quality`: `TAS-A` when eval tasks, judges, fixtures, or runners changed

Hard gates:

- `evidence-quality` below `TAS-A` cannot pass overall review
- `integration-readiness` below `TAS-A` cannot pass overall review
- `ui-quality` cannot pass if required functionality checks fail

## Rubric Selection

Choose rubric families from the ticket context:

- ticket `Done / Proof`:
  - start with declared rubric families, TAS gates, and hard gates
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
  - `frontend-guidelines` via `web-design-guidelines` when source files are available
  - `frontend-code-maintainability` when UI source files are long, stateful,
    reused, provider-like, component-heavy, or likely to keep growing
  - `vercel-react-best-practices` as a supporting skill when React/Next.js
    performance, waterfalls, bundle size, data fetching, rerenders, or
    rendering behavior are in scope
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
- skill or skill-system review:
  - `skill-contract`
  - `integration-readiness`
  - `evidence-quality`
- prompt review:
  - `prompt-quality`
  - `evidence-quality`
  - `integration-readiness`
- eval review:
  - `eval-quality`
  - `evidence-quality`
  - `integration-readiness`

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

### 4b. Frontend Guidelines Metric
- File: `frontend-guidelines.md`
- Focus:
  - source-fresh Web Interface Guidelines audit
  - accessibility, focus, forms, navigation, animation, content handling, and web-interface fundamentals
  - comparable metric for aligning agent reviews with an external checklist

### 4c. Frontend Code Maintainability
- File: `frontend-code-maintainability.md`
- Focus:
  - React/component modularity, file length, hooks, state ownership, DRY, comments, and testable helper seams
  - agent/human readability for frontend code that will grow by breadth
  - long-file thresholds and extraction cues for dialogs, providers, pages, canvas scenes, and feature modules
  - routing React/Next.js performance-specific review to `vercel-react-best-practices` instead of duplicating that rulebook

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

### 11. Skill Contract
- File: `skill-contract.md`
- Focus:
  - trigger accuracy
  - first-load todo list quality
  - repeatability from files alone
  - actor-prompt versus skill-contract boundaries
  - duplication control
  - proof and registry readiness

### 12. Prompt Quality
- File: `prompt-quality.md`
- Focus:
  - task clarity
  - durable context and pointer handling
  - role and boundary fit
  - output contract
  - hallucination and overreach control
  - evidence and tool-use expectations

### 13. Eval Quality
- File: `eval-quality.md`
- Focus:
  - task/reference-point clarity
  - judge rubric fit
  - fixture realism
  - harness-native execution
  - artifact traceability
  - failure usefulness

## Review Result

Write the final review as a linked artifact and surface it from ticket `Links`
or `State`.

Required fields:

- `work_type`
- `search_scope`
- `reviewed_at`
- `rubrics_used`
- `overall_tas`
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

- `tas`
- `pass`
- `checks`
- `failed_checks`
- `findings`
- `next_action`

## Reviewer Heuristics

Always ask:

- What would make a skeptical human reviewer reject this?
- What claim is not actually proven?
- Which failed check is keeping this out of `TAS-A`?
- What specific weakness makes this `TAS-B` instead of `TAS-A`, or `TAS-C`
  instead of `TAS-B`?
- What hard gate is failing?
- What is the weakest family and why?
- What concrete next pass would move the result to `TAS-A`?
- Which neighboring surface did I check to rule out or confirm drift?
- Is this finding severe enough and proven enough to deserve a blocking slot?
