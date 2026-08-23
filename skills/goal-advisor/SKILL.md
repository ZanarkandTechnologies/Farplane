---
name: goal-advisor
description: "Turn an ambitious request into Goal architecture, ticket-backed loop state, and a native Codex /goal prompt when warranted."
tier: 3
group: operations
source: local
version: 0.2.0
template_uses:
  skill-template: "0.2.0"
  skill-eval-task: "0.2.0"
  skill-qa-checklist: "0.1.0"
eval: evals/evals.json
qa_checklist: qa_checklist.md
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Goal Advisor

## Context

Goal Advisor is Farplane's execution compiler. Use it after an intent or ticket
is selected enough to become a native Goal, heartbeat, rollout, feedback loop,
or direct-route decision. Tiny one-turn work stays direct.

Native Goal is the only continuation engine. Farplane keeps its state visible:

```text
GoalPacket := ticket.md + program.md + progress.md + generated_goal_prompt
            + hypothesis-tree.json? + listed context/evidence files?
```

Ownership is strict:

- `ticket.md`: valuable outcome, scope, Done, QA/proof, blockers, links.
- `program.md`: trigger, metric/provider, budget, decision loop, drift, stops.
- `hypothesis-tree.json`: current experiment state, only when experimental.
- `progress.md`: append-only observations, evidence, decisions, next action.
- Goal Advisor: compile/regenerate packet and launcher; never choose each turn.

Every program uses one runtime backbone:

```text
observe -> choose_next(execute | diagnose | report_now | request_feedback | stop)
        -> act -> verify -> write_back
```

Metric Advisor is setup/repair only. Leverage Advisor is conditional on several
plausible moves needing judgment. Plan Next Wave refills an empty board and
never participates inside an active Goal. The domain skill executes.

## Skill Signature

```text
advise_goal_use(intent, files?, trigger?, budget?, proof_policy?, approval_policy?)
  -> goal_architecture + goal_packet? + native_goal_prompt? + next_action
state:
  reads(operator intent, ticket/program/tree/progress, named context and proof);
  writes(ticket/program/tree?/progress?, generated prompt, or direct-route note)
gates:
  material_goal_has_files; loop_owner_single; metric_provider_named;
  budget_and_stops_named; drift_and_logging_named; proof_route_named;
  packet_context_budget_pass; material_packet_approved
routes:
  metric-advisor | impl-plan | optimize-with-human | qa | visual-qa |
  agent-qa-test | review | direct-answer
fails:
  hidden_loop; prompt_only_material_goal; full_progress_first_load;
  duplicated_ticket_policy; self_certified_material_proof; stale_packet;
  plan_next_wave_inside_active_goal; advisor_chain_owns_next_turn;
  invented_baseline_or_threshold; invented_budget
```

## Phase Boundary

Goal Advisor chooses the architecture and may create the packet and launcher.
It does not launch hidden schedulers or execute the domain work. When called
from `impl-plan`, compile the preview with `approval: pending`; regenerate it
whenever the ticket changes. For branch detail load only the relevant reference:

- prompt emission -> `references/prompt-templates.md`
- heartbeat, batch, rollout, project goals -> `references/goal-shapes.md`
- composed workflows or retired-route migration -> `references/goal-algebra.md`
- delayed reward -> the program template's `Check-In Program`
- prompt-heavy/judgment-heavy packet -> golden example plus `qa_checklist.md`

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind intent, files, authority, and whether Goal is warranted.
  - [ ] Keep tiny work direct. Material Goal work requires `ticket.md`,
    `program.md`, `progress.md`, and an inline literal `Files:` list.
  - [ ] Ask at most three questions only for missing inputs that materially
    affect scope, metric, budget, proof, approval, spend, deploy, or safety.
  - [ ] Never invent a baseline, threshold, budget, attempt count, or example
    outcome. Preserve placeholders and name exact missing bindings. Even a
    blocked architecture still returns the literal Files list and compact
    launcher skeleton so the approval surface is complete.
  - [ ] Add `hypothesis-tree.json` only for skill improvement, ML autoresearch,
    or another truly experiment-backed loop; never duplicate its derived state.
- [ ] 2. Classify one trigger shape.
  - [ ] `active_goal`: uninterrupted bounded execution window.
  - [ ] `heartbeat`: delayed inspection over the same packet; it is not a
    second runtime. Load `references/goal-shapes.md` for its action vocabulary.
  - [ ] `feedback`, `rollout`, `batch`, or `project_goals`: load only the
    selected branch. Use `optimize-with-human` for skill optimization whose
    honest provider is human feedback.
- [ ] 3. Compile the minimal program.
  - [ ] Bind objective, mutable surface, metric/provider, guards, anti-metrics,
    budget, proof route, drift policy, and stop conditions without copying the
    ticket or tree.
  - [ ] Use Metric Advisor only when the measurement contract is unclear.
  - [ ] Select the honest provider class even when its threshold is still
    pending. For an underspecified “clearly better” workflow with no reliable
    market baseline, default to `hybrid` frozen-scenario eval plus explicit
    human/reviewer judgment; keep the rubric and threshold unresolved rather
    than leaving the provider itself unchosen or inventing numbers.
  - [ ] Compile delayed `accept | kill | monitor` procedure only for matured
     Reward work; immediate Goals mark it not applicable.
  - [ ] Compile `Contract Diagram -> Change Plan -> exit assertions -> proof`
    into the program's Execution Path. Reject missing, contradictory, or
    circular bindings instead of asking the executor to infer them.
  - [ ] Emit a Reference Manifest where every listed file names the node,
    assertion, proof, or drift decision that consumes it; remove orphan refs.
  - [ ] Emit Completion Closure mapping every ticket Done assertion to an
    executable proof method and evidence owner. Unsupported rows keep the
    packet in `revise` or `blocked`.
  - [ ] Convert and echo every operator complaint tied to a screenshot as one
    Completion Closure row: `source image + exact complaint | design
    state/viewport | repair proof | newer comparable capture | independent
    verdict | pending|supported|operator_withdrawn`. Write it to `program.md`
    or `progress.md`. Stale, wrong-state, partial, or unrelated evidence keeps
    `stop_complete` withheld.
  - [ ] Echo the semantic bindings in the visible compilation receipt before
    returning `ready`: ordered `Execution Path`, failure branch, consumed-only
    `Reference Manifest`, and one `Done assertion -> owning change -> evidence
    source -> supported | pending` row per Completion Closure item. End with
    `stop_complete: withheld until every closure row is supported`.
  - [ ] Use the shared Decision Backbone. Invoke Leverage Advisor only when
    several plausible moves need judgment; otherwise act directly.
- [ ] 4. Enforce the first-load budget.
  - [ ] Initial context is full `ticket.md`, full `program.md`, and at most the
    latest 80 lines of `progress.md`. Load older receipts or artifacts only for
    a named evidence gap.
  - [ ] Target at most 300 lines and require `ticket.context-budget` to block
    above 400. Consolidate duplication or move bulky evidence; never weaken
    scope, safety, proof, or reconstruction behavior to hit the cap.
- [ ] 5. Compile state, logging, and drift.
  - [ ] `Files:` names every required ticket/program/tree/progress/spec/design/
    board/artifact file. Project harness/metrics files appear only when needed
    and every non-core file has a Reference Manifest consumer.
  - [ ] After each turn append observation, evidence, learning, decision,
    remaining budget, and next action; update the tree before the receipt.
  - [ ] Use inline drift for small Goals and `goal-drift-reviewer` for material,
    long-running, strategic, rollout, or self-approval-prone work.
- [ ] 6. Compile proof and completion.
  - [ ] Ticket Done and QA Strategy win over program or launcher prose.
  - [ ] Name `qa-tester`, `visual-qa`, `agent-qa-test`, `reviewer`, `demo`, or
    human feedback when required; self-certification is not proof.
  - [ ] Material implementation invariant: ordered sanity checks -> QA evidence
    review -> narrated lead-engineer demo MP4 -> ticket-scoped response draft ->
    completion review with `approved_response` -> ticket writeback ->
    `farplane ticket finalize TASK-XXXX` -> `stop_complete`.
  - [ ] Require current official/maintained implementation grounding for feature
    work unless explicitly local-only, and best screenshot evidence for UI work.
- [ ] 7. Emit the launcher only after loading `references/prompt-templates.md`.
  - [ ] Keep literal sections `Files`, `Task`, `Logging`, `Metric`, and `After
    each turn`; point to files instead of restating them.
  - [ ] Make `choose_next`, outside options, provider evaluation, writeback,
    budget, drift, blockers, and final proof explicit.
  - [ ] A material architecture is invalid unless it literally states the
    300/400 context gate and 80-line progress tail, evaluates with the provider
    before writeback, compares `execute | diagnose | report_now |
    request_feedback | stop`, names `goal-drift-reviewer` plus when it runs,
    and gives the receipt fields `observation`, `evidence`, `learning`,
    `decision`, `remaining_budget`, and `next_action`.
  - [ ] Do not paraphrase the selector as “compare options.” The launcher must
    literally preserve `choose_next(objective, evidence, eligible_moves,
    remaining_budget) -> execute | diagnose | report_now | request_feedback |
    stop` so the owner and vocabulary survive compilation.
- [ ] 8. Finish-check packet freshness, approval, and QA.
  - [ ] Record the ticket `updated_at` compiled into the packet. Regenerate
    after ticket, suite, evaluator, scope, or proof-policy drift.
  - [ ] Material packets remain pending until the operator approves ticket,
    program, tree when present, progress scaffold, and launcher together.
  - [ ] Apply `qa_checklist.md`; route material prompt/packet review to the
    reviewer using `goal-program-contract` plus prompt/evidence families, and
    do not accept below the required TAS gate.
  - [ ] Return an explicit compilation verdict: `ready`, `revise`, or `blocked`.
    When not ready, list the failed bindings, report Completion Closure as
    unsupported, and state that the launcher and `stop_complete` are withheld.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Goal packet compilation:

```text
ticket_to_goal_packet(ticket.md)
  intent_and_boundaries <- Summary + Scope + Delta
  execution_units <- Change Plan
  completion_scoreboard <- Done
  proof_policy <- QA Strategy
  current_state <- State + latest 80 progress lines
  context_and_evidence <- Links + only branch-required files
  execution_path <- Contract Diagram + Change Plan + assertions
  completion_closure <- Done + QA Strategy + evidence owners
```

Compiled launcher shape:

```text
/goal Run the listed files as one Goal Packet.
Files: <literal paths>
Task: <ticket scope and Done>
Logging: <tree-first when present; compact progress receipt>
Metric: <program provider and guards>
After each turn: observe -> choose_next(objective, evidence, eligible_moves,
remaining_budget) -> execute | diagnose | report_now | request_feedback | stop
-> act -> verify -> write_back
Context gate: ticket + program + latest 80 progress lines; target 300, hard 400
Drift reviewer: goal-drift-reviewer at <checkpoint>
Approval: <pending | approved | revise | blocked>
```

Compilation result shape:

```text
Verdict: ready | revise | blocked
Failed bindings: <diagram/order | stale reference | orphan reference | proof closure>
Completion Closure: supported | unsupported
Launcher: emitted | withheld
stop_complete: allowed | withheld
```

The compact progress receipt is:

```yaml
observation:
evidence: []
learning:
decision: execute | diagnose | report_now | request_feedback | stop | blocked
remaining_budget:
next_action:
```

Material completion output:

```text
Ticket:
Execution Path: <ordered diagram IDs -> owning changes>
Reference Manifest: <only consumed references -> named consumers>
Completion Closure: <Done assertion -> change -> evidence -> status>
Verification:
Artifacts:
Grounding:
Residual risk:
```

Do not hide semantic compilation inside artifact links. The receipt must expose
the ordered path, failure branches, consumed references, and every closure row;
state that `stop_complete` remains withheld unless all rows are supported.

## Gotchas

- `program.md` is executable loop policy, not a second ticket or optional note.
- `progress.md` is evidence memory, not a transcript; initial load uses its tail.
- A listed file is context or evidence unless the ticket grants executable scope.
- Heartbeat is a trigger over the same packet, never hidden autonomy.
- Honest review/human/market signals beat fake numeric metrics.
- Do not route new work through retired `$work`, `$ralph`, or `batch-work`.
- A Stop hook does not repair proof, review, closeout, or packet drift.

## Reference Map

- [Goal Packet feature](../../docs/features/FEAT-0032-goal-advisor-execution-compilation.md)
- [Prompt templates](references/prompt-templates.md) — load for launcher text.
- [Goal shapes](references/goal-shapes.md) — load for non-default triggers.
- [Goal algebra](references/goal-algebra.md) — load for composed workflows.
- [Golden material packet](examples/golden/material-goal-packet.md) — load with
  QA for prompt-heavy/judgment-heavy planning and independent review.
- [Program template](../../tickets/templates/goal-loop/program.md)
- [Progress template](../../tickets/templates/goal-loop/progress.md)
- [Metric Advisor](../metric-advisor/SKILL.md)
- [Optimize With Human](../optimize-with-human/SKILL.md)

## Output

Return or write one of:

- direct-route recommendation for one-turn work;
- Goal Architecture with Ticket, Program, Progress, Files, Trigger, Budget,
  Metric/Provider, Drift, Decision Backbone, Proof, Approval, and Next Action;
- created/updated packet paths plus the compact native `/goal` or heartbeat
  launcher.

For every screenshot complaint, show and write a Completion Closure row:

```text
source image | exact complaint | design state + viewport | newer comparable capture |
independent verdict | supported | pending | operator_withdrawn
```

Only `supported` or an explicit, recorded `operator_withdrawn` can release
that row. Never summarize the row away in a completion answer.
