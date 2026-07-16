---
skill: video-production
date: 2026-07-15
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: tickets/TASK-0378/artifacts/seedance-reference-test/visual-review.md
after_ref: tickets/TASK-0378/artifacts/seedance-reference-test/repair-1-visual-review.md
reasoning_basis: eval
proof_artifacts:
  - tickets/TASK-0378/artifacts/seedance-reference-test/repair-1-generation-receipt.json
  - tickets/TASK-0378/artifacts/seedance-reference-test/repair-1-visual-review.md
  - tickets/TASK-0378/artifacts/seedance-reference-test/repair-1-rights-review.md
  - tickets/TASK-0378/artifacts/seedance-reference-test/skill-review.json
  - tickets/TASK-0378/progress.md
eval_required: yes
---

# Seedance Reference-Conditioning Audit

## Change

- Before: the profile used source evidence only to compile prose and relied on
  original image bibles for unproven Seedance shots; Remotion later became the
  accidental owner of primary animation.
- After: an explicitly approved short source excerpt may condition
  motion/editing/style at runtime when muted, caption-cropped, excluded from the
  skill package/final edit, paired with original bibles, and independently
  reviewed for visual success and no-copy rights. Seedance owns primary
  animation; Remotion owns assembly and light VFX.
- Why: the operator rejected the deterministic animatic as completion and
  requested a reference-video-first Seedance workflow.
- Tradeoff accepted: provider spend and an additional rights gate in exchange
  for materially better model-native motion and a simpler assembly path.

## First-Principles Reasoning

- Objective: recreate the reusable low-poly storytelling grammar without
  copying source identity/content or substituting code animation for model
  output.
- Placement logic: reusable conditional behavior belongs in the collocated
  profile/prompts/example; exact experiment state belongs in the profile's
  self-improve program and TASK-0378 artifacts; one generic runtime guardrail
  belongs in video-production QA/evals.
- Expected behavior delta: approved reference video becomes a bounded provider
  input, not a final-edit asset; original bibles remain identity/setting truth;
  contact prompts use fixed landmarks and minimum world-relative displacement.
- Proof needed: actual provider output, immutable input/output/cost receipt,
  before/after visual assertion, independent rights review, skill checks, and
  independent structure/behavior review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` already requires collocated profile loading and model-native routing. |
| `reference_load_precision` | pass | Profile, prompts, and example are loaded together only after the named style resolves. |
| `missing_context_rate` | pass | Runtime authorization, source replacement, review, and assembly boundaries are present in the profile package and QA. |
| `noisy_context_rate` | pass | Exact task IDs, provider receipts, and hashes remain in TASK-0378/self-improve evidence rather than `SKILL.md`. |
| `duplicated_instruction_count` | pass | Profile owns grammar; prompts own packet syntax; example owns the filled mechanism repair; QA owns the reusable gate. |
| `prompt_size_tokens` | pass | `SKILL.md` remains 236 lines; no first-load profile recipe was added. |
| `task_success_rate` | pass | Repair flips mechanism legibility false -> true while the other five visual assertions remain true. |
| `review_tas_rate` | pass | Repair rights review is PASS/TAS-A; visual reviewer recommends promotion. |
| `maintenance_locality` | pass | Future style changes remain under the profile directory and self-improve program. |
| `composition_clarity` | pass | Source reference supplies style/motion only; original bibles supply identity/setting; Seedance supplies animation; Remotion supplies assembly. |

## First-Load Review

```yaml
first_load_review:
  line_count_before: 236
  line_count_after: 236
  kept_in_skill: existing profile-resolution and model-native routing contract
  moved_to_reference: source-conditioning recipe and mechanism-displacement pattern
  deleted_as_duplicate_or_rationale: none
  extra_sections_kept_with_reason: none added to SKILL.md
  remaining_sections_over_budget: none; SKILL.md below 250-line review threshold
  proof_surface_fit: pass; live provider proof plus independent visual/rights review
  task_case_quality: pass; eval mirrors the operator's actual source-reference request
  anti_cheat_case_design: pass; eval does not name a skill or reveal checklist wording
  qa_preflight_loaded: pass; video-production SKILL.md declares qa_checklist.md
  qa_finish_independence: pass; separate visual and rights lanes reviewed repair output
  qa_gotcha_deduplication: pass; one new QA guardrail, no duplicated gotcha catalog
  project_specific_context_isolation: pass; exact task evidence stays outside first-load refs
  low_value_prose_scan: pass; added clauses change routing, safety, proof, or ownership
  verdict: pass
```

## Proof Artifacts

- Skill-local eval: `video_production_runtime_style_reference_boundary_01`.
- Structure validation: `python3 skills/skill-maintenance/scripts/check_skills.py --write` passed.
- Reviewer receipt: PASS/TAS-A at
  `tickets/TASK-0378/artifacts/seedance-reference-test/skill-review.json`,
  SHA-256 `4b186e94050aebbaec0e7a0115801dc10bf1e49433777ec84c343c984f7d1dcc`.
- Evidence gap: full 45–50 second Seedance shot batch and voice-performance gate
  remain outside this profile-clause promotion.

## Before Behavior

Reference evidence informed prose only, and the only complete video used
Remotion as the primary animator. The first real reference-conditioned take
passed five visual assertions but its final stance did not prove loss of
traction.

## After Behavior

One reference-conditioned Seedance repair uses fixed tile seams, minimum shoe
travel, lower pelvis collapse, and a held final pose. It passes all six visual
assertions and TAS-A rights review for USD 2.9798 cumulative spend.

## Followups

- Apply the same topology to the remaining hand/rail, tire/road, and crawling
  mechanism families before the final shot batch.
- Resolve the independent voice-performance failure before full-video
  finalization.
