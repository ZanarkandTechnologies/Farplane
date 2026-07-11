---
title: Code Audit Component Ranking
owner: code-audit
status: active
kind: reference
---

# Component Ranking

Use this reference after the component inventory exists and before selecting the
audit order. Ranking should make the next audit action obvious, not create a
false precision scoreboard.

```text
rank_component(component, evidence)
  -> priority + reason + confidence + audit_depth
```

## Signals

Prioritize components with more of these signals:

- Product-critical workflow: users or operators cannot receive the core value
  if this component fails.
- Architectural centrality: many modules call it, import it, configure it, or
  depend on its data contract.
- Blast radius: defects can corrupt data, break auth, leak secrets, block
  execution, or misroute work.
- Churn: recent or frequent edits suggest the boundary is active and expensive
  to maintain.
- Complexity: deep nesting, many responsibilities, weak names, hidden global
  state, or high branching.
- Security exposure: auth, secrets, filesystem, network, subprocess,
  user-supplied inputs, dependency loading, or untrusted content.
- Dependency risk: direct use of unstable APIs, pinned old packages, generated
  code, shell commands, external services, or optional credentials.
- Test weakness: no characterization tests, no smoke command, brittle fixtures,
  or missing integration proof for high-value behavior.
- Documentation mismatch: public docs, PRD, architecture docs, or tickets
  describe a different boundary than the code implements.

## Output Shape

```text
Component:
  name:
  paths:
  role:
  priority: critical | high | medium | low
  audit_depth: architecture | focused-module | smoke-only | defer
  evidence:
  confidence: high | medium | low
  why_before_other_components:
```

## Rules

- Use `critical` only when failure affects the primary product workflow,
  security boundary, data integrity, or agent/task lifecycle.
- Use `low` or `defer` for interesting cleanup that does not change operator
  value, risk, speed, or future implementation leverage.
- Prefer a short top-ranked wave over a full inventory that no one will act on.
- Preserve dissent: when a component looks important but evidence is weak,
  record an evidence gap instead of inflating confidence.
