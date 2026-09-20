---
schema: farplane_project_automation
framework_template_version: 1.0.0
owner: automation-advisor
id: farplane-weekly-interval
name: Farplane Weekly Operating Review
kind: cron
status: active
target:
  workspace: /Users/kenjipcx/Zanarkand Technologies/projects/Farplane
schedule:
  type: weekly
  timezone: Asia/Kuala_Lumpur
  days:
  - Mon
  time: 05:45
---
Task storage override: follow tickets/README.md. Multica is dashboard-only;
resolve project bindings, keep issues unassigned, and use --no-start for updates.
Create/update task records through the existing Multica CLI, never ticket.md.
Do not invoke filesystem materializers, finalizers or dispatch based on local
migration snapshots. If a phase requires such a legacy adapter, report that
phase as unavailable; continue independent read-only reporting. Never start
Multica agents, squads, autopilots or runs.

Use $pm-weekly.

Run the Farplane adaptation of Zanarkand AI's four-step Company OS Weekly.

1. Fetch all context. Freeze the previous completed week, the next week, and
   the exact Multica Project inventory. Resolve Projects only through their
   project-local `farplane/bindings.yaml#integrations.multica.project_id`.
   Collect every expected Project Memory file, Daily coverage and extraction
   receipt, prior weekly report, and each Project's existing Multica issue
   inventory with current revisions. Preserve source revisions and content
   hashes. Paginate provider reads; incomplete Project coverage remains a
   blocking gap.
2. Save the complete frozen weekly context under
   `.farplane/company-os/weekly/context/<run-id>/`, including Project and issue
   inventories, coverage, issue revisions, source revisions, hashes, and
   adjacent source caches.
3. Run `$pm-weekly` once over that local set. The skill reads no provider and
   writes exactly `.farplane/company-os/weekly/extractions/<run-id>.json`.
4. Validate complete Project coverage, JSON shape, source refs, the exact
   action type/payload allowlist, frozen issue membership, expected revisions,
   and blockers before any effect. A missing Project, malformed result, unknown
   or extra action field, or stale source blocks mutation. Render Project and
   company reports under
   `.farplane/company-os/weeks/<week>/reports/`, carry the accepted commitments
   into next week's Project Memory, and apply only exact authorized actions to
   existing Multica issues. Reread before mutation, block duplicates or stale
   revisions, use `--no-start`, keep issues unassigned, and read back changes.

Do not create tickets, invent business strategy, promote broad knowledge, send
external messages, or execute work. No deploy, publish, spend, customer contact,
account mutation, destructive cleanup, or private-data expansion.

Return context/extraction/report paths, coverage, money movement, constraints,
next-week commitments, applied/duplicate/blocked action receipts, source gaps,
and operator-needed decisions. State `multica_execution: none`.

Config source:
farplane/automations/weekly-operating-review.md id="farplane-weekly-interval"
