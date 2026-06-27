---
title: "Taste Loop Controller Memory Hardening"
owner: taste-loop
status: complete
created_at: 2026-06-27
---

# Taste Loop Controller Memory Hardening

## Behavior Delta

Before: the active-hours loop could behave like an hourly dispatcher and write
no-op reports even when there was no useful work.

After: the loop treats Codex automation `memory.md` as the controller ledger,
reuses or resumes an active worker before creating a new one, and keeps
ordinary no-op beats side-effect free.

## Evidence

- `skills/taste-loop/SKILL.md` now defines the controller memory contract.
- `skills/taste-loop/templates/heartbeat-prompt.md` tells the runtime prompt to
  read automation memory, avoid `workers.jsonl`, and avoid no-op artifacts.
- `skills/taste-loop/eval_task.json` includes memory reuse, direct/related
  heat, and side-effect-free no-op reference points.
- `docs/features/FEAT-0064-skill-signals.md` defines direct heat plus related heat
  as reward-shaping signals with proxy-gaming penalties.

## Verdict

pass: source contract hardened. Runtime behavior still depends on the live
Codex heartbeat following the updated installed skill and prompt.
