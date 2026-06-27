---
name: taste-loop
version: 0.1.0
description: "Run a Codex-native active-hours heartbeat prompt that turns human taste into Goal-backed concept and execution feedback loops."
tier: 3
group: self-improvement
source: local
template_uses:
  skill-template: "0.2.0"
allowed-tools: Read, Glob, Grep, Bash
eval: eval_task.json
---

# Taste Loop

## Context

Use this when a Farplane project should convert active human attention into
structured feedback on product artifacts through the official optional Codex
automation heartbeat. The loop's reward is to impress Kenji enough that he
wants the thing made, while spending as few execution steps as possible. The
heartbeat prompt reads `farplane/products.md`, selects one high-compounding
artifact workflow, creates or reuses a dedicated worker Goal Packet and Codex
thread, and instructs that worker to run a phase-aware
`optimize-with-human` loop.

This skill is a prompt owner, not a script, scheduler, hidden daemon, or
alternate continuation runtime. Codex automation records own cadence; product
lanes own what outputs matter; persistent Codex threads own Telegram reply
routing; worker Goal Packets own durable state; `goal-advisor` compiles the
packet; `metric-advisor` chooses the honest provider; `optimize-with-human`
owns the worker's phase-aware human-feedback protocol; artifact-producing
skills own end-to-end generation after the planning idea passes.

## Skill Signature

```text
taste_loop(project_root, config?, now?)
  -> no_op | artifact_worker_thread_report | artifact_feedback_report |
     idea_feedback_report | artifact_goal_handoff_report | blocked_report
state: reads(farplane/automations.md automation-config TOML?,
             Codex automation memory.md?,
             farplane/products.md,
             farplane/products.md#taste-loop-artifact-workflows,
             docs/skills/registry.jsonl,
             docs/features/FEAT-0064-skill-compounding-score.md,
             tickets/TASK-*/artifacts/agi-toy-shop-scenario.md?,
             tickets/*/ticket.md?,
             skill graph heat / FARPLANE_SKILL_HEAT_*,
             .farplane/automation/taste-loop/*?);
       writes(Codex automation memory.md?,
              .farplane/reports/taste-loop/*.md?,
              tickets/TASK-*/ticket.md?,
              tickets/TASK-*/program.md?,
              tickets/TASK-*/progress.md?,
              .farplane/automation/taste-loop/artifacts/*,
              .farplane/automation/taste-loop/feedback/*?,
              .farplane/automation/taste-loop/preview/*?)
gates: automation_schedule_loaded; feedback_budget_checked; product_lane_selected;
       impress_reward_bound; idea_execution_phases_bound;
       controller_memory_checked; active_worker_reused_or_resumed;
       artifact_workflow_selected; worker_packet_created_or_reused;
       goal_packet_created_or_reused; planning_experiment_logged;
       worker_thread_created_or_reused; optimize_with_human_bound_in_worker;
       taste_proposal_or_artifact_ref_visible; artifact_generated_or_goal_handoff;
       preview_ref_visible_for_visual_artifacts; open_feedback_deduped;
       legacy_invalid_feedback_excluded_from_budget; no_hidden_scheduler
routes: landing-page | social-content | video-production |
  product-photography | farplane-evidence-content |
  farplane-experiment-report | farplane-ablation-proof |
  farplane-productization | optimize-with-human | goal-advisor | create_thread |
  review
fails: creates a local runner as the primary surface; runs hidden loops;
  asks for feedback on a skill summary; selects broad router skills as direct
  targets; creates a feedback card without an artifact; optimizes generic skill
  quality instead of a products.md output; routes to retired autoresearch by
  default; sends Telegram feedback from the parent heartbeat thread when a
  dedicated worker thread is needed; spams more feedback than budget allows;
  creates a separate workers.jsonl ledger instead of reusing automation memory;
  asks Kenji to judge a thin hook-only card when the artifact needs a proposal;
  writes repo/runtime files for a simple no-op beat; executes full artifacts
  before an idea passes when the artifact is not itself the tiny planning test;
  edits target skills after one rejection instead of logging and rerunning a
  phase experiment
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Load automation config and controller memory.
  - [ ] Read the `farplane/automations.md` marker-delimited TOML config block
    and prompt block for `farplane-active-hours-taste-loop` when available.
  - [ ] Treat the Codex automation schedule as cadence metadata owned by the
    Codex automation record; do not re-check active hours inside the skill.
  - [ ] Use the prompt block `Params` section for Taste Loop knobs such as
    `top_n`, `max_open_feedback`, target groups, output channels, cooldown,
    convergence, and `log_noop`.
  - [ ] Read the Codex automation `memory.md` when the automation runtime
    provides one.
  - [ ] Treat manual invocation as explicit operator intent to run one bounded
    beat now, regardless of the configured schedule.
- [ ] 2. Collect candidate targets.
  - [ ] Read `docs/features/FEAT-0064-skill-compounding-score.md`.
  - [ ] Read `docs/skills/registry.jsonl`.
  - [ ] Read `farplane/products.md` Work Lanes and Taste Loop Artifact
    Workflows.
  - [ ] Use existing skill heat generated from `.farplane/events/` and
    `FARPLANE_SKILL_HEAT_*` controls when available.
  - [ ] Split heat into direct heat and weaker composition heat from referring
    skills, matching `docs/features/FEAT-0064-skill-compounding-score.md`.
  - [ ] Prefer artifact workflows tied to configured target groups and
    product/money-making lanes.
  - [ ] Exclude broad router skills as direct targets. `frontend-craft`,
    `functional-ui`, `remotion`, `remotion-render`, `goal-advisor`,
    `self-improve`, and `skill-maintenance` can support a workflow but should
    not be the thing Kenji is asked to judge.
  - [ ] Include existing open feedback and cooldown state.
  - [ ] Include active worker, waiting feedback, and last action state from
    automation memory before reading legacy Taste Loop runtime files.
  - [ ] Normalize open feedback by `target_id + feedback_question` before
    applying the budget gate; duplicate open rows are hygiene findings, not
    extra budget usage.
  - [ ] Count only valid product-workflow feedback toward `max_open_feedback`.
    Feedback cards that target broad router skills or skill summaries are
    `legacy_invalid_feedback` hygiene findings and must not block the impress
    loop.
- [ ] 3. Score and select top N.
  - [ ] Use the FEAT-0064 skill signal contract: direct heat, composition heat,
    maintenance burden, and uniqueness; expose the raw signals and the final
    recommendation in the report.
  - [ ] Keep skill signals distinct from eval score, review TAS, and human
    preference labels.
  - [ ] Require `artifact_workflow_fit`: the candidate can create or hand off a
    reviewable artifact end-to-end from `products.md`.
  - [ ] Penalize unique open feedback, cooldown, ambiguous targets, and fake
    metric risk.
- [ ] 4. Bind the impress loop.
  - [ ] Set reward objective to `impress Kenji enough that he wants the thing
    made`.
  - [ ] Treat planning artifacts as first-class TasteProposal objects:
    best-bet briefs, storyboard premises, offer angles, proof angles, or hook
    batches with enough audience, insight, beats, risks, and next step detail
    for Kenji to judge.
  - [ ] Treat execution artifacts as second-stage outputs: landing pages,
    reels, carousels, scripts, proof reports, demos, or shipped proposals.
  - [ ] Use the fixed AGI Toy Shop scenario when no live product context is
    explicitly better.
  - [ ] Allow a small planning multi-batch, default max 3 concept rollouts, when
    fast idea feedback is more useful than one polished execution.
  - [ ] Keep `idea_pass_rate` and `execution_pass_rate` separate in memory and
    reports.
  - [ ] Do not edit target skills from first rejection; log the experiment and
    perturb planning or execution first.
- [ ] 5. Route exactly one Codex-native bounded action by default.
  - [ ] Ask `metric-advisor` for an honest provider before creating benchmarks,
    harder task suites, or Goal handoffs.
  - [ ] Prefer `artifact_worker_thread` for human-feedback product artifacts:
    first reuse or resume an active worker from automation memory; otherwise
    create or reuse a ticket-backed Goal Packet, then create or reuse a
    dedicated Codex worker thread whose prompt tells the worker to use
    `optimize-with-human`.
  - [ ] Generate a small concept artifact immediately when the owning artifact
    skill can do so inside the worker thread without hidden continuation.
  - [ ] Start full execution only after planning feedback passes, unless the
    artifact is tiny enough to be the planning test.
  - [ ] Use `artifact_goal_handoff` when native Goal mode should generate the
    artifact in a bounded continuation.
  - [ ] Use direct `artifact_feedback_report` through `optimize-with-human` only
    when an existing worker thread already owns the reply path or the artifact
    is intentionally local/manual.
  - [ ] Use `blocked_report` when the target lacks product-lane ownership,
    artifact workflow ownership, proof, config, or generation feasibility.
  - [ ] Do not route to legacy autoresearch unless explicitly configured later.
- [ ] 6. Write visible state, not hidden runtime output.
  - [ ] Update Codex automation memory with the active worker ledger when
    available; do not create a separate `workers.jsonl`.
  - [ ] Write a Markdown report under `.farplane/reports/taste-loop/` only for
    emitted actions, blockers, diagnostics, or when
    `FARPLANE_TASTE_LOOP_LOG_NOOP=1`.
  - [ ] For `artifact_worker_thread`, write or update `ticket.md`, `program.md`,
    and `progress.md` under `tickets/TASK-*`, and record the worker thread id
    in the ticket links, progress log, and Taste Loop report.
  - [ ] Ensure `program.md` defines the planning and execution phases, fixed
    scenario, feedback shape, budget, and skill-promotion rule.
  - [ ] Ensure `progress.md` logs experiment proposals and results before and
    after every phase attempt.
  - [ ] Write generated artifacts under
    `.farplane/automation/taste-loop/artifacts/`.
  - [ ] Write feedback-card and Goal-handoff Markdown artifacts under
    `.farplane/automation/taste-loop/feedback/` when useful.
  - [ ] For website, image, video, or other visual artifacts, also write a
    preview wrapper or manifest under `.farplane/automation/taste-loop/preview/`
    so Kenji can open a single URL or Farplane UI-ready file without hunting
    through reports.
  - [ ] Feedback cards must include `proposal_ref`, `concept_ref`, or
    `artifact_ref`; if no planning or execution artifact was produced or handed off, write
    `blocked_report` instead of a feedback card.
  - [ ] Keep generated feedback questions short and decision-shaped.
  - [ ] When duplicate open feedback exists, report the canonical card and
    duplicate rows; do not create another duplicate for that target/question.
- [ ] 7. Stop cleanly.
  - [ ] Report the action, skipped targets, report path, and next trigger.
  - [ ] Do not edit target skills directly from this heartbeat.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Automation Config

Project-specific automation metadata lives in `farplane/automations.md` as a
marker-delimited TOML block. Skill invocation params live in the adjacent
prompt block because they are part of the Codex instruction, not scheduler
metadata.

```toml
[schedule]
type = "active_hours_interval"
timezone = "Asia/Kuala_Lumpur"
days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
start = "10:00"
end = "18:00"
interval_minutes = 60
```

The schedule block compiles to the Codex automation cadence. Taste Loop should
not duplicate that cadence as environment variables. The prompt block should
carry the normal Markdown/text `Params` and `Overrides` sections. Once invoked,
the skill runs one bounded beat; it does not perform an additional active-hours
check.

## Heartbeat Prompt

The automation prompt is the runtime surface. Use
[templates/heartbeat-prompt.md](templates/heartbeat-prompt.md) as the reusable
prompt body, and keep `farplane/automations.md` as the project-specific copied
automation record.

## Scoring Contract

The prompt should consume the FEAT-0064 skill signal contract from
`docs/features/FEAT-0064-skill-compounding-score.md`, then apply the Taste
Loop-specific artifact workflow gate. Expose readable signals and a
recommendation rather than hiding a magic ranking:

```text
skill_signals(skill, project_state, lifecycle_refs, now?)
  -> direct_heat + composition_heat + maintenance_burden + uniqueness
  -> maintenance_recommendation + route_hint
```

Signal ownership:

- algorithm and component meanings: `docs/features/FEAT-0064-skill-compounding-score.md`
- tier, group, description, links: `docs/skills/registry.jsonl`
- lifecycle-reference distance: `docs/farplane-framework/lifecycle.md` and
  lifecycle graph data when available
- heat: generated skill graph heat from `.farplane/events/` and
  `FARPLANE_SKILL_HEAT_*`
- product lane: `farplane/products.md`
- artifact workflow fit: `farplane/products.md` Taste Loop Artifact Workflows
- schedule and params: `farplane/automations.md` TOML automation config
- feedback budget and cooldown: automation config plus controller memory
- active worker state: Codex automation `memory.md`
- metric route: `metric-advisor`

Taste Loop may use broad skills as support routes, but the selected target is
always:

```text
product_lane + workflow_id + owner + artifact_ref
```

`feedback_card` is invalid without `artifact_ref`.

## Impress Loop Contract

Taste Loop's human-facing reward is:

```text
maximize P(Kenji says "that's sick, make that") per unit of attention
```

Use a two-stage loop:

```text
planning_phase:
  taste pack + product goal + fixed scenario + best-of-worlds synthesis
  -> one to three TasteProposal planning artifacts
  -> Kenji approve | revise | reject

execution_phase:
  approved concept becomes frozen brief
  -> artifact-producing skill executes
  -> Kenji approve | revise | reject
```

Planning feedback is usually cheaper and higher-signal than full artifact
feedback. Do not spend execution effort until an idea passes, unless the output
is tiny enough to serve as the idea test.

Default fixed scenario:

```text
tickets/TASK-0237/artifacts/agi-toy-shop-scenario.md
```

Use live product context instead only when the automation prompt, worker
ticket, or operator explicitly supplies a better target.

Taste proposals are the default first-stage artifacts. Hook-only concept cards
are valid only when the planned artifact itself is a hook, headline, or other
tiny unit. For normal content, website, video, proof, or campaign workflows,
planning feedback should expose enough detail for Kenji to judge the idea
without asking follow-up questions.

```text
TasteProposal:
  title:
  one_line_bet:
  audience_or_buyer:
  taste_insight:
  artifact_shape:
  core_angle:
  execution_beats:
    - beat_1:
    - beat_2:
    - beat_3:
    - beat_4:
    - beat_5:
  why_it_could_win:
    - reason_1:
    - reason_2:
    - reason_3:
  what_would_make_it_cringe:
    - risk_1:
    - risk_2:
  references_or_taste_pack:
  feedback_question:
  next_if_approved:
```

Use [templates/taste-proposal.md](templates/taste-proposal.md) for the compact
proposal shape and Telegram digest.

Keep phase metrics separate:

```text
idea_pass_rate = planning approvals / planning attempts
execution_pass_rate = execution approvals / execution attempts
```

If planning fails, perturb planning: references, best-bet synthesis, hook,
positioning, scenario angle, or concept batch. If execution fails but the idea
still passes, perturb execution: artifact skill, brief, layout, copy, media,
proof, or rendering path. Promote skill changes only after repeated same-phase
failures or an obviously reusable approved pattern.

## Worker Thread Contract

Taste Loop's default human-feedback action is a worker handoff:

```text
artifact_worker_thread(product_lane, workflow_id, owner, feedback_question)
  -> ticket_ref + program_ref + progress_ref + worker_thread_ref + report_ref
```

The parent heartbeat selects and dispatches. It does not own artifact iteration.
The worker thread prompt must name the Goal Packet files inline and instruct the
worker to use `optimize-with-human` after creating a reviewable artifact.

## Controller Memory Contract

Use the Codex automation's own memory as the controller ledger when available.
Do not add a tracked or ignored `workers.jsonl` just to remember active Taste
Loop workers.

Each action beat should append or update a compact memory row with:

```text
active_worker:
  workflow_id:
  product_lane:
  ticket_ref:
  worker_thread_ref:
  status: active | waiting_for_feedback | revising | blocked | complete
  artifact_ref:
  preview_ref:
  last_request_at:
  last_feedback_at:
  next_action:
```

On every heartbeat, read memory before creating work:

```text
if active_worker.status in [active, waiting_for_feedback, revising]:
  inspect or resume that worker
  do not create a new worker
else:
  score candidates and dispatch at most one new worker
```

Simple no-op beats should be side-effect free: no worker thread, ticket,
artifact, preview, feedback card, Telegram message, or repo/runtime report.
Only write a no-op report when explicitly diagnosing with `log_noop = true`;
otherwise the Codex automation run and memory surface are enough.

Required worker prompt shape:

```text
Files:
- tickets/TASK-XXXX/ticket.md
- tickets/TASK-XXXX/program.md
- tickets/TASK-XXXX/progress.md
- tickets/TASK-0237/artifacts/agi-toy-shop-scenario.md when no live scenario is supplied

Task:
Use $<artifact-owner> to run a phase-aware improvement loop for <workflow>.
First log a planning experiment proposal in progress.md, then create one to
three TasteProposal planning artifacts for Kenji. Use $optimize-with-human with
target=<workflow>, objective=<what should improve>, channel=telegram,
feedback_policy=ask_when_artifact_ready, and phases=planning,execution. Each
proposal must include audience/buyer, taste insight, artifact shape, core
angle, 5+ execution beats, why it could win, cringe risks, references or taste
pack, feedback question, and next step if approved. When Kenji approves a
proposal, freeze the approved brief, log an execution experiment proposal in
progress.md, and execute the artifact. When Kenji replies, append feedback to
progress.md and continue the right phase. Stop only on
keep/approve/convergence/budget/blocker.
```

For Telegram-routed feedback, the feedback request should point Kenji at the
worker thread identity and the artifact preview, not at the parent heartbeat
thread. Localhost URLs are allowed only as computer-side smoke proof; the worker
must prefer a public/mobile-viewable URL, attached screenshot, or Farplane
UI-ready preview when asking for phone feedback.

## Feedback Budget

Open feedback budget is based on unique active requests, not raw JSONL rows.
Normalize each open feedback row by:

```text
feedback_key = target_id + "\n" + feedback_question
```

Only one open row for a key counts toward the configured `max_open_feedback`.
Additional open rows with the same key
must be listed in the report as `duplicate_open_feedback` and should not block
new useful work. If the top selected target already has an open canonical card,
skip it with `open_feedback_and_cooldown` and pick the next eligible target
rather than creating another duplicate.

Budget eligibility is stricter than open-card detection:

- valid idea feedback has a `workflow_id`, `product_lane`, and `proposal_ref`
  or `concept_ref`;
- valid execution feedback has a `workflow_id`, `product_lane`, and
  `artifact_ref`;
- older broad skill/router cards such as `target_id=frontend-craft`,
  `functional-ui`, `remotion`, `remotion-render`, `goal-advisor`,
  `self-improve`, or `skill-maintenance` are `legacy_invalid_feedback`;
- `legacy_invalid_feedback` and duplicates are reported as hygiene findings but
  do not count toward `max_open_feedback`.

## Experiment Log Contract

Taste Loop workers must append experiment proposals and results to their
`progress.md` before and after every phase attempt:

```text
experiment:
  id: TL-EXP-###
  phase: planning | execution
  scenario: AGI Toy Shop | live_context
  hypothesis:
  skill_delta_candidate:
  rollout_batch:
    - proposal_or_artifact_id:
      proposal_ref:
      plan:
      expected_feedback:
  selected_rollout:
  feedback:
  result: pass | revise | reject | no_reply | blocker
  promotion_decision: keep_local | rerun | harden_skill | discard
```

`promotion_decision=harden_skill` requires repeated same-phase failure or an
operator-approved pattern that clearly belongs in a reusable skill contract.

## Benchmark And Convergence

Do not create benchmarks by default. Use an existing target-skill eval or
benchmark when it exists. Create harder tasks only after `metric-advisor`
selects `eval` or `agent_qa` and `self-improve` defines a baseline, rubric, and
promotion rule. When human taste is the honest signal, use
`optimize-with-human` instead of pretending a benchmark exists.

Convergence is comparable-run based: hold or stop when recent score, review, or
feedback deltas stay below the configured `minimum_delta` across the configured
`convergence_window` comparable runs.

## Output

Return and write:

- `status`: `no_op`, `artifact_worker_thread`, `artifact_feedback`,
  `idea_feedback`, `artifact_goal_handoff`, or `blocked`
- `report_path` when an action, blocker, diagnostic, or configured no-op log is
  written
- `selected_product_lane`
- `selected_artifact_workflow`
- `worker_ticket_ref`
- `worker_thread_ref`
- `artifact_ref`
- `proposal_ref`
- `concept_ref`
- `idea_pass_rate`
- `execution_pass_rate`
- `preview_ref` for website, image, video, or visual artifacts
- `score_breakdown`
- `action`
- `skipped_targets`
- `open_feedback_count`
- `next_trigger`

## Gotchas

- Do not make Daily/Weekly Interval execute this loop internally. Intervals set
  priorities; this heartbeat turns active human attention into feedback cards
  or Goal handoffs.
- Do not call `optimize-with-human` as the parent heartbeat's first move when
  Telegram replies need a stable worker thread. Create or reuse the packet and
  thread first, then instruct the worker to call `optimize-with-human`.
- Do not add a local runner just to make the prompt testable. The behavior is
  reviewed as a prompt contract plus sample artifacts.
- Do not call this a training loop. It creates structured feedback and
  accepted writeback opportunities; it does not train models.
- Do not ask Kenji to review a skill summary, skill README, or generic skill
  quality target. Ask for feedback on an artifact created by a product workflow.
- Do not use broad router skills as direct targets. Pick an artifact workflow
  from `farplane/products.md`; use router skills only as supporting routes.
- Do not create execution `feedback_card` without `artifact_ref`.
- Do not create an idea feedback card without `concept_ref` or `proposal_ref`.
- Do not skip the Goal Packet for optimize-with-human workers. Worker state
  belongs in `ticket.md`, `program.md`, and `progress.md`.
- Do not run execution before planning approval unless the execution artifact
  is intentionally tiny enough to be the planning artifact.
- Do not edit target skills on first rejection. Log and rerun planning or
  execution experiments first; harden skills only for repeated same-phase
  failures or proven reusable patterns.
- Do not make Kenji choose from a giant batch. Use one best bet by default and
  at most three TasteProposal rollouts when fast comparison is useful.
- Do not ask Kenji to judge shallow hook cards for non-hook artifacts. Planning
  proposals need audience, insight, artifact shape, execution beats, why it
  could win, risks, and next step.
- Do not send website feedback without a browser-viewable `preview_ref`, local
  URL, deploy URL, or Farplane UI-ready preview manifest.
- Do not send phone-facing Telegram feedback with only `localhost`. Include a
  worker thread reference plus a public/mobile-viewable URL, screenshot, or
  Farplane UI-ready preview fallback.
- Do not let open feedback pile up. Respect `MAX_OPEN_FEEDBACK`.
- Do not let duplicate feedback rows consume the open-feedback budget. Count
  unique active requests and report duplicate rows as hygiene.
- Do not optimize by fake numeric taste scores. Use labels, rankings, and
  accept/revise/reject when that is the honest signal.
- Do not invent a second heat, product, or benchmark system. Reuse the skill
  graph, `products.md`, `metric-advisor`, and target skill evals first.
- Do not create a new worker when automation memory shows an active or waiting
  worker. Resume, steer, or block that worker first.
- Do not create tracked or ignored worker ledgers. The Codex automation memory
  is the Taste Loop controller state.
- Do not write `.farplane/reports/taste-loop/` files for ordinary no-op beats.
  No-op means no worker, no artifact, no feedback, no Telegram, and no runtime
  report unless diagnostic logging is explicitly enabled.
- Do not restore `FARPLANE_TASTE_LOOP_*` as the normal active-hours settings.
  Active-hours belong in the Codex automation schedule and the
  `farplane/automations.md` TOML config block.

## Reference Map

- [../metric-advisor/SKILL.md](../metric-advisor/SKILL.md) - metric provider
  and route hints.
- [../optimize-with-human/SKILL.md](../optimize-with-human/SKILL.md) -
  feedback protocol and feedback schema.
- [../self-improve/SKILL.md](../self-improve/SKILL.md) - skill memory,
  baselines, candidates, and promotion rules.
- [../goal-advisor/SKILL.md](../goal-advisor/SKILL.md) - Goal Packet and
  heartbeat prompt compilation.
- `docs/features/FEAT-0064-skill-compounding-score.md` - official score algorithm and
  component source ownership.
- `farplane/automations.md` - reviewed automation prompt source.
- [templates/taste-proposal.md](templates/taste-proposal.md) - planning
  proposal template and phone-friendly digest shape.
