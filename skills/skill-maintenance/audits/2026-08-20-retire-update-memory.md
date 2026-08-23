---
skill: skill-maintenance
date: 2026-08-20
change_type: retirement
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: working-tree-before-retirement
after_ref: working-tree
reasoning_basis: operator_direction
proof_artifacts:
  - skills/skill-maintenance/scripts/test_generate_farplane_lifecycle_graph.py
  - docs/skills/registry.jsonl
eval_required: no
---

# Retire Update Memory Audit

## Decision

Retire the inactive `update-memory` catch-all and make knowledge extraction
route by durable owner:

- operational procedures and reusable SOPs -> `skill-maintenance` and the
  owning skill package;
- project knowledge and article details -> `doc-advisor` and the owning
  project files;
- sourced entity facts and relationships -> `manage-wiki` and Entity Markdown.

Historical mentions in append-only lessons, troubles, and prior audits remain
historical evidence rather than live routing instructions.

## Delta

- Before: one generic memory-upkeep skill overlapped skills, project docs, and
  the Wiki without an active automation owner.
- After: callers, workflow maps, lifecycle projections, and the generated skill
  registry expose three distinct destinations.
- Example: a deployment runbook becomes a skill procedure, an architecture
  decision updates project docs, and a customer relationship updates the Wiki.

## Proof

- The source skill package is deleted and absent from the generated registry.
- Lifecycle graph validation requires `doc-advisor` and `manage-wiki`, rejects
  the retired skill node, and nests durable routing under the
  `interval_knowledge_phase` projection.
- Focused lifecycle graph tests and diff hygiene pass.
- Full skill and documentation checks are recorded separately when unrelated
  in-progress work prevents a clean repository-wide result.

## Review

Independent reviewer verdict: TAS-A, pass, no P1/P2 findings, no hard-gate
failures, and completion approved. Unrelated dirty-worktree changes under the
skill installer were excluded from this retirement claim.
