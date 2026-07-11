---
template_uses:
  skill-qa-checklist: "0.1.0"
---

# Code Audit QA Checklist

Use this checklist before running a code audit and again before calling the
audit output ready. Record each item as `pass`, `violation`, `not_applicable`,
or `deferred` in the audit artifact or ticket proof notes.

## Checklist

- [ ] The audit binds local context: PRD/specs or explicit absence, architecture
  docs or explicit absence, product-critical workflows, project rules, tests,
  configs, dependencies, and ticket history.
- [ ] Component ranking is evidence-backed and action-oriented: each top
  component has paths, role, priority reason, confidence, and audit depth.
- [ ] The architecture pass happens before module tickets: boundaries,
  dependency direction, public contracts, state flow, side effects, proof, and
  operational risks are considered before local cleanup.
- [ ] Every finding has a primary owner route, proof route, evidence ref, and
  residual-risk note; low-confidence ideas remain evidence gaps.
- [ ] The output resists broad rewrite behavior: it proposes or creates
  coherent tickets and names one concrete next ticket rather than implying the
  whole codebase should be upgraded at once.
