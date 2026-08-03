---
skill: editing-advisor
date: 2026-08-02
change_type: structure
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: no dedicated editing advisor
after_ref: skills/editing-advisor/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/editing-advisor/evals/evals.json
  - skills/editing-advisor/qa_checklist.md
  - .farplane/evals/runs/20260802-155201-editing-advisor-timing-rerun-2026-08-02/summary.json
eval_required: yes
---

# Skill Audit

## Change

- Before: Editing techniques could exist in Resource Bank or Brand Kits, but no
  broad advisor owned selection, compatibility, timed recipe compilation, and
  renderer handoff.
- After: `editing-advisor` retrieves complete editing elements, applies six
  focused methods, decides `use | adapt | reject | block`, and produces an
  ordered edit recipe without duplicating the corpus.
- Why: Recreating accumulated Vox-style techniques requires reusable editorial
  judgment between creative planning and rendering.
- Tradeoff accepted: The advisor adds one explicit production handoff, in
  exchange for preventing title-only technique use and renderer improvisation.

## First-Principles Reasoning

- Objective: Make editing knowledge reusable and executable across projects.
- Placement logic: Resource Bank owns reusable records; Brand Kit owns approved
  snapshots; the advisor owns choice/composition; renderers own pixels.
- Expected behavior delta: Callers receive compatible timed recipes and proof
  contracts instead of loose editing references.
- Proof needed: Structure validation, focused behavior evals, query-spoiler
  check, and independent reviewer receipt.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | latest results are A across all five eval cases |
| `reference_load_precision` | pass | retrieval reference loads only for discovery/source questions |
| `missing_context_rate` | pass | provisional recipe contract preserved useful work under missing inputs |
| `noisy_context_rate` | pass | TAS-A independent scoped review |
| `duplicated_instruction_count` | pass | techniques remain in Resource Bank |
| `prompt_size_tokens` | pass | 9 todos, 5 QA items, and 5 evals within enrolled surface budget |
| `task_success_rate` | pass | latest verdict for each of five cases is A |
| `review_tas_rate` | pass | independent reviewer TAS-A |
| `maintenance_locality` | pass | package-local runtime, QA, eval, and retrieval reference |
| `composition_clarity` | pass | independent reviewer found no scoped blocker |

## Proof Artifacts

- Skill-local evals, when needed: `skills/editing-advisor/evals/evals.json`
- Structure evals, when needed: canonical skill checker
- Reviewer receipt: independent scoped rereview, TAS-A, no hard-gate failures
- Validator: registry, JSON, query lint, todo-tier, and Tier 0 checks pass;
  repo checker retains pre-existing Content Impl Plan 19/19 surface debt
- Eval required: yes
- Evidence gaps: None for this scoped change.

Initial behavior run `20260802-153145-editing-advisor-2026-08-02` returned
`B/C` on all five advisor cases. Agents honored blockers but over-blocked on
missing timing, recipes, or accepted files. The first-load contract now requires
a relative, dependency-aware provisional recipe plus exact retrieval and proof
ownership before isolating those blockers. A rerun is required.

Rerun `20260802-154117-editing-advisor-rerun-2026-08-02` improved to two `A`,
two `B`, and one `C`. The remaining misses were unnamed per-step renderer
ownership, policy/technique table blur, unsupported “conceptual” retrieval
claims, and unspecified expected file paths. Those contracts are now explicit;
a focused rerun of the three affected cases is required.

Focused rerun `20260802-154655-editing-advisor-focused-rerun-2026-08-02`
passed cross-owner handoff and left two `B` verdicts caused by one provenance
blur: advisor-authored operations entered the reusable-technique table. The
contract now gives original brief-derived direction a distinct record and
provenance; the two affected cases require a final focused rerun.

Provenance rerun `20260802-155001-editing-advisor-provenance-rerun-2026-08-02`
passed the Brand Kit boundary and left one `B` caused by mixed canonical timing
coordinates. The runtime contract now requires one timing basis per packet and
permits conversions only as labeled derived metadata.

Final latest-case evidence is five `A` verdicts: transition and incomplete in
`20260802-154117-editing-advisor-rerun-2026-08-02`, cross-owner in
`20260802-154655-editing-advisor-focused-rerun-2026-08-02`, Brand Kit boundary
in `20260802-155001-editing-advisor-provenance-rerun-2026-08-02`, and Resource
Bank recipe in `20260802-155201-editing-advisor-timing-rerun-2026-08-02`.
Independent rereview passed at TAS-A with no scoped hard-gate failures.

## Before Behavior

- Content planning could map an editing element directly to a renderer without
  a dedicated compatibility and timed-recipe owner.

## After Behavior

- Complete editing elements pass through a dedicated advisor before rendering,
  with source boundaries, explicit decisions, ordered operations, and proof.

## Followups

- Ingest newly learned Vox techniques into Resource Bank as `editing`
  CreativeElements instead of expanding this skill with recipe prose.
