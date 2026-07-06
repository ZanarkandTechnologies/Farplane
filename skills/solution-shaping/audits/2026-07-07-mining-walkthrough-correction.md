---
skill: solution-shaping
change_type: harden-skill
date: 2026-07-07
ticket: TASK-0307
source_thread: 019f30b7-d8fc-7231-874d-4c1464eba30b
evidence:
  - .farplane/evals/runs/20260706-165737-task-0307-mining-walkthrough-hardening/summary.json
  - .farplane/evals/runs/20260706-170453-task-0307-outreach-route-hardening/summary.json
  - .farplane/evals/runs/20260706-170552-task-0307-solution-shaping-corrected-final/tasks
  - .farplane/evals/runs/20260706-165854-task-0307-solution-shaping-mining-final/summary.json
---

# Mining Walkthrough Correction Audit

## Behavior Delta

- Before: the skill could turn the mining complaint into a plausible set of
  modules or a generic mineability/prospectivity workbench. It did not strongly
  preserve the end-of-thread solution: one ERP-adjacent mine-to-margin planning
  layer with a concrete operational walkthrough.
- After: the skill requires operational MVPs to include a walkthrough, and it
  specifically hardens mine-to-margin and production-planning cases around:
  material lots, route options, resource calendars, buyer or demand windows,
  price scenarios, margin or service outcomes, and rebalance.
- After: ERP-adjacent planning briefs must state that the MVP sits beside ERP,
  APS, GIS, mine-planning, or accounting systems rather than replacing systems
  of record.
- After: mine-to-margin and production-planning proof must include the demo
  trio: normal campaign plan, labor/resource shortage rebalance, and price or
  premium spike.

## Why The Earlier Answer Was Wrong

The three mining prompts looked separable:

- 60% vs 65% indexed-price comparison.
- Sabah prospectivity mapping with drone/geospatial data.
- Mineability and overburden judgment dependent on a senior geologist.

The actual product insight from the source thread was that these are not three
standalone products. They are inputs into one planning decision:

```text
material lots -> processing routes -> resources -> buyers/time windows ->
price scenarios -> margin/risk -> reviewed plan -> actuals feedback
```

The wrong answer stopped at modules. The correct MVP explains how an operator
runs the planning loop, what the system calculates, what it allocates, where it
shows bottlenecks, and how actuals update the next run.

## Edits

- Added an explicit ERP-adjacent system-boundary todo.
- Added a production-planning proof-scenario todo requiring normal campaign,
  shortage rebalance, and price/premium spike.
- Expanded the mining operational-loop example with beside-ERP positioning,
  lot splitting, capacity consumption, flexible inventory, and actuals feedback.
- Added a gotcha against omitting the operational demo trio.
- Added `Pre-implementation route` to the solution-brief template and reinforced
  inferred outreach routing after a full-suite run exposed a separate outreach
  near miss.

## Eval Results

| Run | Result | Notes |
| --- | --- | --- |
| `20260706-165737-task-0307-mining-walkthrough-hardening` | 1/1 A | Mining regression passed with explicit mine-to-margin planner, ERP-adjacent boundary, walkthrough, and demo trio. |
| `20260706-165854-task-0307-solution-shaping-mining-final` | 8/9 A, 1 B | Mining passed; outreach regressed because the answer missed explicit pre-implementation route. |
| `20260706-170453-task-0307-outreach-route-hardening` | 1/1 A | Outreach route regression passed after adding visible pre-implementation handoff. |
| `20260706-170552-task-0307-solution-shaping-corrected-final` | 8 judged rows all A; mining judge incomplete | Non-mining judged rows all passed, including outreach. The mining agent answer was written and had the corrected shape, but the runner wedged before writing the mining judge artifact. Focused mining proof above remains the accepted mining verdict. |

## Reward-Hacking Review

```text
query_spoiler_verdict: pass
reason:
  - The mining eval query names the real client problems but does not name the
    mine-to-margin planner, ERP-adjacent decision layer, or proof demo trio.
  - The desired reasoning remains in reference points and skill behavior, not
    leaked into the user-facing query.
  - The suite still includes negative controls where a static calculator is
    sufficient and where outreach must stay pre-implementation.
remaining_risk:
  - The source thread is private local context, so the eval uses a sanitized
    hardcase rather than raw transcript.
  - The final all-rows run wedged on one mining judge task; accepted proof is
    composed from the focused mining A plus corrected final non-mining A rows.
```

## Validation

- `python3 skills/eval/scripts/check_eval_queries.py --root .` -> pass.
- `python3 -m json.tool skills/solution-shaping/eval_task.json` -> pass.
- `python3 skills/skill-maintenance/scripts/check_skills.py --write` -> pass.
- `farplane install` -> pass; live `~/.codex/skills/solution-shaping/SKILL.md`
  contains the ERP-adjacent, demo-trio, and pre-implementation route guardrails.

## QA Checklist Notes

```text
line_count_before: 209 before mining correction, 222 after mining patch, 228 after outreach route patch
line_count_after: 228
first_load_sufficiency: pass
reference_load_precision: pass; no new references added
noisy_context_rate: pass; details are short first-load gates needed to prevent the observed miss
maintenance_locality: pass; runtime behavior lives in SKILL.md, reusable proof rows live in eval_task.json
proof_surface_fit: pass; behavior is variable AI output, so proof is skill-local Codex eval
audit_verdict: pass
```
