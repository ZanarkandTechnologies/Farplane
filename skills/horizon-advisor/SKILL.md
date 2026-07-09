---
name: horizon-advisor
description: "Turn ambiguous long-horizon intent into goals.yaml, KPI trees, feedback-sized projects, and Goal Advisor handoffs."
tier: 3
group: harness
source: local
template_uses:
  skill-template: "0.3.0"
allowed-tools: Read, Write, Glob, Grep

---

# Horizon Advisor

## Context

`horizon-advisor` owns long-horizon strategy authoring for Farplane projects:
North Star, value function, KPI tree, project goal map, current milestone,
holds, and `farplane/goals.yaml` deltas. Product-level goals and KPI membership
live in `farplane/products/<product>/product.md` and must stay aligned with the
global goal tree. It exists so `goal-advisor` can stay focused on
execution compilation: selected frontier -> Goal Packet -> native Goal or
heartbeat prompt.

Use this skill when a project needs to decide what winning means, which levers
matter, how to measure progress, and which feedback-sized projects should be
expanded next. Do not use it for tiny execution tasks or for compiling a Goal
prompt after the selected frontier is already clear; use `goal-advisor` then.

## Skill Signature

```text
horizon_advice(project_root?, intent?, current_goals?, evidence?, constraints?)
  -> goals_delta
   + value_function
   + kpi_tree
   + project_goal_map
   + current_milestone
   + goal_advisor_handoff?
state: reads(farplane/goals.yaml, farplane/harness.md, farplane/products/*/product.md, farplane/products.json?, farplane/automations.toml?, tickets, progress, metrics, memory, relevant strategy docs); writes(farplane/goals.yaml delta, product.md goal/KPI delta, or strategy artifact when explicitly in scope)
gates: north_star_named; value_function_named; metrics_have_proof_surfaces; anti_metrics_named; current_frontier_expanded_only; execution_handoff_goes_to_goal_advisor
routes: metric-advisor | goal-advisor | update-strategy | deep-interview | review
fails: vague goals; fake precision; turning all goals into tasks; compiling native Goal prompts; hiding strategy in chat; optimizing proxy metrics without a shared value function
```

## Phase Contract

```text
horizon_phase(task, state)
  -> grounded_context
   + operator_intent
   + value_function
   + levers_and_metrics
   + project_goals_delta
   + proof_or_review
   + writeback_or_handoff
```

## Phase Boundary

This skill follows Tier 0 phases inline. Use `deep-interview` only when the
operator's winning condition, non-goals, or decision boundaries are genuinely
missing. Use `review` when a material `goals.yaml` delta or strategy artifact
will become canonical. Hand execution to `goal-advisor`; do not compile native
Goal prompts here.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the horizon target.
   - [ ] Resolve project root, goal artifact path, current horizon, operator
     intent, available metrics, product definitions, and whether this run
     should write files or only advise.
   - [ ] Read current `farplane/goals.yaml`, `farplane/harness.md`,
     `farplane/products/*/product.md`, generated product indexes, automation
     prompts when present, tickets/progress, and relevant memory before asking
     for facts.
- [ ] 2. Define the value function before goals.
   - [ ] Name the primary winning condition, such as users, money, attention,
     capability proof, autonomy, quality, or learning.
   - [ ] Name weighted maximize/minimize terms and hard constraints.
   - [ ] Include anti-metrics that would make the goal misleading.
- [ ] 3. Build the KPI tree.
   - [ ] Choose one North Star or learning objective.
   - [ ] Decompose into 3-5 controllable levers and leading metrics.
   - [ ] Pair every metric with a provider and proof surface:
     `artifact_presence`, `mechanical`, `review`, `agent_qa`,
     `human_feedback`, `market`, `learning`, or `hybrid`.
   - [ ] Put metric mechanics in `farplane/bindings.yaml` recipes with inline
     source and update prompt. Put product KPI membership in the owning
     `farplane/products/<product>/product.md`. Keep `farplane/goals.yaml` KPI
     lists to stable IDs plus interpretation.
   - [ ] Derive a metric card for any KPI whose provider, guard metric,
     anti-metric, or proof surface is unclear.
   - [ ] Avoid fake precision when the honest signal is qualitative,
     researcher-led, or early-stage.
- [ ] 4. Shape the project goals.
   - [ ] Load [references/project-goals.yaml](references/project-goals.yaml) when
     writing or materially changing a long-horizon project goal map.
   - [ ] Expand only the first evidence-producing branch deeply.
   - [ ] Use feedback-sized projects as the default durable unit.
   - [ ] Create child tickets only for real execution, unblock, approval,
     review, dependency, or proof boundaries.
- [ ] 5. Write the goal artifact or handoff.
   - [ ] If file writes are in scope, patch `farplane/goals.yaml`; patch
     product `product.md` files when product-level goals or KPI membership
     change; patch `farplane/bindings.yaml` when metric recipes, inline
     sources, pinned state, units, or update prompts change; regenerate
     `farplane/products.json` after product-file changes.
   - [ ] If the horizon needs a separate parent, make that parent a Farplane
     project with its own `farplane/goals.yaml` instead of creating a standalone
     strategy file.
   - [ ] If execution is ready, produce a `goal_advisor(...)` handoff over the
     selected frontier instead of compiling the Goal prompt here.
- [ ] 6. Verify and finish.
   - [ ] Confirm the goals are measurable enough to review and not merely task
     labels.
   - [ ] Confirm metrics optimize the shared value function rather than local
     proxies.
   - [ ] Confirm strategy state is in files, not hidden in chat.
   - [ ] Run available validators when skill or project files changed.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Core Model

Use Farplane's harness objective function as the default high-level value
function when a project is about autonomous agents:

```text
maximize:
  meaningful_long_running_output
+ quality
+ validated_improvement
+ reliability
+ reusable_behavior
+ auditability

minimize:
  human_intervention
+ false_completion
+ agent_churn
+ coordination_cost
+ ungrounded_claims
+ brittle_state_loss
```

Hard constraints come first: user goal satisfied, groundedness sufficient,
correctness/safety not regressed, proof exists, and operator control is
preserved.

## Templates

Goal statement:

```text
Improve <system/project> from <baseline or unknown>
to <meaningful result threshold>
by <timeframe>,
measured by <quality metric + intervention metric + proof surface>,
without <safety/quality/operator-control regression>.
```

Handoff to execution:

```text
goal_advisor(
  files=[farplane/goals.yaml, <selected_ticket_or_project>, <program?>, <progress?>],
  task="compile the selected horizon frontier into a Goal Packet",
  metric_provider=<provider>,
  trigger=<active_goal | heartbeat | feedback_loop>,
  gates=[<hard constraints>]
) -> ticket.md + program.md + progress.md + native_goal_prompt?
```

## Gotchas

- Do not make "more users" the goal unless the strategy names the loop,
  audience, channel, conversion point, and proof surface.
- Do not make "AI self-improves" the goal without intervention budget,
  accepted-improvement criteria, eval/ablation evidence, and anti-metrics.
- Do not convert every horizon node into a ticket. Goals describe outcomes;
  projects group evidence-producing bets; tickets execute bounded work.
- Do not bury long-horizon strategy in `progress.md`; use `farplane/goals.yaml`
  for project-level strategy and product `product.md` files for stable
  product-level goals.
- Do not compile native `/goal` prompts here. That boundary belongs to
  `goal-advisor`.

## Reference Map

- [references/project-goals.yaml](references/project-goals.yaml) - load when
  writing or materially changing a long-horizon project goal map.
- [../../docs/fundamentals/harness-algebra.md](../../docs/fundamentals/harness-algebra.md)
  - shared harness objective function and optimization terms.
- [../../docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md](../../docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md)
  - project goals, Goal Packet, ticket/program/progress boundary.
- [../goal-advisor/SKILL.md](../goal-advisor/SKILL.md) - handoff target for
  selected frontier execution compilation.
- [../metric-advisor/SKILL.md](../metric-advisor/SKILL.md) - metric cards for
  KPI providers, guard metrics, anti-metrics, and no-metric rationale.

## Output

Return or write:

```text
Horizon Strategy:
North Star:
Value Function:
KPI Tree:
Project Goal Map / Goals Delta:
Current Milestone:
Anti-metrics / Holds:
Goal Advisor Handoff:
Proof / Validation:
```
