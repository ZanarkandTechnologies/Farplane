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
automation heartbeat. The loop's reward is to earn Kenji's founder conviction
that a product/artifact bet is worth making, selling, or testing, while spending
as few execution steps as possible. The
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
     idea_feedback_report | feedback_reminder_report |
     artifact_goal_handoff_report | blocked_report
state: reads(farplane/automations.md automation-config TOML?,
             Codex automation memory.md?,
             farplane/products.md,
             farplane/products.md#taste-loop-artifact-workflows,
             docs/skills/registry.jsonl,
             docs/features/FEAT-0064-skill-signals.md,
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
       artifact_workflow_selected; founder_lens_bound;
       workflow_ticket_reused_until_terminal; worker_packet_created_or_reused;
       goal_packet_created_or_reused; planning_hypothesis_logged;
       worker_thread_created_or_reused; optimize_with_human_bound_in_worker;
       worker_thread_visible_or_blocked; stale_feedback_reminded_or_deferred;
       progress_hypothesis_cycle_validated;
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
  asks Kenji to judge internal planning metadata instead of a customer-facing
  pitch with context, problem, solution, and the exact decision;
  records a worker id that cannot be found in the Codex thread list;
  claims Telegram was sent without a phone-viewable message artifact and send
  proof; lets stale open feedback sit silently past the reminder interval;
  writes repo/runtime files for a simple no-op beat; executes full artifacts
  before an idea passes when the artifact is not itself the tiny planning test;
  edits target skills after one rejection instead of logging and rerunning a
  phase hypothesis cycle; creates a new TL ticket or fresh named TL-EXP item
  for each update in the same active workflow instead of appending hypothesis,
  attempt, feedback, learning, and next hypothesis to the existing workflow
  progress log until convergence, approval, blocker, budget, or operator
  closeout; skips the hypothesis-cycle validator when `program.md` opts into
  `progress_unit = hypothesis_cycle`
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
  - [ ] Read `docs/features/FEAT-0064-skill-signals.md`.
  - [ ] Read `docs/skills/registry.jsonl`.
  - [ ] Read `farplane/products.md` Work Lanes and Taste Loop Artifact
    Workflows.
  - [ ] Use existing skill heat generated from `.farplane/events/` and
    `FARPLANE_SKILL_HEAT_*` controls when available.
  - [ ] Split heat into direct heat and weaker composition heat from referring
    skills, matching `docs/features/FEAT-0064-skill-signals.md`.
  - [ ] Prefer artifact workflows tied to configured target groups and
    product/money-making lanes.
  - [ ] Exclude broad router skills as direct targets. `frontend-craft`,
    `functional-ui`, `remotion`, `remotion-render`, `goal-advisor`,
    `self-improve`, and `skill-maintenance` can support a workflow but should
    not be the thing Kenji is asked to judge.
  - [ ] Include existing open feedback and cooldown state.
  - [ ] Include active worker, waiting feedback, and last action state from
    automation memory before reading legacy Taste Loop runtime files.
  - [ ] For every active worker, verify the recorded `worker_thread_ref` is
    app-visible when thread tools are available; if not, block instead of
    claiming the worker is waiting.
  - [ ] Check stale feedback reminders using `last_request_at`,
    `last_reminder_at`, `reminder_count`, `reminder_after_hours`, and
    `max_reminders_per_feedback`.
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
  - [ ] Set reward objective to `earn Kenji's founder conviction that this bet
    is worth making, selling, or testing`.
  - [ ] Bind `founder_lens=true` for product-lane content, offer,
    distribution, market-learning, and artifact workflows.
  - [ ] Require founder framing in planning artifacts: customer/buyer, painful
    or funny problem, wedge, offer/artifact, distribution angle, validation
    question, next bet if approved, and pivot trigger if rejected.
  - [ ] Treat planning artifacts as first-class TasteProposal objects:
    best-bet briefs, storyboard premises, offer angles, proof angles, or hook
    batches with enough audience, insight, beats, risks, and next step detail
    for Kenji to judge.
  - [ ] Make planning feedback customer-facing before it is evaluative:
    explain the task context, bigger problem, proposed solution, what Kenji is
    judging, and a vivid marketing pitch that makes the idea feel desirable.
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
    find and reuse the active ticket/Goal Packet for the same
    `product_lane + workflow_id` until that workflow reaches a terminal state;
    only create a new ticket for a new workflow, a terminal prior ticket, or an
    explicit operator request. Then create or reuse a dedicated Codex worker
    thread whose prompt tells the worker to use `optimize-with-human`.
  - [ ] When a visible worker is waiting for feedback and the reminder interval
    has elapsed, route exactly one phone-viewable reminder through that same
    worker thread, then update `progress.md` and automation memory. Prefer
    simple Telegram Markdown for Taste Loop feedback/reminder bodies.
  - [ ] If the recorded worker thread is missing or unfindable, write a blocker
    in the ticket/progress/report instead of creating another replacement
    worker with an unverified id.
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
  - [ ] After creating or reusing a worker thread, set or confirm a searchable
    title containing `Taste Loop`, the ticket id, and workflow id; only then
    record it as the active worker.
  - [ ] Ensure `program.md` defines the planning and execution phases, fixed
    scenario, feedback shape, budget, and skill-promotion rule.
  - [ ] Ensure `progress.md` logs hypothesis cycles before and after every
    phase attempt: current hypothesis, planned attempt, artifact refs, human
    question, feedback result, learning, and next hypothesis.
  - [ ] When `program.md` declares `progress_unit = hypothesis_cycle`, run
    `python3 skills/taste-loop/scripts/check_progress_hypothesis_cycles.py
    <program.md> <progress.md>` before recording waiting/completion state.
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
  - [ ] Reminder messages must include the reviewable summary again, not just
    "please reply" or a local path.
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
`docs/features/FEAT-0064-skill-signals.md`, then apply the Taste
Loop-specific artifact workflow gate. Expose readable signals and a
recommendation rather than hiding a magic ranking:

```text
skill_signals(skill, project_state, lifecycle_refs, now?)
  -> direct_heat + composition_heat + maintenance_burden + uniqueness
  -> maintenance_recommendation + route_hint
```

Signal ownership:

- algorithm and component meanings: `docs/features/FEAT-0064-skill-signals.md`
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
maximize P(Kenji says "that's worth making/selling/testing") per unit of attention
```

Taste Loop should operate like a tiny founder loop for product-lane artifacts:

```text
founder_loop(product_lane, workflow_id, scenario, phase, feedback?)
  -> customer_or_buyer
   + problem
   + wedge
   + offer_or_artifact
   + distribution_angle
   + validation_question
   + next_bet_if_approved
   + pivot_trigger_if_rejected
```

The founder lens is not a roleplay flourish. It is the decision frame that
keeps planning from becoming internal artifact grading. The worker should ask
whether the bet is worth building, selling, testing, or revising, and should
explain what customer reaction, distribution signal, or founder conviction the
artifact is trying to earn.

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
  task_context:
  customer_or_buyer:
  bigger_problem:
  wedge:
  proposed_solution:
  distribution_angle:
  validation_question:
  customer_pitch:
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
  pivot_trigger_if_rejected:
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
The controller must set or confirm an app-visible title before writing the
worker id as live state:

```text
Taste Loop Worker: TASK-XXXX <workflow_id>
```

If the thread cannot be found by id or title after creation/reuse, the action is
`blocked_report`, not `waiting_for_feedback`.

## Workflow Ticket Reuse Contract

Taste Loop tickets are workflow containers, not per-experiment receipts. Reuse
one active ticket and Goal Packet for the same:

```text
ticket_key = product_lane + "/" + workflow_id
```

Append each planning or execution attempt as a timestamped hypothesis cycle in
`progress.md`, and keep artifacts under the same ticket's `artifacts/` folder.
Create a new ticket only when no ticket exists for the workflow, the prior
workflow ticket is terminal (`complete`, `blocked`, `discarded`, `closed`,
`budget_exhausted`, or explicit operator closeout), or the operator explicitly
asks for a fresh ticket. A `revise`, `reject`, reminder, or no-reply state is
not terminal; keep using the same ticket and worker/Goal Packet when visible.

## Controller Memory Contract

Use the Codex automation's own memory as the controller ledger when available.
Do not add a tracked or ignored `workers.jsonl` just to remember active Taste
Loop workers.

Each action beat should append or update a compact memory row with:

```text
active_worker:
  workflow_id:
  product_lane:
  ticket_key:
  ticket_ref:
  worker_thread_ref:
  status: active | waiting_for_feedback | revising | blocked | complete
  artifact_ref:
  preview_ref:
  last_request_at:
  last_reminder_at:
  reminder_count:
  last_feedback_at:
  next_action:
```

On every heartbeat, read memory before creating work:

```text
if active_worker.status in [active, waiting_for_feedback, revising]:
  verify worker_thread_ref is visible when thread tools are available
  if missing: write blocked_report and stop
  if waiting_for_feedback and reminder_due: send a phone-viewable reminder from
    the worker thread, update progress/memory, and stop
  inspect or resume that worker
  do not create a new worker
else:
  find reusable active workflow ticket by ticket_key before creating a new one
  score candidates and dispatch at most one new worker
```

Simple no-op beats should be side-effect free: no worker thread, ticket,
artifact, preview, feedback card, Telegram message, or repo/runtime report.
Only write a no-op report when explicitly diagnosing with `log_noop = true`;
otherwise the Codex automation run and memory surface are enough.

## Feedback Reminder Contract

Waiting-for-feedback is an active state, not a silent terminal state. On each
heartbeat, if a visible worker is waiting for planning or execution feedback,
compare the current time to `last_request_at` and `last_reminder_at`.

```text
reminder_due(worker, now, reminder_after_hours, max_reminders_per_feedback)
  -> true when worker.status in [waiting_for_feedback,
                                waiting_for_idea_feedback,
                                waiting_for_execution_feedback]
   and reminder_count < max_reminders_per_feedback
   and hours_since(max(last_request_at, last_reminder_at)) >= reminder_after_hours
```

When due, send exactly one reminder from the visible worker thread using
`telegram-message`. The reminder must be phone-viewable: start with
`Review artifact`, `Skill/workflow`, `Product`, `Stage`, and `Not judging` so
Kenji can immediately tell whether he is reviewing an idea, video, product
build, copy draft, or internal skill artifact. Then include the current
proposal/artifact summary, the one reply action, and only then desktop refs.
Use simple Telegram Markdown for controlled Taste Loop feedback/reminder bodies
so the decision is easier to scan on a phone. Use raw text only when the body
contains arbitrary code, JSON, dense paths, or generated text that could break
Telegram Markdown parsing.
After the send or fallback, append reminder status to `progress.md` and update
automation memory. If Telegram is unavailable, write a visible fallback request
and a blocker; do not silently wait.

Required worker prompt shape:

```text
Files:
- tickets/TASK-XXXX/ticket.md
- tickets/TASK-XXXX/program.md
- tickets/TASK-XXXX/progress.md
- tickets/TASK-0237/artifacts/agi-toy-shop-scenario.md when no live scenario is supplied

Task:
Use $<artifact-owner> to run a phase-aware improvement loop for <workflow>.
First log a planning hypothesis cycle in progress.md, then create one to
three TasteProposal planning artifacts for Kenji. Use $optimize-with-human with
target=<workflow>, objective=<what should improve>, channel=telegram,
feedback_policy=ask_when_artifact_ready, phases=planning,execution, and
founder_lens=true. Each
proposal must first orient the review object in phone-viewable terms: review
artifact type, owner skill/workflow, product/lane, stage, and what Kenji is not
judging. Then sell the idea like a customer-facing pitch: task context, bigger
problem, proposed solution, what Kenji is judging, and vivid marketing language
that makes the concept feel desirable. Then include founder framing:
customer/buyer, problem, wedge, offer/artifact, distribution angle, validation
question, next bet if approved, and pivot trigger if rejected, plus taste
insight, artifact shape, core angle, 5+ execution beats, why it could win,
cringe risks, references or taste pack, feedback question, and next step. When
Kenji approves a proposal, freeze the approved brief, append an execution
hypothesis cycle in progress.md, and execute the artifact. When Kenji replies,
append feedback, learning, and the next hypothesis to progress.md, then
continue the right phase in the same workflow ticket. If Kenji replies with
`revise` or `reject`, the worker
response must restate the corrected review object and ask for the next
instruction or send the revised review request; do not merely acknowledge,
create a new ticket, create a fresh named TL-EXP item, or stop.
Stop only on
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

## Progress Log Contract

Taste Loop workers must append hypothesis cycles to `progress.md` before and
after every phase attempt. The progress log is the autoresearch-style state
machine: write the hypothesis, try it, ask the human, record the signal, learn,
then write the next hypothesis. Do not create a fresh named `TL-EXP-###` item
for every update. Use stable artifact filenames when useful, but make
`progress.md` the source of truth.

```text
hypothesis_cycle:
  phase: planning | execution
  scenario: AGI Toy Shop | live_context
  current_hypothesis:
  planned_attempt:
  artifact_refs:
    - path:
      role:
  human_question:
  expected_signal:
  skill_delta_candidate:
  human_signal:
    verdict: approve | revise | reject | no_reply | blocker
    feedback:
    labels:
  learning:
  next_hypothesis:
  promotion_decision: keep_local | rerun | harden_skill | discard
```

`promotion_decision=harden_skill` requires repeated same-phase failure or an
operator-approved pattern that clearly belongs in a reusable skill contract.

Mechanical guard:

```bash
python3 skills/taste-loop/scripts/check_progress_hypothesis_cycles.py \
  tickets/TASK-XXXX/program.md \
  tickets/TASK-XXXX/progress.md
```

The validator is intentionally history-tolerant: old `TL-EXP` entries remain
valid as historical state, but once a ticket records `progress_unit =
hypothesis_cycle`, new progress entries must not introduce fresh `TL-EXP`
primary work units and every `hypothesis_cycle:` block must include the required
fields.

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
  `idea_feedback`, `feedback_reminder`, `artifact_goal_handoff`, or `blocked`
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
- `reminder_status` when stale feedback is nudged or blocked
- `skill_signals`
- `maintenance_recommendation`
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
  execution hypothesis cycles first; harden skills only for repeated same-phase
  failures or proven reusable patterns.
- Do not make Kenji choose from a giant batch. Use one best bet by default and
  at most three TasteProposal rollouts when fast comparison is useful.
- Do not ask Kenji to judge shallow hook cards for non-hook artifacts. Planning
  proposals need audience, insight, artifact shape, execution beats, why it
  could win, risks, and next step.
- Do not ask Kenji to judge an internal option sheet. Make the first screen
  customer-facing: what are we making, what bigger problem does it solve, why
  should he care, and what exact taste decision should he make?
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
- Do not record phantom worker ids. If the worker is not app-visible by id or a
  searchable title, mark the ticket blocked and do not claim Telegram routing.
- Do not let waiting feedback become silent. Send a bounded, phone-viewable
  reminder when the configured interval elapses, or record a visible blocker.
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
- `docs/features/FEAT-0064-skill-signals.md` - official signal contract and
  component source ownership.
- `farplane/automations.md` - reviewed automation prompt source.
- [templates/taste-proposal.md](templates/taste-proposal.md) - planning
  proposal template and phone-friendly digest shape.
