---
skill: skill-creator
date: 2026-07-18
change_type: structure
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/skill-creator/SKILL.md@HEAD
after_ref: skills/skill-creator/SKILL.md
reasoning_basis: advise
proof_artifacts:
  - bin/validators/test_check_changed_file_line_count.py
  - .farplane/evals/runs/20260718-075355-skill-line-cap-before/summary.json
  - .farplane/evals/runs/20260718-075133-skill-line-cap-after/summary.json
  - .farplane/evals/runs/20260718-081318-skill-line-cap-final3/summary.json
  - .farplane/evals/runs/20260718-081537-skill-line-cap-repair7/summary.json
eval_required: yes
---

# Skill Audit

## Change

- Before: creation guidance used advisory size thresholds and the first-load
  contract was 270 lines.
- After: staged authored skill text has a hard 200-line cap; `SKILL.md` is 178
  lines and preserves owner, placement, proof, QA, review, book-grounding, and
  new-skill eval/self-improve routing.
- Why: a deterministic file invariant belongs at the commit boundary and must
  also be visible while authors shape a skill.
- Tradeoff accepted: existing oversized files are ratcheted when next staged
  instead of blocking on 194 unrelated legacy files now.

## First-Principles Reasoning

- Objective: prevent oversized skill source from entering new commits.
- Placement logic: pre-commit validator owns enforcement; this skill teaches
  creation-time behavior and repair.
- Expected behavior delta: agents split authored files before staging without
  hiding mandatory first-load behavior.
- Proof needed: unit tests, line counts, skill-system validation, staged hook,
  and independent review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | signature, todos, gates, proof, and output remain in `SKILL.md` |
| `reference_load_precision` | pass | each conditional reference names its load condition |
| `missing_context_rate` | pass | default workflow did not move to a reference |
| `noisy_context_rate` | pass | repeated output and long checklist prose removed |
| `duplicated_instruction_count` | pass | one cap rule plus one execution todo |
| `prompt_size_tokens` | pass | 270 → 178 lines |
| `maintenance_locality` | pass | validator enforces; creator teaches |
| `composition_clarity` | pass | signature names state, gates, routes, and fails |

## Proof Artifacts

- Skill-local evals: required because compaction changed an agent behavior
  contract, even though the line cap itself is deterministic.
- Structure checks: `python3 skills/skill-maintenance/scripts/check_skills.py --write` passed.
- Reviewer receipt: initial TAS-B evidence fix completed; final independent
  rerun returned TAS-A with no blockers.
- Validator: focused unit tests passed. The real staged pre-commit selected and
  passed blocking `skill_file_line_count`; the overall hook failed only because
  six unrelated terminal tickets are already unarchived.
- Evidence boundary: line-cap and diff checks read staged blobs only.
  `check_skills.py` passed against the full dirty working tree, which contains
  unrelated user changes and is not staged-pure evidence.
- Evidence gaps: none for the staged change.

## Eval Comparison And Repair

- Parent commit `66976dcc`: 1/5 aggregate pass; both creator cases were C.
- Immediate compacted commit `b4fea3bc`: 1/5 aggregate pass, but assertion-level
  behavior differed, so aggregate parity was insufficient.
- Repair restored explicit book-source convergence/schema/placement/proof and
  runnable eval/deferred-proof/self-improve lifecycle obligations.
- Final coherent suite: 4/5 A at `20260718-081318-skill-line-cap-final3`; the
  remaining smallest-failing-case rerun field was then added.
- Focused final rerun: the remaining creator case passed A at
  `20260718-081537-skill-line-cap-repair7`.
- Residual risk: model-judged evals showed run-to-run variance; use the coherent
  suite plus focused repair receipt rather than claiming determinism.
- Corrective independent review: TAS-A with no blockers.

## Current QA Verdicts

| Check | Verdict | Evidence |
| --- | --- | --- |
| 1 first-load sufficiency | pass | default contract remains in `SKILL.md` |
| 2 reference precision | pass | conditional refs name when to load |
| 3 missing context | pass | gates, routing, proof, output retained |
| 4 noisy context | pass | repeated detail removed |
| 5 duplication | pass | validator enforces; skill teaches |
| 6 authored file cap | pass | six staged skill text files are <=200 |
| 7 maintenance locality | pass | commit gate is enforcement owner |
| 8 composition clarity | pass | signature exposes state and routes |
| 9 section necessity | pass | template spine only |
| 10 gotcha integration | pass | failures live in todos/gates/gotchas |
| 11 workflow duplication | pass | one numbered workflow |
| 12 instruction alignment | pass | executable actions are in todos |
| 13 reference escape hatch | pass | each moved branch is routed |
| 14 line review | pass | 270 → 178 lines |
| 15 question signature | not_applicable | no long intake list |
| 16 extra section value | pass | signature is template-supported |
| 17 proof fit | pass | deterministic validator and unit tests |
| 18 signal layer fit | pass | no metric or reward changes |
| 19 task-case quality | pass | boundary, exclusion, binary cases |
| 20 anti-cheat | not_applicable | no agent eval prompt changed |
| 21 QA preflight | pass | todo 1 loads creator QA |
| 22 QA independence | pass | native reviewer used |
| 23 QA/gotcha dedupe | pass | QA and gotchas have distinct jobs |
| 24 context isolation | pass | no private context added |
| 25 low-value prose | pass | first-load prose is operational |
| 26 golden independence | not_applicable | no golden used |
| 27 lean owner reuse | pass | existing validator extended |

## Before Behavior

Skill authors could treat line size as advisory and finish with oversized files.

## After Behavior

Skill authors must keep each staged authored skill text file at or below 200
lines and split by branch or responsibility without weakening first load.

## Followups

Migrate legacy oversized files opportunistically when they are next edited.
