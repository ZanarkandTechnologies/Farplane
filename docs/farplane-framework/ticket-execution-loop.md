---
title: "Ticket Execution Loop"
status: active
owner: farplane-framework
created_at: 2026-06-29
updated_at: 2026-07-27
framework_template_version: "0.2.1"
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
  - docs/features/FEAT-0032-goal-advisor-execution-compilation.md
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

## Goal Packet Ownership

Keep each concern in one durable owner:

```text
ticket.md   = desired end state + scope + constraints + Done / Proof
skill       = domain procedure + detailed evaluation logic
program.md  = budget + continuation + drift + stopping + optional optimization roadmap
progress.md = observations + evidence links + learned constraints + next action
Goal prompt = compact pointer to the packet
```

The common continuation cycle is:

```text
read state
  -> choose one bounded move
  -> act
  -> evaluate with the provider declared by the ticket or skill
  -> append the observation, evidence, learning, and next action
  -> drift-check when required
  -> continue | complete | block
```

Evaluation is therefore a distinct step, not another name for choosing what to
do next. The ticket or domain skill owns what counts as evidence and how to
interpret it. `program.md` only binds that evaluator into the continuation
loop. For optimization Goals, promising candidates remain in the program's
roadmap or frontier until evidence rejects or invalidates them. `progress.md`
records the selected move, rejected alternatives when relevant, learned
constraints, evidence links, and the current `next_action`; selecting one move
does not silently discard the remaining candidates.

### Lean `program.md`

A lean `program.md` fills the existing template sections without repeating the
ticket. Its after-turn and stopping instructions can be as compact as this:

```markdown
## After Each Turn

- Re-read the ticket and progress tail.
- Choose the largest unresolved acceptance, evidence, or blocker gap. For an
  optimization loop, select from the program roadmap or frontier using current
  progress learnings.
- Execute one bounded move, run the evaluator declared by the ticket or active
  skill, and append the observation, evidence, learning, and next action.
- Use `goal-drift-reviewer` before a material replan or completion.

## Stop Conditions

- `blocked_when:` Report attempted paths, strongest evidence, remaining work, and
  the exact input or contract change that would unlock progress.
```

This excerpt belongs in `program.md`, not `ticket.md`. Still fill the
template's required Goal Mode, budget, Metric Provider, Proof Policy, drift,
check-in, batch, or rollout sections when applicable.

The launcher stays small because it is not the durable contract:

```text
/goal Work on TASK-1243 until its Done and QA Strategy pass or the declared
budget ends. Read ticket.md, program.md, and progress.md. Follow program.md
between iterations. Do not expand ticket scope. If blocked, return attempted
paths, evidence, and the required unlock.
```

`best_so_far` is useful only for optimization campaigns whose candidates can
be compared. Ordinary feature work instead records completed proof and the
remaining `next_action`.

### Evaluation By Goal Shape

The shared cycle stays constant while the evaluation provider changes.
`ml_autoresearch` is an allowed Goal Mode instantiated through its skill-owned
preset, while `delayed_reward` belongs under Check-In Program rather than the
top-level mode field.

| Shape or program submode | Evaluation after a move | What feeds the next action |
| --- | --- | --- |
| Active ticket Goal | ticket `Done / Proof`, tests, QA evidence, and required review | unresolved in-scope ticket gaps |
| Skill improvement | frozen skill eval plus agent-behavior QA when declared | ranked prompt, workflow, or harness interventions |
| ML autoresearch | frozen metric evaluator; diagnose surprising or invalid results before trusting them | ranked experiment techniques and learned constraints |
| Feedback loop | structured human verdict and next instruction | remaining revisions implied by accepted feedback |
| Heartbeat | eligibility and current-state check; choose `start_goal`, `resume_goal`, `request_feedback`, `replan`, `blocked`, or `no_op` | the next proceedable ticket or unblock action |
| Delayed-reward check-in | matured external evidence against the declared acceptance rule | `accept`, `kill`, or continue monitoring |
| Batch Goal | each ticket's own proof contract, plus integration proof when required | remaining proceedable tickets |
| Rollout policy | sample or batch evidence against promotion and rollback rules | promote, repair, roll back, or run the next batch |

Detailed experiment receipts, surprise handling, feedback schemas, and rollout
rules remain in their owning skill or ticket. The generic program should
reference them rather than copy them into every Goal Packet.

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

## Ticket Thread Association

Ticket-level autonomy metrics need to know which Codex thread owned a ticket
after execution started. Raw thread or session IDs are runtime state, not ticket
frontmatter. Store them under the ignored runtime state path:

```text
.farplane/state/ticket-thread-associations.jsonl
```

Each row should be a compact JSON object:

```json
{"ticket_id":"TASK-0000","thread_id":"019f...","execution_started_at":"2026-07-01T10:00:00Z"}
```

`session_id` may be used instead of `thread_id` when that is the available
runtime identifier. The reducer counts user turns after
`execution_started_at` and before the ticket completion time. Missing,
ambiguous, or polluted association data must become a metric source gap rather
than a guessed intervention count. Keep stable human-facing ownership in ticket
frontmatter fields such as `claimed_by`; keep raw transport identifiers in
`.farplane/state/`.

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

`qa_checklist.md` files are self/preflight/repair guardrails and reviewer
ammunition, not acceptance forms. The typed `reviewer` lane owns checklist
judgment and harsh pass/revise/block decisions. The typed `qa-tester` lane owns
runtime, browser, UI, and proof capture. Tiny local checks can stay inline, but
material plans, skill changes, prompts, evidence bundles, and completion claims
should not self-approve when a reviewer lane is available.

When material completion needs both proof and judgment, spawn `qa-tester` and
`reviewer` in parallel when possible:

```text
material_completion(ticket)
  -> qa-tester(ticket, proof_targets) -> evidence_bundle
  -> reviewer(ticket, checklist?, evidence_bundle?, rubrics) -> TAS verdict
  -> coordinator reconciles both receipts before pass/revise/block
  -> farplane ticket close TASK-XXXX on pass
```

Do not use generic subagents for these roles when typed agents are available.

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
