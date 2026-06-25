---
kind: harness-creator-worksheet
status: draft
created_at: TODO
updated_at: TODO
template_id: project-harness
template_version: "0.3.2"
feature_refs:
  - FEAT-0027
  - FEAT-0048
project_id: TODO
automation_status: preview
framework_template_version: "0.3.0"
canonical_targets:
  - farplane/harness.md
  - farplane/products.md
  - farplane/goals.md
  - farplane/automations.md
  - farplane/bindings.md
  - farplane/hooks.json
  - .agents/skills/README.md
---

# Harness Creator Worksheet

This is a transient planning worksheet. It is not a canonical project charter
and must not replace `farplane/harness.md`.

Use it to review proposed split-surface deltas before writing the standard
Farplane files:

- `farplane/harness.md` owns the static human charter: mission, human thesis,
  operating principles, non-tradeoffs, static leverage commitments, agent
  authority, allocation guardrails, and change rule.
- `farplane/products.md` owns the product catalog and work-lane weights.
- `farplane/goals.md` owns dynamic strategy, KPIs, current bets, milestone, and
  holds.
- `farplane/automations.md` owns reviewable automation prompt text.
- `farplane/bindings.md` owns non-secret project coordinates.
- `farplane/hooks.json` owns declarative project hook config.
- `.agents/skills/` owns project-local product workflow skills.

## Static Charter Delta

Target: `farplane/harness.md`

Approval required before applying changes to the human thesis, durable leverage
commitments, non-tradeoffs, agent authority, or change rule.

## Mission

TODO: why this project or business exists.

## Human Thesis

TODO: durable human thesis the agents must preserve.

## Operating Principles

- TODO: principle that should guide repeated decisions.

## Static Leverage Commitments

| Commitment | Why It Compounds | Evidence To Seek | Pivot Signal |
| --- | --- | --- | --- |
| TODO | TODO | TODO | TODO |

## Non-Tradeoffs

- TODO: what cannot be sacrificed for local wins.

## Agent Authority

- Agents may evolve products, audiences, tickets, and goals through
  evidence-backed deltas.
- Agents may challenge the static thesis with evidence.
- Agents may propose a charter delta in a dated interval report.
- Agents may not silently rewrite the static thesis or durable leverage
  commitments.

## Change Rule

Static charter changes require an explicit human-approved harness delta.
Interval reports may propose the delta, but cannot apply it silently.

## Allocation Guardrails

| Lane | Min | Max | Why |
| --- | ---: | ---: | --- |
| TODO | TODO | TODO | TODO |

## Product Catalog Delta

Target: `farplane/products.md`

Use this section for team identity, product rows, work-lane weights, and
constraints. Do not put planning algorithms or operational workflow steps in
`farplane/products.md`; those belong in skills and automation prompts.

| ID | Product | Audience | Output | Reward |
| --- | --- | --- | --- | --- |
| TODO | TODO | TODO | TODO | TODO |

| Lane | Default Weight | Purpose |
| --- | ---: | --- |
| TODO | TODO | TODO |

## Product Skill Plan

Target: `.agents/skills/<product-skill>/SKILL.md` or a refinement ticket.

Map existing reusable skills before creating local product skill stubs.

```text
derive_local_product_skills(products, existing_skills, goals, constraints)
  -> product_skill_reuse_map
   + local_product_skill_stubs?
   + product_skill_refinement_ticket?
   + pm_activation_gate
```

| Product | Existing Skill Route | Local Skill Path | Status | Next Ticket |
| --- | --- | --- | --- | --- |
| TODO | TODO | `.agents/skills/TODO/SKILL.md` | reuse / stub / refine_ticket / defer | TODO |

Promotion rule: keep product skills under `.agents/skills/` until repeated
runs prove the workflow is reusable across projects.

## Strategy Delta

Target: `farplane/goals.md`

Use this section for north star, value function, KPI axes, current bets,
current milestone, and holds. Strategy must stay inside the static charter but
is not itself the charter.

| Field | Value |
| --- | --- |
| North Star | TODO |
| Horizon | TODO |
| Metric | TODO |

| Bet | Why | Evidence | Next Review |
| --- | --- | --- | --- |
| TODO | TODO | TODO | TODO |

## Automation And Binding Delta

Targets: `farplane/automations.md`, `farplane/bindings.md`

- `automation_delta:`
- `safe_binding_delta:`
- `activation_status:` preview / needs_operator_setup / ready_for_automation_advisor
- `side_effect_gates:`

## Evidence

- `facts:`
- `research_refs:`
- `local_refs:`
- `operator_inputs:`
- `metric_sources:`

## Assumptions

- `inferred_values:`
- `inferred_products:`
- `inferred_goals:`
- `unverified_domain_claims:`
- `why_research_was_or_was_not_needed:`

## Open Questions

- `operator_decisions:`
- `permissions_or_accounts:`
- `budgets:`
- `taste_or_strategy_questions:`

## Unblock Tickets

Create tickets for each unblock/setup task that blocks the milestone,
instrumentation, memory sync, notifications, or feedback loops.

| Ticket | Type | Human Step | Enables | Fallback |
| --- | --- | --- | --- | --- |
| `tickets/TASK-XXXX-unblock-*.md` | unblock |  |  |  |

## Optional Inventory Views

Use these only when the program becomes hard to audit.

### Capability Map

| Capability | Program Node | Existing Skill / Tool | Required Input | Status | Decision |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  | ready / needs_config / needs_access / needs_operator_setup / needs_reference / needs_eval / needs_wrapper / missing / defer |  |

### Missing Systems

| System | Program Node | Evidence | Action | Owner |
| --- | --- | --- | --- | --- |
|  |  |  | use_existing / init_advisor / create_ticket / goal_advisor_handoff / defer |  |
