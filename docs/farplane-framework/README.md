---
title: Farplane Framework
status: active
owner: harness
created_at: 2026-06-15
updated_at: 2026-07-22
framework_template_version: "0.3.2"
source_of_truth:
  - docs/prd.md
  - docs/farplane-framework/lifecycle.md
  - docs/farplane-framework/project-files.md
  - docs/farplane-framework/init-advisor-critical-path.md
  - docs/farplane-framework/pulse-and-interval-loop.md
  - docs/farplane-framework/ticket-execution-loop.md
  - docs/farplane-framework/hooks-and-runtime.md
  - docs/farplane-framework/entities.md
  - docs/farplane-framework/reporting.md
  - docs/farplane-framework/graph-contract.md
  - docs/farplane-framework/harness-maintenance.md
  - farplane/manifest.json
tags:
  - farplane
  - framework
  - documentation-routing
---

# Farplane Framework

This directory contains Farplane's technical framework contracts. The
[Farplane V1 PRD](../prd.md) owns product requirements; these docs explain how
the project substrate implements them.

```text
product truth   -> docs/prd.md
technical map   -> lifecycle.md
specific detail -> one owner document below
```

Do not add another versioned framework specification. Update the PRD for
product-boundary changes, Lifecycle for end-to-end behavior, or the smallest
technical owner for implementation-contract changes.

## Start Here

Read [Lifecycle](lifecycle.md) first. It summarizes the V1 system:

```text
program files + capability skills
-> one ticket board
-> one Work Pulse
-> bounded scheduled sources
-> ticket-local execution, QA, review, and learning
```

Then open only the contract needed for the current question:

| Question | Owner document |
| --- | --- |
| Which tracked and generated files exist? | [Project Files](project-files.md) |
| How is a project initialized or migrated? | [Init Advisor Critical Path](init-advisor-critical-path.md) |
| How do Pulse, planning, reports, Feed Scout, and Dogfood coordinate? | [Work Pulse And Scheduled Ticket Sources](pulse-and-interval-loop.md) |
| How does a shaped idea become reviewed completed work? | [Ticket Execution Loop](ticket-execution-loop.md) |
| What may hooks do, and where does runtime state live? | [Hooks And Runtime](hooks-and-runtime.md) |
| Where do canonical entities, named views, paragraph links, World, and CRM projections live? | [Entity Memory](entities.md) |
| What report metadata and registry shape does Core expose? | [Reporting](reporting.md) |
| How are lifecycle graph projections represented? | [Graph Contract](graph-contract.md) |
| How do registries, rollout, validators, and graph generators fit together? | [Harness Maintenance](harness-maintenance.md) |

## Ownership Boundary

- `docs/prd.md` owns audience, problem, jobs, requirements, metrics, acceptance,
  non-goals, and release policy.
- `lifecycle.md` owns the friendly end-to-end technical flow and state-owner
  summary.
- Each specialist document owns one deeper contract and links to its source
  implementation or feature specs.
- `docs/features/` owns first-class capability specs and generated feature
  registry inputs.
- `docs/systems/` groups those features into public product systems.
- Skills own operational procedures; tickets own current work and proof.
- `farplane/manifest.json` owns the machine-readable project and framework graph
  entrypoints.

Historical migrations remain in `docs/HISTORY.md`, archived tickets, and git
history. Do not keep proposal docs, global audit shelves, or retired duplicate
specifications in this directory solely for historical search.

## Maintenance

When a framework contract changes:

1. update its smallest owner document and implementation surface;
2. update the PRD or Lifecycle only when their public contract changed;
3. regenerate feature/system registries or graph projections when applicable;
4. run documentation references, project-file validation, and the relevant
   behavioral proof; and
5. delete superseded documentation rather than introducing another truth
   layer.
