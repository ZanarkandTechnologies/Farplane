---
skill: skill-maintenance
date: 2026-08-23
change_type: maintenance
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: install.sh
after_ref: rules/skill-profiles.toml
reasoning_basis: first_principles + local-evidence
proof_artifacts:
  - skills/skill-maintenance/scripts/test_render_skill_profiles.py
  - bin/tests/test_install_config_render.py
eval_required: no
---

# Skill Audit: Installer Profile Rendering

## Change

- Before: full install backed up twelve generated role profile files without recreating them and did not migrate desktop or plugin tables into the local config overlay.
- After: the source-owned profile map renders replacement matrices after registry validation; the installer preserves `desktop` and `plugins.*` blocks in `config.local.toml`.
- Why: install must be recoverable without depending on stale live-generated files.
- Tradeoff accepted: profile membership is explicit role policy in one compact rule file, not inferred from unrelated capability metadata.

## First-Principles Reasoning

- Objective: keep full install idempotent for the installed role profiles and Codex Desktop runtime configuration.
- Placement logic: role membership belongs in `rules/skill-profiles.toml`; deterministic rendering belongs in the skill-maintenance script; destination writes and backups belong in `install.sh`.
- Expected behavior delta: a full install validates and recreates 12 profile matrices while retaining local desktop/plugin configuration across config rendering.
- Proof needed: unit-render proof, temporary-home full-install proof, TOML parse, and independent integration review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | No prompt or skill first-load change. |
| `reference_load_precision` | pass | The renderer loads only the registry and role map. |
| `missing_context_rate` | pass | Every manifest skill is checked against the registry. |
| `noisy_context_rate` | pass | Profile membership is outside global prompts. |
| `duplicated_instruction_count` | pass | One source manifest replaces twelve live-only outputs. |
| `prompt_size_tokens` | pass | No always-loaded prompt expansion. |
| `task_success_rate` | pass | Temporary-home install test passes. |
| `review_tas_rate` | pass | Native reviewer returned TAS-A. |
| `maintenance_locality` | pass | Policy, renderer, installer, and tests use their owner surfaces. |
| `composition_clarity` | pass | The renderer has one input map and explicit installed outputs. |

## Proof Artifacts

- `python3 -m unittest skills.skill-maintenance.scripts.test_render_skill_profiles bin.tests.test_install_config_render bin.tests.test_install_bin_surface` passes 9 tests.
- The install test runs against a temporary Codex home and verifies generated profile files, generated base matrix, valid TOML, and preserved desktop/plugin values.
- Live installation rendered 12 profiles across 65 managed skills, refreshed 118 installed skills, preserved 23 local TOML tables, and backed up the prior config and generated profile files under `/Users/kenjipcx/.codex/.install-backups/20260823-185227/`.
- Reviewer receipt: native reviewer lane returned TAS-A for integration readiness, evidence quality, code quality, and debloatability; no hard-gate failures.
- Eval required: no; this is deterministic installer behavior covered by unit and integration tests.

## Before Behavior

- Generated profile files could be moved into the install backup without a source renderer to recreate them.
- Desktop and plugin activation state could remain only in the overwritten rendered config.

## After Behavior

- `render_profiles(repo, output_dir) -> base_matrix + profile_files` validates source policy before touching the target.
- Full install migrates desktop/plugin tables to the local overlay and installs fresh profile files from generated temporary output.

## Followups

- No follow-up is required for the installer repair.
