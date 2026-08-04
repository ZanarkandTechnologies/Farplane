# Bin

Executable helpers for the Codex harness.

## Purpose

This folder contains public command wrappers used by the live Codex config plus
shared repo commands that are intentionally broader than one skill package.
Core implementations live under `bin/core/`; hook/runtime implementations live
under `bin/runtime/`; Core tests live under `bin/tests/`; validators live under
`bin/validators/`; package-specific scripts should live with their owning
package, such as `skills/<name>/scripts/`.

Primary control plane:

- `impl-plan`
- `goal-advisor`
- persistent builder lanes

Live Stop handling applies the final-response prose budget and sends telemetry.
Native Goal mode plus ticket-local QA/review evidence owns completion.

Inspect response accounting without invoking the hook:

```bash
farplane response check --stdin --json < response.md
farplane response check response.md --json
```

Codex does not need to draft its final answer into a file for the normal path.
The installed Stop hook receives `last_assistant_message` and applies the same
accountant automatically. Path/stdin mode is an optional preflight for agents,
operators, tests, and any Markdown file that benefits from category counts.

Exit `0` means prose is within its configured word and line limits; exit `1`
means it is over. Closed Mermaid blocks, exact absolute/HTTPS image-video
embeds, and a trailing link-only References/Citations section are reported
separately. Malformed or mixed forms remain prose.

The `bin/` directory is now mostly shim/utility territory, not the main
orchestration story. `install.sh` installs an explicit allowlist of live
runtime helpers instead of symlinking every script, validator, and test.

## Entrypoints

- `farplane validate ticket <ticket.md> --phase planning|complete` - canonical
  ticket-facing validation API. Completion also requires an explicit `--base`
  or repeated `--path`; receipts are written under the ticket's
  `artifacts/validation/` directory.
- `core/validation/*` - shared selection, execution, and receipt machinery.
- `validators/farplane_checks.py` - allowlisted Farplane-wide leaf checks;
  skill-specific validators remain under `skills/<owner>/scripts/`.
- `validators/check_harness_invariants.py` - narrow validator for high-value root/runtime/ticket-boundary invariants
- `farplane` / `farplane.py` - Core-owned global CLI for install, hooks,
  doctor checks, UI linking/start, skill rollout projections, and delegation
  into the linked Farplane-UI module checkout
- `core/*` - implementation modules for the global CLI, ticket lifecycle,
  mining, telemetry status, and adoption helpers
- `runtime/*` - implementation modules for Codex hooks, user-turn capture,
  notification, and runtime telemetry
- `tests/*` - Core-owned tests for `bin/core`, `bin/runtime`, and public
  command wrappers
- `validators/check_doc_parity.py` - narrow canonical-doc parity validator for README/spec/ticket surfaces
- `validators/check_doc_refs.py` - local reference validator for active docs and registries;
  use `--all` for broader cleanup audits across tickets, experiments, and tests
- `validators/sync_skill_registry.py` - deterministic generated-registry check
  for `docs/skills/registry.jsonl`
- `validators/check_skill_todo_tiers.py` - first-load skill todo dependency
  validator
- `validators/check_tier0_phase_protocol.py` - Tier 0 phase-protocol migration
  guard
- `validators/check_skill_capabilities.py` - skill capability fixture validator
- `validators/check_template_version_metadata.py` - staged metadata and
  version-bump guard for template files listed in
  `rules/template-version-watch.toml`
- `validators/check_source_line_growth.py` - deterministic pre-commit and
  pre-push guard that blocks new Python files over 500 lines and growth in
  already-oversized files. `rules/source-line-baseline.toml` is the one-time
  adoption ceiling until the comparison base contains the guard.
- `capture_user_turn.py` - turn-start user-intent writer for the hook surface
- `core/farplane_ticket_close.py` - explicit ticket completion, archive, event,
  and mining boundary used by `farplane ticket finalize TASK-XXXX --github-issue-url URL`
- `core/farplane_event_store.py` - durable local event/outbox primitives shared
  by explicit Core commands
- `farplane.py adoption scan` - local adoption resolver for project
  `farplane/manifest.json` pins, optional project `.agents/skills/`, feature/template
  registries, drift, and Office-consumable adoption stats; implementation lives
  in `bin/core/farplane_adoption.py`
- `notify.py` - local notification helper
The installed binary allowlist contains one user-facing command, `farplane`,
plus the hook and notification launchers that Codex configuration calls
directly. Internal helpers are imported from `bin/core/` or `bin/runtime/`;
they are not separately installed command surfaces.

`farplane.py` is only the executable edge. Parser construction, install/hooks,
UI/config, and domain command adapters live in focused `bin/core/farplane_cli_*`
modules so each responsibility stays independently testable and below the
source-size ceiling.

Runtime state stays lightweight and machine-facing. The grouped `claim` object
tracks the active ticket/run/session ownership for hook consumers, while
`last_user_turn` carries the saved current-turn user ask.

For live multi-session coordination:

- `session_id` remains the transport/runtime identity
- `session_name` is the human-facing session alias, derived from the runtime
  session as `codex-<session-fragment>` such as `codex-019ef784`
- `session_origin` records whether a session is `control`, `internal`, or `non_owning`
- ticket frontmatter may mirror only the human-facing alias as `claimed_by`
- raw `session_id` should stay runtime-only

Delegated worker metadata is additive:

- `worker_name` identifies the lane role for the current live path
- `main_artifact_path` points at the worker's canonical work object
- `grounding_summary` captures the worker's explicit artifact-grounding line when available
- `worker_started_at`, `last_checkpoint_at`, and `checkpoint_summary` support stale-wait backpressure reads

The live `status` surface now derives a first advisory backpressure signal:

- `backpressure_state`: `within_budget`, `over_budget`, `inactive`, or `unknown`
- `stale_for_secs`: elapsed seconds since the latest checkpoint when available
- `recommended_action`: present for over-budget waits

Runtime routing is session-first for parallel Codex usage:

- explicit run-state selector when a managed lane exports one
- hook `session_id` for telemetry and association-log correlation
- `.farplane/state/ticket-thread-associations.jsonl` for ticket/thread joins
- completed ticket packets plus optional bounded operator-turn windows as
  improvement-mining evidence, with one deduped Core-projected `todo` ticket
  when a grounded issue and improvement exist

`UserPromptSubmit` no longer writes `.farplane/state/current-run.json` or
`.farplane/state/sessions/<session_id>.json`. Those Ralph-era singleton and
per-session files may remain in fixtures or historical local state, but they
are not authoritative runtime ownership surfaces.

## Preferred Agent-Facing Command Surfaces

Use the existing helpers directly, but prefer output modes that keep routine
success quiet and make failure output the thing that stands out.

- `python3 skills/delegate-cli/scripts/delegate_cli_agent.py doctor --profile frontend-pi-kimi --json`
  Use before a live external CLI run to check the profile templates, copied
  skill sources, executable, and required environment variables
- `python3 skills/delegate-cli/scripts/delegate_cli_agent.py run --profile frontend-pi-kimi --ticket <ticket> --dry-run --json`
  Use to render the Pi/Kimi frontend delegation prompt, command, runtime logs,
  and durable ticket artifacts without spending tokens or editing files
- `python3 skills/skill-maintenance/scripts/install_selected_skills.py --search frontend`
  Use to discover shareable skills without rendering the full Farplane config.
- `python3 skills/skill-maintenance/scripts/install_selected_skills.py --skills review,visual-qa --dry-run`
  Use to preview selected skill symlinks into `~/.codex/skills`.
- `python3 skills/skill-maintenance/scripts/import_installed_skills.py --list`
  Use to list installed Codex skills and see whether each already exists in
  repo source.
- `python3 skills/skill-maintenance/scripts/import_installed_skills.py --skills notion-task-field-fill,reel-collage --dry-run`
  Use to preview importing installed skills into `skills/*` before writing.
- `python3 skills/skill-maintenance/scripts/import_installed_skills.py --skills <name> --overwrite`
  Use to replace an existing repo skill from the installed copy, with the old
  repo package backed up under `.farplane/import-backups/`.
- `python3 skills/skill-maintenance/scripts/sync_skill_plugins.py --check`
  Use after changing `skills/*` to prove plugin packages can still be generated.
- `python3 skills/skill-maintenance/scripts/sync_skill_plugins.py --install-local --plugins farplane-core`
  Use to expose selected Farplane plugin bundles through your personal Codex
  marketplace under `~/.agents/plugins`.
- `python3 skills/pr-review-watch/scripts/pr_review_watch.py classify --repo <repo> --pr <number> --json`
  Compatibility command for the `pr-review-watch` skill-owned classifier.
- `python3 bin/validators/check_doc_refs.py`
  Use after moving docs or updating local references. The old top-level
  `bin/check_doc_refs.py` wrapper was removed during TASK-0218 bin
  minimization.
- `python3 bin/validators/sync_skill_registry.py --check`
  Use after skill metadata changes when debugging the broader
  `skills/skill-maintenance/scripts/check_skills.py --write` path.
- `python3 bin/farplane.py adoption scan --project-root . --json`
  Use to inspect a project's Farplane manifest pins, local skill presence,
  feature/template adoption, and drift against the global Farplane standard.
- `python3 bin/farplane.py adoption scan --roots-file ~/.farplane/state/projects.json --json`
  Use when Farplane Office or global state already knows the local project
  roots; the CLI reads the same project-root list shape instead of crawling the
  whole computer.
- `python3 bin/farplane.py skills rollout scan --json`
  Use to inspect the current skill rollout and template-consumer projection that
  Farplane UI can render without reading generated graph files directly.
- `python3 tickets/scripts/check_ticket_metadata.py`
  Current mode: already near the desired quiet-success shape; keep the single-line pass output

Examples:

```text
followup ok: TASK-0033 -> building pane=%42 session=main run=.farplane/runs/task-0033-building-20260410T091500000000Z.json dry-run
```

## Minimal Example

```bash
python3 skills/delegate-cli/scripts/delegate_cli_agent.py doctor --profile frontend-pi-kimi --json
python3 skills/delegate-cli/scripts/delegate_cli_agent.py run \
  --profile frontend-pi-kimi \
  --ticket tickets/TASK-0014/ticket.md \
  --dry-run \
  --json

```

In the live interactive path, `goal-advisor` compiles the Goal-backed ticket
execution contract. Native Goal mode owns persistence and ticket-local
QA/review evidence owns completion; the live Stop hook adds only a deterministic
final-response length retry beside telemetry.

## How To Test

- `python3 bin/validators/check_harness_invariants.py`
- `python3 bin/validators/check_doc_parity.py`
- `python3 bin/validators/check_doc_refs.py`
- `python3 -m unittest bin/validators/test_harness_invariants.py`
- `python3 -m unittest bin/validators/test_doc_parity.py`
- `python3 -m unittest skills/delegate-cli/scripts/test_delegate_cli_agent.py`
- `python3 -m unittest skills/pr-review-watch/scripts/test_pr_review_watch.py`
- `python3 -m unittest bin/tests/test_ticket_metadata.py`
- `python3 -m unittest bin/tests/test_ticket_runtime.py`
- `python3 -m py_compile bin/core/farplane_ticket_runtime.py bin/tests/test_ticket_runtime.py`
- `python3 -m py_compile bin/capture_user_turn.py bin/runtime/capture_user_turn.py bin/runtime/user_turn.py`
- `python3 -m py_compile bin/validators/check_harness_invariants.py bin/validators/test_harness_invariants.py`
- `python3 -m py_compile bin/validators/check_doc_parity.py bin/validators/test_doc_parity.py`
- `python3 -m py_compile bin/validators/check_doc_refs.py bin/validators/test_check_doc_refs.py`
- `python3 -m unittest bin/validators/test_check_template_version_metadata.py`
- `python3 -m py_compile skills/delegate-cli/scripts/delegate_cli_agent.py`
- `python3 -m unittest discover -s bin/tests -p 'test_*.py'`
