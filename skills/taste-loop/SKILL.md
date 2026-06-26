---
name: taste-loop
version: 0.1.0
description: "Run a Codex-native active-hours heartbeat prompt that creates product-lane artifacts and asks for human taste feedback."
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
automation heartbeat. The heartbeat prompt reads `farplane/products.md`, selects
one high-compounding artifact workflow from the Taste Loop Artifact Workflows
table, generates or hands off one reviewable artifact, and asks for a compact
human taste judgment on that artifact.

This skill is a prompt owner, not a script, scheduler, hidden daemon, or
alternate continuation runtime. Codex automation records own cadence; product
lanes own what outputs matter; native Goal mode owns uninterrupted artifact
generation turns; `goal-advisor` compiles Goal Packets; `metric-advisor`
chooses the honest provider; `optimize-with-human` owns human-feedback
protocol; artifact-producing skills own end-to-end generation.

## Skill Signature

```text
taste_loop(project_root, config?, now?)
  -> no_op | artifact_feedback_report | artifact_goal_handoff_report |
     blocked_report
state: reads(config env, farplane/products.md,
             farplane/products.md#taste-loop-artifact-workflows,
             docs/skills/registry.jsonl,
             docs/specs/skill-compounding-score.md,
             skill graph heat / FARPLANE_SKILL_HEAT_*,
             .farplane/automation/taste-loop/*?);
       writes(.farplane/reports/taste-loop/*.md,
              .farplane/automation/taste-loop/artifacts/*,
              .farplane/automation/taste-loop/feedback/*?,
              .farplane/automation/taste-loop/preview/*?)
gates: active_hours_checked; feedback_budget_checked; product_lane_selected;
       artifact_workflow_selected; artifact_generated_or_goal_handoff;
       artifact_ref_visible; preview_ref_visible_for_visual_artifacts;
       open_feedback_deduped; no_hidden_scheduler
routes: landing-page | social-content | video-production |
  product-photography | farplane-evidence-content |
  farplane-experiment-report | farplane-ablation-proof |
  farplane-productization | optimize-with-human | goal-advisor | review
fails: creates a local runner as the primary surface; runs hidden loops;
  asks for feedback on a skill summary; selects broad router skills as direct
  targets; creates a feedback card without an artifact; optimizes generic skill
  quality instead of a products.md output; routes to retired autoresearch by
  default; spams more feedback than budget allows
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Load active-hours and budget config in the Codex heartbeat turn.
  - [ ] Read `FARPLANE_TASTE_LOOP_*` values from the rendered Codex config or
    environment available to the automation.
  - [ ] Stop with a no-op report when disabled or outside active hours.
- [ ] 2. Collect candidate targets.
  - [ ] Read `docs/specs/skill-compounding-score.md`.
  - [ ] Read `docs/skills/registry.jsonl`.
  - [ ] Read `farplane/products.md` Work Lanes and Taste Loop Artifact
    Workflows.
  - [ ] Use existing skill heat generated from `.farplane/events/` and
    `FARPLANE_SKILL_HEAT_*` controls when available.
  - [ ] Prefer artifact workflows tied to configured target groups and
    product/money-making lanes.
  - [ ] Exclude broad router skills as direct targets. `frontend-craft`,
    `functional-ui`, `remotion`, `remotion-render`, `goal-advisor`,
    `self-improve`, and `skill-maintenance` can support a workflow but should
    not be the thing Kenji is asked to judge.
  - [ ] Include existing open feedback and cooldown state.
  - [ ] Normalize open feedback by `target_id + feedback_question` before
    applying the budget gate; duplicate open rows are hygiene findings, not
    extra budget usage.
- [ ] 3. Score and select top N.
  - [ ] Use the Skill Compounding Score; expose every component in the report.
  - [ ] Keep the score distinct from eval score, review TAS, and human
    preference labels.
  - [ ] Require `artifact_workflow_fit`: the candidate can create or hand off a
    reviewable artifact end-to-end from `products.md`.
  - [ ] Penalize unique open feedback, cooldown, ambiguous targets, and fake
    metric risk.
- [ ] 4. Route exactly one Codex-native bounded action by default.
  - [ ] Ask `metric-advisor` for an honest provider before creating benchmarks,
    harder task suites, or Goal handoffs.
  - [ ] Generate a small artifact immediately when the owning artifact skill can
    do so inside one heartbeat without hidden continuation.
  - [ ] Use `artifact_goal_handoff` when native Goal mode should generate the
    artifact in a bounded continuation.
  - [ ] Use `artifact_feedback_report` through `optimize-with-human` only after
    an artifact path, preview, screenshot, or URL exists.
  - [ ] Use `blocked_report` when the target lacks product-lane ownership,
    artifact workflow ownership, proof, config, or generation feasibility.
  - [ ] Do not route to legacy autoresearch unless explicitly configured later.
- [ ] 5. Write visible state, not hidden runtime output.
  - [ ] Write a Markdown report under `.farplane/reports/taste-loop/`.
  - [ ] Write generated artifacts under
    `.farplane/automation/taste-loop/artifacts/`.
  - [ ] Write feedback-card and Goal-handoff Markdown artifacts under
    `.farplane/automation/taste-loop/feedback/` when useful.
  - [ ] For website, image, video, or other visual artifacts, also write a
    preview wrapper or manifest under `.farplane/automation/taste-loop/preview/`
    so Kenji can open a single URL or Farplane UI-ready file without hunting
    through reports.
  - [ ] Feedback cards must include `artifact_ref`; if no artifact was produced
    or handed off, write `blocked_report` instead of a feedback card.
  - [ ] Keep generated feedback questions short and decision-shaped.
  - [ ] When duplicate open feedback exists, report the canonical card and
    duplicate rows; do not create another duplicate for that target/question.
- [ ] 6. Stop cleanly.
  - [ ] Report the action, skipped targets, report path, and next trigger.
  - [ ] Do not edit target skills directly from this heartbeat.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Config

The install template provides non-secret defaults:

```text
FARPLANE_TASTE_LOOP_ENABLED=1
FARPLANE_TASTE_LOOP_TIMEZONE=Asia/Kuala_Lumpur
FARPLANE_TASTE_LOOP_ACTIVE_DAYS=Mon,Tue,Wed,Thu,Fri
FARPLANE_TASTE_LOOP_ACTIVE_START=10:00
FARPLANE_TASTE_LOOP_ACTIVE_END=18:00
FARPLANE_TASTE_LOOP_TOP_N=3
FARPLANE_TASTE_LOOP_MAX_ACTIONS_PER_BEAT=1
FARPLANE_TASTE_LOOP_MAX_OPEN_FEEDBACK=3
FARPLANE_TASTE_LOOP_TARGET_GROUPS=content-social,content-video,frontend,harness,self-improvement
FARPLANE_TASTE_LOOP_OUTPUT_CHANNELS=local_report,telegram_ready,farplane_ui_ready
FARPLANE_TASTE_LOOP_COOLDOWN_HOURS=24
FARPLANE_TASTE_LOOP_CONVERGENCE_WINDOW=5
FARPLANE_TASTE_LOOP_MINIMUM_DELTA=qualitative_threshold
```

## Heartbeat Prompt

The automation prompt is the runtime surface. Use
[templates/heartbeat-prompt.md](templates/heartbeat-prompt.md) as the reusable
prompt body, and keep `farplane/automations.md` as the project-specific copied
automation record.

## Scoring Contract

The prompt should consume the official Skill Compounding Score from
`docs/specs/skill-compounding-score.md`, then apply the Taste Loop-specific
artifact workflow gate. Expose a readable score breakdown rather than hiding a
magic ranking:

```text
skill_compounding_score(skill, project_state, lifecycle_refs, now?)
  -> ranked_target_score + score_breakdown + route_hint
```

Signal ownership:

- algorithm and component meanings: `docs/specs/skill-compounding-score.md`
- tier, group, description, links: `docs/skills/registry.jsonl`
- lifecycle-reference distance: `docs/farplane-framework/lifecycle.md` and
  lifecycle graph data when available
- heat: generated skill graph heat from `.farplane/events/` and
  `FARPLANE_SKILL_HEAT_*`
- product lane: `farplane/products.md`
- artifact workflow fit: `farplane/products.md` Taste Loop Artifact Workflows
- feedback budget and cooldown: `.farplane/automation/taste-loop/`
- metric route: `metric-advisor`

Taste Loop may use broad skills as support routes, but the selected target is
always:

```text
product_lane + workflow_id + owner + artifact_ref
```

`feedback_card` is invalid without `artifact_ref`.

## Feedback Budget

Open feedback budget is based on unique active requests, not raw JSONL rows.
Normalize each open feedback row by:

```text
feedback_key = target_id + "\n" + feedback_question
```

Only one open row for a key counts toward
`FARPLANE_TASTE_LOOP_MAX_OPEN_FEEDBACK`. Additional open rows with the same key
must be listed in the report as `duplicate_open_feedback` and should not block
new useful work. If the top selected target already has an open canonical card,
skip it with `open_feedback_and_cooldown` and pick the next eligible target
rather than creating another duplicate.

## Benchmark And Convergence

Do not create benchmarks by default. Use an existing target-skill eval or
benchmark when it exists. Create harder tasks only after `metric-advisor`
selects `eval` or `agent_qa` and `self-improve` defines a baseline, rubric, and
promotion rule. When human taste is the honest signal, use
`optimize-with-human` instead of pretending a benchmark exists.

Convergence is comparable-run based: hold or stop when recent score, review, or
feedback deltas stay below `FARPLANE_TASTE_LOOP_MINIMUM_DELTA` across
`FARPLANE_TASTE_LOOP_CONVERGENCE_WINDOW` comparable runs.

## Output

Return and write:

- `status`: `no_op`, `artifact_feedback`, `artifact_goal_handoff`, or
  `blocked`
- `report_path`
- `selected_product_lane`
- `selected_artifact_workflow`
- `artifact_ref`
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
- Do not add a local runner just to make the prompt testable. The behavior is
  reviewed as a prompt contract plus sample artifacts.
- Do not call this a training loop. It creates structured feedback and
  accepted writeback opportunities; it does not train models.
- Do not ask Kenji to review a skill summary, skill README, or generic skill
  quality target. Ask for feedback on an artifact created by a product workflow.
- Do not use broad router skills as direct targets. Pick an artifact workflow
  from `farplane/products.md`; use router skills only as supporting routes.
- Do not create `feedback_card` without `artifact_ref`.
- Do not send website feedback without a browser-viewable `preview_ref`, local
  URL, deploy URL, or Farplane UI-ready preview manifest.
- Do not let open feedback pile up. Respect `MAX_OPEN_FEEDBACK`.
- Do not let duplicate feedback rows consume the open-feedback budget. Count
  unique active requests and report duplicate rows as hygiene.
- Do not optimize by fake numeric taste scores. Use labels, rankings, and
  accept/revise/reject when that is the honest signal.
- Do not invent a second heat, product, or benchmark system. Reuse the skill
  graph, `products.md`, `metric-advisor`, and target skill evals first.

## Reference Map

- [../metric-advisor/SKILL.md](../metric-advisor/SKILL.md) - metric provider
  and route hints.
- [../optimize-with-human/SKILL.md](../optimize-with-human/SKILL.md) -
  feedback protocol and feedback schema.
- [../self-improve/SKILL.md](../self-improve/SKILL.md) - skill memory,
  baselines, candidates, and promotion rules.
- [../goal-advisor/SKILL.md](../goal-advisor/SKILL.md) - Goal Packet and
  heartbeat prompt compilation.
- `docs/specs/skill-compounding-score.md` - official score algorithm and
  component source ownership.
- `farplane/automations.md` - reviewed automation prompt source.
