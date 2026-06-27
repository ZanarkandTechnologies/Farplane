---
kind: skill-audit
skill: landing-page
mode: harden_skill
status: pass
created_at: 2026-06-26
owner: skill-maintenance
---

# Landing Page Ambition Gate Hardening

## Behavior Delta

```text
expected_behavior:
  When the operator supplies rich landing-page effects, references, video
  scroll, 3D/WebGL, generated media, or asks for a stunning site, landing-page
  workers must choose a high-craft method first and must not ask for page
  direction feedback on a basic static artifact.

current_behavior:
  TASK-0236 worker produced a deployed static HTML/card prototype and asked for
  keep/revise/reject feedback, despite available landing-page references for
  cinematic frame sequences, composed scroll animation, generated media, and
  Three.js/WebGL.

behavior_delta:
  Add a first-load Ambition Gate, a runtime QA checklist, planner/executor
  quality-target fields, and a concrete V2 workflow artifact.
```

## Changed Files

- `skills/landing-page/SKILL.md`
- `skills/landing-page/qa_checklist.md`
- `skills/landing-page/references/planner-executor.md`
- `tickets/TASK-0236/artifacts/landing-page-offer-v2/STUNNING_WORKFLOW.md`

## First-load Review

```text
line_count_before: 392
line_count_after: 448
kept_in_skill:
  - Ambition Gate
  - quality_target todo
  - supplied effects inventory todo
  - downgrade/feedback guardrails
moved_to_reference:
  - detailed planner/executor quality-target fields
  - full runtime checklist in qa_checklist.md
deleted_as_duplicate_or_rationale: none
extra_sections_kept_with_reason:
  - Ambition Gate: first-load guardrail needed before a worker chooses a build
    depth or sends feedback.
remaining_sections_over_budget:
  - SKILL.md was already long; this hardening keeps the prevention rule in
    first-load because deferring it caused the observed failure.
proof_surface_fit:
  - Markdown runtime checklist plus skill audit; future eval can cover this if
    repeated.
task_case_quality:
  - Source case is TASK-0236, where a stunning/premium expectation degraded to a
    static deployed page.
anti_cheat_case_design: not_applicable
qa_preflight_loaded:
  - SKILL.md now points to qa_checklist.md before implementation.
qa_finish_independence:
  - SKILL.md now requires qa_checklist.md in final QA.
qa_gotcha_deduplication:
  - Short first-load gotchas remain; detailed checks live in qa_checklist.md.
project_specific_context_isolation:
  - Generic skill hardening kept in skill; TASK-specific plan lives under the
    ticket artifact.
low_value_prose_scan:
  - skipped; hardening is preventive and first-load-relevant.
verdict: pass
```

## Validation

`python3 skills/skill-maintenance/scripts/check_skills.py --write` passed.

Key signals:

- skill todo list sections OK
- skill registry OK, 97 rows
- skill todo tier check OK
- Tier 0 phase protocol check OK
- doc refs OK, 1741 refs checked
- Python validator compile checks passed
