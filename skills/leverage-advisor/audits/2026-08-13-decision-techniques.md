---
skill: leverage-advisor
date: 2026-08-13
change_type: source_upgrade
owner: skill-maintenance
status: pass
review_route: reviewer
reasoning_basis: book_to_skill + focused_evals
source_mode: mixed
proof_artifacts:
  - .farplane/evals/runs/20260813-075219-task0433-decision-techniques/summary.json
  - .farplane/evals/runs/20260813-075532-task0433-precommit-repair/summary.json
  - .farplane/evals/runs/20260813-080514-task0433-final-targeted/summary.json
  - tickets/TASK-0433/ticket.md
  - tickets/TASK-0433/artifacts/review/2026-08-13-review.md
eval_required: yes
---

# Source-attributed decision techniques

## Change

> **Before:** Leverage Advisor ranked a grounded frontier and chose a cheap
> falsifier, but it did not require a bottleneck diagnosis, pre-outcome bet
> record, or proof that the chosen observation could change the decision.
>
> **After:** The advisor requires a Rumelt-style diagnosis/policy/coherent
> move, a Duke-style thesis/confidence/downside/falsifier, and a Hubbard-style
> decision-changing test. It explicitly compares the winning move with
> `report_now`, `request_feedback`, and `stop` before spending more budget.

## Source Packet And Decisions

| Source | Confidence | Transferable method | Decision |
| --- | --- | --- | --- |
| [Richard Rumelt, *Good Strategy/Bad Strategy*](https://www.penguinrandomhouse.com/books/208668/good-strategy-bad-strategy-by-richard-rumelt/) | high | Diagnose the obstacle, choose a guiding policy, then take coherent action. | adopt |
| [Annie Duke, *Thinking in Bets*](https://www.annieduke.com/thinking-in-bets-2/) | high | Pre-commit a thesis and do not equate outcome with decision quality. | adapt |
| [Douglas Hubbard, *How to Measure Anything*](https://onlinelibrary.wiley.com/doi/book/10.1002/9781118983836) and [value-of-information method](https://onlinelibrary.wiley.com/doi/abs/10.1002/9781118983836.ch7) | high | Prefer the smallest observation that can alter a decision. | adopt |

Rejected: numeric opportunity scoring, author voice/prose, a generic book
summary, and private personal-opportunity criteria. The skill keeps ordinal
judgement and accepts `uncalibrated` when evidence cannot support probability.

## Proof

| Check | Result | Evidence |
| --- | --- | --- |
| JSON, links, generated registry, template, surface budget, and eval-query lint | pass | `python3 skills/skill-maintenance/scripts/check_skills.py --write` |
| Non-decisive measurement case | A | `20260813-075219-task0433-decision-techniques` |
| Pre-outcome decision case, first attempt | B: outside-option comparison implicit | `20260813-075219-task0433-decision-techniques` |
| Repair: explicit outside-option comparison in workflow, program, and output | applied | `skills/leverage-advisor/SKILL.md` |
| Pre-outcome decision case, repaired | A, 5/5 assertions | `20260813-075532-task0433-precommit-repair` |
| Broader regression | surfaced output omissions, then targeted repair | `20260813-075839-task0433-full-leverage-regression` |
| Final targeted suite: source gap, pre-outcome bet, non-decisive measurement | A, 3/3 | `20260813-080514-task0433-final-targeted` |
| Independent review | TAS-A, pass, no hard gates | `tickets/TASK-0433/artifacts/review/2026-08-13-review.md` |

## Structure Review

- Kept in `SKILL.md`: every-invocation gates, source names, explicit outside
  option rendering, and output fields.
- Moved to `references/decision-techniques.md`: source links, source-method
  detail, decision-record template, and adoption limits.
- Kept in QA: reusable runtime checks for diagnosis, pre-outcome reasoning, and
  decisive evidence.
- Kept in evals: two blind cases; their queries omit author and framework names.
- Not changed: execution, Goal compilation, ticket lifecycle, scoring method,
  and personal/project-specific criteria.

## Remaining Risk

The final three-case targeted suite proves the source-gap, bet, and
decision-changing measurement behavior, not that every real-world opportunity
is correctly ranked. The seven-case broad regression exposed pre-existing
coverage gaps outside this source-method delta; its results are recorded rather
than hidden and should be handled by a separate reliability-hardening ticket.
