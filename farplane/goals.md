---
kind: project-goals
status: active
project: Farplane
created_at: 2026-06-15
updated_at: 2026-06-30
framework_template_version: "0.3.0"
owner: horizon-advisor
source: horizon-advisor
refs:
  - farplane/harness.md
  - farplane/products.md
  - farplane/automations.md
  - docs/fundamentals/harness-algebra.md
  - skills/horizon-advisor/SKILL.md
  - skills/goal-advisor/SKILL.md
---

# Farplane Goals

## North Star

Farplane becomes the standard way researchers and builders create harnesses
that run longer, improve from evidence, and produce higher-quality results with
less human intervention.

## Value Function

| Direction | Variables |
| --- | --- |
| Maximize | meaningful long-running output; accepted agent output; quality; validated improvement; reliability; reusable behavior; auditability; context-isolated execution |
| Minimize | human intervention; false completion; agent churn; coordination cost; ungrounded claims; brittle state loss; context bleed; source gaps; skill-backpropagation delay |
| Preserve | user goal satisfaction; groundedness; correctness; safety; proof; operator control; context isolation |

## KPI Axes

| Axis | Question | Signal |
| --- | --- | --- |
| validated_self_improvement | Can Farplane complete meaningful improvement cycles with less human intervention? | validated cycles, accepted harness improvements, intervention minutes, accepted agent-hours, skill backpropagation events |
| quality_and_proof | Do long-running agents preserve quality, proof, and operator control? | sufficient proof, validator pass rate, false completion incidents, proof closure rate |
| project_control | Can Farplane control dynamic projects with their own completion criteria and intervention budgets? | active projects with goals/proof state, useful interval reports, projects advanced without human unblock |
| distribution_from_evidence | Can Farplane turn real harness evidence into audience, users, and research authority? | evidence-backed content shipped, qualified attention, serious conversations, pilot users |
| framework_adoption | Can more project types initialize into Farplane and run a first measured loop? | initialized projects with config, goals, tickets, automations, and first Goal Advisor handoff |

## Tracked KPIs

This table is the project-local KPI registry for interval snapshots and the
Farplane UI cockpit. `aggregation=point` means the latest observed value is the
chart value for that day. `aggregation=daily` means the value belongs to that
day; when `cumulative=true`, the UI snapshot also derives a running total and
target-hit marker.

| Metric | Label | Axis | Product | Source | Aggregation | Cumulative | Target | Unit | Display |
| --- | --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| x_followers | X followers | distribution_from_evidence | distribution | manual_x_account | point | false | 1000 | followers | line |
| instagram_followers | Instagram followers | distribution_from_evidence | distribution | manual_instagram_account | point | false | 1000 | followers | line |
| x_views | X views | distribution_from_evidence | distribution | manual_x_account | daily | true | 100000 | views | bar_plus_cumulative |
| instagram_views | Instagram views | distribution_from_evidence | distribution | manual_instagram_account | daily | true | 100000 | views | bar_plus_cumulative |
| x_likes | X likes | distribution_from_evidence | distribution | manual_x_account | daily | true | 10000 | likes | bar_plus_cumulative |
| instagram_likes | Instagram likes | distribution_from_evidence | distribution | manual_instagram_account | daily | true | 10000 | likes | bar_plus_cumulative |
| x_retention_score | X retention score | distribution_from_evidence | distribution | manual_x_account | point | false | 40 | percent | line |
| instagram_retention_score | Instagram retention score | distribution_from_evidence | distribution | manual_instagram_account | point | false | 40 | percent | line |
| posts_published | Posts published | distribution_from_evidence | distribution | manual_social_posts | daily | true | 30 | posts | bar_plus_cumulative |
| accepted_output_events | Accepted output events | validated_self_improvement | productization | pulse_reward_ledger | daily | true | 50 | events | bar_plus_cumulative |
| accepted_harness_improvements | Accepted harness improvements | validated_self_improvement | productization | pulse_reward_ledger | daily | true | 20 | events | bar_plus_cumulative |
| proof_closure_events | Proof closure events | quality_and_proof | productization | pulse_reward_ledger | daily | true | 20 | events | bar_plus_cumulative |
| latest_eval_pass_rate | Latest eval pass rate | quality_and_proof | experiments | eval_summary_index | point | false | 1.0 | ratio | line |
| ready_unclaimed_ticket_count | Ready unclaimed tickets | project_control | productization | ticket_board | point | false | 3 | tickets | line |
| stale_claim_count | Stale claims | project_control | maintenance | ticket_board | point | false |  | tickets | line |
| pulse_execute_count | Pulse executions | project_control | maintenance | pulse_decision_ledger | daily | true | 10 | beats | bar_plus_cumulative |
| pulse_request_planning_count | Pulse planning requests | project_control | maintenance | pulse_decision_ledger | daily | true |  | beats | bar_plus_cumulative |

## Current Bets

| Bet | Horizon | Output | Proof Signal | Owner |
| --- | --- | --- | --- | --- |
| framework_standardization | 1 week | clear tracked config split for harness, goals, products, automation prompts, bindings, tickets, and reports | project-file validators and docs make ownership obvious | harness-creator |
| goal_advisor_program_grammar | 1 week | clear Horizon Advisor to Goal Advisor boundary | agents do not duplicate strategy and execution roles | horizon-advisor |
| low_intervention_experiment_engine | quarter | experiment and ablation reports that improve Farplane with explicit intervention/proof accounting | accepted improvements with baseline, metric, proof, and accept/reject decision | optimize-harness |
| evidence_distribution_engine | quarter | evidence-backed content and demos from accepted experiments | qualified attention, serious conversations, pilot users | social-content |
| pulse_interval_framework_standard | 2 weeks | reusable Pulse plus Daily/Weekly Interval automation standard | a project initializes the preset without custom files | automation-advisor |
| skill_memory_hierarchy | 2 weeks | local lessons and skill findings roll up without losing project context | parent reports summarize child state without reading every child report | skill-maintenance |

## Current Milestone

Make Farplane's horizon layer explicit enough to optimize meaningful
long-running autonomous improvement per human intervention hour, while
preserving quality, proof, operator control, and context isolation.

## Holds

- Do not add hidden daemon behavior.
- Do not store secrets in tracked config.
- Do not make Notion canonical until the project explicitly opts in.
- Do not execute broad leaf tickets from interval automations.
- Do not split projects into child tickets unless there is a real execution,
  unblock, review, dependency, approval, or proof boundary.
- Do not claim self-improvement without baseline, metric provider, proof
  surface, intervention accounting, and accept/reject decision.
- Do not optimize distribution metrics independently from evidence-backed
  harness improvement.
