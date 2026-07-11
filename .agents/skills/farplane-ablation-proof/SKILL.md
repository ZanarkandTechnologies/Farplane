---
name: farplane-ablation-proof
description: "Turn a Farplane trust claim into an ablation proof report when proving whether a feature or workflow actually matters."
tier: 3
source: local
group: capability
template_uses:
  skill-template: "0.3.2"
---

# Farplane Ablation Proof

## Context

Use this project-local capability when Farplane needs to prove or reject a
trust claim with a with/without comparison. Typical targets are a skill rule,
checklist, eval, validator, report phase, automation prompt, or UI proof
surface.

The output is a trust ablation report: what changes when the surface is present
versus absent, and whether the claim should remain part of the harness.

## Skill Signature

```text
farplane_ablation_proof(claim, surface, task_case, with_surface?, without_surface?, ticket?)
  -> ablation_report + trust_decision + follow_up
state: reads(farplane/harness.yaml, farplane/metrics.yaml, target surface, task/eval evidence); writes(ticket artifact)
gates: claim_is_specific; comparison_is_fair; evidence_cites_both_conditions; no_proof_theater
routes: root skill `prototyping` | root skill `eval` | root skill `agent-qa-test` | ../farplane-productization/SKILL.md
fails: uses only intuition; compares different tasks; keeps a surface because it sounds good
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the trust claim.
  - [ ] State the claim in falsifiable language.
  - [ ] Name the surface being tested and the user or agent behavior it should improve.
- [ ] 2. Choose one representative ablation case.
  - [ ] Keep task, inputs, and success criteria stable across both conditions.
  - [ ] Use `prototyping` when a smaller honest case is needed.
- [ ] 3. Capture both conditions.
  - [ ] Record quality, failure mode, cost, and supervision evidence.
- [ ] 4. Write claim, method, observed delta, decision, and residual risk.
- [ ] 5. Keep and roll out a meaningful win; remove, simplify, or repair a weak surface.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

- Ticket-local ablation report.
- Trust decision: keep, change, remove, or retest.
- Follow-up ticket or durable-rollout handoff only when evidence warrants it.
