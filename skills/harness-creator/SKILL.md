---
name: harness-creator
description: "Turn a high-level project or business idea into a values-goals-KPI-heartbeat harness, skill/ticket map, and current milestone."
tier: 3
group: harness
source: local
template_uses:
  skill-template: "0.2.0"
allowed-tools: Read, Write, Glob, Grep, Bash, web_search

---

# Harness Creator

## Context

Use this skill when the operator gives a high-level project, business, channel,
academy, research, product, ecommerce, or internal-ops idea and needs Farplane
to design the operating harness before execution. This is the layer above
`goal-advisor`: it writes a compact **Harness Program** for the idea, grounded
by evidence, then selects the current milestone.

The default output is one operator-readable Markdown file:

```text
project-harness.md = YAML metadata
                   + one fenced harness-program block
                   + evidence / assumptions / open questions
```

Use the `harness-program` block as the compact source of truth. Use Markdown
around it only for evidence, assumptions, review notes, and handoff context.
Split into child Goal Packet files only when the selected milestone is ready to
run.

`deep-init-project` is the normal public setup entrypoint for making a project
a Farplane project. It routes here as the internal operating-program phase when
`harness_depth != none`. Call this skill directly only for explicit harness
redesign, advanced operating-program work, or existing projects that already
have substrate files.

The first version is experimental. Do not claim this can bootstrap arbitrary
domains until pilot evidence proves the loop. Start with the smallest
evidence-producing harness and expand only after review or feedback.

When the harness includes long-horizon project goals, default to feedback-sized
projects: the smallest durable project whose output can be reviewed, measured,
shown, or exposed to user/market feedback. Put obvious next moves in
`starting_tasks`. Create child tickets only for real execution, unblock,
approval, review, dependency, or proof boundaries.

## Skill Signature

```text
project_harness_creator(project_idea, values?, priorities?, mode_presets?, context?, constraints?, budget?)
  -> project_harness
   + harness_program
   + evidence_wrapper
   + proposed_tickets
   + current_milestone
   + goal_advisor_handoff
state: reads(operator idea, values, constraints, local assets/docs/tickets/skills, docs/skills/registry.jsonl, harness doctrine, farplane/goals.md, farplane/automations.md, and farplane/bindings.md when present, current external research only when domain truth matters); writes(project-harness.md, proposed tickets, farplane/automations.md, and farplane/bindings.md when configuring recurring work, optional capability/gap/handoff sidecars, optional Goal Packet drafts)
gates: values_or_default_values_named; priorities_named; feedback_loop_defined_or_ticketed; metric_providers_honest; existing_tickets_checked_first; missing_systems_named; blockers_ticketed; side_effect_gates_named; current_milestone_named; goal_advisor_handoff_ready
routes: deep-init-project | research:* | ingest-content | harness-advisor | skill-creator | goal-advisor | optimize-with-human | interval-update | review | relevant domain skill
fails: runs Goal before designing harness; treats parent harness as an indefinite native Goal; schedules hidden runtime; analyzes metrics that do not exist; creates skills before checking existing systems; performs R&D when a standard system template is enough; triggers publishing/spend/account/customer side effects without approval
```

## Phase Contract

```text
project_harness_creation_phase(project_idea, state)
  -> grounded_goal
   + values_priorities_goal_kpi_model
   + feedback_loop_skill_model
   + mode_preset_decisions
   + harness_program
   + skill_gap_and_missing_system_decisions
   + proposed_ticket_plan
   + scrum_heartbeat_policy
   + current_milestone
   + goal_advisor_handoff
```

## Phase Boundary

This skill follows Tier 0 phases inline. Call workflow skills only for smaller
child scopes: `deep-init-project` for standard project systems, `research:*`
for real domain uncertainty, `harness-advisor` for Farplane surface placement,
`skill-creator` for a stable reusable missing primitive, `goal-advisor` after
the current milestone is selected, and `review` for material readiness.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the project idea, values, and constraints.
   - [ ] State the idea as an outcome, not a task label.
   - [ ] Name `values.mission`, `values.operating_principles`,
     `values.priorities`, `values.non_tradeoffs`, and `mode_presets`; if
     absent, infer defaults and mark the inference.
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
   - [ ] Define values, modes, goals, axes, systems, skill bindings, operator
     tickets, heartbeats, gates, current milestone, and Goal Advisor handoff.
   - [ ] For project-goal-shaped harnesses, keep `project` as the default durable
     planning unit and use `starting_tasks` only as hints unless a child ticket
     has a real boundary reason.
- [ ] 4. Define strategy axes, KPIs, and metric honesty.
   - [ ] Pick axes from the library: reach/acquire, activate/first value,
     retain/loyalty, refer/share, monetize/resources, impact/mission,
     deliver/quality, efficiency/capability, learning/evidence, and risk/trust.
   - [ ] For each axis, fill `strategy_state(axis, weight, current_bet, KPI,
     metric_provider, evidence, anti_metric, heartbeat, update_rule)`.
   - [ ] If instrumentation does not exist, mark `missing_instrumentation` and
     define the concrete feedback skill needed plus an unblock/setup ticket
     instead of pretending measurement exists.
   - [ ] Define at least one init-time feedback loop before refinement:
     `skill feedback_capability { status, requires, use, action }` plus the
     concrete `ticket { type: unblock }` when access, export, account setup,
     operator labels, or instrumentation is missing.
   - [ ] Prefer specific feedback skills such as `instagram_attention_graph`,
     `youtube_retention_metrics`, `posthog_activation_funnel`,
     `sales_call_pattern_reader`, or `operator_usefulness_labels`; avoid vague
     tickets like "define first feedback loop".
- [ ] 5. Inventory existing tickets, systems, skills, assets, and tools before
  inventing new ones.
   - [ ] Check proceedable tickets first when the harness is for an existing
     project; proactive gap work comes after the current board has no safe
     proceedable work.
   - [ ] Check `docs/skills/registry.jsonl`.
   - [ ] Search relevant local docs, tickets, examples, artifacts, and asset
     stores.
   - [ ] If the repo lacks standard operating files, feedback surfaces, QA
     surfaces, ticket templates, or bootstrap docs, route setup through
     [deep-init-project](../deep-init-project/SKILL.md).
   - [ ] Classify capabilities as `ready`, `needs_config`, `needs_access`,
     `needs_operator_setup`, `needs_reference`, `needs_eval`, `needs_wrapper`,
     `missing`, or `defer`.
   - [ ] Represent external data, accounts, notifications, and shared team
     systems as `skill` capabilities with required inputs, not as a separate
     external-IO concept.
   - [ ] Put project-specific non-secret coordinates in `farplane/bindings.md`
     rather than inventing provider-specific config files.
   - [ ] For each human access/setup/approval blocker, create or propose a
     `ticket` node with `type: unblock` instead of expanding the harness
     Markdown.
- [ ] 6. Define the Scrum-style operating cadence.
   - [ ] Create or update tracked `farplane/automations.md`; keep ignored
     `.farplane/` for runtime state, reports, eval runs, and logs.
   - [ ] Create or update tracked `farplane/bindings.md` for project-specific
     external coordinates needed by skills.
   - [ ] Default to explicit project loops first: `pulse-update` for bounded
     immediate actions plus daily and weekly `interval-update` automations for
     reporting, drift checks, strategy/backlog/memory/skill maintenance, and
     long-horizon rollups.
   - [ ] Keep ticket selection inside `pulse-update`: fetch local tickets
     first, skip blocked or approval-required work, rank for priority and
     compounding ROI, run `impl-plan` if needed, then use `goal-advisor` to
     execute one ticket as far as possible.
   - [ ] `interval-update`: report on a bounded review window, plan the next
     bounded window, and produce dated interval reports plus local ticket
     deltas or Goal Advisor handoffs.
   - [ ] When horizon work can split safely, express subagent lanes as
     `delegate(context_ref, task_prompt, skills?, output?)`; `context_ref` must
     be a file, ticket, Goal Packet, or artifact path.
   - [ ] Use [update-strategy](../update-strategy/SKILL.md) for new strategy,
     system gaps, experiments, and ticket deltas.
   - [ ] Use [update-memory](../update-memory/SKILL.md) for consolidated
     memory, README/doc deltas, and stale-context notes.
   - [ ] Use `skill-maintenance(mode: harden_skill)` for new evals, gotchas,
     regression cases, and improvement tickets from fresh lessons/troubles.
   - [ ] Use `skill-maintenance(mode: refine_skill)` to consolidate older
     evals/gotchas and shorten skill surfaces after hardening exists.
   - [ ] `update_system_gaps`: when no ticket can advance, inspect missing systems,
     weak metrics, stale assumptions, and safe preparation work.
   - [ ] Treat extra metric, memory, or chief-of-staff automations as optional
     escalations after the three default compiled lanes prove
     insufficient.
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
- [ ] 9. Compile the current milestone.
   - [ ] Use [templates/goal-advisor-handoff.md](templates/goal-advisor-handoff.md)
     to make the handoff explicit.
   - [ ] Use [goal-advisor](../goal-advisor/SKILL.md) only after the milestone,
     source files, metric provider, drift policy, and stop conditions are known.
   - [ ] Use [optimize-with-human](../optimize-with-human/SKILL.md) when the
     operator's labels, rankings, approval, or taste are the honest early
     metric.
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
Values / Operating Principles / Priorities:
Strategy Axes / KPI Map:
Feedback Skill Loops:
Heartbeat Preview:
Automation Manifest:
Skill Gap Map:
Missing Systems / Missing Primitives:
Operator Unblock Tickets:
Feedback Skill / Metric Plan:
Approval Gates:
Current Milestone:
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
  goal-advisor-handoff.md            # optional sidecar when milestone is ready

tickets/TASK-YYYY-unblock-*.md      # preferred for human access/setup blockers
```

## Gotchas

- Program first: the `harness-program` block is the source of truth; tables and
  Markdown are evidence or inventory sidecars.
- Evidence first: no refinement, validation, or "business is working" claim
  without at least one honest feedback loop or a concrete feedback-skill ticket.
- Smallest lever first: check existing skills/tickets/systems before creating
  new skills, external-IO abstractions, hidden automations, or root-prompt rules.
- Leaf execution first: parent harnesses coordinate; native Goal runs selected
  milestones or tickets, and `pulse-update` selects one proceedable bounded
  action per beat before proactive gap work.
- Human gates first: publishing, spend, accounts, customer contact, private
  data, credentials, and feedback access become explicit gates or
  `ticket { type: unblock }` nodes.

## Reference Map

- [references/harness-il.md](references/harness-il.md) - load before writing
  the compact Harness Program notation.
- [templates/project-harness.md](templates/project-harness.md) - copy first
  when writing the primary one-file project or business operating harness.
- [templates/capability-map.md](templates/capability-map.md) - copy when the
  skill/tool/asset inventory needs its own artifact.
- [templates/missing-primitive-plan.md](templates/missing-primitive-plan.md) -
  copy when gaps need owner/action decisions.
- [templates/goal-advisor-handoff.md](templates/goal-advisor-handoff.md) - copy
  before asking `goal-advisor` to compile the selected milestone.
- [deep-init-project](../deep-init-project/SKILL.md) - use when a project lacks
  standard repo, ticket, QA, feedback, or bootstrap systems.
- [interval-update](../interval-update/SKILL.md) - scheduled report-then-plan primitive for
  project-specific strategy refreshes configured by automation prompts or
  project docs.
- [update-strategy](../update-strategy/SKILL.md) - generic project strategy
  refresh primitive for interval updates.
- [update-memory](../update-memory/SKILL.md) - generic project memory refresh
  primitive for interval updates.
- [examples/faceless-ai-channel.md](examples/faceless-ai-channel.md) - pilot
  example for the first proof case.
