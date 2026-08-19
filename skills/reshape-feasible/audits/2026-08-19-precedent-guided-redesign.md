---
skill: reshape-feasible
date: 2026-08-19
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/reshape-feasible/audits/2026-08-17-initial-skill.md
after_ref: skills/reshape-feasible/SKILL.md
reasoning_basis: eval
proof_artifacts:
  - .farplane/evals/runs/20260819-061103-reshape-feasible-precedent-baseline/summary.json
  - .farplane/evals/runs/20260819-061654-reshape-feasible-precedent-candidate/summary.json
  - .farplane/evals/runs/20260819-062009-reshape-feasible-precedent-repair/summary.json
  - .farplane/evals/runs/20260819-062123-reshape-feasible-precedent-final/summary.json
  - skills/reshape-feasible/audits/2026-08-19-precedent-guided-review.md
eval_required: yes
no_self_improve_reason: "This correction has one accepted precedent but no repeated live focused-mission outcomes from which to define an honest personal-utility metric. Revisit after three real operator uses with recorded outcomes."
---

# Reshape Feasible Precedent-Guided Redesign Audit

## Change

- Before: The skill returned a fixed Feasibility Card containing known/assumed
  facts, a Trust Ladder, floor/promise/stretch levels, portfolio placement, and
  a small first action.
- After: The skill preserves the large ambition as direction, removes it from
  the active horizon, selects one meaningful result for a focused push, and
  ends with one direct action. An operator-accepted precedent and contrasting
  failure calibrate the response.
- Why: Operator feedback showed that detailed decomposition preserved the felt
  workload. The desired intervention is concentrated attention on one
  substantial near-term result, such as one signed, paid `$10,000` customer.
- Tradeoff accepted: The skill provides less comprehensive planning in exchange
  for lower cognitive load and stronger immediate agency. Full planning remains
  available through other goal and planning surfaces.

## First-Principles Reasoning

- Objective: Make an intimidating ambition easier to act on without arguing it
  down or pretending the remaining work has disappeared.
- Placement logic: `reshape-feasible` already owns this stable trigger. The
  change belongs in its `SKILL.md`, accepted example, evals, and interface copy;
  no global prompt, agent role, hook, script, or new skill is required.
- Expected behavior delta: Replace card construction and whole-goal modeling
  with precedent-guided horizon collapse, one meaningful focused mission, and
  one immediate move.
- Proof needed: Same-suite baseline/candidate evidence, anti-spoiler checks,
  skill-system validation, installed-copy parity, and independent review.

## Lean Receipt

```yaml
target: reshape-feasible behavior correction
current_need: accepted output shape conflicts with the card-first contract
rung: reuse_local
evidence:
  - existing reshape-feasible package owns the trigger
  - existing skill-local eval runner supports baseline and candidate runs
  - accepted precedent supplies the missing behavioral target
smallest_next_action: replace only the owner-local contract, precedent, evals, and interface copy
proof_preserved: same five natural prompts and judge contract run before and after mutation
review_route: review:skill-contract
```

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` declares trigger, signature, gates, five-step normal path, and output. |
| `reference_load_precision` | pass | Todo 1 names exactly when and why to load `examples/one-week-mission/example.md`. |
| `missing_context_rate` | pass | Default horizon, evidence reuse, safety/capacity boundary, portfolio behavior, and no-question-first behavior are explicit. |
| `noisy_context_rate` | pass | The fixed card schema and separate runtime QA sidecar were removed; the longer accepted case is owner-local and precisely loaded. |
| `duplicated_instruction_count` | pass | Transfer invariants live once in `SKILL.md`; the example explains decisions and incidental details rather than restating the workflow. |
| `prompt_size_tokens` | pass | First load no longer includes a card template or mandatory QA sidecar; accepted-case detail stays in one example. |
| `task_success_rate` | pass | Same-suite A pass rate moved from 2/5 to 5/5; the two smallest failing candidate cases passed after targeted repair. |
| `review_tas_rate` | pass | Independent re-review returned TAS-A after installed parity and registry-boundary remediation. |
| `maintenance_locality` | pass | Contract, precedent, evals, interface copy, and audit remain under `skills/reshape-feasible/`. |
| `composition_clarity` | pass | Signature declares one `focused_mission`, reads/writes, gates, routes, failures, and external-state boundary. |

## Structure Receipt

```text
first_load_review:
  authored_file_structure: one executable SKILL plus one annotated precedent
  kept_in_skill: trigger, signature, horizon rule, five-step workflow, four invariants, failures, output
  moved_to_reference: accepted artifact, decisions, evidence, incidental details, contrasting failure
  deleted_as_duplicate_or_rationale: Feasibility Card schema and separate runtime QA checklist
  extra_sections_kept_with_reason: none
  proof_surface_fit: variable behavior -> skill-local evals; judgment -> reviewer
  task_case_quality: one canonical regression plus four distinct transfer cases
  anti_cheat_case_design: natural prompts; expected behavior remains outside prompts
  qa_preflight_loaded: not applicable; no target QA sidecar remains
  qa_finish_independence: pass; native reviewer returned TAS-A
  qa_gotcha_deduplication: not applicable
  project_specific_context_isolation: pass; precedent is sanitized and transferable
  low_value_prose_scan: pass
  golden_calibration_independence: candidate runs use the precedent; reviewer receives artifacts and held-out results, not scratch reasoning
  lean_owner_reuse: pass
  verdict: pass
```

## Eval Receipt

```text
eval_query_review:
  changed_files: skills/reshape-feasible/evals/evals.json
  reviewed_rows: 5
  reviewer: reviewer
  query_spoiler_verdict: pass
  fixes_applied: none; check_eval_queries.py passed
  deferrals: none
  remaining_risk: none at the current behavior-readiness boundary

behavior_eval_review:
  suite: skills/reshape-feasible/evals/evals.json
  baseline_artifact: .farplane/evals/runs/20260819-061103-reshape-feasible-precedent-baseline/summary.json
  candidate_artifact: .farplane/evals/runs/20260819-062123-reshape-feasible-precedent-final/summary.json
  comparison_artifact: this audit
  promotion_decision: accept
```

## Proof Artifacts

- Baseline: 2 A, 1 B, 2 C; `pass_rate: 0.4`.
- Initial candidate: 3 A, 2 B; exposed the missing `$10,000` focus target and
  incomplete product-use definition.
- Smallest-case repair: 2/2 A.
- Final suite: 5/5 A; `pass_rate: 1.0`.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  passed, including JSON, registry, surface budget, capability, eval-query, and
  documentation-reference checks.
- Installed parity: selected-skill install passed; recursive source/live diff
  returned no differences and the removed QA sidecar is absent from the live
  package.
- Registry ownership boundary: the generated registry was already dirty with
  unrelated user-owned work before this task. This task owns only the accurate
  `reshape-feasible` row; generator check passes for the current source tree,
  and unrelated rows were not reverted or claimed.
- Reviewer receipt: initial TAS-C blockers were remediated; independent
  re-review returned TAS-A with no hard-gate failures.
- Eval required: yes; complete pending independent review.
- Evidence gaps: No three-use live outcome set exists for `self-improve`.

## Before Behavior

- The exact revenue case produced one customer without the accepted `$10,000`
  threshold and rendered a formal card.
- A progressed commercial case resumed total-goal arithmetic and stopped before
  a direct buyer action.
- A video case could stop at outlining rather than publication progress.

## After Behavior

- The exact revenue case keeps `$1 million` as direction and makes one signed,
  paid `$10,000` customer the seven-day mission.
- Content, product, progressed-commercial, and capacity-bound cases transfer
  the pattern without copying the revenue facts.
- Every passing final answer ends with a direct move toward the meaningful
  result and avoids reconstructing the full goal.

## Followups

- Revisit `self-improve` only after three real operator uses have recorded the
  selected mission, whether it felt actionable, and what happened by the end of
  the focus horizon.
