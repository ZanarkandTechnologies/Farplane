---
kind: automation-preview
status: draft
created_at: 2026-06-15
owner: project-pm-automation
---

# PM And Ticket Update Automation Preview

This preview normalizes project automations into two recurring functions:

```text
weekly_pm_update(project, goals, strategy_state, metrics, tickets, memory, overrides) -> strategy_delta + ticket_deltas + delegated_reports + blockers
ticket_update(project, tickets, strategy_state, memory, overrides) -> selected_ticket + work_handoff + evidence_or_blocker
```

Default board policy is local-first: inspect project-local `tickets/` before
fetching Notion unless an override explicitly makes Notion canonical.

## Farplane Active Automations

### `farplane-weekly-pm-update`

```text
weekly_pm_update(
  project = "/Users/kenjipcx/Zanarkand Technologies/projects/Farplane",
  goals = "keep Farplane's harness, skills, tickets, docs, feedback loops, and proof surfaces compounding",
  strategy_state = read(AGENTS.md, docs/MEMORY.md, docs/HISTORY.md, active tickets, recent artifacts),
  metrics = read(docs/TROUBLES.md, docs/LESSONS.md, docs/skills/registry.jsonl, validation output),
  tickets = read(local:tickets/),
  memory = read(docs/MEMORY.md, docs/HISTORY.md, docs/LESSONS.md, docs/TROUBLES.md),
  overrides = {
    board_policy: "local_first",
    notion_policy: "context_only_when_explicitly_named",
    ticket_creation_policy: "local_ticket_only",
    weekly_subagents: "delegate bounded lanes with durable context_ref",
    skill_upkeep_policy: "skill-maintenance.harden_skill then skill-maintenance.refine_skill",
    registry_drift_policy: "weekly PM subroutine, not separate cron"
  }
) -> strategy_delta + memory_delta + skill_upkeep_handoffs + registry_drift_result + local_ticket_deltas + blockers
```

Subroutines:

- `update-strategy`: refresh Farplane strategy, system gaps, experiments, and ticket deltas.
- `update-memory`: consolidate durable memory and stale-context notes.
- `skill-maintenance(mode: harden_skill)`: turn fresh troubles/lessons into evals, gotchas, guardrails, or tickets.
- `skill-maintenance(mode: refine_skill)`: compact older accumulated evals/gotchas without weakening protection.
- Registry drift check: validate skill/source/feature registry state and ticket ambiguous gaps.

### `farplane-ticket-update`

```text
ticket_update(
  project = "/Users/kenjipcx/Zanarkand Technologies/projects/Farplane",
  tickets = read(local:tickets/ first, notion only when project config enables it),
  strategy_state = read(selected ticket only when needed),
  memory = none,
  overrides = {
    board_policy: "local_first",
    notion_policy: "skip unless farplane/automations.md enables Notion binding",
    execution_limit: "one_ticket",
    ticket_creation_policy: "local_ticket_only",
    review_lane: "required when ticket requires review"
  }
) -> selected_ticket + impl_plan_result + goal_advisor_execution + evidence_or_blocker
```

Behavior:

- Select one proceedable local ticket.
- Run `impl-plan` if planning is missing or stale.
- Hand selected work to `goal-advisor` for execution.
- If no local ticket can safely advance, write a no-op report with blocker categories.
- Write progress and evidence into the local ticket or ticket-scoped artifact.

## Life Preview

The Life project is the main intentional exception to the default local-first
policy because the existing task board is Notion-canonical. The override should
be explicit so other projects do not accidentally inherit Notion-first behavior.

### Existing `weekly-opportunity-deep-research` As `life-weekly-pm-update`

```text
weekly_pm_update(
  project = "/Users/kenjipcx/life",
  goals = "choose Kenji's highest-leverage priorities across work, projects, relationships, health, and opportunities",
  strategy_state = read(life docs/MEMORY.md, prior weekly bundles, Plan Week, done/not-done tasks, Codex thread drift),
  metrics = read(Notion task state, meeting notes, people signals, opportunity scan, completed/deprioritized work),
  tickets = read(notion:canonical tasks, then linked local project tickets),
  memory = read(life docs/MEMORY.md, docs/HISTORY.md, docs/LESSONS.md, docs/TROUBLES.md),
  overrides = {
    board_policy: "notion_first_for_life_canonical_task_board",
    local_ticket_policy: "resolve linked project-local ticket after selecting a Notion task",
    ticket_creation_policy: "create local project ticket only after resolving project root and concrete scope",
    strategy_skill: "weekly-strategy-analysis",
    weekly_subagents: "task retro, meeting/people signals, Codex drift, grand-plan deltas, opportunity scan",
    free_text: "Keep this as the single weekly Life strategy trigger; write the context bundle under /Users/kenjipcx/life/docs/strategy-automation/runs/."
  }
) -> weekly_report + priorities + depriorities + due_dates + ticket_deltas + blockers
```

This preserves the existing `weekly-strategy-analysis` specialization instead
of replacing it with a generic prompt.

### Existing `autonomous-ticket-planner-and-builder` As `life-ticket-update`

```text
ticket_update(
  project = "/Users/kenjipcx/life",
  tickets = read(notion:canonical In Progress/Not started tasks, then linked local project tickets),
  strategy_state = read(life docs/MEMORY.md + selected project AGENTS.md + selected ticket),
  memory = read(life docs/MEMORY.md, docs/TROUBLES.md, docs/LESSONS.md, docs/HISTORY.md),
  overrides = {
    board_policy: "notion_first_for_life_canonical_task_board",
    local_ticket_policy: "after Notion selection, prefer linked local ticket; create one only when project has tickets/ and task is concrete",
    execution_limit: "one_ticket",
    review_lane: "move Notion task to Review only after evidence is written",
    side_effect_gates: "no push, deploy, publish, spend, account changes, or destructive cleanup",
    free_text: "This is a dispatcher, not a planning sidecar. Spawn a Goal-backed Codex worker in the resolved project directory."
  }
) -> selected_notion_task + selected_local_ticket + codex_exec_handoff + evidence_or_blocker
```

`notion-task-field-fill` remains separate: it maintains task metadata and review
requests, while `life-ticket-update` executes one safe work item.

## Reusable Rule

```text
project_automation_contract(
  default_board_policy = "local_first",
  project_override = optional structured policy + free_text,
  weekly = weekly_pm_update(...),
  daily = ticket_update(...)
) -> visible strategy loop + visible work loop
```

Use structured fields for stable behavior and `free_text` for project-specific
judgment that would be awkward to overfit into schema too early.
