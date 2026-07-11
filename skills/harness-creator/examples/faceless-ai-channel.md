---
kind: harness-creator-example
status: draft
created_at: 2026-06-14
---

# Faceless AI / Harness Engineering Channel Example

This is the first pilot case for `harness-creator`. It should prove whether a
compact Harness Program can reduce handholding and produce a useful first
`goal-advisor` handoff.

## Harness Program

```harness-program
project "Faceless AI Engineering Channel" {
  values {
    mission: "Teach practical AI and harness engineering so serious builders become more capable"
    operating_principles: [
      "teach from real work, not recycled theory",
      "prefer depth and trust over shallow reach",
      "make claims auditable",
      "turn repeated failures into system improvements"
    ]
    priorities: [
      impact.high,
      loyal_users.high,
      learning.high,
      trust.high,
      money.low,
      efficiency.medium
    ]
    non_tradeoffs: [
      "do not publish unreviewed claims",
      "do not chase virality by lowering technical honesty",
      "do not optimize revenue before usefulness"
    ]
  }

  modes: [channel, academy, lab]

  goal north_star {
    outcome: "Teach practical AI and harness engineering so builders become more capable"
    metric: human_feedback("useful / not useful")
    horizon: "first pilot video"
  }

  axis reach_acquire {
    bet: "Find high-signal AI engineering learners with sharp topic and hook choices"
    kpi: review_metric("hook/title clarity and audience fit")
    evidence: ref("research-baseline.md")
    heartbeat: weekly_interval
  }

  axis activate_first_value {
    bet: "Each video teaches one useful harness engineering move"
    kpi: human_feedback("viewer learned a useful move")
    evidence: ref("operator_feedback")
    heartbeat: weekly_interval
  }

  axis retain_loyalty {
    bet: "A coherent episode ladder gives viewers a reason to return"
    kpi: review_metric("series promise and next-video pull")
    evidence: ref("farplane/metrics.yaml")
    heartbeat: weekly_interval
  }

  axis efficiency_capability {
    bet: "Reuse Farplane docs, tickets, and video templates to reduce cycle time"
    kpi: learning_metric("time from idea to reviewed draft")
    evidence: ref("local Farplane corpus")
    heartbeat: weekly_interval
  }

  axis risk_trust {
    bet: "No fake authority, no misleading claims, no unreviewed publishing"
    kpi: review_metric("trust and claim accuracy")
    evidence: ref("review")
    heartbeat: weekly_interval
  }

  system publishing_gate {
    status: ready
    evidence: ref("operator approval requirement")
    action: use_existing("explicit approval before publish")
  }

  system analytics {
    status: missing_instrumentation
    evidence: ref("no YouTube metrics before publish")
    action: ticket(youtube_analytics_export)
  }

  skill youtube_retention_metrics {
    status: needs_access
    requires: [youtube_analytics_export]
    use: "read retention, watch time, CTR, saves, comments, and returning viewer signals"
  }

  ticket youtube_analytics_export {
    type: unblock
    human_step: "Connect read-only analytics access or provide a recurring export after publishing is approved"
    why: "Market metrics cannot guide content strategy before a data source exists"
    enables: [youtube_retention_metrics]
    fallback: human_feedback("Kenji labels pilot scripts and drafts until market metrics exist")
    gates: [no_account_changes, no_publish]
  }

  skill video_production {
    status: ready
    use: "script, storyboard, and production planning"
  }

  skill goal_advisor {
    status: ready
    use: "compile the first research/episode-selection milestone"
  }

  heartbeat rhythm_update {
    first: rank_day_range_lanes
    optional: ticket_drainer
    gates: [no_publish, no_spend, no_account_changes]
  }

  heartbeat weekly_interval {
    first: grouped_jobs_with_report_cache
    jobs: [update_external_context, update_memory, skill_hardening, skill_refinement, update_strategy, quarterly_plan, annual_review]
    skills: [feed_scout, update_memory, update_strategy, skill_maintenance, goal_advisor, review]
    delegate: delegate(ref("project-harness.md"), "refresh channel strategy and skill upkeep", skills=[weekly_strategy_analysis, skill_maintenance])
    gates: [review_before_external_side_effects]
  }

  milestone first_episode_selection {
    task: "Research and choose the first pilot episode"
    route: goal_advisor
    metric: review_metric("episode choice is useful, differentiated, and produceable")
    files: ["project-harness.md", "research-baseline.md"]
    gates: [no_publish, no_spend]
    stop_when: "first episode handoff is ready for review"
  }
}
```

## Evidence

- `research_refs:` use `research:parity` for AI education, faceless
  documentary, and technical explainer channel workflows.
- `competitor_refs:` use `research:competitor` after the first candidate set is
  chosen.
- `local_refs:` Farplane docs, skills, tickets, examples, and prior artifacts
  are source material.
- `operator_inputs:` Kenji's taste and usefulness judgment are the first honest
  metric.

## Assumptions

- The first loop optimizes learning and trust before money.
- Publishing, paid media generation, spend, account changes, and YouTube
  analytics setup stay gated until approved.
- Market metrics are unavailable before publishing, so early metrics use review
  and human feedback.
- Analytics access is represented as a skill capability plus a `ticket` with
  `type: unblock`, not as a separate external-IO abstraction.

## Goal Advisor Handoff

- `task:` Research and choose the first pilot episode.
- `trigger:` active_goal or heartbeat, depending on operator timing.
- `metric_provider:` review_metric.
- `side_effect_gates:` no publish, no spend, no account changes.
- `stop_conditions:` episode handoff ready, or blocked by missing operator
  decision.
