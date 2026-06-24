---
skill: skill-creator
date: 2026-06-24
change_type: maintenance
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/skill-creator/SKILL.md
after_ref: skills/skill-creator/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/skill-creator/SKILL.md
  - skills/skill-creator/scripts/init_skill.py
  - skills/skill-creator/scripts/quick_validate.py
eval_required: no
---

# Skill Audit

## Change

- Before: `skill-creator` declared stale `skill-template: "0.2.0"`, carried a
  malformed inline template example, and shipped helper scripts that rejected
  modern `template_uses` metadata or scaffolded placeholder support files by
  default.
- After: `skill-creator` declares `skill-template: "0.3.2"`, points to
  docs-owned templates instead of embedding a partial template, accepts
  `template_uses`, and scaffolds only `SKILL.md` unless optional support-file
  flags are passed.
- Why: The skill creator should model the current skill standard rather than
  teaching one standard while validating another.
- Tradeoff accepted: Placeholder support files are now opt-in, so callers must
  request scaffolding when they actually need references, assets, or helper
  scripts.

## First-Principles Reasoning

- Objective: Make the authoring skill internally consistent with the docs-owned
  template standard and prevent it from generating dead scaffolding.
- Placement logic: First-load `SKILL.md` should name the standard and path;
  deterministic script behavior belongs in `scripts/*`.
- Expected behavior delta: New skills scaffold from `docs/skills/templates` and
  do not get empty-looking helper/reference files unless requested.
- Proof needed: Script compile, quick validator, scaffold smoke, and full
  skill-maintenance validation.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` links to docs-owned skill and method-reference templates. |
| `reference_load_precision` | pass | Book-to-skill remains explicitly branch-loaded. |
| `missing_context_rate` | pass | Full starter template path is named in `Templates` and `Reference Map`. |
| `noisy_context_rate` | pass | Malformed inline template body was removed from first load. |
| `duplicated_instruction_count` | pass | Template body lives in docs, not copied into `SKILL.md`. |
| `prompt_size_tokens` | pass | `SKILL.md` is shorter after removing the inline template block. |
| `task_success_rate` | unknown | No LLM behavior eval run; deterministic script smoke passed. |
| `review_tas_rate` | unknown | Self-check only. |
| `maintenance_locality` | pass | Script behavior is in scripts; template standard is in docs. |
| `composition_clarity` | pass | Current template version and optional scaffold flags are explicit. |

## Proof Artifacts

- Skill-local evals, when needed: not required
- Structure evals, when needed:
  - `python3 skills/skill-creator/scripts/quick_validate.py skills/skill-creator`
  - `python3 skills/skill-creator/scripts/init_skill.py sample-skill --path "$tmp"`
  - `python3 scripts/check_skills.py --write` from `skills/skill-maintenance`
- Reviewer receipt: none
- Validator: passed on 2026-06-24
- Eval required: no
- Evidence gaps: no independent reviewer lane

## Before Behavior

- The skill claimed an old template version while telling agents to use newer
  docs-owned template paths.
- Its quick validator failed against the skill's own frontmatter.
- Its scaffold command created helper/reference/assets files by default.

## After Behavior

- The skill claims the current template version.
- The quick validator accepts `template_uses`.
- The scaffold command creates only `SKILL.md` unless optional support flags
  are requested.

## Followups

- Consider replacing emoji CLI output if these scripts become CI-facing rather
  than human-facing helpers.
