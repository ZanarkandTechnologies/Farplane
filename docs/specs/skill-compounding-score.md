---
title: "Skill Compounding Score"
status: active
owner: skill-system
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - skills
  - compounding
  - taste-loop
refs:
  - docs/farplane-framework/lifecycle.md
  - docs/farplane-framework/graph-contract.md
  - docs/skills/system.md
  - docs/skills/README.md
  - farplane/products.md
  - skills/taste-loop/SKILL.md
  - skills/skill-maintenance/graph/README.md
feature_refs:
  - FEAT-0064
---

# Skill Compounding Score

The Skill Compounding Score ranks skills as improvement targets. It is not an
eval score, quality grade, template-health score, or claim that one skill is
"better" than another in general.

```text
skill_compounding_score(skill, project_state, lifecycle_refs, now?)
  -> ranked_target_score + score_breakdown + route_hint
```

Use it when a Farplane loop needs to decide which skill should receive the next
unit of human attention, self-improvement work, proof design, or maintenance.
The score answers:

```text
Which skill improvement is most likely to compound through the current
Farplane lifecycle if we spend one more feedback or improvement beat now?
```

## Boundary

Do not use this score as a substitute for:

- `eval` pass rate or task verdicts.
- `review` TAS judgments.
- skill-template rollout status.
- human preference labels.
- product KPI results.

Those signals may feed the score as evidence of opportunity or proof fit, but
the score itself is a prioritization function.

## Canonical Signals

The default score is a weighted, explainable sum. Consumers may normalize each
component to a `0..1` range and render the weighted contribution.

```text
score =
  30 * tier_leverage
+ 20 * lifecycle_ref_fit
+ 15 * product_lane_fit
+ 10 * observed_heat_fit
+ 10 * downstream_leverage_fit
+ 10 * improvement_gap_fit
+  5 * feedback_fit
+  5 * proof_fit
- penalties
```

The default component owners are:

| Component | Meaning | Source |
| --- | --- | --- |
| `tier_leverage` | How broadly upgrades to this skill tend to propagate. Lower numeric tiers rank higher. | `docs/skills/system.md`, `docs/skills/registry.jsonl` |
| `lifecycle_ref_fit` | How close the skill is to the lifecycle references, advisor boundaries, workflow routes, and graph nodes that Farplane currently treats as core. | `docs/farplane-framework/lifecycle.md`, lifecycle graph data when available |
| `product_lane_fit` | How directly the skill supports the current project products and weighted work lanes. | `farplane/products.md` |
| `observed_heat_fit` | How recently and broadly the skill has been invoked in real work. | skill graph heat from `.farplane/events/` and `FARPLANE_SKILL_HEAT_*` |
| `downstream_leverage_fit` | How many useful downstream skills, routes, or workflow edges may improve if this skill improves. | `todo_skill_refs`, `routes`, `common_chains`, generated skill/lifecycle graphs |
| `improvement_gap_fit` | How much known unresolved opportunity exists for this skill. | open lessons, troubles, self-improve deltas, missing proof, stale template status, review findings |
| `feedback_fit` | Whether the next useful signal can be obtained from the human in a short label/rank/accept/revise/reject interaction. | `optimize-with-human`, Taste Loop state |
| `proof_fit` | Whether the improvement has an honest proof route before mutation or promotion. | `metric-advisor`, target skill evals, QA/review/proof artifacts |

Penalties include open feedback over budget, cooldown, ambiguous ownership,
missing source files, fake metric risk, and convergence hold.

## Component Definitions

### Tier Leverage

Numeric skill tiers are compounding upgrade classes:

```text
tier_leverage(tier):
  tier 1 -> 1.00
  tier 2 -> 0.67
  tier 3 -> 0.33
  missing -> 0.00
```

This follows the skill-system contract: lower numeric tiers should be kept
sharper earlier because upgrades propagate through more downstream workflows.
Tier is not a call-stack depth and not a runtime phase.

### Lifecycle Reference Fit

Lifecycle reference fit measures distance from the skill to the references and
routes that Farplane's lifecycle doc names as core.

When graph data is available:

```text
lifecycle_ref_fit(skill) =
  1 / (1 + min_graph_hops(skill_node, lifecycle_reference_nodes))
```

Use `docs/farplane-framework/lifecycle.md` frontmatter refs, advisor-boundary
skills, self-update routes, and generated lifecycle graph nodes as the
`lifecycle_reference_nodes`.

When graph data is not available, use this prompt-safe fallback:

```text
direct lifecycle owner or advisor boundary -> 1.00
directly linked from a lifecycle owner skill -> 0.67
same group as a selected lifecycle owner -> 0.50
no visible lifecycle relationship -> 0.00
```

This is the "distance from the refs" signal: skills closer to lifecycle-critical
references are higher-compounding because an improvement there is more likely to
affect project setup, goals, tickets, Pulse/Interval, proof, memory, or skill
maintenance.

### Product Lane Fit

Project product lanes provide the business/product prior. Normalize the
selected lane's `Default Weight` from `farplane/products.md` against the maximum
lane weight.

```text
product_lane_fit = selected_lane_weight / max_lane_weight
```

If a skill maps to multiple lanes, use the highest lane weight and report the
matched lane. If no lane mapping is justified by the skill description, group,
routes, or current ticket/report context, use `0.00` and name the source gap.

### Observed Heat Fit

Use the existing skill graph heat algorithm. Do not invent a second heat
system.

```text
heat_score =
  invocation_count_window
+ distinct_threads_window
+ distinct_tickets_window
```

Normalize against the highest visible heat score in the candidate set. If no
heat data exists, use `0.00` and continue; absence of telemetry is not a
failure.

### Downstream Leverage Fit

Count visible downstream dependencies, capped and normalized:

```text
downstream_leverage_fit =
  min(1.0, weighted_downstream_edges / 5)
```

Include ordered todo-chain refs, signature `routes`, `common_chains.after`, and
lifecycle graph outgoing edges. Weight edges to lower-tier downstream skills
slightly higher because those skills are themselves compounding surfaces.

### Improvement Gap Fit

Improvement gap is opportunity, not quality. It can come from:

- a failing or stale skill-local eval.
- a self-improve baseline/current delta.
- open `docs/TROUBLES.md` or `docs/LESSONS.md` rows that name the skill.
- missing proof surface for a high-heat skill.
- stale template rollout when the skill is otherwise high leverage.
- repeated review findings against the skill.

If there is no grounded gap, use `0.00`. Do not invent a gap to justify a
heartbeat action.

### Feedback Fit

Use high feedback fit when the next useful signal can be gathered from a
compact human interaction: label, rank, accept, revise, reject, pick best hook,
pick best UI, or name the taste failure.

Use low feedback fit when the next step is mechanical, requires long context,
or would spam the operator.

### Proof Fit

Use high proof fit when a metric provider is honest and available:

- `eval` for runnable behavior cases.
- `agent_qa` for multi-turn agent behavior proof.
- `review` for judgment-heavy artifacts.
- `human_feedback` for taste labels and rankings.
- `none mechanical` when no metric is honest and the next action should be a
  blocked report or proof-design step.

`metric-advisor` owns the provider choice before Taste Loop creates benchmarks,
harder tasks, or Goal handoffs.

## Scorecard Shape

Every consumer should expose the score breakdown:

```text
Skill:
Route:
Score:
Components:
  tier_leverage:
  lifecycle_ref_fit:
  product_lane_fit:
  observed_heat_fit:
  downstream_leverage_fit:
  improvement_gap_fit:
  feedback_fit:
  proof_fit:
Penalties:
Decision:
Evidence refs:
```

Prefer relative ranking and short explanations over fake precision. A score
should explain why one target is first, not pretend to be scientific telemetry.

## Taste Loop Contract

Taste Loop is the first official consumer. It should:

1. Gate on active hours and feedback budget.
2. Build candidates from `farplane/products.md` Taste Loop Artifact Workflows,
   then use the skill registry, product lanes, heat, lifecycle refs, and recent
   Taste Loop state as scoring evidence.
3. Rank product-lane artifact workflows with Skill Compounding Score plus an
   `artifact_workflow_fit` gate.
4. Emit one bounded action by default: no-op, artifact feedback, artifact Goal
   handoff, or blocked report.
5. Ask `metric-advisor` for a provider before benchmark or Goal creation.
6. Stop without editing target skills directly.

Taste Loop must not ask for feedback on a skill summary. A valid feedback card
requires a generated artifact, artifact preview, screenshot, URL, or Goal
handoff artifact. Broad router skills such as `frontend-craft`,
`functional-ui`, `remotion`, `remotion-render`, `goal-advisor`,
`self-improve`, and `skill-maintenance` can support artifact generation, but
they are not direct Taste Loop targets.

## UI Contract

Farplane UI may render Skill Compounding Score as a human-friendly target board:

- score rank and route.
- component bars.
- lifecycle distance explanation.
- product lane match.
- open feedback count.
- next human action.
- proof provider and missing proof warning.

The UI should make it easy to give feedback without requiring the operator to
understand the whole formula. It must still preserve the score breakdown for
audit.

## Known Limits

- This spec defines the official algorithm and source owners; it does not ship
  a standalone scorer or UI component.
- Graph distance is prompt-computable today and should become mechanical only
  when a consumer needs deterministic repeatability.
- The score is project-relative. A skill can be low priority in one project and
  high priority in another.
- Human taste remains a feedback provider, not a fake numeric benchmark.
