---
name: goal-advisor
description: "Turn an ambitious request into Goal architecture, ticket-backed loop state, and a native Codex /goal prompt when warranted."
tier: 3
group: harness
source: local
version: 0.2.0
skill_template_version: "0.2.0"
feature_refs:
  - FEAT-0029
  - FEAT-0046
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Goal Advisor

## Context

`goal-advisor` is the canonical execution compiler for durable Farplane work.
Use it when the operator wants to turn an intent, ticket, board, batch, rollout,
portfolio, skill-improvement loop, or feedback loop into a native Goal,
heartbeat, or direct-route recommendation.

Native Goal mode is the only formal continuation loop. Farplane adds visible
state around it through a Goal Packet:

```text
GoalPacket := files[] + ticket.md + program.md + progress.md + generated_goal_prompt + drift_check_contract
GoalFiles := [ticket.md | program.md | progress.md | spec.md | board.md | artifact]
```

Generated prompts must name source files inline under `Files:`. Do not expose a
new abstraction such as `refs[]` to the operator.

`ticket.md` owns the task contract and proof. `program.md` owns loop config,
metric, budget, heartbeat, drift, and stop policy. `progress.md` owns compact
append-only observations. `portfolio.md` is optional parent state for
long-horizon graphs; it is not required for normal multi-file Goals.

This skill owns both architecture choice and final native `/goal` or heartbeat
prompt compilation. Keep templates with this skill, but load full template
references only after the branch requires prompt emission.

`$work`, `$ralph`, and `batch-work` are retired public orchestration surfaces.
Their useful policies live here as admission/profile, heartbeat board-drain,
batch proof rows, compute/budget, and blocker handling. `$impl` remains the
coding-ticket leaf executor when the selected file set is build-ready.

## Skill Signature

```text
advise_goal_use(intent, files?, trigger?, budget?) -> goal_architecture + files[] + goal_packet? + heartbeat_prompt? + native_goal_prompt? + next_action
state: reads(operator intent, listed files, tickets, board files?, portfolio.md?, program.md?, progress.md?, goal-loop contract, relevant skills/docs); writes(ticket/program/progress? portfolio? generated goal prompt? or recommendation)
gates: material_goal_has_files; loop_owner_single; progress_surface_named; metric_provider_named; budget_named; drift_policy_named; logging_policy_named
routes: optimize-with-human | impl | review | direct-answer
fails: creates hidden loop runtime; uses Goal without durable state; treats human feedback/heartbeat/rollout as competing loop owners; emits prompt-only material Goal; hides required files behind transcript memory; routes public work through retired work/ralph/batch-work surfaces
```

## Phase Contract

```text
goal_advice_phase(intent, state)
  -> task_shape
   + files[]
   + trigger_mode
   + budget
   + state_surfaces
   + metric_provider
   + drift_policy
   + native_goal_prompt?
   + next_owner
```

## Phase Boundary

This skill may route to `optimize-with-human`, `$impl`, or `review` only after
it chooses the Goal architecture. It does not run the Goal loop itself, launch
hidden schedulers, or preserve retired public orchestration skills as peers.

## Progressive Load Rule

Use this placement test before loading or adding detail:

```text
place_goal_advisor_detail(detail)
  -> SKILL.md when defer_loading_risk > context_rot_risk + compaction_loss_risk
  -> reference when defer_loading_risk <= context_rot_risk + compaction_loss_risk
```

Keep first load limited to rules that affect the next decision. Load references
only after the branch is selected:

- prompt emission -> `references/prompt-templates.md`
- loop-shape nuance, batch, board drain, rollout, or portfolio boundary ->
  `references/goal-shapes.md`
- workflow-skill composition or retired-surface migration detail ->
  `references/goal-algebra.md`
- portfolio design depth -> `references/goal-portfolio.md`
- worked examples -> `examples/`

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the intent and decide whether this is material enough for Goal.
   - [ ] If the task is tiny or one-turn, recommend direct work instead of Goal.
   - [ ] If native Goal or heartbeat is warranted, require listed source files
     or a create/update step for `ticket.md`, `program.md`, and `progress.md`.
- [ ] 2. Classify the loop shape.
   - [ ] `active_goal`: uninterrupted execution window with no planned pause.
   - [ ] `heartbeat`: continuation when pauses, board drain, feedback, external
     state, or cadence matter.
   - [ ] `feedback_loop`: needs human or reviewer feedback before continuing.
   - [ ] `skill_improvement`: improves a target skill using evals, review, or
     feedback.
   - [ ] `rollout`: applies a proven pattern across a target set.
   - [ ] `batch_goal`: executes a listed file set inside one time/budget window
     while preserving per-ticket proof.
   - [ ] `business_loop` or `goal_portfolio`: coordinates recurring or
     long-horizon work through parent heartbeat/manual resume and leaf Goals.
   - [ ] Load `references/goal-shapes.md` when the chosen shape needs more than
     the one-line classifier above.
- [ ] 3. Choose the state surfaces.
   - [ ] `Files:` in the generated prompt names every ticket, program,
     progress, board, spec, or artifact file the Goal must read.
   - [ ] Use `portfolio.md` only when a longer planning graph is needed beyond
     the listed files.
- [ ] 4. Choose the time/budget policy.
   - [ ] Treat the unit as a time/budget window, not ticket size.
   - [ ] Name time, token/model/compute, subagent, review, QA, feedback, and
     spend limits when they matter; write `none` or `not specified` otherwise.
   - [ ] Use heartbeat when the next useful action depends on elapsed time,
     feedback arrival, an external event, or a periodic board-drain check.
- [ ] 5. Choose the metric or feedback provider.
   - [ ] `mechanical`: command, script, eval, benchmark, or artifact check.
   - [ ] `review`: TAS verdict from review.
   - [ ] `agent_qa`: adversarial QA evidence.
   - [ ] `human_feedback`: human score, qualitative feedback, or approval.
   - [ ] `market`: external result such as clicks, replies, sales, or retention.
   - [ ] `hybrid`: combine signals without inventing fake numbers.
- [ ] 6. Define batch, board-drain, or leaf execution policy when relevant.
   - [ ] For multi-ticket file lists, preserve one proof row per ticket plus
     any batch/integration proof.
   - [ ] For board drain, compile a heartbeat prompt that fetches proceedable
     tickets, skips blocked/gated work, and logs no-op when nothing can advance.
   - [ ] For coding leaves, route execution through `$impl` only after the Goal
     architecture and file list are set.
   - [ ] Load `references/goal-shapes.md` for batch, board-drain, rollout, or
     portfolio details.
- [ ] 7. Define drift policy.
   - [ ] Use inline drift checks for small normal goals.
   - [ ] Use `goal-drift-reviewer` for material, long-running, strategic,
     rollout, or self-approval-prone loops.
   - [ ] Drift review is read-only and compares the listed files plus recent
     progress; it does not plan or implement.
- [ ] 8. Craft the native `/goal` or heartbeat prompt when Goal mode is warranted.
   - [ ] Load `references/prompt-templates.md` before emitting prompt text.
   - [ ] Include an inline `Files:` list before `Task`, `Logging`, `Metric`, and
     `After each turn`.
   - [ ] Bind the prompt to the listed files, honest metric provider, logging
     files, drift policy, budget, and completion/blocked policy.
   - [ ] Ask only missing execution-safety questions that materially affect the
     Goal contract; cap questions at 3.
   - [ ] Reject proxy-only completion evidence unless it satisfies the actual
     objective.
- [ ] 9. Decide the next owner.
   - [ ] Use `optimize-with-human` when the metric provider is `human_feedback`
     and the loop needs a Telegram-first feedback protocol.
   - [ ] Use `$impl` when a coding-ticket file set is ready for leaf execution.
   - [ ] Use direct ticket creation/update when the missing surface is state.
- [ ] 10. Return a Goal Architecture note, create Goal Packet scaffolding, or
   output the final native `/goal` prompt.
   - [ ] Include before/after behavior when this changes how a loop will run.
   - [ ] Name open risks, blocked decisions, and proof path.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Goal Contract

A strong Goal contract includes:

- `Files`: inline list of every source file the Goal must read
- `Task`: what must be true, from `ticket.md`
- `Logging`: how to update `progress.md`
- `Metric`: how progress is judged, from `program.md`
- `After each turn`: how to drift-check, continue, wait, complete, or block
- `Budget`: optional time/token/model/compute/subagent/review/QA/spend limit

## Output

Return either:

```text
Goal Architecture:
Portfolio:
Ticket:
Program:
Progress:
Files:
Trigger:
Budget:
Metric / Feedback Provider:
Drift Policy:
Heartbeat Prompt:
Native Goal Prompt:
Next Action:
```

Or create/update the Goal Packet files and then report their paths.

## Gotchas

- Do not treat `program.md` as a second ticket. The ticket says what must be
  true; the program says how the loop runs.
- Do not treat `progress.md` as transcript storage. It is compact observed
  state.
- Do not make parent tickets mandatory. Use an inline file list for normal
  multi-file Goals; add `portfolio.md` only when the planning graph needs it.
- Do not hide required files behind transcript memory. If the Goal depends on a
  ticket, program, progress log, board, spec, or artifact, list it in `Files:`.
- Do not make heartbeat automations into hidden autonomy. They are delayed
  triggers for the same Goal Packet contract.
- Do not force numeric metrics onto judgment-heavy work. Use human feedback,
  review verdicts, or artifact-presence signals when those are more honest.
- Do not emit a prompt-only material Goal without a named ticket/program/progress
  setup path.
- Do not route new public execution through `$work`, `$ralph`, or `batch-work`.
  Use Goal Advisor modes instead.

## Reference Map

- [docs/specs/goal-loop-contract.md](../../docs/specs/goal-loop-contract.md) -
  canonical Goal Packet, heartbeat, feedback, drift, and rollout model.
- [references/prompt-templates.md](references/prompt-templates.md) - load only
  when emitting native Goal, heartbeat, setup, or skill-improvement prompt text.
- [references/goal-shapes.md](references/goal-shapes.md) - load when loop-shape
  nuance, batch proof, board drain, rollout, or portfolio boundaries matter.
- [references/goal-algebra.md](references/goal-algebra.md) - load when several
  workflow skills compose into one Goal contract or retired-surface migration
  detail matters.
- [references/goal-portfolio.md](references/goal-portfolio.md) - load before
  designing portfolio-level goal graphs.
- [examples/agi-toy-shop-portfolio.md](examples/agi-toy-shop-portfolio.md) -
  worked long-horizon portfolio example.
- [optimize-with-human](../optimize-with-human/SKILL.md) - route optimization
  loops through human feedback and feedback-file contracts.
- [tickets/templates/goal-loop/portfolio.md](../../tickets/templates/goal-loop/portfolio.md) -
  optional portfolio template.
- [tickets/templates/goal-loop/program.md](../../tickets/templates/goal-loop/program.md) -
  program template.
- [tickets/templates/goal-loop/progress.md](../../tickets/templates/goal-loop/progress.md) -
  progress template.
