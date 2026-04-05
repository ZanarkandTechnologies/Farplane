# `prompts/AGENTS.md`

Rules for tracked prompt files.

## Purpose

Prompt files in this folder are stable phase contracts for `codex exec` handoffs.

They should behave like function bodies:

- orchestrator passes runtime context
- prompt defines phase behavior
- worker exits after one bounded phase

## Keep Prompts

- phase-specific
- concise
- deterministic
- explicit about write-back targets
- explicit about the one final result line

## Do Not

- duplicate full system design docs
- mix multiple phases into one prompt
- hide orchestration policy inside ad-hoc prose
- make transcripts or sidecars the durable source of truth

## Required Inputs

Each `ralph*` prompt should expect:

- primary state file: `.ralph/state/current-run.json`
- optional overrides:
  - `RALPH_TICKET`
  - `RALPH_RUN_STATE`
  - `RALPH_EXECUTOR_TARGET`

The prompt should tell the worker to read state first and use env vars only as overrides.

## Required Output

Every phase prompt must require exactly one final result line:

`RALPH_RESULT: status=<enum> next=<enum> reason=<optional>`
