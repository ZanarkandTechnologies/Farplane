---
title: "Hardening Risk Model"
status: active
owner: hardening
created_at: 2026-06-25
updated_at: 2026-06-25
tags:
  - hardening
  - risk
refs:
  - skills/hardening/SKILL.md
---

# Hardening Risk Model

Use this model to rank work before patching.

```text
residual_risk_score(surface) =
  trust_boundary
+ input_abuse
+ authn_authz
+ secrets_data
+ dependency_supply_chain
+ availability_overload
+ concurrency_state
+ observability_response
+ recovery_rollback
+ unsafe_configuration
```

## Risk Dimensions

- Trust boundary: user, network, file, subprocess, model/tool, database, or
  service boundary.
- Input abuse: malformed, malicious, huge, repeated, reordered, or replayed
  input.
- Authn/authz: who can do what, and whether checks happen at the right layer.
- Secrets/data: credentials, private data, logs, redaction, retention, and
  transport.
- Dependency/supply chain: unpinned packages, unsafe APIs, generated code,
  binaries, and install scripts.
- Availability/overload: timeouts, retries, queues, rate limits, backpressure,
  graceful degradation, and capacity assumptions.
- Concurrency/state: races, idempotency, locks, partial writes, and transaction
  boundaries.
- Observability/response: logs, metrics, alerts, auditability, and incident
  recovery evidence.
- Recovery/rollback: migration rollback, feature flags, backups, and safe
  disable paths.
- Configuration: least privilege, secure defaults, environment separation, and
  accidental exposure.

## Prioritization

```text
priority = impact * likelihood * exploitability * feature_exposure
```

Reduce priority when a risk is speculative, unreachable, or already covered by
strong tests and controls. Increase priority for public entry points, data
mutation, secrets, money, identity, persistence, and automated agents.

## Residual Risk

Always report what remains:

```text
residual_risk:
  accepted:
  deferred:
  owner:
  trigger_to_revisit:
```
