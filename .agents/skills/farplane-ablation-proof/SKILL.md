---
name: farplane-ablation-proof
description: "Turn a Farplane trust claim into an ablation proof report when proving whether a feature or workflow actually matters."
tier: 3
source: local
group: capability
template_uses:
  skill-template: "0.3.2"
  skill-eval-task: "0.2.0"
eval: evals/evals.json
qa_checklist: qa_checklist.md
planner_contract:
  required_arguments: ["problem_ref", "system_ref", "feature_refs", "claim", "surface", "task_case", "baseline"]
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
farplane_ablation_proof(problem_ref, system_ref, feature_refs, claim, surface, task_case, baseline, with_surface?, without_surface?, expectation?, ticket?, audience_context?)
  -> ablation_report + trust_decision + follow_up
state: reads(farplane/harness.yaml, farplane/metrics.yaml, ticket audience_context first or configured Feed Scout memory as fallback, target surface, task/eval evidence); writes(ticket artifact)
gates: claim_is_specific; canonical_icp_bound; baseline_named; comparison_is_fair; evidence_cites_both_conditions; no_proof_theater
routes: root skill `prototyping` | root skill `eval` | root skill `agent-qa-test` | ../farplane-productization/SKILL.md
fails: uses only intuition; compares different tasks; keeps a surface because it sounds good
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the trust claim.
  - [ ] State the claim in falsifiable language.
  - [ ] Before reading the comparison, preregister the expected observation,
        horizon, confidence, falsifier, and surprise trigger.
  - [ ] Name the surface being tested and the user or agent behavior it should improve.
  - [ ] Read ticket-owned `audience_context` first. If absent, resolve the
        selected area's ICP and configured Feed Scout memory; name the baseline
        and the belief or workflow decision this proof should change. External
        memory is optional only when the claim is purely internal and local
        run/eval evidence is the stronger grounding.
- [ ] 2. Choose one representative ablation case.
  - [ ] Keep task, inputs, and success criteria stable across both conditions.
  - [ ] Use `prototyping` when a smaller honest case is needed.
- [ ] 3. Capture both conditions.
  - [ ] Record quality, failure mode, cost, and supervision evidence.
- [ ] 4. Write claim, method, observed delta, decision, and residual risk.
- [ ] 5. Route a material expectation miss or implausibly strong result through
      `agent-qa-test:experiment` before remove or productization; keep the
      ablation owner responsible for execution and state.
- [ ] 6. Keep and roll out a meaningful win; remove, simplify, or repair a weak surface.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

- Ticket-local ablation report.
- Trust decision: keep, change, remove, or retest.
- Follow-up ticket or durable-rollout handoff only when evidence warrants it.
