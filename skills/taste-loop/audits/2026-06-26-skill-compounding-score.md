---
title: "Taste Loop Skill Compounding Score Audit"
owner: skill-maintenance
status: complete
created_at: 2026-06-26
change_type: skill-contract
refs:
  - docs/features/FEAT-0064-skill-compounding-score.md
  - skills/taste-loop/SKILL.md
  - skills/taste-loop/templates/heartbeat-prompt.md
---

# Taste Loop Skill Compounding Score Audit

## Claim

Taste Loop now consumes the official Skill Compounding Score instead of owning a
local ad hoc score formula.

## Before

- Taste Loop ranked high-compounding skills from registry, product lanes, and
  existing heat.
- The score breakdown lived inside `skills/taste-loop/SKILL.md` and the
  heartbeat prompt.
- There was no canonical distinction between skill priority score and eval
  score beyond local wording.

## After

- `docs/features/FEAT-0064-skill-compounding-score.md` owns the official algorithm,
  component meanings, and source owners.
- Taste Loop reads that spec and reports the score breakdown as a consumer.
- The score is explicitly not an eval score, review TAS, template-health score,
  or human preference label.

## Skill Structure QA

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` names the score spec, state reads, route options, gates, and output fields. |
| `reference_load_precision` | pass | The scoring spec is loaded during candidate collection and listed in the Reference Map. |
| `duplicated_instruction_count` | pass | The formula moved to the spec; Taste Loop keeps only consumer instructions. |
| `maintenance_locality` | pass | Future scoring changes belong in the spec; heartbeat behavior stays in Taste Loop. |
| `proof_surface_fit` | pass | Validation uses feature registry, skill registry, doc refs, graph generation, and prompt/eval reference points. |

## Validation

- `python3 docs/features/validate_features.py --write`
- `python3 skills/skill-maintenance/scripts/check_skills.py --write`
- `python3 bin/validators/sync_skill_registry.py --check`
- `python3 bin/validators/check_farplane_project_files.py`
- `python3 tickets/scripts/check_ticket_metadata.py`
- `python3 skills/skill-maintenance/scripts/generate_harness_graph.py`
- `python3 skills/skill-maintenance/scripts/generate_skill_graph.py`
- `python3 skills/skill-maintenance/scripts/generate_farplane_lifecycle_graph.py`
- `python3 bin/validators/check_doc_refs.py`
- `git diff --check`

## Review

Local review using `review` with `skill-contract`, `prompt-quality`,
`integration-readiness`, `evidence-quality`, and `spec-contract` rubrics found
no blocking issues. Native reviewer subagent was not spawned because the
available subagent tool contract requires explicit user-requested delegation.
