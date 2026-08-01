---
title: Learn-from-video scope-confirmation hardening
status: accepted
owner: learn-from-video
kind: skill-audit
created_at: 2026-08-02
source_refs:
  - .farplane/learn-from-video/DZdCD2YNk4d/
changed_files:
  - skills/learn-from-video/SKILL.md
  - skills/learn-from-video/qa_checklist.md
  - skills/learn-from-video/evals/evals.json
---

# Scope-confirmation hardening

## Behavior delta

```text
expected_behavior:
  broad request + multiple source-grounded targets
  -> concise target choices
  -> operator confirmation
  -> frozen eval and candidate
current_behavior:
  optional learning_goal could be silently narrowed before eval freeze
mode: harden_skill
```

> **Before:** “Make something similar” could become one inferred technique.
> **After:** Multiple plausible learning layers require confirmation before the
> frozen eval or candidate generation.
> **Example:** An editorial reference produces choices for layout/type, camera,
> annotations, print treatment, and `full_system`; the operator may select more
> than one.

## Evidence

The retained regression packet first reconstructed only animated line mechanics.
The operator then clarified that the intended target also included newspaper
layout, zooms, arrows, circles, underlines, grain, and typography. The former
contract made `learning_goal` optional and lacked a hard confirmation gate.

## Proof plan

- New held-out skill eval:
  `learn_video_confirms_ambiguous_scope_before_reconstruction_01`.
- Round-one candidate returned the correct clarification gate but offered five
  choices. The repaired contract caps the complete choice set at four and makes
  `full_system` consume one slot.
- Final focused behavior eval passed TAS-A:
  `.farplane/evals/runs/20260801-181130-20260802-scope-newsprint-round2/summary.json`.
- Runtime prevention is present in the skill gates, todo path, QA, and output
  schema.
- Query-spoiler check and full skill-system validation must pass.
- Independent reviewer must return TAS-A before acceptance.

## Structure review

```text
first_load_review:
  authored_file_structure: unchanged
  kept_in_skill: scope gate, normal-path decision rule, output field
  moved_to_reference: none
  deleted_as_duplicate_or_rationale: none
  extra_sections_kept_with_reason: none
  proof_surface_fit: behavior eval + QA + independent review
  task_case_quality: realistic broad reference request based on sanitized regression
  anti_cheat_case_design: user prompt does not name the skill or expected route
  qa_preflight_loaded: yes
  qa_finish_independence: reviewer TAS-A
  qa_gotcha_deduplication: pass
  project_specific_context_isolation: pass
  low_value_prose_scan: pass
  golden_calibration_independence: pass
  lean_owner_reuse: pass
  behavior_eval_verdict: A
  verdict: accepted
```

Independent reviewer verdict: TAS-A, no hard gates or blocking findings.
