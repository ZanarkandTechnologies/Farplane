---
skill: learn-from-video
date: 2026-07-28
change_type: behavior-and-eval
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: .farplane/evals/runs/20260728-152426-task0419-baseline-3case
after_ref: .farplane/evals/runs/20260728-154342-task0419-full-4case-final-r5
reasoning_basis: eval
proof_artifacts:
  - tickets/TASK-0419/artifacts/learned-video-packet.md
  - tickets/TASK-0419/artifacts/comparison.md
  - skills/learn-from-video/evals/evals.json
eval_required: yes
---

# Skill Audit

## Change

- Before: three eval cases covered a happy reconstruction, a generic-demo
  rejection, and insufficient private evidence.
- After: a fourth cold case carries a real narrated candidate, frozen
  source-output eval, manifest, contact sheet, and preserved failed transition;
  the root workflow also prevents substitute content from becoming a fidelity
  requirement and prevents a repair plan from substituting for a generated
  replacement candidate.
- Why: TASK-0419 demonstrated that render integrity and plausible style can
  still hide a failed scene boundary, and suite replay exposed two neighboring
  acceptance ambiguities.
- Tradeoff accepted: a 652 KB rights-safe 1080p proxy of the accepted candidate
  plus two narrow first-load gates in exchange for executable regression proof.

## First-Principles Reasoning

- Objective: make “learned from a tutorial” mean observable workflow transfer.
- Placement logic: fixture and acceptance behavior belong to
  `learn-from-video`; Remotion continues to own implementation; identity stays
  in the Brand Kit.
- Expected behavior delta: inspect complete evidence, preserve failed media,
  distinguish integrity from fidelity, require the real replacement candidate,
  and never mistake clean-room content for a source mechanic.
- Proof needed: targeted cold eval, unchanged full suite, media/type checks,
  structure validation, and independent review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | both new normal-path gates are in Todo 4/7 |
| `reference_load_precision` | pass | no new conditional reference |
| `missing_context_rate` | pass | source anchors, candidate, frozen eval, and regression are staged |
| `noisy_context_rate` | pass | two short gates; detailed case remains in eval fixtures |
| `duplicated_instruction_count` | pass | no new production instructions |
| `task_success_rate` | pass | final suite is 4/4 TAS-A with 4/4 behavior traces |
| `review_tas_rate` | pass | TASK-0419 independent review is TAS-A |
| `maintenance_locality` | pass | workflow behavior and proof remain in one package |
| `composition_clarity` | pass | production ownership is unchanged |

## Eval History

| Run | Result | Observation | Decision |
| --- | --- | --- | --- |
| `20260728-152426-task0419-baseline-3case` | 3/3 TAS-A | prior suite healthy | preserve |
| `20260728-152724-task0419-script-led-workflow` | TAS-C, 5/7 | candidate package lacked frozen-eval provenance | add missing fixture; prompt/assertions unchanged |
| `20260728-152901-task0419-script-led-workflow-r2` | TAS-A, 7/7 | complete package produced correct blocked-for-review handoff | accept fixture |
| `20260728-153034-task0419-full-4case-final` | failed during replay | substitute content promoted to must-match; generic repair did not explicitly require a replacement candidate | add two narrow root gates |
| `20260728-153335-task0419-full-4case-final-r2` | failed during replay | required frozen fields and individual comparison checks were still omitted | harden packet schema |
| `20260728-154043-task0419-script-led-r4` | TAS-A, 7/7 | new case returns a replayable review-gated packet | accept targeted behavior |
| `20260728-154229-task0419-existing-happy-r5` | TAS-A, 7/7 | legacy case uses real frozen provenance and blocks exact mismatches | accept legacy behavior |
| `20260728-154342-task0419-full-4case-final-r5` | 4/4 TAS-A, 4/4 behavior pass | unchanged full replay | accept candidate pending review |
| `20260728-160552-task0419-script-led-proxy-r8` | TAS-A, 7/7 | sub-1 MB 1080p committed proxy preserves the cold reconstruction behavior | accept repository fixture |

## Structure QA

```text
first_load_review:
  authored_file_structure: pass
  kept_in_skill: source-only must-match gate; real replacement candidate gate
  moved_to_reference: none
  deleted_as_duplicate_or_rationale: none
  extra_sections_kept_with_reason: none added
  proof_surface_fit: pass; variable agent behavior is covered by eval
  task_case_quality: pass; real candidate and preserved failure
  anti_cheat_case_design: pass; prompt omits mechanics and owner answer
  qa_preflight_loaded: pass
  qa_finish_independence: pass; independent-review.md is TAS-A
  qa_gotcha_deduplication: pass
  project_specific_context_isolation: pass
  low_value_prose_scan: pass
  golden_calibration_independence: pass
  lean_owner_reuse: pass
  verdict: pass
```

## Followups

- Do not add a Remotion root rule or a Vox production skill from this one case.
- Reconsider a focused Remotion example only after a second independent
  narration-boundary or persisted-control failure.
