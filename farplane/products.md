---
kind: project-products
status: active
project: Farplane
created_at: 2026-06-25
updated_at: 2026-06-26
framework_template_version: "0.2.0"
owner: harness
source_of_truth:
  - farplane/harness.md
  - farplane/goals.md
  - skills/interval-update/SKILL.md
---

# Farplane Products

## Team

| Field | Value |
| --- | --- |
| Archetype | autonomous_ai_harness_lab |
| Core product | evidence-backed harness improvements |
| Secondary product | trust distribution from proven work |

## Products

| ID | Product | Audience | Output | Reward |
| --- | --- | --- | --- | --- |
| experiments | Experiment reports | builders, researchers, Farplane operators | baseline, variant, measurement, decision | validated improvement or rejected hypothesis |
| ablations | Trust ablations | skeptical operators and reviewers | with/without comparison, proof report, decision | accepted or rejected trust claim |
| productization | Harness improvements | Farplane users and projects | skill, spec, eval, validator, hook, automation, or UI handoff | reviewed shipped behavior |
| distribution | Evidence content | potential users and serious builders | post, demo, video, paper, or launch note | qualified attention, useful feedback, adoption |
| market_learning | Market learning | Farplane strategy owners | interview, parity scan, opportunity brief | sharper product or distribution bet |

## Work Lanes

| Lane | Default Weight | Purpose |
| --- | ---: | --- |
| metric_experiments | 30 | improve measured harness behavior |
| trust_ablations | 20 | prove or reject trust claims |
| productization | 20 | ship accepted wins |
| trust_distribution | 15 | distribute proven evidence |
| market_learning | 10 | sharpen user and pain understanding |
| maintenance | 5 | keep the system operable |

## Constraints

- Products are not chores.
- Pulse executes tickets; intervals create, split, reprioritize, or request
  product-shaped tickets.
- Operational planning, refill, and prioritization logic belongs in
  `interval-update`, not this file.
