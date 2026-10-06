---
schema: farplane_project_automation
framework_template_version: 1.0.0
owner: automation-advisor
id: farplane-morning
name: Farplane Morning
kind: cron
status: active
runtime: claude
runtime_task: farplane-morning
target:
  workspace: /Users/kenjipcx/Zanarkand Technologies/projects/Farplane
schedule:
  type: daily
  timezone: Asia/Kuala_Lumpur
  time: "05:00"
---
Run Farplane's **Morning** chain on Claude Code. It's four records, run in this order in one session, each followed exactly. The front matter is metadata; each record owns its steps and write policy.

Work in `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane`.

1. **Fetch Context:** `farplane/automations/daily-collect.md`. Write today's run and its `_run.json` marker. Also copy each floor's whiteboard strategy doc found under `~/.farplane` into the run folder as `_strategy/<file>`, unchanged. That copy is the day's snapshot of the rolling strategy notes.
2. **Metrics Refresh:** `farplane/automations/metrics-refresh.md`.
3. **Knowledge Update:** `farplane/automations/knowledge-update.md`, on the run from step 1.
4. **Progress Updater:** `farplane/automations/daily-operating-update.md`, on the run from step 1 and the fresh metrics from step 2, including its pace check.

If a step fails or is blocked, record why, then carry on with the later steps where they can still run. Step 3 and step 4 both need step 1's completion marker; without it, report them as blocked.

Runtime notes (they don't change the records' rules):
- A skill written `$name` in a record is the Claude skill `name` (e.g. `progress-update`, `manage-wiki`); invoke it with the Skill tool.
- Tasks are GitHub Issues of each project's own repo; use the `gh` CLI. The only write allowed is a `gh issue comment` on an existing issue, through Progress Updater's allowlist. Public repos (Farplane, Farplane-UI, farplane-bunker) get engineering facts only. Multica is archived.
- Read Notion (the Plan Week and Life Plan adapter, and call notes) through the Notion connector, read-only.
- Credentialed commands go through `farplane run -- <command>`; never print secrets.
- Wiki: anything that is leverage for Kenji's life, career included. It stays local, outside every git repo. No health details.
- Never send messages, publish, spend, or change settings. Other people's actions and unclear ownership stay proposals.

End with one short report per step: each record's final response, condensed.
