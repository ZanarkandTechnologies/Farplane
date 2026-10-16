---
title: Farplane Guides
status: active
owner: harness
created_at: 2026-06-15
updated_at: 2026-10-15
framework_template_version: "0.4.0"
source_of_truth:
  - docs/prd.md
  - docs/guides/work-loop.md
  - docs/guides/project-files.md
  - docs/guides/cli.md
  - docs/guides/hooks-and-runtime.md
  - docs/guides/wiki-and-entities.md
  - docs/guides/reporting.md
  - docs/guides/graphs.md
  - farplane/manifest.json
tags:
  - farplane
  - framework
  - documentation-routing
---

# Farplane Guides

How a Farplane project works. The [Farplane engine PRD](../prd.md) owns product
requirements; these guides explain how the project substrate implements them.
Start with the work loop, then open only the guide your question needs.

- [Work Loop](work-loop.md): how work enters as a GitHub issue, runs through
  `goal-advisor`, resumes at check-ins, completes, what the scheduled jobs do
  around it, and the Monday business loop that seeds floor queues.
- [Skills](skills.md): how skills are organized into desks, installed, called,
  and proved, and where the rules for making them live.
- [Project Files](project-files.md): which tracked and ignored files a project
  has, and what each may and may not hold.
- [Command Line](cli.md): which `farplane` command does a job, and the rules a
  command change keeps.
- [Hooks And Runtime](hooks-and-runtime.md): what hooks may do, the Stop gate,
  telemetry, and where runtime state lives.
- [Wiki And Entities](wiki-and-entities.md): Wiki pages, views, CRM, search and
  sync, and thread notes in the local memory repo.
- [Reporting](reporting.md): where reports live, which ones the UI indexes,
  and how a report reads.
- [Graphs](graphs.md): the harness GraphIR projections, the lifecycle graph
  contract, and the boundary with the Wiki graph.

Two framework procedures live with their skills: project setup in the
`setup-advisor` [critical path](../../skills/setup-advisor/references/critical-path.md),
and registries, rollout, validators, and graph generators in `harness`
[maintenance](../../skills/harness/references/harness-maintenance.md).

## Ownership

- `docs/prd.md` owns audience, problem, jobs, requirements, metrics,
  acceptance, non-goals, and release policy.
- Each guide owns one part of how the framework works and links to its source
  implementation.
- Skills own operational procedures; GitHub issues own current work and proof.
- `farplane/manifest.json` owns the machine-readable project and framework
  graph entrypoints (`farplane_graph.framework_core.include` lists these
  guides).

Do not add another versioned framework specification. Change the PRD for
product-boundary changes, the work loop for end-to-end behavior, or the
smallest guide for an implementation contract. Historical migrations stay in
`docs/HISTORY.md`, archived tickets, and git history; do not keep proposal
docs, audit shelves, or retired duplicate specifications here for historical
search.

## Maintenance

When a framework contract changes:

1. update its smallest owner guide and implementation surface;
2. update the PRD or the work loop only when their public contract changed;
3. regenerate graph projections when applicable;
4. run documentation references, project-file validation, and the relevant
   behavioral proof; and
5. delete superseded documentation rather than introducing another truth
   layer.
