---
kind: bootstrap-brief
status: active
project: Farplane
created_at: 2026-06-21
updated_at: 2026-06-21
framework_template_version: "0.1.0"
owner: harness
source:
  - skills/init-advisor/SKILL.md
  - farplane/manifest.json
  - docs/farplane-framework/project-files.md
---

# Bootstrap Brief

## Summary

- Project: Farplane
- Goal: Make autonomous Codex work visible, reviewable, repeatable, and useful
  through files, tickets, skills, goals, automations, and proof.
- Audience: Kenji, Farplane operators, and agents working inside this repo.

## Intent

- Why now: Farplane is dogfooding the project substrate created by
  `init-advisor`.
- What good looks like: A new agent can find the project harness, current
  goals, automation manifest, runtime state, tickets, proof commands, and
  stop conditions without relying on transcript memory.
- Optimize for first: visible state, safe autonomous execution, focused review,
  and low-friction continuation.

## Goal Intake Status

- Current state: `farplane/goals.yaml` exists and captures the latest inferred
  Farplane operating portfolio.
- Missing setup: the operator has not yet completed a fresh goal-intake pass
  for this project bootstrap.
- Rule: do not treat the bootstrap as fully initialized until the operator's
  desired outcome, success criteria, non-goals, and decision boundaries have
  been captured and reconciled into `farplane/goals.yaml`.
- Next route: run `deep-interview --bootstrap` and then update
  `farplane/goals.yaml` through an explicit goals delta.

## Recommended Shape

- Project profile: harness repo / project operating system.
- Lifecycle route: bootstrap substrate -> goals portfolio -> ticket-backed
  Goal Packets -> review and proof.
- App type: no app scaffold; repo is an orchestration and documentation system.
- Topology recommendation: tracked `farplane/` config plus ignored
  `.farplane/` runtime state.
- Why this topology: canonical project facts stay reviewable in git while
  generated run state remains local.
- Non-goals for v1: hosted scheduler, hidden daemon, broad external mutation,
  and automatic deploy/publish/spend.

## Runtime / QA Commands

- Preferred app-only run path: none; this repo is not an app runtime.
- Preferred QA / evidence-capture run path:
  `python3 bin/validators/check_farplane_project_files.py`
- Required local services: none for framework validation.
- Process vs compose expectation: direct shell commands from repo root.
- Expected targets or base URLs: none.
- Port / env assumptions agents must honor: do not assume app ports.
- Evidence-capture notes: put bulky proof under ticket-scoped
  `tickets/TASK-XXXX/artifacts/` when a ticket owns the work.

## Validation and Hooks

- Required local checks:
  - `python3 bin/validators/check_farplane_project_files.py`
  - `python3 bin/validators/check_harness_invariants.py`
  - `python3 bin/validators/check_doc_refs.py`
  - `python3 skills/skill-maintenance/scripts/check_skills.py --write`
- Optional heavy local checks: ticket metadata checks, skill graph generation,
  eval runs, and browser proof when a ticket requires them.
- Hook policy: hooks are visible optional scaffolding, not auto-enabled.
- Hook activation choice: disabled unless the operator explicitly runs
  `git config core.hooksPath .githooks`.
- Preferred hook stages: pre-push for heavier checks; pre-commit only for fast
  mechanical checks.
- Codex SDK pre-push diff reviewer policy: optional, ticket-driven.
- Canonical TAS reviewer route: reviewer lane for material review when
  available.
- Desloppify policy: use only when cleanup is the explicit scope or a ticket
  requires it.
- Separate CI / deployment gate: no deploy/publish action without explicit
  operator approval.

## Agent Experience / Testability

- Important states the agent must reach quickly:
  - current project harness in `farplane/harness.md`
  - dynamic portfolio in `farplane/goals.yaml`
  - automation program in `farplane/automations.toml`
  - live runtime reports in `.farplane/reports/`
  - active tickets in `tickets/`
- Fast-entry surfaces to create or preserve: ticket `Done / Proof`, Goal
  Packet files, validator commands, and report paths.
- Reset / seed / fixture strategy: avoid destructive reset; create ticket-local
  fixtures or experiment artifacts when needed.
- Hidden state that needs probes, HUDs, or DOM mirrors: none by default.
- Preferred browser proof stack: delegated `qa-tester` / `agent-browser` for
  user-visible flows; direct validators for repo framework checks.
- Initial QA cookbook workflows to document: framework validation, ticket
  metadata validation, skill validation, and UI/browser proof when Farplane UI
  work is active.

## Autonomy Readiness

- Human inputs/assets needed before unattended work: ticket acceptance or an
  active Goal Packet for material changes.
- Credentials / external-service access needed: only when a ticket explicitly
  uses GitHub, Notion, Telegram, Console, analytics, deploy, or billing.
- Compute needs: local shell by default.
- Tooling gaps the agent should surface before implementation: missing
  bindings, missing Console key, unavailable thread tools, unavailable QA
  lane, or missing validator coverage.
- Hard-to-QA or hard-to-inspect surfaces: live automation behavior and
  cross-thread lineage.
- Required human gates:
  - Plan review: material architecture, workflow, public API, prompt, or
    harness-policy changes.
  - QA review: UI/user-visible work when ticket requires QA.
  - Deploy/publish: always.
  - Spend/billing: always.
  - Destructive or migration actions: always.
- Decisions the agent may make autonomously: small same-scope fixes, local
  validator hardening, ticket-scoped docs, and proof artifacts.
- Decisions that must stop and ask: durable architecture changes, live
  scheduler/automation activation, external mutation, billing, deploy, publish,
  or destructive cleanup.

## Decision Boundaries

- The scaffold may decide automatically: local file placement that already
  follows the current Farplane manifest and docs.
- Still requires confirmation: enabling hooks, activating paused automations,
  changing live cadence, adding external bindings, or mutating external systems.

## Defaults Chosen

- Recommended defaults accepted:
  - no code scaffold
  - tracked `farplane/` config
  - ignored `.farplane/` runtime state
  - local tickets first
  - Notion disabled by default
  - live side effects gated
- Explicit extensions: Farplane dogfoods richer goals and automation manifests
  than a minimal new project template.
