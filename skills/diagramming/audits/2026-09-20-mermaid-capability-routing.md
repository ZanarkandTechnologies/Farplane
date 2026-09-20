---
skill: diagramming
date: 2026-09-20
change_type: reference
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/diagramming/references/patterns.md@pre-mermaid-capability-routing
after_ref: skills/diagramming/references/patterns.md
reasoning_basis: first_principles + official_docs + reviewer
proof_artifacts:
  - https://mermaid.js.org/intro/syntax-reference.html
  - https://mermaid.js.org/syntax/mindmap
  - https://mermaid.js.org/syntax/timeline
eval_required: yes
---

# Diagramming Mermaid Capability Routing Audit

## Change

- Before: the form selector covered the normal Farplane diagram questions but
  did not expose Mermaid's broader supported diagram families.
- After: the conditional patterns reference maps hierarchy, chronology, actor
  interaction, state, ownership, schema, work history, and quantitative
  questions to current Mermaid families with renderer and fallback guards.
- Why: agents were treating Mermaid mainly as flowcharts and could not discover
  mindmaps, timelines, Gantt, journeys, architecture, schema, or data-chart forms.
- Tradeoff accepted: the catalog adds conditional reference depth while keeping
  the first-load `SKILL.md` focused on choosing the reader's question.

## First-Principles Reasoning

- Objective: choose the smallest visual form that makes the reader's approval
  question inspectable.
- Placement logic: selection behavior stays in `SKILL.md`; the long, evolving
  Mermaid type catalog belongs in `references/patterns.md`.
- Expected behavior delta: a diagramming invocation can consider the full
  useful Mermaid form space without forcing unsupported or decorative diagrams.
- Proof needed: official catalog grounding, focused skill validation, and an
  independent skill-contract review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` now names hierarchy, chronology, causal/strategy, quantitative, and exact-mapping routes. |
| `reference_load_precision` | pass | The catalog loads only after the reader question requires diagram selection. |
| `missing_context_rate` | pass | The catalog covers Mermaid's current major families and names renderer verification. |
| `noisy_context_rate` | pass | Detailed syntax remains in official docs rather than the local reference. |
| `duplicated_instruction_count` | pass | The reference extends the existing selector without copying syntax examples. |
| `prompt_size_tokens` | pass | Three first-load routing lines were added; the evolving catalog remains in the conditional reference. |
| `task_success_rate` | pass | `diagramming_rich_form_selection_01` passed candidate and baseline with verdict A. |
| `review_tas_rate` | pass | Independent rereview found the behavior TAS-A after this evidence reconciliation. |
| `maintenance_locality` | pass | Mermaid capability detail has one owner in the diagramming patterns reference. |
| `composition_clarity` | pass | The selector takes reader question and renderer support and returns a diagram family. |

## Proof Artifacts

- Skill-local eval: `skills/diagramming/evals/evals.json` covers hierarchy,
  chronology/dependency, exact-mapping, and table-fallback routing.
- Structure evals, when needed: focused skill-system validation.
- Eval receipt:
  `.farplane/evals/runs/20260920T080118Z-diagramming-rich-form-routing-v2/summary.json`
  passed `1/1`; candidate and baseline passed with verdict A.
- Reviewer receipt: independent first-principles rereview on 2026-09-20 found
  all behavior and ownership blockers fixed; TAS-A after audit reconciliation.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py`.
- Eval required: yes; first-load routing changed and needs a focused behavior
  comparison before promotion.
- Evidence gaps: renderer support varies by client and must be verified at use time.
- Eval calibration: the first comparison correctly routed all three questions
  but failed because its rubric required two unrequested final-answer
  statements; the corrected case judges the form-selection behavior directly.

## Before Behavior

- The skill chose seven common forms but offered no route to Mermaid's wider
  hierarchy, chronology, planning, schema, work-state, or quantitative catalog.

## After Behavior

- The skill keeps question-first selection and can route to the wider catalog,
  while experimental or unsupported forms fall back to stable Mermaid, ASCII,
  tables, or prose.

## Followups

- Add a renderer-fallback eval only if that behavior is later claimed as tested
  rather than guarded by first-load instructions and use-time verification.
