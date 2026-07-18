---
skill: skill-maintenance
date: 2026-07-18
change_type: structure
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/skill-maintenance/SKILL.md@HEAD
after_ref: skills/skill-maintenance/SKILL.md
reasoning_basis: advise
proof_artifacts:
  - bin/validators/test_check_changed_file_line_count.py
  - .farplane/evals/runs/20260718-075355-skill-line-cap-before/summary.json
  - .farplane/evals/runs/20260718-075133-skill-line-cap-after/summary.json
  - .farplane/evals/runs/20260718-081318-skill-line-cap-final3/summary.json
eval_required: yes
---

# Skill Audit

## Change

- Before: maintenance had advisory size review and a 465-line first-load file.
- After: the 200-line staged cap is a hard gate; `SKILL.md` is 159 lines,
  structure QA is compacted below the cap, and conditional mode detail lives in
  a precisely routed 99-line reference.
- Why: maintenance must repair violations without weakening skill behavior.
- Tradeoff accepted: untouched legacy violations remain until staged.

## First-Principles Reasoning

- Objective: make compact skill source a repeatable commit invariant.
- Placement logic: validator owns blocking; maintenance owns safe splitting,
  validation, audit, and reviewer routing.
- Expected behavior delta: maintainers split oversized authored files by real
  ownership boundaries and rerun affected proof.
- Proof needed: line counts, validator unit tests, skill-system checks, staged
  hook, and independent review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | default modes, ownership, gates, and finish path remain first-load |
| `reference_load_precision` | pass | todo 2 explicitly loads `maintenance-modes.md` after mode selection |
| `missing_context_rate` | pass | line cap, validation, audit, and review remain in `SKILL.md` |
| `noisy_context_rate` | pass | automation and handoff templates moved behind the mode branch |
| `duplicated_instruction_count` | pass | detailed mode prose has one reference owner |
| `prompt_size_tokens` | pass | 465 → 159 lines |
| `maintenance_locality` | pass | enforcement and repair owners are explicit |
| `composition_clarity` | pass | signature exposes modes, gates, routes, and failures |

## Proof Artifacts

- Skill-local evals: required because the compaction changed an agent behavior
  contract, even though cap enforcement itself is deterministic.
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

- Parent commit `66976dcc`: maintenance passed 1/3 in one model-judged run.
- Immediate compacted commit `b4fea3bc`: maintenance passed 1/3, with a different
  case passing; aggregate parity hid changed behavior.
- Repair restored explicit sandbox isolation, template/checklist findings,
  exact registry/validation routing, blocker-before-done, and live-copy timing.
- Final coherent suite `20260718-081318-skill-line-cap-final3`: all three
  maintenance cases passed A.
- Residual risk: model-judged evals are stochastic; the final coherent receipt
  is stronger evidence than comparing aggregate pass rates alone.
- Corrective independent review: TAS-A with no blockers.

## Current QA Verdicts

| Check | Verdict | Evidence |
| --- | --- | --- |
| 1 first-load sufficiency | pass | default modes and gates remain first-load |
| 2 reference precision | pass | mode reference loads after selection |
| 3 missing context | pass | repair and finish contracts retained |
| 4 noisy context | pass | conditional modes moved |
| 5 duplication | pass | detailed mode prose has one owner |
| 6 authored file cap | pass | all six staged skill text files are <=200 |
| 7 maintenance locality | pass | validator enforces; skill repairs |
| 8 composition clarity | pass | modes, gates, routes, fails explicit |
| 9 section necessity | pass | template spine only |
| 10 gotcha integration | pass | recurrence rules are operationalized |
| 11 workflow duplication | pass | one numbered workflow |
| 12 instruction alignment | pass | executable actions are in todos |
| 13 reference escape hatch | pass | mode branch names its reference |
| 14 line review | pass | SKILL 465 → 159; QA 351 → 149 |
| 15 question signature | not_applicable | no long intake list |
| 16 extra section value | pass | signature is template-supported |
| 17 proof fit | pass | deterministic validator and unit tests |
| 18 signal layer fit | pass | no metric or reward changes |
| 19 task-case quality | pass | boundary, exclusion, binary cases |
| 20 anti-cheat | not_applicable | no agent eval prompt changed |
| 21 QA preflight | pass | todo 2 loads structure QA by mode |
| 22 QA independence | pass | native reviewer used |
| 23 QA/gotcha dedupe | pass | checklist and gotchas stay distinct |
| 24 context isolation | pass | no private context added |
| 25 low-value prose | pass | first-load prose is operational |
| 26 golden independence | not_applicable | no golden used |
| 27 lean owner reuse | pass | existing validator and gate reused |

## Before Behavior

Maintenance reviewed length but could accept oversized authored skill files.

## After Behavior

Maintenance runs the staged cap, splits by branch or responsibility, and
revalidates imports, links, generators, tests, audits, and review evidence.

## Followups

Use the ratchet to compact legacy oversized skill files as they are next staged.
