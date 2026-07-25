---
title: "BAU Interval Review-to-Ticket Contract"
status: active
owner: interval-update
kind: reference
---

# BAU Interval Review-to-Ticket Contract

Daily and Weekly are evidence profiles over one decision primitive:

```text
review_interval(interval_id, review_window, evidence, board, authority)
  -> finalized_report
   + sparse_highlights
   + candidate_interventions
   + ticket_deltas
   + source_gaps
```

The invariant order is:

1. resolve the configured provider and gather the bounded evidence window;
2. review metric/outcome movement through bottleneck and root cause;
3. compare interventions and record every admission decision;
4. finalize the immutable report;
5. append independently selected TASK-0405 highlights;
6. apply qualified ticket deltas without executing them.

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
8. Map every actionable finding to one qualified ticket delta or an explicit
   no-action reason. Decide independently; there is no count target or cap.

## Daily Evidence Profile

Daily reviews the recent window, normally 24 hours:

- current metric movement and unavailable/stale readings;
- completed, blocked, abandoned, active, and review-waiting outcomes;
- repeated execution failures, attention drift, and feedback obligations;
- fresh proof, review artifacts, and latest completed provider reports supplied
  through `context_refs`;
- prior unresolved Interval problems needed to understand current evidence.

Daily may refresh selected/pinned stale metrics when explicitly enabled. It
does not call the provider whose completed report it reads.

## Weekly Evidence Profile

Weekly executes the same reasoning and admission gates over the wider window:

- completed Daily reports and their carried/resolved problems;
- weekly metric movement and repeated/regressing patterns;
- completed, abandoned, or stalled work and pending proof;
- review/intervention load, resource consumption, and policy-defined budget;
- completed provider reports explicitly supplied inside the window.

The wider window can increase root-cause confidence or expose recurrence; it
does not grant broader authority or lower ticket quality.

## Problems And Immutable Report

Use ordinary Markdown:

```markdown
## Problems

- [ ] Worsening acceptance rate after the parser change. Evidence: `reports/...`. Ticket: none
- [x] Repeated stale review request. Evidence: `tickets/TASK-0100/...`. Ticket: `TASK-0110`
```

The draft records movement, bottleneck/root-cause reasoning, intervention
comparison, and intended board deltas. Finalization makes it an immutable audit
snapshot before highlight append and board mutation. Later reports carry
unresolved rows by prior-report link rather than rewriting history.

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
result, or outcome. A known cause and known intervention creates a solution
ticket or updates a matching `todo`. An uncertain cause/intervention can create
an investigation only when its required output is exactly:

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
| Evidence-grounded bottleneck review and qualified ticket delta | Interval |
| Weak-board refill from insufficiently grounded candidates | Plan Next Wave |
| Feed/provider discovery and source-backed report | provider skill |
| Harness self-improvement portfolio review | weekly Dogfood Review automation |
| Ticket execution and matured Reward check-in | Work Pulse |

Missing sources never cause Interval to invoke another workflow. Record the gap,
finish the report with available evidence, and apply no authority-unsafe delta.
The operator summary states what changed and why, admitted and rejected ticket
deltas, blocked systems, missing feedback, and the next native Goal/heartbeat
owner without starting that route.
