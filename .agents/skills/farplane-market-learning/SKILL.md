---
name: farplane-market-learning
description: "Turn a Farplane adoption question into decision-oriented market-learning evidence."
tier: 3
source: local
group: capability
template_uses:
  skill-template: "0.3.2"
planner_contract:
  required_arguments: ["problem_ref", "system_ref", "feature_refs", "question", "audience", "decision"]
---

# Farplane Market Learning

## Context

Use this project-local capability when Farplane needs evidence about users,
pain, adoption, alternatives, distribution channels, or positioning before
planning customer-facing or content work. The output is a decision-oriented
learning brief, not generic research.

## Skill Signature

```text
farplane_market_learning(problem_ref, system_ref, feature_refs, question, audience, decision, source_refs?, ticket?, audience_context?)
  -> learning_brief + implication + next_action
state: reads(farplane/harness.yaml, farplane/metrics.yaml, ticket audience_context first or configured Feed Scout memory as fallback, source refs, ticket context); writes(ticket artifact)
gates: canonical_icp_bound; baseline_named; decision_named; source_quality_named; implication_not_generic; outreach_requires_approval
routes: root skill `research` | root skill `best-of-worlds` | root skill `harness-scout` | ../farplane-content-creation/SKILL.md
fails: produces broad notes with no decision; changes direction without evidence; contacts users without approval
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. State the audience, positioning, distribution, or adoption decision this should inform. Read ticket-owned `audience_context` first; otherwise resolve the selected area's ICP and configured Feed Scout memory. Name the current baseline/default and which belief or behavior the learning could change.
- [ ] 2. Read current goals and use local evidence before external research.
- [ ] 3. Record question, sources, findings, confidence, implication, and next action.
- [ ] 4. Route useful implications to BAU planning or evidence content; keep external actions gated.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

- Ticket-local learning brief.
- Decision implication.
- Next ticket, content handoff, or no-action rationale.
