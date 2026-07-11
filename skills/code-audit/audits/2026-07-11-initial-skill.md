---
skill: code-audit
date: 2026-07-11
change_type: structure
owner: skill-creator
status: pass
review_route: deliberative_advice
before_ref: no dedicated code-audit skill package
after_ref: skills/code-audit/SKILL.md
reasoning_basis: deliberative_advice + first_principles
proof_artifacts:
  - tickets/TASK-0324/ticket.md
  - skills/code-audit/eval_task.json
  - python3 skills/skill-maintenance/scripts/check_skills.py --write
  - python3 bin/validators/sync_skill_registry.py --check
  - python3 tickets/scripts/check_ticket_metadata.py
eval_required: yes
---

# Skill Audit

## Change

- Before: Whole-codebase improvement curiosity could route informally to
  `refactoring` or `hardening`, creating pressure toward broad cleanup.
- After: `code-audit` owns top-down inventory, component ranking, architecture
  audit, module audit sequencing, and ticket-backed follow-ups.
- Why: Ranking and ticket creation are distinct from executing a refactor or
  mitigation. A separate skill keeps newer-model audit passes useful without
  making them rewrite buttons.
- Tradeoff accepted: One new Tier 3 orchestration skill is added instead of
  expanding existing execution skills.

## First-Principles Reasoning

- Objective: Use newer model capability to find high-leverage improvements
  while preserving Farplane's ticket-first proof discipline.
- Placement logic: `refactoring` owns behavior-preserving code shape changes;
  `hardening` owns risk mitigation; `code-audit` owns deciding what should be
  inspected and ticketed first.
- Expected behavior delta: Agents should rank core components, audit
  architecture before modules, create or propose coherent tickets, and stop
  before broad implementation.
- Proof needed: Skill validation, structure checklist pass, and eval cases that
  catch rewrite temptation, architecture-first behavior, and evidence-gap
  handling.

## Binary Rubric

Use `pass`, `fail`, or `unknown`. Use `unknown` when evidence does not exist.

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` includes trigger, signature, budget, todo path, gates, routes, gotchas, references, and output contract. |
| `reference_load_precision` | pass | Each reference is named with a load condition in the todo list and Reference Map. |
| `missing_context_rate` | pass | Normal audit behavior is in first load; only scoring/workflow/ticket detail is conditional. |
| `noisy_context_rate` | pass | Long ranking, audit, and ticket details are in references instead of first load. |
| `duplicated_instruction_count` | pass | `SKILL.md`, references, QA checklist, eval, and example have distinct jobs. |
| `prompt_size_tokens` | pass | `SKILL.md` is below the 250-line review trigger. |
| `task_success_rate` | unknown | Eval cases are added but no eval runner result exists yet. |
| `review_tas_rate` | unknown | No independent reviewer receipt exists yet. |
| `maintenance_locality` | pass | Future edits have one package owner under `skills/code-audit/`. |
| `composition_clarity` | pass | Signature and todos name inputs, outputs, reads, writes, routes, and failure modes. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/code-audit/eval_task.json`
- Structure evals, when needed: not run in this pass
- Reviewer receipt: not available in this pass; inline checklist review used
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  passed; `python3 bin/validators/sync_skill_registry.py --check` passed;
  `python3 tickets/scripts/check_ticket_metadata.py` passed
- Eval required: yes, because this is a prompt-like behavioral skill
- Evidence gaps: live agent-behavior test of the new skill remains future work

## Before Behavior

- A user asking "new model came out, upgrade the codebase" could produce broad
  refactoring/hardening advice or implementation without ranking core
  components and creating proof-backed tickets.

## After Behavior

- The same request should produce a component inventory, ranked audit order,
  architecture-first findings, owner-skill routes, ticket specs, proof routes,
  residual risks, and a concrete next ticket.

## Followups

- Run the new eval cases through the local eval harness once the current skill
  package validates.
- Use `code-audit` on a focused Farplane surface, such as the skill system or
  ticket lifecycle, before expanding to a full repo audit.
