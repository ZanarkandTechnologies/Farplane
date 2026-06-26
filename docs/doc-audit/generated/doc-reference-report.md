---
title: "Docs Reference Audit"
status: generated
owner: skill-maintenance
created_at: 2026-06-11
updated_at: 2026-06-11
tags:
  - docs
  - harness-map
  - skill-maintenance
refs:
  - skills/skill-maintenance/scripts/generate_harness_graph.py
  - skills/skill-maintenance/graph/harness-graph.json
---

# Docs Reference Audit

Generated at `2026-06-26T09:17:31+00:00` from local Markdown links and literal repo-path
references. This is a navigation and cleanup aid, not a deletion authority.

## Harness Math Doc

The harness math doc is `docs/fundamentals/harness-algebra.md`.

- All inbound refs: `16`
- Skill-origin refs: `7`
- Cleanup rule: keep this as the canonical equation/model surface and point
  workflow docs back to it instead of duplicating the algebra.

## Counts

- Scanned files: `1234`
- Nodes: `864`
- Edges: `4102`
- Unresolved local-looking refs: `987`

## Most Referenced Docs

| Doc | All refs | Skill refs |
| --- | --- | --- |
| `docs/specs/self-improvement-contracts.md` | 71 | 61 |
| `docs/specs/README.md` | 59 | 26 |
| `docs/MEMORY.md` | 57 | 26 |
| `docs/LESSONS.md` | 55 | 25 |
| `docs/TROUBLES.md` | 46 | 20 |
| `docs/HISTORY.md` | 39 | 15 |
| `docs/skills/registry.jsonl` | 37 | 23 |
| `docs/skills/README.md` | 33 | 15 |
| `docs/features/registry.jsonl` | 32 | 11 |
| `docs/skills/best-practices.md` | 23 | 16 |
| `docs/specs/goal-loop-contract.md` | 23 | 11 |
| `docs/bootstrap-brief.md` | 23 | 19 |
| `docs/prd.md` | 22 | 19 |
| `docs/skills/system.md` | 21 | 15 |
| `docs/specs/filesystem-lifecycle.md` | 21 | 9 |
| `docs/skills/templates/SKILL_TEMPLATE.md` | 20 | 9 |
| `docs/TASTE.md` | 19 | 14 |
| `docs/sources/registry.jsonl` | 17 | 6 |
| `docs/specs/harness-techniques.md` | 17 | 2 |
| `docs/fundamentals/harness-engineering-doctrine.md` | 16 | 7 |

## Spec Status Preview

| Spec | All refs | Skill refs | Suggested status |
| --- | --- | --- | --- |
| `docs/specs/AGENTS.md` | 1 | 0 | keep active |
| `docs/specs/README.md` | 59 | 26 | keep active |
| `docs/specs/adaptive-backoff.md` | 8 | 6 | keep active |
| `docs/specs/agent-testability-surfaces.md` | 4 | 3 | keep active |
| `docs/specs/context-and-handoff-policy.md` | 7 | 4 | keep active |
| `docs/specs/doc-governance.md` | 11 | 4 | keep active |
| `docs/specs/feature-catalog.md` | 12 | 1 | keep active |
| `docs/specs/filesystem-lifecycle.md` | 21 | 9 | keep active |
| `docs/specs/first-principles-planning.md` | 6 | 4 | keep active |
| `docs/specs/goal-loop-contract.md` | 23 | 11 | keep active |
| `docs/specs/harness-techniques.md` | 17 | 2 | keep active |
| `docs/specs/inspiration-vault.md` | 2 | 0 | keep active |
| `docs/specs/invocation-and-adapters.md` | 13 | 2 | keep active |
| `docs/specs/minimal-autonomy-loop.md` | 4 | 3 | keep active |
| `docs/specs/nested-pm-projects.md` | 0 | 0 | keep active |
| `docs/specs/product-convergence-plan.md` | 0 | 0 | keep active |
| `docs/specs/program-notation.md` | 9 | 7 | keep active |
| `docs/specs/review-gates.md` | 10 | 4 | keep active |
| `docs/specs/self-improvement-contracts.md` | 71 | 61 | keep active |
| `docs/specs/skill-compounding-score.md` | 0 | 0 | keep active |
| `docs/specs/spec-authoring-contract.md` | 5 | 2 | keep active |
| `docs/specs/spec-first-execution-loop.md` | 6 | 0 | keep active |
| `docs/specs/steer-pulse-automation.md` | 12 | 6 | keep active |

## Suggested Global Docs Bundle

These are the first docs to ship or copy alongside installed skills if a skill
needs local doc references outside its own package.

| Doc | Why |
| --- | --- |
| `docs/fundamentals/harness-algebra.md` | high leverage for installed skills or harness placement |
| `docs/fundamentals/harness-engineering-doctrine.md` | high leverage for installed skills or harness placement |
| `docs/specs/self-improvement-contracts.md` | high leverage for installed skills or harness placement |
| `docs/specs/invocation-and-adapters.md` | high leverage for installed skills or harness placement |
| `docs/skills/README.md` | high leverage for installed skills or harness placement |
| `docs/skills/system.md` | high leverage for installed skills or harness placement |
| `docs/skills/best-practices.md` | high leverage for installed skills or harness placement |
| `docs/review/rubrics/review-rubric-index.md` | high leverage for installed skills or harness placement |
| `docs/review/rubrics/reviewer-handoff.md` | high leverage for installed skills or harness placement |
| `docs/specs/filesystem-lifecycle.md` | high leverage for installed skills or harness placement |

## Unreferenced Docs Preview

Unreferenced here means no local link or literal-path reference was detected in
the scanned files. Directory-loaded files, validators, and historical evidence
can still be worth keeping.

| Doc | Note |
| --- | --- |
| `docs/AGENTS.md` | keep if loaded by directory convention |
| `docs/automation-previews/2026-06-15-pm-ticket-update-automation-preview.md` | review before archive or merge |
| `docs/automation-previews/2026-06-24-life-weekly-interval-preview.md` | review before archive or merge |
| `docs/features/AGENTS.md` | keep if loaded by directory convention |
| `docs/private-tool-context.md` | review before archive or merge |
| `docs/sources/AGENTS.md` | keep if loaded by directory convention |
| `docs/specs/nested-pm-projects.md` | review before archive or merge |
| `docs/specs/product-convergence-plan.md` | review before archive or merge |
| `docs/specs/skill-compounding-score.md` | review before archive or merge |

## Next Cleanup Pass

1. Reduce unresolved local-looking refs that point to missing active surfaces,
   especially template-era `docs/progress.md` and old external repo paths.
2. Keep `docs/review/rubrics/*` as canonical docs even when individual family
   files are primarily reached through the directory and rubric index.
3. Move temporary research and speculative notes to tickets, experiments, or
   `tmp/**`; keep tracked docs for live contracts and generated inventories.
4. Use this report before deleting or moving docs: redirect active inbound refs
   first, then remove the superseded file.
