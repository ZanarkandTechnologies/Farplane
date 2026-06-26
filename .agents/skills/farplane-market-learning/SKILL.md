---
name: farplane-market-learning
description: "Turn a Farplane adoption question into market-learning evidence when sharpening product, audience, or distribution bets."
tier: 3
source: local
group: product
template_uses:
  skill-template: "0.3.2"
---

# Farplane Market Learning

## Context

Use this project-local skill when Farplane needs evidence about users, pain,
adoption, alternatives, distribution channels, or market positioning before
planning product or content work.

The output is a decision-oriented learning brief, not generic research.

## Skill Signature

```text
farplane_market_learning(question, audience?, source_refs?, ticket?)
  -> learning_brief + product_or_distribution_implication + next_action
state: reads(farplane/harness.md, farplane/products.md, farplane/goals.md, source refs, ticket context); writes(brief or ticket artifact)
gates: decision_named; source_quality_named; implication_not_generic; outreach_requires_approval
routes: root skill `research` | root skill `best-of-worlds` | root skill `harness-scout` | root skill `farplane-evidence-content`
fails: produces broad market notes with no decision; changes product direction without evidence; contacts users without approval
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the learning decision.
  - [ ] State what product, audience, or distribution decision this research
    should inform.
  - [ ] Read `farplane/harness.md`, `farplane/products.md`, and
    `farplane/goals.md`.
- [ ] 2. Gather grounded evidence.
  - [ ] Use local evidence first when available.
  - [ ] Use external research only when the decision depends on current market,
    peer, or customer context.
- [ ] 3. Write the learning brief.
  - [ ] Include question, sources, findings, confidence, implication, and next
    action.
- [ ] 4. Route the implication.
  - [ ] Product implications route to weekly planning or productization.
  - [ ] Distribution implications route to evidence content.
  - [ ] Outreach, publishing, spend, or account mutation remains
    approval-required.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

- Market-learning brief path or inline brief.
- Decision implication.
- Next ticket, content handoff, or no-action rationale.
