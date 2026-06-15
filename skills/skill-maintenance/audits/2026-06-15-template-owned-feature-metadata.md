---
skill: skill-maintenance
date: 2026-06-15
change_type: template
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/skill-creator/references/SKILL_TEMPLATE.md
after_ref: skills/skill-creator/references/SKILL_TEMPLATE.md
reasoning_basis: advise
proof_artifacts:
  - docs/skills/registry.jsonl
  - skills/skill-maintenance/graph/skill-template-intelligence.json
  - skills/skill-maintenance/graph/skill-graph.json
eval_required: no
---

# Skill Audit

## Change

- Before: Skill frontmatter carried optional `feature_refs`, which duplicated
  template-level structural features and made adoption state hard to trust.
- After: Skill template `0.3.0` owns structural `feature_refs`; individual
  skills expose only local `eval`, `qa_checklist`, and `skill_ui` surface
  metadata.
- Why: Template features are inherited from the template version, while eval,
  checklist, and UI surfaces vary per skill and need direct queryability.
- Tradeoff accepted: Existing skills were not blindly bumped to
  `skill_template_version: "0.3.0"` because template-version truth requires
  structure verification; rollout intelligence now reports them as stale or
  missing until a separate onboarding pass.

## First-Principles Reasoning

- Objective: Make feature adoption inferable from template versions while
  keeping skill-local operational surfaces easy to query.
- Placement logic: Structural feature IDs belong in the versioned skill
  template; skill package frontmatter should carry only local surfaces that
  cannot be derived from the template.
- Expected behavior delta: New skills generated from the template no longer
  receive per-skill `feature_refs`; registry sync rejects skill-level
  `feature_refs`; generated registry rows include eval, QA checklist, and UI
  metadata.
- Proof needed: Registry sync, template intelligence regeneration, graph
  regeneration, focused unit tests, migration idempotency, and whitespace check.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Template metadata is in the template artifact; skill docs name the new frontmatter contract. |
| `reference_load_precision` | pass | Conditional detail remains in docs and generated intelligence; skill frontmatter stays compact. |
| `missing_context_rate` | pass | `docs/skills/AGENTS.md`, `README.md`, and `system.md` all name the new ownership split. |
| `noisy_context_rate` | pass | Per-skill `feature_refs` were removed instead of expanded. |
| `duplicated_instruction_count` | pass | Structural feature IDs live once on the template metadata layer. |
| `prompt_size_tokens` | pass | New per-skill metadata is one-line surface paths only when a surface exists. |
| `task_success_rate` | unknown | No live agent-task eval was run for downstream behavior. |
| `review_tas_rate` | unknown | Native reviewer subagent was not invoked because this tool session only allows subagents when explicitly requested. |
| `maintenance_locality` | pass | Changes are in skill template, skill registry generator, skill-maintenance scripts, and skill-system docs. |
| `composition_clarity` | pass | `skill_features(skill) = template_features(version) + local_surfaces(skill)` is now represented by files. |

## Proof Artifacts

- Skill-local evals, when needed: not changed.
- Structure evals, when needed: `skills/skill-maintenance/scripts/test_generate_template_intelligence.py`.
- Reviewer receipt: not run; see `review_tas_rate`.
- Validator:
  - `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  - `python3 skills/skill-maintenance/scripts/generate_skill_graph.py`
  - `python3 bin/validators/test_sync_skill_registry.py`
  - `cd skills/skill-maintenance/scripts && python3 test_generate_template_intelligence.py`
  - `python3 -m py_compile skills/skill-creator/scripts/init_skill.py skills/skill-creator/scripts/quick_validate.py skills/skill-maintenance/scripts/migrate_skill_surfaces.py skills/skill-maintenance/scripts/generate_template_intelligence.py skills/skill-maintenance/scripts/generate_skill_graph.py bin/validators/sync_skill_registry.py`
  - `git diff --check`
  - `python3 skills/skill-maintenance/scripts/migrate_skill_surfaces.py`
- Eval required: no; this is a metadata/schema rollout with deterministic
  validators.
- Evidence gaps: No downstream Farplane UI filter was added in this slice.

## Before Behavior

- New skills inherited a `feature_refs: FEAT-XXXX` placeholder.
- The generated skill registry allowed per-skill feature references.
- Skill UI, eval, and QA checklist state were discoverable only by convention
  or file scanning.

## After Behavior

- New skills inherit `skill_template_version: "0.3.0"` from a two-layer
  template file whose top metadata declares template-owned features.
- The generated registry rejects skill-level `feature_refs`.
- Skill rows expose local `eval`, `qa_checklist`, and `skill_ui` fields when
  present.
- Template intelligence exposes template metadata and rollout state separately
  from skill-local surfaces.

## Followups

- Add graph UI filters/badges for `eval`, `qa_checklist`, and `skill_ui`.
- Decide whether to onboard selected high-value skills to
  `skill_template_version: "0.3.0"` after structure proof.
