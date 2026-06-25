---
title: "Hardening Tooling"
status: active
owner: hardening
created_at: 2026-06-25
updated_at: 2026-06-25
tags:
  - tooling
  - security
  - reliability
refs:
  - skills/hardening/SKILL.md
---

# Hardening Tooling

Choose tools by risk class. Do not install, enable, or connect paid/cloud
services without explicit operator approval.

## Static And Security Analysis

- Semgrep: custom unsafe pattern rules, SAST, framework-specific guardrails.
- CodeQL: deeper dataflow/security analysis when supported.
- SonarQube/SonarCloud: reliability, security hotspots, duplication, and
  maintainability trends.
- ESLint/TypeScript ESLint, Ruff, Pylint, Clippy, go vet: language-specific
  correctness and unsafe-pattern checks.

## Dependencies And Supply Chain

- npm audit, pnpm audit, yarn npm audit: JavaScript dependency advisories.
- pip-audit, safety, uv audit when available: Python dependency advisories.
- OSV-Scanner: cross-ecosystem dependency advisories.
- lockfile checks and package-manager frozen installs.

## Secrets And Configuration

- gitleaks or detect-secrets: secret scanning.
- dotenv/schema validators: required env vars and unsafe defaults.
- CIS Benchmarks or provider hardening guides for infrastructure configuration
  when the project owns deployment environments.

## Resilience

- unit/integration tests for timeouts, retries, idempotency, and partial
  failures.
- load or stress checks only when a safe local harness exists.
- chaos/failure injection only with scoped local fixtures or explicit approval.

## Project Rules Slots

Record adopted commands in `PROJECT_RULES.md`:

```text
Hardening:
  SAST:
  Dependency audit:
  Secret scan:
  Config validation:
  Resilience/failure tests:
  Authz/security regression tests:
```
