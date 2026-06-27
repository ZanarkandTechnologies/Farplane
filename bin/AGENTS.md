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
  global Farplane CLI edge, shared cross-skill commands, repo-wide validator
  wrappers, or compatibility wrappers for moved public commands
- put Core helper implementations under `bin/core/`, Codex hook/runtime
  implementations under `bin/runtime/`, and Core-owned tests under `bin/tests/`
- move skill-specific implementations and their tests to
  `skills/<owner>/scripts/`
- move repo-wide validators and validator tests to `bin/validators/`
- delete generated caches such as `__pycache__`

When in doubt, add the implementation to the owning package and leave a tiny
`bin/` wrapper only if an existing public command path must keep working.

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
- orchestrator composes worker + judge; it does not implement code itself
- tickets remain the canonical execution contract
- explicit ticket selectors outrank ambient run-state when both are present
- explicit run-state selectors outrank hook `session_id`, which outranks ambient `.farplane/state/current-run.json`
- run-state files remain runtime-only and lightweight
- runtime state should group active execution ownership into a lightweight `claim` object instead of scattering claim semantics across multiple ad hoc top-level reads
- native Goal mode owns implementation persistence. Legacy Stop-hook
  same-ticket continuation, `auto_continue`, and runtime claim routing are
  quarantined and must not be used as live completion authority.
- `close-ticket` is the canonical live documenting-phase control skill. Runtime
  parsing may still accept `$docs-closeout` as an alias, but live prompts and
  handoffs should use `$close-ticket`. See `MEM-0043`.
- on completion-like paths, ticket-local QA/review evidence is the authority;
  the main model's completion claim is candidate-only until the ticket's
  `Done / Proof`, Goal program, and required delegated reviews are satisfied.
- delegated workers should keep `worker_name`, `main_artifact_path`, and `grounding_summary` visible in the same runtime contract when available
- delegated stale-wait reads should stay advisory-first and use explicit checkpoint timing instead of hidden watchdog behavior
- current-turn user intent should be captured at `UserPromptSubmit` when available; worker-entry capture is fallback-only degraded mode
- canonical current-turn capture belongs only to control sessions whose first owned prompt explicitly invokes a public control skill; internal or non-owning sessions must not overwrite `.farplane/state/current-run.json`. See `MEM-0029`.
- native Goal mode owns implementation persistence; stored `session_id` is a recovery hint only. See `MEM-0005`.
- legacy stop-hook role configs are TOML-backed under `agents/*.toml` and are
  not live by default. If this runtime is revived, keep stdout machine-only and
  reserve diagnostics for stderr. See `MEM-0010` and `MEM-0056`.
