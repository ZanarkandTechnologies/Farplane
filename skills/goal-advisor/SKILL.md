---
name: goal-advisor
description: "Use for \"set up a goal\", \"keep improving this until\", \"run this unattended\" or \"optimize with my feedback\": Goal Packet architecture, loop state, and a native /goal prompt when warranted."
department: leadership
source: local
version: 0.3.0
template_uses:
  skill-template: "0.6.6"
  skill-eval-task: "0.2.0"
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Goal Advisor

## Context

Goal Advisor is Farplane's execution compiler. Use it once an intent or GitHub
issue is selected enough to become a native Goal, heartbeat, rollout, feedback
loop, or direct-route decision. Tiny one-turn work stays direct. Native Goal is
the only continuation engine; Farplane keeps its state on the project's own
GitHub issue (`tickets/README.md`, Current GitHub Issues workflow):

```text
GoalPacket := issue body (ticket sections + ## Goal program + ## Current Goal state)
            + Goal turn comments + Goal launcher comment
            + .farplane/goal-advisor/issue-<n>/hypothesis-tree.json? + listed repo files?
```

- Ticket sections: valuable outcome, scope, Done, QA/proof, blockers, links.
- `## Goal program` (after the ticket sections): trigger, metric/provider,
  budget, decision loop, drift, stops, and every decision that still binds.
- `## Current Goal state` (last section): the latest checkpoint, rewritten each turn.
- Goal turn comments (`**Goal turn N**`, heartbeats included): append-only
  history; a `Decision:` comment records why a binding rule changed.
- `**Goal launcher**` comment: the compiled `/goal` prompt. It is the run's
  prompt, so first load skips it.
- `hypothesis-tree.json`: local experiment state, never pasted into the public
  issue; each turn comment names the selected node and result so it can be rebuilt.
- Goal Advisor compiles the packet and launcher, never each turn; the metric
  card is setup/repair only; the domain skill executes.

A project with no GitHub repository keeps the legacy files (`tickets/README.md`);
nothing else falls back to files.

## Skill Signature

```text
advise_goal_use(intent, issue?, files?, trigger?, budget?, proof_policy?, approval_policy?)
  -> goal_architecture + goal_packet? + native_goal_prompt? + next_action
reads: operator intent, issue body and latest Goal turn comments, named repo files
does: compiles one Goal program and launcher over the issue, or routes direct
writes: ## Goal program, ## Current Goal state, launcher comment, local tree, or direct-route note
returns: Goal Architecture, compilation verdict, launcher or withheld launcher
routes: impl-plan | notify | qa | review | direct-answer
gates: material_goal_has_issue; loop_owner_single; metric_provider_named;
  budget_and_stops_named; drift_and_logging_named; proof_route_named;
  first_load_within_400; packet_fresh; material_packet_approved
fails: hidden_loop; prompt_only_material_goal; full_history_first_load;
  duplicated_ticket_policy; local_packet_beside_issue; self_certified_material_proof;
  stale_packet; advisor_chain_owns_next_turn; invented_baseline_or_threshold; invented_budget
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Bind the issue, authority, and whether a Goal is warranted.**
  `intent + issue -> active_goal | heartbeat | direct | blocked(missing bindings)`

  Rule: Material Goal work requires one GitHub issue (`owner/repo#n`) and an
  inline literal `Files:` list whose first entry is that issue. Ask at most
  three questions, only for scope, metric, budget, proof, approval, spend,
  deploy, or safety. Never invent a baseline, threshold, budget, attempt count,
  or outcome; keep placeholders and name the missing binding. The repository is
  public: engineering facts only in the body and comments.

  Assert:
  - A blocked architecture still returns the Files list and launcher skeleton.
  - `hypothesis-tree.json` appears only for skill improvement, ML autoresearch,
    or another experiment-backed loop, and its frontier is never duplicated.
- [ ] **N2 — Classify one trigger shape.**
  `bound intent -> active_goal | heartbeat | feedback | rollout | batch | project_goals`

  Rule: `heartbeat` is delayed inspection over the same issue, not a second
  runtime (`references/goal-shapes.md`). Load `references/human-feedback.md`
  when the honest provider is Kenji's judgment.

  Assert: only the selected branch reference is loaded.
- [ ] **N3 — Compile the minimal `## Goal program`.**
  `issue ticket sections -> Goal program | revise`

  Rule: Bind objective, mutable surface, metric/provider, guards, anti-metrics,
  budget, proof route, drift policy, and stops without copying the ticket.
  Compile `Contract Diagram -> Change Plan -> exit assertions -> proof` into the
  Execution Path; reject missing, contradictory, or circular bindings. An
  underspecified "clearly better" goal with no market baseline defaults to a
  `hybrid` frozen-scenario eval plus explicit human/reviewer judgment, with the
  rubric and threshold left unresolved. Compile delayed `accept | kill |
  monitor` only for matured Reward work. Diagnose blocking failures with
  `code-health` debug.

  Example: a screenshot complaint becomes one Completion Closure row `source
  image + exact complaint | design state/viewport | repair proof | newer capture
  | independent verdict | pending|supported|operator_withdrawn`.

  Assert:
  - The Reference Manifest names the consumer of every listed file; no orphans.
  - Every Done assertion has a Completion Closure row with proof and evidence
    owner; unsupported rows keep the packet `revise` or `blocked`.
  - The visible receipt echoes the Execution Path, failure branch, consumed-only
    manifest, and one `Done assertion -> change -> evidence -> supported |
    pending` row each, ending `stop_complete: withheld until every closure row
    is supported`.
- [ ] **N4 — Enforce the first-load budget and writeback.**
  `Goal program -> context gate + logging + drift policy`

  Rule: Initial context is the output of the first-load command in
  `prompt-templates.md`: the issue body plus the newest whole Goal turn comments
  within 80 lines (always the newest). Its line count is the gate: target 300, hard 400, above
  that `revise`. Load other comments or artifacts only for a named evidence gap;
  consolidate or move bulky evidence, never weakening scope, safety, proof, or
  reconstruction. After each turn update the tree first when present, post one
  Goal turn comment (observation, evidence, learning, decision, remaining
  budget, next action), then replace only `## Current Goal state`, leaving the
  body above it byte-identical.

  Assert: drift is inline for small Goals and `goal-drift-reviewer` for
  material, long-running, strategic, rollout, or self-approval-prone work.
- [ ] **N5 — Compile proof and completion.**
  `ticket Done + QA Strategy -> proof route + completion sequence`

  Rule: Ticket Done and QA Strategy win over program or launcher prose. Name
  `qa-tester`, `qa` (visual, adversarial, closeout), `reviewer`, or human
  feedback when required; self-certification is not proof. Material
  implementation order: sanity checks -> QA evidence review -> narrated
  lead-engineer demo MP4 -> response draft -> completion review with
  `approved_response` -> one proof comment that checks every Done item with its
  evidence -> `gh issue close <n> --reason completed` -> `stop_complete`.

  Assert: feature work cites current official or maintained grounding unless
  local-only; UI work carries its best screenshot evidence.
- [ ] **N6 — Emit the launcher from `references/prompt-templates.md`.**
  `Goal program -> **Goal launcher** comment`

  Rule: Keep literal `Files`, `Task`, `Logging`, `Metric`, and `After each turn`
  sections and point to the issue instead of restating it. Preserve literally
  `choose_next(objective, evidence, eligible_moves, remaining_budget) -> execute
  | diagnose | report_now | request_feedback | stop`; never paraphrase it as
  "compare options".

  Assert:
  - A material launcher states the 300/400 gate and the 80-line comment tail,
    evaluates with the provider before writeback, names `goal-drift-reviewer`
    and when it runs, and gives receipt fields `observation`, `evidence`,
    `learning`, `decision`, `remaining_budget`, and `next_action`.
- [ ] **N7 — Finish-check freshness, approval, and QA.**
  `packet -> ready | revise | blocked`

  Rule: Record `compiled_from_ticket_sha` (`prompt-templates.md`); the executor
  and drift reviewer recompute it, and a mismatch returns here. Regenerate after
  ticket, suite, evaluator, scope, or proof-policy drift. Material packets stay
  `approval: pending` until the operator approves the ticket sections, Goal
  program, tree, and launcher together. Route material packet review to the reviewer with
  `goal-program-contract` plus prompt/evidence families; accept nothing below
  the required TAS gate.

  Assert: when not `ready`, list failed bindings, report Completion Closure
  unsupported, and state that the launcher and `stop_complete` are withheld.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- `## Goal program` is loop policy, not a second ticket. A local `program.md`/`progress.md` beside a GitHub issue is a second
  writable task: fold it into the issue.
- A listed file is context or evidence unless the ticket grants scope. Honest
  review/human/market signals beat fake numeric metrics.
- Do not route new work through retired `$work`, `$ralph`, or `batch-work`.
- A Stop hook does not repair proof, review, closeout, or packet drift.

## Reference Map

- [Prompt templates](references/prompt-templates.md) — launcher, setup, verdict
  block, and Goal turn receipt.
- [Goal shapes](references/goal-shapes.md) — heartbeat, batch, rollout, project goals.
- [Goal algebra](references/goal-algebra.md) — composed workflows, retired routes;
  [choose next](references/choose-next.md) — several eligible moves.
- [Human feedback](references/human-feedback.md), [metric card](references/metrics.md),
  [loop presets](references/loop-presets.md) — provider, metric, rollout or ML.
- [Golden material packet](examples/golden/material-goal-packet.md) — with QA for
  judgment-heavy planning; [feature](../../docs/features/FEAT-0032-goal-advisor-execution-compilation.md).
- [Goal program](../../tickets/templates/goal-loop/program.md) and
  [state and turn comment](../../tickets/templates/goal-loop/progress.md) templates.

## Output

A direct-route note, a Goal Architecture (`prompt-templates.md`), or the updated
issue sections plus the launcher comment. Material completion output names
`Ticket`, `Execution Path`, `Reference Manifest`, `Completion Closure`,
`Verification`, `Artifacts`, `Grounding`, and `Residual risk`, showing every
closure row; only `supported` or a recorded `operator_withdrawn` releases a
screenshot row.
