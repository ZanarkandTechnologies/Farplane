---
kind: project-products
status: active
project: Farplane
created_at: 2026-06-25
updated_at: 2026-06-25
framework_template_version: "0.1.0"
owner: harness
source_of_truth:
  - farplane/harness.md
  - farplane/goals.md
  - skills/pulse-update/SKILL.md
---

# Farplane Products

This file defines the repeatable outputs this project exists to create. Products
are not chores. Products are the value artifacts a team should refill tickets
toward when the board is empty or stale; chores stay in Pulse's default action
arms.

## Team Archetype

Farplane is an autonomous AI harness lab. Its job is to write evidence-backed
papers about agent harness behavior, run experiments and ablations, reject weak
changes, productize accepted wins into Farplane itself, and distribute trust by
turning real pain points into educational product content.

## Operating Flywheel

```text
observe harness pain, trust gap, or efficiency opportunity
  -> research real-world equivalents and current baseline
  -> write an experiment or ablation plan
  -> run the experiment with proof, metrics, and a comparison point
  -> write a paper/report with accepted, rejected, or deferred decision
  -> productize successful experiments into Farplane
  -> distribute evidence through pain-point marketing or educational content
  -> use adoption, trust, and operator feedback to choose the next experiment
```

## Primary Products

| Product | Audience | Artifact Examples | Reward Signals | Owner Skills |
| --- | --- | --- | --- | --- |
| Papers and experiment reports | builders, researchers, Farplane operators | research notes, experiment reports, ablation reports, result writeups | accepted/rejected decisions, clearer claims, reproducible evidence | `research`, `eval`, `optimize-harness`, `documentation` |
| Metric-optimizing feature experiments | Farplane Core and downstream projects | baseline, variant, measurement plan, experiment ticket, result artifact | better autonomy, quality, proof closure, context isolation, or intervention efficiency | `optimize-harness`, `harness-advisor`, `eval` |
| Trust ablations for implemented features | skeptical operators and reviewers | with/without comparisons, feature ablations, trust reports | proven usefulness, reduced false completion, stronger proof, rejected fluff | `eval`, `agent-qa-test`, `review`, `proof-advisor` |
| Productized harness improvements | Farplane users and projects | framework files, skills, validators, runtime hooks, automations, specs | successful experiment becomes accepted product behavior | `harness-advisor`, `skill-maintenance`, `automation-advisor` |
| Trust distribution content | builders, researchers, potential users | real-pain-point product marketing, educational posts, demos, videos | qualified attention, serious conversations, adoption feedback | `social-content`, `video-production`, `research` |

## Supporting Products

| Product | Audience | Artifact Examples | Reward Signals | Owner Skills |
| --- | --- | --- | --- | --- |
| Customer and market learning | Farplane strategy owners | interviews, opportunity briefs, parity scans, feedback syntheses | sharper trust distribution, better productization choices | `research`, `feed-scout`, `horizon-advisor` |
| Adoption examples | new Farplane projects | initialized project examples, Goal Packets, report samples, ticket walkthroughs | more projects reaching first measured loop | `init-advisor`, `goal-advisor`, `documentation` |
| Codebase and harness hardening | Farplane maintainers | refactors, validator hardening, dependency cleanup, bug fixes | lower maintenance drag, fewer repeated failures | `skill-maintenance`, `testing`, `runtime-debugging` |

## Autonomous Project Types

| Project Type | When To Create It | Output | Proof / Reward Signal |
| --- | --- | --- | --- |
| Metric experiment paper | An existing feature or workflow may improve a target metric. | Experiment plan, run artifact, paper/report | measurable improvement or rejected hypothesis |
| Trust ablation paper | An implemented feature needs proof that it actually increases trust. | With/without comparison, ablation report, decision | accepted trust claim, rejected feature, or follow-up proof gap |
| Productization | A successful experiment should become durable Farplane behavior. | Framework, skill, eval, hook, doc, automation, or UI handoff | accepted implementation with proof and review |
| Trust distribution | A proven result maps to a real user pain point or trust objection. | Educational content, product marketing, demo, video, or launch note | qualified attention, serious conversations, adoption feedback |
| Admin / maintenance | Work is necessary to keep the lab operating but is not a product. | Research note, cleanup, hardening, metadata repair, blocker clarification | reduced drag, cleaner board, better future experiments |

## Admin Work

Admin work is allowed, but it is not the main product of the Farplane Core
team. Treat customer research, market research, source scans, codebase
maintenance, dependency cleanup, ticket metadata repair, blocker clarification,
and routine hardening as admin unless they directly feed a paper, experiment,
productization decision, or trust distribution artifact.

## Product Selection Notes

- Prefer papers/experiments when the current weekly plan, goals, or board state
  shows a measurable autonomy, quality, proof, trust, or context-isolation gap.
- Prefer productization only after an experiment or ablation has produced an
  accepted win.
- Prefer trust distribution only when a proven result maps to a real user pain
  point, trust objection, or educational angle.
- Treat adoption as evidence distribution, not generic marketing. Do not create
  content unless it is grounded in an accepted experiment, ablation, product
  improvement, user question, or adoption gap.
- Do not treat routine metadata repair, blocker clarification, QA collection,
  report writing, or ticket cleanup as products. Those are chores or proof
  actions.
- When products conflict, prefer the product with the clearest reward signal
  inside the current weekly interval plan.

## Pulse Refill Guidance

When no proceedable ticket exists, Pulse may create or refine one product-shaped
ticket in this priority order:

1. write a metric experiment paper for an existing feature or workflow.
2. write a trust ablation paper for an implemented feature.
3. productize a successful experiment into Farplane itself.
4. create trust distribution from accepted evidence and a real pain point.
5. run admin work only when it unblocks the above.

The ticket should name the project type, intended audience, expected artifact,
proof signal, owner skill, baseline or comparison point, and why the work is not
just a chore.

If no product-shaped refill is grounded, Pulse should fall back to default chore
arms such as metadata repair, QA/eval collection, blocker clarification, or
Goal Advisor consultation.
