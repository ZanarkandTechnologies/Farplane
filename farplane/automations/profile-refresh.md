---
schema: farplane_project_automation
framework_template_version: 1.0.0
owner: automation-advisor
id: farplane-profile-refresh
name: Farplane Profile Refresh
kind: cron
status: active
runtime: claude
runtime_task: farplane-profile-refresh
target:
  workspace: /Users/kenjipcx/Zanarkand Technologies/projects/Farplane
schedule:
  type: weekly
  timezone: Asia/Kuala_Lumpur
  days:
  - Mon
  time: "06:30"
---
Refresh `/Users/kenjipcx/.farplane/USER.md` once a week, after Monday's weekly report, using only current local work evidence.

Read:
- `/Users/kenjipcx/.farplane/company.json`
- the current USER.md
- this week's plan: the newest `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane/.farplane/company-os/daily/context/<run>/_operator-plan.md` (the Plan Week copy Morning fetches)
- recent git activity and concise project documentation in:
  - `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane`
  - `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane-UI-v2`
  - registered active project paths from company.json, only when needed

Write policy:
- Edit only `/Users/kenjipcx/.farplane/USER.md`.
- Never edit, reorder or remove a `## Standing permissions` section; Kenji sets it by hand.
- Preserve its work-focused scope and all Boundary rules.
- Add or remove project entries only with current evidence; the week's plan counts as evidence of what is active.
- Add inferred interests only when they recur across meaningful work, and label them provisional.
- Never infer or store sensitive identity, health, family, finance, politics or location data.
- Never change project files, create tickets, run external searches, or commit.
- If the evidence doesn't justify a real profile change, keep the profile text intact and only refresh its date, plus a short evidence note.

Finish with the profile path, whether it changed, and a one-sentence evidence summary.

Close: run `farplane/automations/steps/close-run.md`.
