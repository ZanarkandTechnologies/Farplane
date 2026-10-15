---
schema: farplane_project_automation
framework_template_version: 1.0.0
owner: automation-advisor
id: farplane-prospector-watch
name: Farplane Prospector Watch
kind: cron
status: paused
target:
  workspace: /Users/kenjipcx/Zanarkand Technologies/projects/Farplane
schedule:
  type: daily
  timezone: Asia/Kuala_Lumpur
  time: "05:45"
---
Task record: GitHub Issues of each project's repo (tickets/README.md); this job never writes them.

The Prospector's daily watch: the Sales island's first employee in the bunker (Farplane-UI-v2
`docs/prd.md`, "The employees"). It finds companies that show a dated buying signal, keeps only the
ones new since the last run, and hands the best to the Outreach lead as a draft task. It runs inside
Morning; this record is never scheduled on its own.

Use $prospect, recipe 6 in `skills/prospect/references/data-recipes.md` (dated signals, then fit x
timing tiers).

For each floor in `~/.farplane/company.json` whose repo's `farplane/bindings.yaml` has a
`prospect_watch` block:

1. **Budget gate.** Sum this week's (Monday to Sunday) rows in the Spend log of `~/.farplane/USER.md`.
   If that sum plus the block's `budget_usd` would pass the weekly cap, make no paid call: price the
   run with treg's free `catalog_get`, write the status below with `state: waiting` and a summary
   naming the price and the cap, and go to the next floor.
2. **Signals.** Pull only dated, linkable signals for the block's `signals` since the last run
   (`seen.json`'s `lastRun`, else 7 days): job postings whose titles are in `signals.hiring` at
   companies inside `fit.headcount`, in `fit.countries`. Count first where the provider counts for
   free, then pull at most `max_companies` rows. Stop when the run's spend reaches `budget_usd`.
3. **New only.** Drop every company domain already in `seen.json`.
4. **Fit x timing.** One `why now` line per company from its signal. Tier A: fit and timing both high
   (inside the ICP and a posting under 7 days old); B: one of them; C: neither.
5. **People, tier A only.** Find the owner or the head of the job's function (getleads.io decision
   makers is free; fall back to `treg.people.search`), then find the work email cheapest-first and
   verify it as its own step. Keep only deliverable addresses.
6. **Write** `<floor repo>/.farplane/watch/prospector/`:
   - `YYYY-MM-DD.md`: the run's report: every company with its tier, why-now line, signal link,
     the person and email for tier A, and the spend per step.
   - `seen.json`: `{ "lastRun": ISO, "domains": [...] }` with today's domains added.
   - `latest.json`: `{ "role": "prospector", "ranAt": ISO, "state": "ok" | "waiting" | "failed",
     "summary": one sentence, "found": new companies, "spendUsd": number, "report": path }`. The
     office reads this file to show the Prospector's desk; write it last, and on a failure too.
7. **Hand off.** When tier A has anyone, queue one task for the Outreach lead on that floor:
   `office-queue add --floor <floor> --routine prospector-<YYYY-MM-DD> --title "Draft outreach for N new
   leads" --gate send`, with the brief on stdin: the report path and "use $approach for each tier-A
   lead". The routine id keeps a rerun from queueing twice; the draft waits for Kenji; nothing is sent.
8. **Log spend.** Add one Spend log row to `~/.farplane/USER.md` for any non-zero run.

Params:
config_ref = "<floor repo>/farplane/bindings.yaml#prospect_watch"
weekly_cap_usd = 100
write_policy = "writes only <floor repo>/.farplane/watch/prospector/ and one office-queue task per floor; never sends, posts or writes a CRM"

Final response: per floor, one line: found N new (A/B/C), spend, the report path, or why it waited.
