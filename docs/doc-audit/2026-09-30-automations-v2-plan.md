# Automations v2 on Claude: implementation plan — 2026-09-30

The one doc for Farplane's automations: the catalog, what's live, and what's still open. It
replaces the 24 Sep automation-loop handoff, whose open items are folded in below. The bunker's own
product doc is `Farplane-UI-v2/docs/prd.md`. Operator decision (2026-09-30): pause the Codex
automations and run the jobs on Claude Code.

**Architecture rule:** collectors are the only jobs that read providers. Skills are pure (files in,
JSON out). Only apply steps write back, rereading before each write. Every run ends with a completion
marker, and consumers ignore unfinished runs. A source with a single consumer (feeds, bookmarks) keeps
its fetch inside that consumer.

**Operating flow:** define goals, plan the critical path, execute. There's no self-discovery strategy
loop: strategy changes are A/B tests seeded from proven outside examples. Killed: Weekly
Self-Improvement, Monthly Registry Consolidation, and the autoresearch and autostrategy loops.

## Contract

```text
Claude scheduled task (thin prompt: "run farplane/automations/<record>.md")
  -> the record (one owner of steps, sources, write policy)
  -> skills ($name = the Claude skill of the same name)
  -> dated files + completion marker -> the next job reads the newest complete run
```

- One owner per job: the record in `farplane/automations/`. The scheduled task names the
  record and adds nothing but runtime notes, so prompts never fork again (the Codex TOMLs
  were copies that drifted).
- Codex keeps its automation folders, all paused, as a rollback.
- Scheduled tasks run while the Claude app is open; a missed run fires on next launch.
- Readers start an hour after Fetch Context (the scheduler adds a few minutes of jitter), and
  block rather than fetch when no complete run under 12 hours old exists.

## Phase 1 — live today (this plan)

| Job (Catalog v2) | Record | Claude task | When (KL) |
|---|---|---|---|
| Fetch Context | `daily-collect.md` | `farplane-fetch-context` | daily 05:00 |
| Knowledge Update | `knowledge-update.md` | `farplane-knowledge-update` | daily 06:00 |
| Progress Updater | `daily-operating-update.md` | `farplane-progress-updater` | daily 06:15 |
| Intel Digest (bookmarks first) | `bookmark-recovery.md` | `farplane-intel-digest` | daily 23:15 |
| Session Friction Retro | `weekly-thread-friction-audit.md`, now daily | `farplane-session-friction-retro` | daily 23:40 |
| Report Gen | `weekly-operating-review.md` | `farplane-report-gen` | Mon 05:45 |
| Profile Refresh | Codex `monthly-operator-profile-refresh` prompt | `farplane-profile-refresh` | 1st of month 09:00 |

Record changes: status `active` for the six above; the friction record becomes daily
(`window = last_24h`, name Session Friction Retro); Daily Collect's Agent sessions row
already indexes Claude Code transcripts.

Codex: pause `farplane-daily-interval`, `farplane-weekly-interval`,
`farplane-weekly-thread-friction-audit`, `monthly-operator-profile-refresh` and
`zanarkand-weekly-office-showcase-draft` (Report Gen absorbs the showcase).

Stay paused: Task Runner (`work-pulse`, until a plan exists), Feed Scout (it files Multica
recovery tickets; merges into Intel Digest in Phase 2), Weekly Self-Improvement and Monthly
Registry Consolidation (killed).

**Proof (2026-09-30, done):** Fetch Context wrote `20260930T080451Z` with its `_run.json`
marker (status `partial`: three client Projects have no local binding). Knowledge Update read it
and no-oped (no new calls). Progress Updater rendered W40 Project Memory for four Projects with no
Multica actions due. Intel Digest read the bookmarks in the browser: two candidates, no person
matches.

## Phase 2 — skill updates (next)

| Change | Why | Size |
|---|---|---|
| ~~Rename `pm-daily` → `progress-update`, `pm-weekly` → `report-gen`~~ **done 2026-09-30**: skills, 34 referencing files, registry sync, snapshot, Claude + Codex links | Catalog v2 names; one current name | ~50 files |
| Rename records/ids to the catalog names (`fetch-context`, `session-friction-retro`, …) | same | records + tests |
| `extract-friction` skill out of the friction record | daily rows feed Report Gen | new skill |
| ~~Intel Digest = Feed Scout + bookmarks~~ **done 2026-10-01**: the Intel Digest task runs both records (Feed Scout without paid scraping or issues), and the office's Intel panel shows Feed Scout's latest watch (Farplane-UI-v2 `8a096e1`). Still to do: `match-plays` and one store with `intelligest` | open question 3 | record + skill |
| Metrics Refresh record | metrics need `fetch` lines first (none in `farplane/metrics.yaml`; the company goal metrics are in the Wiki) | record |
| Chain by completion markers, not clock offsets | open question 4 | records |

Open, operator's call: Multica bump-to-start (question 1), where the check-in list lives
(question 2).

## Decision 2026-10-01: GitHub Issues replace Multica

Operator: "we no longer use Multica; everything in this office is Claude." Accepted model:

- **Projects:** `~/.farplane/company.json` (what the bunker reads) replaces Multica's inventory.
- **Tasks:** open GitHub issues (and PRs) of each project's own repo. A project with no repo has
  no task source, recorded as a gap.
- **One label:** `check-in`, with a `Due: YYYY-MM-DD` line; every other issue is just work.
  Issues a job opens say so in their first line.
- **Writes:** Progress Updater and Report Gen may only comment on existing issues. They never
  create, close, label or assign, and never start agents.
- **Privacy:** Farplane, Farplane-UI and farplane-bunker are public, so they take engineering
  issues only; comments there carry no clients, money, prices, strategy or personal details.
  Client and business work goes in private repos (updated below).
- **Multica:** frozen as a read-only archive; its 48 issues aren't migrated. One is recreated on
  GitHub only when its work resumes.

Turned down: typing every issue (`build`, `recovery`, `strategy`), since no job filters on them;
strategy steps as issues, since they'd land in public repos (they stay in the private Wiki's setups,
drawn on the heist board); a check-in ledger file (two places to look).

Still open: private repos for the businesses and for the clients that don't have one yet.

Applied 2026-10-01:
- **Changed:** all ten records and their recipes, `progress-update` and `report-gen`,
  `tickets/README.md`, `AGENTS.md`, and `bindings.yaml` (`kanban.provider: github_issues`, which the
  validator now accepts). The README's "Active queue" line and its doc-parity rule changed too.
- **Label:** `check-in` added to the Farplane repo.
- **Status and priority:** these changes become local `proposed` items; only comments reach GitHub.
- **Task Runner (`work-pulse`):** stays paused. Its `$pulse-update` still creates and dispatches
  tickets, so it needs a redesign around the bunker's Queue before it runs again.

Update 2026-10-01 (later): private repos, corrected to the operator's model. Client deployments
are not businesses: they're deployments and products of one AI deployments service. Their tasks go
in their own private repos, registered in `~/.farplane/company.json`. Client names stay there, not
in this public repo.
Still open: where business-level follow-ups live; asked of the screen-redesign thread, which holds
the business model.

Update 2026-10-01 (later still): projects can start without a repo. `company.json` projects carry
`kind` and `business`; a project with no repo uses its private checklist
(`~/.farplane/projects/<slug>/checklist.md`, template `docs/templates/project-onboarding-checklist.md`)
as its task source in Fetch Context. Progress Updater lists due checklist items and unchecked
onboarding steps. The business map is in the private strategy folder, not here.

Update 2026-10-01 (superseded the checklist route): every project gets a GitHub repo, private by
default. The onboarding checklist is one pinned `Onboarding: <name>` issue labelled `onboarding`
(template `docs/templates/project-onboarding-checklist.md`), read like any issue; dated follow-ups
are `check-in` issues. A project with no GitHub remote records `task_source: none` as a gap. The
two checklist projects now have private repos, and `~/.farplane/projects/` moved to
`~/.farplane/archive/`.

## Still open (from the 24 Sep handoff)

- **How much AI the Progress Updater needs.** The proposal has three tiers:
  1. **Rules** (a script): stale reviews, blocked without a comment, overdue, missing proof, commits
     without an issue.
  2. **A fast model, as a yes/no batch:** an unanswered question and who it's for, waiting on a
     person, handoff-ready docs.
  3. **A reasoning model, weekly:** the narrative, the constraint nearest revenue, plan vs actual,
     and the next commitment.

  Recent daily runs mostly said "unchanged".
- **Trim the Progress Updater's prompt.** About a third of its checklist is real guards; the existing-issue
  allowlist and the revision check should become a validator. The rest repeats `tickets/README.md`
  and the skill. Keep "activity is not movement" and "gaps are not empty".
- **Plan vs actual** belongs in Report Gen (planned vs unplanned work, missed goals and why). It needs
  the operator's plan in the collected context.
- **Conversation mining:** a daily batch over Claude and Codex transcripts and closed issues, sorting
  friction, decisions, commitments, skill gaps and learnings into project memory and the Wiki. It
  would reuse the `farplane mining` engine without its finalize trigger.
- **Leverage chain:** Knowledge Extract after Fetch Context (call notes → person, company, problem and
  resource updates; business facts only), and Intel Digest ending in `match-plays` (at most 3 plays a
  day, each with a reason and both sources). Report Gen lists the plays sent, accepted and their outcome.
- **The match window:** problems older than 30 days drop out of matching unless flagged `ongoing` or
  `size: big`. Decide whether older open client problems should be flagged.
- **X bookmarks:** the browser is the X source. The API path needs one operator re-authorization to
  save rotated tokens to `~/.farplane/state/x-oauth2.json`.

Update 2026-10-01: office propagation checked. Intel (bookmark inbox, now plus Feed Scout's watch),
Wiki graph/Clients/Mission (Knowledge Update's pages), Weekly report (Progress Updater's project memory),
New projects easel (checklists) read the jobs' files. The Mission board and Weekly report only matched the
old weekly friction file name; they now read the daily retro too (Farplane-UI-v2 `93e0d57`), and the retro
writes the headline they parse. Blocker: scheduled runs stop at their first tool permission prompt until
each job's tools are approved once with "Always allow" (or allowed in settings), which is the operator's call.

## Decision 2026-10-01 (evening): minimal data and jobs

Operator decisions. The canonical list is in Farplane-UI-v2 `docs/prd.md` Notes.

- **Tasks:** GitHub Issues only; every project gets a repo (private by default). Business checklists
  retire once the two businesses have repos.
- **Goals and critical paths:** the mission board / whiteboard; Notion stays the operator's input.
- **Captures:** Convex, through intelligest (media goes to Content, "use this" to the Resource Bank).
- **Numbers:** `farplane/metrics.yaml` per repo.
- **A/B:** one `ab/` store.
- **Telemetry:** Convex.

Applied:

- **Morning job:** one job runs Fetch Context → Metrics Refresh → Knowledge Update → Progress Updater in
  order (`farplane-morning`, 05:00). The four separate tasks are disabled, not deleted.
- **Pace check:** Progress Updater gained it, writing replan proposals; re-dating the operator's own
  steps may apply automatically.
- **Telemetry:** runtime events now post to the Convex site's `/ingest` when no explicit endpoint is set
  (`bin/runtime/runtime_telemetry.py`), so they reach Convex like the hook events. The local log stays
  only because `farplane metrics primitives` and project snapshots read it. Making Convex the only
  copy needs those readers moved to Convex first.

Next:

- The A/B merge.
- Captures into Convex: the Clipper and Bookmark Recovery send through intelligest with the UI fields
  as its prompt and parameters, and Library/Intel read Convex.
- Private repos for the two businesses, once the operator says yes.
- Task Runner rebuilt on the bunker's Queue.
