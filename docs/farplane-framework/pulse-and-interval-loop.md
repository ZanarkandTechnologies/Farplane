---
title: "Work Pulse And Company OS Reviews"
status: active
owner: farplane-framework
created_at: 2026-06-29
updated_at: 2026-09-23
framework_template_version: "0.3.0"
tags:
  - farplane
  - lifecycle
  - automations
  - pulse
  - company-os
refs:
  - docs/farplane-framework/README.md
  - docs/prd.md
  - docs/farplane-framework/ticket-execution-loop.md
  - docs/features/FEAT-0071-project-work-pulse.md
  - docs/features/FEAT-0067-daily-interval-review-reports.md
---

# Work Pulse And Company OS Reviews

Farplane has one execution loop and one operating-review loop.

The AI Office owns one Daily and one Weekly record in `farplane/automations/`.
Each managed repository is an ordinary project with a thin `farplane/`
adapter; it does not receive another copy of those portfolio reviews.

```text
Work Pulse heartbeat -> reconcile and execute accepted Multica work
Company OS Daily     -> refresh each project's operating memory
Company OS Weekly    -> compare the full portfolio and commit the next week
```

## Work Pulse

Work Pulse is the sole heartbeat and execution owner. It reconciles existing
Multica issues, resumes accepted work, requests due review, and refills a thin
queue only through the configured planning skills. It does not produce the
Daily or Weekly operating review.

## Company OS Daily

The Daily cron fetches the bounded provider context, splits it by eligible
Project, freezes one local input bundle per Project, and calls `progress-update` once
per bundle. The skill reads project-local Farplane configuration and evidence,
then emits one JSON extraction describing:

- the operator-defined commercial bet and next monetization event;
- observed result movement, with unknowns kept unknown;
- the constraint closest to that event; and
- one smallest useful commitment against existing authorized work.

The automation validates the extraction, updates the existing Project Memory
section, applies any authorized existing-issue action, and reads the result
back. It does not create work or execute it.

## Company OS Weekly

The Weekly cron freezes a complete Project inventory and the full week of
Project Memory. It calls `report-gen` once over that set. Missing Project
coverage blocks effects. The automation validates and renders the Project and
company reports, applies authorized updates to existing issues, and reads back
every effect.

## Scheduled work by purpose

All configured records live in `farplane/automations/`, including the AI
Office's PM pair. Root `automations/` holds reusable recipes. This table catalogs their jobs; the
linked Markdown records remain the exact schedule and prompt owners.

| Record | Purpose | Main result | Relationship to PM |
| --- | --- | --- | --- |
| [Daily collect](../../farplane/automations/daily-collect.md) | Fetch Multica, Git, the operator plan, and agent-session indexes once | Dated context run with coverage | Owns all shared provider reads |
| [Daily operating update](../../farplane/automations/daily-operating-update.md) | Review each Project's results, blockers, and next commitment | Project Memory and bounded existing-issue updates | Owns daily Project interpretation |
| [Weekly operating review](../../farplane/automations/weekly-operating-review.md) | Compare the full Project portfolio and carry forward commitments | Project and company reports, next-week memory | Owns weekly prioritization and proposals |
| [Work Pulse](../../farplane/automations/work-pulse.md) | Reconcile and execute accepted Work | Ticket and worker receipts | Executes admitted work; the only heartbeat |
| [Bookmark Recovery](../../farplane/automations/bookmark-recovery.md) | Recover personal saves and match them to current Project Memory | Local candidate inbox and hypothetical Project links | Supplies optional research leads; currently paused |
| [Feed Scout](../../farplane/automations/feed-scout.md) | Monitor configured external and competitor sources | Dated report, Scout Brief, candidate interventions | Supplies source-backed planning context |
| [Weekly Thread Friction Audit](../../farplane/automations/weekly-thread-friction-audit.md) | Review Codex conversations for agent and operator interaction friction | Dated correction and friction report | Specialized behavior review; currently does not compare conversation allocation with Project Work |
| [Weekly Self-Improvement](../../farplane/automations/weekly-self-improvement.md) | Review self-improvement ticket and Reward evidence | Dated Dogfood portfolio checkpoint | Supplies planner context, not Project operating evidence |
| [Monthly Registry Consolidation](../../farplane/automations/monthly-registry-consolidation.md) | Find stale, duplicate, and wrongly owned registry entries | Dated maintenance report | Harness maintenance outside PM |

The Thread Friction Audit record calls `$gap-analysis`, but this checkout and
the installed skill directory currently contain no `gap-analysis/SKILL.md`.
Its desired schedule is visible; successful execution is unverified until the
skill binding is repaired.

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
The separate Thread Friction Audit can continue to study interaction failures.

## Boundary

```text
provider reads + pagination + caching        -> automation
commercial interpretation + next commitment -> PM skill
rendering + stale-write guard + effects      -> automation
ticket execution                             -> Work Pulse
```

Daily and Weekly may update authorized existing issues. They cannot admit new
tasks, start Multica runs, invent strategy, broadly promote knowledge, contact
external parties, spend money, deploy, or perform destructive actions.

The former Interval skill, weekly draft, promotion machinery, and recovery
admission path are deleted. Reusable metric reading lives in
`bin/core/farplane_metric_refresh.py`; it is a deterministic helper rather than
a separate operating loop.

## Proof

- Desired and live Daily prompts call `progress-update` once per eligible Project.
- Desired and live Weekly prompts call `report-gen` once over complete coverage.
- Exactly one Work Pulse heartbeat owns execution.
- PM skills have no provider access and emit one structured local result.
