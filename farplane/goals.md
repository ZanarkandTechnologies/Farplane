---
kind: project-goals
status: active
project: Farplane
created_at: 2026-06-15
updated_at: 2026-07-02
framework_template_version: "0.4.3"
owner: horizon-advisor
source: horizon-advisor
refs:
  - farplane/harness.md
  - farplane/products.md
  - farplane/bindings.md
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

## Goals

Goal axes own strategic targets and interpretation. Each SMART goal lists KPI
target pairs so dashboards can parse target-hit status. Metric units, chart
shape, pinned status, sources, commands, skills, and update hints live in
`farplane/bindings.md` metric recipes.

```yaml
goals:
  validated_self_improvement:
    question: Can Farplane complete meaningful improvement cycles with less human intervention?
    evidence_hints:
    - validated cycles
    - accepted harness improvements
    - human attention minutes
    - autonomous worker elapsed minutes
    - skill backpropagation events
    smart_goals:
    - id: autonomous_improvement_q3
      target: >-
        20 accepted harness improvements and more autonomous worker time than human thread attention by 2026-09-30
      kpis:
      - id: accepted_harness_improvements
        target: 20
        direction: above
      - id: accepted_evidence_cycles
        target: 20
        direction: above
      - id: auto_time_ratio
        target: 1
        direction: above
      - id: ticket_intervention_turn_count
        target: 0
        direction: below
      - id: auto_completion_rate
        target: 0.8
        direction: above
      interpretation: >
        The main autonomy claim is stronger when accepted improvements and evidence cycles rise while auto_time_ratio exceeds 1 and post-start ticket intervention turns fall. Treat turn-count intervention metrics as supporting KPIs until ticket/thread association coverage is reliable.
  quality_and_proof:
    question: Do long-running agents preserve quality, proof, and operator control?
    evidence_hints:
    - sufficient proof
    - validator pass rate
    - false completion incidents
    - proof closure rate
    smart_goals:
    - id: proof_quality_q3
      target: 90% of completed material tickets have sufficient proof and review evidence by 2026-09-30
      kpis:
      - id: latest_eval_pass_rate
        target: 0.9
        direction: above
      interpretation: >
        Quality is improving when proof closure and eval pass rate hold while issue/PR backlog stays bounded. Missing review-pass-rate providers should become source gaps or instrumentation tickets, not fake counts.
  project_control:
    question: Can Farplane control dynamic projects with their own completion criteria and intervention budgets?
    evidence_hints:
    - active projects with goals and proof state
    - useful interval reports
    - projects advanced without human unblock
    smart_goals:
    - id: project_control_q3
      target: Keep ready unclaimed tickets under 3 while completing 10 Pulse execution cycles by 2026-09-30
      kpis:
      - id: ready_unclaimed_ticket_count
        target: 3
        direction: below
      interpretation: >
        Project control is improving when Pulse keeps executing or requesting useful planning, stale and ready-unclaimed tickets stay low, and more accepted work is handled by autonomous workers.
  distribution_from_evidence:
    question: Can Farplane turn real harness evidence into audience, users, and research authority?
    evidence_hints:
    - evidence-backed content shipped
    - qualified attention
    - serious conversations
    - pilot users
    smart_goals:
    - id: evidence_distribution_q3
      target: 100000 evidence-backed content views by 2026-09-30
      kpis:
      - id: evidence_distribution_reach
        target: 100000
        direction: above
      interpretation: >
        Distribution matters only when it is tied to real harness evidence. Platform-specific metrics explain the rollup; missing retention or qualified-reply access should be recorded as source gaps.
```

## Current Bets

| Bet | Horizon | Output | Proof Signal | Owner |
| --- | --- | --- | --- | --- |
| framework_standardization | 1 week | clear tracked config split for harness, products, goals, bindings, tickets, and reports | project-file validators and docs make ownership obvious | harness-creator |
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
- Do not claim self-improvement without baseline, metric observation, proof
  surface, intervention accounting, and accept/reject decision.
- Do not optimize distribution metrics independently from evidence-backed
  harness improvement.
