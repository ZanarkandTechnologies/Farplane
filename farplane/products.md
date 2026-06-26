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

## Taste Loop Artifact Workflows

Taste Loop turns active human attention into feedback on generated artifacts,
not feedback on skill summaries. Each candidate must name a product lane,
artifact workflow, owning skill or method, and reviewable output.

| Lane | Workflow ID | Owner | Reviewable Artifact | Feedback Question |
| --- | --- | --- | --- | --- |
| trust_distribution | landing_page_offer | `landing-page` | landing page draft, HTML, or screenshot | keep / revise / reject the offer and page direction |
| trust_distribution | social_thread | `social-content:twitter-thread` | draft thread | keep / revise / reject the hook and argument |
| trust_distribution | evidence_carousel | `social-content:carousel` | carousel outline or slides | keep / revise / reject the proof story |
| trust_distribution | explainer_script | `video-production:explainer` | short script or storyboard | keep / revise / reject the explanation |
| trust_distribution | demo_video_brief | `video-production:marketing` | video concept, shot list, or demo script | keep / revise / reject the demo angle |
| market_learning | offer_test | `landing-page` | offer variants or landing page section | pick best / revise / reject the offer |
| experiments | experiment_report | `farplane-experiment-report` | experiment report draft | accept / revise / reject the decision |
| ablations | ablation_proof | `farplane-ablation-proof` | ablation proof report | accept / revise / reject the proof |
| productization | productization_handoff | `farplane-productization` | shipped-behavior proposal or handoff | accept / revise / reject the productization move |

## Constraints

- Products are not chores.
- Pulse executes tickets; intervals create, split, reprioritize, or request
  product-shaped tickets.
- Operational planning, refill, and prioritization logic belongs in
  `interval-update`, not this file.
- Taste Loop feedback cards must point to a generated artifact from a workflow
  in `Taste Loop Artifact Workflows`; broad router skills such as
  `frontend-craft`, `functional-ui`, `remotion`, and `remotion-render` can
  support those workflows but are not direct Taste Loop targets.
