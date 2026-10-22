---
schema: farplane_project_automation
framework_template_version: 1.0.0
owner: automation-advisor
id: disk-review
name: Mac disk review
kind: cron
status: active
runtime: claude
runtime_task: farplane-disk-review
target:
  workspace: /Users/kenjipcx/Zanarkand Technologies/projects/Farplane
schedule:
  type: weekly
  timezone: local
  days:
  - Mon
  time: "09:00"
---
Review this Mac's disk and app usage once a week and propose what Kenji can
delete. Never delete, move, trash, empty or clean anything yourself. On 22 Oct
2026 the disk hit 99% full (14 GB free) and blocked a 110 GB install; 27 GB of
it was 410 leaked Chrome test profiles in the temp folder that nobody noticed.

Work in `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane`.

1. **Scan.** Run `python3 bin/disk-review.py` (no flags; it takes a few
   minutes). It is read-only outside its own state folder: it measures free
   space, the largest folders, known caches, project build folders, temp-folder
   leftovers, old installers in Downloads and installed apps (size and last
   activity; Spotlight is off here), compares with last week's snapshot in
   `.farplane/disk-review/snapshots/`, writes the full report to
   `.farplane/disk-review/reports/<date>.md`, and prints one JSON summary.
2. **Read the report** at the path in the JSON. Show it to Kenji in full as
   this run's final message (it is the record). Do not edit its commands.
3. **Message Kenji.** Use the `notify` skill (Telegram) to send one short
   phone-readable message, addressed to "boss", with `--parse-mode none`:
   - free space and the change since the last run;
   - the proposed total and the top three proposals, each with its size and
     how to get it back (no commands longer than one line);
   - any leak (a folder that keeps growing, or temp folders piling up) with the
     tool that creates it when the report names one;
   - apps unused for 60+ days, names only;
   - the report path, and the reply action: "reply with the numbers you want
     removed; I'll run them in a thread you open."
   No tables, no raw JSON. Claim "sent" only on a gateway receipt. If free
   space is above 150 GB, nothing grew and there are no proposals over 5 GB,
   skip the message and say so in the receipt.
4. **Never** run any command from the report, delete or trash files, empty
   the Trash, uninstall apps, or prune caches. Kenji's own data (recordings,
   demos, photos, writing, project folders) is never proposed; if the report
   ever proposes it, say so in the receipt as a bug instead of relaying it.

**Receipt.** End with: free space and change, proposed total, number of
proposals, leaks found (or none), whether a message was sent (receipt or
reason), scan seconds, and "deletions: none".

Close: run `farplane/automations/steps/close-run.md`.
