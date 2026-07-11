---
skill: interval-update
date: 2026-07-09
change_type: structure
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/interval-update/SKILL.md@445-lines-before-slimming-pass
after_ref: skills/interval-update/SKILL.md@239-lines-after-followup-correction
reasoning_basis: advise
proof_artifacts:
  - skills/interval-update/SKILL.md
  - the former workflow index and ticket-reward reference, deleted during
    TASK-0319 refinement
  - skills/interval-update/references/parent-run-contract.md
  - reviewer:019f44fc-d055-72b0-b60b-c527f8b484ac
  - reviewer-final:019f44fc-d055-72b0-b60b-c527f8b484ac TAS pass-ready
  - reviewer-followup:019f4506-87a4-7cf2-bd9e-5ea01ce14886 TAS-A pass
eval_required: no
---

# Interval Update First-Load Slimming Audit

## Change

- Before: `SKILL.md` mixed the parent interval contract with Daily/Weekly/Pulse
  boundary prose, optional workflow catalog entries, metric helper signatures,
  and ticket reward detail.
- After: `SKILL.md` keeps the parent contract, signature, gates, todo path, and
  precise reference load conditions. Detailed catalogs moved to references.
- Why: normal interval invocations need the parent run contract first; optional
  workflow and caller-boundary details should load only after the relevant flag
  or branch is selected.
- Tradeoff accepted: agents must follow a reference link for workflow catalogs
  and ticket reward detail instead of seeing all optional detail at first load.

## First-Principles Reasoning

- Objective: make `interval-update` easier to execute without losing the
  subagent isolation, summary-context, reward-checkins exception, and
  report-before-mutation gates.
- Placement logic: first-load keeps details needed to choose, execute, stop, or
  prove one normal interval run; refs own conditional schemas and catalogs.
- Expected behavior delta: no runtime behavior change; reduced prompt load and
  clearer ownership boundaries.
- Proof needed: line budget, reference load precision, JSON validity, and skill
  registry sync.

## Low-Value Prose Scan

| Candidate | Decision | Reason |
| --- | --- | --- |
| Daily/Weekly wrapper prose in `SKILL.md` | move | Caller preset ownership matters only when reasoning about automations. |
| Pulse boundary prose in `SKILL.md` | move | The executable first-load rule is "do not reconcile boards or execute tickets"; detailed Pulse ownership belongs in a reference/Pulse. |
| Workflow reference index in `SKILL.md` | move | Needed only when optional workflows are enabled. |
| Metric helper signatures in `SKILL.md` | move | Needed only for metric workflows and refresh implementation. |
| Ticket reward block detail in `SKILL.md` | move | Needed before creating ticket deltas, not before every interval invocation. |
| Duplicate Output bullet list | rewrite | Signature and todo already carry the output contract. |

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` keeps parent contract, signature, gates, todo path, and output sentence. |
| `reference_load_precision` | superseded | TASK-0319 removed the old workflow index and Interval reward contract; the compact skill now loads only the BAU reporting reference and audit-only parent contract. |
| `missing_context_rate` | pass | Mandatory lane isolation, summary/raw evidence, reward exception, and report-before-mutation gates remain first-load. |
| `noisy_context_rate` | pass | Optional catalog, metric helpers, and caller-boundary prose moved out of first-load. |
| `duplicated_instruction_count` | pass | Workflow catalog now has one owner reference. Parent contract has a short first-load authority and an audit/shareable ref. |
| `prompt_size_tokens` | pass | `SKILL.md` reduced from 445 lines before this slimming pass to 239 lines after follow-up correction. |
| `task_success_rate` | unknown | No live interval run was executed for this structural-only change. |
| `review_tas_rate` | pass | Reviewer `019f44fc-d055-72b0-b60b-c527f8b484ac` final rerun returned TAS pass-ready with no blockers. |
| `maintenance_locality` | pass | Workflow catalog, ticket reward contract, parent contract, and extended interval config have separate owner refs. |
| `composition_clarity` | pass | Signature and todo still expose inputs, outputs, state, gates, routes, fails, and proof path. |

## Proof Artifacts

- Skill-local evals, when needed: not needed; behavior contracts from the prior
  isolation pass are unchanged.
- Structure evals, when needed: line count and skill-maintenance checklist
  applied manually in this audit.
- Reviewer receipt: `019f44fc-d055-72b0-b60b-c527f8b484ac`; final rerun was
  TAS pass-ready. Earlier TAS-B findings were fixed by making reward check-ins
  post-report patches, routing `parent-run-contract.md` as audit/compaction-only,
  and adding the ticket Reward patch write path to the signature/state contract.
- Follow-up correction: moved the `interval-update.md` reference load condition
  into the todo path and added `instruction_todo_alignment` to the
  skill-maintenance QA checklist so executable first-load instructions do not
  live only in prose. Reviewer `019f4506-87a4-7cf2-bd9e-5ea01ce14886` returned
  TAS-A pass with no blockers for this correction.
- Second follow-up correction: Step 4 now explicitly spawns a separate isolated
  lane for each enabled reward/leverage/maintenance workflow, and the
  `reward_checkins` todo is a single bounded analyzer-lane instruction.
- Validator: `python3 -m json.tool skills/interval-update/eval_task.json`;
  `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Eval required: no.
- Evidence gaps: installed live Codex skill sync was not run.

## Before Behavior

- First-load included scheduler/preset explanation, workflow catalog detail,
  metric helper signatures, and ticket reward detail before the branch was
  selected.

## After Behavior

- First-load is the parent interval contract. Optional branches load
  owner-specific references only when enabled or when ticket deltas are being
  created.

## Followups

- If another skill needs the same isolated-lane pattern, consider extracting a
  separate reusable method skill after a second concrete use case exists.
