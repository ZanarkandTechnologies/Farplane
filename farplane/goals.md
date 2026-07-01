---
kind: project-goals
status: active
project: Farplane
created_at: 2026-06-15
updated_at: 2026-07-01
framework_template_version: "0.4.1"
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

## Goals

Goal axes own their SMART goals directly. Each SMART goal names stable KPI keys
and gives the interval agent an update hint. KPI names stay stable; content,
ticket, or post IDs belong in metric snapshot item breakdowns.

```yaml
goals:
  validated_self_improvement:
    question: Can Farplane complete meaningful improvement cycles with less human intervention?
    evidence_hints:
      - validated cycles
      - accepted harness improvements
      - intervention minutes
      - accepted agent-hours
      - skill backpropagation events
    smart_goals:
      - id: autonomous_improvement_q3
        target: 20 accepted harness improvements with less intervention per accepted change by 2026-09-30
        kpis:
          - accepted_output_events
          - accepted_harness_improvements
        update_hint: >
          Derive readings from the Pulse reward ledger. Record gaps for
          intervention minutes, accepted agent-hours, or skill backpropagation
          events until their providers exist.

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
          - proof_closure_events
          - latest_eval_pass_rate
        update_hint: >
          Derive available proof readings from rewards, eval summaries, ticket
          Done/Proof blocks, and review receipts. Record feedback gaps for
          review pass rate or false-completion tracking until providers exist.

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
          - ready_unclaimed_ticket_count
          - stale_claim_count
          - pulse_execute_count
          - pulse_request_planning_count
        update_hint: >
          Derive readings from the ticket board and Pulse decision ledger.
          Treat negative daily diffs on stale or ready-unclaimed counts as
          useful progress, not a source gap.
      - id: budget_accountability_weekly
        target: Every active project records a weekly contribution mode, expected reward, and runway decision
        kpis:
          - weekly_runway_review_count
          - projects_with_runway_decisions
        update_hint: >
          Derive readings from weekly interval reports and ops-memory active
          project sections. Treat missing spend precision as acceptable early;
          record source gaps only when active projects lack contribution mode,
          expected reward, or continue/narrow/pause/instrument/stop decisions.

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
          - x_followers
          - instagram_followers
          - x_views
          - instagram_views
          - x_likes
          - instagram_likes
          - x_retention_score
          - instagram_retention_score
          - posts_published
        update_hint: >
          Use x-account, instagram-account, social-content, and ops-memory
          tracked content when available. Aggregate relevant content item
          readings into stable KPI keys. Record missing providers, unavailable
          retention, or missing qualified-reply tracking as source gaps.

  framework_adoption:
    question: Can more project types initialize into Farplane and run a first measured loop?
    evidence_hints:
      - initialized projects with config
      - goals
      - tickets
      - automations
      - first Goal Advisor handoff
    smart_goals:
      - id: framework_adoption_q3
        target: 3 project types initialized with goals, tickets, automations, and first Goal Advisor handoff by 2026-09-30
        kpis:
          - initialized_project_count
          - first_goal_handoff_count
        update_hint: >
          Record a feedback gap until framework adoption events have a provider
          such as an init-advisor ledger, project registry, or manual snapshot.
```

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
