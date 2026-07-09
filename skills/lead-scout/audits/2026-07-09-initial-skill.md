---
skill: lead-scout
date: 2026-07-09
change_type: structure
owner: skill-creator
status: pass
review_route: self_check
before_ref: none
after_ref: skills/lead-scout/SKILL.md
reasoning_basis: advise
proof_artifacts:
  - skills/lead-scout/eval_task.json
eval_required: yes
---

# Skill Audit

## Change

- Before: prospect discovery had no dedicated skill owner; `feed-scout`,
  `customer-research`, and `solution-shaping` were adjacent but not the right
  owner for candidate ranking.
- After: `lead-scout` owns bounded prospect discovery, qualification, and
  handoff to `customer-research` and `solution-shaping`.
- Why: lead discovery is similar to feed scouting but the artifact and safety
  contract are different: people/prospect packets instead of content feed rows.
- Tradeoff accepted: one extra Tier 3 skill, with qualification folded in to
  avoid a premature `prospect-qualification` split.

## First-Principles Reasoning

- Objective: produce outreach-ready candidate packets from public/supplied
  sources without turning the workflow into a scraper or private dossier.
- Placement logic: sibling to `feed-scout`; upstream of `customer-research`;
  not a CRM system.
- Expected behavior delta: agents should rank prospects before researching
  them and label public facts, inferences, and unknowns.
- Proof needed: registry validation plus eval smoke rows for routing and
  unbounded-scrape refusal.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Signature, todo list, gates, routes, and output are in `SKILL.md`. |
| `reference_load_precision` | pass | References are direct handoff owners, not required hidden workflow. |
| `missing_context_rate` | pass | Source boundary, filter, ranking, handoff, and CRM limits are first-load. |
| `noisy_context_rate` | pass | Detailed platform recipes are not included. |
| `duplicated_instruction_count` | pass | Feed-scout relationship is stated once as boundary. |
| `prompt_size_tokens` | pass | First-load file is below the structure review threshold. |
| `task_success_rate` | unknown | Requires future eval runner evidence. |
| `review_tas_rate` | unknown | No independent reviewer lane run in this pass. |
| `maintenance_locality` | pass | Future edits belong in `skills/lead-scout/`. |
| `composition_clarity` | pass | Routes and outputs are explicit. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/lead-scout/eval_task.json`
- Structure evals, when needed:
  `python3 skills/skill-maintenance/scripts/check_skills.py --write` passed.
- Reviewer receipt: self-check; no reviewer lane used because this is a small
  initial package with no runtime scripts or external mutation.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  passed.
- Eval required: yes, but runner execution is a follow-up when eval suite is
  selected.
- Evidence gaps: no live prospecting run performed.

## Before Behavior

- Agents could overuse `feed-scout` or jump straight to `customer-research`.

## After Behavior

- Agents should first produce a bounded, deduped, ranked candidate packet, then
  route only qualified candidates to downstream research.

## Followups

- Add platform-specific examples after the first real campaign run.
