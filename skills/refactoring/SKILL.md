---
name: refactoring
version: 0.1.0
description: "Turn working code into simpler behavior-preserving structure with smell metrics, tests, and reviewable proof."
tier: 2
source: local
template_uses:
  skill-template: "0.3.2"
allowed-tools: Read, Glob, Grep, Bash
eval: eval_task.json
---

# Refactoring Skill

## Context

Use this after or before feature work when the desired behavior is already
known and the code shape is slowing future changes. The skill owns
maintainability target selection, behavior-preserving transformation, smell
score reduction, and proof that public behavior stayed intact.

Route bug diagnosis to `runtime-debugging`, local diff findings to
`code-review`, broad proof selection to `proof-advisor`, test execution choices
to `testing`, and budget resolution to `budget-advisor`.

## Skill Signature

```text
refactoring(target, context?, budget?) -> behavior_preserved + smell_delta + patch_plan? + proof + residual_risk?
state: reads(code, tests, git churn, lint/static-analysis output, project rules, docs); writes(refactor patch?, tests?, proof artifact?)
gates: behavior_locked; smallest_transformations; score_not_gamed; proof_after_change
routes: budget-advisor | code-review | testing | proof-advisor | review | runtime-debugging
fails: style-only churn; unproved behavior changes; metric gaming; broad cleanup unrelated to target
```

Use `budget-advisor` when `budget` is present:

```text
RefactoringBudget = {
  budget_mode?: "none" | "light" | "normal" | "deep" | "max",
  available_time?: string,
  review_depth?: 0 | 1 | 2,
  ensemble?: {
    count: number,
    perspective_mode?: "same" | "different",
    personas?: RefactoringPersona[],
    aggregation?: "synthesize" | "score_then_synthesize" | "hierarchical_synthesis"
  },
  coverage?: "smoke" | "focused" | "broad",
  evidence_depth?: "light" | "strong",
  max_budget_depth?: 0 | 1
}
```

Default `max_budget_depth` to `0` for subskill calls and `1` only for the
top-level refactoring invocation. Budgeted lanes must preserve the output
contract: behavior proof, smell delta, patch plan or patch, and residual risk.

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
- [ ] 3. Resolve budget when present.
  - [ ] Call `budget-advisor` with this contract and `RefactoringBudget`.
  - [ ] For different-perspective ensembles, use persona prompts from
    [budget-personas](references/budget-personas.md) unless the caller supplied
    complete personas.
  - [ ] Cap recursive budget expansion at the resolved `max_budget_depth`.
- [ ] 4. Lock behavior before changing structure.
  - [ ] Use existing tests, characterization tests, snapshots, fixtures, or
    manual proof to capture intended behavior.
  - [ ] If behavior cannot be locked, route to `testing` or `proof-advisor`.
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

## Templates

```text
RefactoringPersona = {
  name: string,
  prompt: string,
  focus: string[],
  avoid?: string[],
  output_shape?: string
}
```

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
- [budget-personas](references/budget-personas.md) - read for high-budget
  different-perspective ensembles.
- [budget-advisor](../budget-advisor/SKILL.md) - read when `budget` is present.
- [code-review](../code-review/SKILL.md) - route local maintainability findings
  or final diff review.
- [testing](../testing/SKILL.md) - route proof command selection.

## Output

Return or update an artifact with:

- refactoring target and behavior boundary
- budget program summary when budget was used
- smell score inputs and prioritized target
- transformation plan or patch summary
- behavior-preservation proof
- smell delta and residual risk
- review or escalation note
