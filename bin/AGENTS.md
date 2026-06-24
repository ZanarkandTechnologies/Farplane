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
- same-ticket `goal-advisor` continuation must require both an explicit
  session-scoped loop gate and a matching runtime `claim`; legacy
  `auto_continue` must not be treated as activation truth. See `MEM-0025`.
- explicit `goal-advisor` control-session turns must seed selected-ticket
  runtime ownership when ticket resolution is explicit or unambiguous; a
  session-only control stub is not enough for Stop-hook same-ticket
  continuation. See `MEM-0032`.
- `close-ticket` is the canonical live documenting-phase control skill. Runtime
  parsing may still accept `$docs-closeout` as an alias, but live prompts and
  handoffs should use `$close-ticket`. See `MEM-0043`.
- on completion-like paths, Stop-hook reviewer judgment is the authority for routing to the orchestrator; the main model's completion claim is candidate-only, and reviewer must fail completion when an obvious in-scope next step still remains. See `MEM-0034`.
- delegated workers should keep `worker_name`, `main_artifact_path`, and `grounding_summary` visible in the same runtime contract when available
- delegated stale-wait reads should stay advisory-first and use explicit checkpoint timing instead of hidden watchdog behavior
- current-turn user intent should be captured at `UserPromptSubmit` when available; worker-entry capture is fallback-only degraded mode
- canonical current-turn capture belongs only to control sessions whose first owned prompt explicitly invokes a public control skill; internal or non-owning sessions must not overwrite `.farplane/state/current-run.json`. See `MEM-0029`.
- native Goal mode owns implementation persistence; stored `session_id` is a recovery hint only. See `MEM-0005`.
- stop-hook role configs are TOML-backed under `agents/*.toml`; load exact `developer_instructions` from TOML instead of relying on prompt-level agent-name loading. See `MEM-0010`.
- Stop-hook stdout is machine-only. When `bin/stop_hook.py` handles a `Stop` event, reserve stdout for one valid JSON payload and send notification fallbacks or diagnostics to stderr instead. See `MEM-0056`.
