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
compounding claim about a core harness system with a with/without comparison.
The tested variable must be an actual harness surface such as `AGENTS.md`, a
skill, eval, review, QA checklist, template, or automation—not a random feature.

The output is a trust ablation report: what changes when the surface is present
versus absent, and whether the claim should remain part of the harness.

## Skill Signature

```text
farplane_ablation_proof(problem_ref, system_ref, feature_refs, claim, surface, task_case, baseline, with_surface?, without_surface?, expectation?, ticket?, audience_context?)
  -> ablation_report + trust_decision + follow_up
state: reads(farplane/harness.yaml stable problems, docs/systems and docs/features registries, current ICP complaint evidence, farplane/metrics.yaml, ticket audience_context first or configured Feed Scout Brief as fallback, target surface, task/eval evidence); writes(ticket artifact)
gates: strategic_ref_bound; compounding_difference; one_main_variable; claim_is_specific; canonical_icp_bound; current_pain_grounded; recognizable_baseline; comparison_is_fair; visible_result; evidence_cites_both_conditions; no_proof_theater
routes: root skill `prototyping` | root skill `eval` | root skill `agent-qa-test` | ../farplane-productization/SKILL.md
fails: random_feature; generic_internal_test; multiple_main_variables; uses only intuition; compares different tasks; keeps a surface because it sounds good
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind one stable `problem_ref`, canonical `system_ref`, relevant `feature_refs`, and the current ICP complaint evidence that makes this a consequential Farplane difference.
- [ ] 2. Bind the trust claim.
  - [ ] State the claim in falsifiable language.
  - [ ] Before reading the comparison, preregister the expected observation,
        horizon, confidence, falsifier, and surprise trigger.
  - [ ] Name the surface being tested and the user or agent behavior it should improve.
  - [ ] Read ticket-owned `audience_context` first. If absent, resolve the
        selected area's ICP and configured Feed Scout Brief; name the baseline
        and the belief or workflow decision this proof should change. External
        memory is optional only when the claim is purely internal and local
        run/eval evidence is the stronger grounding.
- [ ] 3. Choose one representative ablation case with one main harness variable and a recognizable baseline.
  - [ ] Keep task, inputs, and success criteria stable across both conditions.
  - [ ] Use `prototyping` when a smaller honest case is needed.
- [ ] 4. Capture both conditions and a visible result; record quality, failure mode, cost, supervision, and audience-relevant consequence.
- [ ] 5. Write claim, method, observed delta, residual risk, and an explicit `keep | modify | delete` decision.
- [ ] 6. Route a material expectation miss or implausibly strong result through
      `agent-qa-test:experiment` before `delete` or productization; keep the
      ablation owner responsible for execution and state.
- [ ] 7. Route a meaningful win to content and productization; simplify or remove a weak surface.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

- Ticket-local ablation report.
- Trust decision: keep, change, remove, or retest.
- Follow-up ticket or durable-rollout handoff only when evidence warrants it.
