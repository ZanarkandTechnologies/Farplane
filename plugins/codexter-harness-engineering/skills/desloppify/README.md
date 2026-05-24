# Desloppify Skill

## Purpose

Provide one public skill for `desloppify`-driven cleanup, with explicit behavior
for both the coordinating main agent and the delegated execution worker.
The main agent delegates. The worker executes. Nested Codex review runners are
handed back instead of recursing.

## Public API / Entrypoints

- `SKILL.md`: main workflow and mode selector
- `README.md`: module summary and test checklist
- `AGENTS.md`: maintenance notes
- `todos.md`: plain-language checklist for repeated cleanup passes

## Minimal Example

1. Trigger `desloppify` from the main session.
2. If this is the main agent, spawn one worker with an instruction like:

```text
Spawn a subagent to use the desloppify CLI for /repo/path.
Ref: desloppify skill subagent mode.
You are that delegated desloppify worker.
Do not spawn another worker.
Own install/update, exclude review, scan, next, fix, resolve, and periodic rescan.
Surface any non-obvious exclude candidate before excluding it.
If `desloppify` requires nested `review --run-batches --runner codex`, stop and report that blocker instead of running it.
Write progress back to <ticket-or-doc-path>.
```

3. In worker mode, run `pip install --upgrade "desloppify[full]"`.
4. Run `desloppify update-skill codex`.
5. Exclude obvious generated/vendor/runtime paths, but surface questionable
   ones before excluding.
6. Run `desloppify scan --path .`, then `desloppify next`, fix the current
   issue, run the resolve command shown by `next`, and repeat.
7. If the worker hits subjective review that requires nested Codex runner
   batches, stop and return that blocker to the main agent.

## How to Test

- Confirm `SKILL.md` defines both `main-agent mode` and `worker mode`.
- Confirm the worker handoff text explicitly says not to spawn another worker.
- Confirm worker mode explicitly stops instead of running nested
  `--runner codex` review batches.
- Confirm `.desloppify/` is ignored at the repo root.
- Confirm the docs inventory mentions the public skill.
- Confirm `todos.md` stays plain natural-language checklist text.
