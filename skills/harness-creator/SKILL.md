---
name: harness-creator
description: "Turn a high-level project or business idea into a values-goals-KPI-heartbeat harness, skill gap map, and Goal Advisor frontier."
tier: 3
group: harness
source: local
skill_template_version: "0.2.0"
allowed-tools: Read, Write, Glob, Grep, Bash, web_search
---

# Harness Creator

## Context

Use this skill when the operator gives a high-level project, business, channel,
academy, research, product, ecommerce, or internal-ops idea and needs Farplane
to design the operating harness before execution. This is the layer above
`goal-advisor`: it writes a compact **Harness Program** for the idea, grounded
by evidence, then selects the first executable frontier.

The default output is one operator-readable Markdown file:

```text
project-harness.md = YAML metadata
                   + one fenced harness-program block
                   + evidence / assumptions / open questions
```

Use the `harness-program` block as the compact source of truth. Use Markdown
around it only for evidence, assumptions, review notes, and handoff context.
Split into child Goal Packet files only when the selected frontier is ready to
run.

The first version is experimental. Do not claim this can bootstrap arbitrary
domains until pilot evidence proves the loop. Start with the smallest
evidence-producing harness and expand only after review or feedback.

## Skill Signature

```text
project_harness_creator(project_idea, values?, goal_weights?, mode_presets?, context?, constraints?, budget?)
  -> project_harness
   + harness_program
   + evidence_wrapper
   + current_frontier
   + goal_advisor_handoff
state: reads(operator idea, values, constraints, local assets/docs/tickets/skills, docs/skills/registry.jsonl, harness doctrine, Goal Portfolio templates, current external research only when domain truth matters); writes(project-harness.md, optional capability/gap/handoff sidecars, optional Goal Packet drafts)
gates: values_or_default_values_named; goal_weights_named; metric_providers_honest; existing_tickets_drained_first; missing_systems_named; side_effect_gates_named; first_frontier_named; goal_advisor_handoff_ready
routes: deep-init-project | research:* | ingest-content | harness-advisor | skill-creator | goal-advisor | optimize-with-human | weekly-strategy-analysis | review | relevant domain skill
fails: runs Goal before designing harness; treats parent harness as an indefinite native Goal; schedules hidden runtime; analyzes metrics that do not exist; creates skills before checking existing systems; performs R&D when a standard system template is enough; triggers publishing/spend/account/customer side effects without approval
```

## Phase Contract

```text
project_harness_creation_phase(project_idea, state)
  -> grounded_goal
   + values_goal_kpi_model
   + mode_preset_decisions
   + harness_program
   + skill_gap_and_missing_system_decisions
   + scrum_heartbeat_policy
   + first_executable_frontier
   + goal_advisor_handoff
```

## Phase Boundary

This skill follows Tier 0 phases inline. Call workflow skills only for smaller
child scopes: `deep-init-project` for standard project systems, `research:*`
for real domain uncertainty, `harness-advisor` for Farplane surface placement,
`skill-creator` for a stable reusable missing primitive, `goal-advisor` after
the current frontier is selected, and `review` for material readiness.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the project idea, values, and constraints.
   - [ ] State the idea as an outcome, not a task label.
   - [ ] Name `values`, `goal_weights`, and `mode_presets`; if absent, infer
     defaults and mark the inference.
   - [ ] Name safety and operator gates: publishing, spend, accounts, customer
     contact, scraping, payments, legal/regulatory, brand, and private data.
   - [ ] If gates are not supplied, assume no external side effects until
     approval.
- [ ] 2. Decide the mode preset and discovery depth.
   - [ ] Use mode presets such as `business`, `channel`, `academy`, `lab`,
     `research`, `community`, `product`, `ecommerce`, or `internal_ops` to
     prefill goals, axes, KPIs, and heartbeats.
   - [ ] Cheat when the system is standard: use known templates for feedback,
     analytics, tickets, QA, strategy refresh, and project bootstrap instead of
     asking the agent to rediscover them.
   - [ ] Use [research:parity](../research/SKILL.md#researchparity) when the
     domain workflow, peer norms, startup guides, or comparable operators are
     unknown.
   - [ ] Use [research:competitor](../research/SKILL.md#researchcompetitor)
     when named or discoverable products, channels, creators, stores, or tools
     shape the opportunity.
   - [ ] Use [research:user-grounding](../research/SKILL.md#researchuser-grounding)
     when the customer, audience, buyer, user, or operator job is unclear.
   - [ ] Use [research:gap](../research/SKILL.md#researchgap) when the desired
     harness must be compared with current Farplane capability.
   - [ ] Keep research proportional to choosing the first honest evidence loop;
     do not spend R&D budget when no marginal value exists.
- [ ] 3. Fill the Harness Program / project harness.
   - [ ] Load [references/harness-il.md](references/harness-il.md) before
     writing the compact program notation.
   - [ ] Use [templates/project-harness.md](templates/project-harness.md) as
     the default one-file operator artifact.
   - [ ] Lead with a fenced `harness-program` block. Put facts, assumptions,
     research refs, and open questions in the Markdown evidence wrapper.
   - [ ] Define values, modes, goals, axes, systems, skill bindings,
     heartbeats, gates, current frontier, and Goal Advisor handoff.
- [ ] 4. Define strategy axes, KPIs, and metric honesty.
   - [ ] Pick axes from the library: reach/acquire, activate/first value,
     retain/loyalty, refer/share, monetize/resources, impact/mission,
     deliver/quality, efficiency/capability, learning/evidence, and risk/trust.
   - [ ] For each axis, fill `strategy_state(axis, weight, current_bet, KPI,
     metric_provider, evidence, anti_metric, heartbeat, update_rule)`.
   - [ ] If instrumentation does not exist, mark `missing_instrumentation` and
     create a missing-system ticket or Goal Advisor handoff instead of
     pretending measurement exists.
- [ ] 5. Inventory existing tickets, systems, skills, assets, and tools before
  inventing new ones.
   - [ ] Drain proceedable tickets first when the harness is for an existing
     project; proactive gap work comes after the current board has no safe
     proceedable work.
   - [ ] Check `docs/skills/registry.jsonl`.
   - [ ] Search relevant local docs, tickets, examples, artifacts, and asset
     stores.
   - [ ] If the repo lacks standard operating files, feedback surfaces, QA
     surfaces, ticket templates, or bootstrap docs, route setup through
     [deep-init-project](../deep-init-project/SKILL.md).
   - [ ] Classify capabilities as `ready`, `needs_config`,
     `needs_reference`, `needs_eval`, `needs_wrapper`, `missing`, or `defer`.
- [ ] 6. Define the Scrum-style operating cadence.
   - [ ] `hourly_board_drain`: inspect active tickets and Goal Packets, start
     or resume one proceedable leaf, and log no-op when nothing can advance.
   - [ ] `idle_gap_audit`: when no ticket can advance, inspect missing systems,
     weak metrics, stale assumptions, and safe preparation work.
   - [ ] `daily_chief_of_staff`: summarize opportunities, risks, blockers,
     feedback needs, and the next best actions.
   - [ ] `weekly_strategy_refresh`: run `refresh_strategy(last_strategy,
     findings, metrics_or_feedback)` and update bets, holds, experiments, and
     Goal Advisor handoffs.
   - [ ] Keep all automations as `preview` or `ready_for_goal_advisor` until a
     real scheduler/automation is explicitly approved.
- [ ] 7. Choose harness levers from doctrine.
   - [ ] Use [harness-advisor](../harness-advisor/SKILL.md) when ownership is
     unclear across skill, ticket, template, docs, subagent, hook, validator,
     tool, automation, or prompt surface.
   - [ ] Prefer proof/review, ticket/program/progress, skill selection,
     references/templates, subagents, tools, validators, heartbeat, and root
     prompt in that rough order.
   - [ ] Do not expand root/global prompt unless the rule is truly global,
     durable, and expensive to recover later.
- [ ] 8. Decide missing primitive and missing system actions.
   - [ ] Use [templates/missing-primitive-plan.md](templates/missing-primitive-plan.md)
     when the gap list is material.
   - [ ] Use [skill-creator](../skill-creator/SKILL.md) only when a missing
     capability has a stable trigger and reusable workflow.
   - [ ] Otherwise choose reference, ticket, tool connector, eval, validator,
     subagent, `deep-init-project`, defer-until-pilot, or no-op.
- [ ] 9. Compile the first executable frontier.
   - [ ] Use [templates/goal-advisor-handoff.md](templates/goal-advisor-handoff.md)
     to make the handoff explicit.
   - [ ] Use [goal-advisor](../goal-advisor/SKILL.md) only after the frontier,
     source files, metric provider, drift policy, and stop conditions are known.
   - [ ] Use [optimize-with-human](../optimize-with-human/SKILL.md) when
     Kenji's labels, rankings, approval, or taste are the honest early metric.
- [ ] 10. Finish with proof and review.
   - [ ] Produce the filled harness packet or state why the task should remain
     template-only.
   - [ ] Run [review](../review/SKILL.md) for material harness packets,
     skill-creation choices, or readiness claims.
   - [ ] State what can run autonomously now, what requires approval, what
     evidence is missing, and the exact next Goal/heartbeat/feedback route.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

Return or write:

```text
Project Harness:
Harness Program:
Values / Goal Weights:
Strategy Axes / KPI Map:
Heartbeat Preview:
Skill Gap Map:
Missing Systems / Missing Primitives:
Feedback / Metric Plan:
Approval Gates:
Current Frontier:
Goal Advisor Handoff:
Autonomy Boundary:
Evidence Gap:
Next Action:
```

Default artifact paths when ticketed:

```text
tickets/TASK-XXXX/artifacts/harness-creator/
  project-harness.md
  capability-map.md                 # optional sidecar when inventory is large
  missing-primitive-plan.md          # optional sidecar when gaps are material
  goal-advisor-handoff.md            # optional sidecar when frontier is ready
```

## Gotchas

- Do not confuse a harness with a plan. A harness names the state, skills,
  tools, proof, feedback loops, and next executable route agents will use.
- Do not create a skill for every generic checklist step. Use the smallest
  reliable lever and defer unstable gaps until a pilot exposes repetition.
- Do not call a goal launched or a business validated because assets exist.
  Market or feedback signals must be captured honestly.
- Do not let the parent harness become an indefinite native Goal. Parent
  coordination is portfolio/heartbeat/manual resume; native Goal is for the
  selected leaf.
- Do not reinvent Scrum or startup operating basics during every harness run.
  Use the default daily/weekly cadence and standard missing-system checklist
  unless the project is genuinely doing R&D.
- Do not skip existing proceedable tickets in favor of open-ended proactive
  work. Drain the board first, then run gap audits when nothing safe can
  advance.
- Do not let Markdown tables become the source of truth for the business
  program. Tables are sidecar inventory views; the `harness-program` block is
  the compressed program.

## Reference Map

- [references/harness-il.md](references/harness-il.md) - load before writing
  the compact Harness Program notation.
- [templates/project-harness.md](templates/project-harness.md) - copy first
  when writing the primary one-file project or business operating harness.
- [templates/harness-portfolio.md](templates/harness-portfolio.md) - copy when
  a legacy or smaller portfolio sidecar is needed.
- [templates/capability-map.md](templates/capability-map.md) - copy when the
  skill/tool/asset inventory needs its own artifact.
- [templates/missing-primitive-plan.md](templates/missing-primitive-plan.md) -
  copy when gaps need owner/action decisions.
- [templates/goal-advisor-handoff.md](templates/goal-advisor-handoff.md) - copy
  before asking `goal-advisor` to compile the selected frontier.
- [deep-init-project](../deep-init-project/SKILL.md) - use when a project lacks
  standard repo, ticket, QA, feedback, or bootstrap systems.
- [weekly-strategy-analysis](../weekly-strategy-analysis/SKILL.md) - use when a
  weekly strategy refresh needs existing Farplane project signals.
- [examples/faceless-ai-channel.md](examples/faceless-ai-channel.md) - pilot
  example for the first proof case.
