---
title: "Farplane engine PRD"
status: active
owner: farplane
created_at: 2026-05-26
updated_at: 2026-10-15
version: "1.0"
refs:
  - docs/guides/work-loop.md
  - docs/guides/project-files.md
  - farplane/harness.yaml
  - farplane/metrics.yaml
  - tickets/README.md
---

# Farplane engine PRD

## Product Thesis

Farplane is a file-backed operating system for moving an operator-chosen
commercial bet toward money. It helps a human operate long-running agent work
through visible project goals, current evidence, bounded actions, tickets,
capability skills, automations, and reviewable proof.

```text
Farplane = commercial intent + execution + evidence
```

The engine's product promise is simple:

> Give Farplane an explicit customer, painful problem, offer, price, and route
> to sale. It should keep the resulting projects moving, expose the constraint
> closest to money, ask for the smallest missing fact or decision, and preserve
> enough evidence for the operator to continue, revise, or kill the bet.

The operator owns strategy. Farplane may expose when evidence contradicts the
commercial hypothesis, but it does not claim to autonomously discover a novel
business strategy or outperform the operator's judgment. Its strength is
maintaining context, following through, reconciling evidence, and keeping the
next consequential action visible.

### Direction Status

This PRD is the accepted product direction. The money-execution boundary and
lean Daily/Weekly Company OS contract are implemented by the active automation
prompts and the `report-gen` skill (`daily` and `weekly` modes). The AI Office
is the Farplane bunker, specified in its own PRD (see AI Office Product Story).
The Interval weekly-draft and broad promotion machinery is legacy reference and
has no active Daily or Weekly binding.

Since 2026-10-01, active tasks live in GitHub Issues in each project's own
repository (`tickets/README.md`); `tickets/TASK-*/` is legacy proof and
migration history. Scheduled jobs run as Claude Code scheduled tasks over
`farplane/automations/` records
([work loop guide](guides/work-loop.md)).
There is no execution heartbeat: Work Pulse was retired on 2026-10-12 (#41), and Weekly
Self-Improvement and Monthly Registry Consolidation are killed. No automation
executes issues.

## Problem

General-purpose agents can produce useful work, but sustained operation breaks
down when:

- priorities and constraints live only in chat;
- multiple planners or automation loops compete to choose direction;
- waiting for humans or external signals consumes execution capacity;
- experiments, QA, review, and check-ins use separate state systems;
- evidence is scattered across generic runtime directories;
- reusable workflows are confused with independent products or controllers;
- self-improvement adds machinery before the basic work loop is proven.
- work looks productive but has no evidenced relationship to earning,
  retaining, accelerating, or protecting money.

The result is hidden state, duplicate work, weak attribution, inflated
metadata, and operator distrust.

## Audience

- Primary: founders and operators running agent-heavy projects.
- Secondary: engineers and agent designers maintaining reusable harnesses.
- Tertiary: collaborators reviewing artifacts, decisions, and evidence without
  reading raw transcripts or runtime logs.

## Jobs To Be Done

1. When I define a commercial bet, I want agents to execute bounded work that
   moves it toward money without losing my constraints.
2. When work spans turns or days, I want durable state that another agent can
   resume without hidden conversation context.
3. When an agent needs review or waits for reality, I want execution capacity
   released while the obligation remains visible.
4. When the board runs out of useful work, I want the smallest next commitments
   grounded in the commercial hypothesis, money-linked evidence, ticket
   history, and current constraints.
5. When the harness changes itself, I want the cheapest honest proof route and
   a reversible promotion decision.
6. When I inspect the system, I want every important claim to lead back to an
   owning ticket, report, metric observation, or durable policy file.

## Operating Model

```text
project program
-> GitHub Issues in the project's own repository
-> the operator, or a session they start, runs goal-advisor on an issue
   (native Goal); small work runs directly
   -> due check-ins (`check-in` issues with `Due: YYYY-MM-DD`) are listed by
      Daily Collect, surfaced in the morning brief, and resumed the same way
-> scheduled jobs collect, report, and propose (no execution heartbeat)
-> issue-local QA, review, and one proof comment + `gh issue close`
-> durable learning back into metric objectives, policy, skills, docs, or features
```

Scheduled jobs are `farplane/automations/*.md` records run as Claude scheduled
tasks (`runtime: claude`): Morning (Daily Collect, Metrics Refresh, Knowledge
Update, Daily Operating Update, then the brief), Report Gen (weekly review),
Intel Digest (Bookmark Recovery, then Feed Scout), Profile Refresh, Session
Friction Retro, and Token Burn. They never create, close, label, assign, or
edit issues and never start runs. The business loop for bunker floors (step
plans, Monday seeding through `farplane loop monday`) is owned by the bunker
PRD's [The operating loop](../../Farplane-UI-v2/docs/prd.md#the-operating-loop-how-a-business-runs).

Every project uses the same decision rule:

```text
commercial hypothesis
-> current evidence
-> constraint closest to money
-> smallest useful action, question, or decision
-> observed result
-> continue | revise | stop
```

Delivery, learning, distribution, capability, and maintenance are supporting
work. They enter the loop only when evidence or the project configuration ties
them to earning, retaining, accelerating, or protecting money. Missing money
evidence remains unknown rather than being replaced with activity proxies.

### Daily And Weekly Reviews

Daily and Weekly are execution reviews, not independent strategy engines.
Daily maintains each project's current memory, surfaces material blockers or
missing evidence, and selects the smallest useful follow-up. Weekly compares
expected movement with observed results, consolidates what changed, carries
forward the closest commitments to monetization, and escalates contradictions
in the customer, problem, offer, price, or route to sale to the operator.

Reasoning techniques such as plan-versus-actual comparison, root-cause
analysis, and intervention comparison are helpers for filling the existing
project and report forms. They do not require separate workflow stages,
artifacts, or governance machinery.

### Canonical State

| Surface | Responsibility |
| --- | --- |
| `farplane/harness.yaml` | identity, planning areas/instructions, authority, capability refs, selected metrics |
| `farplane/metrics.yaml` | metric meaning, direction, freshness, and guard rules |
| `farplane/bindings.yaml` | safe provider coordinates |
| `farplane/automations/` | one record per live scheduled job; the steps they call in `steps/` |
| GitHub issue in the project's repo | work, Goal program, progress comments, blockers, review |
| `tickets/` | ticket policy, template, legacy `TASK-*` proof and history |
| `skills/*`, `.agents/skills/*` | reusable and project-local capabilities |
| `.farplane/reports/`, `.farplane/metrics/` | derived context and observations |

### Minimal Ticket Lifecycle

```text
todo | active | awaiting_review | waiting_signal |
blocked | done | failed | rejected
```

Required ticket metadata is limited to identity, status, and timestamps.
Priority, claim, dependencies, human gate, and compute target are sparse
routing overrides. QA, reward, review, evidence, blockers, and next actions
remain in the ticket body, Goal Packet, progress log, or artifacts.

### Work Sources

| Source | Authority |
| --- | --- |
| Feed Scout (in Intel Digest) | source report, candidates, recovery candidates, and single-source adopt/adapt/reject/defer verdicts (no tickets) |
| Daily/Weekly review | project memory, targeted follow-ups, weekly reports, and operator-visible work proposals; no independent strategy or ticket admission |
| Operator | explicit direction, feedback, correction, or approval; opens issues |

Only the operator, or a session they start, executes issues and due check-ins.

## Functional Requirements

### FR-1: Project Program

- A project can express stable policy, planning areas, selected metrics,
  provider bindings, capability routes, and automation topology in tracked files.
- Generated observations never silently replace those source owners.

### FR-2: Ticket-As-Program

- A material task can be reconstructed from its GitHub issue body (scope,
  `## Goal program`, `## Current Goal state`), its top-level comments, and
  linked repository artifacts.
- Ticket state is sufficient for selection, resumption, proof, review, and
  closeout without transcript memory.

### FR-3: Operator-Started Execution

- No heartbeat, dispatcher, or refill planner exists; Work Pulse is retired.
- Work enters as a GitHub issue in the project's own repository. The operator,
  or a session they start, runs `goal-advisor` on it (native Goal) or does
  small work directly.
- Ordinary issues and due check-ins use the same path: a check-in is an open
  `check-in` issue with `Due: YYYY-MM-DD`, listed by Daily Collect, surfaced in
  the morning brief, and resumed through `goal-advisor`'s Delayed Check-In
  Resume prompt.
- Review waits, signal waits, and blocked issues hold no session; their state
  lives in issue labels or body.

### FR-4: Human Review

- A session that needs human review records it on the issue (label or body)
  and ends; it does not hold the issue open waiting.
- Queue size provides backpressure but does not itself trigger chasing.
- The morning brief folds overdue check-ins into one decide-or-kill line; no
  automation sends reminders on an issue.

### FR-5: Scheduled Sources

- The scheduled jobs in `farplane/automations/` (Morning, Report Gen, Intel
  Digest, Profile Refresh, Session Friction Retro, Token Burn) run as bounded
  cron records, not heartbeats.
- Scheduled sources write bounded reports or context but do not admit proactive
  tickets. Daily/Weekly maintains project memory and may apply only explicitly
  authorized comments on existing issues. Candidates reach the operator through
  reports and the morning brief; work starts only when an issue is opened.
- Daily/Weekly does not choose new strategy; Feed Scout does not create or
  execute opportunities.

## AI Office Product Story

The AI office is the Farplane bunker. Its one product doc, covering what it is, why, what was turned
down and what's next, is `docs/prd.md` in the farplane-bunker repo (Farplane-UI-v2). This PRD covers the
engine underneath it.

### FR-6: Self-Improvement

- Every proposed change names a target surface, objective, feedback class,
  proof route, budget, guard, and rollback.
- Immediate feedback runs inside the current Goal-backed ticket.
- Delayed feedback stays on the original ticket and resumes through its
  Check-In Program.
- Accepted patterns require transfer evidence before doctrine promotion.
- Self-improvement is one evidence-gated planning area competing for operator
  attention, not a separate loop or guaranteed weekly quota.

### FR-7: Capability Boundary

- Important recurring artifact workflows are callable skills, not independent
  planning controllers by default.
- Independent state is introduced only for a genuinely distinct event stream,
  authority boundary, budget, or prioritization policy.
- Long-lived prospects remain CRM records; only bounded actions become tickets.

### FR-8: Proof And Observability

- QA evidence and reviewer receipts live under the ticket they judge.
- Reports and registries link to source evidence rather than copying canonical
  state.
- Missing or ambiguous evidence becomes a source gap, not an inferred pass.

### FR-9: Completion Learning Without Events

- An issue closes with one proof comment and `gh issue close`; Core emits no
  completion event and runs no completion mining (retired 2026-10-13: it had
  not run since tickets moved to GitHub Issues, and nothing read its output).
- The closing session routes each lesson to its owner (skill, eval, validator,
  or `docs/MEMORY.md`), and the daily `report-gen` automation reads issues
  closed since its last run.
- `hooks.json` owns lifecycle telemetry plus bounded deterministic guards such
  as final-response length; it never owns completion.

### FR-10: Money-Execution Boundary

- Project goals state the commercial hypothesis or their explicit contribution
  to earning, retaining, accelerating, or protecting money.
- Daily and Weekly may read project-local harness configuration, metric
  definitions, and current observations when filling existing memory and report
  forms.
- Nonfinancial progress is material only when its relationship to money is
  explicit in configuration or supported by evidence.
- When evidence challenges the customer, painful problem, offer, price, or
  route to sale, the system escalates the strategy decision to the operator.
- Legal, trust, delivery-quality, authority, and runway constraints remain hard
  guards; short-term cash does not override them.

## Success Metrics

The primary outcome is verified money movement. Each deployment chooses the
authoritative money measure available to it, such as cash collected, gross
profit, recurring revenue, retained revenue, or validated paid commitments.
Pre-revenue measures are diagnostic only and must state their evidenced path to
the selected money outcome.

### Selected Money Outcome

Each deployment selects the applicable authoritative outcome; it does not
maximize every row simultaneously.

| Metric | Direction | Meaning |
| --- | --- | --- |
| `revenue_usd` | maximize | realized revenue from the authoritative connected business system; missing access remains unknown rather than zero |
| `active_subscriptions` | maximize | paid active relationships when subscriptions represent the selected money model |

### Money-Linked Diagnostic Measures

These measures guide work only when the project configuration states their
evidenced relationship to the selected money outcome.

| Metric | Direction | Meaning |
| --- | --- | --- |
| `github_views` | maximize | builders find the repository; social reach is measured by the media business, not Farplane |
| `accepted_evidence_cycles` | maximize | ablations, experiments, or proof cycles finish with accepted reusable evidence |
| `activated_external_projects` | maximize | nearby non-standard projects run the current contract after migration |

### System-Health Guards

These protect execution quality; they are not alternate business objectives.

| Metric | Direction | Meaning |
| --- | --- | --- |
| `auto_completion_rate` | maximize | completed associated tickets required no post-start human intervention |
| `intervention_free_ticket_count` | maximize | autonomous completion produces useful throughput |
| `ticket_intervention_turn_count` | minimize within quality floor | supervision falls without false completion or drift |
| `rejected_ai_ticket_count` | minimize; guard ≤ 1/day | rejected AI-planned work backpressures planner quality |
| `todo_unclaimed_ticket_count` | bounded operating signal | executable supply is visible without uncontrolled backlog growth |
| `accepted_harness_improvements` | increase selectively | self-improvement produces reviewed durable value |
| `latest_eval_pass_rate` | diagnostic | latest local eval result is visible without treating unrelated suites as one global guard |

Metric semantics and grouped refresh prompts live in `farplane/metrics.yaml`; provider coordinates
live in `farplane/bindings.yaml`. Dispatch correctness, review-worker release,
resumeability, maintenance precision, and experiment-packet completeness remain
binary feature/test gates until repeated operation justifies registered metric
cards.

## Acceptance

- [x] Product-scoped Pulse controllers and product state are retired, and so
      is Work Pulse (#41); no execution heartbeat exists.
- [x] `harness.yaml` owns typed identity, planning areas, capabilities, and metric selection.
- [x] Ordinary issues and due check-ins start through `goal-advisor` (or
      directly) from the operator or a session they start.
- [x] Ticket metadata is reduced to lifecycle and sparse routing.
- [x] Human review and signal waits hold no session; their state lives on
      the issue.
- [x] Daily/Weekly uses the project-memory, money-linked review contract and
      does not independently admit tickets or choose strategy.
- [x] Immediate and delayed self-improvement use ticket Goal Packets.
- [x] `metrics.yaml` owns metric definitions; bindings own provider mechanics.
- [x] Completion learning needs no event or miner; closed issues reach the
      daily report.
- [x] QA and review evidence are ticket-scoped.
- [x] Current Farplane project files and init templates validate.
- [ ] Representative scheduled operation proves the loop over longer real
  windows without unacceptable duplicate supply or operator burden.

The remaining acceptance work is representative scheduled operation over
longer real windows. The AI Office's own acceptance lives in the bunker PRD.

## Non-Goals

- A hidden scheduler, daemon, hosted control plane, or autonomous cloud wrapper.
- A separate planner or worker pool for every capability or artifact category.
- A generic runtime, evidence, review, or hand-maintained registry ontology.
- Treating reports, CRM records, prospects, or observations as tickets by
  default.
- High-volume content-market experimentation without a separate budget and
  interference contract.
- Automatic doctrine promotion from one successful experiment.
- Silent changes to human thesis, spend, publishing, customer contact, deploy,
  or destructive authority.

## Risks And Backpressure

| Risk | Backpressure |
| --- | --- |
| Automations create busywork | jobs only report and propose; the operator opens issues; search open issues before creating one |
| Review queue overwhelms operator | waits hold no session; the morning brief folds overdue check-ins into one decide-or-kill line |
| Delayed experiments interfere | explicit experiment WIP and delayed-live caps |
| Reports become alternate planners | source-specific authority and report Problems ledger |
| Self-improvement bloats the harness | hardening/refinement proof, toy/eval routes, rollback, transfer tests |
| Generated state becomes canonical | owner-named source files and registry/report links back to owners |
| Minimal schema hides necessary state | Goal Packet and ticket artifacts retain detail outside frontmatter |

## Not Yet Built

- Conversation-to-Work alignment as a PM evidence source: match conversations
  to exact Projects and Work by supported identifiers, record coverage and
  unmatched conversations, and distinguish discussion, decision, deliverable,
  and verified result. Message volume or chat time alone never proves progress
  or waste.

## Release And Change Policy

This engine contract is the current standard. Future changes must begin from observed operating
failures or accepted operator direction, update the smallest owner surface, and
prove that the change improves the relevant metric without violating quality,
authority, or proof constraints.

Structural replacements of the engine kernel require an explicit reviewed PRD or
architecture decision. Ordinary refinements should update the owning guide,
skill, template, validator, or ticket contract without inventing a new
framework generation name.
