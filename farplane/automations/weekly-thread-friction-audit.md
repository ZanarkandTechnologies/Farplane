---
schema: farplane_project_automation
framework_template_version: 1.0.0
owner: automation-advisor
id: farplane-weekly-thread-friction-audit
name: Farplane Weekly Thread Friction Audit
kind: cron
status: active
target:
  workspace: /Users/kenjipcx/Zanarkand Technologies/projects/Farplane
schedule:
  type: weekly
  timezone: Asia/Kuala_Lumpur
  days:
  - Mon
  time: 07:00
---
Task storage override: follow tickets/README.md. Multica is dashboard-only;
resolve project bindings, keep issues unassigned, and use --no-start for updates.
Create/update task records through the existing Multica CLI, never ticket.md.
Do not invoke filesystem materializers, finalizers or dispatch based on local
migration snapshots. If a phase requires such a legacy adapter, report that
phase as unavailable; continue independent read-only reporting. Never start
Multica agents, squads, autopilots or runs.

Use $gap-analysis.

Audit locally indexed Codex operator conversations from the last week as raw
interaction evidence. Enumerate the local thread catalog through a fixed
cutoff, select interactive root tasks, replay their full rollout histories,
and measure correction loops, repeated requirements, premature stopping,
reference/taste misses, scope drift, and avoidable clarification burden.
Separate agent misses from underspecified input, tool/context limits, and
genuinely branching decisions. Ground every material finding in replayable
thread/turn locators and preserve uncertainty for judgment-coded labels.

Write one dated report at
`.farplane/research/<YYYY-MM-DD>-weekly-thread-friction-audit.md` containing the
coverage receipt, exclusions, correction register, contribution split, ranked
friction patterns, recurring taste/preferences, and the smallest evidence-
backed improvement candidates. Compare with the previous dated report when
present. Treat inaccessible cloud-only conversations as a source gap; never
imply all-product coverage from the local catalog.

This run is report-only. Do not mutate skills, prompts, policies, tickets,
Goals, automations, or source histories, and do not execute improvement work.
Dogfood Review remains the separate owner for self-improvement ticket and Goal
portfolio evidence.

Params:
project_root = "/Users/kenjipcx/Zanarkand Technologies/projects/Farplane"
window = "last_week"
timezone = "Asia/Kuala_Lumpur"
write_policy = "one dated raw-thread report only"

Reads:
- local Codex thread catalog and the rollout paths it references
- previous dated weekly thread-friction report when present
- current Dogfood report only to distinguish portfolio evidence from raw-thread evidence

Final response:
- Link the dated report and state exact task/turn/correction coverage.
- Summarize the three largest preventable friction patterns and evidence-backed taste signals.
- List improvement candidates with owner surface, proof metric, and reason.
- Name inaccessible sources and classification uncertainty.
- Include the no-mutation receipt: no skill, prompt, policy, ticket, Goal,
  automation, source-history, or execution changes.

Config source:
farplane/automations/weekly-thread-friction-audit.md id="farplane-weekly-thread-friction-audit"
