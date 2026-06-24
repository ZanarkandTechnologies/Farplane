---
skill: proof-advisor
date: 2026-06-24
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/task-case-design/SKILL.md
after_ref: skills/proof-advisor/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - docs/skills/registry.jsonl
  - skills/skill-maintenance/graph/skill-graph.json
  - skills/skill-maintenance/graph/farplane-lifecycle-graph.json
  - tickets/TASK-0220/ticket.md
eval_required: no
---

# Proof Advisor Rename And Workflow Inference Audit

## Change

- Before: proof selection lived in `task-case-design` and several active docs
  blurred Proof Advisor with `eval`.
- After: `proof-advisor` owns proof selection and proof-case design; `eval`
  remains the runnable eval executor after eval is selected.
- Why: proof routing is a decision step across tests, validators, eval, QA,
  visual QA, agent QA, review, and source gaps.
- Tradeoff accepted: historical audit text still names `task-case-design` as
  source history, but no active skill package or routing surface keeps the old
  name as compatibility.

## First-Principles Reasoning

- Objective: make proof routing, workflow-chain visibility, and goals scaffolds
  explicit with minimal manual metadata.
- Placement logic: skill package owns proof-routing behavior; registry/graph
  tooling owns generated workflow edges; deep-init owns project goals scaffold.
- Expected behavior delta: callers route proof uncertainty through
  `proof-advisor` before executor skills; high-level workflows opt into graph
  extraction with only `workflow: true`.
- Proof needed: skill-system validation, generated registry rows,
  lifecycle/skill graph checks, eval query lint, doc refs, and diff hygiene.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `skills/proof-advisor/SKILL.md` has trigger boundary, signature, todo path, proof surfaces, refs, and outputs. |
| `reference_load_precision` | pass | Source ledger and proof-case rubric have explicit load conditions. |
| `missing_context_rate` | pass | Proof selection, executor routing, and handoff output are in first load. |
| `noisy_context_rate` | pass | External source details and detailed rubric remain in references. |
| `duplicated_instruction_count` | pass | Active docs separate `proof-advisor` from `eval`; generated registry is not hand-edited. |
| `prompt_size_tokens` | pass | `skills/proof-advisor/SKILL.md` is 201 lines after rename. |
| `task_success_rate` | unknown | No live Codex eval run in this pass. |
| `review_tas_rate` | unknown | External reviewer not run. |
| `maintenance_locality` | pass | Proof behavior lives in `skills/proof-advisor/`; graph extraction lives in registry/graph generators. |
| `composition_clarity` | pass | `workflow: true` plus Todo List explicit refs generate ordered `workflow_refs`. |

## Proof Artifacts

- Skill-local evals, when needed: not rerun; eval rows linted.
- Structure evals, when needed: focused parser/graph tests passed.
- Reviewer receipt: not run; self-check with validators.
- Validator:
  - `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  - `python3 skills/skill-maintenance/scripts/generate_farplane_lifecycle_graph.py --check`
  - `PYTHONPATH=. uvx pytest skills/skill-maintenance/scripts/test_generate_farplane_lifecycle_graph.py skills/skill-maintenance/scripts/test_generate_skill_graph.py bin/validators/test_sync_skill_registry.py bin/validators/test_check_farplane_project_files.py`
  - `python3 skills/eval/scripts/check_eval_queries.py --root .`
  - `python3 bin/validators/check_doc_refs.py`
  - `git diff --check`
- Eval required: no, because this pass renamed/routed and added deterministic
  parser coverage rather than changing model-behavior semantics.
- Evidence gaps: external reviewer was not run; use reviewer before publishing
  this as a major skill-system milestone.

## Before Behavior

- Proof-selection responsibility could be read as `eval` in active lifecycle
  docs, causing eval execution to absorb proof-routing decisions.
- Workflow chains could be represented only through `common_chains`, `routes`,
  curated lifecycle edges, or prose.
- Deep-init goals template was plain Markdown rather than Markdown plus a
  parseable `goal-program` block.

## After Behavior

- `proof-advisor` is the operator-facing proof-routing skill with:
  `proof_advice(claim_or_behavior, risk_context?, source_material?, proof_goal?)`.
- High-level workflow skills can set `workflow: true`; generated
  `workflow_refs` come only from explicit Todo List refs such as Markdown
  `SKILL.md` links, backticked `skill-name`, or `$skill-name`.
- `skills/deep-init-project/references/GOALS_TEMPLATE.md` scaffolds one
  `farplane/goals.md` file with human Markdown plus fenced `goal-program`.

## Followups

- Consider a later reviewer pass if this workflow-chain graph becomes a UI
  contract.
- Add a goal-program parser only when a graph consumer needs generated goal
  nodes; keep `farplane/goals.md` canonical until then.
