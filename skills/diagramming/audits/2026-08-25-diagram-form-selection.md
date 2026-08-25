---
skill: diagramming
date: 2026-08-25
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/diagramming/SKILL.md@pre-TASK-0445
after_ref: skills/diagramming/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - tickets/TASK-0445/artifacts/qa/diagram-form-calibration.md
  - tickets/TASK-0445/artifacts/review/completion-review.md
eval_required: no
---

# Skill Audit: Diagram Form Selection

## Change

- Before: the skill made Before/After Mermaid maps the default, while the ticket
  template calibrated a generic arrow chain. A user journey, recovery state,
  data boundary, dry run, UI path, and system delta could all be forced into
  the wrong shape.
- After: the first action is to bind the reader's approval question and select
  one compact sequence, state, boundary/data, trace, wireflow, delta, or table
  form. Before/After remains required for an `impl-plan` delta companion.
- Why: the observed miss is form selection, not missing diagram syntax.
- Tradeoff accepted: the guide adds a short taxonomy and examples, but does not
  add a field, runtime, validator, or mandatory Mermaid output.

## First-Principles Reasoning

- Objective: let an unfamiliar reader simulate the specific decision a diagram
  is supposed to make inspectable.
- Placement logic: the global template provides one universal routing sentence;
  the ticket template and README own ticket authoring; `diagramming` owns the
  reusable selection procedure and patterns; UI visual direction remains in
  `functional-ui` and `visual-design`.
- Expected behavior delta: `scope -> generic chain` becomes
  `scope -> approval question -> matching compact form -> proof-bearing view`.
- Proof needed: six-scope calibration, structural validation, and independent
  review of owner boundaries and prompt quality.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` contains selector, rendering boundary, companion rule, and rejection rule. |
| `reference_load_precision` | pass | Concrete forms live in `references/patterns.md`; normal selection remains first-load. |
| `missing_context_rate` | pass | The six requested scope classes are named in the selection guide. |
| `noisy_context_rate` | pass | Global guidance is one routing sentence; detailed examples stay local. |
| `duplicated_instruction_count` | pass | Global routes, ticket authoring guides, and the diagramming procedure have separate jobs. |
| `prompt_size_tokens` | pass | The skill shrank from 192 to 103 lines while making form choice explicit. |
| `task_success_rate` | unknown | Future operated use is needed for a rate claim. |
| `review_tas_rate` | pass | Current independent review returns TAS-A. |
| `maintenance_locality` | pass | Future pattern changes route to `skills/diagramming/references/patterns.md`. |
| `composition_clarity` | pass | UI behavior, visual design, ticket contract, and standalone packs are explicitly separated. |

## Proof Artifacts

- Skill-local evals: not added; visual-form selection is judgment-heavy and the
  bounded calibration matrix plus independent review are the honest proof lane.
- Structure validation: focused ticket, template, skill, documentation, and
  invariant checks pass; see `tickets/TASK-0445/artifacts/qa/validation.md`.
- Reviewer receipt: TAS-A at
  `tickets/TASK-0445/artifacts/review/completion-review.md`.
- Eval required: no; add an eval only if observed use shows repeatable form
  selection failures that a fixture can judge reliably.
- Evidence gaps: no live corpus of post-change ticket diagrams yet.

## Before Behavior

- A delta map was the default even when the reader needed a flow, state, data,
  dry-run, or UI answer.

## After Behavior

- The approval question selects form before rendering syntax.
- A table is allowed for a mapping/comparison; a ticket retains its minimal
  directed ASCII Contract Diagram alongside it.
- Before/After is constrained to system-delta questions and the explicit
  `impl-plan` companion contract.

## Followups

- If a future ticket still uses a mismatched form, add one realistic eval or
  reviewer calibration case at the owning diagramming surface.
