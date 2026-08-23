---
skill: skill-maintenance
date: 2026-08-20
change_type: maintenance
owner: skill-maintenance
status: pass
review_route: reviewer
review_tas: TAS-A
live_catalog_correction_ref: 2026-08-21-live-skill-catalog-drift.md
before_ref: skills/skill-maintenance/audits/2026-08-20-skill-portfolio-rationalization.md
after_ref: docs/skills/registry.jsonl
reasoning_basis: first_principles + operator_approval + eval + reviewer
proof_artifacts:
  - tickets/TASK-0442/artifacts/qa-report.md
  - tickets/TASK-0442/artifacts/qa/2026-08-20_223108_skill_portfolio/result.json
  - skills/research/audits/2026-08-20-merge-external-patterns.md
  - skills/consolidate/audits/2026-08-20-merge-knowledge-tidier.md
eval_required: yes
---

# Skill Portfolio Migration Audit

## Change

- Before: 125 packages shared one discovery surface, explicit-request telemetry
  recognized only seven controls, two workflows duplicated owners, and six
  native or CLI wrappers remained callable.
- After: 117 packages are classified as 42 core, 46 domain, 18 integration,
  and 11 explicit-only shortcuts; 64 configured packages load through 12
  profiles, while the base prompt exposes only core skills.
- Why: keep artifact-producing, integration, ensemble, safety, and proof
  behavior while removing duplicate or non-owning entrypoints.
- Tradeoff accepted: configured skills require an agent or named profile, and
  runtime-selected invocation count remains unavailable until Codex exposes a
  trustworthy skill-load event.
- Correction: `125` described the source portfolio. The live Codex home also
  contained nine copied packages retired by earlier commits and three nested
  test-fixture skills; TASK-0442's first pass did not inventory them because
  they were absent from the top-level source registry.

## First-Principles Reasoning

- Objective: reduce automatic context and public overlap without deleting
  unique capabilities.
- Placement logic: extend the canonical registry, existing user-turn telemetry,
  native Codex skill policy, profile config, plugin projection, and installer.
- Expected behavior delta: explicit `$name` requests are counted for every
  registry skill; shortcuts remain directly callable but never compose; domain
  and integration skills appear only in relevant profiles.
- Proof needed: transferred merge evals, registry/graph invariants, runtime
  parser tests, operated Codex prompt inspection, recoverable live retirement,
  QA evidence review, and independent completion review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Core owners retain outcome, evidence, and state contracts. |
| `reference_load_precision` | pass | Branch-only merge guidance moved to method references. |
| `missing_context_rate` | pass | Transferred merge evals retain unique source and knowledge behavior. |
| `noisy_context_rate` | pass | Base prompt excludes all 64 configured skills and 11 shortcuts. |
| `duplicated_instruction_count` | pass | Two duplicate owners and six wrapper packages are removed. |
| `prompt_size_tokens` | pass | Ordinary discovery falls from 125 packages to 42 core packages. |
| `task_success_rate` | pass | Merge candidates pass 2/2 and 2/2 against failing baselines. |
| `review_tas_rate` | pass | Whole-task completion review returned TAS-A with no hard gates. |
| `maintenance_locality` | pass | Metadata in each `SKILL.md` generates registry, profiles, graph, and plugins. |
| `composition_clarity` | pass | Shortcut edges are rejected in both directions across three edge types. |

## Proof Artifacts

- Skill-local evals: research merge 2/2 candidate versus 0/2 baseline;
  knowledge merge cases 1.0 versus 0.2 and 1.0 versus 0.125.
- Structure evals: integrated unit tests pass; post-install focused suites pass
  6 installer tests, 32 telemetry tests, and 66 registry/profile/plugin tests;
  `check_skills.py --write`, TOML parsing, and diff hygiene pass.
- Operated proof: base Codex discovery exposes `review` but not advertising or
  shortcut skills; `-p advertising-specialist` exposes `ad-advisor`,
  `ad-impl-plan`, and `meta-ads`, while still excluding `asset-advisor`.
- Live install: the eight TASK-0442 retired directories are absent from
  `/Users/kenjipcx/.codex/skills/`; stale source-deleted `update-memory` was
  also retired through the installer to
  `/Users/kenjipcx/.codex/.install-backups/20260820-222938/skills/update-memory`.
- Telemetry: registry-driven explicit requests emit `skill_requested` with
  `source=user_explicit_request` and `status=requested`; agent-selected load
  telemetry is recorded as unavailable rather than inferred.
- QA and review: implementation QA passes; whole-task completion review is
  TAS-A with no hard-gate failures.
- Evidence gaps: runtime-selected skill-load telemetry is unavailable in Codex
  0.147.0 and is deliberately not inferred.

## Before Behavior

Every installed Farplane skill could crowd ordinary discovery, prompt shortcuts
participated in automatic routing, and request heat could not cover arbitrary
registry skills.

## After Behavior

`skill_portfolio(task, profile?) -> core + configured(profile) + explicit_shortcuts`

The registry is the single classification source. Install and plugin surfaces
derive from it, shortcut sidecars prohibit implicit invocation, validators
prohibit composition edges, and explicit requests are measurable across all
117 rows.

## Followups

- Re-score usefulness after at least 30 days of corrected explicit-request
  telemetry. Treat first-window zero use as `watch`, not automatic deletion.
- Keep the installer retirement ledger as the single owner for known copied
  packages and include live/source/registry set equality in future audits.
