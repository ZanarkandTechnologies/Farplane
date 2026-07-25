Context:
AGI Toy Shop is a clean-room toy app company fully run by agents.

It has an agent-run storefront, toy inventory, support desk, safety review,
marketing, release workflow, docs, skills, and tickets.

Use this fixture for generic harness evals that test language, reasoning,
routing, escalation, pushback, planning, artifact selection, self-improvement,
or proof behavior. Respond as the harness agent for this fictional company
without touching real files.

---

Skill under evaluation: interval-update
Source file: skills/interval-update/SKILL.md

Skill context:

---
name: interval-update
description: "Turn one Daily or Weekly evidence window into a first-principles bottleneck review, dated report, sparse highlights, and concrete ticket deltas."
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

Use this skill for one bounded Daily or Weekly control-loop review. The Codex
app owns cadence; both profiles use the same reasoning and admission quality.
Daily emphasizes recent movement and outcomes. Weekly adds recurrence, wider
ticket history, resource use, and unresolved proof. Each run identifies the
dominant bottleneck, distinguishes symptom from root cause, compares coherent
interventions, finalizes an immutable report, appends sparse presentation
highlights, and only then applies qualified ticket deltas.

Interval does not execute admitted work or maintain a separate strategy store.
Insufficiently grounded work remains a report candidate for Plan Next Wave.
Work Pulse owns execution and due experiment check-ins. The weekly
self-improvement automation owns its portfolio review.

Before reading work items, load `farplane/bindings.yaml` when present and
resolve exactly one kanban provider. Provider failure remains a `source_gap`;
an excluded filesystem board is never a fallback or hidden dedupe source.

## Skill Signature

```text
interval_update(project_root, interval_id, review_window, context_refs?,
                write_policy?, now?, refresh_metrics = false,
                refresh_scope = "selected_stale")
  -> interval_report
   + problems
   + feedback_loop_status
   + system_gaps
   + bottleneck_analysis
   + candidate_interventions
   + ticket_deltas
   + highlights {wins[0..1 per team], failures[0..1 per team]}
   + highlight_receipt
   + metric_refresh_receipt?
   + source_gaps

state:
  reads(farplane/bindings.yaml?, farplane/harness.yaml?, farplane/metrics.yaml?,
        .farplane/metrics/**?, configured kanban evidence,
        .farplane/reports/pulse/**, .farplane/reports/interval/**,
        completed provider reports supplied through context_refs,
        review/run artifacts and project memory refs when supplied)
  writes(.farplane/reports/interval/<interval_id>/<timestamp>.md,
         .farplane/highlights/wins.jsonl?,
         .farplane/highlights/failures.jsonl?,
         qualified ticket deltas through the configured authorized board route)

gates:
  interval_id in [daily, weekly] or explicit BAU profile;
  review_window_bound; configured_provider_resolved; report_finalized;
  report_complete_before_highlight_append; highlight_cap_respected;
  ticket_deltas_after_highlights; material_problem; executable_intervention;
  concrete_output_and_proof; active_duplicate_absent; write_authority;
  largest_coherent_intervention; protected_state_immutable;
  no_planning_residue; no_execution

routes:
  pulse-update | plan-next-wave | feed-scout | review

fails:
  creating vague planning or low-materiality tickets; splitting one correction
  into analysis/design/build/proof tickets; rewriting active, review, waiting,
  or terminal work; bypassing provider or authority gates; treating highlights
  as planning input; invoking providers; executing admitted work
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind one evidence window and provider.
  - [ ] Read `qa_checklist.md`; resolve `project_root`, `interval_id`,
        `review_window`, optional `context_refs`, write authority, and metric
        refresh inputs.
  - [ ] Run `scripts/resolve_evidence_binding.py --project-root <project_root>`.
        Obey the selected provider, non-secret coordinates, and
        `filesystem_ticket_policy`; never infer a second board.
  - [ ] Use the same review algorithm for Daily and Weekly. Change only the
        window and evidence coverage described in the reference.
- [ ] 2. Build the bounded evidence bundle.
  - [ ] For Daily only when `refresh_metrics = true`, resolve selected/pinned
        stale metric IDs through `scripts/metric_refresh.py refresh-plan`.
        Execute each returned refresh group once, record partial readings or
        source gaps, and write flat observations before synthesis. Weekly and
        disabled runs execute zero refresh groups.
  - [ ] Read configured board evidence, metric movement, Pulse/report evidence,
        outcomes, proof, and the previous finalized Interval report inside the
        profile's window.
  - [ ] Read only completed provider reports supplied through `context_refs`.
        Never invoke a missing provider. Normalize Notion rows immediately and
        keep raw IDs, URLs, tokens, and payloads out of tracked artifacts.
  - [ ] If provider access fails, record a `source_gap`. With
        `filesystem_ticket_policy: exclude`, do not inspect, dedupe, or write
        `tickets/**`; finish from the remaining evidence.
- [ ] 3. Run the first-principles review.
  - [ ] Diagnose the feedback loop as working, proxy-only, human-review-only,
        or missing instrumentation. Do not optimize from vibes. When feedback
        is missing, compare a concrete instrumentation/unblock intervention
        under the same admission predicate as every other candidate.
  - [ ] Name material improving, flat, worsening, unavailable, and incomparable
        movement without inventing favorable momentum from source gaps.
  - [ ] Identify material stalls/regressions and outcome gaps; select the
        dominant current bottleneck by objective impact rather than activity.
        Ground every problem/system-gap diagnosis in ticket, progress, metric,
        feedback, or completed-report evidence.
  - [ ] Separate observed symptom from root cause, state confidence and ruled-
        out alternatives, and rebuild the simplest correct path from the
        objective and constraints.
  - [ ] Compare coherent interventions by expected compounding effect,
        recurrence prevention, time to evidence, reversibility, dependencies,
        and risk. Prefer one largest coherent intervention per root problem.
- [ ] 4. Finalize the dated report and Problems ledger.
  - [ ] Use `templates/interval-report.md` under
        `.farplane/reports/interval/<interval_id>/<timestamp>.md` with Core
        report frontmatter.
  - [ ] Record ordinary Markdown problem checkboxes with evidence and optional
        ticket links; add no finding IDs, frontmatter, or registry.
  - [ ] Record metric movement, bottleneck/root-cause reasoning, compared
        interventions, feedback-loop status, blocked systems, admission
        decisions, and intended ticket deltas. For each actionable finding,
        record the admitted delta or an explicit no-action reason.
  - [ ] Finalize the snapshot before any highlight append or board mutation.
        Carry unresolved prior problems by link; never rewrite prior reports.
- [ ] 5. Append sparse TASK-0405 highlights.
  - [ ] Bind a stable project-local team slug and select at most one win and one
        failure per team for this report; prefer an honest no-op to filler.
  - [ ] Require explicit comparative numeric evidence for a record, meaningful
        threshold crossing, or exceptional delta. Routine delivery is not a
        win. Require consequence/context plus a reusable lesson for a failure.
  - [ ] Append with `scripts/highlight_ledger.py`; use only win
        `{team, report, summary, links?}` or failure
        `{team, report, summary, lesson, links?}`.
  - [ ] Treat `(kind, team, report)` as identity and `already_exists` as an
        idempotent no-op. Do not read highlights as correction/planning input or
        mutate the finalized report.
- [ ] 6. Apply qualified ticket deltas after highlights.
  - [ ] Evaluate every candidate independently; there is no numeric ticket cap.
        Admission requires a material problem AND executable next intervention
        AND concrete artifact/behavior/experiment-result/outcome plus proof AND
        no active duplicate, with provider write authority and coherent scope.
  - [ ] For a known cause/intervention, create a concrete solution ticket or
        clarify/reprioritize/date a substantially matching `todo` ticket. The
        ticket itself must state the correction, concrete output, proof or
        falsifier, and stop condition rather than leaving those only in the
        report.
  - [ ] For an uncertain cause/intervention, admit only one decision-changing
        investigation whose required output is reproduced cause, ruled-out
        alternatives, selected correction, and proof artifact.
  - [ ] Reject planning residue, low-materiality chores, vague strategy work,
        artifact-free work, duplicates, unsafe writes, and incoherent splits.
        Keep source gaps and insufficient grounding as report candidates.
  - [ ] Preserve explicit approval gates for spend, publishing, customer
        contact, account changes, and private-data use. Lack of authority means
        no mutation even when the intervention is otherwise qualified.
  - [ ] Never rewrite `active`, `review`, waiting-signal, blocked execution, or
        terminal ticket contracts. Reject stale `todo` tickets with a reason
        rather than deleting history; create a replacement only when the
        qualified intervention needs one.
  - [ ] Do not start Goal, Pulse, a worker, an experiment, or implementation.
- [ ] 7. Finish-check and return.
  - [ ] Reapply `qa_checklist.md` and index the report when the CLI is available.
  - [ ] Return the provider receipt, source gaps, report path, problems,
        feedback-loop status, bottleneck, candidate decisions, ticket deltas,
        blocked systems, missing feedback, highlight receipts, operator-needed
        items, next Goal/heartbeat owner, and a no-execution receipt.
  - [ ] Summarize 2-4 findings and every candidate's admission result and reason
        so the operator can understand the decision without opening the report.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

- [templates/interval-report.md](templates/interval-report.md) - shared Daily
  or Weekly movement-to-bottleneck-to-ticket report.

## Gotchas

- Cadence changes evidence coverage, never decision quality or admission gates.
- A new same-run problem may be ticketable when its cause/intervention is known
  and all admission gates pass; novelty does not imply uncertainty.
- “Investigate” is ticketable only with the complete decision-changing output,
  not as permission to think, research generally, or write a plan.
- Missing feedback is not evidence that a favored intervention works. Treat a
  qualified instrumentation/unblock ticket as the intervention when it is the
  fastest path to decision-changing evidence. Name the exact signal, capture
  artifact, decision the evidence unlocks, stop condition, and systems blocked
  by the missing feedback; do not return generic "add instrumentation" work or
  merely repeat those category names. If the input does not supply concrete
  bindings, either bind the smallest honest representative signal/artifact/
  threshold/stop contract or return no-action plus the missing bindings. Name
  the next execution owner while keeping Interval itself non-executing.
- Multiple independent material root problems may each produce a ticket. One
  problem should not produce lifecycle-stage fragments.
- Provider suggestions are context, not automatically grounded problems.
- Highlight selection remains presentation judgment after report finalization,
  not a second Problems ledger, planning memory, or correction mechanism.
- Ticket reasoning is independent of highlights, not independent of report
  evidence: every admission or rejection must cite the finalized report's
  movement, bottleneck, root-cause, intervention, and source-gap evidence.
- For scenario, eval, or operator decision questions, return the whole compact
  decision chain even when the final ticket count is obvious:
  `movement/bottleneck/root cause/interventions -> finalized report ->
  highlights -> per-candidate admission (including Plan Next Wave boundary) ->
  no-execution receipt`. State that candidates are evaluated independently,
  there is no numeric cap or volume-as-momentum claim, and grounded work is not
  delayed for Plan Next Wave.

## Reference Map

- [BAU interval contract](references/interval-update.md) - Daily/Weekly evidence
  profiles, first-principles review, admission examples, and carry-forward.
- [Parent run contract](references/parent-run-contract.md) - caller integration
  checks; this `SKILL.md` remains runtime authority.
- [../pulse-update/SKILL.md](../pulse-update/SKILL.md) - owns execution.
- [../plan-next-wave/SKILL.md](../plan-next-wave/SKILL.md) - owns board refill
  when Interval evidence remains insufficiently grounded.

## Output

- Never answer an Interval scenario with only a ticket count or disposition.
  Always state the compact chain: movement/bottleneck/cause/intervention,
  report finalized, highlight append or honest no-op, then board mutation.
  Explicitly say qualified ticket count is not momentum and no numeric target
  exists. For every admitted ticket, say that the ticket contract itself
  contains the correction, concrete output, proof/falsifier, and stop
  condition. End with an explicit receipt that Interval started no Goal, no
  Pulse, no worker, and no execution.
- One immutable dated Daily or Weekly report with movement, bottleneck,
  root-cause, intervention comparison, Problems, and ticket-decision evidence.
- Zero or more independently qualified ticket deltas with no arbitrary cap.
- Zero or one exceptional win and zero or one lesson-bearing failure per team,
  appended idempotently after report finalization and before ticket deltas.
- Source/provider receipts and proof that Interval neither invoked missing
  providers nor planned in highlights nor executed admitted work.

User request:
The review has ticket activity but no outcome feedback, proxy, or human-review signal. Someone proposes optimizing onboarding anyway. A second, material and executable candidate would capture the `first_value_accepted` signal in `.farplane/evidence/onboarding-acceptance.jsonl`, use 20 completed trials to decide whether onboarding A or B reaches the 60% acceptance threshold, then stop; its local write route is authorized and no active ticket owns it. What does Interval do?
