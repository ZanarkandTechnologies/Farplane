---
kind: codex-heartbeat-prompt
skill: taste-loop
version: 0.1.0
---

# Farplane Active-Hours Taste Loop

Run one Codex-native taste-loop heartbeat for:

```text
project_root = "{{PROJECT_ROOT}}"
```

## Load

Read the project-local `AGENTS.md`, then load `skills/taste-loop/SKILL.md`,
`farplane/automations.md`, `farplane/products.md`, and
`docs/features/FEAT-0064-skill-signals.md`.

Extract the marker-delimited TOML config block and prompt block for
`farplane-active-hours-taste-loop` from `farplane/automations.md`. Use the
TOML `[schedule]` block as the desired Codex automation schedule. Use the
prompt block's `Params` section as the Taste Loop runtime knobs. The live Codex
automation record owns cadence. Once this prompt is invoked, run one bounded
beat; do not perform a second active-hours check inside the skill.

Read the Codex automation memory when available. Treat that memory as the
controller ledger for active Taste Loop workers. Do not create or consult a
separate `workers.jsonl`.

Load the default fixed scenario when no live product context is explicitly
better:

```text
tickets/TASK-0237/artifacts/agi-toy-shop-scenario.md
```

## Gate

Stop with a side-effect-free no-op when any hard gate fails:

- disabled
- valid unique open feedback count is at or above the cap
- Taste Loop Artifact Workflows are missing from `farplane/products.md`
- no candidate workflow can create or hand off a reviewable artifact
- no candidate workflow can create or hand off a reviewable planning artifact
  such as a TasteProposal

For ordinary no-op beats, do not create worker threads, tickets, artifacts,
feedback cards, Telegram messages, or `.farplane/reports/taste-loop/` files.
Only write a no-op report when `log_noop = true`; otherwise the
automation run and memory surface are enough.

Before scoring candidates, inspect controller memory. If it contains an
`active`, `waiting_for_feedback`, or `revising` worker, resume, inspect, or
block that worker in this beat instead of creating a new worker.

If the active worker is waiting for feedback, first verify that its
`worker_thread_ref` is discoverable in the Codex app thread list or by its
searchable title. If the worker cannot be found, write a blocked report and
update the ticket/progress; do not claim it is waiting and do not create another
replacement worker with an unverified id.

If the visible worker is waiting for feedback and the configured reminder
interval has elapsed, send exactly one phone-viewable reminder from that worker
thread using `telegram-message`. The reminder must first label the review
object with `Review artifact`, `Skill/workflow`, `Product`, `Stage`, and
`Not judging`, then include the proposal or artifact summary and the one reply
action inside Telegram itself. Prefer simple Telegram Markdown for controlled
Taste Loop feedback/reminder bodies; use raw text only when the body contains
arbitrary code, JSON, dense paths, or generated text that could break Markdown
parsing. Record `last_reminder_at`, `reminder_count`, and send/fallback status
in `progress.md` and automation memory, then stop the beat.

When no active worker is present, reuse an existing active ticket and Goal
Packet for the same `product_lane + workflow_id` before creating a new ticket.
Taste Loop tickets are workflow containers: append timestamped hypothesis
cycles to the same `progress.md` until that workflow reaches `complete`,
`blocked`, `discarded`, `closed`, `budget_exhausted`, or explicit operator
closeout. `revise`, `reject`, no-reply, and reminder states are not terminal.
When a ticket declares `progress_unit = hypothesis_cycle`, run
`python3 skills/taste-loop/scripts/check_progress_hypothesis_cycles.py
<program.md> <progress.md>` before recording a waiting or terminal state. If it
fails, update the ticket/progress with a blocker instead of sending another
feedback request.

## Select

Read:

- `docs/features/FEAT-0064-skill-signals.md`
- `docs/skills/registry.jsonl`
- `farplane/products.md`
- `docs/farplane-framework/lifecycle.md`
- generated skill graph heat when available, using `FARPLANE_SKILL_HEAT_*`
  config as the heat-window owner
- Codex automation memory for active worker, last request, last feedback, and
  next action state
- recent `.farplane/reports/taste-loop/` reports when present
- existing `.farplane/automation/taste-loop/` feedback or handoff artifacts

Build candidates from `farplane/products.md` Taste Loop Artifact Workflows.
Each candidate must include:

```text
product_lane:
workflow_id:
owner:
planning_artifact:
execution_artifact:
feedback_question:
```

Do not select broad router skills as direct targets. `frontend-craft`,
`functional-ui`, `remotion`, `remotion-render`, `goal-advisor`,
`self-improve`, and `skill-maintenance` may support a workflow, but Kenji
should not be asked to review those skills or their summaries.

Normalize open feedback before gating:

```text
feedback_key = target_id + "\n" + feedback_question
```

Count one open card per key toward
`max_open_feedback` only when the card is valid product-workflow feedback:

- idea feedback requires `workflow_id`, `product_lane`, and `proposal_ref` or
  `concept_ref`;
- execution feedback requires `workflow_id`, `product_lane`, and `artifact_ref`.

Duplicate open rows for the same key are `duplicate_open_feedback` hygiene
findings and do not consume additional budget. Legacy broad-skill/router cards
that target `frontend-craft`, `functional-ui`, `remotion`, `remotion-render`,
`goal-advisor`, `self-improve`, or `skill-maintenance` are
`legacy_invalid_feedback` hygiene findings and do not consume budget. List
duplicates and invalid legacy cards in the report with their canonical
target/question.

Select the top `top_n` artifact workflows with the FEAT-0064 skill signal
contract plus the Taste Loop artifact gate. Keep this distinct from eval score
or review TAS.

Use only these durable skill signals:

- `direct_heat`: observed direct usage or invocation evidence.
- `composition_heat`: weaker indirect usefulness from deduped incoming refs
  from recently used skills.
- `maintenance_burden`: stale template, first-load bloat, missing eval or QA,
  unclear owner, generated-output drift, or repeated source gaps.
- `uniqueness`: distinct trigger, workflow, proof surface, or user-facing
  capability that would be lost if the skill were merged or retired.

Then apply the Taste-specific artifact gate:

- `product_lane_fit`: the workflow belongs to a product lane in
  `farplane/products.md`.
- `artifact_workflow_fit`: the workflow can produce or hand off a reviewable
  artifact end-to-end.
- `planning_artifact_fit`: the planning artifact is concrete enough to request
  human feedback.
- penalties: cooldown, valid open feedback, ambiguity, fake-metric risk, and
  convergence without useful new output.

Expose signals and recommendation in the report:

```text
Product lane:
Workflow:
Owner:
Planning artifact:
Execution artifact:
Route:
Signals:
  direct_heat:
  composition_heat:
  maintenance_burden:
  uniqueness:
Taste gate:
  product_lane_fit:
  artifact_workflow_fit:
  planning_artifact_fit:
Penalties:
Recommendation: keep | harden | refine | merge | watch | retire_review
Decision:
Evidence refs:
```

## Act

Take at most `max_actions_per_beat` action. Default to one.

Use:

- `artifact_worker_thread` for normal human-feedback artifact workflows. Create
  or reuse a ticket-backed Goal Packet first, then create or reuse a dedicated
  Codex worker thread. Reuse or resume the active worker from automation memory
  before considering any new worker. The worker prompt must tell that thread to
  log a planning experiment, generate TasteProposal planning artifacts, and
  then use `$optimize-with-human` with `feedback_channel=telegram` and
  `phases=planning,execution`.
- `idea_feedback` when the worker can produce TasteProposal artifacts now but
  should wait for planning approval before full execution.
- `artifact_feedback` through `optimize-with-human` only when an existing worker
  thread already owns the Telegram reply path or the artifact is intentionally
  local/manual.
- `artifact_goal_handoff` through `goal-advisor` when native Goal mode should
  generate the artifact in a bounded continuation.
- `blocked_report` when proof, config, product-lane ownership, artifact
  ownership, metric provider, or generation feasibility is unclear.

Do not ask for feedback on a skill summary, skill README, or broad skill target.
Do not create a feedback card without `proposal_ref`, `concept_ref`, or
`artifact_ref`. Do not edit target skills directly from this heartbeat or from
a first rejection. Do not send Telegram feedback from the parent heartbeat
thread when Kenji's reply needs to resume the worker. Do not create a local runner, hidden daemon,
unbounded queue, external mutation, deploy, publish, spend, or legacy
autoresearch session by default.

Before creating a benchmark, harder task suite, or Goal handoff, derive a
compact proof card:

```text
Objective:
Provider:
Primary signal:
Guardrails:
Anti-signals:
Minimum meaningful delta:
Measurement method:
Route hint:
```

Use an existing target-skill eval or benchmark when it exists. Create harder
tasks only when the metric provider is `eval` or `agent_qa` and `self-improve`
can define a baseline, rubric, and promotion rule. When the honest signal is
human taste, use `optimize-with-human` and do not fake a benchmark.

Use phase metrics, not fake taste benchmarks:

```text
idea_pass_rate = planning approvals / planning attempts
execution_pass_rate = execution approvals / execution attempts
```

Convergence means comparable-run convergence: hold or stop when recent
score/review/feedback deltas remain below
`minimum_delta` across `convergence_window` comparable runs.

## Write

Write a Markdown report under:

```text
.farplane/reports/taste-loop/<YYYY-MM-DDTHHMMSS>.md
```

Write this report only when an action, blocker, diagnostic, or configured
no-op log is emitted. When an action is emitted, also write a small artifact
under:

```text
tickets/TASK-*/ticket.md
tickets/TASK-*/program.md
tickets/TASK-*/progress.md
tickets/TASK-0237/artifacts/agi-toy-shop-scenario.md
.farplane/automation/taste-loop/artifacts/
.farplane/automation/taste-loop/feedback/
.farplane/automation/taste-loop/preview/
```

For `artifact_worker_thread`, find and reuse the active ticket Goal Packet for
the same `product_lane + workflow_id`; create a new ticket only when no active
workflow ticket exists or the prior ticket is terminal. Write or update that
Goal Packet before creating the Codex thread. The worker thread prompt must
include:

```text
Files:
- tickets/TASK-XXXX/ticket.md
- tickets/TASK-XXXX/program.md
- tickets/TASK-XXXX/progress.md
- tickets/TASK-0237/artifacts/agi-toy-shop-scenario.md when no live scenario is supplied

Task:
Use $<artifact-owner> to run a Goal-backed phase-aware founder loop for
<workflow_id>. Start with the planning phase. Log a hypothesis cycle in
progress.md, use AGI Toy Shop as the fixed default scenario unless live context
is supplied, generate one to three TasteProposal artifacts using
skills/taste-loop/templates/taste-proposal.md, then use $optimize-with-human
with target=<workflow_id>, objective=<founder conviction that the bet is worth
making/selling/testing>, channel=telegram,
feedback_policy=ask_when_artifact_ready, phases=planning,execution, and
founder_lens=true. Each TasteProposal must include customer/buyer, problem,
wedge, offer/artifact, distribution angle, validation question, next bet if
approved, pivot trigger if rejected, taste insight, artifact shape, core angle,
5+ execution beats, why it could win, cringe risks, references or taste pack,
feedback question, and next step. Before the options, frame the
Telegram-facing proposal like a founder/customer pitch: what we are trying to
make, the bigger problem, the proposed solution, why the idea should feel
desirable, what distribution or buyer reaction it is trying to earn, and
exactly what founder decision Kenji is making. Do not send an internal planning
table as the primary review surface. When Kenji approves a proposal, freeze
the approved brief, append an execution hypothesis cycle in progress.md, and
execute the artifact. When Kenji replies in this thread, append feedback,
learning, and the next hypothesis to progress.md and continue the right phase
in the same workflow ticket. If Kenji replies with
revise or reject, restate the clarified review object, then either ask for the
next instruction or send the next revised review request. Do not stop after
only acknowledging the feedback, and do not create a fresh TL ticket for a
non-terminal revision or a fresh named TL-EXP item for each update. Stop only
on keep/approve/convergence/budget/blocker.
```

After the thread is created or found, record `worker_thread_ref` in the ticket,
`progress.md`, the Taste Loop report when one is written, and the Codex
automation memory. Set the thread title to a searchable name when the tool is
available:

```text
Taste Loop Worker: TASK-XXXX <workflow_id>
```

Do not write `waiting_for_feedback` until the worker thread is visible by id or
title, the Telegram send or fallback proof is recorded, and the hypothesis
cycle validator passes when `program.md` opts into `progress_unit =
hypothesis_cycle`.

Automation memory row shape:

```text
active_worker:
  workflow_id:
  product_lane:
  ticket_key:
  ticket_ref:
  worker_thread_ref:
  status: planning | waiting_for_idea_feedback | execution |
    waiting_for_execution_feedback | blocked | complete
  approved_brief_ref:
  proposal_ref:
  concept_ref:
  artifact_ref:
  preview_ref:
  idea_pass_rate:
  execution_pass_rate:
  last_request_at:
  last_reminder_at:
  reminder_count:
  last_feedback_at:
  next_action:
```

Use Markdown for human review. A planning feedback artifact must point to a
TasteProposal or only use a hook/concept card when the artifact itself is just a
hook. An execution feedback artifact must point to the generated
artifact path, screenshot, preview, or URL. For website, image, video, or other
visual artifacts, also create a preview wrapper or manifest under
`.farplane/automation/taste-loop/preview/` and include a `preview_ref` in the
feedback card and report. Localhost previews are smoke-test evidence only; do
not send phone-facing Telegram feedback with only a localhost URL. Prefer a
public/mobile-viewable URL, attached screenshot, or Farplane UI-ready preview
fallback. Keep feedback questions short enough to answer from Telegram or a
compact Farplane UI card.

Hypothesis cycle row shape for worker `progress.md`:

```text
hypothesis_cycle:
  phase: planning | execution
  scenario: AGI Toy Shop | live_context
  current_hypothesis:
  planned_attempt:
  artifact_refs:
  human_question:
  expected_signal:
  skill_delta_candidate:
  human_signal:
  learning:
  next_hypothesis:
  promotion_decision: keep_local | rerun | harden_skill | discard
```

Do not promote skill edits from one rejection. Use `harden_skill` only after
repeated same-phase failure or a reusable operator-approved pattern.

## Final Output

Return:

- status: `no_op`, `artifact_worker_thread`, `artifact_feedback`,
  `idea_feedback`, `feedback_reminder`, `artifact_goal_handoff`, or `blocked`
- report path
- selected product lane, artifact workflow, skill signals, recommendation, and proof provider
- worker ticket ref and worker thread ref, if created or reused
- artifact ref, if generated or handed off
- concept ref, if planning feedback was requested
- idea pass rate and execution pass rate when known
- preview ref or deploy URL for visual artifacts
- reminder status if a waiting feedback item was nudged or blocked
- action artifact path, if any
- skipped target reasons
- unique open feedback count and duplicate open feedback count
- legacy invalid feedback count
- next trigger expectation
