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

## Ralph Prototype Rules

For `ralph` prototype scripts:

- worker launcher runs exactly one bounded phase
- judge decides only from ticket + result + evidence state
- orchestrator composes worker + judge; it does not implement code itself
- tickets remain the canonical execution contract
- explicit ticket selectors outrank ambient run-state when both are present
- explicit run-state selectors outrank hook `session_id`, which outranks ambient `.ralph/state/current-run.json` for runtime lane routing
- run-state files remain runtime-only and lightweight
- runtime state should group active execution ownership into a lightweight `claim` object instead of scattering claim semantics across multiple ad hoc top-level reads
- delegated workers should keep `worker_name`, `main_artifact_path`, and `grounding_summary` visible in the same runtime contract when available
- delegated stale-wait reads should stay advisory-first and use explicit checkpoint timing instead of hidden watchdog behavior
- current-turn user intent should be captured at `UserPromptSubmit` when available; worker-entry capture is fallback-only degraded mode
- tmux lanes reuse a live interactive Codex pane before creating a replacement pane; stored `session_id` is the recovery path only. See `MEM-0005`.
- stop-hook role configs are TOML-backed under `agents/*.toml`; load exact `developer_instructions` from TOML instead of relying on prompt-level agent-name loading. See `MEM-0010`.
