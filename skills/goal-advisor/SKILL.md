---
name: goal-advisor
description: "Turn an ambitious request into Goal architecture, ticket-backed loop state, and a native Codex /goal prompt when warranted."
tier: 3
group: harness
source: local
version: 0.2.0
template_uses:
  skill-template: "0.2.0"
  skill-eval-task: "0.1.0"
  skill-qa-checklist: "0.1.0"
eval: eval_task.json
qa_checklist: qa_checklist.md
allowed-tools: Read, Write, Glob, Grep, Bash

---

# Goal Advisor

## Context

`goal-advisor` is the canonical execution compiler for durable Farplane work.
Use it when the operator wants to turn an intent, ticket, board, batch, rollout,
selected project-goal frontier, skill-improvement loop, or feedback loop into a
native Goal, heartbeat, or direct-route recommendation.

Use `horizon-advisor` before this skill when the work is still about deciding
the North Star, KPI tree, project goal map, current milestone, or `goals.md`
strategy delta. `goal-advisor` starts once a frontier is selected enough to
compile into files and execution policy.

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
append-only observations. `farplane/goals.md` is project-level strategy context
when a selected frontier comes from a long-horizon goal graph.

This skill owns both architecture choice and final native `/goal` or heartbeat
prompt compilation. Keep templates with this skill, but load full template
references only after the branch requires prompt emission.

`$work`, `$ralph`, `batch-work`, and the legacy impl skill are retired public
orchestration surfaces. Their useful policies live here as admission/profile,
heartbeat board-drain, batch proof rows, coding-ticket Goal execution,
compute/budget, and blocker handling.

## Skill Signature

```text
advise_goal_use(intent, files?, trigger?, budget?, proof_policy?, approval_policy?) -> goal_architecture + files[] + goal_packet? + heartbeat_prompt? + native_goal_prompt? + next_action
state: reads(operator intent, listed files, tickets, board files?, farplane/goals.md?, program.md?, progress.md?, goal-loop contract, relevant skills/docs); writes(ticket/program/progress? generated goal prompt? or recommendation)
gates: missing_execution_inputs_resolved_or_asked; material_goal_has_files; loop_owner_single; progress_surface_named; metric_provider_named; budget_named; drift_policy_named; logging_policy_named; proof_route_named; final_evidence_policy_named; approval_before_goal_run_when_material
routes: metric-advisor | impl-plan | optimize-with-human | qa | visual-qa | agent-qa-test | review | direct-answer
fails: creates hidden loop runtime; uses Goal without durable state; treats human feedback/heartbeat/rollout as competing loop owners; emits prompt-only material Goal; hides required files behind transcript memory; routes public work through retired work/ralph/batch-work surfaces; emits long Goal prompt that restates ticket context; allows self-certified QA/review/visual completion; runs material Goal before packet approval
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

This skill may route to `optimize-with-human` or `review` only after it chooses
the Goal architecture. It may also emit the native Goal prompt for direct
coding-ticket execution. It does not launch hidden schedulers or preserve
retired public orchestration skills as peers.

When `loop_shape == skill_improvement | optimization` and
`metric_provider == human_feedback`, name `optimize-with-human` as the
human-feedback optimization preset. The Goal Packet still owns state and native
Goal continuation; `optimize-with-human` supplies the feedback protocol:
`feedback-request.md` plus `feedback.json` with `artifact_id`, `score` or
`null`, `verdict`, `feedback`, `labels`, and `next_instruction`.

When called from `impl-plan`, this skill compiles a Goal Packet preview for the
same approval surface as the ticket plan. It should create or update
`program.md`, `progress.md`, and the native `/goal` prompt preview, then pause
for human approval unless an explicit approved auto-run policy already exists.
If the ticket plan changes, rerun this skill and replace the preview before
execution.

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
- loop-shape nuance, batch, board drain, rollout, or project-goals boundary ->
  `references/goal-shapes.md`
- workflow-skill composition or retired-surface migration detail ->
  `references/goal-algebra.md`
- project-goals authoring or strategy design -> `../horizon-advisor/SKILL.md`
- worked examples -> `examples/`

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the intent and decide whether this is material enough for Goal.
   - [ ] Ask up to 3 clarifying questions only when missing execution inputs
     are blocking or materially change files, budget, metric, proof route,
     drift policy, human gates, or destructive/deploy/spend boundaries.
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
   - [ ] If the shape is `skill_improvement` and feedback is Kenji's fastest
     honest quality signal before market tests or benchmarks, route through the
     `optimize-with-human` preset inside the Goal Packet rather than inventing a
     separate feedback runtime.
   - [ ] `rollout`: applies a proven pattern across a target set.
   - [ ] `batch_goal`: executes a listed file set inside one time/budget window
     while preserving per-ticket proof.
   - [ ] `business_loop` or `project_goals`: coordinates recurring or
     long-horizon project work through heartbeat/manual resume and leaf Goals.
   - [ ] For `project_goals` parent work, explicitly explain the boundary:
     native Goal is for one uninterrupted time/budget window over a selected
     file set, while heartbeat/manual resume is for paused, recurring, or
     parent-controller work that chooses the next leaf after state changes.
   - [ ] For any `heartbeat`, explicitly say heartbeat is a trigger over the
     same Goal Packet state, not a separate loop runtime, hidden scheduler, or
     second state owner.
   - [ ] For parent heartbeats, define the action vocabulary:
     `start_goal` starts a ready leaf Goal, `resume_goal` continues a blocked or
     paused child when its blocker clears, `request_feedback` asks for missing
     human/reviewer input, `replan` revises the frontier when the current one is
     exhausted or invalid, and `no_op` logs that nothing useful can advance.
   - [ ] For non-parent heartbeat answers, still name `resume`, `blocked`, and
     `no_op`: resume when a paused Goal can continue, blocked when required
     input/approval/evidence is missing, and no-op when no useful eligible work
     can advance.
   - [ ] Any heartbeat prompt's `Action vocabulary` must include:
     `start_goal`, `resume_goal`, `request_feedback`, `replan`, `blocked`, and
     `no_op`, with one-line meanings.
   - [ ] After a child completes, parent heartbeat records the child completion,
     updates the child node to `complete` or `complete_candidate`, runs or
     requests required proof/review before treating it as done, then chooses
     exactly one next action: `start_goal` or `resume_goal` for the next eligible
     sibling, `request_feedback`, `replan` when the current frontier is
     complete/invalid, or `no_op`.
   - [ ] Load `references/goal-shapes.md` when the chosen shape needs more than
     the one-line classifier above.
- [ ] 3. Choose the state surfaces.
  - [ ] `Files:` in the generated prompt names every ticket, program,
    progress, board, spec, or artifact file the Goal must read.
  - [ ] Include `farplane/goals.md` only when the selected frontier needs
    project-level strategy context.
- [ ] 4. Choose the time/budget policy.
   - [ ] Treat the unit as a time/budget window, not ticket size.
   - [ ] Name time, token/model/compute, subagent, review, QA, feedback, and
     spend limits when they matter; write `none` or `not specified` otherwise.
   - [ ] Use heartbeat when the next useful action depends on elapsed time,
     feedback arrival, an external event, or a periodic board-drain check.
- [ ] 5. Choose the metric or feedback provider.
   - [ ] If the provider, guard metrics, anti-metrics, or no-metric rationale
     are unclear, derive a metric card before writing `program.md`.
   - [ ] `mechanical`: command, script, eval, benchmark, or artifact check.
   - [ ] `review`: TAS verdict from review.
   - [ ] `agent_qa`: adversarial QA evidence.
   - [ ] `human_feedback`: human score, qualitative feedback, or approval.
   - [ ] For `human_feedback` optimization loops, name `optimize-with-human`,
     `feedback-request.md`, and `feedback.json`; define feedback shape as
     `artifact_id`, `score` or `null`, `verdict`, `feedback`, `labels`, and
     `next_instruction`.
   - [ ] `market`: external result such as clicks, replies, sales, or retention.
   - [ ] `hybrid`: combine signals without inventing fake numbers.
   - [ ] If proof weight includes `qa`, `visual_qa`, `agent_qa`, `review`, or
     `demo`, require delegated proof and reject self-certification as the
     metric.
- [ ] 6. Define batch, board-drain, or leaf execution policy when relevant.
   - [ ] For multi-ticket file lists, preserve one proof row per ticket plus
     any batch/integration proof.
   - [ ] For board drain, compile a heartbeat prompt that fetches proceedable
     tickets, skips blocked/gated work, and logs no-op when nothing can advance.
   - [ ] For coding leaves, compile an `active_goal` prompt over the ticket,
     program, progress, and proof files.
   - [ ] For coding leaves that implement features, require a grounding step
     before final evidence: check code documentation or maintained
     implementation evidence through Ref MCP, official docs, GitHub code
     search, maintained examples, or web search unless the ticket is explicitly
     local-only.
   - [ ] For material feature leaves, require execution to follow the ticket's
     critical-path proof notes in `Done / Proof`: run the smaller sanity checks
     in order before claiming a long workflow or lifecycle, record evidence for
     each checkpoint, and block or revise when the final path remains unrun
     without an explicit residual-risk note.
   - [ ] For project-goals leaf Goals, list only the selected leaf file set plus
     `farplane/goals.md` when project strategy context is needed; do not include
     sibling tickets as executable work files.
   - [ ] Leaf Goal logging must append `progress.md` observations and a
     completion entry for every changed ticket before returning control to the
     parent heartbeat.
   - [ ] Load `references/goal-shapes.md` for batch, board-drain, rollout, or
     project-goals details.
- [ ] 7. Define drift policy.
   - [ ] Use inline drift checks for small normal goals.
   - [ ] Use `goal-drift-reviewer` for material, long-running, strategic,
     rollout, or self-approval-prone loops.
   - [ ] Use delegated reviewer or QA lanes for material coding leaves when
     the ticket proof route is judgment-heavy, user-visible, or UI-affecting.
   - [ ] Drift review is read-only and compares the listed files plus recent
     progress; it does not plan or implement.
- [ ] 8. Craft the native `/goal` or heartbeat prompt when Goal mode is warranted.
   - [ ] Load `references/prompt-templates.md` before emitting prompt text.
   - [ ] Include an inline `Files:` list before `Task`, `Logging`, `Metric`, and
     `After each turn`.
   - [ ] Bind the prompt to the listed files, honest metric provider, logging
     files, drift policy, budget, and completion/blocked policy.
   - [ ] Keep the Goal prompt compact: cite ticket/program/design/progress files
     as source of truth instead of restating their full contents.
   - [ ] Include final evidence policy. For UI/user-visible work, completion
     must return best screenshot/image evidence or block with the missing proof.
   - [ ] Include critical-path proof policy for material feature work:
     completion must report which ordered sanity checks ran, where evidence
     lives, and which full-path check remains blocked if the real workflow was
     not exercised.
   - [ ] For implementation feature work, include a final `Grounding:` evidence
     rule in the prompt: name the source class checked, such as Ref MCP,
     official docs, GitHub code search, maintained examples, or web sources, or
     state the local-only reason.
   - [ ] For UI/user-visible work, include literal Markdown image syntax in the
     prompt's final evidence rule:
     `Final evidence: include ![best evidence](ABSOLUTE_SCREENSHOT_PATH), or
     block/revise with the missing screenshot proof.`
   - [ ] Ask only missing execution-safety questions that materially affect the
     Goal contract; cap questions at 3.
   - [ ] Reject proxy-only completion evidence unless it satisfies the actual
     objective.
- [ ] 9. Decide the next owner.
   - [ ] When called from `impl-plan`, return a Goal Packet preview with
     `approval: pending` and `Next Action: human approves plan + Goal Packet`
     unless explicit auto-run approval already exists.
   - [ ] If the ticket plan changed since the packet was compiled, regenerate
     `program.md`, `progress.md`, and the native `/goal` prompt before approval.
   - [ ] Use `optimize-with-human` when the metric provider is `human_feedback`
     and the loop needs a Telegram-first feedback protocol.
   - [ ] For skill-improvement loops with human feedback before market tests,
     output `Use optimize-with-human preset` in the Goal Architecture and
     include the concrete feedback artifact shape.
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
- `Proof route`: which delegated lane owns QA, visual QA, adversarial QA,
  review, demo, or human feedback
- `Final evidence`: what must be shown to the operator before completion,
  including rendered image links for UI/user-visible work when screenshots
  exist
- `Approval`: whether the packet is `pending`, `approved`, `revise`, or
  `blocked`; material packets pause before native Goal execution unless
  explicitly pre-approved

For UI or user-visible work with `visual_qa` proof weight, the Goal prompt must
spell out the concrete lane chain instead of generic "visual proof" language:

```text
Proof route: qa-tester captures screenshots/logs/result.json -> visual-qa judges screenshots against design.md -> reviewer judges final evidence sufficiency.
Self-certification: forbidden for QA, visual judgment, and final completion.
Final evidence: final response includes ![best evidence](ABSOLUTE_SCREENSHOT_PATH), or blocks/revises with the exact missing screenshot proof.
```

## Output

Return either:

```text
Goal Architecture:
Project Goals:
Ticket:
Program:
Progress:
Files:
Trigger:
Budget:
Metric / Feedback Provider:
Drift Policy:
Proof Route:
Final Evidence:
Approval:
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
  multi-file Goals; add `farplane/goals.md` only when project strategy context
  is needed.
- Do not hide required files behind transcript memory. If the Goal depends on a
  ticket, program, progress log, board, spec, or artifact, list it in `Files:`.
- Do not make heartbeat automations into hidden autonomy. They are delayed
  triggers for the same Goal Packet contract.
- Do not force numeric metrics onto judgment-heavy work. Use human feedback,
  review verdicts, or artifact-presence signals when those are more honest.
- Do not re-invent the metric contract inside the Goal prompt. When the signal
  is unclear, derive the metric card first and cite it compactly.
- Do not emit a prompt-only material Goal without a named ticket/program/progress
  setup path.
- Do not route new public execution through `$work`, `$ralph`, or `batch-work`.
  Use Goal Advisor modes instead.
- Do not produce bloated native Goal prompts. The Goal prompt should be a
  compact execution contract over listed files, not a rewritten ticket.
- Do not allow Goal completion to self-certify proof-heavy work. Delegate drift,
  QA, visual judgment, adversarial evidence review, and final readiness when the
  ticket proof route requires those lanes.
- Do not call UI/user-visible work complete unless the final response includes
  the strongest screenshot/image evidence or a clear blocker explaining why no
  such evidence exists.

## Reference Map

- [docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md](../../docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md) -
  canonical Goal Packet, heartbeat, feedback, drift, and rollout model.
- [references/prompt-templates.md](references/prompt-templates.md) - load only
  when emitting native Goal, heartbeat, setup, or skill-improvement prompt text.
- [references/goal-shapes.md](references/goal-shapes.md) - load when loop-shape
  nuance, batch proof, board drain, rollout, or project-goals boundaries matter.
- [references/goal-algebra.md](references/goal-algebra.md) - load when several
  workflow skills compose into one Goal contract or retired-surface migration
  detail matters.
- [../horizon-advisor/SKILL.md](../horizon-advisor/SKILL.md) - use before this
  skill when project-level goal graphs or `goals.md` strategy deltas still
  need to be authored.
- [../metric-advisor/SKILL.md](../metric-advisor/SKILL.md) - derive honest
  metric cards before Goal Packet metric provider compilation.
- [optimize-with-human](../optimize-with-human/SKILL.md) - route optimization
  loops through human feedback and feedback-file contracts.
- [tickets/templates/goal-loop/program.md](../../tickets/templates/goal-loop/program.md) -
  program template.
- [tickets/templates/goal-loop/progress.md](../../tickets/templates/goal-loop/progress.md) -
  progress template.
