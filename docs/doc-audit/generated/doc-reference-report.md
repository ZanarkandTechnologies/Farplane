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

Generated at `2026-06-11T16:52:43+00:00` from local Markdown links and literal repo-path
references. This is a navigation and cleanup aid, not a deletion authority.

## Harness Math Doc

The harness math doc is `docs/specs/harness-algebra.md`.

- All inbound refs: `9`
- Skill-origin refs: `4`
- Cleanup rule: keep this as the canonical equation/model surface and point
  workflow docs back to it instead of duplicating the algebra.

## Counts

- Scanned files: `934`
- Nodes: `649`
- Edges: `2155`
- Unresolved local-looking refs: `766`

## Most Referenced Docs

| Doc | All refs | Skill refs |
| --- | --- | --- |
| `docs/specs/README.md` | 50 | 27 |
| `docs/MEMORY.md` | 45 | 20 |
| `docs/LESSONS.md` | 36 | 18 |
| `docs/HISTORY.md` | 30 | 7 |
| `docs/TROUBLES.md` | 28 | 12 |
| `docs/features/registry.jsonl` | 25 | 8 |
| `docs/skills/registry.jsonl` | 24 | 11 |
| `docs/skills/README.md` | 22 | 11 |
| `docs/prd.md` | 19 | 17 |
| `docs/specs/harness-techniques.md` | 18 | 2 |
| `docs/TASTE.md` | 18 | 14 |
| `docs/specs/invocation-and-adapters.md` | 14 | 2 |
| `docs/sources/registry.jsonl` | 14 | 5 |
| `docs/specs/self-improvement-contracts.md` | 14 | 6 |
| `docs/skills/system.md` | 13 | 8 |
| `docs/skills/best-practices.md` | 13 | 10 |
| `docs/review/rubrics/review-rubric-index.md` | 12 | 6 |
| `docs/specs/harness-engineering-doctrine.md` | 12 | 5 |
| `docs/features/README.md` | 11 | 3 |
| `docs/review/rubrics/reviewer-handoff.md` | 9 | 6 |

## Spec Status Preview

| Spec | All refs | Skill refs | Suggested status |
| --- | --- | --- | --- |
| `docs/specs/AGENTS.md` | 1 | 0 | keep active |
| `docs/specs/README.md` | 50 | 27 | keep active |
| `docs/specs/adaptive-backoff.md` | 7 | 6 | keep active |
| `docs/specs/agent-testability-surfaces.md` | 4 | 3 | keep active |
| `docs/specs/context-and-handoff-policy.md` | 4 | 1 | keep active |
| `docs/specs/diagram-first-conventions.md` | 7 | 7 | keep active |
| `docs/specs/doc-governance.md` | 6 | 0 | keep active |
| `docs/specs/filesystem-lifecycle.md` | 6 | 1 | keep active |
| `docs/specs/first-principles-planning.md` | 7 | 6 | keep active |
| `docs/specs/harness-algebra.md` | 9 | 4 | keep active |
| `docs/specs/harness-engineering-doctrine.md` | 12 | 5 | keep active |
| `docs/specs/harness-techniques.md` | 18 | 2 | keep active |
| `docs/specs/invocation-and-adapters.md` | 14 | 2 | keep active |
| `docs/specs/review-gates.md` | 7 | 2 | keep active |
| `docs/specs/self-improvement-contracts.md` | 14 | 6 | keep active |
| `docs/specs/spec-authoring-contract.md` | 5 | 3 | keep active |
| `docs/specs/spec-first-execution-loop.md` | 5 | 0 | keep active |

## Suggested Global Docs Bundle

These are the first docs to ship or copy alongside installed skills if a skill
needs local doc references outside its own package.

| Doc | Why |
| --- | --- |
| `docs/specs/harness-algebra.md` | high leverage for installed skills or harness placement |
| `docs/specs/harness-engineering-doctrine.md` | high leverage for installed skills or harness placement |
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
| `docs/features/AGENTS.md` | keep if loaded by directory convention |
| `docs/private-tool-context.md` | review before archive or merge |
| `docs/research/code-reviews/2026-04-05_ralph-prototype_review.md` | review before archive or merge |
| `docs/skills/AGENTS.md` | keep if loaded by directory convention |
| `docs/sources/AGENTS.md` | keep if loaded by directory convention |

## Next Cleanup Pass

1. Reduce unresolved local-looking refs that point to missing active surfaces,
   especially template-era `docs/progress.md` and old external repo paths.
2. Keep `docs/review/rubrics/*` as canonical docs even when individual family
   files are primarily reached through the directory and rubric index.
3. Keep `docs/research/**` as historical evidence unless a source registry row
   or active spec requires a new location.
4. Use this report before any future archive move: redirect active inbound refs
   first, then move superseded files under `docs/archive/`.
