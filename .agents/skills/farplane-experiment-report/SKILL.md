---
name: farplane-experiment-report
description: "Turn a Farplane harness hypothesis into an experiment report and next action when measuring a feature, skill, or workflow change."
tier: 3
source: local
group: product
template_uses:
  skill-template: "0.3.2"
---

# Farplane Experiment Report

## Context

Use this project-local skill when a Farplane ticket asks for an experiment that
tests whether a harness, skill, prompt, eval, validator, hook, automation, or
workflow change improves a measurable behavior.

The output is an evidence-backed experiment report, not direct productization.
If the experiment is accepted, route the follow-up to
`../farplane-productization/SKILL.md`.

## Skill Signature

```text
farplane_experiment_report(hypothesis, target_surface, metric, baseline?, variant?, ticket?)
  -> experiment_report + keep_reject_decision + follow_up_ticket_or_handoff
state: reads(farplane/harness.md, farplane/goals.md, farplane/products.md, ticket/progress/proof refs, target surface); writes(report or ticket artifact)
gates: baseline_named; metric_direction_named; evidence_not_vibes; productization_not_implicit
routes: root skill `task-case-design` | root skill `eval` | root skill `agent-behavior-test` | ../farplane-productization/SKILL.md
fails: changes strategy without evidence; claims improvement without baseline; productizes before deciding keep/reject
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the experiment.
  - [ ] Name the hypothesis, target surface, metric, expected direction, and
    decision threshold.
  - [ ] Read the ticket or current request plus `farplane/harness.md`,
    `farplane/goals.md`, and `farplane/products.md`.
- [ ] 2. Establish the comparison.
  - [ ] Use an existing baseline when available.
  - [ ] If no baseline exists, create the smallest honest baseline before
    evaluating the variant.
- [ ] 3. Run or design the proof.
  - [ ] Use deterministic validators for mechanical claims.
  - [ ] Use `eval`, `task-case-design`, or `agent-behavior-test` when the claim
    depends on agent behavior.
- [ ] 4. Write the experiment report.
  - [ ] Include baseline, variant, metric, evidence, decision, risks, and next
    action.
- [ ] 5. Route the outcome.
  - [ ] Accepted improvements route to productization.
  - [ ] Rejected hypotheses record the learning and stop.
  - [ ] Inconclusive results get one smaller follow-up only when the metric or
    baseline was flawed.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

- Experiment report path or inline report.
- Keep / reject / inconclusive decision.
- Follow-up ticket or productization handoff when accepted.
