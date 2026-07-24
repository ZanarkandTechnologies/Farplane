---
skill: feed-scout
date: 2026-07-15
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/feed-scout/SKILL.md@HEAD-250-lines-plus-concurrent-world-memory-rename
after_ref: skills/feed-scout/SKILL.md@256-lines
reasoning_basis: reviewer
proof_artifacts:
  - tickets/TASK-0380/artifacts/agent-qa/plan.md
  - skills/feed-scout/scripts/test_validate_world_memory.py
eval_required: yes
---

# Causal World Memory Audit

## Change

- Before: World Memory sources could be relevant-looking without stating what
  attention they showed, what pattern was compelling, what gap remained, or
  how the planner should use the fact.
- After: trend and notable facts carry evidence level, attention signal,
  compelling pattern, gap, and causal use alongside time/confidence/sources.
- Why: citations must change the idea, not decorate it.
- Tradeoff accepted: richer compact facts and stricter validation.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Skill todo/output contract names typed causal facts. |
| `reference_load_precision` | pass | Template and validator remain owner-local. |
| `missing_context_rate` | pass | Evidence levels and causal-use requirement are explicit. |
| `noisy_context_rate` | pass | Six first-load lines added; schema detail remains in the template. |
| `duplicated_instruction_count` | pass | Template defines shape; validator/tests enforce it. |
| `prompt_size_tokens` | pass | Aggregate line count is 250 -> 256. |
| `task_success_rate` | pass | Current and planner fixture World Memory files validate. |
| `review_tas_rate` | unknown | Completion review pending. |
| `maintenance_locality` | pass | All changes preserve Feed Scout as evidence owner. |
| `composition_clarity` | pass | Downstream planner use is explicit without giving Feed Scout admission authority. |

## Proof Artifacts

- Validator/tests: `validate_world_memory.py` and
  `test_validate_world_memory.py`.
- Evidence gap: live model judgment remains blocked; deterministic source
  shape is proved.

## Before Behavior

- A title, date, confidence, and source could look grounded while having no
  inspectable effect on candidate design.

## After Behavior

- Each usable fact distinguishes evidence status and names its causal use; a
  source gap cannot masquerade as observed resonance.

## Followups

- None inside Feed Scout; the five-round planner experiment owns human signal.
