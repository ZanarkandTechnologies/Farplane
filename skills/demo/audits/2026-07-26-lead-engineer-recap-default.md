---
skill: demo
date: 2026-07-26
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: git:HEAD:skills/demo/SKILL.md
after_ref: skills/demo/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - tickets/archive/TASK-0413/artifacts/validation/
  - tickets/archive/TASK-0413/artifacts/review/
eval_required: yes
---

# Demo Skill Audit

## Change

- Before: Generic demo packaging selected screenshots, HTML, slides, clips, or
  video without one narrative or finish contract.
- After: One evidence-grounded narrated lead-engineer MP4 is the default for
  material implementation Goals after QA.
- Why: Long-running work needs a fast context refresh that also preserves proof.
- Tradeoff accepted: Material Goal completion gains one production/review phase.

## First-Principles Reasoning

- Objective: Make completed Goal work understandable and defensible in under
  two minutes.
- Placement logic: The skill owns the stable recipe; `program.md` owns the
  invocation order; tickets remain context and proof rather than configuration.
- Expected behavior delta: The candidate should consistently select narrated
  MP4, bind claims to evidence, and block on failed QA or unauthorized spend.
- Proof needed: Static skill validation, candidate/baseline evals, and
  independent TAS-A review.

## Eval Experiment Expectation

```text
hypothesis: Loading the upgraded demo skill makes the recap route and its gates
  explicit compared with the no-skill baseline.
expected_observation: Candidate passes at least 3/4 tasks and materially
  outperforms baseline on MP4 selection, evidence mapping, and blocker behavior.
observation_horizon: one four-task paired run
confidence: medium
falsifier: candidate passes fewer than 3 tasks or does not beat baseline
surprise_trigger: 4/4 candidate and 0/4 baseline requires leakage/trigger review
surprise_route: agent-qa-test:experiment
```

The expectation is separate from task prompts and grading assertions.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Signature, context, gates, eight-step todo |
| `reference_load_precision` | pass | Recipe loads only after QA/run-dir setup |
| `missing_context_rate` | pass | Final candidate evals 4/4 TAS-A |
| `noisy_context_rate` | pass | Stable recipe moved to one method reference |
| `duplicated_instruction_count` | pass | Goal surfaces contain invocation only |
| `prompt_size_tokens` | unknown | Not measured; surface budget passes |
| `task_success_rate` | pass | Final candidate evals 4/4 TAS-A |
| `review_tas_rate` | pass | Independent completion review TAS-A |
| `maintenance_locality` | pass | Behavior, QA, evals, and recipe are demo-owned |
| `composition_clarity` | pass | Child routes specialize plan/story/audio/render |

## Proof Artifacts

- Skill-local evals, when needed: `skills/demo/evals/evals.json`
- Structure evals, when needed: skill-system validator
- Reviewer receipt:
  `tickets/archive/TASK-0413/artifacts/review/2026-07-26-completion-receipt.json`
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
- Eval required: yes
- Evidence gaps: native paired trigger comparison was inconclusive; no
  candidate-over-baseline rate is claimed

## Eval Query Review

```text
eval_query_review:
  changed_files: [skills/demo/evals/evals.json]
  reviewed_rows: [demo_builds_verified_lead_recap_01,
    demo_blocks_without_passing_qa_01,
    demo_rejects_pptx_and_generated_visuals_01,
    demo_blocks_unauthorized_narration_spend_01]
  reviewer: self plus Codex judge
  query_spoiler_verdict: pass
  fixes_applied: none
  deferrals: independent reviewer will recheck the rows
  remaining_risk: native skill-trigger telemetry was inconsistent
```

## Before Behavior

- Output format varied per run.
- There was no stable executive narrative, media probe, evidence map, or TAS-A
  recap gate.

## After Behavior

- Material implementation Goals compile `QA -> demo MP4 -> completion review ->
  close`.
- Direct fixes and non-implementation Goal modes skip the phase.
- `result.json` stays compatible with existing Farplane validators.

## Followups

- Candidate evals: 4/4 TAS-A across the final unchanged and rerun task groups.
- Goal compiler checkpoint: 1/1 TAS-A.
- Paired native-discovery baseline: inconclusive due inconsistent trigger
  telemetry; no improvement-rate claim is made.
- Independent reviewer: TAS-A across skill-contract, prompt-quality,
  eval-quality, integration-readiness, and evidence-quality.
