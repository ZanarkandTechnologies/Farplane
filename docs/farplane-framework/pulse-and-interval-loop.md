---
title: "Morning Chain And Weekly Review"
status: active
owner: farplane-framework
created_at: 2026-06-29
updated_at: 2026-10-14
framework_template_version: "0.3.0"
tags:
  - farplane
  - lifecycle
  - automations
  - company-os
refs:
  - docs/farplane-framework/README.md
  - docs/prd.md
  - docs/farplane-framework/ticket-execution-loop.md
  - docs/features/FEAT-0067-daily-interval-review-reports.md
  - farplane/automations/morning.md
  - farplane/automations/report-gen.md
---

# Morning Chain And Weekly Review

Farplane has no execution heartbeat. Work Pulse, the former heartbeat, was
retired on 2026-10-12 (#41). Scheduled
jobs are cron records in `farplane/automations/` that run as Claude scheduled
tasks (`runtime: claude`). They collect, report and propose; they never create,
close, label, assign or edit issues and never start agents or runs.

Farplane's own `farplane/automations/` holds the portfolio Morning and weekly
records. Each managed repository is an ordinary project with a thin `farplane/`
adapter; it does not receive another copy of those portfolio reviews.

```text
Morning (daily)   -> collect, refresh metrics and knowledge, update Project Memory, write the brief
Report Gen (weekly) -> compare the full portfolio and carry next-week commitments
Execution         -> operator, or a session they start, runs goal-advisor on a GitHub issue
```

## Execution

Work enters as a GitHub issue in the project's own repository. Execution starts
when the operator, or a session they start, runs `goal-advisor` on the issue
(native Goal); small work runs directly. Completion is one proof comment and
`gh issue close` (`tickets/README.md`).

Due check-ins are open issues labelled `check-in` with a `Due: YYYY-MM-DD`
line. Daily Collect lists them and the morning brief surfaces them; the
operator, or a session they start, resumes that Goal with `goal-advisor`'s
Delayed Check-In Resume prompt.

## Morning

[Morning](../../farplane/automations/morning.md) runs its steps in order in one
session; the record owns the exact chain:

1. [Daily Collect](../../farplane/automations/steps/daily-collect.md) fetches
   GitHub issues, Git, the operator plan, call notes, and agent-session indexes
   once and freezes them as a dated run.
2. [Metrics Refresh](../../farplane/automations/steps/metrics-refresh.md)
   refreshes every registered Project's metric readings.
3. [Knowledge Update](../../farplane/automations/steps/knowledge-update.md)
   turns the run's call notes into local Wiki pages.
4. [Daily Operating Update](../../farplane/automations/steps/daily-operating-update.md)
   calls `report-gen` in `daily` mode once per eligible Project. The skill reads
   project-local Farplane configuration and evidence, then emits one JSON
   extraction describing:
   - the operator-defined commercial bet and next monetization event;
   - observed result movement, with unknowns kept unknown;
   - the constraint closest to that event; and
   - one smallest useful commitment against existing authorized work.

   The automation validates the extraction, updates the existing Project Memory
   section, applies any authorized existing-issue comment, and reads the result
   back. It does not create work or execute it.
5. The morning brief reads the run, metric, Wiki, and Project Memory changes and
   due check-ins, and writes one private brief.

## Weekly Report Gen

[Report Gen](../../farplane/automations/report-gen.md) freezes a complete
Project inventory and the full week of Project Memory. It calls `report-gen`
once over that set. Missing Project coverage blocks effects. The automation
validates and renders the Project and company reports, folds in the week's
Session Friction Retro reports, applies authorized comments on existing issues,
and reads back every effect.

## Scheduled work by purpose

Jobs live in `farplane/automations/`, one file per live routine; the steps they
call live in `farplane/automations/steps/` and are never scheduled on their
own. This table catalogs them; the linked records remain the exact schedule and
prompt owners.

| Record | Purpose | Main result |
| --- | --- | --- |
| [Morning](../../farplane/automations/morning.md) | Daily collect, metrics, knowledge, and Project review chain | Dated run, Project Memory, bounded existing-issue comments, morning brief |
| [Report Gen](../../farplane/automations/report-gen.md) | Compare the full Project portfolio and carry forward commitments | Project and company reports, next-week memory |
| [Intel Digest](../../farplane/automations/intel-digest.md) | Run [Bookmark Recovery](../../farplane/automations/steps/bookmark-recovery.md), then [Feed Scout](../../farplane/automations/steps/feed-scout.md) | Bookmark candidate inbox, dated Feed Scout report and Scout Brief |
| [Session Friction Retro](../../farplane/automations/session-friction-retro.md) | Review the day's agent sessions for agent and operator interaction friction | Dated correction and friction report, read by the weekly review |
| [Profile Refresh](../../farplane/automations/profile-refresh.md) | Refresh the operator profile after the weekly report | Updated operator profile |
| [Token Burn](../../farplane/automations/token-burn.md) | Use leftover usage before the weekly reset | Local-only commits and a dated report |
| [Thread Sweeper](../../farplane/automations/thread-sweeper.md) | Every 2 hours in waking hours, find agent threads that went quiet unfinished | Nudges to stalled threads, one Telegram list of what waits on Kenji, dated report |

The automation owns provider access, collection, frozen input files, validation,
rendering, external effects, and readback. Its skill interprets those files and
writes one structured result file. This boundary matters when the same judgment
could be rerun on frozen evidence, audited, or safely withheld from provider
effects. It does not require a new skill for every small deterministic mapping.

Conversation-to-Work alignment is an unimplemented PM evidence source. A first
slice should match accessible conversations to exact Projects and Work using
supported identifiers, record coverage and unmatched conversations, and
distinguish discussion, decision, deliverable, and verified result. Daily could
surface consequential drift against the current commitment; Weekly could
summarize repeated allocation patterns across the complete Project set. Message
volume and elapsed chat time alone do not prove progress or wasted effort.

## Boundary

```text
provider reads + pagination + caching        -> automation
commercial interpretation + next commitment -> report-gen skill
rendering + stale-write guard + effects      -> automation
issue execution                              -> operator or session via goal-advisor
```

Daily and Weekly may comment on authorized existing issues. They cannot create,
close, label, assign or edit issues, start agents or runs, invent strategy,
broadly promote knowledge, contact external parties, spend money, deploy, or
perform destructive actions.

The former Interval skill, weekly draft, promotion machinery, and recovery
admission path are deleted. Reusable metric reading lives in
`bin/core/farplane_metric_refresh.py`; it is a deterministic helper rather than
a separate operating loop.

## Proof

- The desired Morning chain calls `report-gen` `daily` once per eligible Project.
- The desired weekly record calls `report-gen` `weekly` once over complete coverage.
- No execution heartbeat exists; GitHub Issues hold work state.
- PM skills have no provider access and emit one structured local result.
