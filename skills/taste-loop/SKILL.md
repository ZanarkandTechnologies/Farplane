---
name: taste-loop
version: 0.1.0
description: "Run a Codex-native active-hours heartbeat prompt that selects high-compounding skills and emits feedback cards or Goal handoffs."
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
structured skill or product improvement signals through the official optional
Codex automation heartbeat. The heartbeat prompt selects the top compounding
targets with the official Skill Compounding Score; gates on active hours and
feedback budget; then emits one bounded action per beat: no-op, feedback card,
Goal Advisor handoff, or blocked report.

This skill is a prompt owner, not a script, scheduler, hidden daemon, or
alternate continuation runtime. Codex automation records own cadence; native
Goal mode owns uninterrupted improvement turns; `goal-advisor` compiles Goal
Packets; `metric-advisor` chooses the honest provider; `optimize-with-human`
owns human-feedback protocol; `self-improve` owns target-skill experiment
memory.

## Skill Signature

```text
taste_loop(project_root, config?, now?)
  -> no_op | feedback_card_report | goal_handoff_report | blocked_report
state: reads(config env, farplane/products.md, docs/skills/registry.jsonl,
             docs/specs/skill-compounding-score.md,
             skill graph heat / FARPLANE_SKILL_HEAT_*,
             .farplane/automation/taste-loop/*?);
       writes(.farplane/reports/taste-loop/*.md,
              .farplane/automation/taste-loop/*.md?)
gates: active_hours_checked; feedback_budget_checked; top_n_selected;
       output_artifact_visible; no_hidden_scheduler
routes: metric-advisor | optimize-with-human | self-improve | goal-advisor |
  review
fails: creates a local runner as the primary surface; runs hidden loops;
  bypasses human feedback; routes to retired autoresearch by default; spams
  more feedback than budget allows
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
  - [ ] Read `farplane/products.md` Work Lanes.
  - [ ] Use existing skill heat generated from `.farplane/events/` and
    `FARPLANE_SKILL_HEAT_*` controls when available.
  - [ ] Prefer configured target groups and known product/money-making skills.
  - [ ] Include existing open feedback and cooldown state.
- [ ] 3. Score and select top N.
  - [ ] Use the Skill Compounding Score; expose every component in the report.
  - [ ] Keep the score distinct from eval score, review TAS, and human
    preference labels.
  - [ ] Penalize open feedback, cooldown, ambiguous targets, and fake metric
    risk.
- [ ] 4. Route exactly one Codex-native bounded action by default.
  - [ ] Ask `metric-advisor` for an honest provider before creating benchmarks,
    harder task suites, or Goal handoffs.
  - [ ] Use `feedback_card` through `optimize-with-human` when human taste is
    the honest next metric.
  - [ ] Use `goal_handoff` with `self-improve` context when a bounded
    skill-improvement Goal should run in native Goal mode.
  - [ ] Use `blocked_report` when the target lacks proof or config.
  - [ ] Do not route to legacy autoresearch unless explicitly configured later.
- [ ] 5. Write visible state, not hidden runtime output.
  - [ ] Write a Markdown report under `.farplane/reports/taste-loop/`.
  - [ ] Write or update feedback-card and Goal-handoff Markdown artifacts
    under `.farplane/automation/taste-loop/` when useful.
  - [ ] Keep generated feedback questions short and decision-shaped.
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
`docs/specs/skill-compounding-score.md` and expose a readable score breakdown
rather than hiding a magic ranking:

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
- feedback budget and cooldown: `.farplane/automation/taste-loop/`
- metric route: `metric-advisor`

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

- `status`: `no_op`, `feedback_card`, `goal_handoff`, or `blocked`
- `report_path`
- `selected_targets`
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
- Do not let open feedback pile up. Respect `MAX_OPEN_FEEDBACK`.
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
