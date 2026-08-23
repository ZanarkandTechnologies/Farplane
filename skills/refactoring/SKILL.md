---
name: refactoring
version: 0.1.0
description: "Turn working code into simpler behavior-preserving structure with smell metrics, tests, and reviewable proof."
tier: 2
source: local
template_uses:
  skill-template: "0.3.2"
allowed-tools: Read, Glob, Grep, Bash
eval: evals/evals.json
---

# Refactoring Skill

## Context

Use this after or before feature work when the desired behavior is already
known and the code shape is slowing future changes. The skill owns
maintainability target selection, behavior-preserving transformation, smell
score reduction, and proof that public behavior stayed intact.

Route bug diagnosis to `runtime-debugging`, local diff findings to
`code-review`, and unresolved proof selection to `proof-advisor`. Run
already-selected deterministic proof commands in the native execution phase.

## Skill Signature

```text
refactoring(target, context?, ensemble?: auto | max) -> behavior_preserved + smell_delta + patch_plan? + proof + residual_risk?
state: reads(code, tests, git churn, lint/static-analysis output, project rules, docs); writes(refactor patch?, tests?, proof artifact?)
gates: behavior_locked; smallest_transformations; score_not_gamed; proof_after_change
routes: code-review | proof-advisor | review | runtime-debugging
fails: style-only churn; unproved behavior changes; metric gaming; broad cleanup unrelated to target
```

When `ensemble` is requested, load `ensemble.yaml`: `auto` selects its three
personas and `max` selects all. Collect independent assessments before
synthesis while preserving the behavior-proof and residual-risk contract.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the refactoring target.
  - [ ] Name the target files, behavior boundary, callers, public contracts,
    non-goals, and success criteria.
  - [ ] Stop if the request actually needs bug diagnosis, feature design, or
    product scope before refactoring.
- [ ] 2. Load the right references.
  - [ ] Read [workflow](references/workflow.md) for normal refactoring passes.
  - [ ] Read [metrics](references/metrics.md) before optimizing a smell score.
  - [ ] Read [tooling](references/tooling.md) when choosing stack-specific
    static-analysis or maintainability commands.
- [ ] 3. Resolve ensemble mode when requested.
  - [ ] Load `ensemble.yaml`; `auto` uses its three relevant personas and
    `max` uses all personas.
  - [ ] Keep testing, proof, review, and debugging child calls on their normal paths.
- [ ] 4. Lock behavior before changing structure.
  - [ ] Use existing tests, characterization tests, snapshots, fixtures, or
    manual proof to capture intended behavior.
  - [ ] If behavior cannot be locked, route to `proof-advisor`.
- [ ] 5. Score and prioritize the smallest honest target.
  - [ ] Prefer changed or high-churn code with high complexity, duplication,
    nesting, low coverage, or boundary violations.
  - [ ] Do not optimize whole-repo smell counts by default.
- [ ] 6. Apply behavior-preserving transformations in small steps.
  - [ ] Separate pure extraction, rename, move, dedupe, type tightening, and
    side-effect isolation from behavior changes.
  - [ ] Keep public APIs stable unless the target explicitly permits an API
    migration and proof covers callers.
- [ ] 7. Verify and review.
  - [ ] Re-run the behavior proof and relevant static-analysis checks.
  - [ ] Report smell delta, files changed, proof command/output, and residual
    risk.
  - [ ] Route material completion to `review` or the reviewer lane.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Do not count a lower smell score as success when readability, tests, or
  boundaries got worse.
- Do not split code only to satisfy line-count metrics; responsibility and
  behavior proof matter more than raw size.
- Do not mix a new feature with refactoring unless preparatory refactoring is
  explicitly scoped and behavior stays locked.

## Reference Map

- [workflow](references/workflow.md) - read for the ordered refactoring loop.
- [metrics](references/metrics.md) - read when scoring or prioritizing code
  smells.
- [tooling](references/tooling.md) - read when selecting stack-specific tools
  or commands.
- [ensemble.yaml](ensemble.yaml) - read for `ensemble: auto | max`.
- [code-review](../code-review/SKILL.md) - route local maintainability findings
  or final diff review.

## Output

Return or update an artifact with:

- refactoring target and behavior boundary
- selected personas and dissent when ensemble mode was used
- smell score inputs and prioritized target
- transformation plan or patch summary
- behavior-preservation proof
- smell delta and residual risk
- review or escalation note
