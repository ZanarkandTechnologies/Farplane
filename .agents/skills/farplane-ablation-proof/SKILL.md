---
name: farplane-ablation-proof
description: "Turn a Farplane trust claim into an ablation proof report when proving whether a feature or workflow actually matters."
tier: 3
source: local
group: product
template_uses:
  skill-template: "0.3.2"
---

# Farplane Ablation Proof

## Context

Use this project-local skill when Farplane needs to prove or reject a trust
claim with a with/without comparison. Typical targets are a skill rule,
checklist, eval, validator, report phase, automation prompt, or UI proof
surface.

The output is a trust ablation report: what changes when the surface is present
versus absent, and whether the claim should remain part of the harness.

## Skill Signature

```text
farplane_ablation_proof(claim, surface, task_case, with_surface?, without_surface?, ticket?)
  -> ablation_report + trust_decision + follow_up
state: reads(farplane/harness.md, farplane/goals.md, target surface, task/eval evidence); writes(report or ticket artifact)
gates: claim_is_specific; comparison_is_fair; evidence_cites_both_conditions; no_proof_theater
routes: root skill `task-case-design` | root skill `eval` | root skill `agent-qa-test` | ../farplane-productization/SKILL.md
fails: uses only intuition; compares different tasks; keeps a surface because it sounds good
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the trust claim.
  - [ ] State the claim in falsifiable language.
  - [ ] Name the surface being tested and the user or agent behavior it should
    improve.
- [ ] 2. Choose the ablation case.
  - [ ] Prefer one realistic task case that can be run or reviewed in both
    conditions.
  - [ ] Use `task-case-design` when the case is not already clear.
- [ ] 3. Compare with and without the surface.
  - [ ] Keep task, inputs, and success criteria stable across both conditions.
  - [ ] Capture evidence for quality, failure mode, cost, and supervision need.
- [ ] 4. Write the proof report.
  - [ ] Include claim, method, both conditions, observed delta, decision, and
    residual risk.
- [ ] 5. Route the decision.
  - [ ] Keep and productize meaningful wins.
  - [ ] Remove, simplify, or ticket repair for weak or harmful surfaces.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

- Ablation report path or inline report.
- Trust decision: keep, change, remove, or retest.
- Follow-up ticket or productization handoff.
