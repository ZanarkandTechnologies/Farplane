---
skill: reshape-feasible
date: 2026-08-17
change_type: behavior
owner: skill-creator
status: pass
review_route: reviewer
before_ref: none
after_ref: skills/reshape-feasible/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/reshape-feasible/evals/evals.json
  - skills/reshape-feasible/qa_checklist.md
  - skills/reshape-feasible/examples/one-video-proof/example.md
  - skills/reshape-feasible/examples/one-agency-pilot/example.md
  - skills/reshape-feasible/audits/2026-08-17-forward-test.md
  - .farplane/evals/runs/20260817-091742-reshape-feasible-initial/summary.json
  - .farplane/evals/runs/20260817-095144-reshape-feasible-candidate-suite/summary.json
  - .farplane/evals/runs/20260817-095537-reshape-feasible-bare-goal-rerun/summary.json
  - skills/reshape-feasible/audits/2026-08-17-review.md
  - skills/reshape-feasible/audits/2026-08-17-remediation-review.md
eval_required: yes
eval_result: "pass: candidate suite found 1 failure; the smallest failing case was fixed and rerun A"
eval_baseline_result: deferred
readiness: pass_with_deferred_baseline
eval_blocker: "The Codex comparison runner requires a configured baseline profile; no $CODEX_HOME/*.config.toml profile exists locally, and creating one would be an out-of-scope live configuration change."
rerun_rule: "Fix and rerun the smallest failing eval, reshape_feasible_bare_goal_01, before readiness is reaffirmed."
no_self_improve_reason: "No live user-rated Feasibility Cards or portfolio outcomes exist yet, so a synthetic suite cannot supply an honest personal-utility metric or baseline. Revisit after three real operator uses with recorded outcomes."
---

# Skill Audit

## Change

- Before: Ambitious personal goals required an ad-hoc conversation and often
  felt like one intimidating volume commitment.
- After: `reshape-feasible` produces one Feasibility Card that progresses from
  a large goal through a complete proof to a repeatable unit and a current
  action, with an honest portfolio placement.
- Why: The operator needs a low-pressure route from ambition to self-trust;
  generic interviews and weekly reflection do not own this action boundary.
- Tradeoff accepted: The first version is proposal-only. It formats a supplied
  goal portfolio but does not perform Notion, calendar, task, or goal writes.

## First-Principles Reasoning

- Objective: make a large commitment actable now without pretending the full
  commitment is already feasible.
- Placement logic: Tier 2 because this is a reusable planning interface, not a
  Farplane execution Goal, Notion integration, or weekly-review replacement.
- Expected behavior delta: agents start from a bare goal, produce a complete
  proof plus small action, and use actual proof evidence before scaling.
- Proof needed: static skill validation, a held-out forward test, and independent
  structure review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | SKILL.md contains trigger, signature, default path, gates, and card shape. |
| `reference_load_precision` | pass | No external reference is required for the normal path. |
| `missing_context_rate` | pass | Bare-goal and portfolio-absent behavior are explicit. |
| `noisy_context_rate` | pass | The first load keeps one output and no provider tutorial. |
| `duplicated_instruction_count` | pass | It does not duplicate interview, weekly-review, Notion-write, or Goal execution ownership. |
| `prompt_size_tokens` | pass | The first-load route is concise; the longer calibrated card is an example fixture. |
| `task_success_rate` | pass | Candidate suite exposed 4/5 initial passes; the repaired bare-agency case reran A, while the other four cases already passed A. |
| `review_tas_rate` | pass | Independent reviewer returned TAS-A. |
| `maintenance_locality` | pass | Behavior, QA, evals, and audit are owned by one package. |
| `composition_clarity` | pass | The signature declares one card, gates, routes, state, and failures. |

## Proof Artifacts

- Skill-local evals: `skills/reshape-feasible/evals/evals.json`.
- Positive calibration: `skills/reshape-feasible/examples/one-video-proof/example.md`.
- Structure validation: `python3 skills/skill-maintenance/scripts/check_skills.py --write` passed.
- Forward test: `skills/reshape-feasible/audits/2026-08-17-forward-test.md` passed all target QA guards.
- Runnable eval: `.farplane/evals/runs/20260817-091742-reshape-feasible-initial/summary.json` passed 1/1 selected skill case with an A verdict.
- Candidate suite: `.farplane/evals/runs/20260817-095144-reshape-feasible-candidate-suite/summary.json` initially passed 4/5. The bare-agency case failed on explicit commercial unknowns and the final-action order; its smallest-case rerun passed after remediation.
- Candidate/baseline comparison: deferred because no local `*.config.toml` Codex baseline profile exists. This is recorded rather than fabricated.
- Remediation: the card now labels buyer, market, offer, price, and delivery as commercial unknowns; `Do now` is the final card field; and `examples/one-agency-pilot/example.md` calibrates this branch. `.farplane/evals/runs/20260817-095537-reshape-feasible-bare-goal-rerun/summary.json` reran the exact case and returned A.
- Reviewer receipt: `skills/reshape-feasible/audits/2026-08-17-review.md` returned TAS-A after the example and template-metadata fixes.
- Remediation review: `skills/reshape-feasible/audits/2026-08-17-remediation-review.md` returned TAS-A after the bare-agency failure was fixed and rerun.

## Skill Creator QA

| Check | Verdict | Evidence |
| --- | --- | --- |
| `ownership` | pass | The stable fear-of-commitment trigger is not owned by interview, weekly review, Notion field filling, or Goal execution. |
| `first_load_executable` | pass | `SKILL.md` defines one card, all normal-path gates, five domain steps, and an inline output shape. |
| `metadata_and_references` | pass | Generated registry contains current template markers; both examples have explicit load conditions. |
| `conservative_scaffolding` | pass | No scripts, Notion write path, extra state store, or hidden questionnaire was added. |
| `proof_and_qa` | pass with deferred baseline | Natural eval rows, a full candidate suite, smallest-case repair/rerun, domain QA, structure validation, and independent review exist. Candidate/baseline comparison remains explicitly deferred by the missing local profile. |
| `self_improve` | not_applicable | `no_self_improve_reason` is recorded in frontmatter: no live human-rated outcomes or utility baseline yet. |
- Eval required: yes; no baseline exists because this is a new skill.
- Evidence gaps: live Notion portfolio writes are intentionally out of scope.

## Before Behavior

- Agents could motivate, interview, or decompose an ambition, but no named
  workflow reliably chose an end-to-end first proof and bounded immediate move.

## After Behavior

- `$reshape-feasible` accepts an ambitious personal goal without interrogating
  the user, then returns a portfolio-ready card that can earn trust through
  completed evidence.

## Followups

- Promote to a live Notion write path only after a real portfolio schema and
  explicit write approval establish the required integration contract.
