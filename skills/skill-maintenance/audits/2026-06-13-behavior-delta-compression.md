---
skill: skill-maintenance
date: 2026-06-13
change_type: structure
owner: skill-maintenance
status: complete
review_route: reviewer
before_ref: skills/skill-maintenance/SKILL.md
after_ref: skills/skill-maintenance/SKILL.md
reasoning_basis: deliberative_advice
proof_artifacts:
  - experiments/decisions/2026-06-13-skill-maintenance-rewrite-council/context.md
  - experiments/decisions/2026-06-13-skill-maintenance-rewrite-council/synthesis.md
  - tickets/TASK-0197/ticket.md
  - tickets/TASK-0197/artifacts/proof.md
eval_required: yes
---

# Behavior Delta Compression Audit

## Change

- Before: `skill-maintenance` had two equal signatures and a verbose
  prose-heavy maintenance checklist.
- After: `skill-maintenance` has one primary behavior-delta signature,
  mode-based branch routing, variable-bound todos, and audit as a mode/output
  path.
- Why: the council selected Option B because it improves operator scan cost and
  entrypoint clarity while preserving safety gates.
- Tradeoff accepted: the todo list is more abstract, so proof must show that
  hard gates were not weakened by compression.

## First-Principles Reasoning

- Objective: make the frequent skill-update entrypoint faster and clearer while
  preserving reliable skill-system maintenance.
- Placement logic: `SKILL.md` owns every-invocation state, gates, branch
  routing, proof commands, and output; references own conditional detail.
- Expected behavior delta: agents should bind `edited_skill`,
  `expected_behavior`, `current_behavior`, `mode`, and `evidence`, then choose
  the owner surface explicitly before editing.
- Proof needed: mechanical validation, eval-case review, sandbox fixture
  dry-run, structure checklist, and reviewer pass.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | First load includes context, one signature, modes, gates, branch todo, validation, audit/review, gotchas, references, and output. |
| `reference_load_precision` | pass | Reference Map and Todo step 2 define when to load the structure checklist, eval/checklist surfaces, import preview, audit template, and fixture sandbox. |
| `missing_context_rate` | pass | Safety gates for source ownership, prototype-before-bulk, template truth, registry sync, eval-to-QA sync, audit, reinstall, and reviewer routing remain inline. |
| `noisy_context_rate` | pass | First load is 201 lines and removes the second equal signature plus broad Core Rules prose. |
| `duplicated_instruction_count` | pass | Audit behavior is now a mode/output path instead of a second signature. |
| `prompt_size_tokens` | pass | `wc -l skills/skill-maintenance/SKILL.md` reports 201 lines. |
| `task_success_rate` | unknown | Existing eval cases were reviewed against the new contract, but no live agent eval run was executed. |
| `review_tas_rate` | unknown | Reviewer verdict is pending. |
| `maintenance_locality` | pass | The behavior-delta flow keeps skill package updates owner-local. |
| `composition_clarity` | pass | Signature names inputs, outputs, state reads/writes, modes, gates, routes, and failure modes. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/skill-maintenance/eval_task.json`
  reviewed in `tickets/TASK-0197/artifacts/proof.md`.
- Structure QA, when needed: `skills/skill-maintenance/qa_checklist.md`
  applied in `tickets/TASK-0197/artifacts/proof.md`.
- Reviewer receipt: `reviewer` returned overall `TAS-A`; `skill-contract`,
  `integration-readiness`, and `evidence-quality` all passed with no blocking
  findings and no rerun required.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  passed; `--template-version 0.2.0` failed on unrelated skills, not
  `skill-maintenance`.
- Eval required: yes, via existing eval-case review and fixture dry-run.
- Evidence gaps: global template-version command still fails on unrelated
  skills (`code-review`, `goal-advisor`, `learning-drain`, `plan`), accepted as
  out of scope by reviewer for TASK-0197.

## Before Behavior

- Agents had to scan two signatures and a broad 10-step maintenance checklist
  before deciding how to update one skill.

## After Behavior

- Agents bind the target skill and behavior delta, choose a mode, route to the
  owner surface, validate, and audit with explicit branches for eval-to-QA sync,
  installed-copy differences, bulk rollout, template-version changes, and
  registry/frontmatter changes.

## Followups

- Consider script-assisted eval-to-checklist detection only after this
  human-readable contract receives reviewer approval.
- Handle unrelated `--template-version 0.2.0` failures in a separate ticket if
  global template-version cleanliness becomes a release gate.
