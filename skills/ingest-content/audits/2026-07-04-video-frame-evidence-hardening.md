---
skill: ingest-content
date: 2026-07-04
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/ingest-content/SKILL.md
after_ref: skills/ingest-content/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/ingest-content/eval_task.json
  - skills/ingest-content/qa_checklist.md
eval_required: yes
---

# Skill Audit

## Change

- Before: Video/social visual-style ingestion could fall back to public
  metadata and thumbnail evidence after one failed media fetch.
- After: Video/social visual-style ingestion must escalate through available
  evidence routes and produce representative frames/contact sheet, or mark
  thumbnail-only as degraded evidence with attempted routes and blockers.
- Why: The operator's Instagram reference had accessible video through browser
  cookies, but the first ingestion saved only thumbnail-backed analysis.
- Tradeoff accepted: The skill now requires extra extraction effort for visual
  video references, but saves materially better reusable levers and prevents
  false confidence.

## First-Principles Reasoning

- Objective: Save reusable inspiration with enough evidence for future creator
  skills to recover the actual style, pacing, and visual system.
- Placement logic: `ingest-content/SKILL.md` owns every-invocation gates;
  `references/phase-router.md` owns the route ladder; `qa_checklist.md` and
  `eval_task.json` own runtime and regression checks.
- Expected behavior delta: Thumbnail-only becomes a degraded fallback rather
  than normal completion for video style notes.
- Proof needed: Skill validation plus an eval reference case that would fail
  the original behavior.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` gates, fails, todos, gotcha updated. |
| `reference_load_precision` | pass | Phase-router carries route ladder detail. |
| `missing_context_rate` | pass | QA checklist and eval specify frame-backed expectation. |
| `noisy_context_rate` | pass | Added concise operational gates only. |
| `duplicated_instruction_count` | pass | Detailed ladder lives in reference; first-load has gate and todos. |
| `prompt_size_tokens` | unknown | Not measured. |
| `task_success_rate` | unknown | Requires future ingestion runs. |
| `review_tas_rate` | unknown | No independent reviewer was run. |
| `maintenance_locality` | pass | Changes stay inside `skills/ingest-content/`. |
| `composition_clarity` | pass | Media route remains delegated to `media-ingest`; storage remains in `ingest-content`. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/ingest-content/eval_task.json`
- Structure evals, when needed: not run.
- Reviewer receipt: not run; self-check only.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
- Eval required: yes; regression case added, not executed.
- Evidence gaps: Future live eval runner should exercise the regression with a
  sandboxed social-video fixture or mocked browser-cookie availability.

## Before Behavior

- A public social video with metadata and thumbnail could be saved as
  thumbnail-only when unauthenticated video fetch failed.

## After Behavior

- The agent must try available public fetch, browser-cookie/authenticated fetch,
  local export, or browser playback screenshot capture before accepting
  thumbnail-only evidence for a visual-style video note.

## Followups

- Add a deterministic fixture or mocked media-ingest harness if this eval is
  promoted into an automated skill test suite.
