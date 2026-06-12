---
date: 2026-06-12
change: initial-optimize-with-human
skill: optimize-with-human
---

# Initial Optimize With Human Audit

## Reason

Human feedback is a metric provider for optimization loops, not a standalone
autoresearch runtime. The previous name described a parameter but did not
clearly name the reusable operator task: optimize a target by asking Kenji for
fast labels, scores, rankings, or revision decisions.

## After

`optimize-with-human` owns feedback policy, Telegram-first request handoff,
feedback schema, and pause/resume protocol. `goal-advisor` owns Goal
architecture and native `/goal` prompt compilation, native Goal mode owns
continuation, and the Goal Packet owns durable state.
