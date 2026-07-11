---
name: interval-update
description: "Turn one Daily or Weekly BAU review window into a dated problem report and bounded resurfacing of already-evidenced maintenance."
tier: 3
group: harness
source: local
template_uses:
  skill-template: "0.2.0"
  skill-eval-task: "0.1.0"
eval: eval_task.json
qa_checklist: qa_checklist.md
allowed-tools: Read, Glob, Grep, Bash

---

# Interval Update

## Context

Use this skill for one bounded Daily or Weekly BAU reporting automation. The
Codex app owns cadence. This skill compresses the completed review window into
a dated report, maintains a small Markdown `Problems` ledger, and may resurface
already-observed maintenance as bounded ticket deltas.

Interval does not choose new direction. It does not run Feed Scout, Dogfood
Review, reward check-ins, priority planning, leverage planning, harness
self-improvement, or ticket execution. Separate provider reports are evidence;
Work Pulse owns execution and due experiment check-ins; `plan_next_wave` owns
new BAU direction; the weekly self-improvement automation owns experiments.

## Skill Signature

```text
interval_update(project_root, interval_id, review_window, context_refs?,
                maintenance_ticket_limit = 0, write_policy?, now?)
  -> interval_report
   + problems
   + maintenance_ticket_deltas[0..maintenance_ticket_limit]
   + source_gaps

state:
  reads(farplane/harness.md?, farplane/goals.yaml?, farplane/metrics.yaml?,
        tickets/**, .farplane/reports/pulse/**,
        .farplane/reports/interval/**,
        latest completed provider reports supplied through context_refs,
        review/run artifacts and project memory refs when supplied)
  writes(.farplane/reports/interval/<interval_id>/<timestamp>.md,
         optional tickets/TASK-XXXX/ticket.md only after the report and only
         for eligible prior-evidenced maintenance)

gates:
  interval_id in [daily, weekly] or explicit BAU profile;
  review_window_bound; report_written_before_ticket_delta;
  problems_ledger_present; same_run_discovery_ledger_only;
  prior_evidence_required; maintenance_only; active_ticket_deduped;
  proof_and_stop_condition_named; ticket_cap_respected;
  no_new_direction; no_experiment_or_reward_mutation

routes:
  pulse-update | ticket-opportunity-generator | feed-scout | review

fails:
  planning new product, campaign, strategy, capability, or harness direction;
  running provider or self-improvement workflows; scoring ticket rewards;
  creating a ticket for a problem first observed in the same report;
  creating duplicate or unbounded maintenance tickets; executing created work
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind one BAU report window.
  - [ ] Read `qa_checklist.md` before gathering evidence.
  - [ ] Resolve `project_root`, `interval_id`, `review_window`, optional
        `context_refs`, and `maintenance_ticket_limit`.
  - [ ] Use `daily` for recent BAU failures, drift, obligations, and provider
        signals; use `weekly` for repeated problems, completed/abandoned work,
        review load, resource use, and pending proof.
- [ ] 2. Build a compact evidence bundle.
  - [ ] Read tickets and Pulse/report evidence inside `review_window` plus the
        previous finalized report for carry-forward problems.
  - [ ] Read only the latest completed Feed Scout or other provider report
        explicitly supplied through `context_refs`; missing inputs become
        source gaps and never trigger the provider.
  - [ ] Separate `prior_evidence` from `same_run_discovery` before admission.
- [ ] 3. Write the dated report and Problems ledger.
  - [ ] Use `templates/interval-report.md` and write under
        `.farplane/reports/interval/<interval_id>/<timestamp>.md`.
  - [ ] Include Core report frontmatter: `ref`, `kind: interval-report`,
        `created_at`, and `ui_summary` plus the interval and review window.
  - [ ] Record each problem as a Markdown checkbox with evidence and optional
        ticket link; do not add finding IDs, frontmatter, or another registry.
  - [ ] Keep same-run discoveries ledger-only. Once finalized, treat the dated
        report as a snapshot and carry unresolved problems forward by link.
- [ ] 4. Optionally resurface known maintenance after the report exists.
  - [ ] For each candidate, prove it was already observed in a prior finalized
        report, ticket, review, or run artifact; current-report evidence alone
        is insufficient.
  - [ ] Require unresolved state, materiality, executable scope, no active
        duplicate, proof target, stop condition, and authority to write locally.
  - [ ] Create or update at most `maintenance_ticket_limit` tickets and link
        them back to the Problems ledger. These are corrective maintenance,
        never a new direction or experiment.
  - [ ] Do not start Goal, Pulse, a worker, or ticket implementation.
- [ ] 5. Finish-check and return.
  - [ ] Apply `qa_checklist.md` again and index reports when the CLI is available.
  - [ ] Return report path, carried/new/resolved problems, created or updated
        maintenance ticket paths, source gaps, and a no-execution receipt.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

- [templates/interval-report.md](templates/interval-report.md) - compact Daily
  or Weekly BAU report and Problems ledger.

## Gotchas

- A source can be new to the current report while the problem is old. Admission
  depends on a cited prior finalized artifact, not on when the agent noticed it.
- A suggestion in a provider report is context, not automatically a known
  maintenance problem. Feed Scout owns its own source-backed ticket projection.
- Weekly repetition increases confidence but does not grant broader authority.

## Reference Map

- [BAU interval contract](references/interval-update.md) - load for Daily versus
  Weekly profile detail, prior-evidence admission, and carry-forward examples.
- [Parent run contract](references/parent-run-contract.md) - load for audits or
  caller integration checks; this `SKILL.md` remains runtime authority.
- [../pulse-update/SKILL.md](../pulse-update/SKILL.md) - owner of ticket
  execution and matured experiment check-ins.
- [../ticket-opportunity-generator/SKILL.md](../ticket-opportunity-generator/SKILL.md)
  - owner of new BAU direction when the board needs refill.

## Output

- One dated Daily or Weekly BAU report with a Markdown Problems ledger.
- Zero or more bounded maintenance ticket deltas backed by evidence that
  predates the current report, never exceeding `maintenance_ticket_limit`.
- Source gaps and a receipt that Interval did not plan direction, run providers,
  score experiments, or execute tickets.
