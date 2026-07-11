---
name: hardening
version: 0.1.0
description: "Turn working software into lower-risk software with threat, failure, abuse, and resilience proof."
tier: 2
source: local
template_uses:
  skill-template: "0.3.2"
allowed-tools: Read, Glob, Grep, Bash
eval: evals/evals.json
---

# Hardening Skill

## Context

Use this after a feature works when the next question is whether it survives
abuse, bad inputs, dependency failures, overload, unsafe configuration, or
operational surprises. The skill owns risk mapping, mitigation planning,
adversarial tests, hardening changes, and residual-risk reporting.

Route behavior-preserving structure cleanup to `refactoring`, bug diagnosis to
`runtime-debugging`, broad proof selection to `proof-advisor`, test execution
choices to `testing`, and budget resolution to `budget-advisor`.

## Skill Signature

```text
hardening(target, context?, budget?) -> risk_map + mitigations + adversarial_tests + proof + residual_risk
state: reads(code, config, dependencies, logs, tests, docs, threat boundaries, runtime commands); writes(mitigations?, tests?, evidence?, follow-up tickets?)
gates: boundary_mapped; risks_prioritized; mitigations_tested; residual_risk_named
routes: budget-advisor | proof-advisor | testing | review | runtime-debugging | refactoring
fails: generic checklist dump; untested mitigation; security theater; hidden residual risk
```

Use `budget-advisor` when `budget` is present:

```text
HardeningBudget = {
  mode?: "base" | "plus" | "max",
  available_time?: string,
  persona_count?: 1 | 3 | 5,
  personas?: HardeningPersona[],
  coverage?: "smoke" | "focused" | "broad",
  evidence_depth?: "light" | "strong",
  delegate_budget?: Record<skill_name, BudgetRequest>
}
```

Child skills use their own base reviewed path unless `delegate_budget`
explicitly names them. Budgeted persona lanes must preserve the output contract:
risk map, mitigations, adversarial tests, proof, and residual risk.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the hardening target.
  - [ ] Name the feature, entry points, trust boundaries, data, users,
    dependencies, runtime environment, and success criteria.
  - [ ] Stop or reroute when the request is primarily refactoring, debugging,
    or feature design.
- [ ] 2. Load the right references.
  - [ ] Read [risk-model](references/risk-model.md) before ranking risks.
  - [ ] Read [workflow](references/workflow.md) for the normal hardening loop.
  - [ ] Read [tooling](references/tooling.md) when selecting static-analysis,
    SAST, dependency, or resilience checks.
- [ ] 3. Resolve budget when present.
   - [ ] Call `budget-advisor` with this contract and `HardeningBudget`.
  - [ ] For `plus` or `max`, use persona prompts from
    [budget-personas](references/budget-personas.md) unless the caller supplied
    complete personas.
  - [ ] Do not copy the parent budget into proof, testing, or review child
    calls unless `delegate_budget` explicitly names the child skill.
- [ ] 4. Build a risk map.
  - [ ] Cover input validation, authn/authz, secrets, data protection,
    dependency/supply chain, availability, concurrency, observability,
    recovery, and unsafe configuration as relevant.
  - [ ] Prioritize realistic risks by impact, likelihood, exploitability, and
    evidence.
- [ ] 5. Add or propose mitigations and adversarial proof.
  - [ ] Prefer deterministic tests, static checks, validators, or runtime
    probes when possible.
  - [ ] Use `proof-advisor` when the right proof surface is unclear.
  - [ ] Avoid broad hardening patches with no failing or adversarial case.
- [ ] 6. Verify and report.
  - [ ] Re-run relevant checks and adversarial tests.
  - [ ] Report mitigations, exact proof, residual risk, and follow-up owner.
  - [ ] Route material completion to `review` or the reviewer lane.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

```text
HardeningPersona = {
  name: string,
  prompt: string,
  focus: string[],
  avoid?: string[],
  output_shape?: string
}
```

## Gotchas

- Do not claim hardening from a checklist alone; a mitigation needs proof or an
  explicit residual-risk note.
- Do not hide security, reliability, or operational residual risk because it is
  uncomfortable.
- Do not install or enable external scanners, paid services, cloud resources, or
  live automations without explicit operator approval.

## Reference Map

- [risk-model](references/risk-model.md) - read before ranking hardening work.
- [workflow](references/workflow.md) - read for the ordered hardening loop.
- [tooling](references/tooling.md) - read when choosing stack-specific
  hardening tools or commands.
- [budget-personas](references/budget-personas.md) - read for `plus` or `max`
  persona councils.
- [budget-advisor](../budget-advisor/SKILL.md) - read when `budget` is present.
- [proof-advisor](../proof-advisor/SKILL.md) - route proof-surface uncertainty.
- [testing](../testing/SKILL.md) - route proof command selection.

## Output

Return or update an artifact with:

- hardening target and trust/failure boundaries
- budget program summary when budget was used
- prioritized risk map
- mitigations or mitigation plan
- adversarial tests and exact proof
- residual risk and follow-up owner
- review or escalation note
