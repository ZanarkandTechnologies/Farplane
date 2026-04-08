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
- run-state files remain runtime-only and lightweight
- tmux lanes reuse a live interactive Codex pane before creating a replacement pane; stored `session_id` is the recovery path only. See `MEM-0005`.
