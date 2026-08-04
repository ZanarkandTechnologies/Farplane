---
skill: impl-plan
date: 2026-08-04
change_type: structure-and-behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: working-tree:pre-TASK-9016
after_ref: working-tree:skills/impl-plan
reasoning_basis: first_principles
proof_artifacts:
  - tickets/TASK-9016/artifacts/qa/validation.md
  - tickets/TASK-9016/artifacts/review/completion-review.md
eval_required: yes
---

# Canonical Ticket Compaction Audit

## Change

- Before: `impl-plan` repeated the ticket schema across `SKILL.md`, a 245-line
  prompt, and a 227-line reference template; every plan required a separate
  `diagrams.md` even when prose was clearer.
- After: `tickets/templates/ticket.md` is the sole body-schema owner;
  `impl-plan` owns reasoning, context resolution, execution order, proof, and
  readiness; visual companions are conditional.
- Tradeoff: raw first-load lines remain the hard context gate even though the
  shared accountant reports prose, Mermaid, media, and references separately.

## First-Principles Basis

- Objective: preserve reconstructable implementation intent while removing
  repeated representation policy and diagram ceremony.
- Ownership: the ticket template defines shape, the planner fills it, the
  validator diagnoses context pressure, and `goal-advisor` compiles approved
  execution.
- Falsification: fail if a simple ticket needs a companion, two active schemas
  remain, a builder must invent scope/order/proof, or category accounting
  weakens the raw 300/400 first-load boundary.

## Size Evidence

| Authored surface | Before | After |
| --- | ---: | ---: |
| `SKILL.md` | 471 | 169 |
| `qa_checklist.md` | 261 | 118 |
| `prompts/plan.md` | 245 | 102 |
| `references/template.md` | 227 | 20 |
| `README.md` | 85 | 56 |
| `AGENTS.md` | 101 | 63 |

The reference template remains only as a superseded pointer so historical
links resolve. Examples and the optional visual template remain branch-loaded,
and every edited authored skill file is below 200 lines.

## Behavior Evidence

- A ticket with neither a companion link nor `diagrams.md` passes.
- Inline Mermaid passes and is still counted in the raw ticket context.
- A linked missing companion and an orphaned file fail.
- A linked companion still requires canonical metadata, Before/After Mermaid,
  legends, and applied semantic classes.
- The localized-backend eval row now rejects a parallel schema and unnecessary
  diagrams; eval-query lint and deterministic skill/eval tests pass.
- A live judged rerun is deferred because the existing local eval receipts
  record an external Codex usage ceiling; no result is claimed from that lane.

## Five-Ticket Diagnostic Sample

| Ticket | Prose words | Prose lines | Raw planning result |
| --- | ---: | ---: | --- |
| TASK-9015 | 1061 | 194 | pass |
| TASK-9006 | 374 | 76 | pass |
| TASK-0422 | 3411 | 534 | fail at 799 first-load lines |
| TASK-0426 | 231 | 43 | pass |
| TASK-0425 | 583 | 101 | pass |

This sample supports category diagnostics without turning line count into a
quality score. TASK-0422 remains an honest hard-limit failure rather than being
rewritten to improve the metric.

## Skill-Maintenance Review

| Check | Verdict | Evidence |
| --- | --- | --- |
| first-load sufficiency | pass | signature and eight-step Todo retain the normal path and gates |
| reference-load precision | pass | only examples and complex companion guidance are branch-loaded |
| duplicated instruction count | pass | canonical body schema has one owner |
| authored file structure | pass | prompt, QA, examples, validator, and historical pointer have distinct owners |
| composition clarity | pass | reads, writes, context decisions, gates, failures, and Goal handoff are explicit |
| proof surface fit | pass | parser/validator behavior has unit tests; variable plan behavior has eval rows; judgment routes to reviewer |
| anti-cheat case design | pass | backend prompt states product constraints without naming the desired internal workflow |
| lean owner reuse | pass | ticket validation imports the existing response accountant rather than duplicating parsing |

## Promotion Gate

- Deterministic validation: see the ticket QA receipt.
- Behavioral suite: updated and linted; live judge rerun deferred as recorded.
- Independent review: `completion-review.md` passed TAS-A after the reviewer
  caught and we removed a competing `tickets/README.md` section catalogue.
- Promotion decision: accept.

## Post-Review Correction

- A follow-up audit found that QA was loaded before planning and named in the
  prompt, but the first-load Todo did not explicitly reapply it at the end.
- The final handoff step now reapplies `qa_checklist.md` after drafting and
  repairs, resolves `revise`, stops on `block`, and records the finish verdict
  before independent review.
