---
kind: goal-program-template
mode: ml_autoresearch
status: active
owner: skills/ml-autoresearch
---

# ML Autoresearch Goal Program Preset

Instantiate this compact preset into the owning campaign ticket's `program.md`
through Goal Advisor. The ticket owns scope and proof; `progress.md` owns
observations; Goal Advisor separately compiles the Files-listed native Goal
launcher.

````markdown
---
kind: goal-program
mode: ml_autoresearch
trigger: native_goal
status: draft
approval: pending
compiled_from_ticket_updated_at: <ticket-updated-at>
generated_prompt: <native-goal-prompt-path>
---

# ML Autoresearch: <campaign>

```yaml
files:
  - <ticket.md>
  - <program.md>
  - <progress.md>
  - <target docs/code>
  - <mutable surface>
  - <frozen evaluator/data contract>

experiment_contract:
  mutable_surface: <exact files or parameters allowed to change>
  frozen_surfaces: <evaluator, data/splits, prohibited inputs, metric>
  baseline: <candidate and full-evaluator receipt>
  simplicity_guard: <tie or complexity rule>

metric:
  provider: <command/evaluator>
  primary: <metric and direction>
  guards: <guard metrics and thresholds>
  anti_metrics: <signals that cannot promote>

selection:
  owner: leverage-advisor
  roadmap:
    objective: <campaign objective>
    candidates: <initial technique frontier or project-local catalog ref>
    first_proof: <baseline-grounded first experiment>
    contingencies: <positive, flat, negative, branch-specific, invalid, and budget branches>
  before_each_experiment:
    inputs:
      - this program.md roadmap
      - progress.md learnings, prior selections, and rejected moves
      - current full-evaluator experiment receipts
      - remaining time, compute, spend, attempt, and patience budget
    output: one next experiment + hypothesis + expected observation +
      observation horizon + confidence + falsifier + surprise trigger +
      changed boundary + rejected alternatives + replan conditions
    rule: invoke leverage-advisor; do not continue a fixed roadmap order

loop:
  baseline: run and record before any mutation
  round:
    - select one experiment through leverage-advisor
    - preregister hypothesis, expected observation, observation horizon,
      confidence, falsifier, surprise trigger, changed boundary, cost, guards,
      and keep/kill rule
    - implement the smallest attributable delta on the mutable surface
    - run correctness smoke
    - when valid, run the exact full frozen evaluator
    - append an immutable receipt and update the learned frontier
    - if the observation materially violates the expectation or is implausibly
      strong, route the receipt through agent-qa-test:experiment before method
      rejection or candidate promotion; the domain executor owns any repair or
      rerun inside the campaign's remaining budget
    - keep | discard | repair_once | defer | failed

after_each_turn:
  - read this roadmap and the complete progress.md tail
  - use leverage-advisor on roadmap + progress learnings + current receipts + remaining budget
  - execute at most one selected experiment
  - append selected move, rejected alternatives, hypothesis, metrics, guards, receipt, learning, cumulative budget, decision, and next action to progress.md
  - continue, replan, block, or complete from the declared rules

drift:
  - stale when ticket scope, mutable/frozen surfaces, data/splits, evaluator, metric, guards, budget, or approval changes
  - regenerate the packet and baseline before continuing after material drift

stop:
  complete: success threshold and guards pass, or no higher-value supported move remains after final verification
  negative: bounded frontier evidence supports no improvement inside the current campaign contract
  blocked: required data/compute/evaluator is unavailable or the packet is stale
  budget: the next faithful experiment would cross a declared ceiling
```

Leverage Advisor chooses; the domain executor runs; native Goal continues; the
ticket packet owns state. Do not add another runner, planner skill, state file,
or ticket per experiment.
````
