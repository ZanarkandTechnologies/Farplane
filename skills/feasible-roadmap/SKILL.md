---
name: feasible-roadmap
description: "Turn a goal, current state, constraints, and horizon into a feasible phased roadmap, milestones, risks, and immediate next move."
tier: 2
source: local
capability:
  kind: shortcut
template_uses:
  skill-template: "0.4.1"
  skill-eval-task: "0.2.0"
eval: evals/evals.json
allowed-tools: Read, Glob, Grep
---

# Feasible Roadmap

## Context

Use this direct operator shortcut when a goal needs an honest path from the
current state to a stated horizon. It produces enough phases, milestones, and
risks to make progress legible—not a ticket program, staffing plan, or a
fictional precise forecast.

Respect supplied constraints, evidence, and capacity. When a pivotal fact is
unknown, label the assumption and give the cheapest check that would revise the
roadmap. Do not mutate tasks, calendars, portfolios, or external systems.

## Skill Signature

```text
feasible_roadmap(goal, constraints?, current_state?, horizon?) -> phased_roadmap

state: reads(supplied goal, evidence, constraints, and horizon); writes(response
  or caller-owned roadmap); never mutates external state
owns: phased_roadmap
gates: destination_named; current_state_honest; phases_ordered;
  milestones_observable; assumptions_visible; immediate_move_direct
routes: direct-action | implementation planning | interval update
fails: fabricated certainty; calendar theater; task-dump; ticket-program;
  skipping the first proof
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. State the goal, horizon, current state, and hard constraints.
  - Separate observed facts from assumptions. Ask only the one question that
    would materially change the sequence; otherwise provide a marked
    provisional path.
- [ ] 2. Define the smallest credible proof of progress.
  - Prefer an observed customer result, shipped core workflow, paid commitment,
    or other completed loop over preparation or output volume alone.
- [ ] 3. Build three to five ordered phases.
  - Give each phase a purpose, an observable exit milestone, its main risk, and
    the dependency that makes the next phase feasible.
  - Use ranges or conditions for timing when evidence does not support dates.
- [ ] 4. Name the gating risks and cheap evidence checks.
  - Include only risks that can alter sequence, scope, or viability; do not add
    generic caution.
- [ ] 5. End with one immediate move.
  - It must advance the first phase directly. Route software implementation
    planning only after the roadmap identifies the slice.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

```text
Goal and horizon
Current state and constraints

Phase 1 — <purpose>
  Exit milestone: <observable result>
  Main risk / evidence check: <risk -> cheapest check>

Phase 2 — ...
Phase 3 — ...

Assumptions that could change the roadmap
Immediate next move
```

## Gotchas

- Do not turn a personal or strategic roadmap into a fake engineering plan.
- Do not promise dates, capacity, or outcomes not supported by the input.
- Do not list tasks without explaining their phase exit condition.
- Do not replace a first proof with strategy work, infrastructure, or a polished
  portfolio artifact.
