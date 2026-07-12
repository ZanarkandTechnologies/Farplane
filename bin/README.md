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

Live Stop handling sends telemetry only. Native Goal mode plus ticket-local
QA/review evidence owns completion.

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
- `core/*` - implementation modules for global CLI, invocation, board, compute,
  ticket-runtime, telemetry-status, and adoption helpers
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
- `validators/check_changed_file_line_count.py` - staged-only warning for
  files enrolled in explicit line-count limits; it never rewrites files or
  calls a model
- `capture_user_turn.py` - turn-start user-intent writer for the hook surface
- `hooks/farplane_file_change.py` - PostToolUse file-change boundary; captures
  typed events to the local outbox and launches the fixed Core drain subprocess
- `hooks/farplane_local_event.py` - PostToolUse local skill/thread telemetry
  capture without Farplane UI, Node, or `tsx`
- `farplane_boards.py` - board adapter contract plus the filesystem
  `FileTicketAdapter` that normalizes `tickets/TASK-*/ticket.md` into a
  `WorkItem`
- `farplane_compute.py` - compute admission policy for `local_shared`,
  `local_worktree`, `symphony`, and `codex_cloud`; it emits blockers and setup
  hints but never launches compute
- `farplane_invocation.py` - contract helper for `WORKFLOW.md`,
  `FarplaneRunEnvelope`, board-backed `WorkItem`, compute selection, skill
  routing, and `ProofPacket` validation; it does not launch Codex
- `farplane.py adoption scan` - local adoption resolver for project
  `farplane/manifest.json` pins, optional project `.agents/skills/`, feature/template
  registries, drift, and Office-consumable adoption stats; implementation lives
  in `bin/core/farplane_adoption.py`
- `notify.py` - local notification helper
- `ticket_runtime.py` / `ticket-runtime` - local helper for ticket runtime
  records, optional isolated checkouts, port reservation, runtime
  launch/teardown, and QA target lookup

## Runtime Decisions

- `capture_user_turn.py`: keep
- `ticket_runtime.py`: keep

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
- conversation windows for lightweight prompt/response cadence

`UserPromptSubmit` no longer writes `.farplane/state/current-run.json` or
`.farplane/state/sessions/<session_id>.json`. Those Ralph-era singleton and
per-session files may remain in fixtures or historical local state, but they
are not authoritative runtime ownership surfaces.

See [the invocation and adapters spec](../docs/features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md) for the canonical runtime and invocation decision table.

## Preferred Agent-Facing Command Surfaces

Use the existing helpers directly, but prefer output modes that keep routine
success quiet and make failure output the thing that stands out.

- `python3 bin/ticket_runtime.py ensure ...`
  Use when a skill or operator needs a ticket-scoped runtime record, optional
  isolated checkout path, declared commands, and QA targets without launching yet
- `python3 bin/ticket_runtime.py up ...`
  Use when the ticket runtime should actually start configured frontend/backend
  processes or a compose-backed runtime
- `python3 bin/ticket_runtime.py qa ...`
  Use when QA needs the current runtime status plus only the live targets that
  are actually open for the ticket right now
- `python3 bin/ticket_runtime.py down ...`
  Use when the helper should stop tracked processes or run the declared
  compose-down command, then release reserved ports
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
- `python3 -m unittest bin/tests/test_farplane_boards.py`
  Use to prove the filesystem BoardAdapter path containment and ticket
  normalization contract before changing invocation or Ralph selection behavior
- `python3 -m unittest bin/tests/test_farplane_compute.py`
  Use to prove compute precedence, blockers, worktree runtime hints, and future
  target behavior without launching local or remote compute
- `python3 bin/farplane_invocation.py prepare --ticket <ticket> --phase planning --proof .farplane/results/<ticket>.proof.json`
  Use to validate a local Farplane invocation envelope and inspect the selected
  skill route without launching Codex
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
python3 bin/ticket_runtime.py up \
  --ticket TASK-0014 \
  --branch pr-123 \
  --checkout-mode worktree \
  --runtime-mode branch-runtime \
  --create-worktree \
  --reserve frontend \
  --reserve backend \
  --frontend-cmd "npm run dev" \
  --backend-cmd "npm run api" \
  --json

python3 bin/ticket_runtime.py qa --ticket TASK-0014 --json
python3 bin/ticket_runtime.py down --ticket TASK-0014 --json

python3 skills/delegate-cli/scripts/delegate_cli_agent.py doctor --profile frontend-pi-kimi --json
python3 skills/delegate-cli/scripts/delegate_cli_agent.py run \
  --profile frontend-pi-kimi \
  --ticket tickets/TASK-0014/ticket.md \
  --dry-run \
  --json

```

In the live interactive path, `goal-advisor` compiles the Goal-backed ticket
execution contract. Native Goal mode owns persistence and ticket-local
QA/review evidence owns completion; live Stop hooks are telemetry-only.

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
- `python3 -m py_compile bin/ticket_runtime.py bin/core/ticket_runtime.py bin/tests/test_ticket_runtime.py`
- `python3 -m py_compile bin/capture_user_turn.py bin/runtime/capture_user_turn.py bin/runtime/user_turn.py`
- `python3 -m py_compile bin/validators/check_harness_invariants.py bin/validators/test_harness_invariants.py`
- `python3 -m py_compile bin/validators/check_doc_parity.py bin/validators/test_doc_parity.py`
- `python3 -m py_compile bin/validators/check_doc_refs.py bin/validators/test_check_doc_refs.py`
- `python3 -m unittest bin/validators/test_check_template_version_metadata.py`
- `python3 -m py_compile skills/delegate-cli/scripts/delegate_cli_agent.py`
- `python3 -m unittest discover -s bin/tests -p 'test_*.py'`
