---
title: Interval Update QA Checklist
owner: interval-update
status: active
kind: qa-checklist
applies_to:
  - interval-update
  - daily-bau-report
  - weekly-bau-report
---

# Interval Update QA Checklist

Use before an Interval run and again before returning its report.

```text
interval_check(report, evidence, analysis, candidates, ticket_deltas,
               weekly_draft, promotion_deltas, knowledge_receipt, highlights)
  -> pass | violation | source_gap
```

## Evidence And Provider

- [ ] The run is a bounded Daily, Weekly, or BAU-only profile and writes one
      dated report with Core report frontmatter.
- [ ] Daily and Weekly used the same evidence-quality, movement, bottleneck,
      root-cause, candidate, and dedupe rules. Their authority differs: Daily
      stages; Weekly dispositions and promotes.
- [ ] `farplane/bindings.yaml#integrations.kanban` was resolved before board
      evidence. Only the configured provider and non-secret coordinates were
      used for review, dedupe, and authorized writes.
- [ ] A Notion binding used a named private handle plus `ntn`; reports, gaps,
      candidates, and tickets contain no private IDs, URLs, tokens, or payload
      dumps. `access_ready` required a successful bounded compact query.
- [ ] Provider failure is a `source_gap`. A binding with
      `filesystem_ticket_policy: exclude` never falls back to `tickets/**`,
      including review, dedupe, or mutation.
- [ ] Completed Feed Scout and provider outputs were context only. Missing
      outputs did not cause Interval to invoke another workflow.
- [ ] Missing, stale, invalid, zero-time, or incomparable metric evidence did
      not become invented flat/favorable momentum.
- [ ] Metric views came from the run's bounded review window and project
      timezone; `metrics.yaml` was not used to store cadence, comparison, or
      cumulative projection options.
- [ ] Repository artifacts and project-mapped Codex task conclusions were
      bounded to the review window. Raw transcripts, secrets, client details,
      and unrelated tasks were not copied into durable outputs.
- [ ] Every retained source has a stable locator and evidence ref. Daily did
      not rescan the week; Weekly preferred the current weekly draft and
      completed Daily receipts over raw-source replay.

## First-Principles Review

- [ ] Feedback-loop status is explicitly working, proxy-only,
      human-review-only, or missing instrumentation. Missing feedback did not
      become optimization from vibes; a proposed instrumentation/unblock ticket
      names its signal, capture artifact, unlocked decision, and stop condition.
- [ ] Material stalls, regressions, and outcome gaps are tied to evidence; raw
      activity or ticket volume is not treated as progress.
- [ ] Every problem and system-gap diagnosis cites ticket, progress, metric,
      feedback, or completed-report evidence.
- [ ] The report names the dominant bottleneck, separates symptoms from the
      root-cause claim, records confidence and ruled-out alternatives, and
      rebuilds the simplest correct path from objective and constraints.
- [ ] Candidate interventions are compared for compounding effect, recurrence
      prevention, time to evidence, reversibility, dependencies, and risk.
- [ ] Each root problem prefers one largest coherent intervention; analysis,
      design, implementation, and proof were not split into planning tickets.
- [ ] The report contains an ordinary Markdown Problems checklist and no
      finding IDs, finding frontmatter, or findings registry.

## Ordering And Highlights

- [ ] The report was finalized as an immutable snapshot before highlight append
      or board mutation. Prior finalized reports were not rewritten; unresolved
      problems were carried by reference.
- [ ] Highlight selection bound a stable project-local team slug and ran only
      after report finalization. Ticket deltas ran only after highlight
      selection completed or no-op'd.
- [ ] Each team/report emitted at most one win and one failure. Repeated append
      returned `already_exists`; an honest no-highlight result was allowed.
- [ ] Each win cites explicit comparative numeric evidence for a record,
      meaningful threshold, or exceptional delta. Routine completion,
      unquantified improvement, and filler were rejected.
- [ ] Each failure states a material event, consequence/context, and reusable
      lesson without duplicating the correction plan.
- [ ] Rows use only win `{team, report, summary, links?}` or failure
      `{team, report, summary, lesson, links?}` with safe project-relative
      links. Highlights were not read as planning/correction evidence and did
      not mutate reports, tickets, skills, gotchas, or lessons. Ticket decisions
      stayed grounded in finalized report evidence rather than highlights.

## Weekly Draft, Promotion, And Mutation

- [ ] One current weekly draft holds at most five current-context bullets plus
      independent progress, problem, decision, SOP, resource, entity,
      documentation-quality, completeness, and follow-up lanes.
- [ ] Every retained finding is upserted by stable source locator, intended
      owner, and content digest. Reruns append no duplicate candidate.
- [ ] The final response explicitly reports that fingerprint basis and the
      candidate upsert count; it does not rely on implied deduplication.
- [ ] Daily wrote an immutable report, updated the draft, and recorded
      `canonical_promotions: 0`. It created no problem ticket, Decision/Memory
      row, skill rule, project doc, Wiki fact, quality edit, source comment, or
      outgoing chase. Only explicitly supported mutable task progress was
      eligible for an authorized write.
- [ ] Weekly read the draft and Daily receipts, replaced every pending candidate
      with `promoted | duplicate | monitor | dismissed | source_gap | blocked`,
      and blocked finalization when a disposition was missing.
- [ ] Problems route to qualified tickets; SOPs through `skill-maintenance`;
      project resources, domain decisions, project-level precedents, and
      approved doc-quality patches through `doc-advisor`; entity facts through
      `manage-wiki`. Chases remain proposals unless separately authorized.
- [ ] Only durable, source-backed candidates passing their value gate,
      destination diff, promotion authority, privacy, and route validation were
      promoted. Tasks and threads remained evidence rather than destinations.
- [ ] Weekly finalized the report before canonical promotion, recorded observed
      results in the immutable receipt, marked the draft finalized, and opened
      the next draft. It never edited a generated index or projection directly.
- [ ] The receipt records fingerprint, destination, digest, disposition,
      observed result, changed paths, and validation. Daily/Weekly receipts plus
      current destinations make reruns idempotent without a global ledger.

## Ticket Admission And Mutation

- [ ] Every admitted delta satisfies the exact core predicate: material problem
      AND executable next intervention AND concrete output/proof AND no active
      duplicate. Provider write authority and coherent scope also pass.
- [ ] On Weekly, known cause/intervention work creates a concrete solution
      ticket or updates a matching mutable `todo`; Daily stages a new problem
      and may update only explicitly supported mutable progress. A promoted
      ticket states correction, concrete output, proof/falsifier, and stop.
- [ ] Every investigation ticket requires reproduced cause, ruled-out
      alternatives, selected correction, and proof artifact. Generic research,
      “plan strategy,” roadmap, option analysis, and artifact-free thinking are
      rejected as planning residue.
- [ ] Low-materiality chores, vague work, duplicates, unsafe writes, and
      incoherent lifecycle fragments are rejected with reasons. Insufficient
      grounding and source gaps remain visible report candidates.
- [ ] Every actionable finding maps to an admitted delta or explicit no-action
      reason. Spend, publishing, customer contact, account changes, and
      private-data use remain behind explicit approval gates.
- [ ] Every independently qualified intervention may be admitted; no numeric
      cap or target is applied. Multiple tickets indicate multiple material
      root problems, not momentum.
- [ ] Dedupe checks substantially matching ownership, not just exact titles.
      An active/review/waiting/blocked-execution/terminal ticket is never
      silently rewritten.
- [ ] Only `todo` tickets may be clarified, reprioritized, dated, or rejected.
      Rejection preserves history and a reason; no ticket is physically deleted.
- [ ] Board mutation uses only the configured authorized provider route. A
      missing write route yields `blocked_by_authority`, not a local fallback.

## Ownership And Return

- [ ] The run did not call Dogfood Review, priority/leverage planning, Goal,
      Pulse, a worker, or ticket execution. Owner-routed local knowledge writes
      did not expand into deploy, publish, spend, account, or customer actions.
- [ ] The final result includes provider/binding receipt, source gaps, report
      path, what changed and why, feedback-loop status, bottleneck, candidate
      decisions and reasons, weekly draft, applied ticket deltas, knowledge
      receipt, promotions, changed owners, blocked systems, missing feedback,
      highlights, operator-needed items, next owner, and no-execution receipt.
- [ ] Scenario/eval answers expose the compact full decision chain, including
      independent candidate evaluation, no numeric cap or volume-as-momentum
      claim, Plan Next Wave boundary, ordering, and no-ticket-execution receipt.
