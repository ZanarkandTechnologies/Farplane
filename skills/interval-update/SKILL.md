---
name: interval-update
description: "Turn one Daily or Weekly evidence window into a control-loop report, a current weekly draft, and selectively promoted project knowledge."
tier: 3
group: operations
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

Use this skill as the parent Daily or Weekly control loop. One bounded evidence
bundle feeds reporting and independent candidate lanes. Daily writes an
immutable window report, upserts source-linked findings into the current weekly
working draft, and may apply only explicitly supported mutable task progress.
It does not promote problems or durable knowledge.

Weekly reads that draft and completed Daily receipts, gives every candidate a
disposition, freezes the weekly report, applies only authorized promotions to
canonical owners, writes the observed-result receipt, and opens the next draft.
The draft is current operational context, not a second strategy or memory store.

## Skill Signature

```text
interval_update(project_root, interval_id, review_window, context_refs?,
                write_policy?, knowledge_write_policy = "stage_daily_promote_weekly",
                now?, refresh_metrics = false,
                refresh_scope = "selected_stale")
  -> interval_report + problems + feedback_loop_status + bottleneck_analysis
   + candidate_sets {problems, decisions, sops, resources, entities,
                     doc_quality, completeness, followups}
   + weekly_draft_delta + ticket_deltas + highlights
   + knowledge_receipt + promoted_records? + next_week_draft? + source_gaps

state:
  reads(bindings, metrics, configured board, Pulse/Interval reports,
        bounded Git/ticket/proof/doc changes, project-mapped Codex task
        conclusions, current weekly draft, canonical destination owners,
        prior Daily knowledge receipts)
  writes(.farplane/reports/interval/<interval_id>/<timestamp>.md,
         .farplane/reports/interval/weekly/<YYYY-Www>/draft.md,
         .farplane/reports/interval/<interval_id>/<timestamp>-knowledge.md,
         sparse highlights, authorized task/ticket deltas,
         Weekly-only validated promotions through skill-maintenance,
         doc-advisor, or manage-wiki)
gates: bounded_window; configured_provider_resolved; source_bound;
  candidate_fingerprint; daily_no_promotion; weekly_disposition_complete;
  report_finalized_before_promotion; promotion_authority; durable_fact;
  owner_route_resolved; destination_diff_exists; route_validation;
  ambiguous_or_large_delta_not_promoted; no_ticket_execution
routes: skill-maintenance | doc-advisor | manage-wiki | pulse-update |
  plan-next-wave | review
fails: raw transcript copying; week-wide Daily rescans; generic memory buckets;
  duplicate candidate append; Daily durable promotion; unsupported facts;
  direct generated-index edits; unsafe owner mutation; protected-ticket rewrites;
  unapproved chases; Goal/Pulse/worker execution
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind one window, provider, and write policy.
  - [ ] Read `qa_checklist.md`; resolve `project_root`, cadence, bounded window,
        context refs, board authority, and knowledge write authority.
  - [ ] Run `scripts/resolve_evidence_binding.py --project-root <project_root>`.
        Obey one configured provider and its filesystem policy; failures are
        `source_gap`, never permission to infer a fallback.
- [ ] 2. Build one shared evidence bundle.
  - [ ] Read metric/outcome movement, board evidence, Pulse/reports, proof, and
        repository artifacts created or changed inside the window.
  - [ ] Read bounded conclusions from project-mapped Codex tasks created,
        updated, or archived inside the window. Treat raw transcripts as private
        source material and never copy them into reports or durable docs.
  - [ ] Give every retained source a stable locator and evidence ref. Daily must
        not rescan the week; Weekly prefers the current draft and completed Daily
        receipts over replaying raw sources.
  - [ ] Refresh selected stale metrics only for Daily when explicitly enabled.
- [ ] 3. Run the reporting phase.
  - [ ] Diagnose feedback as working, proxy-only, human-review-only, or missing;
        never optimize from vibes or invent favorable movement from source gaps.
  - [ ] Ground the dominant bottleneck and root cause, state confidence and
        ruled-out alternatives, then compare coherent interventions.
  - [ ] Record each ticket candidate as qualified, duplicate, protected,
        planning residue, low materiality, source gap, or blocked by authority.
- [ ] 4. Project independent findings into the current weekly draft.
  - [ ] Classify progress, problems, decisions, SOPs, reusable project
        knowledge, entity facts, document-quality gaps, missing information,
        and stale follow-ups without making one lane own another lane's write.
  - [ ] Upsert each retained finding by stable source locator, intended owner,
        and content digest. Record evidence, value gate, missing authority, and
        proposed destination; reruns must not append duplicates.
  - [ ] Daily writes only the draft delta and explicit mutable task progress.
        It creates no problem ticket, Decision/Memory row, skill rule, project
        doc, Wiki fact, quality edit, source comment, or outgoing chase.
- [ ] 5. Finalize the immutable run report, then apply reporting deltas.
  - [ ] Write the dated report and Problems ledger before any highlight, board,
        skill, docs, or Wiki mutation; carry prior problems by link.
  - [ ] Append sparse highlights. Daily may then update only authorized mutable
        task progress; Weekly may apply independently qualified ticket deltas.
        Never execute admitted work.
- [ ] 6. On Weekly, disposition and promote; on Daily, receipt the projection.
  - [ ] Weekly assigns every candidate `promoted | duplicate | monitor |
        dismissed | source_gap | blocked`. A missing disposition blocks freeze.
  - [ ] Route promoted SOPs through `skill-maintenance`; project resources,
        domain decisions, project-level precedents, and approved doc-quality
        patches through `doc-advisor`; entity facts through `manage-wiki`.
        Problems become qualified tickets. Chases remain proposals.
  - [ ] Freeze the weekly report before promotion. Invoke owner validations,
        never edit generated projections directly, write the observed-result
        receipt, mark the draft finalized, and open the next week's draft.
  - [ ] Daily receipts record candidate upserts and `canonical_promotions: 0`.
        Weekly receipts record source, destination, digest, disposition, result,
        changed paths, and validation. Receipts plus destinations make reruns
        idempotent without a global ledger.
- [ ] 7. Finish-check and return.
  - [ ] Reapply `qa_checklist.md`; return the report, current/finalized draft,
        receipt, candidate dispositions, changed owners, source gaps,
        operator-needed items, next owner, and no-ticket-execution proof.
  - [ ] Explicitly receipt that one bounded bundle fed both phases and that
        tasks/threads were treated as evidence containers, not destinations.
  - [ ] Receipt the cadence authority: Daily promotion count is zero; Weekly
        finalized before promotion and opened the next draft afterward.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

- [Interval report](templates/interval-report.md) — stages reporting and
  candidate decisions before mutation.
- [Weekly working draft](templates/weekly-working-draft.md) — compact current
  context and source-fingerprinted promotion candidates.
- [Knowledge receipt](templates/knowledge-receipt.md) — records observed owner
  writes or Daily candidate projection after report finalization.
- [BAU interval contract](references/interval-update.md) — provider, admission,
  cadence, knowledge routing, receipt, and carry-forward details.

## Gotchas

- Cadence changes authority, not evidence quality: Daily stages; Weekly promotes.
- A task/thread is evidence, not automatically durable knowledge.
- `farplane/harness.yaml` remains stable project identity; the weekly draft is
  current context and finalized reports are history.
- Report finalization precedes canonical promotion; the sibling receipt records
  observed results without rewriting the report.
- Highlights never feed ticket or knowledge decisions.

## Reference Map

- [Parent run contract](references/parent-run-contract.md) — caller checks.
- [Skill maintenance](../skill-maintenance/SKILL.md) — SOP and skill deltas.
- [Doc advisor](../doc-advisor/SKILL.md) — project documentation deltas.
- [Manage Wiki](../manage-wiki/SKILL.md) — sourced entity articles and links.
- [Pulse](../pulse-update/SKILL.md) — ticket execution.

## Output

Return one immutable run report, the current or finalized weekly draft, one
immutable knowledge receipt, reporting/ticket decisions, candidate dispositions,
promoted records, source/provider receipts, ordering proof, and proof that no
Goal, Pulse, worker, or ticket execution started.

End every Interval scenario or run response with these explicit receipts:
`shared_evidence_bundle: yes`, `tasks_threads_are_evidence_not_destinations: yes`,
`candidate_fingerprint_basis: source_locator + intended_owner + content_digest`,
`daily_canonical_promotions: 0 | not_daily`,
`weekly_candidate_dispositions_complete: yes | not_weekly`,
`report_finalized_before_promotion: yes`,
`knowledge_receipt_written_after_projection_or_owner_routes: yes`, and
`direct_generated_index_or_projection_edits: 0`, and
`ticket_goal_pulse_worker_execution: none`.
