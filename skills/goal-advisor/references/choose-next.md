# Choose Next: Multi-Move Comparison

Load inside a running Goal's `choose_next` step only when several eligible
moves need judgment. A mechanically implied move executes directly. The
comparison is stateless: it reads the packet, returns one selection and the
tree mutation it expects, and leaves execution, tree writes, and Goal
compilation to their owners.

```text
choose_next(objective, evidence, eligible_moves, remaining_budget)
  -> execute | diagnose | report_now | request_feedback | stop
```

## Inputs

Program policy, eligible pending leaves of `hypothesis-tree.json` when present
(derive leaves from parent and status; never store ranks or a second frontier;
the tree is the sole research-state owner for experiment-backed Goals, and this
file owns its search semantics, never copied into ordinary Goal Packets),
the latest Goal turn comments' learnings and receipts, current evaluator evidence, and
remaining budget. When any is absent, return a source gap: list the presence or
exact absence of each input, render a comparison labelled `conditional`, and
select nothing until the missing state is bound.

## Rules

1. **Filter before ranking.** Mark every prerequisite-invalid, conflicting,
   exhausted, or over-budget move `reject` or `defer` and name the failed
   prerequisite. Omission is not filtering.
2. **One ordinal comparison.** Rank on bottleneck fit, information gain,
   options unlocked, proof speed, cost, risk, reversibility, and interference.
   No pairwise tournament, no uncalibrated numeric lift, no persisted scores.
3. **Beat the outside options.** Compare the best move with `report_now`,
   `request_feedback`, and `stop`, one win/lose line each, then name the
   winner. Spend more budget only when the move wins.
4. **Pre-commit the bet.** Before acting, record what must be true, a
   confidence range or `uncalibrated`, downside, and falsifier. Judge the later
   result against this record, not by the outcome alone.
5. **Only decision-changing observations.** The first proof is the cheapest
   observation whose positive and negative results lead to different next
   actions. Drop any observation that would leave the ranking, spend, scope,
   or an outside option unchanged, however easy it is to collect.
6. **Contingent replan, not a ladder.** State how positive, flat, negative,
   branch-specific, invalid, and budget-exhausting results change the frontier.
7. **Diagnose ambiguity, then backtrack.** For a surprising, invalid, or
   causally ambiguous result add at most the program-bounded diagnostic
   children, preserve credible siblings, and resolve to `repair | reject |
   defer | backtrack`. Expected negatives close directly.
8. **One campaign, one ticket.** Experiments sharing one objective, evaluator,
   owner, and budget stay in one campaign ticket; split only at an ownership,
   proof, approval, spend, or objective boundary.

## Seeding the first frontier

From local failures and bounded sources, extract source refs, techniques,
mechanisms, and variables, then write each initial node with `hypothesis`,
`mechanism`, `expected_observation`, `falsifier`, `expected_reward`,
`reward_basis`, and `source_refs`. Admit an externally sourced candidate only
with an `adopt | adapt | reject | defer` disposition. Return a source gap
rather than inventing candidates. Guard against seed anchoring: keep credible sibling
branches and widen sources only for a named coverage gap.

## Output

```text
Inputs: program | leaves | progress | evidence | budget (present or absent)
Filtered: <move -> reject|defer + failed prerequisite>
Ranked frontier: <ordinal, one line of evidence each>
Outside options: best move | report_now | request_feedback | stop -> winner
Bet: thesis | confidence or uncalibrated | downside | falsifier
First proof: <observation> -> if positive <action> | if negative <action>
Replan: positive | flat | negative | branch | invalid | budget
Diagnostic (ambiguous only): children | preserved siblings | repair/reject/defer/backtrack
Writeback order: hypothesis-tree.json, then Goal turn comment, then ## Current Goal state
```

Example: a flat representation probe that helped one target class -> rank a
class-specific follow-up above a new model family; if positive, deepen that
representation; if flat, inspect label limits before any neural model; compare
with `report_now` because the asymmetric result is already worth reporting.
