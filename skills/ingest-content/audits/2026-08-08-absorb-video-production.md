---
skill: ingest-content
date: 2026-08-08
change_type: structure
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: tickets/TASK-9020/ticket.md
after_ref: skills/ingest-content/SKILL.md
eval_required: no
eval_skip_reason: owner routing changed without a runnable generation path; registry, reference, JSON, and ticket checks cover the deterministic contract
---

# Skill Audit: Retire Video Production Router

## Change

- Before: `video-production` repeated ticket planning, narrative design, asset
  routing, platform specs, and provider routing while owning three useful
  details.
- After: `ingest-content` owns saved-capture style-profile compilation,
  `storyboard` owns scene-grid packets, and `ai-video-advisor` owns provider
  continuity preflight; the duplicate router is deleted.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Each retained rule sits in the owner that invokes it. |
| `duplicated_instruction_count` | pass | Generic planner methods, model, upstream maps, and router package are removed. |
| `maintenance_locality` | pass | Capture/profile, scene packet, and provider envelope each have one owner. |
| `composition_clarity` | pass | Content ticket → Storyboard → AI Video → Remotion has explicit handoffs. |
| `proof_surface_fit` | pass | Registry/reference/ticket validation and completion review pass. |

## Proof

- `python3 skills/skill-maintenance/scripts/check_skills.py --write` — 117
  skill rows, references and eval-query checks pass.
- `python3 docs/features/validate_features.py --write` — system records pass.
- `python3 -m unittest skills/skill-maintenance/scripts/test_sync_skill_plugins.py` — pass.
- `tickets/TASK-9020/artifacts/review/completion-review.md` — `TAS-A` pass.
