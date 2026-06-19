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

Generated at `2026-06-19T18:20:44+00:00` from local Markdown links and literal repo-path
references. This is a navigation and cleanup aid, not a deletion authority.

## Harness Math Doc

The harness math doc is `docs/fundamentals/harness-algebra.md`.

- All inbound refs: `13`
- Skill-origin refs: `5`
- Cleanup rule: keep this as the canonical equation/model surface and point
  workflow docs back to it instead of duplicating the algebra.

## Counts

- Scanned files: `1075`
- Nodes: `790`
- Edges: `3078`
- Unresolved local-looking refs: `866`

## Most Referenced Docs

| Doc | All refs | Skill refs |
| --- | --- | --- |
| `docs/LESSONS.md` | 54 | 25 |
| `docs/specs/README.md` | 53 | 26 |
| `docs/MEMORY.md` | 47 | 18 |
| `docs/TROUBLES.md` | 45 | 20 |
| `docs/HISTORY.md` | 37 | 11 |
| `docs/specs/self-improvement-contracts.md` | 32 | 25 |
| `docs/skills/README.md` | 30 | 13 |
| `docs/skills/registry.jsonl` | 29 | 15 |
| `docs/features/registry.jsonl` | 27 | 9 |
| `docs/prd.md` | 23 | 20 |
| `docs/skills/best-practices.md` | 21 | 15 |
| `docs/skills/system.md` | 19 | 13 |
| `docs/sources/registry.jsonl` | 18 | 6 |
| `docs/specs/harness-techniques.md` | 18 | 2 |
| `docs/TASTE.md` | 18 | 14 |
| `docs/specs/goal-loop-contract.md` | 18 | 9 |
| `docs/specs/invocation-and-adapters.md` | 15 | 2 |
| `docs/fundamentals/harness-engineering-doctrine.md` | 13 | 5 |
| `docs/fundamentals/harness-algebra.md` | 13 | 5 |
| `docs/review/rubrics/review-rubric-index.md` | 12 | 6 |

## Spec Status Preview

| Spec | All refs | Skill refs | Suggested status |
| --- | --- | --- | --- |
| `docs/specs/AGENTS.md` | 1 | 0 | keep active |
| `docs/specs/README.md` | 53 | 26 | keep active |
| `docs/specs/adaptive-backoff.md` | 7 | 6 | keep active |
| `docs/specs/agent-testability-surfaces.md` | 4 | 3 | keep active |
| `docs/specs/context-and-handoff-policy.md` | 7 | 4 | keep active |
| `docs/specs/doc-governance.md` | 8 | 0 | keep active |
| `docs/specs/filesystem-lifecycle.md` | 8 | 1 | keep active |
| `docs/specs/first-principles-planning.md` | 8 | 6 | keep active |
| `docs/specs/goal-loop-contract.md` | 18 | 9 | keep active |
| `docs/specs/harness-techniques.md` | 18 | 2 | keep active |
| `docs/specs/inspiration-vault.md` | 1 | 0 | keep active |
| `docs/specs/invocation-and-adapters.md` | 15 | 2 | keep active |
| `docs/specs/product-convergence-plan.md` | 0 | 0 | keep active |
| `docs/specs/program-notation.md` | 11 | 7 | keep active |
| `docs/specs/review-gates.md` | 7 | 2 | keep active |
| `docs/specs/self-improvement-contracts.md` | 32 | 25 | keep active |
| `docs/specs/spec-authoring-contract.md` | 6 | 3 | keep active |
| `docs/specs/spec-first-execution-loop.md` | 5 | 0 | keep active |

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
| `docs/archive/research/code-reviews/2026-04-05_ralph-prototype_review.md` | review before archive or merge |
| `docs/archive/research/web-research/2026-04-02_run-artifacts-risk-analysis.md` | review before archive or merge |
| `docs/archive/research/web-research/2026-04-03_ralf-form-factor-proposal.md` | review before archive or merge |
| `docs/archive/research/web-research/2026-04-03_ralf-ideal-product-form-factor.md` | review before archive or merge |
| `docs/archive/research/web-research/2026-05-05_external-cli-frontend-delegation-proposal.md` | review before archive or merge |
| `docs/archive/research/web-research/2026-05-27_ai-agent-skill-file-structure-brief.md` | review before archive or merge |
| `docs/automation-previews/2026-06-15-pm-ticket-update-automation-preview.md` | review before archive or merge |
| `docs/features/AGENTS.md` | keep if loaded by directory convention |
| `docs/futureideas/autonomous-unit-filesystem.md` | review before archive or merge |
| `docs/private-tool-context.md` | review before archive or merge |
| `docs/sources/AGENTS.md` | keep if loaded by directory convention |
| `docs/specs/product-convergence-plan.md` | review before archive or merge |

## Next Cleanup Pass

1. Reduce unresolved local-looking refs that point to missing active surfaces,
   especially template-era `docs/progress.md` and old external repo paths.
2. Keep `docs/review/rubrics/*` as canonical docs even when individual family
   files are primarily reached through the directory and rubric index.
3. Keep `docs/archive/research/**` as historical evidence unless a source registry row
   or active spec requires a new location.
4. Use this report before any future archive move: redirect active inbound refs
   first, then move superseded files under `docs/archive/`.
