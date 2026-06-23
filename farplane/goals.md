---
kind: project-goals
status: active
project: Farplane
created_at: 2026-06-15
updated_at: 2026-06-23
framework_template_version: "0.2.0"
owner: project-pm-automation
source: horizon-advisor
refs:
  - farplane/harness.md
  - farplane/steer.config.json
  - farplane/bindings.md
  - docs/farplane-framework/README.md
  - docs/specs/program-notation.md
  - docs/fundamentals/harness-algebra.md
  - skills/horizon-advisor/SKILL.md
  - skills/horizon-advisor/references/project-goals.md
---

# Farplane Goals

This file is Farplane's dynamic strategy object. It owns the North Star,
value function, KPI tree, strategy axes, current bets, current milestone,
holds, and Goal Advisor handoffs.

It does not own schedules, grouped jobs, report paths, ticket source policy, or
run-ledger rules. Scheduled planning mechanics live in
[steer.config.json](steer.config.json), while Pulse behavior lives in the
`pulse-update` skill and its runtime state.

## Goal Program

```goal-program
values_ref: farplane/harness.md
steer_config_ref: farplane/steer.config.json
bindings_ref: farplane/bindings.md

goal farplane_os {
  horizon: "1y"
  outcome: "Farplane is the standard way researchers and builders create harnesses that run longer, improve from evidence, and produce higher-quality results with less human intervention."
  metric: hybrid(
    learning_metric("validated meaningful improvement cycles per human intervention hour increases"),
    review_metric("quality, proof, auditability, and operator control are preserved"),
    artifact_presence("goals, tickets, Steer/Pulse automations, evals, reports, and memory stay discoverable")
  )
  anti_metric: "more agent activity without accepted evidence-backed improvement"
  proof: [README.md, ARCHITECTURE.md, docs/fundamentals/harness-algebra.md, docs/MEMORY.md, docs/specs/README.md, farplane/]
}

goal q3_harness_operating_system {
  parent: farplane_os
  horizon: "quarter"
  outcome: "Prove Farplane can coordinate researcher-led, agent-run harness improvement across multiple projects through explicit goals, metrics, experiments, reports, and Goal Packets."
  metric: review_metric("project goals, harness, automation, and ticket examples are readable enough to run")
  anti_metric: "self-improvement claims without intervention budget, ablation/eval evidence, or accepted quality deltas"
}

value_function harness_autonomy_quality {
  maximize: [
    meaningful_long_running_output,
    quality,
    validated_improvement,
    reliability,
    reusable_behavior,
    auditability
  ]
  minimize: [
    human_intervention,
    false_completion,
    agent_churn,
    coordination_cost,
    ungrounded_claims,
    brittle_state_loss
  ]
  constraints: [
    user_goal_satisfied,
    groundedness_sufficient,
    correctness_regression_false,
    safety_regression_false,
    proof_exists,
    operator_control_preserved
  ]
}

axis validated_self_improvement {
  question: "Can Farplane create and complete meaningful improvement cycles with less human intervention?"
  kpi: hybrid(
    learning_metric("validated_improvement_cycles_completed"),
    learning_metric("accepted_harness_improvements"),
    learning_metric("human_intervention_minutes_per_cycle trends down")
  )
  current_signal: ref("docs/fundamentals/harness-algebra.md") + ref("skills/optimize-harness/SKILL.md") + ref("skills/horizon-advisor/SKILL.md")
}

axis quality_and_proof {
  question: "Do long-running agents preserve quality, proof, and operator control instead of just doing more work?"
  kpi: hybrid(
    review_metric("completion claims include sufficient proof and no self-certified QA/review where prohibited"),
    mechanical("framework, doc, harness, and skill validators pass"),
    learning_metric("false_completion and brittle_state_loss incidents trend down")
  )
  current_signal: ref("bin/validators/") + ref("farplane/evals.md") + ref("docs/TROUBLES.md")
}

axis project_control {
  question: "Can Farplane control a dynamic list of projects with their own completion criteria and intervention budgets?"
  kpi: hybrid(
    artifact_presence("each active project has goals/metrics/proof state"),
    review_metric("Steer can select the current frontier without expanding every branch"),
    learning_metric("projects advanced without human unblock")
  )
  current_signal: ref("farplane/goals.md") + ref("tickets/") + ref(".farplane/state/steer-scheduler.json")
}

axis distribution_from_evidence {
  question: "Can Farplane turn real harness evidence into audience, users, and research authority?"
  kpi: hybrid(
    market_metric("qualified subscribers, serious conversations, and pilot users increase"),
    artifact_presence("evidence-backed content/research artifacts ship from experiment reports"),
    learning_metric("content/user feedback changes the next Steer strategy review")
  )
  current_signal: ref(".farplane/state/steer-scheduler.json") + ref("tickets/") + ref("docs/LESSONS.md")
}

axis framework_adoption {
  question: "Can more project types initialize into Farplane and run a first measured improvement loop?"
  kpi: review_metric("new project can produce farplane/ config, goals, evals, tickets, and first Goal Advisor handoff")
  current_signal: ref("skills/deep-init-project/SKILL.md") + ref("docs/farplane-framework/") + ref("skills/horizon-advisor/SKILL.md")
}

project framework_standardization {
  parent: q3_harness_operating_system
  output: "The Farplane project framework has a clear tracked config split: harness, goals, Steer config, bindings, evals, tickets, and runtime reports."
  feedback_surface: review_metric("a new or existing project can tell where strategy, Steer/Pulse automation, bindings, and proof belong")
  budget: time_budget("1 week")
  route: harness_creator
  gates: [no_hidden_automation, no_secret_in_tracked_config, no_duplicate_goal_sources]
  starting_tasks: [
    "keep farplane/goals.md canonical for strategy",
    "keep farplane/steer.config.json canonical for Steer scheduled planning jobs",
    "verify no duplicate strategy source exists outside farplane/goals.md",
    "run framework and doc validators"
  ]
}

project goal_advisor_program_grammar {
  parent: q3_harness_operating_system
  output: "Horizon Advisor authors values -> goals -> KPI trees -> feedback-sized projects; Goal Advisor compiles selected frontiers into executable Goal Packets."
  feedback_surface: review_metric("Horizon Advisor and Goal Advisor boundaries are clear enough that agents do not duplicate strategy and execution roles")
  budget: time_budget("1 week")
  route: horizon_advisor_then_goal_advisor
  gates: [preserve_goal_packet_contract, no_task_explosion]
  starting_tasks: [
    "keep project-goals authoring in horizon-advisor",
    "keep execution compilation in goal-advisor",
    "add evals after the first two horizon-advisor uses reveal failure modes"
  ]
}

project low_intervention_experiment_engine {
  parent: q3_harness_operating_system
  output: "Farplane can propose, run, evaluate, and accept/reject harness improvement experiments with explicit human-intervention accounting."
  feedback_surface: hybrid_metric("validated cycles", "accepted improvements", "human intervention minutes", "quality/proof review")
  budget: time_budget("quarter")
  route: optimize_harness + eval + horizon_advisor
  gates: [no_fake_precision, no_unreviewed_self_improvement_claims, operator_control_preserved]
  starting_tasks: [
    "define validated improvement cycle report format",
    "select first 3 project contexts for low-intervention improvement loops",
    "run ablations only where baseline and proof surface are clear"
  ]
}

project evidence_distribution_engine {
  parent: q3_harness_operating_system
  output: "Farplane turns accepted experiments, ablations, and lessons into research notes, educational content, subscriber growth, and pilot conversations."
  feedback_surface: hybrid_metric("content shipped", "qualified attention", "serious conversations", "pilot users")
  budget: time_budget("quarter")
  route: horizon_advisor + social_content + research
  gates: [claims_backed_by_artifacts, no_generic_ai_content, privacy_review]
  starting_tasks: [
    "create content backlog from accepted experiment reports and lessons",
    "ship evidence-backed posts/research notes on a weekly cadence",
    "track replies, subscribers, conversations, and pilot conversions"
  ]
}

project steer_pulse_framework_standard {
  parent: q3_harness_operating_system
  output: "A reusable project automation standard: Pulse for one bounded idle action and Steer for scheduled planning, strategy, memory, and skill upkeep."
  feedback_surface: review_metric("one project can initialize the preset without inventing custom files")
  budget: time_budget("2 weeks")
  route: deep_init_project
  gates: [automation_preview_before_scheduling, local_files_source_of_truth]
  starting_tasks: [
    "keep Steer job config in farplane/steer.config.json",
    "keep simple ticket selection inside pulse-update",
    "migrate useful daily/weekly PM practices into Steer before deleting old skill packages",
    "write unblock tickets for missing Notion, Telegram, metrics, or binding access"
  ]
}

project skill_memory_hierarchy {
  parent: q3_harness_operating_system
  output: "Local project memories, lessons, troubles, and skill findings can roll up to parent projects without losing project context."
  feedback_surface: review_metric("parent PM report summarizes child project state without reading every child report")
  budget: time_budget("2 weeks")
  route: skill_maintenance
  gates: [no_private_context_leakage, child_context_preserved]
  starting_tasks: [
    "define local-to-parent update_memory behavior",
    "define local-to-parent skill improvement proposals",
    "decide what rolls up globally versus stays project-local"
  ]
}

project console_feedback_visibility {
  parent: farplane_os
  output: "Console makes harness health, activity, nudges, and goal progress visible enough that background work is inspectable."
  feedback_surface: human_feedback("operator can wake up and see what matters now")
  budget: time_budget("quarter")
  route: future_goal_packet
  gates: [no_hidden_autonomy, privacy_review]
  starting_tasks: [
    "define useful wake-up report fields",
    "connect project activity signals",
    "surface blocked tickets and missing feedback loops"
  ]
}

milestone framework_strategy_split {
  task: "Make farplane/goals.md the canonical dynamic strategy file and keep scheduled automation mechanics in farplane/steer.config.json."
  metric: artifact_presence("farplane/goals.md active") + review_metric("no duplicate root strategy file")
  route: one_turn
  gates: [no_commit_without_request]
}
```

## Current Milestone

Make Farplane's horizon layer explicit enough to optimize the harness algebra
value function instead of vague growth or vague self-improvement claims:

- North Star = meaningful long-running autonomous improvement per human
  intervention hour
- Horizon Advisor owns goal/KPI/project-goals authoring
- Goal Advisor owns execution compilation for selected frontiers
- first validated improvement cycles define intervention budget, quality
  metric, proof surface, and accept/reject decision
- distribution work is downstream of evidence, not detached marketing

## Strategy Update Rule

Steer strategy review may propose updates to this file when fresh reports or
tickets change strategy:

```text
update_strategy(farplane/goals.md, steer_reports, tickets, memory)
  -> goal_delta + milestone_delta + holds_delta + ticket_delta
```

Steer should not move schedule, grouped-job, report-path, or run-ledger
configuration into this file. It should update
[steer.config.json](steer.config.json) only when the scheduled planning config
itself changes.
Use `horizon-advisor` when the update needs to rewrite the North Star, value
function, KPI tree, project goal map, or current frontier.

## Holds

- Do not add hidden daemon behavior.
- Do not store secrets in tracked config.
- Do not make Notion canonical until the project explicitly opts in.
- Do not execute broad leaf tickets from Steer; route execution through Pulse,
  tickets, or Goal Advisor.
- Do not split projects into child tickets unless there is a real execution,
  unblock, review, dependency, approval, or proof boundary.
- Do not claim self-improvement without baseline, metric provider, proof
  surface, intervention accounting, and accept/reject decision.
- Do not optimize distribution metrics independently from evidence-backed
  harness improvement.

## Goal Advisor Handoff

Use `goal-advisor` when the current milestone or an active project becomes
executable enough to run as a ticket-backed Goal Packet.

Next eligible handoff:

```text
goal_advisor(
  files=[farplane/goals.md, farplane/steer.config.json, farplane/harness.md, docs/fundamentals/harness-algebra.md, tickets/],
  task="compile the current low-intervention improvement frontier into one concrete ticket-backed Goal Packet",
  metric_provider=hybrid_metric(learning, review, mechanical),
  trigger=active_goal | heartbeat,
  gates=[no_hidden_automation, no_external_side_effects_without_approval, proof_exists, operator_control_preserved]
) -> ticket.md + program.md + progress.md + native_goal_prompt
```
