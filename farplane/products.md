---
kind: project-products
status: active
project: Farplane
created_at: 2026-06-25
updated_at: 2026-07-03
framework_template_version: "0.2.0"
owner: harness
source_of_truth:
  - farplane/harness.md
  - farplane/goals.yaml
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

## Product Skill Breakdown

| Product | Primary skill | Supporting skills | Notes |
| --- | --- | --- | --- |
| Experiment reports | `farplane-experiment-report` | `metric-advisor`, `proof-advisor`, `eval`, `review`, `update-strategy` | Measures a harness hypothesis, records baseline/variant evidence, and turns the decision into either rejection, iteration, or productization. |
| Trust ablations | `farplane-ablation-proof` | `proof-advisor`, `agent-qa-test`, `agent-behavior-test`, `eval`, `review` | Proves whether a feature or workflow matters through with/without comparison and evidence review. |
| Harness improvements | `farplane-productization` | `impl-plan`, `goal-advisor`, `qa`, `demo`, `close-ticket`, `skill-maintenance`, `harness-advisor` | Converts accepted evidence into shipped harness behavior, with ticket proof and reviewer gates. |
| Evidence content | `farplane-evidence-content` | `content-impl-plan`, `storyboard`, `asset-advisor`, `avatar-advisor`, `audio-advisor`, `remotion`, `social-content`, `landing-page`, `video-production`, `infographic`, `reel-collage`, `product-photography`, `ai-image-advisor`, `ai-video-advisor`, `x-account`, `instagram-account` | Turns accepted evidence into distribution artifacts; `content-impl-plan` compiles idea plus Tasty Pack/reference into an advisor action list, while child skills own craft, assets, generation routes, composition, and platform constraints. |
| Market learning | `farplane-market-learning` | `research`, `deep-interview`, `harness-scout`, `best-of-worlds`, `landing-page`, `social-content`, `update-strategy` | Sharpens audience, pain, offer, and distribution bets before product or content execution. |

## Taste Loop Artifact Workflows

Taste Loop turns active human attention into feedback on product-lane
artifacts, not feedback on skill summaries. Each candidate must name a product
lane, artifact workflow, owning skill or method, planning artifact, execution
artifact, and the compact feedback question. Planning artifacts are first-class:
they let Kenji reject or approve ideas before Farplane spends execution effort.

| Lane | Workflow ID | Owner | Planning Artifact | Execution Artifact | Feedback Question |
| --- | --- | --- | --- | --- | --- |
| trust_distribution | landing_page_offer | `landing-page` | offer angle, hero premise, or concept card | landing page draft, HTML, screenshot, or preview URL | keep / revise / reject the offer and page direction |
| trust_distribution | social_thread | `social-content:twitter-thread` | hook and argument concept card | draft thread | keep / revise / reject the hook and argument |
| trust_distribution | evidence_carousel | `social-content:carousel` | proof story concept card | carousel outline or slides | keep / revise / reject the proof story |
| trust_distribution | explainer_script | `content-impl-plan` | explanation angle, Tasty Pack/reference, or storyboard premise | short script, storyboard, and advisor action list | keep / revise / reject the explanation |
| trust_distribution | demo_video_brief | `content-impl-plan` | demo angle, proof claim, or Tasty Pack/reference | video concept, storyboard, asset plan, and Remotion route | keep / revise / reject the demo angle |
| market_learning | offer_test | `landing-page` | offer hypothesis variants | landing page section or offer test draft | pick best / revise / reject the offer |
| experiments | experiment_report | `farplane-experiment-report` | experiment decision angle | experiment report draft | accept / revise / reject the decision |
| ablations | ablation_proof | `farplane-ablation-proof` | proof claim and contrast plan | ablation proof report | accept / revise / reject the proof |
| productization | productization_handoff | `farplane-productization` | productization bet and user-facing delta | shipped-behavior proposal or handoff | accept / revise / reject the productization move |

## Constraints

- Products are not chores.
- Pulse executes tickets; intervals create, split, reprioritize, or request
  product-shaped tickets.
- Operational planning, refill, and prioritization logic belongs in
  `interval-update`, not this file.
- Taste Loop idea feedback cards must point to a planning artifact from a
  workflow in `Taste Loop Artifact Workflows`.
- Taste Loop execution feedback cards must point to an execution artifact from
  the same workflow after the planning artifact passes, unless the execution
  artifact is explicitly a tiny planning test.
- Broad router/support skills such as
  `frontend-craft`, `functional-ui`, `remotion`, and `remotion-render` can
  support those workflows but are not direct Taste Loop targets. `content-impl-plan`
  is a direct planning target for evidence-content video production because it
  creates the reviewable ticket/action list before media execution.
