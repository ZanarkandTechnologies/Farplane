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
table, creates or reuses a dedicated worker Goal Packet and Codex thread, and
instructs that worker to generate reviewable artifacts through
`optimize-with-human`.

This skill is a prompt owner, not a script, scheduler, hidden daemon, or
alternate continuation runtime. Codex automation records own cadence; product
lanes own what outputs matter; persistent Codex threads own Telegram reply
routing; worker Goal Packets own durable state; `goal-advisor` compiles the
packet; `metric-advisor` chooses the honest provider; `optimize-with-human`
owns the worker's human-feedback protocol; artifact-producing skills own
end-to-end generation.

## Skill Signature

```text
taste_loop(project_root, config?, now?)
  -> no_op | artifact_worker_thread_report | artifact_feedback_report |
     artifact_goal_handoff_report | blocked_report
state: reads(config env, farplane/products.md,
             farplane/products.md#taste-loop-artifact-workflows,
             docs/skills/registry.jsonl,
             docs/specs/skill-compounding-score.md,
             tickets/*/ticket.md?,
             skill graph heat / FARPLANE_SKILL_HEAT_*,
             .farplane/automation/taste-loop/*?);
       writes(.farplane/reports/taste-loop/*.md,
              tickets/TASK-*/ticket.md?,
              tickets/TASK-*/program.md?,
              tickets/TASK-*/progress.md?,
              .farplane/automation/taste-loop/artifacts/*,
              .farplane/automation/taste-loop/feedback/*?,
              .farplane/automation/taste-loop/preview/*?)
gates: active_hours_checked; feedback_budget_checked; product_lane_selected;
       artifact_workflow_selected; worker_packet_created_or_reused;
       worker_thread_created_or_reused; optimize_with_human_bound_in_worker;
       artifact_generated_or_goal_handoff; artifact_ref_visible;
       preview_ref_visible_for_visual_artifacts; open_feedback_deduped;
       no_hidden_scheduler
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
  dedicated worker thread is needed; spams more feedback than budget allows
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
  - [ ] Prefer `artifact_worker_thread` for human-feedback product artifacts:
    create or reuse a ticket-backed Goal Packet, then create or reuse a
    dedicated Codex worker thread whose prompt tells the worker to use
    `optimize-with-human`.
  - [ ] Generate a small artifact immediately when the owning artifact skill can
    do so inside the worker thread without hidden continuation.
  - [ ] Use `artifact_goal_handoff` when native Goal mode should generate the
    artifact in a bounded continuation.
  - [ ] Use direct `artifact_feedback_report` through `optimize-with-human` only
    when an existing worker thread already owns the reply path or the artifact
    is intentionally local/manual.
  - [ ] Use `blocked_report` when the target lacks product-lane ownership,
    artifact workflow ownership, proof, config, or generation feasibility.
  - [ ] Do not route to legacy autoresearch unless explicitly configured later.
- [ ] 5. Write visible state, not hidden runtime output.
  - [ ] Write a Markdown report under `.farplane/reports/taste-loop/`.
  - [ ] For `artifact_worker_thread`, write or update `ticket.md`, `program.md`,
    and `progress.md` under `tickets/TASK-*`, and record the worker thread id
    in the ticket links, progress log, and Taste Loop report.
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

## Worker Thread Contract

Taste Loop's default human-feedback action is a worker handoff:

```text
artifact_worker_thread(product_lane, workflow_id, owner, feedback_question)
  -> ticket_ref + program_ref + progress_ref + worker_thread_ref + report_ref
```

The parent heartbeat selects and dispatches. It does not own artifact iteration.
The worker thread prompt must name the Goal Packet files inline and instruct the
worker to use `optimize-with-human` after creating a reviewable artifact.

Required worker prompt shape:

```text
Files:
- tickets/TASK-XXXX/ticket.md
- tickets/TASK-XXXX/program.md
- tickets/TASK-XXXX/progress.md

Task:
Use $<artifact-owner> to generate one reviewable artifact for the selected
workflow. Then use $optimize-with-human with target=<workflow>, objective=<what
should improve>, channel=telegram, and feedback_policy=ask_when_artifact_ready.
When Kenji replies in this thread, append the feedback to progress.md and
produce the next revision. Stop only on keep/approve/convergence/budget/blocker.
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

- `status`: `no_op`, `artifact_worker_thread`, `artifact_feedback`,
  `artifact_goal_handoff`, or `blocked`
- `report_path`
- `selected_product_lane`
- `selected_artifact_workflow`
- `worker_ticket_ref`
- `worker_thread_ref`
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
- Do not create `feedback_card` without `artifact_ref`.
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
