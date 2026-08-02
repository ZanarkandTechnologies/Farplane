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
  - <hypothesis-tree.json>
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
  hypothesis_tree: <hypothesis-tree.json>
  source_stage:
    inputs: <local failures, supplied refs, configured Feed Scout signals, or bounded research>
    extracts: <techniques, mechanisms, variables, failure conditions, source refs>
  rule: one ordinal compounding-leverage judgment; no tournament, persistent rank, or uncalibrated lift
  before_each_experiment:
    inputs:
      - this program.md policy
      - eligible pending hypothesis-tree.json leaves
      - progress.md learnings, prior selections, and rejected moves
      - current full-evaluator experiment receipts
      - remaining time, compute, spend, attempt, and patience budget
    output: one next experiment + hypothesis + expected observation +
      observation horizon + confidence + falsifier + surprise trigger +
      changed boundary + expected reward + reward basis + material selection rationale + replan conditions
    rule: invoke leverage-advisor

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
    - update the selected tree node and append an immutable receipt
    - if the observation materially violates the expectation or is implausibly
      strong, route the receipt through agent-qa-test:experiment before method
      rejection or candidate promotion; the domain executor owns any repair or
      rerun inside the campaign's remaining budget
    - for surprising, invalid, prerequisite-uncertain, or causally ambiguous
      evidence, add only program-bounded diagnostic children; otherwise close
      the node and backtrack to the best credible sibling
    - treat claim failure and causal resolution separately: a missed metric may
      falsify the parent claim but cannot establish a cause without completed
      diagnostic evidence that discriminates against credible alternatives
    - label evidence roles: target-local success proves target learnability but
      not the failed transfer mechanism; background research supports
      plausibility but does not isolate a cause from live confounds
    - when a cause is supported, propagate the causal insight and diagnostic
      evidence refs to the parent node before the progress receipt; when it is
      not isolated, keep the parent cause unresolved and select the next
      highest-information discriminator inside the remaining budget
    - reserve `failed because` for a supported cause; an unresolved branch says
      only that the tested configuration failed and its cause remains unresolved
    - validate diagnostic receipts against the frozen evaluator, split, config,
      code, data, and metric before causal use; preserve drifted receipts
      append-only but remove them from causal evidence, change stale supported
      diagnostic and parent-cause labels to unresolved, mark the packet stale,
      and authorize only Goal Advisor regeneration
    - keep | discard | repair_once | defer | failed

after_each_turn:
  - read this policy, hypothesis-tree.json, and the complete progress.md tail
  - use leverage-advisor on pending tree leaves + progress learnings + current receipts + remaining budget
  - execute at most one selected experiment
  - update the tree, then append receipt ref, learning, tree mutation, decision, and next action to progress.md
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
tree owns current research state and progress owns chronology. Do not add
another runner, planner skill, state file, or ticket per experiment.
````
