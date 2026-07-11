---
name: code-audit
description: "Turn a codebase, PRD, and architecture context into a ranked audit plan, improvement tickets, and routed refactoring or hardening follow-ups."
tier: 3
source: local
group: coding
template_uses:
  skill-template: "0.3.7"
  skill-eval-task: "0.2.0"
  skill-qa-checklist: "0.1.0"
  skill-surface-budget: "0.1.0"
eval: evals/evals.json
qa_checklist: qa_checklist.md
common_chains:
  after: ["goal-advisor"]
allowed-tools: Read, Glob, Grep, Bash
---

# Code Audit

## Context

Use `code-audit` when the operator wants a model-assisted top-down audit of a
working codebase for architecture, modularity, maintainability, security,
resilience, testing, or best-practice gains. The skill owns component
inventory, importance ranking, audit sequencing, ticket creation, and routed
follow-ups.

This skill does not rewrite the codebase. Route behavior-preserving structure
changes to [refactoring](../refactoring/SKILL.md), risk mitigation to
[hardening](../hardening/SKILL.md), bug diagnosis to
[runtime-debugging](../runtime-debugging/SKILL.md), proof selection to
[proof-advisor](../proof-advisor/SKILL.md), implementation planning to
[impl-plan](../impl-plan/SKILL.md), and completion judgment to
[review](../review/SKILL.md).

## Skill Signature

```text
code_audit(codebase, prd?, architecture_docs?, budget?)
  -> component_inventory + ranked_audit_plan + ticket_specs + route_map + evidence
state: reads(code, PRD/specs, architecture docs, tests, configs, dependency files, ticket history, project rules, runtime commands); writes(audit artifact?, ticket specs?, tickets?, evidence refs?)
gates: context_bound; components_ranked; architecture_first; findings_evidence_backed; owner_skill_routed; no_broad_rewrite
routes: impl-plan | refactoring | hardening | runtime-debugging | proof-advisor | testing | review
fails: whole-repo rewrite plan; unranked checklist dump; style-only churn; security theater; tickets without proof routes; hidden assumptions from chat
```

Use a compact budget only when audit breadth changes the workflow:

```text
CodeAuditBudget = {
  scope?: "smoke" | "focused" | "broad";
  evidence_depth?: "light" | "strong";
  ticket_limit?: integer;
  include_security?: boolean;
  include_refactor?: boolean;
  include_tests?: boolean;
}
```

## Phase Boundary

This skill follows Tier 0 phases inline. Call `impl-plan`, `refactoring`,
`hardening`, `proof-advisor`, `testing`, or `review` only when the child scope
is a specific ticket, module, proof question, or evidence bundle smaller than
the whole audit.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the audit target.
  - [ ] Read `qa_checklist.md` as preflight guardrails.
  - [ ] Name the codebase, PRD/spec refs, architecture refs, project rules,
    runtime commands, ticket context, non-goals, and audit budget.
  - [ ] Stop or narrow scope when the request is actually one known bug,
    one refactor target, or one hardening target.
- [ ] 2. Build the component inventory.
  - [ ] Identify product-critical workflows, entry points, modules, data
    boundaries, external dependencies, auth/secrets/config surfaces, tests,
    docs, and operational scripts.
  - [ ] Load [component ranking](references/component-ranking.md) before
    assigning priority scores.
- [ ] 3. Rank audit order.
  - [ ] Rank components by operator value, architectural centrality, blast
    radius, churn, complexity, security exposure, dependency risk, test
    weakness, and evidence confidence.
  - [ ] Keep the ranked list short enough to drive action; split broad audits
    into waves instead of pretending one pass can inspect everything deeply.
- [ ] 4. Audit architecture before modules.
  - [ ] Load [audit workflow](references/audit-workflow.md) for architecture
    and module-level checks.
  - [ ] Check boundaries, ownership, dependency direction, public contracts,
    state flow, side effects, observability, recovery, and test strategy.
- [ ] 5. Audit modules in ranked order.
  - [ ] For each finding, record evidence, impact, owner surface, proof route,
    and whether it is `refactor`, `harden`, `test`, `document`, `delete`,
    `split-ticket`, or `no-action`.
  - [ ] Route local maintainability patches to [refactoring](../refactoring/SKILL.md)
    and risk mitigations to [hardening](../hardening/SKILL.md) instead of
    embedding patch plans in the audit.
- [ ] 6. Produce ticket-backed outputs.
  - [ ] Load [ticket output](references/ticket-output.md) before creating or
    proposing tickets.
  - [ ] Create or propose one ticket per coherent improvement with scope,
    owner skill, acceptance criteria, proof, residual risk, and links to
    evidence.
  - [ ] Mark low-confidence ideas as evidence gaps, not implementation tickets.
- [ ] 7. Finish-check the audit.
  - [ ] Apply `qa_checklist.md` again to the finished output.
  - [ ] Verify the audit ranks core components, starts from architecture,
    routes execution to owner skills, avoids broad rewrites, and leaves a
    concrete next ticket.
  - [ ] Route material audit completion to [review](../review/SKILL.md) or the
    reviewer lane when the output will drive substantial implementation work.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Compact finding shape:

```text
Finding:
  component:
  rank_reason:
  evidence:
  impact:
  route: refactoring | hardening | runtime-debugging | testing | docs | no-action
  ticket:
  proof:
  residual_risk:
```

## Gotchas

- Do not create a modernization epic when the evidence supports one narrow
  refactor or hardening ticket.
- Do not count newer-model confidence as evidence; every finding needs local
  file, command, test, architecture, dependency, or ticket support.
- Do not mix audit and implementation unless the operator selects a specific
  ticket or module after the audit.

## Reference Map

- [component ranking](references/component-ranking.md) - read before scoring
  component importance or audit order.
- [audit workflow](references/audit-workflow.md) - read before architecture or
  module-level inspection.
- [ticket output](references/ticket-output.md) - read before creating or
  proposing audit follow-up tickets.

## Output

Return or write an audit artifact containing:

- target context, PRD/spec refs, architecture refs, and budget
- component inventory and ranked audit order
- architecture-level findings and module-level findings
- routed ticket specs or created ticket refs
- evidence map, proof routes, residual risks, and next owner
