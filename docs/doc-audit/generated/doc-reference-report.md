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

Generated at `2026-06-11T08:01:39+00:00` from local Markdown links and literal repo-path
references. This is a navigation and cleanup aid, not a deletion authority.

## Harness Math Doc

The harness math doc is `docs/specs/harness-algebra.md`.

- All inbound refs: `8`
- Skill-origin refs: `3`
- Cleanup rule: keep this as the canonical equation/model surface and point
  workflow docs back to it instead of duplicating the algebra.

## Counts

- Scanned files: `926`
- Nodes: `615`
- Edges: `2060`
- Unresolved local-looking refs: `762`

## Most Referenced Docs

| Doc | All refs | Skill refs |
| --- | --- | --- |
| `docs/specs/README.md` | 50 | 27 |
| `docs/MEMORY.md` | 45 | 20 |
| `docs/LESSONS.md` | 36 | 18 |
| `docs/HISTORY.md` | 29 | 7 |
| `docs/TROUBLES.md` | 28 | 12 |
| `docs/features/registry.jsonl` | 25 | 8 |
| `docs/skills/registry.jsonl` | 23 | 10 |
| `docs/skills/README.md` | 22 | 11 |
| `docs/prd.md` | 19 | 17 |
| `docs/TASTE.md` | 18 | 14 |
| `docs/specs/harness-techniques.md` | 16 | 2 |
| `docs/review/rubrics` | 14 | 3 |
| `docs/sources/registry.jsonl` | 13 | 5 |
| `docs/skills/best-practices.md` | 13 | 10 |
| `docs/skills/system.md` | 12 | 7 |
| `docs/specs/harness-engineering-doctrine.md` | 12 | 5 |
| `docs/features/README.md` | 11 | 3 |
| `docs/research` | 11 | 2 |
| `docs/specs/self-improvement-contracts.md` | 11 | 6 |
| `docs/review/rubrics/review-rubric-index.md` | 10 | 5 |

## Spec Status Preview

| Spec | All refs | Skill refs | Suggested status |
| --- | --- | --- | --- |
| `docs/specs/AGENTS.md` | 1 | 0 | keep active |
| `docs/specs/README.md` | 50 | 27 | keep active |
| `docs/specs/adaptive-backoff.md` | 7 | 6 | keep active |
| `docs/specs/agent-testability-surfaces.md` | 4 | 3 | keep active |
| `docs/specs/case-based-memory-context-graph.md` | 3 | 1 | merge into harness-algebra or filesystem-lifecycle if the context graph stays conceptual |
| `docs/specs/context-and-handoff-policy.md` | 4 | 1 | keep active |
| `docs/specs/diagram-first-conventions.md` | 7 | 7 | keep active |
| `docs/specs/doc-governance.md` | 6 | 0 | keep active |
| `docs/specs/filesystem-lifecycle.md` | 6 | 1 | keep active |
| `docs/specs/first-principles-planning.md` | 7 | 6 | keep active |
| `docs/specs/harness-algebra.md` | 8 | 3 | keep active |
| `docs/specs/harness-engineering-doctrine.md` | 12 | 5 | keep active |
| `docs/specs/harness-techniques.md` | 16 | 2 | keep active |
| `docs/specs/invocation-and-adapters.md` | 9 | 1 | keep active |
| `docs/specs/meta-harness-automation.md` | 7 | 1 | merge active pieces into harness-techniques and self-improvement-contracts |
| `docs/specs/orchestrator-subagent-loop.md` | 5 | 1 | merge durable gates into spec-first-execution-loop and review-gates |
| `docs/specs/review-gates.md` | 7 | 2 | keep active |
| `docs/specs/runtime-surface.md` | 9 | 1 | merge current runtime boundaries into invocation-and-adapters |
| `docs/specs/self-improvement-contracts.md` | 11 | 6 | keep active |
| `docs/specs/skill-self-healing.md` | 3 | 1 | merge into self-improvement-contracts, eval, and skill-maintenance docs |
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
| `docs/skills/README.md` | high leverage for installed skills or harness placement |
| `docs/skills/system.md` | high leverage for installed skills or harness placement |
| `docs/skills/best-practices.md` | high leverage for installed skills or harness placement |
| `docs/specs/filesystem-lifecycle.md` | high leverage for installed skills or harness placement |

## Unreferenced Docs Preview

Unreferenced here means no local link or literal-path reference was detected in
the scanned files. Directory-loaded files, validators, and historical evidence
can still be worth keeping.

| Doc | Note |
| --- | --- |
| `docs/features/AGENTS.md` | keep if loaded by directory convention |
| `docs/private-tool-context.md` | review before archive or merge |
| `docs/research/2026-04-12_deep-skill-opportunities.md` | review before archive or merge |
| `docs/research/code-reviews/2026-04-05_ralph-prototype_review.md` | review before archive or merge |
| `docs/research/web-research/2026-04-02_run-artifacts-risk-analysis.md` | review before archive or merge |
| `docs/research/web-research/2026-04-03_ralf-form-factor-proposal.md` | review before archive or merge |
| `docs/research/web-research/2026-04-03_ralf-ideal-product-form-factor.md` | review before archive or merge |
| `docs/research/web-research/2026-05-05_external-cli-frontend-delegation-proposal.md` | review before archive or merge |
| `docs/research/web-research/2026-05-27_ai-agent-skill-file-structure-brief.md` | review before archive or merge |
| `docs/review/rubrics/architecture.md` | review before archive or merge |
| `docs/review/rubrics/debloatability.md` | review before archive or merge |
| `docs/review/rubrics/demo-quality.md` | review before archive or merge |
| `docs/review/rubrics/eval-quality.md` | review before archive or merge |
| `docs/review/rubrics/evidence-quality.md` | review before archive or merge |
| `docs/review/rubrics/frontend-code-maintainability.md` | review before archive or merge |
| `docs/review/rubrics/gotchas.md` | review before archive or merge |
| `docs/review/rubrics/implementation-plan.md` | review before archive or merge |
| `docs/review/rubrics/integration-readiness.md` | review before archive or merge |
| `docs/review/rubrics/prompt-quality.md` | review before archive or merge |
| `docs/review/rubrics/spec-contract.md` | review before archive or merge |
| `docs/review/rubrics/ui-quality.md` | review before archive or merge |
| `docs/review/rubrics/user-intent-satisfaction.md` | review before archive or merge |
| `docs/review/rubrics/video-quality.md` | review before archive or merge |
| `docs/review/rubrics/workflows.md` | review before archive or merge |
| `docs/skills/AGENTS.md` | keep if loaded by directory convention |
| `docs/sources/AGENTS.md` | keep if loaded by directory convention |

## Next Cleanup Pass

1. Merge active content from the consolidation candidates into the target
   canonical specs.
2. Update references.
3. Move superseded files under `docs/archive/` only after the graph shows their
   important inbound refs have been redirected.
4. Keep `docs/research/**` as historical evidence unless a source registry row
   or active spec requires a new location.
