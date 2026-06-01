# `skills/impl/AGENTS.md`

Rules for the `impl` skill support files.

## Purpose

`skills/impl/` owns build-phase orchestration support, especially tmux-backed
lane visibility and recovery helpers.

## Keep

- orchestration support explicit
- runtime state lightweight
- lane ownership grouped in the runtime `claim` object
- delegated lane identity explicit via `worker_name`
- delegated main artifact explicit via `main_artifact_path`
- substantive delegated work grounded via `grounding_summary`
- delegated wait/backpressure visible via `worker_started_at`, `last_checkpoint_at`, and `checkpoint_summary`
- ticket mutations visible and intentional
- keep the `SKILL.md` Important Checklist as plain natural-language checklist text with Markdown links rather than a custom mini-language. See `MEM-0028` and `MEM-0124`.

## Do Not

- turn helper scripts into the primary control plane
- duplicate durable planning state outside tickets
- store raw transcript history in runtime claim data
