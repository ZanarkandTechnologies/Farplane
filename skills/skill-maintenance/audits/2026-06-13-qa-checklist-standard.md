---
skill: skill-maintenance
date: 2026-06-13
change_type: structure
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/skill-maintenance/references/skill-structure-checklist.md
after_ref: skills/skill-maintenance/qa_checklist.md
reasoning_basis: first_principles
proof_artifacts:
  - python3 skills/skill-maintenance/scripts/check_skills.py --write
  - python3 skills/skill-maintenance/scripts/generate_skill_graph.py
  - git diff --check
eval_required: no
---

# Skill Audit

## Change

- Before: The skill structure checklist lived under `references/` even though
  skill-maintenance and skill-creator used it as an executable QA gate.
- After: The checklist is a first-class skill-local `qa_checklist.md`, with
  `FEAT-0057`, `MEM-0150`, and skill-system docs describing the general
  standard for future skills.
- Why: Runtime guardrails need a discoverable owner that is distinct from both
  first-load todos and optional reference prose.
- Tradeoff accepted: The standard stays Markdown-only for now; no qacheck
  runner, renderer, or subagent fanout script was introduced.

## First-Principles Reasoning

- Objective: Make skill QA checklists easy to discover, apply, and later render
  without forcing every skill to adopt one immediately.
- Placement logic: `SKILL.md` owns first-load execution, `eval_task.json` owns
  behavior discovery/proof cases, `qa_checklist.md` owns settled real-time
  guardrails, and `references/` owns branch detail.
- Expected behavior delta: Skill edits that change eval reference points or
  runtime guardrails now check whether a root-level `qa_checklist.md` should be
  read, created, or updated.
- Proof needed: Link validation, registry regeneration, stale-path scan, and
  the structure checklist applied to the changed skill files.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `skill-maintenance/SKILL.md` still names when to read the checklist and how to sync eval reference points. |
| `reference_load_precision` | pass | `skill-maintenance/SKILL.md` and `skill-creator/SKILL.md` link `qa_checklist.md` with explicit read conditions. |
| `missing_context_rate` | pass | Every-invocation routing stays in `SKILL.md`; the moved file only owns finish-time QA checks. |
| `noisy_context_rate` | pass | Checklist details remain outside first-load todos until structure review is needed. |
| `duplicated_instruction_count` | pass | Docs state the general standard; `qa_checklist.md` owns the runnable checklist. |
| `prompt_size_tokens` | pass | No large checklist body was added to either `SKILL.md`. |
| `task_success_rate` | unknown | No behavioral eval run was needed for this artifact placement change. |
| `review_tas_rate` | unknown | No independent reviewer receipt was requested for this bounded standard move. |
| `maintenance_locality` | pass | Future skill-local QA edits have one obvious root artifact: `qa_checklist.md`. |
| `composition_clarity` | pass | `docs/skills/system.md` defines `skill_qa_checklist(skill_package, changed_files, claim, budget?)`. |

## Proof Artifacts

- Skill-local evals, when needed: Not required; no executable skill behavior was
  changed.
- Structure QA, when needed: `skills/skill-maintenance/qa_checklist.md` applied
  through this audit rubric.
- Reviewer receipt: Not requested; self-check is sufficient for this bounded
  artifact relocation plus docs standard.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  passed.
- Eval required: no.
- Evidence gaps: No renderer or scripted qacheck runner exists yet.

## Before Behavior

- Agents could read the structure checklist, but the file looked like ordinary
  reference prose and future tooling had no special skill-local artifact to
  discover.

## After Behavior

- Agents can look for `skills/<skill-name>/qa_checklist.md` as the optional
  skill-local runtime QA surface, while `skill-maintenance` decides whether
  eval reference points should promote into that file.

## Followups

- Add a renderer or runner only after multiple skills have adopted
  `qa_checklist.md` and the file shape has stabilized.
