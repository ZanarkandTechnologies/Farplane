---
name: interval-update
description: "Turn one Daily or Weekly BAU review window into a dated problem report, bounded recovery tickets, and planner candidates."
tier: 3
group: harness
source: local
template_uses:
  skill-template: "0.2.0"
  skill-eval-task: "0.2.0"
eval: evals/evals.json
qa_checklist: qa_checklist.md
allowed-tools: Read, Glob, Grep, Bash

---

# Interval Update

## Context

Use this skill for one bounded Daily or Weekly BAU reporting automation. The
Codex app owns cadence. This skill compresses the completed review window into
a dated report, maintains a small Markdown `Problems` ledger, and surfaces
already-observed maintenance as planner candidates and may admit a bounded
recovery ticket when the cause and correction are already evidenced.

Interval does not choose new direction. It does not run Feed Scout, Dogfood
Review, reward check-ins, priority planning, leverage planning, harness
self-improvement, or ticket execution. Separate provider reports are evidence;
Work Pulse owns execution and due experiment check-ins; `plan_next_wave` owns
new BAU direction; the weekly self-improvement automation owns experiments.

Before reading any work-item or filesystem-board evidence, Interval loads
`farplane/bindings.yaml` when present and resolves exactly one kanban provider.
Every provider branch preserves the same outer contract: synthesize and
finalize the bounded report before recovery handoff, do not run the provider's
workflow, and do not start Goal, Pulse, a worker, or ticket execution.

## Skill Signature

```text
interval_update(project_root, interval_id, review_window, context_refs?,
                maintenance_ticket_limit = 1, write_policy?, now?,
                refresh_metrics = false, refresh_scope = "selected_stale")
  -> interval_report
   + problems
   + maintenance_candidates
   + recovery_ticket_paths[0..maintenance_ticket_limit]
   + metric_refresh_receipt?
   + source_gaps

state:
  reads(farplane/bindings.yaml?, farplane/harness.yaml?, farplane/metrics.yaml?,
        .farplane/metrics/**?, configured kanban evidence,
        .farplane/reports/pulse/**,
        .farplane/reports/interval/**,
        latest completed provider reports supplied through context_refs,
        review/run artifacts and project memory refs when supplied)
  writes(.farplane/reports/interval/<interval_id>/<timestamp>.md,
         optional recovery tickets after the report)

gates:
  interval_id in [daily, weekly] or explicit BAU profile;
  review_window_bound; report_written_before_candidate_handoff;
  problems_ledger_present; existing_failure_evidenced;
  recovery_scope_settled; maintenance_only; active_ticket_deduped;
  proof_and_stop_condition_named; recovery_only; ticket_cap_respected;
  no_new_direction; no_experiment_or_reward_mutation

routes:
  pulse-update | plan-next-wave | feed-scout | review

fails:
  planning new product, campaign, strategy, capability, or harness direction;
  running provider or self-improvement workflows; scoring ticket rewards;
  creating a new-direction or experiment ticket; emitting duplicate or
  unbounded maintenance candidates; executing work
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind one BAU report window.
  - [ ] Read `qa_checklist.md` before gathering evidence.
  - [ ] Resolve `project_root`, `interval_id`, `review_window`, optional
        `context_refs`, `maintenance_ticket_limit`, and write authority.
  - [ ] Run `scripts/resolve_evidence_binding.py --project-root <project_root>`.
        When `farplane/bindings.yaml` is present, obey
        `integrations.kanban.provider`, its non-secret coordinates, and
        `filesystem_ticket_policy`; do not infer a second board.
  - [ ] Use `daily` for recent BAU failures, drift, obligations, and provider
        signals; use `weekly` for repeated problems, completed/abandoned work,
        review load, resource use, and pending proof.
- [ ] 2. Build a compact evidence bundle.
  - [ ] For Daily only when `refresh_metrics = true`, resolve selected/pinned
        stale metric IDs through `scripts/metric_refresh.py refresh-plan`.
        Execute each returned refresh group once in the Interval agent context,
        let provider skills return partial readings or source gaps, and write
        flat observations before report synthesis. Weekly and disabled runs
        execute zero refresh groups. A provider gap never blocks the report.
  - [ ] Read the configured kanban evidence and Pulse/report evidence inside
        `review_window` plus the previous finalized report for carry-forward
        problems. A `filesystem_tickets` binding reads its configured project-
        relative directories. A `notion` binding resolves only its named handle
        from private Notion context and queries through `ntn`; normalize rows
        immediately and keep raw IDs, URLs, tokens, and private payloads out of
        tracked reports and tickets.
  - [ ] If the configured provider, private handle, CLI, credential, or compact
        query is unavailable, record a `source_gap`. When
        `filesystem_ticket_policy: exclude`, do not inspect or dedupe against
        `tickets/**` and do not fall back to it even when it exists. Still write
        the bounded report from available metrics, completed reports, prior
        finalized Interval evidence, and supplied `context_refs`.
  - [ ] Read only the latest completed Feed Scout or other provider report
        explicitly supplied through `context_refs`; missing inputs become
        source gaps and never trigger the provider.
  - [ ] Separate evidenced existing failures from observations, opportunities,
        and uncertain diagnoses before admission.
- [ ] 3. Write the dated report and Problems ledger.
  - [ ] Use `templates/interval-report.md` and write under
        `.farplane/reports/interval/<interval_id>/<timestamp>.md`.
  - [ ] Include Core report frontmatter: `ref`, `kind: interval-report`,
        `created_at`, and `ui_summary` plus the interval and review window.
  - [ ] Record each problem as a Markdown checkbox with evidence and optional
        ticket link; do not add finding IDs, frontmatter, or another registry.
  - [ ] Once finalized, treat the dated report as a snapshot and carry
        unresolved problems forward by link.
- [ ] 4. Surface known maintenance candidates after the report exists.
  - [ ] For each candidate, cite current or prior evidence that proves an
        existing failure rather than a speculative opportunity.
  - [ ] Require unresolved state, materiality, executable scope, no active
        duplicate, proof target, stop condition, and authority to write locally.
  - [ ] Keep eligible maintenance candidates in the report. A candidate may
        become a recovery ticket only when evidence proves an existing
        failure, the direct correction is known, an existing KPI/guard and proof
        route are named, no experiment is required, and no active duplicate exists.
  - [ ] Create or update at most `maintenance_ticket_limit` recovery tickets and
        link them to the Problems ledger. New direction, opportunities, and
        uncertain hypotheses remain candidates for the adaptive planner.
  - [ ] Do not start Goal, Pulse, a worker, or implementation.
- [ ] 5. Finish-check and return.
  - [ ] Apply `qa_checklist.md` again and index reports when the CLI is available.
  - [ ] Return the binding ref, selected provider, sanitized configured source,
        filesystem policy, and source gaps; for filesystem providers, state
        that work review and active-work dedupe used only the configured
        directories loaded after binding resolution.
  - [ ] Return report path, carried/new/resolved problems, maintenance
        candidates, recovery ticket paths, source gaps, and a no-execution receipt.
  - [ ] In the final chat response, summarize the report's decision content:
        report path, 2-4 key findings, tickets created or updated, each
        candidate's admission result and reason, operator-needed items, source
        gaps, and the no-execution receipt.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

- [templates/interval-report.md](templates/interval-report.md) - compact Daily
  or Weekly BAU report and Problems ledger.

## Gotchas

- A problem first observed in the current report may still be direct recovery
  when the evidence, correction, KPI/guard, proof, stop, and authority are all
  settled. Novelty alone never makes an uncertain diagnosis ticketable.
- A suggestion in a provider report is context, not automatically a known
  maintenance problem. Feed Scout also supplies candidates, not tickets.
- Provider selection is evidence routing, not permission to run another
  workflow. Notion reads stay read-only and bounded; recovery writes require a
  separately authorized provider write route and otherwise remain candidates.
- Weekly repetition increases confidence but does not grant broader authority.

## Reference Map

- [BAU interval contract](references/interval-update.md) - load for Daily versus
  Weekly profile detail, recovery admission, and carry-forward examples.
- [Parent run contract](references/parent-run-contract.md) - load for audits or
  caller integration checks; this `SKILL.md` remains runtime authority.
- [../pulse-update/SKILL.md](../pulse-update/SKILL.md) - owner of ticket
  execution and matured experiment check-ins.
- [../plan-next-wave/SKILL.md](../plan-next-wave/SKILL.md)
  - owner of new BAU direction when the board needs refill.

## Output

- One dated Daily or Weekly BAU report with a Markdown Problems ledger.
- Zero or more maintenance candidates plus bounded recovery tickets backed by
  evidence of an existing failure and requiring no experiment.
- Source gaps and a receipt that Interval did not plan direction, run providers,
  score experiments, or execute tickets.
- A sanitized provider-resolution receipt proving bindings were loaded before
  work-item evidence and naming the only source used for review and dedupe.
- A final chat receipt that makes the report readable without opening it: key
  findings, created/updated tickets, candidate decisions with reasons,
  operator-needed items, source gaps, and no-execution receipt.
