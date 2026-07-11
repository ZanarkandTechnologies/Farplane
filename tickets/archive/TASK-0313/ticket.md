---
template_id: ticket-template
template_version: "0.1.9"
feature_refs:
  - FEAT-0007
  - FEAT-0008
  - FEAT-0067
  - FEAT-0070
ticket_id: TASK-0313
title: Make dogfood review create one consolidated improvement ticket
phase: complete
status: done
owner: codex
claimed_by:
priority: medium
depends_on: []
blocked_by: []
ready: false
approval_required: false
requires_qa: true
requires_demo: false
human_gate: none
rewards.kpi:
  - accepted_harness_improvements
created_at: 2026-07-07T22:47:25+08:00
updated_at: 2026-07-07T23:16:00+08:00
next_action: none; archived after implementation and reviewer gate completed
last_verification: "2026-07-07T23:16:00+08:00 pass: docs/features/validate_features.py; json.tool dogfood-review and interval-update evals; skill-maintenance check_skills.py --write; ticket metadata; reviewer rereview TAS-A"
---

# TASK-0313: Make dogfood review create one consolidated improvement ticket

## Summary

`dogfood-review` now uses active tracked feature prompts and reviewer lanes, and
material tracked-feature reports can close into exactly one consolidated
improvement ticket path or complete ticket candidate.

Implementation is now complete. The change updates the dogfood-review contract,
report template, QA checklist, evals, interval surfacing, audit record, and
proof artifacts without triggering Goal execution, worker spawn, or live
automation sync.

## Scope

- In:
  - Define the contract for `dogfood-review` to create or emit one consolidated
    improvement ticket from a material tracked-feature report.
  - Keep the output as one ticket per review run, grouped by feature and
    cross-cutting repair, rather than one ticket per feature.
  - Preserve reviewer-lane findings, TAS grades, evidence refs, and feature
    `track` prompts inside the ticket body so the follow-up worker has the real
    checklist context.
  - Add an explicit no-autostart boundary: ticket creation must not invoke
    `impl-plan`, Goal, Pulse execution, or worker spawn by itself.
  - Specify how the interval automation should surface the created ticket path
    or candidate ticket delta in the daily report.
- Out:
  - No Goal Packet or worker spawn from this ticket.
  - No live automation sync.
  - No separate ticket per tracked feature.
  - No repair of the current dogfood findings.

## Delta

```text
overall_before:
  - dogfood-review can generate a report with per-feature reviewer findings.
  - actionable system improvements remain embedded in the report and must be
    manually converted into board work.
  - daily interval can mention dogfood results, but there is no explicit ticket
    artifact that owns the repair bundle.
overall_after:
  - each material dogfood-review run creates or emits exactly one consolidated
    improvement ticket.
  - the ticket carries grouped findings by feature, cross-cutting repairs,
    evidence refs, reviewer TAS, and the feature track prompts used to judge the
    system.
  - ticket creation is visible board state, not execution; `impl-plan` remains
    a later explicit step after review or approval.
why_now:
  - the 2026-07-07 manual dogfood report found useful system issues across
    FEAT-0066 through FEAT-0070, but those issues are easy to lose if they stay
    only in `.farplane/reports`.
  - Kenji wants dogfood review to create the improvement work, while avoiding
    premature implementation routing.
problems:
  - before: reviewer findings are report-only and need manual translation into
      a ticket.
    after: the report includes a created ticket path or a ticket candidate that
      can be reviewed as the next work item.
    why_now: the dogfood loop should close into the board, not only create
      analysis.
  - before: per-feature findings could encourage noisy ticket spam.
    after: one ticket groups all issues from the review run and names the
      coherent repair program.
    why_now: tracked experimental features are tightly coupled system behavior,
      so the improvement work should be reviewed as one system bundle.
  - before: ticket creation could be confused with execution.
    after: the created ticket starts as `phase: planning`, `status: review`,
      `ready: false`, and `approval_required: true` unless the caller
      explicitly requests a different policy.
    why_now: the current request is to stop at ticket creation and key proposal.
first_principles_basis:
  objective: turn dogfood reviewer evidence into durable improvement work
    without hiding execution side effects.
  need: the system needs a visible owner for dogfood-derived repairs, not only
    a report artifact.
  assumptions:
    - material tracked-feature dogfood reports should usually produce at most
      one follow-up ticket.
    - the follow-up ticket should preserve the feature-specific review
      checklists so a later implementer cannot flatten the findings.
    - automatic ticket creation is safe when the ticket is explicitly not ready
      for execution.
  root_cause: dogfood-review currently has evidence aggregation but not a board
    writeback contract.
  constraints:
    - do not create multiple tickets for one report by default.
    - do not invoke `impl-plan`, Goal, worker spawn, or automation sync during
      ticket creation.
    - do not include retired or superseded features as active repair targets.
    - keep bulky reviewer logs in artifacts and keep the ticket compact enough
      to use.
  first_viable_slice: update dogfood-review skill/template/eval so a material
    run emits one ticket candidate or writes one review-gated ticket.
  proof_or_falsification: the change fails if a dogfood run produces multiple
    feature tickets, auto-starts execution, drops TAS/evidence/track prompts, or
    fails to expose the ticket path in the report.
  tradeoff: accept one consolidated ticket that may be slightly larger in order
    to preserve system-level context and avoid board spam.
  non_goals:
    - implement the repairs found in the latest dogfood report.
    - make dogfood-review a general ticket planner.
    - replace `impl-plan`, `goal-advisor`, Pulse, or interval-update.
```

## Reward

```yaml
kpi_rewards:
- reward_id: accepted-harness-improvements-unscheduled
  kpi_id: accepted_harness_improvements
  expected_reward: one reviewed harness-loop improvement that turns dogfood evidence
    into durable board work without premature execution
  check_in_at: null
  actual_result: null
  decision: null
  evaluated_at: null
  evaluation_key: null
  supersedes_evaluation_key: null
  evidence_refs: []
guard: count only after the dogfood-review contract, template, and eval prove exactly-one-ticket
  behavior and no autostart
```

## Key Proposal

```text
dogfood_review(task, state, write_policy?)
  -> dogfood_report
   + reviewer_findings_by_feature
   + skipped_retired_refs
   + improvement_ticket_path_or_candidate
   + no_autostart_receipt

write_policy:
  create_improvement_ticket: false by default unless caller explicitly enables
  ticket_status: review
  ticket_phase: planning
  ready: false
  approval_required: true
  max_tickets_per_report: 1
  autostart_impl_plan: false
  autostart_goal: false
```

Recommended behavior:

- `dogfood-review` should always produce a report.
- For material tracked-feature reviews, the report should include an
  `Improvement Ticket` section.
- When `write_policy.create_improvement_ticket` is enabled, the skill should
  create one ticket under `tickets/TASK-XXXX/ticket.md` and link it from the
  report.
- When the write policy is disabled or unsafe, the skill should emit a complete
  ticket candidate in the report instead of silently dropping the repair work.
- The ticket should be grouped by feature, but the artifact remains one system
  improvement ticket.

Minimum ticket sections generated by dogfood-review:

```text
frontmatter:
  phase: planning
  status: review
  ready: false
  approval_required: true
body:
  Summary:
    - one sentence on the dogfood review run and the system repair theme
  Scope:
    - in/out, including explicit no-autostart
  Findings By Feature:
    - feature_ref
    - track_prompt_summary
    - reviewer_tas
    - issue
    - proposed repair
    - evidence_refs
  Cross-Cutting Repairs:
    - shared changes that cover multiple features
  Done / Proof:
    - exact checks, evals, and reviewer gates for the later implementation
  Links:
    - dogfood report path
    - context packet path
    - reviewer artifact paths or summaries
```

## Seed Findings From Latest Manual Report

Use these as the representative candidate payload when implementing the
contract. They are not being repaired by this ticket.

```text
source_report: .farplane/reports/dogfood-review/2026-07-07T092204Z.md
context_ref: .farplane/reports/dogfood-review/context/2026-07-07T092204Z.md
skipped_active_targets:
  - FEAT-0065 was retired/superseded and must not be tracked as active work.
grouped_findings:
  - feature_ref: FEAT-0066
    reviewer_tas: TAS-B
    issue: product-scoped Pulse produced many unchanged skip reports compared
      with actual admitted work.
    proposed_repair: cap or compress unchanged skip reporting while preserving
      action admissions and evidence.
  - feature_ref: FEAT-0067
    reviewer_tas: TAS-B
    issue: the latest daily interval report did not clearly link or summarize
      tracked-feature dogfood review.
    proposed_repair: make interval-update surface the dogfood report path,
      active refs, skipped refs, and improvement ticket path.
  - feature_ref: FEAT-0068
    reviewer_tas: TAS-C
    issue: TASK-0302 does not yet have a reviewer receipt under its ticket
      artifacts, so Goal-backed execution proof is incomplete.
    proposed_repair: require final reviewer evidence receipts before claiming
      material Goal-backed ticket completion.
  - feature_ref: FEAT-0069
    reviewer_tas: TAS-B
    issue: Taste Loop should remain capped until feedback export and planning
      artifacts are proven.
    proposed_repair: map or exempt `qualified_attention` and require concrete
      feedback planning/output artifacts before uncapping.
  - feature_ref: FEAT-0070
    reviewer_tas: TAS-B
    issue: active-only dogfood review now skips retired features, but daily
      interval ingestion of that active-only report remains unproven.
    proposed_repair: prove Daily's tracked-feature section consumes the
      active-only report and carries the improvement ticket link.
```

## Done / Proof

```text
done_when:
  - `skills/dogfood-review/SKILL.md` defines one consolidated improvement
    ticket output for material tracked-feature reports.
  - `skills/dogfood-review/templates/dogfood-report.md` includes an
    `Improvement Ticket` section with either a created ticket path or a complete
    ticket candidate.
  - `skills/dogfood-review/eval_task.json` proves exactly-one-ticket behavior,
    no per-feature ticket spam, retired-feature exclusion, and no autostart of
    `impl-plan`, Goal, Pulse execution, or worker spawn.
  - `skills/interval-update/SKILL.md` or its report template documents how the
    daily interval surfaces the dogfood improvement ticket path when
    `tracked_feature_review` is enabled.
  - Feature and skill registries validate after source changes.
  - A reviewer lane checks the final prompt/skill behavior for owner-boundary,
    evidence-quality, and integration-readiness before completion.
```

## QA Strategy

```text
qa_strategy:
  proof_weight: review
  checks:
    - python3 docs/features/validate_features.py
    - python3 -m json.tool skills/dogfood-review/eval_task.json
    - python3 skills/skill-maintenance/scripts/check_skills.py --write
    - python3 tickets/scripts/check_ticket_metadata.py tickets/TASK-0313/ticket.md
  manual:
    - run a dogfood-review sample with ticket creation disabled and verify the
      report contains one complete candidate ticket.
    - run a dogfood-review sample with ticket creation enabled in a safe local
      checkout and verify exactly one `tickets/TASK-XXXX/ticket.md` is created.
    - verify the created ticket has `phase: planning`, `status: review`,
      `ready: false`, and `approval_required: true`.
  delegated_lanes:
    - reviewer lane for skill-contract, evidence-quality, and
      integration-readiness.
  review:
    - rubric: skill-contract
      required_tas: TAS-B or better
    - rubric: evidence-quality
      required_tas: TAS-B or better
    - rubric: integration-readiness
      required_tas: TAS-B or better
  evidence:
    - ticket-local artifact with before/after sample dogfood report excerpt
    - ticket-local artifact with created-ticket path and no-autostart receipt
  goal_advisor_inputs:
    proof_route: review plus focused skill eval
    final_evidence: ticket-local artifacts and reviewer receipt
    final_checkpoint: reviewer completion gate before closeout
  residual_risk:
    - the implementation must avoid turning dogfood-review into a broad ticket
      planning surface; it should only convert its own reviewer findings into
      one follow-up ticket.
```

## Docs Strategy

No durable docs change is required for this proposal ticket. If approved and
implemented, update only the dogfood-review and interval-update skill contracts,
templates, and evals unless implementation discovers that feature registry
documentation needs a small owner-boundary note.

## State

- Current: implementation complete and reviewer gate passed.
- Next: archive when desired.
- Blocked: not blocked.

## Links

- Latest manual dogfood report:
  `.farplane/reports/dogfood-review/2026-07-07T092204Z.md`
- Dogfood context packet:
  `.farplane/reports/dogfood-review/context/2026-07-07T092204Z.md`
- Existing reviewer agent:
  `agents/reviewer.toml`
- Prior adversarial-review ticket:
  `tickets/archive/TASK-0310/ticket.md`
- Skill audit:
  `skills/dogfood-review/audits/2026-07-07-improvement-ticket-writeback.md`
- Sample output proof:
  `tickets/TASK-0313/artifacts/sample-dogfood-improvement-ticket-output.md`
- Reviewer receipt:
  `tickets/TASK-0313/artifacts/reviewer-receipt.md`

## Notes

- The live installed daily interval automation is still stale relative to
  source `automations.toml`; syncing live automation is outside this ticket.
