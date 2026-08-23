---
skill: consolidate
date: 2026-08-20
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
review_tas: TAS-A
integrated_status: pass
before_ref: skills/knowledge-tidier/SKILL.md
after_ref: skills/consolidate/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/consolidate/evals/evals.json
  - .farplane/evals/runs/20260820T131727Z-task-0442-knowledge-merge-final/summary.json
  - .farplane/evals/runs/20260820T141447Z-task-0442-knowledge-merge-stale-labels/summary.json
eval_required: yes
---

# Consolidate Knowledge-Pruning Merge Audit

## Change

- Before: `consolidate` delegated knowledge pruning back to a Tier 3 wrapper;
  the two packages formed a circular route and loaded 425 skill lines together.
- After: `consolidate(structure = memory | docs_tree | file)` owns the archive
  gate, knowledge scoring, dispositions, owner routing, Tidy Report, and loss
  check in a 162-line first-load contract. Its eval suite grows from 3 to 5
  cases, and the duplicate package is removed without an alias.
- Why: the Tier 1 primitive already owned inventory, scoring, routing,
  rebuilding, and loss checking; the wrapper added constraints, not a separate
  artifact.
- Tradeoff accepted: the generic primitive carries a compact knowledge branch
  on first load in exchange for one discoverable owner and no nested skill call.

## First-Principles Reasoning

- Objective: preserve knowledge-pruning behavior while removing a duplicate
  public surface.
- Placement logic: reuse the existing `consolidate` owner; do not add a method,
  subskill, compatibility alias, or new runtime.
- Expected behavior delta: callers select a structure and receive the same
  ranked knowledge decisions and report directly from `consolidate`.
- Proof needed: transferred eval cases, exact contract checks, skill-system
  validation, reference scan, and independent review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Archive gate, scoring, routing, report, and loss check remain in `SKILL.md`. |
| `reference_load_precision` | pass | No branch reference is required for normal knowledge pruning. |
| `missing_context_rate` | pass | Both prior eval contracts are represented in the merged first load. |
| `noisy_context_rate` | pass | Skill shrank from 237 to 162 lines while adding the branch. |
| `duplicated_instruction_count` | pass | The wrapper and circular route are deleted. |
| `prompt_size_tokens` | pass | One 162-line owner replaces 425 combined lines. |
| `task_success_rate` | pass | Both transferred cases pass candidate 1.0 against failing retired baselines. |
| `review_tas_rate` | pass | Independent lane review and integrated validation both pass. |
| `maintenance_locality` | pass | One package owns the contract and all five evals. |
| `composition_clarity` | pass | Signature names reads, work, writes, and returned evidence. |

## Proof Artifacts

- Skill-local evals: both transferred cases pass at 1.0 in
  `.farplane/evals/runs/20260820T131727Z-task-0442-knowledge-merge-final/summary.json`
  and
  `.farplane/evals/runs/20260820T141447Z-task-0442-knowledge-merge-stale-labels/summary.json`;
  source hashes are unchanged.
- Structure evals: 162-line cap, JSON/TOML parse, query lint, exact prompt and
  assertion transfer, package absence, and diff whitespace checks pass.
- Reviewer receipt: TAS-A with no blocker.
- Validator: focused checks and the coordinated
  `check_skills.py --write` integration gate pass with 117 registry rows.
- Evidence gaps: none.

## Before Behavior

Knowledge callers loaded a wrapper which immediately called `consolidate`, then
returned a separate but overlapping report contract.

## After Behavior

Knowledge callers invoke `consolidate` directly with a supported knowledge
structure; the result includes the knowledge dispositions and Tidy Report plus
the primitive's standard loss check.

## Followups

- None. TASK-0442 regenerated the canonical registry and passed the integrated
  skill-system gate on 2026-08-20.
