---
skill: skill-maintenance
date: 2026-08-24
change_type: maintenance
owner: skill-maintenance
status: pass
review_route: reviewer
review_tas: TAS-A
before_ref: skills/skill-maintenance/audits/2026-08-23-shortcut-ensemble-consolidation.md
after_ref: skills/skill-maintenance/scripts/install_selected_skills.py
reasoning_basis: first_principles + local_contracts + live_install
proof_artifacts:
  - tickets/TASK-0442/artifacts/qa/2026-08-24_004721_ensemble-retirement/report.md
eval_required: no
eval_skip_reason: deterministic source/registry/live set reconciliation and installer behavior
---

# Ensemble Retirement Live Reconciliation

## Change

- Before: six Aug. 23 source-retired packages remained copied in live Codex;
  source and registry had 114 packages while live had 120.
- After: the installer explicitly retires all six packages; source, registry,
  and live top-level Farplane catalog are equal at 114.
- Why: an unknown local directory must stay protected, but a source-retired
  Farplane package must not remain a callable legacy entrypoint.
- Tradeoff accepted: owner-local `ensemble.yaml` is the only budget-depth
  mechanism. Direct is default; `auto|max` is explicit and never inherited.

## Evidence For Budget Advisor Retirement

The retired package's useful behavior is already owned locally: five packages
provide explicit `ensemble=auto|max`, complete owner personas, independent
first passes, dissent preservation, direct defaults, and stable owner outputs.
No active source caller references its deleted `BudgetRequest`, time, coverage,
custom-persona, or child-budget fields. Restoring a generic adapter would add a
second control surface without a current consumer.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `source_registry_equality` | pass | 114 source names equal 114 registry names. |
| `live_registry_equality` | pass | 114 live top-level names equal registry names after install. |
| `physical_retirement` | pass | All six named copies are absent and recoverably backed up. |
| `ensemble_contract` | pass | Typed linter reports five ensembles and 23 personas. |
| `legacy_eval_metadata` | pass | Derived eval discovery accepts the removed `ad-advisor` `eval:` field. |
| `unknown_directory_safety` | pass | Installer prunes only explicit retired names or repo-managed copies. |
| `review_tas_rate` | pass | Independent correction review returned TAS-A. |

## Proof

- `python3 skills/skill-maintenance/scripts/check_skills.py --write` passed.
- 80 focused contract, registry, installer, install-bin, clean-HOME
  install-render, and runtime telemetry tests passed.
- The installer now reads its four display fields with the standard library,
  keeping the rendered-install path independent of the lint-only YAML stack.
- `farplane run -- farplane install` wrote recoverable backups at
  `/Users/kenjipcx/.codex/.install-backups/20260824-004630/skills/` and
  `/Users/kenjipcx/.codex/.install-backups/20260824-004721/skills/`.
- Source, registry, and live top-level catalog all contain 114 skills; no
  nested non-system SKILL files remain.
- Independent correction review returned `pass` / `TAS-A` after rerunning the
  installer, clean-environment, catalog, and contract evidence; see
  `tickets/TASK-0442/artifacts/ensemble-retirement-review.md`.

## Followup

Do not reintroduce a generic budget router unless a caller needs behavior the
owner-local ensemble contract cannot represent. TASK-0442 awaits only operator
acceptance and explicit remote finalization.
