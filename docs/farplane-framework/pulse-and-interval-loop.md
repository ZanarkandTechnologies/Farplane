---
title: "Work Pulse And Company OS Reviews"
status: active
owner: farplane-framework
created_at: 2026-06-29
updated_at: 2026-09-20
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
Project, freezes one local input bundle per Project, and calls `pm-daily` once
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
Project Memory. It calls `pm-weekly` once over that set. Missing Project
coverage blocks effects. The automation validates and renders the Project and
company reports, applies authorized updates to existing issues, and reads back
every effect.

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

- Desired and live Daily prompts call `pm-daily` once per eligible Project.
- Desired and live Weekly prompts call `pm-weekly` once over complete coverage.
- Exactly one Work Pulse heartbeat owns execution.
- PM skills have no provider access and emit one structured local result.
