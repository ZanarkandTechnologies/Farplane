---
skill: hatch-pet
date: 2026-07-12
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: installed ~/.codex/skills/hatch-pet imported 2026-07-12
after_ref: skills/hatch-pet
reasoning_basis: first_principles
proof_artifacts:
  - skills/hatch-pet/scripts/test_prepare_pet_run.py
  - skills/hatch-pet/evals/evals.json
  - .farplane/evals/runs/20260712-112842-hatch-pet-friend-import-rerun2-20260712/summary.json
eval_required: yes
---

# Skill Audit

## Change

- Before: Person/profile imports were an implicit variant of brand or reference-image generation, with no durable source brief, privacy boundary, animation mapping contract, QA checklist, or eval.
- After: A first-class friend-import branch requires a supplied likeness image, bounds public research, stores source evidence, maps ideas into the fixed atlas, and adds deterministic tests plus QA/eval guardrails.
- Why: Make the chat workflow repeatable for many friends while preserving the proven Mini Kenji/Mini Chua generation and atlas pipeline.
- Tradeoff accepted: The existing long first-load skill remains over the preferred line budget; this pass moves new conditional detail to a reference instead of attempting a risky full compaction alongside behavior changes.

## First-Principles Reasoning

- Objective: Turn an image, optional public profile, notes, and animation ideas into a recognizable packaged Codex pet.
- Placement logic: `SKILL.md` owns routing and gates; `references/friend-import.md` owns conditional person-research detail; the preparer records evidence; QA and evals prevent regression.
- Expected behavior delta: Calls with a real-person image now select a bounded friend-import workflow and preserve its evidence in the run.
- Proof needed: CLI tests, JSON validation, skill validator, install/live-copy inspection, and independent review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Signature and Friend Import route are in `SKILL.md`. |
| `reference_load_precision` | pass | `SKILL.md` names exactly when to load `references/friend-import.md`. |
| `missing_context_rate` | pass | Likeness, privacy, atlas, and QA gates remain in first load. |
| `noisy_context_rate` | pass | Conditional research schema and examples live in the reference. |
| `duplicated_instruction_count` | pass | First load carries gates; reference carries execution detail. |
| `prompt_size_tokens` | fail | Imported skill remains above 400 lines; deferred to a dedicated compaction pass. |
| `task_success_rate` | pass | Two focused behavior evals passed with verdict A. This does not claim a full image-generation run. |
| `review_tas_rate` | pass | Final independent reviewer returned TAS-A with no blockers. |
| `maintenance_locality` | pass | Farplane `skills/hatch-pet/` is now the owner-local source. |
| `composition_clarity` | pass | Signature exposes inputs, outputs, state, gates, and failure modes. |

## First-Load Review

```text
first_load_review:
  line_count_before: 539
  line_count_after: 587
  kept_in_skill: person-import routing, hard gates, CLI handoff, and fixed-row rule
  moved_to_reference: intake precedence, research boundary, brief schema, animation examples
  deleted_as_duplicate_or_rationale: none
  extra_sections_kept_with_reason: existing generation, storage, style, transparency, worker, repair, rules, and acceptance contracts predate this focused behavior pass
  remaining_sections_over_budget: entire imported first-load skill
  proof_surface_fit: deterministic CLI test plus behavior eval and reviewer
  task_case_quality: one normal and one inaccessible-profile case
  anti_cheat_case_design: prompts describe user intent without naming workflow rules
  qa_preflight_loaded: yes
  qa_finish_independence: final independent reviewer returned TAS-A pass
  qa_gotcha_deduplication: pass
  project_specific_context_isolation: pass; Mini examples are optional caller-supplied anchors
  low_value_prose_scan: deferred to dedicated compaction pass
  verdict: pass_with_disclosed_prompt_size_failure
```

## Proof Artifacts

- Unit tests: `python3 -m unittest discover -s skills/hatch-pet/scripts -p 'test_*.py'` -> 2 passed.
- Skill system: `python3 skills/skill-maintenance/scripts/check_skills.py --write` -> pass.
- Eval query lint: `python3 skills/eval/scripts/check_eval_queries.py --root .` -> pass.
- Behavior eval: `.farplane/evals/runs/20260712-112842-hatch-pet-friend-import-rerun2-20260712/summary.json` -> 2/2 pass, verdict A.
- Initial reviewer: TAS-B revise; run-summary evidence and eval-run blockers repaired.
- Final reviewer: TAS-A pass; no hard-gate failures or blocking findings.

## Followups

- Compact the inherited 500+ line first-load contract into precise references without changing generation behavior.
