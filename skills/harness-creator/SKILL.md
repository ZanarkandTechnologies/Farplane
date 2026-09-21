---
name: harness-creator
description: "Turn a high-level project or business idea into a Farplane charter, metric objectives, capability handoffs, and executable starter tickets."
tier: 3
group: operations
source: local
template_uses:
  skill-template: "0.2.0"
  skill-eval-task: "0.2.0"
allowed-tools: Read, Write, Glob, Grep, Bash, web_search
---

# Harness Creator

## Context

Use for a high-level project, business, channel, academy, research, product,
ecommerce, or internal-ops idea that needs an operating harness before work.
`init-advisor` is the public setup entrypoint and calls this in `full` mode;
call directly only for explicit redesign, advanced operating-program work, or
an existing project with substrate files.

The durable result is a split Farplane delta: `farplane/harness.yaml` owns
identity, planning areas, capability and metric refs, constraints, authority,
and change rule; `farplane/metrics.yaml` owns reusable metric definitions;
`farplane/bindings.yaml` owns non-secret provider coordinates; tracked
`farplane/automations/` owns approved cadence; `.agents/skills/` owns
project-specific capability workflows. Use `templates/project-harness.md` only
as a transient review worksheet, never as a replacement charter.

Start experimental: build the smallest evidence-producing harness and
feedback-sized tickets, then expand after review or feedback.

## Skill Signature

```text
project_harness_creator(project_idea, values?, priorities?, mode_presets?, context?, constraints?, budget?)
  -> split_file_deltas + capability_skill_reuse_map + proposed_tickets
     + initial_metric_objectives + goal_advisor_handoff | blocked_report
reads: operator inputs; project files, tickets, skills, registry, local evidence;
       current external evidence only when domain truth changes the first loop
does: designs the project operating model and routes only narrower specialist work
writes: proposed deltas; approved project files, local-skill stubs, or tickets
returns: charter/metric/capability/feedback decisions, proof, and next owner
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Bind intent, authority, and discovery depth.**
  `idea + values + constraints -> mode + authority + evidence need | readiness gap`

  Rule: State an outcome, values, priorities, non-tradeoffs, mode preset, and
  safety gates for publishing, spend, accounts, customer contact, scraping,
  payments, legal/brand, and private data. Mark inferred values; without an
  approved gate, assume no external side effect. Use known templates first;
  use [competitor-research](../competitor-research/SKILL.md),
  [implementation-research](../implementation-research/SKILL.md), or
  [experimental-research](../experimental-research/SKILL.md) only when that
  specific evidence changes the first honest feedback loop.

  Assert: Missing human thesis, non-goals, or authority produces one compact
  question or a readiness gap; safe inspection may continue, but not completion.

- [ ] **N2 — Inventory state and draft the canonical split.**
  `existing work + evidence -> charter/metrics/bindings/cadence delta | unblock`

  Rule: Check proceedable tickets, `docs/skills/registry.jsonl`, root and local
  skills, docs, assets, and standard systems before inventing. Classify each
  capability `ready | needs_config | needs_access | needs_operator_setup |
  needs_reference | needs_eval | needs_wrapper | missing | defer`; use
  [init-advisor](../init-advisor/SKILL.md) if substrate is absent. Use typed
  YAML, never a Markdown charter or compatibility `harness-program` surface.
  Keep selected metric IDs/priorities in `harness.yaml`; label, unit/kind/
  display, direction, freshness, and guards in `metrics.yaml`; provider setup
  in `bindings.yaml`; and temporary commitments in tickets. Route detailed
  metric or guard design to the specialist in the Reference Map when needed.

  Assert: Every live KPI has an honest provider; otherwise name the missing
  credential, account, export, approval, API, or instrumentation and its unblock.

- [ ] **N3 — Establish feedback and capability ownership.**
  `inventory + objectives -> reuse map + feedback loop + local-skill/ticket plan`

  Rule: Reuse root and `.agents/skills/` workflows before proposing a local
  capability skill. Stub `.agents/skills/<capability>/SKILL.md` only for a
  repeated, valuable company-specific output; otherwise create a refinement
  ticket. Keep it local until repeated cross-project proof supports promotion.
  Each required recurring output needs a reusable route, local skill, or
  refinement ticket before PM activation. Model external data, accounts,
  notifications, and shared systems as skill capabilities with required inputs.
  Missing instrumentation requires an explicit feedback capability and unblock
  ticket, not a claimed metric.

  Assert: A missing feedback/KPI primitive names trigger, input/export shape,
  source grounding, private setup, bindings/metric deltas, storage and
  normalization, eval/branch guards, blocked proof, live proof, and owner.

- [ ] **N4 — Choose the smallest operating surfaces and cadence.**
  `capability plan + blockers -> heartbeat/automation/maintenance policy`

  Rule: Use one `pulse-update` heartbeat for board reconciliation and bounded
  dispatch; use Feed Scout, Company OS Daily/Weekly, and Dogfood as
  report/context lanes. `pm-daily` and `pm-weekly` maintain project memory and
  may propose exact existing-issue updates but do not admit or dispatch work;
  `dogfood-review` emits bounded candidates. When no ticket can
  advance, inspect missing systems, weak metrics, stale assumptions, and safe
  preparation work. Keep automations
  `preview` or `ready_for_goal_advisor` until explicit scheduler approval, and
  use `delegate(context_ref, task_prompt, skills?, output?)` only with a durable
  context reference. For unclear owner placement, use
  [harness-advisor](../harness-advisor/SKILL.md); prefer existing proof,
  tickets, skills, references, tools, and validators before new automation or
  root-prompt rules.

  Rule: Route durable procedures to `skill-maintenance`, documents to
  `doc-advisor`, and sourced entities to `manage-wiki`. Harden fresh
  lessons first; for old eval/gotcha/skill-surface compaction, make an inline
  `keep | merge | move | delete` decision and run a preservation/loss check,
  then use `skill-maintenance(mode: refine_skill)` for accepted edits.

  Assert: No hidden runtime, controller, extra heartbeat, or PM loop bypasses
  the capability and approval gates.

- [ ] **N5 — Compile bounded starter tickets and hand off with proof.**
  `approved harness delta + selected milestone -> executable tickets + next owner`

  Rule: Turn every access/setup/approval blocker into `ticket { type: unblock }`.
  Choose an existing capability, reference, tool, eval, validator, subagent,
  [skill-creator](../skill-creator/SKILL.md), or defer before creating a new
  primitive. Use `templates/goal-advisor-handoff.md`; invoke
  [goal-advisor](../goal-advisor/SKILL.md) only after a selected ticket, source,
  metric provider, drift policy, stop conditions, and proof boundary are known.
  Use [optimize-with-human](../optimize-with-human/SKILL.md) when human labels
  are the honest early metric; use [review](../review/SKILL.md) for material
  harness, capability, or readiness claims.

  Assert: State what is autonomous now, what needs approval, missing evidence,
  PM activation status, and the exact next Goal, heartbeat, or feedback route.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

Return or write the approved subset of:

```text
Typed Charter / Area-Capability-Metric Selection Delta: farplane/harness.yaml
Metric Objective Delta: farplane/metrics.yaml
Binding and Automation Manifest Delta: farplane/bindings.yaml, automations/
Capability Skill Reuse Map; Local Skill Stubs or Refinement Ticket
Values, Priorities, Strategy Axes, KPI Map, and Feedback Skill Loops
Feedback Primitive Plan; Missing-System and Operator-Unblock Tickets
Transient Planning Worksheet; Approval Gates; Milestone; PM Activation Gate
Evidence Gap; Autonomy Boundary; Goal Advisor Handoff; Next Action
```

Ticketed artifacts may use `tickets/TASK-XXXX/artifacts/harness-creator/` for
the transient worksheet, capability map, missing-primitive plan, and handoff.

## Gotchas

- A worksheet is evidence, not the charter; keep split-file ownership intact.
- Do not create a Markdown charter or `harness-program` compatibility surface.
- Do not invent human thesis, durable authority, publishing, spend, contact,
  credentials, or feedback access.
- Do not claim refinement or business success without an honest feedback loop
  or concrete feedback-capability ticket.
- Do not create controllers, area-local planners, hidden automations, or a
  native Goal inside this skill; selected tickets are handed to Goal Advisor.
- Keep project-specific capabilities local until repeated cross-project proof.

## Reference Map

- [project-harness worksheet](templates/project-harness.md) — transient review.
- [capability map](templates/capability-map.md) — large inventory only.
- [missing primitive plan](templates/missing-primitive-plan.md) — material gaps.
- [Goal Advisor handoff](templates/goal-advisor-handoff.md) — selected ticket.
- [metric-advisor](../metric-advisor/SKILL.md) — deep metric or guard design.
- [faceless AI channel example](examples/faceless-ai-channel.md) — pilot case.
