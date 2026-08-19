---
name: farplane-market-learning
description: "Turn a Farplane adoption question into decision-oriented market-learning evidence."
tier: 3
source: local
group: capability
template_uses:
  skill-template: "0.3.2"
  skill-eval-task: "0.2.0"
eval: evals/evals.json
qa_checklist: qa_checklist.md
planner_contract:
  required_arguments: ["problem_ref", "system_ref", "feature_refs", "question", "audience", "decision"]
---

# Farplane Market Learning

## Context

Use this project-local capability when Farplane needs current ICP complaint
evidence for one strategic harness system or feature before an ablation or
content decision. The output is a decision-oriented learning brief, not a
generic market report.

## Skill Signature

```text
farplane_market_learning(problem_ref, system_ref, feature_refs, question, audience, decision, source_refs?, ticket?, audience_context?)
  -> learning_brief + implication + next_action
state: reads(farplane/harness.yaml stable problems, docs/systems and docs/features registries, farplane/metrics.yaml, ticket audience_context first or configured Feed Scout Brief as fallback, current source refs, ticket context); writes(ticket artifact)
gates: strategic_ref_bound; canonical_icp_bound; current_complaint_evidence; baseline_named; decision_named; source_quality_named; implication_not_generic; outreach_requires_approval
routes: root skill `research` | root skill `best-of-worlds` | root skill `harness-scout` | ../farplane-content-creation/SKILL.md
fails: generic_market_report; repo_activity_as_customer_pain; stale_or_unsourced_complaints; produces broad notes with no decision; changes direction without evidence; contacts users without approval
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind one configured stable `problem_ref`, one canonical `system_ref`, and its relevant `feature_refs`; state the exact ablation or content decision this research can change.
- [ ] 2. Resolve the canonical ICP and baseline, then gather current direct complaint, workaround, and alternative evidence from places such as X, Reddit, GitHub, and technical discussions. Record recency, frequency, confidence, and source gaps; repo activity alone is not ICP pain.
- [ ] 3. Preserve the audience's own pain language and connect each finding to the named system/feature claim.
- [ ] 4. Write the decision brief with sources, implication, and one candidate ablation or explicit no-action result; keep external actions gated.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

- Ticket-local learning brief.
- Decision implication.
- Next ticket, content handoff, or no-action rationale.
