---
skill: feed-scout
date: 2026-08-20
change_type: refinement
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/feed-scout/SKILL.md@270-lines
after_ref: skills/feed-scout/SKILL.md@126-lines
reasoning_basis: first-principles low-value prose scan
proof_artifacts:
  - tickets/TASK-0441/artifacts/review/completion-review.md
  - skills/feed-scout/qa_checklist.md
  - skills/feed-scout/references/workflow.md
  - skills/feed-scout/scripts/test_validate_scout_brief.py
eval_required: no
---

# Feed Scout First-Load Compaction

## Change

Repeated runbook prose and field inventories moved behind the existing workflow
and data-model references. The first load keeps the trigger, signature, normal
eight-step path, hard authority/recovery gates, Scout Brief contract, finish
check, and output boundary.

## Low-Value Prose Decisions

- `move`: acquisition maps, redundancy examples, source nomination mechanics,
  status/review branches, and field inventories already owned by references.
- `rewrite`: repeated workflow prose became executable todo/gate statements.
- `delete`: duplicated output bullets and rationale that changed no action.
- `keep`: safety, evidence, candidate completeness, recovery cap, validation,
  and no-execution requirements.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| First-load sufficiency | pass | Default route and hard gates remain in `SKILL.md`. |
| Reference precision | pass | Runbook and schemas have explicit load conditions. |
| Behavior preservation | pass | Focused tests passed; independent review returned TAS-A. |
| Surface budget | pass | 126 physical lines, below the 200-line hard cap. |
| Maintenance locality | pass | Changes stay in the Feed Scout package. |

No eval rerun is required for the prose-only compaction; the existing TASK-0441
behavior proof plus deterministic Scout Brief tests own regression evidence.
