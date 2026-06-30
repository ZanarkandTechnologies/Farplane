---
name: harness-creator
description: "Turn a high-level project or business idea into split Farplane project files, advisor handoffs, missing-system tickets, and a current milestone."
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
`goal-advisor`: it is the project operating-model advisor. It writes or
proposes split-file Farplane deltas for the idea, grounds them by evidence,
routes smaller advisor calls when needed, then selects the current milestone.

The default durable outputs are the standard Farplane project files:

```text
farplane/harness.md  = static human charter: mission, thesis, values,
                       non-tradeoffs, leverage commitments, agent authority,
                       allocation guardrails, and change rule
farplane/products.md = product catalog and work-lane weights
farplane/goals.md    = dynamic strategy, KPIs, current bets, milestone, and
                       holds
farplane/hooks.json  = declarative project hook config
.agents/skills/      = local product skills for company-specific production
                       workflows
```

Use `templates/project-harness.md` only as a transient split-surface planning
worksheet or ticket artifact when a one-file review surface helps. It must not
be treated as a canonical replacement for `farplane/harness.md`, and it must
not mix static charter content with dynamic products or current strategy.

`init-advisor` is the normal public setup entrypoint for making a project
a Farplane project. It routes here as the internal operating-program phase when
`init_mode == full`. Call this skill directly only for explicit harness
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
   + split_file_deltas
   + product_skill_reuse_map
   + local_product_skill_stubs?
   + product_skill_refinement_ticket?
   + evidence_wrapper
   + proposed_tickets
   + current_milestone
   + goal_advisor_handoff
state: reads(operator idea, values, constraints, local assets/docs/tickets/skills, docs/skills/registry.jsonl, .agents/skills/**?, harness doctrine, farplane/harness.md, farplane/products.md, farplane/goals.md, farplane/automations.md, and farplane/bindings.md when present, current external research only when domain truth matters); writes(farplane/harness.md static-charter deltas only with explicit approval, farplane/products.md product-catalog deltas, farplane/goals.md strategy deltas through goals policy, proposed tickets, farplane/automations.md, farplane/bindings.md when configuring recurring work, .agents/skills/<product-skill>/SKILL.md stubs or refinement-ticket handoffs, optional capability/gap/handoff sidecars, optional Goal Packet drafts)
gates: values_or_default_values_named; priorities_named; feedback_loop_defined_or_ticketed; metric_providers_honest; existing_tickets_checked_first; existing_skills_checked_before_product_skill_stubs; product_skill_reuse_map_written; missing_systems_named; blockers_ticketed; side_effect_gates_named; current_milestone_named; pm_activation_gate_named; goal_advisor_handoff_ready
routes: init-advisor | research:* | ingest-content | horizon-advisor | harness-advisor | skill-creator | goal-advisor | automation-advisor | optimize-with-human | interval-update | review | relevant domain skill
fails: runs Goal before designing harness; treats parent harness as an indefinite native Goal; schedules hidden runtime; analyzes metrics that do not exist; creates local product skills before checking existing reusable skills and systems; promotes project-local product skills to root skills before repeated proof; activates PM loops before core product skills or refinement tickets exist; performs R&D when a standard system template is enough; triggers publishing/spend/account/customer side effects without approval
```

## Phase Contract

```text
project_harness_creation_phase(project_idea, state)
  -> grounded_goal
   + values_priorities_goal_kpi_model
   + feedback_loop_skill_model
   + feedback_primitive_implementation_plan?
   + mode_preset_decisions
   + split_file_deltas
   + product_skill_reuse_map
   + local_product_skill_plan
   + skill_gap_and_missing_system_decisions
   + proposed_ticket_plan
   + scrum_heartbeat_policy
   + current_milestone
   + goal_advisor_handoff
```

## Phase Boundary

This skill follows Tier 0 phases inline. Call workflow skills only for smaller
child scopes: `init-advisor` for standard project systems, `research:*`
for real domain uncertainty, `horizon-advisor` for strategy/KPI depth,
`harness-advisor` for Farplane surface placement, `skill-creator` for a stable
reusable missing primitive, `goal-advisor` after the current milestone is
selected, `automation-advisor` only for live Codex automation activation, and
`review` for material readiness.

Local product skills are project-owned company workflows. Create or propose
them under `.agents/skills/<product-skill>/SKILL.md` only after mapping
existing root skills and project-local skills first. Promote a local product
skill to root `skills/` only after repeated proof shows cross-project reuse.

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
- [ ] 3. Fill the split Farplane project files.
   - [ ] Use YAML front matter plus Markdown sections in canonical project
     files; do not write fenced `harness-program` blocks to
     `farplane/harness.md`.
   - [ ] Use [templates/project-harness.md](templates/project-harness.md) only
     as a transient split-surface planning worksheet when one review artifact
     is useful.
   - [ ] Write approved static charter content to `farplane/harness.md`;
     product/team output content to `farplane/products.md`; and strategy,
     KPIs, current bets, milestone, and holds to `farplane/goals.md`.
   - [ ] Define static charter values in `harness.md`, product pipelines in
     `products.md`, strategy axes in `goals.md`, prompt cadence in
     `automations.md`, safe skill coordinates in `bindings.md`, and operator
     tickets for missing systems or gates.
   - [ ] For project-goal-shaped harnesses, keep `project` as the default durable
     planning unit and use `starting_tasks` only as hints unless a child ticket
     has a real boundary reason.
- [ ] 4. Define strategy axes, KPIs, and metric honesty.
   - [ ] Pick axes from the library: reach/acquire, activate/first value,
     retain/loyalty, refer/share, monetize/resources, impact/mission,
     deliver/quality, efficiency/capability, learning/evidence, and risk/trust.
   - [ ] For each axis, fill `strategy_state(axis, weight, current_bet, KPI,
     metric_provider, evidence, anti_metric, heartbeat, update_rule)`.
   - [ ] For every live or missing KPI source, define
     `metric_binding(metric_id, source, fetch_skill, auth_status,
     storage_path, display, proof_command)`. If the binding cannot run yet,
     record the missing credential, account, export, approval, or API reference
     as the blocker.
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
     [init-advisor](../init-advisor/SKILL.md).
   - [ ] Classify capabilities as `ready`, `needs_config`, `needs_access`,
     `needs_operator_setup`, `needs_reference`, `needs_eval`, `needs_wrapper`,
     `missing`, or `defer`.
   - [ ] Represent external data, accounts, notifications, and shared team
     systems as `skill` capabilities with required inputs, not as a separate
     external-IO concept.
   - [ ] For each feedback capability, decide whether an existing skill can
     fetch or import the signal now. If not, compile a feedback primitive plan
     before activating the harness: target skill, source docs, scripts,
     bindings, private setup, storage path, evals, QA, and proof commands.
   - [ ] Put project-specific non-secret coordinates in `farplane/bindings.md`
     rather than inventing provider-specific config files.
   - [ ] For each human access/setup/approval blocker, create or propose a
     `ticket` node with `type: unblock` instead of expanding the harness
     Markdown.
- [ ] 6. Derive local product skills after the inventory.
   - [ ] For each `farplane/products.md` product row, write
     `derive_local_product_skill(product, existing_skills, goals, constraints)
     -> reuse_map + local_skill_stub? + refinement_ticket?`.
   - [ ] Prefer reusing existing root `skills/*` and existing
     `.agents/skills/*` before proposing any new local product skill.
   - [ ] If a product workflow is repeated, valuable, and specific to this
     company, propose or create `.agents/skills/<product-skill>/SKILL.md`.
   - [ ] If the workflow is not stable enough to stub, create one product-skill
     refinement ticket that names the product line, existing skills to compose,
     missing proof, and activation gate.
   - [ ] Keep local product skills out of the reusable root `skills/` registry
     until repeated runs prove cross-project reuse.
   - [ ] Gate PM activation on each core product line having either a local
     product skill, an existing reusable skill route, or an explicit refinement
     ticket.
- [ ] 7. Define the Scrum-style operating cadence.
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
   - [ ] Use `consolidate(..., structure = skill)` to decide older
     eval/gotcha/skill-surface compaction, then
     `skill-maintenance(mode: refine_skill)` to apply accepted edits after
     hardening exists.
   - [ ] `update_system_gaps`: when no ticket can advance, inspect missing systems,
     weak metrics, stale assumptions, and safe preparation work.
   - [ ] Treat extra metric, memory, or chief-of-staff automations as optional
     escalations after the three default compiled lanes prove
     insufficient.
   - [ ] Keep all automations as `preview` or `ready_for_goal_advisor` until a
     real scheduler/automation is explicitly approved.
- [ ] 8. Choose harness levers from doctrine.
   - [ ] Use [harness-advisor](../harness-advisor/SKILL.md) when ownership is
     unclear across skill, ticket, template, docs, subagent, hook, validator,
     tool, automation, or prompt surface.
   - [ ] Prefer proof/review, ticket/program/progress, skill selection,
     references/templates, subagents, tools, validators, heartbeat, and root
     prompt in that rough order.
   - [ ] Do not expand root/global prompt unless the rule is truly global,
     durable, and expensive to recover later.
- [ ] 9. Decide missing primitive and missing system actions.
   - [ ] Use [templates/missing-primitive-plan.md](templates/missing-primitive-plan.md)
     when the gap list is material.
   - [ ] Use [skill-creator](../skill-creator/SKILL.md) only when a missing
     capability has a stable trigger and reusable workflow.
   - [ ] When the missing capability is a feedback or KPI primitive that the
     current harness needs, do not stop at a vague unblock ticket. Produce a
     `feedback_primitive_implementation_plan` with:
     trigger, input IDs or export shape, official/source grounding, private env
     keys, non-secret `farplane/bindings.md` rows, `farplane/goals.md` KPI rows,
     storage path, fetch/import scripts, normalization shape, eval rows,
     branch-scoped QA checklist, blocked-mode proof, and live-proof command.
   - [ ] If the primitive is project-specific, keep it under `.agents/skills/`
     or ticket it for project-local implementation. If repeated use across
     projects is likely, route through `skill-creator` for a root skill package
     and include the implementation plan as the handoff.
   - [ ] Otherwise choose reference, ticket, tool connector, eval, validator,
     subagent, `init-advisor`, defer-until-pilot, or no-op.
- [ ] 10. Compile the current milestone.
   - [ ] Use [templates/goal-advisor-handoff.md](templates/goal-advisor-handoff.md)
     to make the handoff explicit.
   - [ ] Use [goal-advisor](../goal-advisor/SKILL.md) only after the milestone,
     source files, metric provider, drift policy, and stop conditions are known.
   - [ ] Use [optimize-with-human](../optimize-with-human/SKILL.md) when the
     operator's labels, rankings, approval, or taste are the honest early
     metric.
- [ ] 11. Finish with proof and review.
   - [ ] Produce the split Farplane file deltas, or a transient worksheet that
     explicitly names the target files and approval gates.
   - [ ] Run [review](../review/SKILL.md) for material harness packets,
     skill-creation choices, or readiness claims.
   - [ ] State what can run autonomously now, what requires approval, what
     evidence is missing, and the exact next Goal/heartbeat/feedback route.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

Return or write:

```text
Static Charter Delta (`farplane/harness.md`):
Product Catalog Delta (`farplane/products.md`):
Product Skill Reuse Map:
Local Product Skill Stubs (`.agents/skills/<product-skill>/SKILL.md`):
Product Skill Refinement Ticket:
Strategy Delta (`farplane/goals.md`):
Planning Worksheet:
Values / Operating Principles / Priorities:
Strategy Axes / KPI Map:
Feedback Skill Loops:
Feedback Primitive Implementation Plan:
Heartbeat Preview:
Automation Manifest:
Skill Gap Map:
Missing Systems / Missing Primitives:
Operator Unblock Tickets:
Feedback Skill / Metric Plan:
Approval Gates:
Current Milestone:
Goal Advisor Handoff:
PM Activation Gate:
Autonomy Boundary:
Evidence Gap:
Next Action:
```

Default artifact paths when ticketed:

```text
tickets/TASK-XXXX/artifacts/harness-creator/
  project-harness.md              # transient worksheet, not canonical charter
  capability-map.md                 # optional sidecar when inventory is large
  missing-primitive-plan.md          # optional sidecar when gaps are material
  goal-advisor-handoff.md            # optional sidecar when milestone is ready

.agents/skills/<product-skill>/SKILL.md
                                     # project-local product workflow skill
tickets/TASK-YYYY-unblock-*.md      # preferred for human access/setup blockers
```

## Gotchas

- Split files first: `farplane/harness.md` owns static human charter content,
  `farplane/products.md` owns product catalog and work lanes, and
  `farplane/goals.md` owns dynamic strategy. A `project-harness.md` worksheet is evidence, not the
  canonical source of truth.
- Evidence first: no refinement, validation, or "business is working" claim
  without at least one honest feedback loop or a concrete feedback-skill ticket.
- Smallest lever first: check existing skills/tickets/systems before creating
  new skills, external-IO abstractions, hidden automations, or root-prompt rules.
- Local before global: product workflow skills start under `.agents/skills/`
  and promote to root `skills/` only after repeated proof of cross-project use.
- Leaf execution first: parent harnesses coordinate; native Goal runs selected
  milestones or tickets, and `pulse-update` selects one proceedable bounded
  action per beat before proactive gap work.
- Human gates first: publishing, spend, accounts, customer contact, private
  data, credentials, and feedback access become explicit gates or
  `ticket { type: unblock }` nodes.

## Reference Map

- [references/harness-il.md](references/harness-il.md) - legacy notation notes;
  use only when reading older worksheets or migrating old examples.
- [templates/project-harness.md](templates/project-harness.md) - copy only when
  a transient split-surface planning worksheet is useful.
- [templates/capability-map.md](templates/capability-map.md) - copy when the
  skill/tool/asset inventory needs its own artifact.
- [templates/missing-primitive-plan.md](templates/missing-primitive-plan.md) -
  copy when gaps need owner/action decisions.
- [templates/goal-advisor-handoff.md](templates/goal-advisor-handoff.md) - copy
  before asking `goal-advisor` to compile the selected milestone.
- [init-advisor](../init-advisor/SKILL.md) - use when a project lacks
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
