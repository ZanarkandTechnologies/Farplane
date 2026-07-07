---
skill: ingest-content
date: 2026-07-07
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/ingest-content/SKILL.md before local character-element update
after_ref: skills/ingest-content/SKILL.md plus references, qa_checklist.md, eval_task.json
reasoning_basis: first_principles
proof_artifacts:
  - skills/ingest-content/eval_task.json
  - skills/ingest-content/qa_checklist.md
  - python3 scripts/check_skills.py --write
eval_required: yes
---

# Skill Audit

## Change

- Before: Ingest Content creative elements covered visual, audio, hook, storyboard, editing, copy, format, and constraint, so distinctive personas could be buried in visual or storyboard prose.
- After: `character` is a first-class creative element kind for distinctive personas, archetypes, guides, hosts, mascots, and recurring character systems.
- Why: Kenji's Railway/Gilfoyle advert note makes the character/persona the taste source, so Resource Bank ingestion needs to preserve it as a reusable element without adding a separate production pattern.
- Tradeoff accepted: The element enum grows by one kind, but the Resource Bank model remains source + analysis + creative elements.

## First-Principles Reasoning

- Objective: Make future ingests extract reusable character/persona value when the note or source makes that the reason the reference matters.
- Placement logic: The enum and pinning rule belong in first-load `SKILL.md`; detailed element semantics belong in references; recurring failure prevention belongs in QA and eval.
- Expected behavior delta: Agents extract `kind: character`, pin it only when grounded in the ingestion note, and pair protected or likeness-adjacent characters with rights-safe `constraint` elements.
- Proof needed: JSON eval validity, skill registry/check validation, and focused search showing no weights or production-pattern object was introduced.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` names `character`, note-backed pinning, and rights-safe remix constraints in the normal element extraction path. |
| `reference_load_precision` | pass | Existing Reference Map points to the Resource Bank contract, reuse taxonomy, and phase router where the detailed character semantics now live. |
| `missing_context_rate` | pass | Required behavior is not only in references; the normal todo carries the extraction, pinning, and constraint gates. |
| `noisy_context_rate` | pass | First-load addition is limited to enum and executable gates; examples stay in references/eval. |
| `duplicated_instruction_count` | pass | `SKILL.md` owns must-do behavior; references elaborate schema/taxonomy/router details. |
| `prompt_size_tokens` | pass | `SKILL.md` line count remains close to the existing size and below the hard failure zone. |
| `task_success_rate` | unknown | No live Resource Bank ingestion was run for a real source in this skill-maintenance update. |
| `review_tas_rate` | unknown | Independent reviewer was not spawned because this turn did not explicitly request subagent delegation; self-check recorded for the scoped skill package update. |
| `maintenance_locality` | pass | Future enum/schema edits have obvious owners: `SKILL.md`, Resource Bank contract, taxonomy, router, QA, and eval. |
| `composition_clarity` | pass | Inputs/outputs remain source, analysis, creative elements, retrieval handle; no production-pattern object or weights were added. |

## Proof Artifacts

- Skill-local evals, when needed: added `ingest_content_character_persona_01`.
- Structure evals, when needed: `skills/skill-maintenance/scripts/check_skills.py --write`.
- Reviewer receipt: not run; self-check recorded because this is a scoped skill package update.
- Validator: pass, `python3 scripts/check_skills.py --write` from `skills/skill-maintenance`.
- Eval required: yes, as regression coverage in `eval_task.json`.
- Evidence gaps: No live Resource Bank write was required or attempted.

## Before Behavior

- A Gilfoyle-like advert could be saved as hook/storyboard/visual/copy without preserving the deadpan technical guide as a reusable first-class element.

## After Behavior

- The same advert should produce a pinned `character` element when Kenji's note explicitly likes the persona, plus a `constraint` element that keeps future remixes rights-safe.

## Followups

- If Farplane-UI validators are not already updated for `character`, land the matching Resource Bank schema change in the UI repo before live writes depend on it.
