---
schema: farplane_project_automation
framework_template_version: 1.0.0
owner: automation-advisor
source_template: automations/weekly-thread-friction-audit.md
source_template_version: 1.0.0
id: farplane-weekly-thread-friction-audit
name: Farplane Session Friction Retro
kind: cron
status: active
runtime: claude
runtime_task: farplane-session-friction-retro
target:
  workspace: /Users/kenjipcx/Zanarkand Technologies/projects/Farplane
schedule:
  type: daily
  timezone: Asia/Kuala_Lumpur
  time: "23:40"
---
Task record: GitHub Issues of each project's repo (tickets/README.md); this job never writes them.

Audit the day's local Codex and Claude Code operator sessions as raw
interaction evidence: where the agents made work slower or worse, and where the
day's time actually went. Report Gen reads these daily reports for the week.

Freeze the window and enumerate sessions for this project from both runtimes'
local transcript stores. Select interactive root tasks and replay their full
histories.

Friction: measure correction loops, repeated requirements, premature stopping,
reference/taste misses, scope drift, and avoidable clarification burden.
Separate agent misses from underspecified input, tool/context limits, and
genuinely branching decisions. Preserve uncertainty for judgment-coded labels.

Time allocation: classify turns by phase (framing/design, planning, execution,
review/QA, rework, waiting on the operator) and report the split per session and
for the day, with rework and correction time shown separately.

Ground every material finding in replayable session/turn locators. Plan-vs-
actual and goal attainment belong to Report Gen; do not duplicate them here.

Write one dated report at
`.farplane/research/<YYYY-MM-DD>-session-friction-retro.md`. Open it with the
headline sentence `**<n> correction episodes across <m> operator turns (<x>%)**`
(the office's Mission board and weekly report read that line), then the
coverage receipt, exclusions, correction register, contribution split, time
allocation table, ranked friction patterns, recurring taste/preferences, and the
smallest evidence-backed improvement candidates. Compare with the previous dated
report when present. Treat cloud-only sessions as a named source gap; never
imply full coverage from the local stores.

This run is report-only. Do not mutate skills, prompts, policies, issues, Goals,
automations, or source histories, and do not execute improvement work. Dogfood
Review remains the separate owner for self-improvement portfolio evidence.

Params:
project_root = "/Users/kenjipcx/Zanarkand Technologies/projects/Farplane"
window = "last_24h"
timezone = "Asia/Kuala_Lumpur"
write_policy = "one dated raw-thread report only"

Reads:
- Daily Collect session indexes (`<project-slug>.sessions.jsonl`) for the day, when present
- local Codex session catalog and the rollout paths it references
- local Claude Code session transcripts (`~/.claude/projects/<project>/`)
- previous dated session friction report when present
- current Dogfood report only to distinguish portfolio evidence from raw-session evidence

Final response:
- Link the dated report and state exact session/turn/correction coverage.
- Summarize the three largest preventable friction patterns, the day's time
  allocation (including rework share), and evidence-backed taste signals.
- List improvement candidates with owner surface, proof metric, and reason.
- Name inaccessible sources and classification uncertainty.
- Include the no-mutation receipt: no skill, prompt, policy, issue, Goal,
  automation, source-history, or execution changes.

Config source:
farplane/automations/weekly-thread-friction-audit.md id="farplane-weekly-thread-friction-audit"
