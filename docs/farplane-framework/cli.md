---
title: The Farplane command system
status: active
owner: harness
created_at: 2026-10-02
updated_at: 2026-10-02
refs:
  - bin/core/farplane_cli_parser.py
  - bin/README.md
  - farplane/automations/metrics-refresh.md
tags:
  - farplane
  - cli
  - agents
---

# The Farplane command system

How agents (and the operator) drive Farplane from a shell, and the rules any change to a command keeps.
Read this before adding, renaming or removing a `farplane` command, or before writing a skill or automation
that calls one. The operator asked for it to be "super intuitive" for agents (2 Oct 2026); this is the bar.

## The rules

1. **One command per job.** A command is named for the job an agent is doing, not for the module that
   implements it. A job that took several commands becomes one: Metrics Refresh was `metrics primitives`, then
   `project snapshot`, then `metrics push`; it is now `farplane metrics refresh`.
2. **`--help` reads as a map of jobs.** Commands are described by when they run: daily, weekly, on setup, to
   inspect, or by the operator (the map below). An agent reads it once and knows which command does the job.
3. **Dates are today on this machine's clock**, which is the operator's timezone (the Morning job runs at
   05:00 in Asia/Kuala_Lumpur, when UTC is still yesterday). Never default a date to UTC.
4. **Every command takes `--json`**, and an error says what to run next instead of only what went wrong.
5. **No aliases and no legacy names.** A renamed command updates every caller in the same change: skills,
   `farplane/automations/*.md`, `~/.claude/scheduled-tasks/*`, hooks, templates and docs. A command nothing
   calls is removed rather than kept "just in case".
6. **Defaults over flags.** `--project-root` defaults to the current folder; a job across every project reads
   the project list from `~/.farplane/company.json` (projects whose folder is its own Git checkout).
7. **Credentials go through `farplane run -- <command>`** (Doppler). Never print a secret.

## The map

| When | Command | The job |
| --- | --- | --- |
| Daily | `farplane run -- farplane metrics refresh` | Every project's readings and snapshot for today, then one push to Convex. `--project-root` for one project, `--no-push` to stay local, `--cash <USD>` to record a balance the operator reported |
| Weekly (Monday) | `farplane loop monday` | Each step plan's review and this week's routine tasks on its floor's queue (the operating loop; the bunker's `docs/prd.md`) |
| Daily, by Knowledge Update | `farplane wiki sync`, `farplane wiki search` | Keep the company Wiki projection current; find a page |
| Content | `farplane content add`, `farplane content list` | Record a published post in the content ledger (what `posts_published` counts); list them |
| Operator | `farplane metrics push --cash <USD>` | Record a cash balance read off the bank by hand (the bank has no API) |
| Setup | `farplane install`, `farplane doctor`, `farplane hooks`, `farplane ui link`, `farplane eval init` | Install and check Farplane on a machine |
| Inspect | `farplane skills rollout`, `farplane harness health`, `farplane lint` | Read the harness's state; nothing is written |
| Secrets | `farplane run -- <command>` | Run anything that needs the project's credentials |

Inside the bunker office, agents also have the office's own commands, each scoped to the agent's floor and
desk: `office-queue` (Recruitment), `office-ab` (A/B tests), `office-whiteboard` (the board, its chat and its
suggestions, including `--system step-plan`). They follow the same rules.

## In progress

The simplification is tracked in [ZanarkandTechnologies/Farplane#32](https://github.com/ZanarkandTechnologies/Farplane/issues/32).
Done so far:

- `farplane metrics refresh` replaces the three-command daily sequence (`metrics primitives` and `project
  snapshot` stay available for one project and a past date until nothing calls them directly).
- `metrics primitives` and `project snapshot` default to today on this machine's clock, not UTC.
- `farplane --help` opens with the jobs map (kept in `bin/core/farplane_cli_base.py` `JOBS`, in step with
  this doc).
- The `bank` alias is gone (the 2026-09-24 cleanup catalog found nothing calls it); use `resource-bank`.

- Also done after the caller audit (comment on #32): `harness health compile` and `project snapshot
  --timezone` default to this machine's date and timezone; `capability-profiles` and `content` accept
  `--json` (they always print JSON); a `CliError` prints `{"ok": false, "error": …}` under `--json`; a group
  run without its subcommand prints that group's help; the `delegate` command, the unreachable
  `resource-bank` parser entry (it is still delegated to Farplane-UI before parsing) and the duplicate
  `capability-profiles resolve` are gone.

**Kept, because running software calls them** (the audit's evidence): `adoption scan`, `skills rollout scan`,
`capability-profiles read/write/snapshot` and `mining` (Farplane-UI's server), `hooks list/install`
(Farplane-UI's install script), `extension youtube` (shown to the operator by Farplane-UI).

Still open:

- `ticket` and `tickets` work on the legacy `tickets/` files, but the `close-ticket`, `impl-plan`,
  `goal-advisor`, `dogfood-review` and `pulse-update` skills still name them; retiring them means moving
  those skills to GitHub Issues first (its own issue).
- `notify` and `reports` have no live caller but are documented operator tools; ask before removing.
- `content add` defaults `--project-root` to the Farplane checkout, not the current folder (the
  `x-account` and `instagram-account` skills rely on that); decide with the content ledger's owner.
- Farplane-UI's file-change hook calls a `mining handle-file-change` subcommand that doesn't exist (the
  hook isn't wired anywhere); a Farplane-UI fix.
