---
kind: harness-creator-worksheet
status: draft
created_at: TODO
updated_at: TODO
template_id: project-harness
template_version: "0.3.9"
feature_refs:
  - FEAT-0007
project_id: TODO
automation_status: preview
framework_template_version: "0.3.0"
canonical_targets:
  - farplane/harness.yaml
  - farplane/metrics.yaml
  - farplane/automations.toml
  - farplane/bindings.yaml
  - farplane/hooks.json
  - .agents/skills/README.md
---

# Harness Creator Worksheet

This is a transient planning worksheet. It is not a canonical project charter
and must not replace `farplane/harness.yaml`.

Use it to review proposed split-surface deltas before writing the standard
Farplane files:

- `farplane/harness.yaml` owns identity, planning areas and instructions,
  feature meaning, selected metric refs, capability refs, constraints, authority, and
  change rule.
- `farplane/metrics.yaml` owns provider-independent metric meaning, direction,
  freshness, and optional guard rules. The planner owns trajectory comparison.
- `farplane/automations.toml` owns reviewable full Codex automation config.
- `farplane/bindings.yaml` owns non-secret project/provider coordinates and
  coordinates; `farplane/metrics.yaml` owns grouped refresh prompts.
- `farplane/hooks.json` owns declarative project hook config.
- `.agents/skills/` owns project-local capability workflows.

## Static Charter Delta

Target: `farplane/harness.yaml`

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

- Agents may evolve capabilities, audiences, tickets, and metric objectives through
  evidence-backed deltas.
- Agents may challenge the static thesis with evidence.
- Agents may propose a charter delta in a dated interval report.
- Agents may not silently rewrite the static thesis or durable leverage
  commitments.

## Change Rule

Static charter changes require an explicit human-approved harness delta.
Interval reports may propose the delta, but cannot apply it silently.

## Allocation Guardrails

| Area | Min | Max | Why |
| --- | ---: | ---: | --- |
| TODO | TODO | TODO | TODO |

## Capability Skill Plan

Targets: stable capability refs in `farplane/harness.yaml`, reusable `skills/*`,
project-local `.agents/skills/<capability>/SKILL.md`, or a refinement ticket.

Map existing reusable skills before creating local capability skill stubs.

```text
derive_local_capability_skills(recurring_outputs, existing_skills, metric_objectives, constraints)
  -> capability_skill_reuse_map
   + local_capability_skill_stubs?
   + capability_skill_refinement_ticket?
   + pm_activation_gate
```

| Recurring Output | Existing Skill Route | Local Skill Path | Status | Next Ticket |
| --- | --- | --- | --- | --- |
| TODO | TODO | `.agents/skills/TODO/SKILL.md` | reuse / stub / refine_ticket / defer | TODO |

Promotion rule: keep project-specific capability skills under `.agents/skills/` until repeated
runs prove the workflow is reusable across projects.

## Metric Selection And Definition Delta

Targets: `farplane/harness.yaml`, `farplane/metrics.yaml`

Use this section for selected objective/guard refs and priorities in the
harness, plus direction, freshness, and guard rules in metric definitions.
Human meaning and unmeasured hard constraints stay in the typed charter.

| Field | Value |
| --- | --- |
| Objective metric | TODO |
| Direction | maximize / minimize |
| Guard | TODO |

| Proposal dimension | Why | Evidence | Next Review |
| --- | --- | --- | --- |
| TODO | TODO | TODO | TODO |

## Metric, Automation, And Binding Delta

Targets: `farplane/metrics.yaml`, `farplane/automations.toml`,
`farplane/bindings.yaml`

- `metric_definition_delta:`
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
- `inferred_capabilities:`
- `inferred_metric_objectives:`
- `unverified_domain_claims:`
- `why_research_was_or_was_not_needed:`

## Open Questions

- `operator_decisions:`
- `permissions_or_accounts:`
- `budgets:`
- `taste_or_strategy_questions:`

## Unblock Tickets

Create tickets for each unblock/setup task that blocks an admitted ticket,
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
