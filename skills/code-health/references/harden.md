# Harden Mode

Load after `SKILL.md` selects `harden`. Rank before patching; prove before
claiming.

## Risk model

Map the boundaries first: entry points, users and permissions, data and
secrets, dependencies and external services, runtime resources and failure
domains. Then cover, as relevant:

- input abuse: malformed, huge, repeated, reordered or replayed input;
- authn/authz: who can do what, checked at the protected action;
- secrets and data: credentials, logs, redaction, retention, transport;
- dependency and supply chain: unpinned packages, install scripts, generated
  code;
- availability: timeouts, retries, queues, rate limits, backpressure;
- concurrency and state: races, idempotency, partial writes, transactions;
- observability and recovery: audit trails, alerts, rollback, safe disable;
- configuration: least privilege, secure defaults, environment separation.

```text
priority = impact x likelihood x exploitability x feature_exposure
```

Lower priority for speculative, unreachable or already well-tested risks.
Raise it for public entry points, data mutation, secrets, money, identity,
persistence and automated agents.

## Choosing proof

- Parseable behaviour: a deterministic failing test.
- Forbidden pattern: a static-analysis rule (Semgrep, CodeQL, linters).
- Trust boundary or dependency behaviour: an integration test.
- Resilience claim: a load or failure probe, only with a safe local harness.
- Judgment-only: route to `review`.

Run the adversarial case before and after when possible, and confirm the
mitigation does not break intended behaviour.

## Tooling

Install, enable or connect nothing paid or cloud without operator approval.
Dependency advisories: npm/pnpm audit, pip-audit, OSV-Scanner. Secrets:
gitleaks or detect-secrets. Config: env schema validators. Record adopted
commands in the project's `AGENTS.md` Validation section (SAST, dependency
audit, secret scan, config validation, resilience tests, authz regression).

## Stop conditions

- No clear entry point or boundary.
- The mitigation cannot be tested or reviewed.
- It needs credentials, live service mutation, paid tooling or deploy access
  the operator has not approved.
- A runtime failure appears: switch to `debug` mode.

## Residual risk

```text
residual_risk: accepted, deferred, owner, trigger_to_revisit
```
