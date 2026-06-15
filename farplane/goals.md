---
kind: goal-portfolio
status: active
project: Farplane
created_at: 2026-06-15
updated_at: 2026-06-15
framework_template_version: "0.1.0"
owner: project-pm-automation
source: migrated-from-root-goal-portfolio
refs:
  - farplane/harness.md
  - farplane/automations.md
  - farplane/bindings.md
  - docs/farplane-framework/README.md
  - docs/specs/program-notation.md
  - skills/goal-advisor/references/goal-portfolio.md
---

# Farplane Goals

This file is Farplane's dynamic strategy object. It owns the North Star,
strategy axes, current bets, current milestone, holds, and Goal Advisor
handoffs.

It does not own schedules, grouped jobs, report paths, ticket source policy, or
run-ledger rules. Those live in [automations.md](automations.md).

## Goal Program

```goal-program
values_ref: farplane/harness.md
automation_ref: farplane/automations.md
bindings_ref: farplane/bindings.md

goal farplane_os {
  horizon: "1y"
  outcome: "Farplane is the dependable local harness for autonomous Codex work across Core, Console, UI, and project-local agent systems."
  metric: hybrid(
    review_metric("operators can turn ideas into artifact-backed Goal loops"),
    artifact_presence("skills, tickets, docs, validators, proof surfaces, and framework files stay discoverable")
  )
  proof: [README.md, ARCHITECTURE.md, docs/MEMORY.md, docs/specs/README.md, farplane/]
}

goal q3_harness_operating_system {
  parent: farplane_os
  horizon: "quarter"
  outcome: "Make high-level intents compile into compact projects, Goal Packets, automations, and skill gaps without transcript-only reasoning."
  metric: review_metric("portfolio, harness, automation, and ticket examples are readable enough to run")
  anti_metric: "more notation than adoption"
}

axis acquire_use {
  question: "Can more project types initialize into the framework?"
  kpi: review_metric("new project can produce farplane/ config, tickets, and first Goal Advisor handoff")
  current_signal: ref("skills/deep-init-project/SKILL.md") + ref("docs/farplane-framework/")
}

axis activate_next_action {
  question: "Can an agent understand the project and pick the right next action?"
  kpi: review_metric("agent can select between weekly PM, ticket drainer, direct answer, or Goal Packet")
  current_signal: ref("AGENTS.md") + ref("farplane/README.md") + ref("tickets/")
}

axis retain_trust {
  question: "Do repeated loops become safer and clearer over time?"
  kpi: learning_metric("fresh lessons/troubles produce skill hardening, evals, or ticket deltas")
  current_signal: ref("docs/LESSONS.md") + ref("docs/TROUBLES.md")
}

axis efficiency_pm {
  question: "Does PM automation reduce manual planning and cleanup?"
  kpi: artifact_presence(".farplane/reports/weekly-pm/latest.md") + artifact_presence(".farplane/reports/ticket-update/latest.md")
  current_signal: ref("farplane/automations.md")
}

axis quality_checks {
  question: "Are standards enforced by checks instead of memory?"
  kpi: mechanical("framework, doc, harness, and skill validators pass")
  current_signal: ref("bin/validators/") + ref("farplane/evals.md")
}

project framework_standardization {
  parent: q3_harness_operating_system
  output: "The Farplane project framework has a clear tracked config split: harness, goals, automations, bindings, evals, tickets, and runtime reports."
  feedback_surface: review_metric("a new or existing project can tell where strategy, automations, bindings, and proof belong")
  budget: time_budget("1 week")
  route: harness_creator
  gates: [no_hidden_automation, no_secret_in_tracked_config, no_duplicate_goal_sources]
  starting_tasks: [
    "keep farplane/goals.md canonical for strategy",
    "keep farplane/automations.md canonical for schedules and grouped jobs",
    "verify no duplicate strategy source exists outside farplane/goals.md",
    "run framework and doc validators"
  ]
}

project goal_advisor_program_grammar {
  parent: q3_harness_operating_system
  output: "Goal Advisor compiles values -> goals -> feedback-sized projects -> milestones -> tickets only when a real boundary exists."
  feedback_surface: review_metric("Goal Advisor reference and templates produce compact, executable portfolios")
  budget: time_budget("1 week")
  route: goal_advisor
  gates: [preserve_goal_packet_contract, no_task_explosion]
  starting_tasks: [
    "keep feedback-sized project rule in Goal Advisor",
    "add example before/after portfolio when needed",
    "decide whether Goal Program gets a fenced block template"
  ]
}

project project_pm_heartbeat_preset {
  parent: q3_harness_operating_system
  output: "A reusable project PM heartbeat preset: weekly strategy refresh, daily ticket update, weekly memory update, and weekly skill self-improvement."
  feedback_surface: review_metric("one project can initialize the preset without inventing custom files")
  budget: time_budget("2 weeks")
  route: deep_init_project
  gates: [automation_preview_before_scheduling, local_files_source_of_truth]
  starting_tasks: [
    "keep weekly PM update in automations.md",
    "keep daily ticket drainer separate from weekly PM",
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
  task: "Make farplane/goals.md the canonical dynamic strategy file and keep automation mechanics in farplane/automations.md."
  metric: artifact_presence("farplane/goals.md active") + review_metric("no root goal portfolio duplicate")
  route: one_turn
  gates: [no_commit_without_request]
}
```

## Current Milestone

Make the Farplane framework standard usable enough that a new project can be
set up with a clear split between:

- tracked `farplane/` config
- ignored `.farplane/` runtime state
- local tickets
- weekly PM update
- daily ticket drainer
- bindings
- context/docs update
- skill harden/refine loop

## Strategy Update Rule

Weekly PM may update this file when fresh reports or tickets change strategy:

```text
update_strategy(farplane/goals.md, reports, tickets, memory)
  -> goal_delta + milestone_delta + holds_delta + ticket_delta
```

The weekly PM should not move schedule, grouped-job, report-path, or run-ledger
configuration into this file. It should update [automations.md](automations.md)
only when the cadence itself changes.

## Holds

- Do not add hidden daemon behavior.
- Do not store secrets in tracked config.
- Do not make Notion canonical until the project explicitly opts in.
- Do not execute leaf tickets from weekly PM unless the project chooses a
  combined cadence.
- Do not split projects into child tickets unless there is a real execution,
  unblock, review, dependency, approval, or proof boundary.

## Goal Advisor Handoff

Use `goal-advisor` when the current milestone or an active project becomes
executable enough to run as a ticket-backed Goal Packet.

Next eligible handoff:

```text
goal_advisor(
  files=[farplane/goals.md, farplane/automations.md, farplane/harness.md, tickets/],
  task="turn the current milestone into one concrete ticket-backed Goal Packet",
  metric_provider=review_metric,
  trigger=active_goal | heartbeat,
  gates=[no_hidden_automation, no_external_side_effects_without_approval]
) -> ticket.md + program.md + progress.md + native_goal_prompt
```
