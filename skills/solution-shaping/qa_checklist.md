---
title: Solution Shaping QA
owner: solution-shaping
status: active
kind: qa-checklist
updated_at: 2026-07-13
---

# Solution Shaping QA

Use this as preflight and final review for material operational or demo-bound
solutions. One QA agent owns the complete review and returns one evidence-backed
`pass | revise | reject` verdict. Do not spawn a separate task for each check.

```text
review_solution_shape(brief, evidence, intended_demo?)
  -> verdict + strongest_evidence + blocking_gaps + next_owner
```

## Five Gates

1. **Decision coherence.** Confirm one actor, recurring decision, stakes,
   horizon, current workflow, and system boundary. Reject feature collections
   that do not resolve into a usable operating loop.
2. **Mechanism credibility.** Identify the calculation, optimization,
   retrieval, rule, or state transition that creates value. Require a
   deterministic owner for material facts instead of asking the language model
   to imitate specialist computation.
3. **Proof responsiveness.** Require representative inputs and a normal case,
   a binding-constraint or shortage case, and a changed-market or changed-demand
   case. State what should change and what would disprove the solution.
4. **Trust and control.** Verify provenance, assumptions, decision rights,
   permissions, failure behavior, adjacent systems, V1/V2 split, and explicit
   non-goals.
5. **Buyer reviewability.** Walk the proposed experience from input through
   mechanism, output, challenge, rerun, and next review. The buyer must be able
   to inspect why the answer changed and identify the production pilot path.

## Receipt

Return one compact receipt containing the verdict for all five gates, the
strongest observed evidence, any blocker, the scenario used to challenge the
shape, and the next owner. A numerical score may summarize discussion, but it
must not replace gate-level reasons.
