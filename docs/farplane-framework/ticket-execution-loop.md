---
title: "Ticket Execution Loop"
status: active
owner: farplane-framework
created_at: 2026-06-29
updated_at: 2026-06-29
framework_template_version: "0.2.0"
tags:
  - farplane
  - lifecycle
  - tickets
  - goals
  - review
refs:
  - docs/farplane-framework/README.md
  - docs/farplane-framework/lifecycle.md
  - docs/features/FEAT-0007-ticket-as-durable-task-memory.md
  - docs/features/FEAT-0008-artifact-first-qa-and-completion-proof.md
  - docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md
  - docs/MEMORY.md
---

# Ticket Execution Loop

Ticket execution is the path from a human-shaped idea to a reviewed, completed
artifact. The loop is intentionally split into human judgment, durable
planning, autonomous execution, and independent proof:

```text
ticket_execution_lifecycle(human_intent)
  -> brainstorm_or_advice
  -> ticket.md
  -> impl_plan(ticket.md)
  -> reviewer_plan_review
  -> goal_advisor(ticket.md)
  -> native_goal_execution
  -> QA/proof artifacts
  -> reviewer_completion_review
  -> closeout + docs/memory writeback
```

The human conversation comes first when the direction is still a product,
workflow, architecture, prompt, or harness choice. `brainstorm`,
`deliberative-advice`, `deep-interview`, `prd`, `spec-to-ticket`, or a direct
operator decision turns fuzzy intent into an accepted direction. Once the
direction is accepted, the ticket becomes the task-local source of truth and
execution can become autonomous inside that scope.

## Phase Owners

| Phase | Primary owner | Ticket or artifact filled | Gate before next phase |
| --- | --- | --- | --- |
| Shape intent | human + `brainstorm` / `advise` / `prd` | accepted direction, examples, rejected options | material choices are explicit |
| Bind work | ticket author / `spec-to-ticket` | `Summary`, `Scope`, initial `Delta`, dependencies, metadata | ticket exists and scope is coherent |
| Plan implementation | `impl-plan` | `architecture_signatures`, `Change Plan`, `Done`, `QA Strategy`, `Docs Strategy`, reviewer handoff | `qa_checklist.md` self-check and plan reviewer pass |
| Compile execution | `goal-advisor` | `program.md`, `progress.md`, native `/goal` prompt | packet approved or explicitly pre-approved |
| Execute | native Codex Goal | changed files, progress entries, command evidence | ticket `Done` and `QA Strategy` satisfied |
| Prove | `qa`, `visual-qa`, `agent-qa-test`, tests, or scripts | artifacts under `tickets/TASK-XXXX/artifacts/` | proof route matches ticket claim |
| Review | native `reviewer` lane / `review` rubrics | review receipt linked from ticket and progress | required TAS gates pass |
| Close | `close-ticket` or coordinating lane | status, links, docs/memory writeback, residual risk | no required proof or review missing |

## How The Ticket Fills Up

The ticket should stay compact but become more executable as it moves through
the loop:

- `Summary` and `Scope` start from the accepted human direction. They name what
  is in, what is out, and why the ticket is the right unit.
- `Delta` explains the before/after and first-principles basis. It should be
  readable without studying implementation details.
- `Change Plan` is filled by `impl-plan`. Material coding tickets start with
  `architecture_signatures`: module-level seams, main-flow signatures, relevant
  typed data movement, and the builder-owned freeform boundary. Per-change
  `signature_or_type_impact` only records local deltas.
- `Done` is the completion scoreboard. It names what must be true, not every
  command needed to prove it.
- `QA Strategy` names proof weight, concrete checks, delegated lanes, reviewer
  rubrics/TAS gates, evidence paths, `goal_advisor_inputs`, final evidence,
  final checkpoint, and residual risk.
- `Docs Strategy` says whether durable docs change and how that decision is
  validated.
- `Links` connect `program.md`, `progress.md`, artifacts, review receipts, and
  source refs.
- `Notes` carry blast radius, rollback, blockers, follow-ups, and compact
  citations when they clarify execution.

`program.md` starts after ticket-plan approval. It does not repeat the ticket;
it records loop shape, trigger, budget, metric or feedback provider, proof
policy, drift policy, stop conditions, and batch/heartbeat rules when relevant.
`progress.md` is append-only observed state: what changed, what was verified,
what review said, what remains blocked, and what the next action is.

## Where Autonomy Starts

Autonomous execution starts only after one of these is true:

- the work is tiny, reversible, and directly requested, so a ticket is not
  needed;
- an accepted ticket or controlling spec already owns the scope;
- an `impl-plan` ticket plan has passed its self-check and reviewer gate; or
- a Goal Packet has been approved or explicitly pre-approved for execution.

Inside a Goal Packet, the executor should try to land the whole selected ticket.
It should not shrink the ticket into a safer internal slice unless the ticket,
proof route, safety boundary, external dependency, or reviewer finding creates
a real split.

## Skill Cooperation

The ticket execution path works because each skill owns a different failure
boundary:

- `brainstorm` expands fuzzy directions and stops before pretending the idea is
  ready for tickets.
- `advise` or `deliberative-advice` chooses among real options and preserves
  the accepted tradeoff.
- `prd` or `spec-to-ticket` turns accepted product or system intent into
  ticket-sized work.
- `impl-plan` turns one selected material coding ticket into an executable
  plan, architecture signatures, QA Strategy, and reviewer handoff.
- `goal-advisor` compiles approved ticket state into a visible Goal Packet and
  compact native `/goal` prompt.
- `qa`, `visual-qa`, `agent-qa-test`, tests, scripts, and demos collect proof
  according to the ticket's `QA Strategy`.
- `review` defines TAS semantics and rubric families; the native `reviewer`
  lane supplies independent judgment and writes or returns receipts.
- `doc-advisor`, `update-memory`, and `close-ticket` handle durable writeback
  after proof exists.

`qa_checklist.md` files are self/preflight/repair guardrails. Reviewer or QA
lanes are independent readiness gates for material claims. Tiny local checks
can stay inline, but material plans, skill changes, prompts, evidence bundles,
and completion claims should not self-approve when a reviewer lane is
available.

## Hardening

Hardening target:

```text
harden_ticket_execution(ticket_lifecycle)
  -> risk_map + mitigations + adversarial_tests + proof + residual_risk
```

Trust boundaries include the human/operator conversation, ticket files, skill
contracts, native Goal execution, subagent reviewer/QA lanes, command output,
generated artifacts, and docs/memory writeback. The most realistic failure
modes are process failures rather than classic network security issues.

| Risk | Impact | Mitigation | Proof or check |
| --- | --- | --- | --- |
| Fuzzy intent becomes durable work too early | wrong ticket, wasted Goal execution | use `brainstorm`, `advise`, `prd`, or explicit acceptance before ticketed execution | ticket `Summary`/`Scope` preserve accepted and rejected options |
| Ticket is chat-only or underfilled | executor invents scope or proof route | material work writes `ticket.md` before plan-ready state | reviewer checks ticket-first and goal-advisor readiness |
| Architecture hides in prose | reviewer cannot catch wrong seams before code | `impl-plan` requires `architecture_signatures` for material plans | `impl-plan` QA checklist and plan reviewer gate |
| Planner self-approves | same model misses its own weak assumptions | `qa_checklist.md` is self-check; reviewer lane is readiness gate | review receipt linked from ticket/progress |
| Goal Packet goes stale after plan edits | executor follows old prompt | rerun `goal-advisor` when ticket plan changes | program/progress prompt timestamp and packet approval state |
| Proof only covers nearby pieces | false completion claim | `QA Strategy` names critical path and smaller ordered sanity checks | evidence-quality reviewer gate |
| Reviewer route is missing or generic | material judgment becomes vibes | caller declares rubric families, TAS gates, hard gates, and evidence | reviewer handoff or ticket QA Strategy |
| Unrelated validator failure blocks or hides real risk | noisy closeout or false confidence | name unrelated residual failures separately from task proof | progress and final response list residual risk |
| Ticket state drifts after execution | board/Pulse may re-run or skip work | update metadata, `Links`, `progress.md`, and closeout state together | ticket metadata/doc refs checks and final reviewer receipt |
| Docs/memory writeback bloats always-loaded context | prompt tax and stale policy | route detail to skill docs, tickets, validators, or lifecycle docs; keep AGENTS compact | global AGENTS QA checklist and documentation review |

Adversarial lifecycle checks:

- Can a reviewer reconstruct the intended change from `ticket.md` without chat?
- Can a Goal executor run from `ticket.md`, `program.md`, and `progress.md`
  without transcript memory?
- Does `QA Strategy` prove the user-facing or system claim, not only adjacent
  files?
- Are all material readiness claims backed by independent reviewer/QA evidence
  or an explicit residual-risk note?
- If validation fails, is the failure linked to this ticket or isolated as
  unrelated residual risk?

Residual risk:

```text
accepted:
  - This lifecycle is enforced by prompts, tickets, reviewers, and validators,
    not by one central runtime. Agents can still bypass it during casual direct
    edits unless the operator or Goal Packet invokes the process.
deferred:
  - Lifecycle graph projections are not automatically updated by this doc.
  - Budget Advisor still has older `review_depth` language; migrate separately
    if review routing needs a cleaner model.
owner:
  - ticket execution loop: farplane-framework
  - ticket execution contract: tickets/README.md, impl-plan, goal-advisor,
    review, AGENTS
trigger_to_revisit:
  - a material ticket completes without reviewer receipt
  - a Goal runs from a stale prompt after ticket-plan edits
  - Pulse or interval automation chooses work from stale ticket state
```
