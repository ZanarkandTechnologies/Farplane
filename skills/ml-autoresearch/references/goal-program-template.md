---
kind: goal-program-template
mode: ml_autoresearch
status: active
owner: skills/ml-autoresearch
---

# ML Autoresearch Goal Program Preset

Instantiate this compact preset into the owning campaign issue's `## Goal
program` section through Goal Advisor. The ticket sections own scope and proof;
Goal turn comments own observations; Goal Advisor separately compiles the
Files-listed native Goal launcher in a `**Goal launcher**` comment.

````markdown
### Goal Mode: ML Autoresearch <campaign>

```yaml
mode: ml_autoresearch
trigger: native_goal
approval: pending
compiled_from_ticket_sha: <first 12 hex of sha256(body above ## Goal program)>
```

```yaml
files:
  - <owner/repo#n>
  - <.farplane/goal-advisor/issue-<n>/hypothesis-tree.json>
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
  owner: active-goal
  hypothesis_tree: <hypothesis-tree.json>
  source_stage:
    misses: <today's best scored per case on every set; only its misses go forward, one row per miss; a held-out set is scored, never mined>
    decision_tree: <splits are questions about a case answerable without the truth; each case kind names the technique that wins on all its cases, handled and missed; the shipped pipeline routes every case down this tree>
    limiting_stage: <the stage whose truth input moves the end score most; missed cases inspected before naming a cause>
    inputs: <local failures, supplied refs, configured Feed Scout signals, or bounded research, searched by case kind>
    technique_catalog: <for latency/size/on-device objectives, references/technique-catalog-efficient-inference.md; append verified outcomes to its Field results>
    extracts: <techniques, mechanisms, variables, failure conditions, source refs, predicted gains from ablation tables>
    generation: add B to today's A (a swap of A stays defer until A + B is kept); combine methods whose misses differ, ending in a per-case pick down the decision tree; permutation, transfer, ablation, or new direction
  rule: choose execute | diagnose | report_now | request_feedback | stop; use goal-advisor references/choose-next.md only for real multi-option judgment
  before_each_experiment:
    inputs:
      - this ## Goal program policy
      - eligible pending hypothesis-tree.json leaves
      - Goal turn comment learnings, prior selections, and rejected moves
      - current full-evaluator experiment receipts
      - remaining time, compute, spend, attempt, and patience budget
    output: one next experiment + hypothesis + target misses + expected observation +
      observation horizon + confidence + falsifier + surprise trigger +
      changed boundary + expected reward + reward basis + material selection rationale + replan conditions
    rule: execute a mechanically implied move directly; otherwise apply goal-advisor references/choose-next.md

loop:
  baseline: run and record before any mutation
  round:
    - choose one experiment directly or through the choose-next comparison when ranking is genuinely needed
    - before scoring, preregister hypothesis, target misses, expected
      observation as a predicted number, observation horizon, confidence,
      falsifier, surprise trigger, changed boundary, cost, guards, and
      keep/kill rule
    - implement the smallest attributable delta on the mutable surface
    - run correctness smoke
    - when valid, run the exact full frozen evaluator
    - update the selected tree node and append an immutable receipt
    - if the observation materially violates the expectation or is implausibly
      strong, route the receipt through eval:experiment before method
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
    - keep | discard | repair_once | defer | failed; keep only on a primary
      gain with every guard passing (with several test sets: a gain on most,
      e.g. 2 of 3, none worse beyond its named noise band)
    - after a keep, the new best's misses are the next source-stage input; a
      case kind no technique covers stays open, not a tree node, naming its need

after_each_turn:
  - read the issue body, hypothesis-tree.json, and the newest Goal turn comments within 80 lines
  - choose execute | diagnose | report_now | request_feedback | stop from pending leaves, evidence, and budget; use the choose-next comparison only when several moves need judgment
  - execute at most one selected experiment
  - update the tree, store the receipt below at a linked ref under .farplane/goal-advisor/issue-<n>/receipts/, then post one compact Goal turn comment with that ref, learning, tree mutation, decision, and next action; rewrite ## Current Goal state
  - continue, replan, block, or complete from the declared rules

turn_report: # the operator response for a loop policy, packet draft, or active turn; not turn-comment content
  packet: ticket sections, Goal program, tree, turn comments, compile state
  tree: source synthesis, eligible leaves, branch state
  progress: turn-comment learnings, current receipt refs
  selector: direct or choose-next, outside options
  experiment: hypothesis, target misses, falsifier, boundary, guards, cost
  expectation: observation, horizon, confidence, surprise trigger
  writeback: receipt ref, decision, constraint, tree mutation, next step

receipt: # stored at the linked ref, never pasted into the turn comment
  experiment_id:
  parent_candidate:
  selected_tree_node:
  progress_evidence_refs: []
  hypothesis:
  target_misses: []
  mechanism:
  expected_observation:
  observation_horizon:
  confidence: low | medium | high
  falsifier:
  kill_rule:
  surprise_trigger:
  expected_reward:
  reward_basis:
  source_refs: []
  changed_boundary:
  config_code_data_evaluator_hashes: {}
  command_environment:
  smoke_result:
  full_metrics: {}
  guards: {}
  runtime_compute_cost: {}
  decision: keep | discard | repair_once | failed | defer
  failure_or_learning:
  causal_status: supported | unresolved | not_required
  supported_cause_or_next_discriminator:
  causal_evidence_refs: []
  tree_mutation:
  next_action:

drift:
  - stale when ticket scope, mutable/frozen surfaces, data/splits, evaluator, metric, guards, budget, or approval changes
  - regenerate the packet and baseline before continuing after material drift

stop:
  complete: success threshold and guards pass, or no higher-value supported move remains after final verification
  negative: bounded frontier evidence supports no improvement inside the current campaign contract
  blocked: required data/compute/evaluator is unavailable or the packet is stale
  budget: the next faithful experiment would cross a declared ceiling
```

The Goal chooses; the choose-next comparison conditionally ranks; the domain executor runs; native Goal continues; the
tree owns current research state and Goal turn comments own chronology. Do not add
another runner, planner skill, state file, or ticket per experiment.
````
