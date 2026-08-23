---
template_id: skill-qa-checklist
template_version: "0.1.2"
feature_refs:
  - FEAT-0057
  - FEAT-0062
consumer_scope: skill
applies_to:
  - skills/*/qa_checklist.md
---

# Skill QA Checklist

Do not create this file by default. Keep it only when a skill has repeated
skill-specific runtime, safety, or preflight guards that cannot be expressed
more clearly as Golden Workflow Node assertions, golden examples, evals,
validators, or review rubrics.

Generic authoring and structure checks belong to the shared skill-contract
rubric, not a copied skill-local checklist.

For skills enrolled in `skill-surface-budget`, keep this checklist to the top 5
runtime guardrails. Use `consolidate(..., structure = skill)` through
`skill-maintenance.refine_skill` before adding item 6.

## Checklist

- [ ] Preflight context is sufficient for the current request.
- [ ] Required references, scripts, evals, or templates were loaded only when
  the active branch needed them.
- [ ] The output satisfies the skill's stated contract.
- [ ] Proof, blocker, or skipped-proof evidence is recorded before completion.
