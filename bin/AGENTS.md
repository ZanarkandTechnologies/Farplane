# `bin/AGENTS.md`

Rules for executable helper scripts in `bin/`.

## Purpose

Scripts here are small operational helpers for the live Codex harness.

## Keep Scripts

- explicit
- low-magic
- file-first
- easy to inspect and debug

## Do Not

- hide orchestration policy in shell tricks
- mutate ticket board state silently
- require network services unless the script is explicitly for that purpose

## Legacy Runtime Rules

For legacy runtime/prototype scripts that still carry older names:

- worker launcher runs exactly one bounded phase
- judge decides only from ticket + result + evidence state
- orchestrator composes worker + judge; it does not implement code itself
- tickets remain the canonical execution contract
- explicit ticket selectors outrank ambient run-state when both are present
- explicit run-state selectors outrank hook `session_id`, which outranks ambient `.harness/state/current-run.json`
- run-state files remain runtime-only and lightweight
- runtime state should group active execution ownership into a lightweight `claim` object instead of scattering claim semantics across multiple ad hoc top-level reads
- same-ticket `$impl` continuation must require both an explicit session-scoped loop gate and a matching runtime `claim`; tmux `auto_continue` is only lane follow-up plumbing, not the global activation truth. See `MEM-0025`.
- explicit `$impl` control-session turns must seed selected-ticket runtime ownership when ticket resolution is explicit or unambiguous; a session-only control stub is not enough for Stop-hook same-ticket continuation. See `MEM-0032`.
- bounded `$loop` runtime is session-owned, not ticket-owned: `bin/user_turn.py` seeds `skill_name: "loop"`, `loop_active`, and `loop_contract`, while `bin/stop_hook.py` evaluates only local deterministic predicates and explicit stop intent. Escape/cancel is not the canonical loop-stop contract. See `MEM-0038`.
- on completion-like paths, Stop-hook reviewer judgment is the authority for routing to the orchestrator; the main model's completion claim is candidate-only, and reviewer must fail completion when an obvious in-scope next step still remains. See `MEM-0034`.
- delegated workers should keep `worker_name`, `main_artifact_path`, and `grounding_summary` visible in the same runtime contract when available
- delegated stale-wait reads should stay advisory-first and use explicit checkpoint timing instead of hidden watchdog behavior
- current-turn user intent should be captured at `UserPromptSubmit` when available; worker-entry capture is fallback-only degraded mode
- canonical current-turn capture belongs only to control sessions whose first owned prompt explicitly invokes a public control skill; internal or non-owning sessions must not overwrite `.harness/state/current-run.json`. See `MEM-0029`.
- tmux lanes reuse a live interactive Codex pane before creating a replacement pane; stored `session_id` is the recovery path only. See `MEM-0005`.
- stop-hook role configs are TOML-backed under `agents/*.toml`; load exact `developer_instructions` from TOML instead of relying on prompt-level agent-name loading. See `MEM-0010`.
