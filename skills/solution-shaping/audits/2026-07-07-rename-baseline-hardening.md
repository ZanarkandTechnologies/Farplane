---
skill: solution-shaping
change_type: rename-and-eval-hardening
date: 2026-07-07
ticket: TASK-0307
before_ref: skills/complaint-to-mvp/SKILL.md
after_ref: skills/solution-shaping/SKILL.md
evidence:
  - .farplane/evals/runs/20260706-162726-task-0307-solution-shaping/summary.json
  - .farplane/evals/runs/20260706-163044-task-0307-solution-shaping-outreach-rerun/summary.json
  - .farplane/evals/runs/20260706-163135-task-0307-solution-shaping-final/summary.json
  - tickets/TASK-0307/ticket.md
  - tickets/TASK-0307/progress.md
---

# Rename And Baseline Hardening Audit

## Behavior Delta

- Before: `complaint-to-mvp` owned agency-style synthesis from reported problem
  or outreach target to MVP brief, but the name made the workflow sound
  reactive and complaint-driven.
- After: `solution-shaping` owns weak-signal or problem-frame input to a
  realistic solution brief, proof model, and PRD/ticket/Goal handoff.
- Reason: the product-level skill should describe the actual job: shape the
  smallest reviewable solution boundary without defaulting to either the
  requested artifact or an overbuilt platform.

## Edits

- Renamed source package from `skills/complaint-to-mvp/` to
  `skills/solution-shaping/`.
- Updated skill metadata, title, signature, output language, examples, and
  upstream `problem-framing` routes.
- Added sanitized iron fabrication/static-calculator baseline coverage.
- Added paraphrase guard to reduce exact prompt memorization.
- Added negative control where a static calculator is sufficient.
- Added outreach correction-ask and pre-implementation grounding guardrail
  after the first eval run exposed a B verdict.

## Eval Results

| Run | Result | Notes |
| --- | --- | --- |
| `20260706-162726-task-0307-solution-shaping` | 7/8 A, 1 B | New iron baseline, paraphrase, and calculator-negative control all passed. Outreach row missed correction ask and grounding route. |
| `20260706-163044-task-0307-solution-shaping-outreach-rerun` | 1/1 A | Failed outreach row passed after skill guardrail patch. |
| `20260706-163135-task-0307-solution-shaping-final` | 8/8 A | Full current-state suite passed after the patch. |

## Reward-Hacking Review

```text
eval_query_review:
  changed_files:
    - skills/solution-shaping/eval_task.json
  reviewed_rows:
    - solution_shaping_iron_static_calculator_baseline_01
    - solution_shaping_iron_quote_paraphrase_guard_01
    - solution_shaping_static_calculator_sufficient_negative_01
  reviewer: self
  query_spoiler_verdict: pass
  fixes_applied:
    - Kept desired reasoning in reference_points rather than query instructions.
    - Added paraphrase guard so the baseline is not a single memorized prompt.
    - Added negative control so "calculator request" does not always force a quote workflow answer.
  deferrals:
    - Exact original thread was not available through a thread-reading tool in this session.
  remaining_risk:
    - Sanitized baseline may miss details from the original thread until an exported source packet is supplied.
```

## Validation

- `python3 skills/eval/scripts/check_eval_queries.py --root .` -> pass.
- `python3 skills/skill-maintenance/scripts/check_skills.py --write` -> pass.
- `python3 .farplane/evals/run_evals.py run --harness codex --judge-harness codex --skill solution-shaping --label task-0307-solution-shaping-final --max-parallel-tasks 2` -> 8/8 A.
- `farplane install` -> installed `solution-shaping`.
- Live stale installed `complaint-to-mvp` copy was moved to
  `/Users/kenjipcx/.codex/.install-backups/20260707-003515-manual-prune/complaint-to-mvp`.
- Live check: `/Users/kenjipcx/.codex/skills/solution-shaping` exists and
  `/Users/kenjipcx/.codex/skills/complaint-to-mvp` is absent.

## Residual Risk

- `python3 tickets/scripts/check_ticket_metadata.py tickets/TASK-0307/ticket.md`
  cannot be used as a targeted validator because the script validates all
  active tickets and currently reports unrelated `TASK-0308` metadata drift.
  A direct `validate_ticket(Path.cwd() / "tickets/TASK-0307/ticket.md")` check
  passed.
