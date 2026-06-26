---
skill: cross-skill
date: 2026-06-26
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: templates/global/AGENTS.md; skills/reference-grounding/SKILL.md; skills/impl-plan/SKILL.md; skills/goal-advisor/SKILL.md
after_ref: templates/global/AGENTS.md; skills/reference-grounding/SKILL.md; skills/impl-plan/SKILL.md; skills/goal-advisor/SKILL.md; skills/eval/examples/farplane-global-harness/tasks.json
reasoning_basis: first_principles
proof_artifacts:
  - node JSON parse for skills/eval/examples/farplane-global-harness/tasks.json
  - python3 skills/eval/scripts/check_eval_queries.py --root .
  - python3 skills/skill-maintenance/scripts/check_skills.py --write
  - python3 skills/eval/scripts/run_evals.py status --harness codex
  - python3 skills/eval/scripts/run_evals.py run --harness codex --tasks skills/eval/examples/farplane-global-harness/tasks.json --task-id global_coding_feature_grounding_01 --label coding-grounding-gate-real-repo-2026-06-26 --max-parallel-tasks 1
eval_required: yes
---

# Coding Grounding Gate Audit

## Change

- Before: Implementation-feature grounding existed as guidance, but direct
  coding, ticket planning, and Goal prompts could still finalize from local
  intuition and tests alone.
- After: Implementation feature work now treats code documentation or
  maintained implementation evidence as a completion gate across global policy,
  `reference-grounding`, `impl-plan`, `goal-advisor`, and one global harness eval
  row.
- Why: Small niche coding requests are exactly where stale API memory and
  ungrounded implementation patterns can slip through.
- Tradeoff accepted: Adds a little ceremony to feature completion while
  preserving a local-only escape hatch for tiny same-scope fixes.

## First-Principles Reasoning

- Objective: Make agents check current code documentation, Ref MCP, official
  docs, GitHub code search, maintained examples, or web evidence before
  finalizing implementation features.
- Placement logic: Global policy catches small non-ticket work; `impl-plan` and
  `goal-advisor` turn the behavior into a proof gate for ticketed and Goal-backed
  work; `reference-grounding` owns the source-choice procedure; the global
  harness eval preserves the behavior.
- Expected behavior delta: A feature-completion answer should include
  `Grounding:` naming the source class checked, or explicitly state the
  local-only reason.
- Proof needed: Static validation plus a focused eval row and a live Codex eval
  run for the new coding-grounding behavior.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Global template and first-load skill files include the finish gate. |
| `reference_load_precision` | pass | Detailed source selection remains in `reference-grounding`; ticket and Goal skills only name the gate. |
| `missing_context_rate` | unknown | Requires live task runs across coding requests. |
| `noisy_context_rate` | unknown | Requires live task runs to see whether agents over-search tiny local-only fixes. |
| `duplicated_instruction_count` | pass | Repetition is intentionally limited to owner gates: global, grounding, plan, Goal, eval. |
| `prompt_size_tokens` | unknown | No token diff measured. |
| `task_success_rate` | pass | `global_coding_feature_grounding_01` passed with verdict `A` in run `20260626-022648-coding-grounding-gate-real-repo-2026-06-26`. |
| `review_tas_rate` | unknown | No reviewer receipt requested. |
| `maintenance_locality` | pass | Changes stay in global template, owning skills, QA checklists, and eval suite. |
| `composition_clarity` | pass | `reference-grounding` owns source choice; `impl-plan` and `goal-advisor` own proof gates. |

## Proof Artifacts

- Skill-local evals, when needed: not used; behavior is global harness behavior.
- Structure evals, when needed: `skills/eval/examples/farplane-global-harness/tasks.json` now includes `global_coding_feature_grounding_01`.
- Reviewer receipt: not requested.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write` passed.
- Eval required: yes; live Codex run passed.
- Evidence gaps: Only one focused case was run; broader coding-feature coverage
  can be added if this behavior regresses in other stacks.

## Before Behavior

- Agents could treat external grounding as good practice but not a completion
  requirement.
- Ticket and Goal proof contracts did not require `Grounding:` evidence for
  feature work.

## After Behavior

- Direct implementation feature work has a global completion gate.
- Material plans require `Grounding evidence:` in `Done / Proof`.
- Coding Goal prompts require a final `Grounding:` source-class rule.
- The global harness eval suite checks a small non-ticket coding feature case.

## Followups

- Add a second stack-specific coding case only if the grounding gate regresses
  outside Python CLI work.
