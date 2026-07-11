---
name: farplane-experiment-report
description: "Turn a Farplane harness hypothesis into an experiment report and next action when measuring a feature, skill, or workflow change."
tier: 3
source: local
group: capability
template_uses:
  skill-template: "0.3.2"
---

# Farplane Experiment Report

## Context

Use this project-local capability when a ticket tests whether a harness, skill,
prompt, eval, validator, hook, automation, or workflow change improves a named
behavior. The output is an evidence-backed experiment report, not automatic
rollout. Accepted results may route to `farplane-productization`.

## Skill Signature

```text
farplane_experiment_report(hypothesis, target_surface, metric, baseline?, variant?, ticket?)
  -> experiment_report + keep_reject_decision + follow_up_ticket_or_handoff
state: reads(farplane/harness.yaml, farplane/metrics.yaml, ticket/program/progress/proof refs, target surface); writes(ticket artifact)
gates: baseline_named; metric_direction_named; evidence_not_vibes; rollout_not_implicit
routes: root skill `prototyping` | root skill `eval` | root skill `agent-behavior-test` | ../farplane-productization/SKILL.md
fails: changes strategy without evidence; claims improvement without baseline; rolls out before deciding keep/reject
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Name the hypothesis, target surface, metric, expected direction, and decision rule.
- [ ] 2. Establish the smallest honest baseline and comparable variant.
- [ ] 3. Use deterministic checks for mechanical claims and behavior evals for agent claims.
- [ ] 4. Write baseline, variant, metric, evidence, decision, risks, and next action.
- [ ] 5. Route accepted results to bounded rollout; record rejected learning and stop.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

- Ticket-local experiment report.
- Keep, reject, or inconclusive decision.
- Follow-up ticket or durable-rollout handoff only when accepted.
