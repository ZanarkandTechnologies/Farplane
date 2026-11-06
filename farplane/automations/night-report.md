---
schema: farplane_project_automation
framework_template_version: 1.0.0
owner: automation-advisor
id: night-report
name: Night Report
kind: cron
status: active
runtime: claude
runtime_task: farplane-night-report
target:
  workspace: /Users/kenjipcx/Zanarkand Technologies/projects/Farplane
schedule:
  type: daily
  timezone: local
  time: "12:30"
---
Add last night to the "While you sleep" section of the Thread Time Profiler
dashboard: how long each thread kept working after Kenji's last message, why it
stopped, and how often it stopped with work left. Kenji sleeps past the morning
automations, so this runs at midday, when the night is over.

1. **Measure.** Run `python3 ~/Eddison/tools/thread-profiler/nights.py --label`.
   It reads the app transcripts, labels new runs with `claude -p` on the
   subscription, and rewrites
   `~/Eddison/tools/thread-profiler/thread-time-profiler.html`. It spends
   nothing. If it fails, stop and report the error.
2. **Publish.** Read the live version with `get_artifact`, slug
   `be28a945-f8d8-470c-ad52-01d4d3428f88`, then republish that one HTML file
   with `publish_files`: `as` is `index.html`, `slug` and `base_version` as read,
   `mode` omitted. If the client refuses the path, copy the file into this
   workspace's `.farplane/reports/night-report/` and publish that copy.
3. **Close the run** with `farplane/automations/steps/close-run.md`. The
   dashboard is the delivery; send no message.
