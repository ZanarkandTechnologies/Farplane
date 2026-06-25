---
title: "Hardening Workflow"
status: active
owner: hardening
created_at: 2026-06-25
updated_at: 2026-06-25
tags:
  - hardening
  - workflow
refs:
  - skills/hardening/SKILL.md
---

# Hardening Workflow

Use this reference after `SKILL.md` selects a normal hardening branch.

```text
hardening_loop(target, risk_model, proof)
  -> risk_map + mitigations + adversarial_tests + proof + residual_risk
```

## Loop

1. Map boundaries.
   - entry points
   - users and permissions
   - data and secrets
   - dependencies and external services
   - runtime resources and failure domains
2. Rank risks.
   - use the risk model
   - include evidence for why a risk is realistic
   - separate severe reachable risks from generic checklist items
3. Choose proof.
   - deterministic test for parseable behavior
   - static-analysis rule for forbidden patterns
   - integration test for trust boundary or dependency behavior
   - load/failure probe for resilience claims
   - review when judgment is required
4. Add mitigations.
   - validate and normalize input
   - enforce authz near the protected action
   - remove or protect secrets
   - add timeouts, backoff, idempotency, or rate limits
   - harden configuration defaults
   - add logs or audit trails where response matters
5. Verify.
   - run the adversarial case before and after when possible
   - prove the mitigation works
   - ensure the mitigation did not break intended behavior
6. Report.
   - risk map
   - mitigations
   - proof
   - residual risk
   - follow-up tickets when the risk is real but out of scope

## Stop Conditions

- The target has no clear entry point or boundary.
- A proposed mitigation cannot be tested or reviewed.
- The work needs credentials, live service mutation, paid tooling, or deploy
  access not approved by the operator.
- A runtime failure appears; route to `runtime-debugging`.
