---
skill: interval-update
date: 2026-08-20
change_type: behavior
owner: interval-update
status: superseded
superseded_by: 2026-08-20-weekly-draft-promotion-lifecycle.md
review_route: reviewer
before_ref: installed-skill-baseline
after_ref: working-tree
reasoning_basis: operator_direction
proof_artifacts:
  - /Users/kenjipcx/.farplane/evals/runs/20260819T212346Z-interval-knowledge-candidate-vs-installed-rerun/summary.json
  - /Users/kenjipcx/.farplane/evals/runs/20260819T213426Z-interval-weekly-candidate-vs-installed-final2/summary.json
eval_required: yes
---

# Interval Reporting And Knowledge Parent Audit

> Superseded on 2026-08-20 by
> `2026-08-20-weekly-draft-promotion-lifecycle.md`. This receipt preserves the
> rejected eager-Daily-write intermediate design; it is not the active
> Interval contract.

## Change

- Before: Interval owned reporting, highlights, and qualified ticket deltas;
  durable knowledge had no scheduled owner.
- After: one bounded Interval evidence bundle feeds reporting and knowledge
  phases. Daily applies incremental owner-routed deltas. Weekly consolidates
  Daily receipts and showcases applied artifacts.
- Tradeoff: local knowledge writes broaden Interval's mutation surface, so only
  patch-sized, source-backed, unambiguous changes may apply and every route
  keeps its own validation and review gates.

## Owner Routing

- reusable operational SOP -> `skill-maintenance` -> owning skill;
- project explanation/runbook/article -> `doc-advisor` -> owning project doc;
- sourced entity fact/relationship -> `manage-wiki` -> Entity Markdown and
  generated projections.

The report stages source locators, destinations, and diffs before mutation. A
sibling immutable receipt records observed results afterward; no mutable global
memory ledger was added.

## Eval Comparison

| Case | Installed baseline | Candidate | Verdict |
| --- | --- | --- | --- |
| Daily owner routing and receipt | fail | pass, 0.975 | accept |
| Weekly receipt consolidation/showcase | fail | pass, 1.0 | accept |

Both comparisons used the same GPT-5.6 Luna low-reasoning Promptfoo profile,
task, grader, sandbox, approvals, network policy, and installed baseline.

## Deterministic Proof

- Skill and automation entrypoints are 163 and 147 lines, below the 200-line
  hard envelope.
- `check_skills.py --write` passed all skill, registry, template, todo-tier,
  surface-budget, eval-query, doc-reference, and compile checks.
- Feature/system registry validation passed for 14 systems and 38 features.
- Farplane project-file conventions, JSON/TOML parsing, and 13 lifecycle graph
  tests passed.

Independent reviewer verdict: `TAS-A`, pass, with no blocking issue or hard
gate failure.
