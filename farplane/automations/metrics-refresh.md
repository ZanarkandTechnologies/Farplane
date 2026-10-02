---
schema: farplane_project_automation
framework_template_version: 1.0.0
owner: automation-advisor
id: farplane-metrics-refresh
name: Farplane Metrics Refresh
kind: cron
status: active
target:
  workspace: /Users/kenjipcx/Zanarkand Technologies/projects/Farplane
schedule:
  type: daily
  timezone: Asia/Kuala_Lumpur
  time: "05:30"
---
Task record: GitHub Issues of each project's repo (tickets/README.md); this job never writes them.

Refresh every registered Project's metric readings and the snapshot the office reads, once a day,
so the CEO desk and the Mission board never show weeks-old numbers.

Execution boundary:

- Work under the Farplane workspace. Read the Project list from `~/.farplane/company.json`.
- Write only Farplane's own metric files under each Project's `.farplane/` (what the commands
  and refreshers below write). Never write GitHub, Notion, Whop, or any provider.
- Never spend. A metric whose source would cost money stays a gap.
- The only other writes go to Farplane-UI's Convex, all inside step 2's `farplane metrics refresh`: the
  metric readings, cash, and the tests' version totals.

## Steps

1. **The other refreshers.** For each Project whose `trackingContext` is its own Git checkout, follow
   every refresher in its `farplane/metrics.yaml` except `local_project_metrics` (step 2's command covers
   it): connected sources such as Whop billing, a company file or a platform API, and local ones such as
   `farplane harness health compile`. Write today's observations for the metrics each one `provides`. A
   source it can't read is a gap, never a zero. Run credentialed reads through `farplane run -- <command>`.
2. **Everything else, in one command:** `farplane run -- farplane metrics refresh --json`. For every
   company.json Project that is its own Git checkout it writes Core's primitive readings and the project
   snapshot for today (this machine's date), then pushes every snapshot's readings and today's company
   cash (the Whop balance of every bound Whop company, `company`/`cash`, source `whop`) to Convex
   `/metrics/readings`; reruns replace the same readings. It also counts every running test's versions
   from their sources since the test began (a Whop plan's paid sales out of its payment attempts, a set of
   Zernio posts' clicks out of their views; `bin/core/farplane_test_versions.py`) and records them on the
   test. Versions with no source are left to whoever runs that step (`office-ab outcome`). It skips a folder that is missing or not its
   own checkout and says why; a Project that fails is that Project's gap and the rest carry on. There is
   no bank feed: a cash gap is reported, never filled, and a balance the operator sends is recorded with
   `farplane run -- farplane metrics push --cash <USD>`. If Convex is unreachable the local snapshots
   still stand.

Final response:

- One line per Project: `refreshed` with the snapshot's source-gap count, `skipped` with the
  reason, or `failed` with the error's first line.
- Name any Project whose snapshot still has no metric readings at all.
- The push: readings sent per Project and for `company` (cash), or `failed` with its reason.
- `github_writes: none`.

Config source:
farplane/automations/metrics-refresh.md id="farplane-metrics-refresh"
