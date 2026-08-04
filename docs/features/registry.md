---
title: "Generated Feature Registry"
status: generated
owner: feature-registry
updated_at: 2026-08-04
refs:
  - docs/features/registry.jsonl
  - docs/features/validate_features.py
---

# Generated Feature Registry

This file is generated. Edit the feature specs in `docs/features/` instead.

| Feature | System | Status | Experimental | Superseded By | Category |
| --- | --- | --- | --- | --- | --- |
| [FEAT-0007 Ticket as durable task memory](../features/FEAT-0007-ticket-as-durable-task-memory.md) | [Work Loop](../systems/work-loop.md) | `implemented` | `false` | `false` | `memory` |
| [FEAT-0008 Artifact-first QA and completion proof](../features/FEAT-0008-artifact-first-qa-and-completion-proof.md) | [Proof And Review](../systems/proof-review.md) | `implemented` | `false` | `false` | `proof` |
| [FEAT-0011 Harness scout source ingestion](../features/FEAT-0011-harness-scout-source-ingestion.md) | [Source And Sidecar Systems](../systems/source-sidecar-systems.md) | `implemented` | `false` | `false` | `source-ingestion` |
| [FEAT-0014 Frontend skill parity upgrade](../features/FEAT-0014-frontend-skill-parity-upgrade.md) | [Domain Skill Families](../systems/domain-skill-families.md) | `retired` | `false` | `false` | `frontend-skills` |
| [FEAT-0015 Retired Symphony-compatible invocation contract](../features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md) | [Retired Invocation Runtime](../systems/invocation-runtime.md) | `retired` | `false` | `false` | `execution` |
| [FEAT-0022 Skill tier leverage classes](../features/FEAT-0022-skill-tier-leverage-classes.md) | [Skill System](../systems/skill-system.md) | `implemented` | `false` | `false` | `skills` |
| [FEAT-0025 Retired video-to-skill source reconstruction](../features/FEAT-0025-video-to-skill-source-reconstruction.md) | [Source And Sidecar Systems](../systems/source-sidecar-systems.md) | `retired` | `false` | `false` | `source-ingestion` |
| [FEAT-0029 Retired Goal Packet architecture](../features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md) | [Horizon Loop](../systems/horizon-loop.md) | `retired` | `false` | `FEAT-0032` | `planning` |
| [FEAT-0030 On-demand skill plugin packaging](../features/FEAT-0030-on-demand-skill-plugin-packaging.md) | [Skill System](../systems/skill-system.md) | `implemented` | `false` | `false` | `skills` |
| [FEAT-0031 Retired agent behavior test workflow](../features/FEAT-0031-agent-behavior-test-workflow.md) | [Proof And Review](../systems/proof-review.md) | `retired` | `false` | `FEAT-0039` | `proof` |
| [FEAT-0032 Goal Advisor execution loop](../features/FEAT-0032-goal-advisor-execution-compilation.md) | [Horizon Loop](../systems/horizon-loop.md) | `implemented` | `false` | `false` | `execution` |
| [FEAT-0034 Adversarial agent QA test skill](../features/FEAT-0034-adversarial-agent-qa-test-skill.md) | [Proof And Review](../systems/proof-review.md) | `implemented` | `false` | `false` | `proof` |
| [FEAT-0039 Farplane evals](../features/FEAT-0039-behavior-correction-hardcase-metadata-and-narrow-eval-capture.md) | [Proof And Review](../systems/proof-review.md) | `implemented` | `false` | `false` | `proof` |
| [FEAT-0042 Retired lean global agent operating kernel](../features/FEAT-0042-lean-global-agent-operating-kernel.md) | [Agent Kernel](../systems/agent-kernel.md) | `retired` | `false` | `false` | `context-routing` |
| [FEAT-0043 Retired project-level system prompt eval suite](../features/FEAT-0043-project-level-system-prompt-eval-suite.md) | [Proof And Review](../systems/proof-review.md) | `retired` | `false` | `FEAT-0039` | `proof` |
| [FEAT-0054 Retired modular skill-local eval tasks](../features/FEAT-0054-modular-skill-local-eval-tasks.md) | [Proof And Review](../systems/proof-review.md) | `retired` | `false` | `FEAT-0039` | `proof` |
| [FEAT-0056 Tasty Pack inspiration vault](../features/FEAT-0056-inspiration-vault.md) | [Content Production](../systems/content-production.md) | `implemented` | `false` | `false` | `content-production` |
| [FEAT-0057 Skill-local QA checklist artifacts](../features/FEAT-0057-skill-local-qa-checklist-artifacts.md) | [Skill System](../systems/skill-system.md) | `implemented` | `false` | `false` | `skills` |
| [FEAT-0060 Registry-backed documentation OS](../features/FEAT-0060-registry-backed-documentation-os.md) | [Documentation OS](../systems/documentation-os.md) | `implemented` | `false` | `false` | `context-routing` |
| [FEAT-0061 Farplane adoption tracker CLI](../features/FEAT-0061-farplane-adoption-tracker-cli.md) | [Maintenance And Release OS](../systems/maintenance-release-os.md) | `implemented` | `false` | `false` | `proof` |
| [FEAT-0062 Capped skill surface budget](../features/FEAT-0062-capped-skill-surface-budget.md) | [Skill System](../systems/skill-system.md) | `implemented` | `false` | `false` | `skills` |
| [FEAT-0063 Metric advisor cards](../features/FEAT-0063-metric-advisor-cards.md) | [Self-Improvement And Learning](../systems/self-improvement-learning.md) | `implemented` | `false` | `false` | `skills` |
| [FEAT-0064 Skill signals](../features/FEAT-0064-skill-signals.md) | [Skill System](../systems/skill-system.md) | `implemented` | `false` | `false` | `skills` |
| [FEAT-0065 Pulse and interval automation](../features/FEAT-0065-pulse-and-interval-automation.md) | [Horizon Loop](../systems/horizon-loop.md) | `retired` | `false` | `FEAT-0067`, `FEAT-0071` | `planning` |
| [FEAT-0066 Product-scoped Pulse loops](../features/FEAT-0066-product-scoped-pulse-loops.md) | [Horizon Loop](../systems/horizon-loop.md) | `retired` | `false` | `FEAT-0071` | `planning` |
| [FEAT-0067 Daily and weekly control-loop reviews](../features/FEAT-0067-daily-interval-review-reports.md) | [Horizon Loop](../systems/horizon-loop.md) | `implemented` | `true` | `false` | `planning` |
| [FEAT-0068 Goal-backed ticket execution](../features/FEAT-0068-goal-backed-ticket-execution.md) | [Work Loop](../systems/work-loop.md) | `implemented` | `true` | `false` | `execution` |
| [FEAT-0069 Retired Taste Loop human-feedback optimization](../features/FEAT-0069-taste-loop-human-feedback-optimization.md) | [Self-Improvement And Learning](../systems/self-improvement-learning.md) | `retired` | `false` | `FEAT-0070`, `FEAT-0071` | `improvement-loop` |
| [FEAT-0070 Dogfood self-improvement portfolio checkpoints](../features/FEAT-0070-experimental-feature-evaluation-reports.md) | [Self-Improvement And Learning](../systems/self-improvement-learning.md) | `implemented` | `true` | `false` | `improvement-loop` |
| [FEAT-0071 Project Work Pulse](../features/FEAT-0071-project-work-pulse.md) | [Horizon Loop](../systems/horizon-loop.md) | `implemented` | `true` | `false` | `planning` |
| [FEAT-0072 Persistent ICP and World Memory](../features/FEAT-0072-persistent-icp-and-world-memory.md) | [Source And Sidecar Systems](../systems/source-sidecar-systems.md) | `implemented` | `true` | `false` | `context-routing` |
| [FEAT-0073 Brand Kit approved creative identity](../features/FEAT-0073-brand-kit-approved-creative-identity.md) | [Content Production](../systems/content-production.md) | `designed` | `false` | `false` | `content-production` |
| [FEAT-0074 Feed Scout Source Instructions](../features/FEAT-0074-feed-scout-source-instructions.md) | [Source And Sidecar Systems](../systems/source-sidecar-systems.md) | `implemented` | `true` | `false` | `source-intelligence` |
| [FEAT-0075 Entity Markdown and World projection](../features/FEAT-0075-entity-markdown-and-world-projection.md) | [Graph Systems](../systems/graph-systems.md) | `implemented` | `false` | `false` | `memory` |
| [FEAT-0076 Typed entity view projections](../features/FEAT-0076-typed-entity-view-projections.md) | [Graph Systems](../systems/graph-systems.md) | `implemented` | `false` | `false` | `projections` |
| [FEAT-0077 CRM entity projection](../features/FEAT-0077-crm-entity-projection.md) | [Graph Systems](../systems/graph-systems.md) | `implemented` | `false` | `false` | `projections` |
| [FEAT-0078 Harness GraphIR projections](../features/FEAT-0078-harness-graphir-projections.md) | [Graph Systems](../systems/graph-systems.md) | `implemented` | `false` | `false` | `projections` |
