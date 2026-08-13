---
title: Lean Check QA Checklist
owner: lean-check
status: active
kind: qa-checklist
applies_to: [lean-receipts, implementation-plans]
---

# Lean Check QA Checklist

Read before returning a lean receipt and apply again when the receipt gates a
material implementation plan.

```text
lean_check_qa(target, receipt, local_evidence) -> pass | revise | block
```

## Checklist

- [ ] The current need is concrete; speculative work receives `skip`.
- [ ] Local reuse and relevant standard, platform, and installed-dependency
  options were inspected before new code was selected.
- [ ] The receipt names one first sufficient rung and evidence for it.
- [ ] The smallest next action preserves correctness, safety, accessibility,
  migration obligations, and required proof.
- [ ] A material plan consumes the receipt without creating a parallel ticket
  schema or a numeric leanness score.

## Finish Gate

```text
lean_receipt_qa:
  need: pass | revise | block
  first_sufficient_rung: pass | revise | block
  evidence: pass | revise | block
  proof_preserved: pass | revise | block
  integration: pass | revise | block
  highest_risk:
  exact_fix_or_deferral:
```
