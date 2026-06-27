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
`docs/features/FEAT-0064-skill-compounding-score.md`.

Extract the marker-delimited TOML config block and prompt block for
`farplane-active-hours-taste-loop` from `farplane/automations.md`. Use the
TOML `[schedule]` block as the desired Codex automation schedule. Use the
prompt block's `Params` section as the Taste Loop runtime knobs. The live Codex
automation schedule is the primary active-hours gate; do not wake hourly just
to check whether active hours are open.

Read the Codex automation memory when available. Treat that memory as the
controller ledger for active Taste Loop workers. Do not create or consult a
separate `workers.jsonl`.

## Gate

Stop with a side-effect-free no-op when any hard gate fails:

- disabled
- manual/off-schedule invocation is clearly outside the configured schedule
- unique open feedback count is at or above the cap
- Taste Loop Artifact Workflows are missing from `farplane/products.md`
- no candidate workflow can create or hand off a reviewable artifact

For ordinary no-op beats, do not create worker threads, tickets, artifacts,
feedback cards, Telegram messages, or `.farplane/reports/taste-loop/` files.
Only write a no-op report when `log_noop = true`; otherwise the
automation run and memory surface are enough.

Before scoring candidates, inspect controller memory. If it contains an
`active`, `waiting_for_feedback`, or `revising` worker, resume, inspect, or
block that worker in this beat instead of creating a new worker.

## Select

Read:

- `docs/features/FEAT-0064-skill-compounding-score.md`
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
reviewable_artifact:
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
`max_open_feedback`. Duplicate open rows for the same key are
`duplicate_open_feedback` hygiene findings and do not consume additional budget.
List duplicates in the report with their canonical target/question.

Select the top `top_n` artifact workflows with the official Skill Compounding
Score plus the Taste Loop artifact gate. Keep this distinct from eval score or
review TAS:

- tier leverage from `docs/skills/registry.jsonl`
- lifecycle-reference fit from `docs/farplane-framework/lifecycle.md` and graph
  distance when available
- product-lane fit from `farplane/products.md`
- observed heat from existing skill graph signals, split into direct heat and
  weaker related heat from recently invoked referring skills
- downstream leverage across skills/routes/graphs
- improvement gap from grounded lessons, troubles, evals, self-improve deltas,
  review findings, or missing proof
- feedback fit and proof fit
- artifact workflow fit from `farplane/products.md`
- cooldown, open-feedback, ambiguity, fake-metric, and convergence penalties

Expose a score breakdown in the report:

```text
Product lane:
Workflow:
Owner:
Reviewable artifact:
Route:
Score:
Components:
  tier_leverage:
  lifecycle_ref_fit:
  product_lane_fit:
  observed_heat_fit:
    direct_heat_fit:
    related_heat_fit:
    top_referring_skills:
  downstream_leverage_fit:
  improvement_gap_fit:
  feedback_fit:
  proof_fit:
  artifact_workflow_fit:
Penalties:
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
  generate the artifact and then use `$optimize-with-human` with
  `feedback_channel=telegram`.
- `artifact_feedback` through `optimize-with-human` only when an existing worker
  thread already owns the Telegram reply path or the artifact is intentionally
  local/manual.
- `artifact_goal_handoff` through `goal-advisor` when native Goal mode should
  generate the artifact in a bounded continuation.
- `blocked_report` when proof, config, product-lane ownership, artifact
  ownership, metric provider, or generation feasibility is unclear.

Do not ask for feedback on a skill summary, skill README, or broad skill target.
Do not create a feedback card without `artifact_ref`. Do not edit target skills
directly from this heartbeat. Do not send Telegram feedback from the parent
heartbeat thread when Kenji's reply needs to resume the worker. Do not create a
local runner, hidden daemon, unbounded queue, external mutation, deploy,
publish, spend, or legacy autoresearch session by default.

Before creating a benchmark, harder task suite, or Goal handoff, derive a
compact metric card:

```text
Objective:
Provider:
Primary metric:
Guard metrics:
Anti-metrics:
Minimum meaningful delta:
Measurement method:
Route hint:
```

Use an existing target-skill eval or benchmark when it exists. Create harder
tasks only when the metric provider is `eval` or `agent_qa` and `self-improve`
can define a baseline, rubric, and promotion rule. When the honest signal is
human taste, use `optimize-with-human` and do not fake a benchmark.

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
.farplane/automation/taste-loop/artifacts/
.farplane/automation/taste-loop/feedback/
.farplane/automation/taste-loop/preview/
```

For `artifact_worker_thread`, write or update the ticket Goal Packet before
creating the Codex thread. The worker thread prompt must include:

```text
Files:
- tickets/TASK-XXXX/ticket.md
- tickets/TASK-XXXX/program.md
- tickets/TASK-XXXX/progress.md

Task:
Use $<artifact-owner> to generate one reviewable artifact for <workflow_id>.
Then use $optimize-with-human with target=<workflow_id>,
objective=<artifact quality objective>, channel=telegram, and
feedback_policy=ask_when_artifact_ready. When Kenji replies in this thread,
append the feedback to progress.md and generate the next revision. Stop only on
keep/approve/convergence/budget/blocker.
```

After the thread is created or found, record `worker_thread_ref` in the ticket,
`progress.md`, the Taste Loop report when one is written, and the Codex
automation memory. Set the thread title to a readable workflow name when the
tool is available.

Automation memory row shape:

```text
active_worker:
  workflow_id:
  product_lane:
  ticket_ref:
  worker_thread_ref:
  status:
  artifact_ref:
  preview_ref:
  last_request_at:
  last_feedback_at:
  next_action:
```

Use Markdown for human review. A feedback artifact must point to the generated
artifact path, screenshot, preview, or URL. For website, image, video, or other
visual artifacts, also create a preview wrapper or manifest under
`.farplane/automation/taste-loop/preview/` and include a `preview_ref` in the
feedback card and report. Localhost previews are smoke-test evidence only; do
not send phone-facing Telegram feedback with only a localhost URL. Prefer a
public/mobile-viewable URL, attached screenshot, or Farplane UI-ready preview
fallback. Keep feedback questions short enough to answer from Telegram or a
compact Farplane UI card.

## Final Output

Return:

- status: `no_op`, `artifact_worker_thread`, `artifact_feedback`,
  `artifact_goal_handoff`, or `blocked`
- report path
- selected product lane, artifact workflow, score breakdown, and metric provider
- worker ticket ref and worker thread ref, if created or reused
- artifact ref, if generated or handed off
- preview ref or deploy URL for visual artifacts
- action artifact path, if any
- skipped target reasons
- unique open feedback count and duplicate open feedback count
- next trigger expectation
