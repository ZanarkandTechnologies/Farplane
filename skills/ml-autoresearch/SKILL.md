---
name: ml-autoresearch
description: "Use for \"set up an ML improvement campaign\", \"plan the next round\", \"what should we try next\" or \"why did this run miss\": an ML experiment loop that picks bets from today's misses and keeps verified gains."
department: operations
source: local
template_uses:
  skill-template: "0.6.9"
  skill-eval-task: "0.2.0"
allowed-tools: Read, Glob, Grep, Bash
---

# ML Autoresearch

## Context

Use this when an ML training or inference system has a frozen evaluator, a
measurable objective, a bounded mutable surface, and compute authority for
repeated experiments. One ticket holds one stable objective, evaluator, data
boundary, and budget; experiments are receipts, not tickets. It adapts
Karpathy's Autoresearch loop to Farplane's Goal Packet: native Goal alone
continues it, and Goal Advisor compiles the packet but never selects techniques.

## Skill Signature

```text
ml_autoresearch(target_system, owning_ticket, mutable_surface, frozen_evaluator,
                primary_metric, guards?, technique_catalog?, budgets?)
  -> approved Goal Packet + best verified candidate + experiment receipts
reads: target code/docs, evaluator and data contract, owning issue, tree, receipts
does: picks bets from a decision tree over misses; one experiment at a time
writes: ## Goal program, hypothesis-tree.json, turn comments, receipts, kept change
returns: packet state, best candidate or a negative/blocked result, residual risks
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Bind the campaign contract and prove the baseline.**
  `ticket + target -> frozen contract + baseline receipt | direct fix | blocked`

  Rule: Bind the mutable surface, frozen evaluator and data boundary, metric and
  direction, guards, and budget; send an obvious bug to direct implementation
  and an unclear metric to Goal Advisor
  [metrics](../goal-advisor/references/metrics.md). Never invent a
  GPU/time/spend/attempt ceiling, metric or guard threshold, or repeatability
  band: an omitted value stays unresolved and blocks packet approval, but the
  non-numeric tree plan is still returned. Hash evaluator, splits, environment,
  and baseline; run the exact full evaluator; smokes never promote.

  Assert:
  - All of the above is named before any mutation, or the gap is the blocker;
    mutating it to manufacture a gain stales the packet.
  - External compute, spend, uploads, or services carry the ticket's authority.
- [ ] **N2 — Grow a decision tree over today's misses.**
  `per-case baseline scores -> case kinds + limiting stage | open kinds`

  Rule: Score today's best on every set; only its misses go forward, one row
  each; a held-out set is scored, never mined. Split misses by questions
  answerable without the truth into a decision tree over case kinds: each kind
  gets the technique that wins on all its cases, handled and missed, and the
  shipped pipeline routes every case down that tree. Give each stage the truth
  in turn; the one that moves the end score most is the limit. Read misses
  before naming a cause.

  Example: `true depth +3, true boxes +20 -> the box detector is the limit`

  Assert:
  - Every split is answerable at run time; "how wrong the output was" is not.
  - The limiting stage comes from a truth swap, or is marked not measured yet.
- [ ] **N3 — Source techniques and card the hypotheses.**
  `case kinds + sources -> carded hypothesis-tree.json | research | open kinds`

  Rule: Per case kind, ask why against the target docs: what does a technique
  see that today's method does not? Search local failures, supplied refs, Feed
  Scout signals, and the optional [efficient-inference
  catalog](references/technique-catalog-efficient-inference.md) (latency or size
  goals) by case kind; route bounded [research](../research/SKILL.md) or Best Of
  Worlds when coverage is missing or stale. Extract techniques, mechanisms,
  variables, failure conditions, source refs, and ablation-table gains,
  recording dispositions before use. Generate: add B to today's A (union, vote,
  median, per-case pick) so A's wins stay, keeping any swap of A `defer` until A
  + B is kept and A's own misses are the limit; combine methods whose misses
  differ, ending in a per-case pick; add permutation, transfer, ablation, or new
  direction. Card each node: `target_misses`, expected observation as a
  predicted number (ablation tables when sourced), falsifier, kill rule, cost,
  expected compounding reward, and `reward_basis`.

  Assert:
  - Nothing is ranked until every eligible node has the whole card; an unlabeled
    or implied reward basis is an incomplete node.
  - `reward_basis` names what compounds (reusable capability, information that
    prunes the tree, options unlocked, proof accelerated), not metric lift.
  - An uncovered case kind stays open, not a node, naming its need.
- [ ] **N4 — Select and preregister the next experiment.**
  `policy + eligible leaves + receipts + budget -> one preregistered move | approval pending | stop`

  Rule: Apply `choose_next` (execute, diagnose, report_now, request_feedback, or
  stop) to the program policy, eligible leaves, turn-comment learnings,
  full-evaluator receipts, and remaining budget; never follow a fixed roadmap
  order. When several credible moves need judgment, make one ordinal
  [choose-next](../goal-advisor/references/choose-next.md) comparison with
  outside options; it returns a decision and stores nothing. No tournament,
  persistent rank, or uncalibrated numeric lift. Preregister the card plus
  observation horizon, named confidence, surprise trigger, changed boundary,
  expected information, and guards. On the first round, `goal-advisor` puts the
  [ML Goal program preset](references/goal-program-template.md) into the issue's
  `## Goal program` with this selection, updates `## Current Goal state`,
  compiles the native Goal prompt, and gets approval before execution.

  Assert:
  - `falsifier` and `surprise_trigger` are separate labels, never one threshold.
  - The experiment is one attributable delta on the allowed surface.
  - One packet, runner, and ticket; split only for a new objective, evaluator,
    owner, approval or spend boundary, or parallel proof surface.
- [ ] **N5 — Run one experiment and diagnose a miss.**
  `preregistered experiment -> receipt + tree update | diagnostic children`

  Rule: Change only the allowed surface, run smokes, then the exact full
  evaluator. Update the tree node (result, evidence, insight) first, then post
  one compact Goal turn comment linking the receipt (preset `receipt` fields);
  never overwrite a failed attempt. A material miss or an implausibly strong
  result goes through `eval:experiment` before rejection or promotion; the
  domain executor owns any repair or rerun within the budget, and
  evaluator-integrity or leakage doubts go to `qa` or `review`. For a
  surprising, invalid, prerequisite-uncertain, or causally ambiguous result, add
  only program-bounded diagnostic children (expected negatives may close), then
  repair, reject, defer, or backtrack to a credible sibling.

  Assert:
  - A missed score can falsify the parent claim but never says why.
  - A cause is `supported` only when completed diagnostics discriminate against
    credible alternatives; target-local success shows learnable signal and
    research shows plausibility, but neither isolates a cause.
  - Supported: the parent gets the insight and diagnostic `evidence_refs` first;
    conclude `<intervention> failed because <cause> within <tested boundary>`.
  - Unresolved: pick the highest-information discriminator within budget and
    conclude only `<intervention> failed within <tested boundary>; cause
    unresolved.`, never "failed because" of an unresolved combination.
  - A receipt whose evaluator, split, config, code, data, or metric drifted
    stays append-only but leaves all causal evidence: its diagnostic and parent
    cause turn `unresolved`, performance stays falsified, the packet goes stale,
    and nothing is selected, preregistered, repaired, rerun, or recommended,
    even with attempts left, until Goal Advisor regenerates an approved packet.
- [ ] **N6 — Keep, replan, or stop mechanically.**
  `receipt + tree -> keep | discard | replan | stop | stale`

  Rule: Keep only a candidate that improves the primary objective with every
  guard passing (several test sets: a gain on most, e.g. 2 of 3, none worse
  beyond its named noise band); prefer the simpler one when materially tied, and
  never cherry-pick a run. Replan after every valid full result; the new best's
  misses re-enter N2. Stop on success, supported negative conclusion, exhausted
  frontier, stale packet, blocker, or budget, never by silently expanding scope.

  Assert:
  - A negative stop or surprise echoes its preregistered expected observation,
    horizon, confidence, falsifier, and surprise trigger and keeps the packet
    active unless the frozen contract or approval changed.
- [ ] **N7 — Review the final claim until TAS-A.**
  `best candidate + receipts -> review(scientific-evidence) -> TAS-A | revise | blocked`

  Rule: Re-run the full evaluator on the frozen best candidate and check receipt
  and budget integrity. Run the `review` skill with family `scientific-evidence`
  (an independent reviewer when available; `qa` when evaluator integrity or
  leakage needs it). On TAS-B, fix the named checks and review again; after
  three rounds report the open checks as the blocker. Close the ticket
  canonically only at TAS-A. Self-review never counts.

  Assert:
  - The output names the family, rounds, final TAS, and residual risks.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Replacing today's method with a paper's higher-scoring one before testing it
  added loses the cases today's method already wins.

## Output

Return the baseline, the approved packet and Goal prompt, linked receipts, tree
decisions, and the best verified candidate or a negative or blocked result. For
any loop policy, packet draft, or active turn, report one line each: `Packet`
(ticket sections, Goal program, tree, turn comments, compile state), `Tree`
(source synthesis, eligible leaves, branch state), `Progress` (turn-comment
learnings, current receipt refs), `Selector` (direct or choose-next, outside
options), `Experiment` (hypothesis, target misses, falsifier, boundary, guards,
cost), `Expectation` (observation, horizon, confidence, surprise trigger), and
`Writeback` (receipt ref, decision, constraint, tree mutation, next step).

For a source-stage or next-round request with concrete inputs, also render the
`Decision tree`, `Limiting stage`, extracted `Source refs`, `Techniques`,
`Mechanisms`, `Variables`, and `Failure conditions`, then every node's
`hypothesis`, `target_misses`, `mechanism`, `expected_observation`, `falsifier`,
`kill_rule`, `cost`, `expected_reward`, `reward_basis`, and `source_refs` (never
a setup checklist or a shared reward basis), then the `Choose-next comparison`
through `choose_next`, naming the selected node or blocking input. For a
surprise or causal request, render the diagnostic children, sibling leaves kept
for breadth, the outcome branch (`repair | reject | defer | backtrack`), the
claim disposition apart from its causal status, the parent's new `insight` and
`evidence_refs`, and the N5 conclusion, writing the tree before the receipt.
