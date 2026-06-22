---
skill: goal-advisor, impl-plan, qa, visual-qa, agent-qa-test
date: 2026-06-22
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer_needed
before_ref: tickets/TASK-0207/ticket.md
after_ref: skills/goal-advisor/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - tickets/TASK-0207/ticket.md
  - tickets/TASK-0207/program.md
  - tickets/TASK-0207/artifacts/fixtures/generated-ui-goal-prompt.md
  - tickets/TASK-0207/artifacts/fixtures/TASK-9999-ticket.md
  - tickets/TASK-0207/artifacts/fixtures/TASK-9999-design.md
  - tickets/TASK-0207/artifacts/checklists/skill-checklist-verdicts.md
  - tickets/TASK-0207/artifacts/evals/manual-eval-results.md
  - skills/goal-advisor/qa_checklist.md
  - skills/impl-plan/qa_checklist.md
  - skills/qa/qa_checklist.md
  - skills/visual-qa/qa_checklist.md
  - skills/agent-qa-test/qa_checklist.md
eval_required: yes
---

# Goal / Impl Plan / QA Proof Cluster Audit

## Change

- Before: Goal-backed implementation work could rely on broad "satisfy
  Done / Proof" language, material `impl-plan` could be chat-shaped, and UI QA
  proof could be scattered across QA skills without forcing final image
  evidence.
- After: The target skill cluster now names ticket-first planning, compact
  file-list Goal prompts, delegated proof/drift lanes, design baselines for UI
  proof, best-image evidence, and adversarial QA boundaries.
- Why: The operator reported that Goal-packaged work felt lazy and
  self-certified, especially when UI work ended without screenshots.
- Tradeoff accepted: This pass adds first-load guardrails and QA checklists
  before doing full first-load compaction. `impl-plan` remains long and should
  be refined separately after the behavior hardening proves useful.

## First-Principles Reasoning

- Objective: Make Farplane completion proof visible and delegated without
  bloating Goal prompts or creating duplicate QA skills.
- Placement logic: Skill contracts and ticket/Goal templates own repeatable
  behavior; root prompts and Stop-hook changes are deferred unless a
  deterministic gate is later proven necessary.
- Expected behavior delta: Material planning starts in a ticket, Goal prompts
  point at files, proof-heavy checks use subagents, and UI completion surfaces
  screenshots in the final report.
- Proof needed: Skill validators, JSON eval syntax, registry sync, ticket
  validation, and reviewer TAS over the behavior and integration.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Target `SKILL.md` files now include signatures/gates or explicit proof-routing text. |
| `reference_load_precision` | pass | Goal prompt details remain in `goal-advisor/references/prompt-templates.md`; runtime guardrails are in skill-local checklists. |
| `missing_context_rate` | pass | Ticket-first, delegated proof, design baseline, and final image rules are in first-load contracts or templates. |
| `noisy_context_rate` | unknown | `impl-plan` remains over line budget; compaction is deferred. |
| `duplicated_instruction_count` | pass | `qa`, `visual-qa`, and `agent-qa-test` now name separate ownership boundaries. |
| `prompt_size_tokens` | unknown | Behavior was hardened without reducing long target skills. |
| `task_success_rate` | pass | Focused eval rows were checked against representative fixtures in `tickets/TASK-0207/artifacts/evals/manual-eval-results.md`. |
| `review_tas_rate` | pending | First reviewer returned TAS-B for evidence gaps; evidence was added and rerun review is required. |
| `maintenance_locality` | pass | Goal prompt behavior lives in goal-advisor; planning proof in impl-plan; artifact proof in qa; visual judgment in visual-qa; adversarial proof in agent-qa-test. |
| `composition_clarity` | pass | Signatures and checklists expose inputs, outputs, gates, routes, and failure modes. |

## Proof Artifacts

- Skill-local evals:
  - `skills/goal-advisor/eval_task.json`
  - `skills/impl-plan/eval_task.json`
  - `skills/qa/eval_task.json`
  - `skills/visual-qa/eval_task.json`
  - `skills/agent-qa-test/eval_task.json`
- Runtime checklists:
  - `skills/goal-advisor/qa_checklist.md`
  - `skills/impl-plan/qa_checklist.md`
  - `skills/qa/qa_checklist.md`
  - `skills/visual-qa/qa_checklist.md`
  - `skills/agent-qa-test/qa_checklist.md`
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  passed on 2026-06-22; output saved at
  `tickets/TASK-0207/artifacts/validation/check-skills.log`.
- Eval JSON check: output saved at
  `tickets/TASK-0207/artifacts/validation/eval-json.log`.
- TASK-0207 metadata check: output saved at
  `tickets/TASK-0207/artifacts/validation/task-0207-metadata.log`.
- Repo-wide metadata check: fails on unrelated TASK-0197, TASK-0201, and
  TASK-0202; output saved at
  `tickets/TASK-0207/artifacts/validation/repo-ticket-metadata.log`.
- Representative fixtures:
  - `tickets/TASK-0207/artifacts/fixtures/generated-ui-goal-prompt.md`
  - `tickets/TASK-0207/artifacts/fixtures/TASK-9999-ticket.md`
  - `tickets/TASK-0207/artifacts/fixtures/TASK-9999-design.md`
- Checklist/eval verdicts:
  - `tickets/TASK-0207/artifacts/checklists/skill-checklist-verdicts.md`
  - `tickets/TASK-0207/artifacts/evals/manual-eval-results.md`
- Reviewer receipt 1: `tickets/TASK-0207/artifacts/review/reviewer-01.md`
  returned TAS-B pending evidence. Rerun reviewer after this evidence pass.
- Remaining evidence gaps:
  - Independent rerun reviewer TAS not yet captured.
  - `impl-plan` still needs a separate compaction/refinement pass.

## Before Behavior

- Goal prompt template could be long or vague, and did not require final UI
  image evidence.
- `impl-plan` emphasized proof but did not gate material planning on a ticket
  surface or design baseline.
- `qa` gathered artifacts but did not require `best_evidence`.
- `visual-qa` did not explicitly read `design.md`.
- `agent-qa-test` could be confused with normal ticket QA.

## After Behavior

- Goal prompts require compact file lists, delegated proof routes, turn drift
  checks, and UI final image evidence.
- `impl-plan` starts with a ticket surface and names test strategy, design
  baseline, proof lanes, and final evidence for UI work.
- `qa` owns artifact reconciliation and best evidence.
- `visual-qa` owns screenshot judgment against ticket/design expectations.
- `agent-qa-test` is reserved for adversarial claim proof.

## Followups

- Run a reviewer lane over `TASK-0207` artifacts and changed files.
- Consider a separate `impl-plan` refinement ticket to reduce first-load size
  after the new behavior is accepted.
- Consider deterministic Stop-hook evidence checks only after these skill-level
  contracts produce stable artifacts.
