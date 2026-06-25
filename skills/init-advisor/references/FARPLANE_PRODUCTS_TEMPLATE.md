---
kind: project-products
status: draft
project: "{{PROJECT_NAME}}"
created_at: "{{DATE}}"
updated_at: "{{DATE}}"
framework_template_version: "0.1.0"
owner: harness
source_of_truth:
  - farplane/harness.md
  - farplane/goals.md
  - skills/pulse-update/SKILL.md
---

# Project Products

This file defines the repeatable outputs this project exists to create. Products
are not chores. Products are the value artifacts a team should refill tickets
toward when the board is empty or stale; chores stay in Pulse's default action
arms.

## Team Archetype

TODO: Describe what kind of team this project is. Examples:

- autonomous AI harness lab
- product engineering team
- marketing team
- research team
- personal operating system
- customer success / operations team

Store the short archetype string in `farplane/manifest.json` as
`project.archetype`; keep the richer explanation here.

## Operating Flywheel

```text
TODO input or signal
  -> research real-world equivalents and current baseline
  -> TODO repeatable project/action
  -> TODO proof or review
  -> TODO product/output
  -> TODO feedback into next cycle
```

## Primary Products

| Product | Audience | Artifact Examples | Reward Signals | Owner Skills |
| --- | --- | --- | --- | --- |
| Core product | target users | artifact examples | success signals | owner skills |

## Supporting Products

| Product | Audience | Artifact Examples | Reward Signals | Owner Skills |
| --- | --- | --- | --- | --- |
| Supporting product | target users or team | artifact examples | success signals | owner skills |

## Autonomous Project Types

| Project Type | When To Create It | Output | Proof / Reward Signal |
| --- | --- | --- | --- |
| Experiment | A change might improve the project. | Experiment ticket and result note | improvement against baseline |
| Ablation | An implemented feature needs proof or a with/without comparison. | Ablation report and decision | accepted claim, rejected feature, or proof gap |
| Productization | A proven win should become durable. | Product, feature, skill, doc, workflow, or asset | accepted implementation with proof |
| Evidence distribution | A proven result can teach users or grow adoption. | Demo, post, note, video, or onboarding artifact | qualified attention or useful feedback |
| Market learning | A promising win needs demand evidence. | Interview, parity scan, gap brief, or opportunity note | clearer product bet or rejected assumption |
| Admin / maintenance | Work is needed to keep the team operating. | Research, cleanup, hardening, metadata repair, blocker clarification | reduced drag or unblocked product work |

## Admin Work

Admin work is allowed, but it is not the project product. Treat customer
research, market research, source scans, codebase maintenance, dependency
cleanup, ticket metadata repair, blocker clarification, and routine hardening as
admin unless they directly feed a primary product, productization decision, or
distribution artifact.

## Product Selection Notes

- Prefer primary products when the current goals or interval plan show a clear
  need for product work.
- Use supporting products when the project needs adoption, learning, evidence,
  or internal leverage.
- Productize only after evidence supports the change.
- Treat adoption as evidence distribution, not generic marketing. Content should
  be grounded in accepted work, user questions, or adoption gaps.
- Do not treat routine metadata repair, blocker clarification, QA collection,
  report writing, or ticket cleanup as products. Those are chores or proof
  actions.

## Pulse Refill Guidance

When no proceedable ticket exists, Pulse may create or refine one product-shaped
ticket if the product need is grounded in goals, interval guidance, recent
Pulse outcomes, user feedback, or source gaps. The ticket should name the
project type, intended audience, expected artifact, proof signal, owner skill,
baseline or comparison point, and why the work is not just a chore.

If no product-shaped refill is grounded, Pulse should fall back to default chore
arms such as metadata repair, QA/eval collection, blocker clarification, or
Goal Advisor consultation.
