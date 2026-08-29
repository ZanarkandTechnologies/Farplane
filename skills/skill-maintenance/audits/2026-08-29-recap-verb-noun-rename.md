---
skill: skill-maintenance
date: 2026-08-29
change_type: migration
owner: skill-maintenance
status: pass
before_ref:
  - skills/product-backbrief/
  - skills/task-recap/
after_ref:
  - skills/recap-idea/
  - skills/recap-task/
reasoning_basis: operator-naming-decision
proof_artifacts:
  - skills/recap-idea/evals/evals.json
  - skills/recap-task/evals/evals.json
  - .farplane/evals/runs/20260829T032515Z-recap-idea-rename-proof-20260829/summary.json
  - .farplane/evals/runs/20260829T032534Z-recap-task-rename-proof-20260829/summary.json
eval_required: yes
---

# Recap Verb–Noun Rename Audit

## Change

- Before: the related shortcuts used inconsistent noun–noun names:
  `product-backbrief` and `task-recap`.
- After: both use the operator-selected verb–noun command family:
  `recap-idea` and `recap-task`.
- Migration rule: one canonical name and package path per skill; no aliases,
  compatibility directories, or fallback identifiers remain.

## Scope

- Rename both package directories, frontmatter names, callable signatures,
  eval suite names and IDs, fixture paths, agent prompt, planner profile,
  reader-facing skill routing, and generated registry rows.
- Preserve each skill's distinct truth contract and behavior.
- Preserve dated audit evidence under the new canonical package paths.
- Do not modify the installed copies under `~/.codex/skills/`; repo source is
  canonical and installation remains a separate explicit operation.

## Proof Plan

- Run JSON and changed-eval contract validation for both suites.
- Regenerate the skill registry and require all skill-system checks to pass.
- Run focused candidate behavior proof for one core case per renamed skill.
- Search active non-audit surfaces for stale identifiers.
- Obtain independent contract and integration review.

## Proof Results

- `farplane lint evals --changed --json`: pass; 82 manifests checked.
- `check_skills.py --write`: pass; all 12 skill-system checks passed and the
  114-row canonical registry was regenerated.
- Active non-audit stale-identifier search: empty for `product-backbrief`,
  `task-recap`, `product_backbrief`, and `task_recap`.
- `recap_idea_selects_user_visible_ui_flow_01`: candidate gate passed, score
  `1.0`, and the observed skill name was `recap-idea`.
- `recap_task_full_ticketed_context_01`: candidate gate passed, score `1.0`,
  and the observed skill name was `recap-task`.
- Focused execution exposed duplicated fixture roots in `recap-task`; all
  file-backed eval paths were corrected to package-relative `examples/...`
  paths before the passing receipt was recorded.
- `git diff --check` on the migration surfaces: pass.

## Review

- Verdict: `TAS-A`, pass, no rerun required, and no hard-gate failures.
- Canonical path, registry, profile, docs routing, agent prompt, distinct
  contracts, eval identifiers, focused receipts, and repo-only installation
  boundary all passed independent inspection.
- Non-blocking scope note: broader pre-existing changes in the generated skill
  registry and skill README were not attributed to this rename.
