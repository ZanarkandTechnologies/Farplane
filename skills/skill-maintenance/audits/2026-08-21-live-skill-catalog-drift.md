---
skill: skill-maintenance
date: 2026-08-21
change_type: maintenance
owner: skill-maintenance
status: pass
review_route: reviewer
review_tas: TAS-A
before_ref: /Users/kenjipcx/.codex/skills
after_ref: docs/skills/registry.jsonl
reasoning_basis: operator_correction + local_inventory + git_history
proof_artifacts:
  - tickets/TASK-0442/artifacts/qa/2026-08-21_005900_live_skill_catalog/result.json
  - tickets/TASK-0442/artifacts/live-skill-catalog-review.md
eval_required: no
eval_skip_reason: deterministic installer, filesystem-set, and registry behavior
---

# Live Skill Catalog Drift Audit

## Change

- Before: Farplane source and registry agreed at 117, but nine previously
  retired `source: local` packages remained as copied top-level directories and
  three nested test-fixture SKILL files were published inside installed
  packages.
- After: source SKILL files, registry rows, and live top-level Farplane SKILL
  files are equal at 117; known retired copies are recoverably pruned by one
  installer-owned retirement ledger.
- Why: the installer correctly protected unknown and personal directories, but
  copied Farplane packages have no provenance marker and therefore survived
  after their source deletion unless their names were explicitly retired.
- Tradeoff accepted: retirement remains an explicit name set so Farplane never
  guesses that an unknown local directory is safe to delete.

## Inventory And Decisions

| Surface | Observed | Decision | Reason |
| --- | ---: | --- | --- |
| Farplane `skills/*/SKILL.md` | 117 | keep | Canonical source matches the generated registry exactly. |
| Live top-level Farplane SKILL files | 126 before, 117 after | prune 9 | The extras were deleted in prior commits and had no source or registry row. |
| Nested Farplane fixture SKILL files | 3 before, 0 after | exclude package `tests/` | Test fixtures are validator inputs, not callable skills. |
| Codex `.system` skills | 6 | keep outside registry | Native Codex-owned packages, not Farplane source. |
| Project `.agents/skills` | 5 | keep outside root registry | Project-local capability skills documented by `.agents/skills/README.md`. |
| Plugin cache SKILL files | 109 cached files | keep outside registry | Provider/plugin-owned cache, including duplicate inactive versions; not Farplane installs. |
| Empty `codex-primary-runtime` directory | 0 SKILL files | remove | Not a skill or active provider package. |

The nine pruned packages are `agent-behavior-test`, `data-viz`,
`deep-ui-design`, `delegate-frontend`, `frontend-craft`, `frontend-design`,
`react-flow`, `update-strategy`, and `video-production`.

The nested fixture leaks were `bad-signature-rollout`, `installed-copy-only`,
and `handoff-preparer`. Installed packages now exclude `tests/`, and a stale
installed tests tree forces package refresh instead of comparing as current.

Git history confirms deliberate retirement ownership:

- `agent-behavior-test` -> Eval behavior traces and `agent-qa-test` proof;
- six frontend/index/router packages -> bounded UI facets, `impl-plan`, and
  generic `delegate-cli` (`1693dcdb`);
- `update-strategy` -> simplified Interval metric-to-ticket loop (`e74891b0`);
- `video-production` -> content/video artifact owners (`f37068e1`).

## Telemetry Finding

The remembered SKILL-read hook is not present. `hooks.json` runs
`skill_file_line_gate.py` only after `apply_patch`, `Edit`, or `Write`; that
hook enforces the 200-line edit limit and emits no Farplane usage event.
`capture_user_turn.py` records explicit `$skill` requests. The Eval runner has
an offline heuristic that recognizes SKILL.md shell reads in `codex exec
--json`, but it is not a live hook and must not be treated as invocation data.

Parsing arbitrary shell commands as skill loads would miss native prompt loads
and count maintenance/support reads as invocations. Actual invocation telemetry
therefore remains unavailable until Codex exposes a structured load event or a
structured file-read hook used by every skill load path.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `source_registry_equality` | pass | 117 source names equal 117 registry names. |
| `live_registry_equality` | pass | 117 live top-level SKILL names equal registry names after reinstall. |
| `physical_retirement` | pass | All 18 current and previously missed retired SKILL paths are absent live and in source. |
| `recursive_fixture_absence` | pass | Recursive live inspection finds only six Codex-owned `.system` SKILL files outside top-level Farplane packages. |
| `external_ownership` | pass | System, plugin, and project-local skills remain outside root registry. |
| `safe_pruning` | pass | Unknown external symlinks/directories remain protected; explicit retired copies move to backup. |
| `single_owner` | pass | `install_selected_skills.py` owns all skill retirement names. |
| `telemetry_claim` | pass | Explicit requests and actual invocations remain separately named. |
| `review_tas_rate` | pass | Independent completion review returned TAS-A with no hard gates. |

## Proof

- Installer dry run selected exactly nine stale directories for pruning.
- Full `farplane install` moved them under
  `/Users/kenjipcx/.codex/.install-backups/20260821-005349/skills/` and
  reinstalled/refreshed the canonical source set.
- A second full install refreshed packages carrying stale `tests/` trees with
  backups under `/Users/kenjipcx/.codex/.install-backups/20260821-005823/`.
- Twenty-two focused installer/surface tests pass after operated installation.
- Deterministic QA passes all catalog/retirement/hook gates; the independent
  completion review is TAS-A with no rerun required.

## Followup

- Future portfolio audits must report source, registry, live top-level,
  project-local, system, and active plugin surfaces separately rather than
  calling the source registry the entire Codex catalog.
- Live installation must not publish package `tests/` directories. Test
  fixtures can contain `SKILL.md` files that Codex discovers as callable
  skills, so `install_selected_skills.py` now treats those paths as
  unpublishable drift and refreshes installed packages that still contain them.
