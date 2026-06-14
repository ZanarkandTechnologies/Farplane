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
  values: [
    impact.high,
    loyal_users.high,
    learning.high,
    trust.high,
    money.low,
    efficiency.medium
  ]

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
    heartbeat: weekly_strategy_refresh
  }

  axis activate_first_value {
    bet: "Each video teaches one useful harness engineering move"
    kpi: human_feedback("viewer learned a useful move")
    evidence: ref("operator_feedback")
    heartbeat: weekly_strategy_refresh
  }

  axis retain_loyalty {
    bet: "A coherent episode ladder gives viewers a reason to return"
    kpi: review_metric("series promise and next-video pull")
    evidence: ref("harness-portfolio.md")
    heartbeat: weekly_strategy_refresh
  }

  axis efficiency_capability {
    bet: "Reuse Farplane docs, tickets, and video templates to reduce cycle time"
    kpi: learning_metric("time from idea to reviewed draft")
    evidence: ref("local Farplane corpus")
    heartbeat: weekly_strategy_refresh
  }

  axis risk_trust {
    bet: "No fake authority, no misleading claims, no unreviewed publishing"
    kpi: review_metric("trust and claim accuracy")
    evidence: ref("review")
    heartbeat: weekly_strategy_refresh
  }

  system publishing_gate {
    status: ready
    evidence: ref("operator approval requirement")
    action: use_existing("explicit approval before publish")
  }

  system analytics {
    status: missing_instrumentation
    evidence: ref("no YouTube metrics before publish")
    action: create_ticket("define first content metrics after publish approval")
  }

  skill video_production {
    status: ready
    use: "script, storyboard, and production planning"
  }

  skill goal_advisor {
    status: ready
    use: "compile the first research/episode-selection frontier"
  }

  heartbeat hourly_board_drain {
    first: drain_proceedable_tickets
    else: idle_gap_audit
    gates: [no_publish, no_spend, no_account_changes]
  }

  heartbeat weekly_strategy_refresh {
    first: refresh_strategy_from_findings_metrics_feedback
    skills: [weekly_strategy_analysis, goal_advisor, review]
    gates: [review_before_external_side_effects]
  }

  frontier {
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

## Goal Advisor Handoff

- `task:` Research and choose the first pilot episode.
- `trigger:` active_goal or heartbeat, depending on operator timing.
- `metric_provider:` review_metric.
- `side_effect_gates:` no publish, no spend, no account changes.
- `stop_conditions:` episode handoff ready, or blocked by missing operator
  decision.
