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

Generated at `2026-06-27T16:32:59+00:00` from local Markdown links and literal repo-path
references. This is a navigation and cleanup aid, not a deletion authority.

## Harness Math Doc

The harness math doc is `docs/fundamentals/harness-algebra.md`.

- All inbound refs: `16`
- Skill-origin refs: `7`
- Cleanup rule: keep this as the canonical equation/model surface and point
  workflow docs back to it instead of duplicating the algebra.

## Counts

- Scanned files: `1215`
- Nodes: `804`
- Edges: `4094`
- Unresolved local-looking refs: `993`

## Most Referenced Docs

| Doc | All refs | Skill refs |
| --- | --- | --- |
| `docs/features/README.md` | 60 | 25 |
| `docs/MEMORY.md` | 53 | 26 |
| `docs/features/validate_features.py` | 50 | 5 |
| `docs/LESSONS.md` | 47 | 25 |
| `docs/HISTORY.md` | 46 | 15 |
| `docs/skills/registry.jsonl` | 41 | 28 |
| `docs/features/registry.jsonl` | 38 | 13 |
| `docs/TROUBLES.md` | 36 | 20 |
| `docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md` | 36 | 18 |
| `docs/skills/README.md` | 33 | 14 |
| `docs/systems/README.md` | 30 | 9 |
| `docs/skills/system.md` | 26 | 16 |
| `docs/skills/best-practices.md` | 26 | 17 |
| `docs/skills/templates/SKILL_TEMPLATE.md` | 24 | 10 |
| `docs/features/FEAT-0065-pulse-and-interval-automation.md` | 24 | 12 |
| `docs/features/FEAT-0060-registry-backed-documentation-os.md` | 23 | 7 |
| `docs/bootstrap-brief.md` | 23 | 19 |
| `docs/prd.md` | 22 | 19 |
| `docs/features/FEAT-0039-behavior-correction-hardcase-metadata-and-narrow-eval-capture.md` | 22 | 8 |
| `docs/TASTE.md` | 19 | 14 |

## Spec Status Preview

| Spec | All refs | Skill refs | Suggested status |
| --- | --- | --- | --- |
| `docs/features/AGENTS.md` | 0 | 0 | keep active |
| `docs/features/FEAT-0007-ticket-as-durable-task-memory.md` | 15 | 4 | keep active |
| `docs/features/FEAT-0008-artifact-first-qa-and-completion-proof.md` | 15 | 4 | keep active |
| `docs/features/FEAT-0011-harness-scout-source-ingestion.md` | 4 | 0 | keep active |
| `docs/features/FEAT-0014-frontend-skill-parity-upgrade.md` | 4 | 0 | keep active |
| `docs/features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md` | 17 | 2 | keep active |
| `docs/features/FEAT-0022-skill-tier-leverage-classes.md` | 4 | 0 | keep active |
| `docs/features/FEAT-0025-video-to-skill-source-reconstruction.md` | 4 | 0 | keep active |
| `docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md` | 36 | 18 | keep active |
| `docs/features/FEAT-0030-on-demand-skill-plugin-packaging.md` | 4 | 0 | keep active |
| `docs/features/FEAT-0031-agent-behavior-test-workflow.md` | 7 | 3 | keep active |
| `docs/features/FEAT-0032-goal-advisor-execution-compilation.md` | 4 | 0 | keep active |
| `docs/features/FEAT-0034-adversarial-agent-qa-test-skill.md` | 4 | 0 | keep active |
| `docs/features/FEAT-0039-behavior-correction-hardcase-metadata-and-narrow-eval-capture.md` | 22 | 8 | keep active |
| `docs/features/FEAT-0042-lean-global-agent-operating-kernel.md` | 10 | 4 | keep active |
| `docs/features/FEAT-0043-project-level-system-prompt-eval-suite.md` | 4 | 0 | keep active |
| `docs/features/FEAT-0054-modular-skill-local-eval-tasks.md` | 4 | 0 | keep active |
| `docs/features/FEAT-0056-inspiration-vault.md` | 6 | 0 | keep active |
| `docs/features/FEAT-0057-skill-local-qa-checklist-artifacts.md` | 4 | 0 | keep active |
| `docs/features/FEAT-0060-registry-backed-documentation-os.md` | 23 | 7 | keep active |
| `docs/features/FEAT-0061-farplane-adoption-tracker-cli.md` | 6 | 0 | keep active |
| `docs/features/FEAT-0063-metric-advisor-cards.md` | 4 | 0 | keep active |
| `docs/features/FEAT-0064-skill-signals.md` | 16 | 8 | keep active |
| `docs/features/FEAT-0065-pulse-and-interval-automation.md` | 24 | 12 | keep active |
| `docs/features/README.md` | 60 | 25 | keep active |
| `docs/features/TEMPLATE.md` | 6 | 1 | keep active |
| `docs/features/registry.md` | 3 | 0 | keep active |

## Suggested Global Docs Bundle

These are the first docs to ship or copy alongside installed skills if a skill
needs local doc references outside its own package.

| Doc | Why |
| --- | --- |
| `docs/fundamentals/harness-algebra.md` | high leverage for installed skills or harness placement |
| `docs/fundamentals/harness-engineering-doctrine.md` | high leverage for installed skills or harness placement |
| `docs/features/FEAT-0039-behavior-correction-hardcase-metadata-and-narrow-eval-capture.md` | high leverage for installed skills or harness placement |
| `docs/features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md` | high leverage for installed skills or harness placement |
| `docs/skills/README.md` | high leverage for installed skills or harness placement |
| `docs/skills/system.md` | high leverage for installed skills or harness placement |
| `docs/skills/best-practices.md` | high leverage for installed skills or harness placement |
| `docs/review/rubrics/review-rubric-index.md` | high leverage for installed skills or harness placement |
| `docs/review/rubrics/reviewer-handoff.md` | high leverage for installed skills or harness placement |
| `docs/features/FEAT-0060-registry-backed-documentation-os.md` | high leverage for installed skills or harness placement |

## Unreferenced Docs Preview

Unreferenced here means no local link or literal-path reference was detected in
the scanned files. Directory-loaded files, validators, and historical evidence
can still be worth keeping.

| Doc | Note |
| --- | --- |
| `docs/AGENTS.md` | keep if loaded by directory convention |
| `docs/features/AGENTS.md` | keep if loaded by directory convention |
| `docs/private-tool-context.md` | review before archive or merge |
| `docs/sources/AGENTS.md` | keep if loaded by directory convention |

## Next Cleanup Pass

1. Reduce unresolved local-looking refs that point to missing active surfaces,
   especially template-era `docs/progress.md` and old external repo paths.
2. Keep `docs/review/rubrics/*` as canonical docs even when individual family
   files are primarily reached through the directory and rubric index.
3. Move temporary research and speculative notes to tickets, experiments, or
   `tmp/**`; keep tracked docs for live contracts and generated inventories.
4. Use this report before deleting or moving docs: redirect active inbound refs
   first, then remove the superseded file.
