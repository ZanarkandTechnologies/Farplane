---
title: "Refactoring Tooling"
status: active
owner: refactoring
created_at: 2026-06-25
updated_at: 2026-06-25
tags:
  - tooling
  - static-analysis
refs:
  - skills/refactoring/SKILL.md
---

# Refactoring Tooling

Choose tools by stack and by the smell being investigated. Do not install tools
without operator approval or a project setup ticket.

## JavaScript / TypeScript

- ESLint or TypeScript ESLint: complexity, max-depth, no restricted imports,
  no floating promises, React hooks rules.
- Oxlint: fast lint coverage for many ESLint-compatible rules.
- Knip or depcheck: unused exports and dependencies.
- dependency-cruiser or Madge: cycles and ownership boundaries.
- jscpd: duplicate code detection.
- Stryker: mutation testing for high-budget proof.

## Python

- Ruff: fast linting and many quality rules.
- Radon: cyclomatic complexity and maintainability index.
- mypy or pyright: type coverage and exported API confidence.
- vulture: dead code discovery.
- mutmut or cosmic-ray: mutation testing for high-budget proof.

## Cross-Language

- SonarQube or SonarCloud: maintainability, code smells, duplication,
  complexity, coverage, and new-code tracking.
- Semgrep: custom structural rules and unsafe API patterns.
- CodeQL: deeper security/dataflow findings when available.
- cloc/scc/tokei: size inventory only; never as a standalone quality score.

## Project Rules Slots

Record adopted commands in `PROJECT_RULES.md`:

```text
Maintainability:
  Lint:
  Complexity:
  Duplication:
  Dependency boundaries:
  Dead code:
  Mutation testing:
  Static analysis dashboard:
```
