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
`farplane/products.md`, and `docs/specs/skill-compounding-score.md`.
Read the active-hours config from the rendered Codex config or environment:

```text
FARPLANE_TASTE_LOOP_ENABLED
FARPLANE_TASTE_LOOP_TIMEZONE
FARPLANE_TASTE_LOOP_ACTIVE_DAYS
FARPLANE_TASTE_LOOP_ACTIVE_START
FARPLANE_TASTE_LOOP_ACTIVE_END
FARPLANE_TASTE_LOOP_TOP_N
FARPLANE_TASTE_LOOP_MAX_ACTIONS_PER_BEAT
FARPLANE_TASTE_LOOP_MAX_OPEN_FEEDBACK
FARPLANE_TASTE_LOOP_TARGET_GROUPS
FARPLANE_TASTE_LOOP_OUTPUT_CHANNELS
FARPLANE_TASTE_LOOP_COOLDOWN_HOURS
FARPLANE_TASTE_LOOP_CONVERGENCE_WINDOW
FARPLANE_TASTE_LOOP_MINIMUM_DELTA
```

If config is missing, use the defaults documented in `config.toml.example` and
record that fallback in the report.

## Gate

Stop with a visible no-op report when any hard gate fails:

- disabled
- outside active days or active hours
- unique open feedback count is at or above the cap
- Taste Loop Artifact Workflows are missing from `farplane/products.md`
- no candidate workflow can create or hand off a reviewable artifact

## Select

Read:

- `docs/specs/skill-compounding-score.md`
- `docs/skills/registry.jsonl`
- `farplane/products.md`
- `docs/farplane-framework/lifecycle.md`
- generated skill graph heat when available, using `FARPLANE_SKILL_HEAT_*`
  config as the heat-window owner
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
`FARPLANE_TASTE_LOOP_MAX_OPEN_FEEDBACK`. Duplicate open rows for the same key
are `duplicate_open_feedback` hygiene findings and do not consume additional
budget. List duplicates in the report with their canonical target/question.

Select the top `FARPLANE_TASTE_LOOP_TOP_N` artifact workflows with the official
Skill Compounding Score plus the Taste Loop artifact gate. Keep this distinct
from eval score or review TAS:

- tier leverage from `docs/skills/registry.jsonl`
- lifecycle-reference fit from `docs/farplane-framework/lifecycle.md` and graph
  distance when available
- product-lane fit from `farplane/products.md`
- observed heat from existing skill graph signals
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

Take at most `FARPLANE_TASTE_LOOP_MAX_ACTIONS_PER_BEAT` action. Default to one.

Use:

- `artifact_feedback` through `optimize-with-human` only after a reviewable
  artifact exists at `artifact_ref`.
- `artifact_goal_handoff` through `goal-advisor` when native Goal mode should
  generate the artifact in a bounded continuation.
- `blocked_report` when proof, config, product-lane ownership, artifact
  ownership, metric provider, or generation feasibility is unclear.

Do not ask for feedback on a skill summary, skill README, or broad skill target.
Do not create a feedback card without `artifact_ref`. Do not edit target skills
directly from this heartbeat. Do not create a local runner, hidden daemon,
unbounded queue, external mutation, deploy, publish, spend, or legacy
autoresearch session by default.

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
`FARPLANE_TASTE_LOOP_MINIMUM_DELTA` across
`FARPLANE_TASTE_LOOP_CONVERGENCE_WINDOW` comparable runs.

## Write

Write a Markdown report under:

```text
.farplane/reports/taste-loop/<YYYY-MM-DDTHHMMSS>.md
```

When an action is emitted, also write a small artifact under:

```text
.farplane/automation/taste-loop/artifacts/
.farplane/automation/taste-loop/feedback/
```

Use Markdown for human review. A feedback artifact must point to the generated
artifact path, screenshot, preview, or URL. Keep feedback questions short enough
to answer from Telegram or a compact Farplane UI card.

## Final Output

Return:

- status: `no_op`, `artifact_feedback`, `artifact_goal_handoff`, or `blocked`
- report path
- selected product lane, artifact workflow, score breakdown, and metric provider
- artifact ref, if generated or handed off
- action artifact path, if any
- skipped target reasons
- unique open feedback count and duplicate open feedback count
- next trigger expectation
