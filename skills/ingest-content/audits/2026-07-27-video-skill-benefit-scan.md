---
skill: ingest-content
date: 2026-07-27
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/ingest-content/SKILL.md@HEAD
after_ref: skills/ingest-content/SKILL.md
reasoning_basis: advise
proof_artifacts:
  - .farplane/evals/runs/20260727-085743-ingest-skill-benefit-2026-07-27-r2
  - .farplane/evals/runs/20260727-085933-ingest-skill-benefit-2026-07-27-r3
  - .farplane/evals/runs/20260727-090054-ingest-skill-benefit-baseline-2026-07-27
  - .farplane/evals/runs/20260727-095118-ingest-skill-benefit-heldout-2026-07-27-r2
eval_required: yes
---

# Video Skill-Benefit Scan

## Change

- Before: ingestion could add optional skill findings during Resource Bank
  storage, but no explicit terminal verification gate, finding contract, or
  escalation boundary existed.
- After: every video ingestion runs a lightweight skill-benefit scan after
  retrieval verification, returns grounded findings or an honest empty list,
  and conditionally routes workflow-teaching evidence to `harness-scout`.
- Why: preserve the source evidence while it is fresh and make useful
  video-to-skill opportunities visible without turning every aesthetic capture
  into skill-maintenance work.
- Tradeoff accepted: video ingestion gains one registry-shortlist judgment step;
  heavier source-todo reconstruction remains conditional.

## First-Principles Reasoning

- Objective: detect whether an ingested video contains an operational technique
  that could improve a current Farplane skill.
- Placement logic: `ingest-content` owns the terminal scan because it already
  has the source evidence and verified capture; `harness-scout` owns deeper
  source-todo reconstruction and adoption judgment.
- Expected behavior delta: videos return `skill_findings[]` using
  `covered | augment | missing | reject | defer`, with evidence and owner
  routing; aesthetic-only videos return `[]`.
- Proof needed: one workflow-teaching case, one aesthetic no-op case,
  deterministic skill validation, and independent review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Signature, ordered todo step, output template, and action boundary are in `SKILL.md`. |
| `reference_load_precision` | pass | `phase-router.md` owns the detailed terminal branch; `harness-scout` has an explicit escalation condition. |
| `missing_context_rate` | pass | Result fields, statuses, evidence sources, empty-result behavior, and blocked retrieval behavior are explicit. |
| `noisy_context_rate` | pass | Full video reconstruction remains behind `harness-scout`; normal ingest uses a registry shortlist only. |
| `duplicated_instruction_count` | pass | Resource Bank references no longer describe skill findings as stored schema. |
| `prompt_size_tokens` | unknown | No token benchmark was run; the first-load delta is bounded to one ordered todo phase and compact routing/output rules. |
| `task_success_rate` | pass | Workflow, aesthetic no-op, and less-leading held-out owner-comparison cases each scored A with behavior trace pass. |
| `review_tas_rate` | pass | Final independent re-review returned TAS-A with no hard-gate failures. |
| `maintenance_locality` | pass | Runtime behavior is owned by `ingest-content`; deeper adoption remains owned by `harness-scout`. |
| `composition_clarity` | pass | Inputs, result fields, status vocabulary, escalation, and no-mutation boundary are named. |

## Proof Artifacts

- Skill-local evals:
  - Workflow-teaching case:
    `.farplane/evals/runs/20260727-085933-ingest-skill-benefit-2026-07-27-r3`
    — A/pass with behavior trace pass.
  - Aesthetic no-op case:
    `.farplane/evals/runs/20260727-085743-ingest-skill-benefit-2026-07-27-r2`
    — A/pass with behavior trace pass.
  - Held-out owner-comparison case:
    `.farplane/evals/runs/20260727-095118-ingest-skill-benefit-heldout-2026-07-27-r2`
    — A/pass with behavior trace pass after the first held-out run exposed and
    hardened an unresolved duplicate-owner recommendation.
- Candidate/baseline comparison:
  `.farplane/evals/runs/20260727-090054-ingest-skill-benefit-baseline-2026-07-27`
  — inconclusive. The workflow candidate did not trigger native-skill
  detection, so its baseline was skipped; the aesthetic case tied at B because
  the candidate invented an unsupported downstream route while the baseline
  omitted the explicit empty finding list. Both behavior traces passed.
- Validator:
  `python3 skills/skill-maintenance/scripts/check_skills.py --write` regenerated
  registries successfully; its only surface-budget findings were pre-existing
  `content-impl-plan` limits outside this package.
- Document refs: `python3 bin/validators/check_doc_refs.py` passed.
- Reviewer receipt:
  `skills/ingest-content/audits/2026-07-27-video-skill-benefit-review.md`
  — initial TAS-B fixes were applied; final re-review passed TAS-A.
- Eval required: yes; focused candidate cases passed, while the optional
  comparison run is retained as variance evidence rather than hidden.
- Evidence gaps: no real Resource Bank video ingestion was performed because
  this is a skill-contract change; fixtures isolate the post-retrieval phase.

## Before Behavior

```text
store_capture(...)
  -> optional skill findings
  -> retrieval
```

The optional finding had no required timing, owner comparison, schema, no-op
behavior, or escalation rule.

## After Behavior

```text
verify_retrieval(capture)
  -> verify_skill_benefit(capture, source_evidence, skill_registry)
  -> { retrievalStatus, scanStatus, skill_findings[] }
```

Each finding contains `skill`, `status`, `evidenceAnchor`, `benefit`,
`confidence`, and `recommendedRoute`. Overlapping candidates resolve to one
primary owner with an explicit boundary. The scan never edits a skill, creates
a skill-improvement ticket, or extends Resource Bank schema.

## Followups

- Target and structure QA were reapplied after reviewer feedback; final review
  passed TAS-A.
- Treat the inconclusive baseline comparison as eval-runner variance evidence;
  do not weaken the evidence or no-mutation contract to optimize trigger
  detection.
