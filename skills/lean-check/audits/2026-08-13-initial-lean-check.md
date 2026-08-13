---
skill: lean-check
date: 2026-08-13
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: absent
after_ref: skills/lean-check/
reasoning_basis: first_principles + harness-advisor + reviewer + focused eval
proof_artifacts:
  - python3 skills/skill-creator/scripts/quick_validate.py skills/lean-check
  - python3 skills/eval/scripts/check_eval_queries.py --root .
  - python3 skills/skill-maintenance/scripts/check_skills.py --write
  - python3 bin/validators/check_harness_invariants.py
  - .farplane/evals/runs/20260813-082547-lean-check-final/summary.json
  - skills/lean-check/audits/2026-08-13-initial-review.json
eval_required: yes
---

# Skill Audit

## Change

- Before: the global agent template carried the implementation ladder and
  `impl-plan` named an undefined `lean_plan_check` gate.
- After: `lean-check` owns a callable ladder receipt; callers consume that
  receipt instead of restating the procedure.
- Why: make the same first-sufficient-rung judgment available for direct code
  work and material implementation planning.
- Tradeoff accepted: seven ladder rungs need seven focused regressions, so this
  skill does not opt into the five-eval surface budget.

## First-Principles Reasoning

- Objective: avoid speculative, duplicate, or overbuilt implementation while
  preserving required behavior and proof.
- Placement logic: reusable judgment lives in a Tier 2 skill; global policy
  requires the call; `impl-plan` consumes the receipt; review owns TAS.
- Expected behavior delta: agents identify the first sufficient existing option
  before adding a surface and explain the smallest safe action.
- Proof needed: source and registry validation, seven rung-specific eval rows,
  global-template check, and independent review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Reviewer found the default path repeatable from `SKILL.md`. |
| `reference_load_precision` | pass | QA detail stays in `qa_checklist.md`; first-load instructions remain compact. |
| `missing_context_rate` | pass | Signature, receipt, evidence, smallest action, and routes are explicit. |
| `noisy_context_rate` | pass | The skill keeps only the ladder, receipt, and necessary boundaries in first load. |
| `duplicated_instruction_count` | pass | The skill owns the full contract; callers retain only the compact call/fallback needed at first load. |
| `prompt_size_tokens` | pass | Reviewer found no bloated first-load content. |
| `task_success_rate` | pass | Seven focused rung cases returned `A` in the final run. |
| `review_tas_rate` | pass | Independent review returned `TAS-A` for all declared families. |
| `maintenance_locality` | pass | The reusable judgment, QA, evals, and audit live under `skills/lean-check/`. |
| `composition_clarity` | pass | `impl-plan` calls one named receipt without a parallel plan schema. |

## Proof Artifacts

- Skill-local evals: `skills/lean-check/evals/evals.json`.
- Structure validation: `quick_validate.py`, eval query lint, and
  `check_skills.py --write` passed.
- Reviewer receipt: [2026-08-13-initial-review.json](2026-08-13-initial-review.json)
  returned `TAS-A` across all declared families.
- Validator: `check_harness_invariants.py` passed.
- Eval required: yes.
- Final eval: `.farplane/evals/runs/20260813-082547-lean-check-final/summary.json`
  is 7/7 `A`.
- Global caller proof: the `lean-check` invocation block in installed
  `~/.codex/AGENTS.md` matches `templates/global/AGENTS.md` exactly. Full-file
  parity is intentionally not claimed after unrelated template text changed
  outside this task.
- Runner note: `.farplane/evals/runs/20260813-083513-global-lean-check-call-final/`
  is not counted as a global-behavior result because its custom task mode injects
  only the toy-shop context, not the installed `AGENTS.md`; it correctly failed
  to observe a rule that was absent from its prompt.
- Evidence gaps: none for the skill contract or installed template; the eval
  runner needs a separate task to inject installed global prompts before it can
  prove automatic global-prompt loading dynamically.

## Before Behavior

- A global heuristic and an undefined planner label could not return a shared,
  inspectable leanness decision.

## After Behavior

- A direct coding task or implementation plan receives one rung, evidence, the
  smallest action, and a proof-preservation statement.

## Followups

- Refresh the installed `lean-check` package after this audit is written, then
  confirm source-to-live package parity.
