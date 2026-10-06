---
schema: farplane_project_automation
framework_template_version: 1.0.0
owner: automation-advisor
id: farplane-profile-refresh
name: Farplane Profile Refresh
kind: cron
status: paused
runtime: claude
runtime_task: farplane-profile-refresh
target:
  workspace: /Users/kenjipcx/Zanarkand Technologies/projects/Farplane
schedule:
  type: monthly
  timezone: Asia/Kuala_Lumpur
  day_of_month: 1
  time: "09:00"
---
Refresh `/Users/kenjipcx/.farplane/USER.md` once, using only current local work evidence. This moved from the paused Codex automation "Monthly Operator Profile Refresh".

Read:
- `/Users/kenjipcx/.farplane/company.json`
- the current USER.md
- recent git activity and concise project documentation in:
  - `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane`
  - `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane-UI`
  - `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane-UI-v2`
  - registered active project paths from company.json, only when needed

Write policy:
- Edit only `/Users/kenjipcx/.farplane/USER.md`.
- Preserve its work-focused scope and all Boundary rules.
- Add or remove project entries only with current evidence.
- Add inferred interests only when they recur across meaningful work, and label them provisional.
- Never infer or store sensitive identity, health, family, finance, politics or location data.
- Never change project files, create tickets, run external searches, or commit.
- If the evidence doesn't justify a real profile change, keep the profile text intact and only refresh its date, plus a short evidence note.

Finish with the profile path, whether it changed, and a one-sentence evidence summary.
