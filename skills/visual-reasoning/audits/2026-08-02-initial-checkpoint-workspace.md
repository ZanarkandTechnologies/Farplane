---
skill: visual-reasoning
date: 2026-08-02
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: docs/skills/registry.jsonl
after_ref: skills/visual-reasoning/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - tickets/TASK-9010/artifacts/verification.md
  - tickets/TASK-9010/artifacts/review/completion-review.md
eval_required: yes
---

# Skill Audit

## Change

- Before: Farplane had adjacent image-generation, screenshot-judgment, and
  frame-reconstruction skills but no analytical visual scratchpad owner.
- After: `visual-reasoning` owns a deterministic mark-render-reobserve loop
  with one latest image, immutable checkpoints, and exact operation receipts.
- Why: exact spatial references are easily lost in language-only reasoning.
- Tradeoff accepted: checkpoint images duplicate pixels so the trail remains
  directly inspectable and recoverable.

## First-Principles Reasoning

- Objective: reduce entity and path reference drift during difficult visual
  reasoning.
- Placement logic: a progressive Tier 3 skill is cheaper and more reusable
  than global prompt policy, a dedicated subagent, or a CV service.
- Expected behavior delta: agents create a workspace only when spatial working
  memory is useful, reobserve every material edit, and return image evidence.
- Proof needed: deterministic lineage tests, natural behavior evals, registry
  checks, and independent skill-contract/evidence review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | installed semantic runs created complete workspaces and receipts from `SKILL.md` |
| `reference_load_precision` | pass | first load points only to the helper, QA checklist, evals, and conditional review route |
| `missing_context_rate` | pass | dense, path, resume, direct, and CV cases have sufficient inputs and explicit workspace rules |
| `noisy_context_rate` | pass | direct-answer case received TAS-A without workspace ceremony |
| `duplicated_instruction_count` | pass | canonical checkpoint, reobserve, and receipt requirements each have one owning section plus checklist invocation |
| `prompt_size_tokens` | pass | skill surface remains within the skill-maintenance budget; aggregate failure belongs only to `content-impl-plan` |
| `task_success_rate` | pass | TAS-A dense behavior trace plus TAS-A dense, path, CV, and direct semantic judgments; resume artifact trail is complete |
| `review_tas_rate` | pass | independent completion review rated skill-contract, integration-readiness, and evidence-quality TAS-A |
| `maintenance_locality` | pass | contract, helper, tests, evals, fixture, checklist, and audit are skill-local |
| `composition_clarity` | pass | direct, workspace, and conditional CV branches have distinct gates and outputs |

## Proof Artifacts

- Skill-local evals: `skills/visual-reasoning/evals/evals.json`
- Structure evals: focused workspace unit tests and `check_skills.py --write`
- Reviewer receipt: `tickets/TASK-9010/artifacts/review/completion-review.md`
- Validator: focused tests and eval lint pass; generated registry includes 124
  rows and only reports unrelated `content-impl-plan` budget debt
- Eval required: yes
- Evidence gaps: real-task ablation between coordinates-only and rendered
  reobservation remains follow-up evidence.

## Before Behavior

- Agents can discuss coordinates or create unrelated image edits, but the
  visual reasoning state is not preserved as a replayable task artifact.

## After Behavior

- Agents can update one latest analytical image while every prior checkpoint
  and operation batch remains inspectable.

## Followups

- Admit background removal, SAM-style segmentation, OCR, detection, or OpenCV
  adapters only after representative failures establish the smallest useful
  provider boundary.
- Run a later ablation comparing plain reasoning, coordinates without render,
  rendered reobservation, and rendered reobservation plus deterministic CV.

`no_self_improve_reason`: this is the first version and has no repeated
real-world usage baseline yet; defer continuous optimization until ablation or
operator-use evidence identifies a measurable weakness.
