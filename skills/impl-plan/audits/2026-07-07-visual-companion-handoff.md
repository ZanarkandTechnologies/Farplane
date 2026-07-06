---
skill: impl-plan
date: 2026-07-07
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/impl-plan/SKILL.md
after_ref: skills/impl-plan/SKILL.md
reasoning_basis: deliberative_advice
proof_artifacts:
  - tickets/TASK-0308/ticket.md
eval_required: yes
---

# Skill Audit

## Change

- Before: `impl-plan` could place optional Mermaid diagrams inside `ticket.md`.
- After: material plans link a non-blocking `diagrams.md` companion generated
  through `diagramming`; the companion includes a target flow and explicit
  before/after delta while `ticket.md` stays canonical and textual by default.
- Why: the operator needs a diagram-first reading surface without turning
  diagrams into reviewer burden or duplicated canonical state.
- Tradeoff accepted: one extra companion artifact per material plan.

## First-Principles Reasoning

- Objective: make material implementation plans easier to read and approve.
- Placement logic: `impl-plan` owns ticket creation and the companion template;
  `diagramming` owns rendering.
- Expected behavior delta: material `impl-plan` output now includes
  `visual_companion_handoff` or a concrete not-applicable reason.
- Proof needed: skill validation plus manual check that ticket diagrams are no
  longer recommended as canonical plan state.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` signature, phase boundary, todo, outputs name the handoff. |
| `reference_load_precision` | pass | Template reference is loaded only for post-plan companion handoff. |
| `missing_context_rate` | pass | Canonical/non-blocking boundary remains in first load. |
| `noisy_context_rate` | pass | Full companion template lives in `references/`. |
| `duplicated_instruction_count` | pass | `impl-plan` owns template; `diagramming` owns rendering convention. |
| `prompt_size_tokens` | pass | Added concise gates instead of embedding full template in `SKILL.md`. |
| `task_success_rate` | unknown | Requires future generated-ticket observation. |
| `review_tas_rate` | unknown | Requires future reviewer receipts. |
| `maintenance_locality` | pass | Future template edits belong in `references/visual-companion-template.md`. |
| `composition_clarity` | pass | Signature now names `visual_companion_handoff`. |

## Proof Artifacts

- Skill-local evals, when needed: not required for this contract wording change.
- Structure evals, when needed: not required.
- Reviewer receipt: inline self-check only.
- Validator: pending in `TASK-0308`.
- Eval required: yes; added `impl_plan_visual_companion_file_01`.
- Evidence gaps: live installed skill behavior not checked until reinstall.

## Before Behavior

- Material plans could keep visual maps inside `Change Plan`.

## After Behavior

- Material plans keep `ticket.md` canonical and link
  `tickets/TASK-XXXX/diagrams.md` as a structured before/after companion.

## Followups

- Observe the next `impl-plan` ticket and add an eval only if agents skip the
  companion or make it canonical again.
