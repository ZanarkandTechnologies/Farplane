---
template_id: ticket-template
template_version: "0.1.4"
feature_refs:
  - FEAT-0007
  - FEAT-0065
ticket_id: TASK-0251
title: Add Farplane ops-memory as active operating state
phase: complete
status: done
owner: codex
claimed_by:
priority: high
depends_on:
  - TASK-0247
blocked_by: []
ready: false
approval_required: false
requires_qa: true
requires_demo: false
created_at: 2026-06-30T08:11:57Z
updated_at: 2026-06-30T08:58:00Z
next_action: complete; run a future manual Pulse beat to observe ops-memory frontier behavior
last_verification: scoped completion review TAS-A/pass, validators passed, and ops-memory implementation evidence recorded
---

# TASK-0251: Add Farplane Ops-Memory as Active Operating State

## Summary
Add `farplane/ops-memory.md` as Farplane's flexible current operating memory:
the short-lived second brain for active focus, active projects, milestone
paths, next frontier tickets, constraints, and parking-lot items. This keeps
stable files split by responsibility while giving Pulse and intervals one
compact place to understand what the autonomous team is trying to accomplish
right now.

The decisive path is to add one Markdown memory surface, wire `pulse-update`
and `interval-update` to read and maintain it, and document the boundary in the
Pulse/Interval framework. Do not introduce a separate roadmap object, project
registry, database, UI, or broad schema layer in this ticket.

## Scope
- `In:`
  - Create `farplane/ops-memory.md` with YAML front matter and compact sections
    for current focus, active projects, critical paths, next frontier,
    constraints, parking lot, and recent decisions.
  - Update `skills/pulse-update/SKILL.md` so Pulse reads ops-memory before
    next-wave planning and updates it when the active frontier changes.
  - Update `skills/interval-update/SKILL.md` and
    `skills/interval-update/references/workflows/priority-planning.md` so Daily
    and Weekly can refresh ops-memory as a strategy input/output.
  - Update `docs/farplane-framework/pulse-and-interval-loop.md` to explain the
    split between stable project files, active ops-memory, tickets, and
    receipts.
  - Optionally update `farplane/automations.md` prompt wording only if needed
    to make the ops-memory read/write expectation visible without bloating the
    automation config.
  - Run focused validators and a grep/readback proving the new surface is
    discoverable by Pulse and intervals.
- `Out:`
  - No new roadmap registry, project schema, database, UI, scheduler, daemon,
    or hidden queue.
  - No KPI/goals/products rewrite.
  - No change to automation cadence or live child-thread caps.
  - No broad ticket metadata migration such as `autonomy_profile` or
    `review_mode`.
  - No execution of generated milestone work inside this ticket.

## Delta
- `Before:`
  - Farplane has stable `goals.md`, `products.md`, `harness.md`, dated
    interval reports, tickets, and Pulse reports.
  - When no ready ticket exists, Pulse can create one tactical next-wave ticket
    from Weekly/Daily strategy, but it has no compact active memory that shows
    the full current focus, multiple active projects, critical path, and next
    frontier.
  - The result is timid one-ticket planning and accidental preference for easy
    maintenance work.
- `After:`
  - `farplane/ops-memory.md` becomes the flexible active operating state.
  - Pulse reads ops-memory, latest Daily/Weekly reports, goals, products, and
    board state before next-wave planning.
  - Pulse may update the current frontier and create tickets from the active
    critical path, while execution remains bounded by heartbeat policy caps.
  - Daily/Weekly refresh ops-memory rather than trying to pre-plan every ticket.
- `Why now:`
  - Live Pulse proved that next-wave planning works mechanically, but it plans
    crumbs. The operator wants the autonomous team to see and pursue the whole
    path to the current daily focus without adding many new artifact concepts.
- `First-principles basis:`
  - `objective:` make autonomous company operation legible and ambitious while
    keeping execution bounded.
  - `need:` one current-state surface that separates active working memory from
    stable goals/products and from dated reports.
  - `assumptions:` Markdown is enough for the first version; multiple active
    projects can be represented as compact sections, not a registry.
  - `root_cause:` Pulse lacks a durable active context between interval reports
    and tickets, so it optimizes for the next safe ticket instead of the
    milestone frontier.
  - `constraints:` no new scheduler, database, schema-heavy PM system, or hidden
    automation state.
  - `first_viable_slice:` one `ops-memory.md` template plus skill/doc wiring.
  - `proof_or_falsification:` a future empty-board Pulse can name the active
    focus, critical path, and next frontier from ops-memory before creating
    tickets.
  - `tradeoff:` accept one mutable working-memory file instead of many new
    roadmap/project artifacts.
  - `non_goals:` project management UI, full second-brain database, external
    account integrations, and live KPI dashboard.

## Change Plan

### Change 1: create the ops-memory surface

```text
fixes:
  - Farplane needs one flexible active-state file for current focus and
    multi-project frontier planning without creating a roadmap object system.
before:
  - Active focus is spread across latest interval reports, tickets, and chat.
after:
  - `farplane/ops-memory.md` exists with compact sections:
    Current Focus, Active Projects, Critical Paths, Next Frontier,
    Constraints, Parking Lot, Recent Decisions, and Pulse Notes.
read:
  - path: farplane/goals.md
    reason: align ops-memory headings with current KPI axes and north star
  - path: farplane/products.md
    reason: align active projects with product lanes and workflows
  - path: docs/farplane-framework/pulse-and-interval-loop.md
    reason: reuse existing Pulse/Interval lifecycle vocabulary
write:
  - path: farplane/ops-memory.md
    change: add the active operating memory file with YAML front matter and
      initial sections seeded from the current discussion and latest strategy
operation:
  - keep the file human-editable Markdown, not JSON schema
  - allow multiple active projects as repeated short project blocks
  - include a tiny cap pointer that says caps live in
    `.farplane/automation/heartbeat-policy.json`
signature_or_type_impact:
  - ops_memory(project) -> current_focus + active_projects + next_frontier
routes:
  docs: update_docs
  qa: tests
  review: inline
qa:
  - verify the file exists and includes the required headings
  - verify it does not duplicate full goals/products content
failure_modes:
  - ops-memory becomes a second goals file
  - active projects become too detailed and recreate ticket bodies
  - maintenance work gets promoted into focus without a reward reason
```

### Change 2: teach Pulse to use ops-memory before next-wave planning

```text
fixes:
  - Pulse can create one tactical ticket from strategy but does not yet require
    a full current-focus frontier before ticket creation.
before:
  - `pulse-update` reads goals, products, tickets, recent interval reports, and
    policy, then creates a bounded tactical next wave when empty.
after:
  - `pulse-update` also reads `farplane/ops-memory.md` when present.
  - Empty-board planning first checks active focus, active projects, critical
    path, next frontier, constraints, and parking lot.
  - Pulse creates tickets from the highest-signal frontier step, not from
    low-value maintenance unless maintenance unblocks the active focus.
read:
  - path: skills/pulse-update/SKILL.md
    reason: current next-wave planning contract
  - path: .farplane/automation/heartbeat-policy.json
    reason: caps remain policy, not ops-memory state
write:
  - path: skills/pulse-update/SKILL.md
    change: add ops-memory to state reads, todo list, next-wave priority ladder,
      output expectations, and failure modes
operation:
  - define `ops_memory_frontier` as a planning input, not a separate execution
    authority
  - record in Pulse reports when ops-memory is missing, stale, or overridden by
    Daily/Weekly strategy evidence
  - keep `maxChildThreadsPerBeat` and future `maxTicketsCreatedPerWave` in
    heartbeat policy, not in ops-memory
signature_or_type_impact:
  - pulse_update(...reads farplane/ops-memory.md?) -> next_wave_ticket_deltas
    should cite active_project/frontier when used
routes:
  docs: update_docs
  qa: tests
  review: inline
qa:
  - focused grep confirms Pulse names `ops-memory.md`
  - manual checklist confirms Pulse still excludes unsafe/human-gated work
failure_modes:
  - Pulse treats ops-memory as permission to mutate goals or product boundaries
  - Pulse plans every possible project instead of the active frontier
  - caps become duplicated between ops-memory and heartbeat policy
```

### Change 3: teach intervals to refresh ops-memory

```text
fixes:
  - Daily and Weekly currently emit reports and strategy inputs, but the active
    focus does not have a compact writable home between reports and tickets.
before:
  - Interval reports carry focus, bets, lane distribution, downstream guidance,
    and Pulse constraints in dated report files only.
after:
  - `interval-update` reads ops-memory as part of default context when present.
  - Priority planning may propose or apply compact ops-memory refreshes:
    current focus, active projects, next frontier, constraints, and parking lot.
  - Material goals/products/harness changes still route to their owning files,
    not ops-memory.
read:
  - path: skills/interval-update/SKILL.md
    reason: default context refs and output contract
  - path: skills/interval-update/references/workflows/priority-planning.md
    reason: final strategy synthesis and downstream guidance owner
  - path: skills/interval-update/templates/interval-report.md
    reason: report template may need a compact ops-memory delta section
write:
  - path: skills/interval-update/SKILL.md
    change: include ops-memory in default refs and outputs
  - path: skills/interval-update/references/workflows/priority-planning.md
    change: define ops-memory refresh guidance and guardrails
  - path: skills/interval-update/templates/interval-report.md
    change: add a compact `Ops Memory Delta` or strategy-output slot if needed
operation:
  - Daily may refresh today's focus/frontier
  - Weekly may refresh active projects and leverage bets
  - both must keep durable goal/product deltas out of ops-memory unless they
    are merely active-focus notes
signature_or_type_impact:
  - interval_update(...) -> interval_report + pulse_guidance + ops_memory_delta?
routes:
  docs: update_docs
  qa: tests
  review: inline
qa:
  - focused grep confirms interval skill/template names ops-memory
  - manual review confirms ops-memory does not replace dated interval reports
failure_modes:
  - interval reports become giant roadmap dumps
  - ops-memory accumulates stale projects because intervals only append
  - strategy changes bypass goals/products approval boundaries
```

### Change 4: document the memory split and cap ownership

```text
fixes:
  - The project needs a simple explanation for why `ops-memory.md` exists and
    where caps live.
before:
  - Framework docs describe Pulse, Daily, Weekly, goals, products, tickets, and
    reports, but not active operating memory.
after:
  - `docs/farplane-framework/pulse-and-interval-loop.md` explains:
    stable truth = harness/goals/products;
    active operating memory = ops-memory;
    execution atoms = tickets;
    receipts = reports/ledgers;
    caps = heartbeat policy.
read:
  - path: docs/farplane-framework/pulse-and-interval-loop.md
    reason: lifecycle documentation owner
  - path: farplane/automations.md
    reason: ensure automation prompt remains lean and points to skills
write:
  - path: docs/farplane-framework/pulse-and-interval-loop.md
    change: add active ops-memory model, before/after behavior, and cap owner
  - path: farplane/automations.md
    change: optional one-line prompt/read expectation only if the skill docs
      are not discoverable enough
operation:
  - include a concise before/after example showing one active project and one
    parked maintenance item
  - state that caps remain in `.farplane/automation/heartbeat-policy.json`
signature_or_type_impact:
  - no code interface impact
routes:
  docs: update_docs
  qa: tests
  review: inline
qa:
  - run doc/reference validators
  - grep for contradictory `roadmap` language that implies a new object system
failure_modes:
  - docs over-explain and bloat the always-read surfaces
  - automation prompt duplicates skill logic
```

## Done

```text
done_when:
  - `farplane/ops-memory.md` exists with YAML front matter and compact active
    operating memory sections
  - `skills/pulse-update/SKILL.md` reads and uses ops-memory for empty-board
    next-wave planning before creating tickets
  - `skills/interval-update/SKILL.md` and priority-planning guidance define how
    Daily/Weekly refresh ops-memory without replacing goals/products/reports
  - `docs/farplane-framework/pulse-and-interval-loop.md` documents the memory
    split and cap ownership
  - ticket metadata and relevant docs/skill validators pass
  - no live automation cadence/cap is changed
```

## QA Strategy

```text
qa_strategy:
  proof_weight: tests
  checks:
    - python3 tickets/scripts/check_ticket_metadata.py
    - python3 skills/skill-maintenance/scripts/check_skills.py --write
    - python3 bin/validators/check_doc_refs.py
    - python3 bin/validators/sync_skill_registry.py --check
    - git diff --check -- farplane/ops-memory.md skills/pulse-update/SKILL.md skills/interval-update/SKILL.md skills/interval-update/references/workflows/priority-planning.md skills/interval-update/templates/interval-report.md docs/farplane-framework/pulse-and-interval-loop.md farplane/automations.md
  manual:
    - inspect `farplane/ops-memory.md` for the active-memory boundary:
      current focus, multiple active projects, critical paths, next frontier,
      constraints, parking lot, recent decisions, and Pulse notes
    - inspect Pulse wording to confirm it plans from active frontier and does
      not plan every possible project
    - inspect Interval wording to confirm Daily/Weekly refresh ops-memory and
      keep material goals/products changes in their owning files
    - verify caps are referenced as `.farplane/automation/heartbeat-policy.json`
      and not duplicated as mutable ops-memory state
  delegated_lanes:
    - reviewer for final completion review if this ticket is implemented as
      Goal-backed material skill/doc work
  review:
    - rubric: docs_prompts_skills
      required_tas: TAS-A or precise needs-revision
  evidence:
    - farplane/ops-memory.md
    - updated skill/doc diffs
    - validator outputs recorded in progress.md or final ticket writeback
  goal_advisor_inputs:
    proof_route: docs_and_skill_contract_checks
    final_evidence: ops-memory file, skill/doc diffs, validator outputs, reviewer receipt if delegated
    final_checkpoint: completion review verifies no new roadmap/project registry was introduced
  residual_risk:
    - The first ops-memory shape may need resizing after one or two live Pulse
      beats; do not add schema until the Markdown file proves too loose.
```

## Docs Strategy

```text
docs_strategy:
  outcome: update_docs
  doc_targets:
    - docs/farplane-framework/pulse-and-interval-loop.md
    - farplane/ops-memory.md
    - skill docs for pulse-update and interval-update
  no_docs_reason:
  validation:
    - python3 bin/validators/check_doc_refs.py
    - focused grep for `ops-memory`
```

## Links

- `program:` `tickets/TASK-0251/program.md`
- `progress:` `tickets/TASK-0251/progress.md`
- `generated_goal_prompt:` `tickets/TASK-0251/artifacts/native-goal-prompt.md`
- `refs:`
  - `farplane/goals.md`
  - `farplane/products.md`
  - `farplane/harness.md`
  - `docs/farplane-framework/pulse-and-interval-loop.md`
  - `skills/pulse-update/SKILL.md`
  - `skills/interval-update/SKILL.md`
  - `skills/interval-update/references/workflows/priority-planning.md`
  - `.farplane/automation/heartbeat-policy.json`
- `review:` `tickets/TASK-0251/artifacts/review/impl-plan-review.md`
- `completion_review:` `tickets/TASK-0251/artifacts/review/completion-review.md`
- `scoped_evidence:` `tickets/TASK-0251/artifacts/review/scoped-evidence.md`

## Notes

- `Decision:` use `farplane/ops-memory.md`, not `farplane/ops.md`, to make the
  memory split explicit.
- `Before:` roadmaps risk becoming a new artifact family.
- `After:` roadmap/project/critical-path thinking lives as flexible sections in
  ops-memory.
- `Example:` ops-memory can contain two active projects, such as
  `evidence-to-content loop` and `pulse/interval autonomy`, each with a done
  signal, critical path, next frontier, and parked low-value maintenance.
- `Caps:` execution and planning caps remain policy-owned in
  `.farplane/automation/heartbeat-policy.json`.
- `Blast radius:` docs and skill contracts only; no runtime code or live
  automation config change unless the implementation proves a one-line prompt
  pointer is necessary.
- `Risks / rollback:` delete or park `farplane/ops-memory.md` and remove skill
  references if it creates more maintenance than clarity.
- `Follow-ups:`
  - After implementation, run one manual Pulse beat and judge whether it names
    the active focus/frontier before creating tickets.
  - Consider `maxTicketsCreatedPerWave` only after observing whether Pulse
    over- or under-plans from ops-memory.
- `plan_qa:`
  - `minimal_required_version:` pass
  - `reuse_before_new_surface:` pass - reuses Markdown project files, skills,
    and existing Pulse/Interval docs rather than adding a registry or database
  - `least_parameters:` pass - no new cap keys required in this ticket
  - `new_files_functions_justified:` pass - one new file is the chosen active
    operating memory owner
  - `minimal_impl_plan_claim:` pass
  - `existing_service_fit:` pass - stable goals/products/harness and dated
    reports are not good owners for churn-heavy active focus
  - `goal_advisor_ready:` pass
  - `clarifying_questions:` pass - operator selected name and multi-project
    shape
  - `change_plan_locality:` pass
  - `qa_strategy_explicit:` pass
  - `docs_strategy:` pass
  - `grounding_evidence:` local_only - this is a local harness contract change
  - `highest_risk:` ops-memory becomes another stale artifact instead of the
    compact current operating brain
  - `fix_or_deferral:` keep first version compact and require Pulse/Interval to
    update existing sections rather than append endlessly
