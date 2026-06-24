---
skill: skill-creator
date: 2026-06-24
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/skill-creator/SKILL.md
after_ref: skills/skill-creator/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/skill-creator/references/book-to-skill.md
  - skills/skill-creator/eval_task.json
eval_required: yes
---

# Skill Audit

## Change

- Before: `skill-creator` required source synthesis when external examples
  mattered, but had no dedicated workflow for mining online book-summary
  videos, articles, blogs, app summaries, or author interviews for actionable
  skill workflows.
- After: `skill-creator` routes book-summary and longform grounding to
  `references/book-to-skill.md`, adds a no-substitute-summary gotcha, and has a
  focused eval case for transforming public summary takeaways into skill
  deltas. The reference now makes source discovery and `summarize` extraction
  explicit before skill synthesis.
- Why: Book grounding is high leverage but risky if it becomes generic book
  notes, derivative summaries, or untraceable inspiration.
- Tradeoff accepted: Keep book-specific detail out of first load and require an
  explicit reference branch, while adding enough first-load routing to prevent
  agents from drafting from memory.

## First-Principles Reasoning

- Objective: Turn online key-takeaway sources into reusable skill behavior with
  evidence, placement, and proof.
- Placement logic: The default `skill-creator` path only needs a branch pointer
  and gotcha; the extraction ladder, note schema, search pattern, and examples
  belong in a reference loaded only for books or longform sources.
- Expected behavior delta: When asked to ground a skill from book-summary
  sources, the agent searches for workflow-bearing summaries, scores candidate
  resources, runs `summarize` extraction for YouTube/articles/local notes when
  appropriate, labels source type and convergence, performs task analysis,
  chooses a skill surface, and adds proof.
- Proof needed: Registry validation plus a future eval run of
  `skill_creator_book_grounding_branch_01`.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` now routes book-summary and longform grounding before drafting. |
| `reference_load_precision` | pass | The reference map and todo item state when to load `references/book-to-skill.md`. |
| `missing_context_rate` | pass | Copyright-safe transformation gate and reference route are in first load. |
| `noisy_context_rate` | pass | Detailed source ladder and schemas are in the reference, not first load. |
| `duplicated_instruction_count` | pass | No existing skill-creator reference owned this book-specific branch. |
| `prompt_size_tokens` | pass | First-load edit is small; detailed workflow is branch-specific. |
| `task_success_rate` | unknown | Needs eval runner evidence after this change. |
| `review_tas_rate` | unknown | Self-check only so far; reviewer can be routed if this becomes a broader skill-system standard. |
| `maintenance_locality` | pass | Future edits belong in `skill-creator/references/book-to-skill.md` unless the first-load route changes. |
| `composition_clarity` | pass | Reference signature names inputs, outputs, state, summarize extraction, gates, routes, and failure modes. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/skill-creator/eval_task.json`
- Structure evals, when needed: not run yet
- Reviewer receipt: none
- Validator: `python3 scripts/check_skills.py --write` from
  `skills/skill-maintenance` passed on 2026-06-24.
- Eval required: yes; added case, runner execution pending
- Evidence gaps: future real invocation should produce a
  `book_summary_to_skill_packet`

## Before Behavior

- A book-summary-grounded skill request could be handled as generic source
  synthesis, ordinary skill creation, or accidental book summarization.

## After Behavior

- A book-summary-grounded skill request has a named reference branch, summary
  source set, resource scoring, `summarize` extraction commands, takeaway note
  shape, workflow-candidate shape, placement rules, and behavior proof
  expectations.

## Followups

- Run the skill-local eval once the eval runner is used for this batch.
- Consider promoting repeated book-source ingestion patterns to `harness-scout`
  only after several real book-to-skill runs show the reference is too narrow.
