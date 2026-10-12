# Loop Presets

Load when the Goal is a staged rollout of a proven play (`rollout`) or a
measurable ML campaign (`ml_autoresearch`). Each preset fills `program.md` and
the trigger shape; Goal Advisor still compiles the packet and launcher, native
Goal still continues, and the domain skill still executes.

## Rollout preset

Use after a feature or capability has a plausible leverage play and the
operator wants it to compound. Do things that do not scale first.

```text
rollout(feature, play, target_set?)
  -> exemplar (1-3 cases) -> sample_proof -> extracted pattern
  -> stop | second exemplar | rollout_goal(pattern, sample_proof, target_set)
     -> staged_batches + child_tickets? + rollout_progress
```

1. Bind the feature and play. When the play is missing or weak, compare the
   grounded candidate plays inline and recommend one with its tradeoff.
   Identify or propose a target set, but do not scale to it yet.
2. Choose one to three exemplars with high learning value, low setup friction,
   real failure exposure, and standalone value if rollout stops; say why each
   is representative and what would prove, falsify, or pause the idea.
3. Run the exemplar directly when tiny, through `impl-plan` when it is a coding
   ticket, or as its own Goal. Write a [metric card](metrics.md) before any
   repeated metric-based exemplar.
4. Capture sample proof from a concrete case, artifact, run, ticket, or
   evaluated output, then extract reusable steps, failure modes, proof
   requirements, target filters, hold or rollback conditions, and operator
   feedback points into the ticket or progress log.
5. **Rollout starts after sample proof, never before.** Stop when the exemplar
   is weak or generic; run a second exemplar when the pattern is not yet
   stable; compile a `rollout` Goal only when pattern, sample proof, and an
   explicit target set exist, with one proof row per staged target or child.
6. Promote the procedure into a skill only after repeated use proves its
   trigger and workflow are stable.

Output: `Selected Play`, `Exemplar Case`, `Sample Proof`, `Extracted Pattern`,
`Rollout Readiness`, `Goal Handoff`, `Next Owner`.

## ML autoresearch preset

Use when an ML training or inference system has a frozen evaluator, a
measurable objective, a bounded mutable surface, and compute authority for
repeated experiments. This adapts Karpathy's Autoresearch loop (baseline, one
experiment, evaluate, keep or discard, repeat) into a visible Goal Packet:
`ticket.md + program.md + hypothesis-tree.json + progress.md`. Instantiate
[the ML program preset](ml-program-preset.md) into the campaign's `program.md`.

1. **One campaign ticket per stable objective, evaluator, data boundary, and
   budget. No ticket per trial:** experiments are append-only progress entries
   and receipts. Split only for a changed objective or evaluator, an
   independent owner, a separate approval or spend boundary, or a genuinely
   parallel proof surface. Route an obvious deterministic bug to direct work.
2. Never invent a GPU, time, spend, or attempt ceiling, metric or guard
   threshold, or repeatability band; keep an omitted fixed cap unresolved and
   block approval while still returning the non-numeric plan.
3. **Hash the frozen evaluator**, data and split inputs, environment, and
   baseline candidate before any mutation, and run the baseline through the
   exact full evaluator. Smokes prove correctness, never promotion.
4. Source stage: start from local failures, any technique catalog, supplied
   references, and Feed Scout signals; route bounded `research` (papers or
   synthesis) when coverage is missing or stale. Seed `hypothesis-tree.json`
   with nodes that each carry `hypothesis`, `mechanism`,
   `expected_observation`, `falsifier`, `expected_reward`, `reward_basis` (what
   compounds: reusable capability, information that prunes the tree, options
   unlocked, or proof accelerated), and `source_refs`. Do not rank incomplete
   nodes. Use [choose-next](choose-next.md) only when several moves need
   judgment; no tournament, persistent rank, or numeric lift.
5. Select each experiment from current tree leaves, recent progress learnings,
   full-evaluator receipts, and remaining budget, never a fixed roadmap order.
   Preregister hypothesis, expected observation, horizon, confidence,
   **`falsifier` and `surprise_trigger` as separate labels** (one failure
   threshold cannot stand in for both), changed boundary, cost, guards, and
   keep/kill rule.
6. Change only the allowed surface. Update the tree node first, then append the
   immutable `progress.md` receipt; never overwrite a failed attempt. Route a
   material miss or implausibly strong result through
   `agent-qa-test:experiment` before rejecting or promoting; the domain
   executor owns any repair or rerun inside the remaining budget.
7. Separate claim failure from causal resolution. A missed score falsifies the
   performance claim, not its cause. Mark a cause `supported` only when
   completed diagnostic children discriminate against credible alternatives.
   **Reserve `failed because` for `causal_status: supported`**; otherwise write
   `<intervention> failed within <tested boundary>; cause unresolved.` and pick
   the highest-information discriminator. Target-local success and background
   research are clues, not isolation.
8. Before causal use, match each receipt's evaluator, split, config, code,
   data, and metric to the frozen campaign. On drift keep the receipt
   append-only, remove it from causal evidence, set the cause `unresolved`,
   mark the packet stale, and run nothing until Goal Advisor regenerates an
   approved packet.
9. Keep only candidates that improve the primary objective with every guard
   passing; prefer the simpler one when tied. Replan after every valid full
   result; stop on success, supported negative conclusion, exhausted frontier,
   stale packet, blocker, or budget. Finish by re-running the full evaluator on
   the frozen best candidate with independent review.

Experiment receipt:

```yaml
experiment_id:
selected_tree_node:
hypothesis:
mechanism:
expected_observation:
observation_horizon:
confidence: low | medium | high
falsifier:
surprise_trigger:
reward_basis:
changed_boundary:
config_code_data_evaluator_hashes: {}
full_metrics: {}
guards: {}
decision: keep | discard | repair_once | failed | defer
causal_status: supported | unresolved | not_required
supported_cause_or_next_discriminator:
causal_evidence_refs: []
tree_mutation:
next_action:
```
