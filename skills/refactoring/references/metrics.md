---
title: "Maintainability Metrics"
status: active
owner: refactoring
created_at: 2026-06-25
updated_at: 2026-06-25
tags:
  - metrics
  - maintainability
refs:
  - skills/refactoring/SKILL.md
---

# Maintainability Metrics

Use metrics to prioritize refactoring, not to replace judgment.

```text
smell_score(file_or_unit) =
  complexity
+ size
+ nesting
+ duplication
+ churn
+ coverage_gap
+ lint_static_issues
+ boundary_violations
+ security_reliability_findings
```

## Primary Target

Optimize first for changed or high-churn code:

```text
priority = smell_score * change_frequency * feature_relevance
```

This avoids spending max budget beautifying stable old code that nobody touches.

## Good Signals

- Cognitive complexity: local reasoning cost.
- Cyclomatic complexity: branch count and path risk.
- Nesting depth: hidden edge cases and hard-to-read control flow.
- Function/file length: crude size pressure; use as a smell, not a law.
- Duplication: risk of divergent bug fixes.
- Churn: where maintainability pain repeatedly hits.
- Coverage gap: risky code without proof.
- Lint/static-analysis issues: typed, async, import, unsafe API, or language
  problems.
- Boundary violations: imports or calls crossing module ownership rules.
- Security/reliability findings: issues that should route or be co-owned with
  `hardening`.

## Anti-Gaming Rules

- Do not split one clear function into scattered helpers only to reduce line
  count.
- Do not hide complexity behind generic utility modules.
- Do not lower duplication by creating an over-general abstraction with unclear
  callers.
- Do not treat coverage percentage as proof when assertions are weak.
- Do not optimize all metrics equally; prioritize the metric that matches the
  current maintenance pain.

## Reporting

Use a small delta table:

```text
metric_delta:
  target:
  before:
  after:
  proof:
  tradeoff:
```
