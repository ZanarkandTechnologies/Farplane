# `bin/AGENTS.md`

Rules for executable helper scripts in `bin/`.

## Purpose

Scripts here are small operational helpers for the live Codex harness.
Top-level `bin/` is for runtime shims and intentionally shared commands.
Repo-wide checks belong in `bin/validators/`; package-specific scripts belong
under the owning package, such as `skills/<name>/scripts/`.

## Placement Gate

Before adding a top-level `bin/*` file, classify it:

- keep top-level `bin/` files only for live installed hook/runtime shims, the
  global Farplane CLI edge, shared cross-skill commands, or repo-wide validator
  wrappers
- put Core helper implementations under `bin/core/`, Codex hook/runtime
  implementations under `bin/runtime/`, and Core-owned tests under `bin/tests/`
- move skill-specific implementations and their tests to
  `skills/<owner>/scripts/`
- move repo-wide validators and validator tests to `bin/validators/`
- delete generated caches such as `__pycache__`

When in doubt, add the implementation to the owning package.

## Keep Scripts

- explicit
- low-magic
- file-first
- easy to inspect and debug

## Do Not

- hide orchestration policy in shell tricks
- mutate ticket board state silently
- require network services unless the script is explicitly for that purpose

## Runtime Helper Rules

For runtime helper scripts:

- worker launcher runs exactly one bounded phase
- judge decides only from ticket + result + evidence state
- tickets remain the canonical execution contract
- explicit ticket selectors outrank ambient run-state when both are present
- explicit run-state selectors outrank hook `session_id`; ambient singleton
  current-run files are retired as authority
- run-state files remain runtime-only and lightweight
- runtime state should group active execution ownership into a lightweight `claim` object instead of scattering claim semantics across multiple ad hoc top-level reads
- native Goal mode owns implementation persistence. Stop hooks are telemetry
  boundaries and must not be used as live completion authority.
- `close-ticket` is the canonical live documenting-phase control skill. Runtime
  parsing does not accept the retired docs-closeout alias; live prompts and
  handoffs should use `$close-ticket`.
- on completion-like paths, ticket-local QA/review evidence is the authority;
  the main model's completion claim is candidate-only until the ticket's
  `Done / Proof`, Goal program, and required delegated reviews are satisfied.
- after those gates pass, `farplane ticket close TASK-XXXX` owns the successful
  terminal metadata, archive movement, completion event, and mining route.
- delegated workers should keep `worker_name`, `main_artifact_path`, and `grounding_summary` visible in the same runtime contract when available
- delegated stale-wait reads should stay advisory-first and use explicit checkpoint timing instead of hidden watchdog behavior
- current-turn user intent should be captured at `UserPromptSubmit` through
  hook telemetry and conversation windows when available
- canonical prompt capture must not create or mutate singleton
  `.farplane/state/current-run.json` or per-session ownership files; use hook
  telemetry, explicit run-state selectors, tickets, and association logs
  instead. See `MEM-0029`.
- native Goal mode owns implementation persistence; stored `session_id` is a recovery hint only. See `MEM-0005`.
