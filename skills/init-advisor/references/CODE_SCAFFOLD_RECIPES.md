---
kind: init-advisor-reference
owner: init-advisor
status: active
---

# Code Scaffold Recipes

Load this reference only when `include_code_scaffold == true`, when the user
asks which stack InitAdvisor can scaffold, or when stack setup commands need
review.

```text
code_scaffold(project_root, stack_profile?, package_manager?, ui?, backend?,
              auth?, theme?, existing_app?, include_code_scaffold?)
  -> stack_command? + skipped_reason? + human_gates + runtime_command_notes
```

## Convex + Next.js + Clerk

```bash
pnpm create convex@latest . -- -t nextjs-clerk
```

- First `pnpm dlx convex@latest dev` cloud setup is interactive and must be run
  by a human.

## Plain Next.js + shadcn UI Baseline

```bash
pnpm create next-app@latest . --ts --tailwind --eslint --app --src-dir
pnpm dlx shadcn@latest init
pnpm dlx shadcn@latest add https://tweakcn.com/r/themes/darkmatter.json
```

## Convex In An Existing Project

```bash
pnpm add convex
pnpm dlx convex@latest dev
```

## Optional Quality Tooling Slots

Record adopted commands in `PROJECT_RULES.md`; install only when the operator
or selected stack setup explicitly includes those tools.

- JavaScript / TypeScript: ESLint or Oxlint, TypeScript checks, jscpd,
  dependency-cruiser or Madge, Knip or depcheck, static analysis dashboard,
  mutation testing for high-budget proof, Semgrep, CodeQL, SonarQube, and
  dependency audit commands.
- Python: Ruff, Radon, mypy or pyright, vulture, pip-audit or uv audit,
  Semgrep, CodeQL, SonarQube, and mutation testing only for high-budget proof.
- Cross-stack hardening: secret scanning, config validation, dependency audit,
  and resilience/failure tests when the project owns the relevant runtime.

## Gates

- Run stack commands only when `include_code_scaffold == true`.
- Stop for interactive setup, credentials, billing, deploys, cloud project
  creation, or other external side effects.
- Record canonical app-only and QA/evidence run commands in `PROJECT_RULES.md`,
  `docs/bootstrap-brief.md`, and the relevant `qa/` cookbook page.
- Route behavior-preserving cleanup to `refactoring`; route risk-reduction work
  to `hardening`.
