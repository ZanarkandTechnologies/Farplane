---
schema: farplane_project_automation
framework_template_version: 1.0.0
owner: automation-advisor
id: runpod-idle-watch
name: RunPod idle watch
kind: cron
status: active
runtime: claude
runtime_task: farplane-runpod-idle-watch
target:
  workspace: /Users/kenjipcx/Zanarkand Technologies/projects/Farplane
schedule:
  type: active_hours_interval
  timezone: local
  active_hours: "09:00-21:00"
  interval_minutes: 720
---
Stop RunPod GPU pods that sit idle, and tell Kenji about anything on RunPod
that bills while nothing runs. Idle GPUs, stopped-pod disks and an unused
network volume have billed while threads waited or the Mac slept.

Work in `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane`.

1. **Check.** Run `bin/runpod-idle-watch.py` (no flags). It reads the account
   with the local RunPod key, stops a running GPU pod after two checks in a row
   under 5% GPU use (never one up less than 20 minutes, never one protected with
   `bin/runpod-idle-watch.py keep <pod-id> <hours>`), stops a pod that has shown
   no container for 25 minutes, and prints one JSON summary. Do not stop,
   delete, start or create anything yourself; the script owns every stop.
2. **Quiet run.** If the JSON says `"notify": false`, end with the receipt
   below and send nothing.
3. **Message Kenji.** Otherwise use the `notify` skill (Telegram) to send one
   short phone-readable message, addressed to "boss":
   - each stopped pod: name, $/h, why, and whether the stop succeeded;
   - each warning (a pod idle once, which will stop at the next check unless
     kept), with the keep command;
   - the daily lines (stopped pods holding disk, network volumes with $/day,
     a low balance), at most once a day as the script decides.
   No tables, no raw JSON. Claim "sent" only on a gateway receipt.
4. **Never** delete pods or network volumes, top up, or change account
   settings; deleting storage can destroy data, so it stays Kenji's call.

**Receipt.** End with: pods running, pods stopped this run (or none), balance,
whether a message was sent (receipt or reason), and "deletions: none".

Close: run `farplane/automations/steps/close-run.md`.
