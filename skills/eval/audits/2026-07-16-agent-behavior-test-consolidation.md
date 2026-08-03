---
title: Agent Behavior Test consolidation
owner: skills/eval
status: implemented
kind: migration
updated_at: 2026-07-16
ticket: TASK-0384
---

# Agent Behavior Test consolidation

Eval `behavior_trace` now owns the former CLI capture contract: exact child
prompt, Codex JSONL events, stdout/stderr, final output, command/usage and
checkpoint scoring, artifact inventory, optional output-schema validation,
task detail, run summary, isolation, and baseline comparison.

The focused parity tests cover a complete trace and a candidate/baseline trace.
The standalone `agent-behavior-test` package is removed without an alias.

Native subagents do not expose the stable Codex CLI JSON event stream. When
Desktop tool access or an existing native role is the proof target, use
`agent-qa-test`; attach its tester report as evidence instead of pretending it
has CLI-event parity.
