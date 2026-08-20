---
title: "BAU Interval Reporting And Knowledge Contract"
status: active
owner: interval-update
kind: reference
---

# BAU Interval Reporting And Knowledge Contract

Daily and Weekly are evidence profiles over one decision primitive:

```text
review_interval(interval_id, review_window, evidence, board, authority)
  -> finalized_report
   + sparse_highlights
   + weekly_draft_delta
   + candidate_sets
   + ticket_deltas
   + knowledge_receipt
   + promoted_records?
   + next_week_draft?
   + source_gaps
```

The invariant order is:

1. resolve the configured provider and gather the bounded evidence window;
2. review metric/outcome movement through bottleneck and root cause;
3. compare interventions and extract independent candidate lanes;
4. upsert source-fingerprinted findings into the current weekly draft;
5. finalize the immutable run report;
6. append independently selected TASK-0405 highlights;
7. on Daily, apply only authorized mutable task progress and receipt zero
   canonical promotions;
8. on Weekly, disposition every candidate, promote authorized records, write
   the observed-result receipt, finalize the draft, and open the next draft.

Highlights are never an input to steps 2, 3, or 6.

## Evidence Provider Binding

Resolve evidence before reading any board:

```text
resolve_interval_evidence(project_root, farplane/bindings.yaml?)
  -> provider + sanitized_coordinates + filesystem_ticket_policy + source_gaps
```

When bindings exist, `integrations.kanban` is authoritative:

```yaml
integrations:
  kanban:
    provider: filesystem_tickets | notion
    filesystem_ticket_policy: include | exclude
    tickets_dir: tickets                 # filesystem_tickets only
    archive_dir: tickets/archive         # filesystem_tickets only
    task_source_handle: notion.tasks.source  # notion only; named handle, not ID
```

`filesystem_tickets` reads and dedupes only its configured project-relative
directories when policy is `include`. `notion` resolves the named handle from
private context and queries through `ntn`; normalize results immediately.
Tracked artifacts may retain human-readable labels and opaque evidence labels,
but never private IDs, URLs, tokens, or payload dumps.

The default filesystem policy is `include` for `filesystem_tickets` and
`exclude` for `notion`. Explicit `exclude` is a hard gate across work review,
dedupe, and mutation. Missing Notion context, handle, CLI, credential, compact
query, or authorized write route becomes a `source_gap` with no filesystem
fallback. CLI/handle discovery alone is not evidence access. When bindings are
absent, the documented legacy filesystem default applies.

## Shared Review Algorithm

Both profiles execute the complete algorithm:

```text
analyze_control_loop(metric_movement, outcomes, proof, board)
  -> material_problem
   + dominant_bottleneck
   + root_cause {claim, confidence, alternatives_ruled_out}
   + candidate_interventions[]

admit_ticket_delta(problem, intervention, board, authority)
  -> create | update_todo | reject_todo | duplicate
   | investigation | candidate | source_gap | blocked_by_authority
```

1. Read direction-normalized metric movement and observed outcomes. Label
   improving, flat, worsening, unavailable, stale, or incomparable honestly.
2. Diagnose the feedback loop as working, proxy-only, human-review-only, or
   missing instrumentation. Missing feedback forbids optimization from vibes;
   compare a concrete instrumentation/unblock intervention when it can restore
   decision-changing evidence.
3. Find material stalls, regressions, and outcome gaps. Ground each diagnosed
   problem or system gap in ticket, progress, metric, feedback, or completed-
   report evidence. Select the dominant
   bottleneck by objective impact and constraint, not activity or ticket count.
4. Separate symptoms from the likely root cause. State confidence and the
   alternatives that evidence rules out; preserve uncertainty where it remains.
5. Rebuild the simplest correct path from the objective, user/system need,
   constraints, and current evidence.
6. Compare candidate interventions by expected compounding effect, recurrence
   prevention, time to evidence, reversibility, dependencies, and risk.
7. Prefer one largest coherent intervention per root problem. Do not split
   analysis, design, implementation, and proof into planning-only tickets.
8. Map every actionable finding to one lane and explicit disposition. Daily
   stages new problems; Weekly may promote independently qualified tickets.

## Daily Evidence Profile

Daily reviews the recent window, normally 24 hours:

- current metric movement and unavailable/stale readings;
- completed, blocked, abandoned, active, and review-waiting outcomes;
- repeated execution failures, attention drift, and feedback obligations;
- fresh proof, review artifacts, and latest completed provider reports supplied
  through `context_refs`;
- prior unresolved Interval problems needed to understand current evidence.
- repository artifacts and project-mapped Codex task conclusions created,
  updated, or archived inside the bounded window;
- the current weekly draft, canonical destinations, and latest relevant Daily
  receipts for idempotency.

Daily may refresh selected/pinned stale metrics when explicitly enabled. It
does not call the provider whose completed report it reads.

## Weekly Evidence Profile

Weekly executes the same reasoning and admission gates over the wider window:

- completed Daily reports and their carried/resolved problems;
- weekly metric movement and repeated/regressing patterns;
- completed, abandoned, or stalled work and pending proof;
- review/intervention load, resource consumption, and policy-defined budget;
- completed provider reports explicitly supplied inside the window.
- the current weekly draft and completed Daily receipts with candidate upserts,
  no-ops, and source gaps.

Weekly prefers the draft and receipts over replaying every raw task or thread.
It dedupes repeated facts, assigns every candidate a disposition, freezes the
weekly report, applies authorized promotions, and opens the next draft.

## Weekly Working Draft And Promotion

Tasks, tickets, threads, commits, reports, and docs are evidence containers, not
knowledge destinations. Daily projects independent findings into
`.farplane/reports/interval/weekly/<YYYY-Www>/draft.md`:

```text
daily_projection(finding, current_draft)
  -> upsert(fingerprint = source_locator + intended_owner + content_digest)
   | no_op | source_gap | blocked

weekly_promotion(candidate, current_owners, authority)
  -> promoted | duplicate | monitor | dismissed | source_gap | blocked
```

The draft holds no more than five current-context bullets, plan versus actual,
problems, promotion candidates, documentation quality, completeness/follow-up
proposals, and next-week commitments. It is current operational context;
`farplane/harness.yaml` remains stable project identity, canonical owners hold
promoted knowledge, and finalized reports preserve history.

| Candidate | Weekly route | Promotion gate |
| --- | --- | --- |
| Material recurring problem | qualified ticket | material, executable, proofable, deduped, authorized |
| Reusable SOP or guardrail | `skill-maintenance` | repeatability evidence and owner authority |
| Project resource or domain decision | `doc-advisor` | future reuse or durable precedent plus destination diff |
| Project-level precedent | `doc-advisor` to `docs/MEMORY.md` | current, factual, important outside a narrower owner |
| Entity fact or relationship | `manage-wiki` | sourced identity and relationship evidence |
| Documentation-quality proposal | `doc-advisor` | changed/high-risk source and approved patch |
| Stale commitment | proposal only | sending remains separately gated |

Daily creates no problem ticket, Decision/Memory row, skill rule, project doc,
Wiki fact, quality edit, source comment, or outgoing chase. It may update only
explicitly supported mutable task progress through the authorized provider.

Weekly must disposition every candidate before finalization. After the weekly
report is frozen, each promoted route owns its validation and generated views.
Interval writes
`.farplane/reports/interval/<interval_id>/<timestamp>-knowledge.md` with source
locator, destination, digest, disposition, observed result, changed paths, and
validation. It then marks the draft finalized and opens the next week. Draft
fingerprints, current destinations, and receipts make reruns idempotent; there
is no mutable global memory ledger.

### Executive Update Extraction

Weekly also records a compact `## Executive Update` section for a separate
company-level editorial workflow. It is not a second planning loop, a Highlight
ledger, or an authorization to publish.

```text
weekly_evidence -> 0..3 executive_update_cards -> finalized_weekly_report
```

Each card must have a reader-facing change, why it matters, at least one durable
proof reference, and a draft-eligibility decision:

| Field | Requirement |
| --- | --- |
| `change` | One concrete outcome, not a task list or raw activity. |
| `why_it_matters` | Product, customer, learning, or capability implication. |
| `proof_refs` | Ticket, report, metric, commit, review, or other durable evidence. |
| `metric` | Include only a verified value or explicit `unavailable`. |
| `demo_or_video` | Include only a public, directly accessible asset; otherwise `none`. |
| `draft_eligibility` | `reader_safe`, `needs_fact_check`, or `internal_only`. |

Use repository changes, ticket/proof outcomes, metrics, and final conclusions
from project-mapped threads when locally accessible. Thread mapping does not
make a raw transcript publishable: omit private paths, system prompts, secrets,
client details, personal data, and unpublished media. An honest
`no_eligible_update` is preferable to filler. The later company publisher may
read only `reader_safe` cards and still requires its own final human approval.

The wider window can increase root-cause confidence or expose recurrence; it
does not grant broader authority or lower ticket quality.

## Problems And Immutable Report

Use ordinary Markdown:

```markdown
## Problems

- [ ] Worsening acceptance rate after the parser change. Evidence: `reports/...`. Ticket: none
- [x] Repeated stale review request. Evidence: `tickets/TASK-0100/...`. Ticket: `TASK-0110`
```

The weekly working draft accumulates source-linked candidates. Daily reports
remain immutable window receipts. Weekly snapshots the reviewed draft as an
immutable audit report before highlight, board, or canonical-owner mutation.
Later drafts carry unresolved rows by reference rather than copying history.

## Admission Predicate

```text
admit(problem, intervention, board, authority) =
  material_problem
  AND executable_next_intervention
  AND concrete_output_and_proof
  AND no_active_duplicate
  AND authorized_provider_write
  AND largest_coherent_scope
```

Every admitted ticket must produce a concrete artifact, behavior, experiment
result, or outcome. Daily stages new problem candidates and may update only
explicit mutable progress. Weekly may create a solution ticket or update a
matching `todo`. An uncertain cause/intervention can create an investigation
only when its required output is exactly:

- reproduced cause;
- ruled-out alternatives;
- selected correction;
- proof artifact.

Anything less is planning residue. Insufficiently grounded problems remain
report candidates for later Plan Next Wave refill.

Missing feedback may qualify a concrete instrumentation or feedback-loop
unblock ticket when it is material, executable, proofable, deduped, authorized,
and coherent. “Get more data” without a named signal, capture artifact,
decision it unlocks, and stop condition is not ticketable.

No numeric cap limits independently qualified work, but admission is not a
ticket-volume objective. Several independent root problems may produce several
tickets; one root problem should produce one coherent intervention.

## Board Delta Rules And Examples

| Evidence and board state | Decision | Reason |
| --- | --- | --- |
| Checkout failures reproduce to one validator branch; repair and regression proof are known; no owner exists | `create` solution ticket | Material, executable, concrete, deduped |
| Cause remains between cache invalidation and provider ordering; a bounded trace can reproduce, rule out one branch, select the fix, and preserve logs | `investigation` ticket | Output changes the correction decision |
| Two independent material root problems each pass every gate | create/update both | No arbitrary count cap |
| A substantially matching active or review ticket owns the problem | `duplicate` / no rewrite | Existing work is the owner |
| A `todo` ticket describes the right intervention but has stale priority, due date, or proof | `update_todo` | Clarify/reprioritize/date only the mutable todo |
| A stale `todo` is superseded or disproved | `reject_todo` with reason | Preserve history; do not delete |
| Matching work is active, waiting on signal, blocked in execution, review, or terminal | no rewrite | Protected state is immutable to Interval |
| “Plan the strategy,” “research options,” or “design a roadmap” | reject | No executable decision-changing output |
| Cosmetic low-impact chore with no objective/guard effect | reject | Low materiality |
| Material symptom but no grounded cause or bounded decision-changing investigation | `candidate` | Preserve uncertainty for planner refill |
| Provider cannot be queried or write authority is absent | `source_gap` / `blocked_by_authority` | Fail closed |

Ticket deltas may create, clarify, reprioritize, assign `due_at`, or reject stale
`todo` work. Interval never physically deletes history and never rewrites
active, review, waiting-signal, blocked-execution, or terminal contracts.
Spend, publishing, customer contact, account changes, and private-data use
remain behind explicit approval gates; Interval records `blocked_by_authority`
instead of performing or authorizing those side effects.

## Highlight Boundary

After report finalization and before ticket mutation, bind a stable team slug
and append at most one exceptional metric win and one material lesson-bearing
failure. Preserve minimal rows, generic project-relative links, natural-key
idempotency, and honest no-op behavior. Routine delivery is not a win.
Highlights never supply evidence for admission or trigger correction.

## Ownership Boundaries

| Decision | Owner |
| --- | --- |
| Evidence-grounded bottleneck review and Daily draft projection | Interval |
| Weekly candidate dispositions, qualified ticket deltas, and promotion receipt | Interval |
| Operational procedure or skill delta | Skill Maintenance |
| Project documentation delta | Doc Advisor |
| Entity article/link delta and projections | Manage Wiki |
| Weak-board refill from insufficiently grounded candidates | Plan Next Wave |
| Feed/provider discovery and source-backed report | provider skill |
| Harness self-improvement portfolio review | weekly Dogfood Review automation |
| Ticket execution and matured Reward check-in | Work Pulse |

Missing sources never cause Interval to invoke another workflow. Record the gap,
finish the report with available evidence, and apply no authority-unsafe delta.
The operator summary states what changed and why, admitted and rejected ticket
deltas, blocked systems, missing feedback, and the next native Goal/heartbeat
owner without starting that route.
