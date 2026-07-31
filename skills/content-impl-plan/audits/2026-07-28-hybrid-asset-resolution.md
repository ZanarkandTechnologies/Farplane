---
skill: content-impl-plan
date: 2026-07-28
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/content-impl-plan/audits/2026-07-27-asset-discovery-svg-ban.md
after_ref: skills/asset-advisor/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/asset-advisor/evals/evals.json
  - .farplane/evals/runs/20260728-161631-hybrid-asset-resolution-r7/summary.json
eval_required: yes
---

# Hybrid asset resolution audit

## Change

- Before: visual discovery selected an existing source or required
  `searched_no_fit` before generation, except when the brief explicitly
  required generation.
- After: visual discovery returns `selected_source`,
  `inspiration_for_generation`, or `searched_no_reference`; the asset decision
  ladder is `reuse -> source -> inspired_generation -> original_generation`.
- Why: a useful stock reference may be valuable as creative grounding without
  being the best final scene asset. Generation should preserve those useful
  traits while producing original raster/video media.
- Tradeoff accepted: generation packets are more explicit because inspiration
  provenance, transferable traits, must-not-copy constraints, owner, prompt,
  output path, rights/likeness note, and acceptance check must survive the
  handoff.

## First-Principles Reasoning

- Objective: maximize scene-specific asset quality without returning to
  authored SVG/JSX substitutes or treating stock libraries as the only valid
  source.
- Placement logic: Asset Advisor owns the decision and receipt. Content
  Implementation Plan and Storyboard preserve it. AI Image/Video Advisor binds
  it into model input. Remotion consumes only accepted materialized files.
- Expected behavior delta: useful search results may route either direct source
  use or inspired original generation; a genuine no-reference result routes
  original generation rather than blocking forever.
- Proof needed: focused skill eval, JSON/link/registry checks, source scan for
  obsolete visual `searched_no_fit` gates, and independent review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Hybrid decision and required packet fields are in each affected `SKILL.md`. |
| `reference_load_precision` | pass | Scene-bundle and documentary detail stays in existing conditional references. |
| `missing_context_rate` | pass | Rights, provenance, avoidance, output, and acceptance fields survive all handoffs. |
| `noisy_context_rate` | pass | The detailed schema stays in Asset Advisor; downstream skills carry compact boundary rules. |
| `duplicated_instruction_count` | pass | Asset Advisor owns resolution; callers and executors only preserve or enforce it. |
| `prompt_size_tokens` | unknown | No token benchmark run. |
| `task_success_rate` | pass | Focused behavior eval R7 passed 1/1 with verdict A. |
| `review_tas_rate` | pass | Final independent rereview: TAS-A, no blocking findings. |
| `maintenance_locality` | pass | Resolution vocabulary and receipt are owned by Asset Advisor. |
| `composition_clarity` | pass | Planner, generator, and Remotion ownership boundaries are explicit. |

## Proof Artifacts

- Skill-local evals: added
  `asset_advisor_hybrid_source_or_generate_01`; updated affected integration
  assertions. R7 passed 1/1 with verdict A and behavior verdict pass.
- Structure evals: `check_skills.py --write` completed registry, todo-link,
  tier, and Tier 0 checks before stopping on pre-existing
  `content-impl-plan` surface-budget debt (19 QA items and 19 evals vs limit
  5). This change did not add a Content Implementation Plan QA item or eval.
- Reviewer receipt: initial TAS-B found two contradictory accepted-file gates;
  both were repaired. Final rereview passed TAS-A with no blockers.
- Validator: focused JSON, diff, registry, todo-tier, and Tier 0 checks.
- Eval required: yes.
- Installed-copy proof: the six selected live skill copies match their repo
  sources byte-for-byte after selected install.
- Evidence gaps: live generation is outside this policy-only change.

## Before Behavior

`search -> selected source | searched_no_fit -> generation`

## After Behavior

`search -> selected source | inspiration packet | no-reference result`

`inspiration packet -> original raster/video generation`

`no-reference result -> original raster/video generation`

`accepted materialized file -> Remotion`

## Followups

- Resolve the existing Content Implementation Plan surface-budget debt in a
  separate compaction pass; do not fold that broad restructuring into this
  behavior correction.
