---
skill: video-production
date: 2026-07-17
change_type: behavior
owner: skill-maintenance
status: needs_revision
review_route: reviewer
before_ref: skills/video-production/references/scene-grid-production.md
after_ref: skills/video-production/references/scene-grid-production.md
reasoning_basis: eval
proof_artifacts:
  - tickets/TASK-0378/artifacts/lester-zero-friction-v1/annotated-storyboard-overview.png
  - tickets/TASK-0378/artifacts/lester-zero-friction-v1/annotation-map.json
  - skills/video-production/evals/evals.json
eval_required: yes
---

# Keyed Motion Annotation Hardening

## Change

- Before: the skill required panel IDs, arrows, landmarks, notes, and prompt
  references, but generic arrows between whole panels could appear sufficient.
- After: every moving subject/body part and fixed displacement landmark needs
  an in-frame ID; arrows originate on moving points; endpoints are mandatory;
  notes and provider prompts repeat the same bindings; the annotated overview
  must be readable during human approval.
- Why: TASK-0378 produced valid-looking P01/P02/P03 boards whose arrows did not
  specify the actual motion. The operator caught the gap before video spend.
- Tradeoff accepted: preparation takes longer, but motion intent becomes
  inspectable before the expensive model-native batch.

## First-Principles Reasoning

- Objective: make each approved storyboard a spatially executable provider
  contract rather than a decorative sequence.
- Placement logic: the first-load todo blocks recurrence; the method reference
  owns schema; QA and eval own repeatable proof.
- Expected behavior delta: generic panel arrows stop generation and route back
  to keyed annotation plus human review.
- Proof needed: valid JSON, skill validator pass, installed-copy parity, and a
  realistic corrected artifact packet.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` names the pre-spend gate. |
| `reference_load_precision` | pass | deliberate scene breaks load the method reference. |
| `missing_context_rate` | pass | subject, landmark, arrow, endpoint, notes, prompt, and approval are explicit. |
| `noisy_context_rate` | pass | detailed schema and example remain in the conditional reference. |
| `duplicated_instruction_count` | pass | gate, method, QA, and eval have distinct jobs. |
| `prompt_size_tokens` | pass | the first-load change is concise. |
| `task_success_rate` | pass | 9/11 Seedance scenes rendered; two privacy-blocked mechanism scenes used exact approved board states in Remotion; 47.06-second final rendered. |
| `review_tas_rate` | revise | Independent review rated the bundle TAS-B: operator acceptance of leaked marks, durable privacy receipts, and a focused eval run remain. |
| `maintenance_locality` | pass | scene-grid behavior has one method owner. |
| `composition_clarity` | pass | bindings expose IDs, points, panels, instructions, and overlay types. |

## First-Load Review

```yaml
first_load_review:
  line_count_before: 252
  line_count_after: 255
  kept_in_skill: hard pre-spend annotation gate
  moved_to_reference: detailed binding schema and definition
  deleted_as_duplicate_or_rationale: none
  extra_sections_kept_with_reason: existing method notes unchanged
  remaining_sections_over_budget: none
  proof_surface_fit: pass
  task_case_quality: pass
  anti_cheat_case_design: pass
  qa_preflight_loaded: pass
  qa_finish_independence: reviewer pending
  qa_gotcha_deduplication: pass
  project_specific_context_isolation: pass
  low_value_prose_scan: pass
  golden_calibration_independence: not_applicable
  lean_owner_reuse: pass
  verdict: pass
```

## Proof Artifacts

- Skill-local eval: `video_production_keyed_motion_annotations_01`.
- Runtime artifact: TASK-0378 corrected annotated boards and keyed prompts.
- Validator and selected-skill reinstall: pass. Independent reviewer returned
  TAS-B pending operator acceptance of leaked control marks, durable privacy
  evidence, and execution of the new focused eval.

## Before Behavior

The packet could appear complete with labels and arrows that did not bind to
feet, hands, tires, rails, or displacement rulers.

## After Behavior

The packet fails until visible points, landmarks, paths, endpoints, notes, and
provider prompts form one inspectable motion contract.

## Runtime Finding

Seedance followed the keyed motion in the completed clips, but a few small
control marks survived into pixels. The method and QA checklist now classify
that as annotation leakage and require repair, deliberate visual acceptance,
or exclusion from the edit.

## Followups

- Evaluate whether clean-grid pixel input plus prompt-only bindings reduces
  leakage without weakening motion compliance.
